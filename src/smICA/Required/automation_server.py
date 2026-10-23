# This file is part of the smICA repository that is distributed under the MIT license; see below.
#
#
# ############################################################################
#
# MIT License
#
# Copyright (c) 2026 Tomasz Kalwarczyk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""Loopback TCP transport for the smICA automation protocol."""

from __future__ import annotations

import hmac
import logging
import socket
import socketserver
import threading
from typing import Any

from .automation_dispatcher import GuiThreadAutomationDispatcher
from .automation_protocol import (
    AutomationProtocolError,
    DEFAULT_MAX_REQUEST_BYTES,
    decode_request,
    encode_response,
    error_response,
    success_response,
)


LOGGER = logging.getLogger(__name__)


class _AutomationTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class _AutomationRequestHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        """Process complete request lines until the client disconnects."""

        self.connection.settimeout(self.server.read_timeout)
        while True:
            try:
                raw_message = self.rfile.readline(self.server.max_request_bytes + 1)
            except socket.timeout:
                self._write_error(None, "READ_TIMEOUT", "Timed out while reading a request.")
                return
            if not raw_message:
                return
            if len(raw_message) > self.server.max_request_bytes:
                self._write_error(
                    None,
                    "REQUEST_TOO_LARGE",
                    "The request exceeds the configured size limit.",
                )
                return
            if not raw_message.endswith(b"\n"):
                self._write_error(
                    None,
                    "INCOMPLETE_REQUEST",
                    "The request must end with a newline.",
                )
                return
            response = self.server.command_server.handle_message(raw_message)
            if not self._write(response):
                return

    def _write_error(self, request_id: str | None, code: str, message: str) -> None:
        self._write(error_response(request_id, code, message))

    def _write(self, response: dict[str, Any]) -> bool:
        try:
            payload = encode_response(response)
        except (TypeError, ValueError):
            LOGGER.exception("Failed to serialize an automation response")
            payload = encode_response(
                error_response(
                    response.get("request_id"),
                    "INTERNAL_ERROR",
                    "smICA could not serialize the command result.",
                )
            )
        try:
            self.wfile.write(payload)
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            return False
        return True


class AutomationTCPServer:
    """Serve validated smICA commands on the IPv4 loopback interface."""

    def __init__(
        self,
        dispatcher: GuiThreadAutomationDispatcher,
        *,
        host: str = "127.0.0.1",
        port: int = 8765,
        authentication_token: str | None = None,
        max_request_bytes: int = DEFAULT_MAX_REQUEST_BYTES,
        read_timeout: float = 30.0,
    ) -> None:
        if host != "127.0.0.1":
            raise ValueError("The automation server may bind only to 127.0.0.1.")
        if isinstance(port, bool) or not isinstance(port, int) or not 0 <= port <= 65535:
            raise ValueError("port must be an integer from 0 through 65535")
        if max_request_bytes < 256:
            raise ValueError("max_request_bytes must be at least 256")
        if read_timeout <= 0:
            raise ValueError("read_timeout must be positive")
        self.dispatcher = dispatcher
        self.host = host
        self.port = port
        self.authentication_token = authentication_token
        self.max_request_bytes = max_request_bytes
        self.read_timeout = float(read_timeout)
        self._server: _AutomationTCPServer | None = None
        self._thread: threading.Thread | None = None
        self._lifecycle_lock = threading.Lock()

    def start(self) -> int:
        """Start the listener and return the effective port."""

        with self._lifecycle_lock:
            if self._server is not None:
                return self.port
            server = _AutomationTCPServer(
                (self.host, self.port),
                _AutomationRequestHandler,
            )
            server.command_server = self
            server.max_request_bytes = self.max_request_bytes
            server.read_timeout = self.read_timeout
            self.port = int(server.server_address[1])
            thread = threading.Thread(
                target=server.serve_forever,
                name="smICA-automation-listener",
                daemon=True,
            )
            self._server = server
            self._thread = thread
            thread.start()
            return self.port

    def stop(self) -> None:
        """Stop accepting requests and close the listening socket."""

        with self._lifecycle_lock:
            server = self._server
            thread = self._thread
            self._server = None
            self._thread = None
        if server is None:
            return
        server.shutdown()
        server.server_close()
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=2.0)

    @property
    def running(self) -> bool:
        return self._server is not None

    def handle_message(self, raw_message: bytes) -> dict[str, Any]:
        """Validate, authenticate, dispatch and await one request."""

        request_id = None
        request_command = None
        try:
            request = decode_request(
                raw_message,
                max_request_bytes=self.max_request_bytes,
            )
            request_id = request.request_id
            request_command = request.command
            LOGGER.info(
                "Automation command received: %s (request_id=%s)",
                request.command,
                request.request_id,
            )
            self._authenticate(request.authentication_token, request.request_id)
            pending = self.dispatcher.submit(request.command, request.parameters)
            # Native GUI callbacks may legitimately run for hours and cannot be
            # cancelled safely after they have started. Wait until the GUI
            # thread reports a real result instead of guessing a duration.
            pending.finished.wait()
            if pending.error is not None:
                raise AutomationProtocolError(
                    pending.error.code,
                    pending.error.message,
                    request_id=request.request_id,
                    details=pending.error.details,
                )
            return success_response(
                request.request_id,
                {
                    "command": request.command,
                    "command_id": pending.command_id,
                    "value": pending.result,
                },
            )
        except AutomationProtocolError as exc:
            details = dict(exc.details or {})
            if request_command is not None:
                details.setdefault("command", request_command)
            return error_response(
                exc.request_id or request_id,
                exc.code,
                exc.message,
                details=details or None,
            )
        except Exception:
            LOGGER.exception(
                "Unhandled automation transport failure for command: %s",
                request_command or "unknown",
            )
            return error_response(
                request_id,
                "INTERNAL_ERROR",
                "The request failed inside smICA. See the local log for details.",
                details=(
                    {"command": request_command}
                    if request_command is not None
                    else None
                ),
            )

    def _authenticate(self, supplied: str | None, request_id: str) -> None:
        if self.authentication_token is None:
            return
        if supplied is None or not hmac.compare_digest(
            supplied,
            self.authentication_token,
        ):
            raise AutomationProtocolError(
                "AUTHENTICATION_FAILED",
                "Authentication failed.",
                request_id=request_id,
            )
