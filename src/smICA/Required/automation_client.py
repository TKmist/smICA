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


"""Command-line client for the local smICA automation server."""

from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import uuid
from typing import Any

from .automation_protocol import PROTOCOL_VERSION


DEFAULT_RESPONSE_LIMIT = 16 * 1024 * 1024


class AutomationClientError(Exception):
    """A local connection or response failure."""


class AutomationClient:
    """Send versioned requests to one running smICA process."""

    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 8765,
        timeout: float = 30.0,
        authentication_token: str | None = None,
        response_limit: int = DEFAULT_RESPONSE_LIMIT,
    ) -> None:
        if host != "127.0.0.1":
            raise ValueError("The client connects only to 127.0.0.1.")
        if not 0 < port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.host = host
        self.port = port
        self.connection_timeout = timeout
        self.authentication_token = authentication_token
        self.response_limit = response_limit

    def call(self, command: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        request = {
            "protocol_version": PROTOCOL_VERSION,
            "request_id": f"cli-{uuid.uuid4().hex}",
            "command": command,
            "parameters": dict(parameters or {}),
        }
        if self.authentication_token is not None:
            request["authentication_token"] = self.authentication_token
        payload = (
            json.dumps(request, ensure_ascii=False, separators=(",", ":")) + "\n"
        ).encode("utf-8")
        try:
            with socket.create_connection(
                (self.host, self.port),
                timeout=self.connection_timeout,
            ) as connection:
                # The timeout protects connection establishment only. Once a
                # command is accepted, wait for the native GUI callback to
                # finish regardless of the dataset size or processing time.
                connection.settimeout(None)
                connection.sendall(payload)
                stream = connection.makefile("rb")
                raw_response = stream.readline(self.response_limit + 1)
        except OSError as exc:
            raise AutomationClientError(f"Connection failed: {exc}") from exc
        if not raw_response:
            raise AutomationClientError("smICA closed the connection without a response.")
        if len(raw_response) > self.response_limit:
            raise AutomationClientError("The response exceeds the client size limit.")
        if not raw_response.endswith(b"\n"):
            raise AutomationClientError("smICA returned an incomplete response.")
        try:
            response = json.loads(raw_response.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AutomationClientError("smICA returned invalid JSON.") from exc
        if not isinstance(response, dict):
            raise AutomationClientError("smICA returned a non-object response.")
        if response.get("protocol_version") != PROTOCOL_VERSION:
            raise AutomationClientError("smICA returned an unsupported protocol version.")
        if response.get("request_id") != request["request_id"]:
            raise AutomationClientError("smICA returned a mismatched request_id.")
        return response


def _load_token(token_file: str | None) -> str | None:
    if token_file:
        token_path = os.path.abspath(os.path.expanduser(token_file))
        with open(token_path, encoding="utf-8") as token_stream:
            token = token_stream.read().strip()
    else:
        token = os.environ.get("SMICA_AUTOMATION_TOKEN", "").strip()
    if token_file and not token:
        raise ValueError("The authentication token file is empty.")
    return token or None


def _parse_parameters(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("parameters must be valid JSON") from exc
    if not isinstance(value, dict):
        raise ValueError("parameters must be a JSON object")
    return value


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smica-call",
        description="Send one command to a running smICA automation server.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=os.environ.get("SMICA_AUTOMATION_PORT", "8765"),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Connection timeout in seconds; command execution has no timeout.",
    )
    parser.add_argument("--token-file")
    parser.add_argument("command", help="Public command name, for example system.health")
    parser.add_argument("parameters", nargs="?", default="{}", help="JSON parameter object")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    try:
        arguments = parser.parse_args(argv)
        parameters = _parse_parameters(arguments.parameters)
        token = _load_token(arguments.token_file)
        client = AutomationClient(
            port=arguments.port,
            timeout=arguments.timeout,
            authentication_token=token,
        )
        print(
            f">>> Sending smICA command: {arguments.command}",
            file=sys.stderr,
            flush=True,
        )
        response = client.call(arguments.command, parameters)
    except (AutomationClientError, OSError, ValueError) as exc:
        print(f"smica-call: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(response, indent=2, ensure_ascii=False), flush=True)
    return 0 if response.get("ok") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
