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


"""Application-level lifecycle for smICA automation infrastructure."""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Any

from .automation_dispatcher import GuiThreadAutomationDispatcher
from .automation_protocol import PROTOCOL_VERSION
from .automation_registry import AutomationCommandRegistry
from .automation_server import AutomationTCPServer


class AutomationService:
    """Own the registry, GUI dispatcher and optional loopback server."""

    def __init__(
        self,
        *,
        application_version: str,
        state_provider: Callable[[], dict[str, Any]],
        shutdown_callback: Callable[[], None] | None = None,
        allow_remote_shutdown: bool = False,
        queue_size: int = 32,
        port: int = 8765,
        authentication_token: str | None = None,
        max_request_bytes: int = 1024 * 1024,
        read_timeout: float = 30.0,
    ) -> None:
        self.application_version = application_version.strip()
        self.state_provider = state_provider
        self.shutdown_callback = shutdown_callback
        self.allow_remote_shutdown = allow_remote_shutdown
        self.requested_port = port
        self.authentication_token = authentication_token
        self.max_request_bytes = max_request_bytes
        self.read_timeout = read_timeout
        self.registry = AutomationCommandRegistry()
        self.dispatcher = GuiThreadAutomationDispatcher(
            self.registry,
            queue_size=queue_size,
            owner_thread_id=threading.get_ident(),
        )
        self.server: AutomationTCPServer | None = None
        self._register_system_commands()

    def _register_system_commands(self) -> None:
        self.registry.register(
            "system.health",
            self._health,
            description="Report smICA automation readiness.",
            result_description="Application, protocol, thread and server status.",
        )
        self.registry.register(
            "system.version",
            self._version,
            description="Report smICA and protocol versions.",
        )
        self.registry.register(
            "system.capabilities",
            self._capabilities,
            description="List every registered public command.",
            result_description="Sorted command metadata.",
        )
        self.registry.register(
            "session.inspect",
            self._inspect_session,
            description="Inspect the current high-level application state.",
        )
        if self.allow_remote_shutdown and self.shutdown_callback is not None:
            self.registry.register(
                "system.shutdown",
                self._shutdown,
                description="Stop a test-controlled smICA process.",
            )

    def _health(self, parameters: dict[str, Any]) -> dict[str, Any]:
        return {
            "application": "smICA",
            "application_version": self.application_version,
            "protocol_version": PROTOCOL_VERSION,
            "ready": True,
            "features": {
                "batch_file_timing": True,
            },
            "server": self.status(),
            "execution_thread_id": threading.get_ident(),
        }

    def _version(self, parameters: dict[str, Any]) -> dict[str, Any]:
        return {
            "application_version": self.application_version,
            "protocol_version": PROTOCOL_VERSION,
        }

    def _capabilities(self, parameters: dict[str, Any]) -> dict[str, Any]:
        return {"commands": self.registry.capabilities()}

    def _inspect_session(self, parameters: dict[str, Any]) -> dict[str, Any]:
        return self.state_provider()

    def _shutdown(self, parameters: dict[str, Any]) -> dict[str, Any]:
        self.shutdown_callback()
        return {"shutdown_requested": True}

    def start(self, *, port: int | None = None) -> int:
        """Start the loopback listener or return its existing port."""

        if self.server is not None and self.server.running:
            return self.server.port
        selected_port = self.requested_port if port is None else port
        server = AutomationTCPServer(
            self.dispatcher,
            port=selected_port,
            authentication_token=self.authentication_token,
            max_request_bytes=self.max_request_bytes,
            read_timeout=self.read_timeout,
        )
        effective_port = server.start()
        self.server = server
        self.requested_port = selected_port
        return effective_port

    def stop(self) -> None:
        """Stop the listener while keeping the GUI dispatcher reusable."""

        server = self.server
        self.server = None
        if server is not None:
            server.stop()

    def close(self) -> None:
        """Stop the service and cancel commands still waiting in the queue."""

        self.stop()
        self.dispatcher.close()

    def process_pending(self, limit: int = 4) -> int:
        return self.dispatcher.process_pending(limit)

    def status(self) -> dict[str, Any]:
        server = self.server
        return {
            "running": bool(server is not None and server.running),
            "host": "127.0.0.1",
            "port": server.port if server is not None and server.running else None,
            "authentication_required": self.authentication_token is not None,
            "queued_commands": self.dispatcher.pending_count,
        }
