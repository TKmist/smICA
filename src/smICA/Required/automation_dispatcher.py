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


"""Bounded GUI-thread command dispatcher for smICA automation."""

from __future__ import annotations

import logging
import queue
import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .automation_protocol import AutomationProtocolError
from .automation_registry import AutomationCommandRegistry


LOGGER = logging.getLogger(__name__)


class DispatchState(str, Enum):
    """Lifecycle of a submitted command."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class PendingAutomationCommand:
    """A validated command waiting for the GUI thread."""

    command_id: str
    name: str
    parameters: dict[str, Any]
    state: DispatchState = DispatchState.QUEUED
    result: Any = None
    error: AutomationProtocolError | None = None
    execution_thread_id: int | None = None
    finished: threading.Event = field(default_factory=threading.Event)
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)


class GuiThreadAutomationDispatcher:
    """Execute registered commands only when drained by its owner thread."""

    def __init__(
        self,
        registry: AutomationCommandRegistry,
        *,
        queue_size: int = 32,
        owner_thread_id: int | None = None,
    ) -> None:
        if queue_size < 1:
            raise ValueError("queue_size must be at least 1")
        self.registry = registry
        self.queue_size = queue_size
        self.owner_thread_id = owner_thread_id or threading.get_ident()
        self._queue: queue.Queue[PendingAutomationCommand] = queue.Queue(queue_size)
        self._closed = False
        self._state_lock = threading.Lock()

    def submit(self, name: str, parameters: dict[str, Any]) -> PendingAutomationCommand:
        """Validate and enqueue one command without blocking the socket thread."""

        with self._state_lock:
            if self._closed:
                raise AutomationProtocolError(
                    "DISPATCHER_CLOSED",
                    "The automation dispatcher is shutting down.",
                )
        command = self.registry.resolve(name)
        normalized = self.registry.validate(command, parameters)
        pending = PendingAutomationCommand(
            command_id=uuid.uuid4().hex,
            name=name,
            parameters=normalized,
        )
        try:
            self._queue.put_nowait(pending)
        except queue.Full as exc:
            raise AutomationProtocolError(
                "QUEUE_FULL",
                "The automation request queue is full.",
                details={"capacity": self.queue_size},
            ) from exc
        return pending

    def process_pending(self, limit: int = 4) -> int:
        """Execute at most ``limit`` commands on the owner GUI thread."""

        if threading.get_ident() != self.owner_thread_id:
            raise RuntimeError("Automation commands must be processed on the GUI thread.")
        if limit < 1:
            return 0
        processed = 0
        while processed < limit:
            try:
                pending = self._queue.get_nowait()
            except queue.Empty:
                break
            try:
                self._execute(pending)
            finally:
                self._queue.task_done()
            processed += 1
        return processed

    def _execute(self, pending: PendingAutomationCommand) -> None:
        with pending.lock:
            if pending.state is DispatchState.CANCELLED:
                return
            pending.state = DispatchState.RUNNING
            pending.execution_thread_id = threading.get_ident()
        try:
            command = self.registry.resolve(pending.name)
            result = command.handler(dict(pending.parameters))
        except AutomationProtocolError as exc:
            details = dict(exc.details or {})
            details.setdefault("command", pending.name)
            with pending.lock:
                pending.error = AutomationProtocolError(
                    exc.code,
                    exc.message,
                    details=details,
                )
                pending.state = DispatchState.FAILED
        except Exception:
            LOGGER.exception("Unhandled automation command failure: %s", pending.name)
            with pending.lock:
                pending.error = AutomationProtocolError(
                    "INTERNAL_ERROR",
                    f"The command '{pending.name}' failed inside smICA. "
                    "See the local log for details.",
                    details={"command": pending.name},
                )
                pending.state = DispatchState.FAILED
        else:
            with pending.lock:
                pending.result = result
                pending.state = DispatchState.COMPLETED
        finally:
            pending.finished.set()

    def cancel(self, pending: PendingAutomationCommand) -> bool:
        """Cancel a queued command; running handlers are not interrupted."""

        with pending.lock:
            if pending.state is not DispatchState.QUEUED:
                return False
            pending.state = DispatchState.CANCELLED
            pending.error = AutomationProtocolError(
                "CANCELLED",
                "The queued command was cancelled.",
            )
            pending.finished.set()
            return True

    def close(self) -> None:
        """Reject new submissions and resolve every queued command."""

        with self._state_lock:
            self._closed = True
        while True:
            try:
                pending = self._queue.get_nowait()
            except queue.Empty:
                break
            try:
                self.cancel(pending)
            finally:
                self._queue.task_done()

    @property
    def pending_count(self) -> int:
        """Return the approximate number of queued commands."""

        return self._queue.qsize()
