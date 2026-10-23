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


from __future__ import annotations

import threading

import pytest

from smICA.Required.automation_dispatcher import (
    DispatchState,
    GuiThreadAutomationDispatcher,
)
from smICA.Required.automation_protocol import AutomationProtocolError
from smICA.Required.automation_registry import AutomationCommandRegistry


def make_registry() -> AutomationCommandRegistry:
    registry = AutomationCommandRegistry()
    registry.register(
        "test.echo",
        lambda parameters: parameters,
        validator=lambda parameters: parameters,
        description="Echo parameters.",
    )
    return registry


def test_registry_rejects_duplicates_and_unknown_commands() -> None:
    registry = make_registry()
    with pytest.raises(ValueError, match="already registered"):
        registry.register("test.echo", lambda parameters: None, description="Duplicate.")
    with pytest.raises(AutomationProtocolError) as raised:
        registry.resolve("test.missing")
    assert raised.value.code == "UNKNOWN_COMMAND"


def test_registry_capabilities_are_sorted_and_detached() -> None:
    registry = make_registry()
    registry.register("system.health", lambda parameters: {}, description="Health.")
    capabilities = registry.capabilities()
    assert [item["name"] for item in capabilities] == ["system.health", "test.echo"]
    capabilities[0]["name"] = "changed"
    assert registry.names()[0] == "system.health"


def test_dispatcher_executes_on_owner_thread() -> None:
    dispatcher = GuiThreadAutomationDispatcher(make_registry(), queue_size=2)
    pending = dispatcher.submit("test.echo", {"value": 7})
    assert dispatcher.process_pending(limit=1) == 1
    assert pending.finished.wait(0.1)
    assert pending.state is DispatchState.COMPLETED
    assert pending.result == {"value": 7}
    assert pending.execution_thread_id == threading.get_ident()


def test_dispatcher_rejects_processing_on_another_thread() -> None:
    dispatcher = GuiThreadAutomationDispatcher(make_registry())
    errors = []

    def process() -> None:
        try:
            dispatcher.process_pending()
        except Exception as exc:
            errors.append(exc)

    worker = threading.Thread(target=process)
    worker.start()
    worker.join()
    assert len(errors) == 1
    assert isinstance(errors[0], RuntimeError)


def test_dispatcher_queue_is_bounded() -> None:
    dispatcher = GuiThreadAutomationDispatcher(make_registry(), queue_size=1)
    dispatcher.submit("test.echo", {"value": 1})
    with pytest.raises(AutomationProtocolError) as raised:
        dispatcher.submit("test.echo", {"value": 2})
    assert raised.value.code == "QUEUE_FULL"


def test_dispatcher_close_cancels_queued_commands() -> None:
    dispatcher = GuiThreadAutomationDispatcher(make_registry())
    pending = dispatcher.submit("test.echo", {})
    dispatcher.close()
    assert pending.finished.wait(0.1)
    assert pending.state is DispatchState.CANCELLED
    with pytest.raises(AutomationProtocolError) as raised:
        dispatcher.submit("test.echo", {})
    assert raised.value.code == "DISPATCHER_CLOSED"


def test_handler_exception_maps_to_stable_internal_error() -> None:
    registry = AutomationCommandRegistry()

    def fail(parameters):
        raise RuntimeError("private traceback content")

    registry.register("test.fail", fail, description="Fail locally.")
    dispatcher = GuiThreadAutomationDispatcher(registry)
    pending = dispatcher.submit("test.fail", {})
    dispatcher.process_pending()
    assert pending.state is DispatchState.FAILED
    assert pending.error.code == "INTERNAL_ERROR"
    assert pending.error.details == {"command": "test.fail"}
    assert "test.fail" in pending.error.message
    assert "private traceback content" not in pending.error.message
