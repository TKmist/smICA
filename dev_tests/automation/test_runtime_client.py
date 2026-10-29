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

import json
import threading
import time

from smICA.Required.automation_client import AutomationClient, main
from smICA.Required.automation_runtime import AutomationService


def execute_with_gui_pump(service, client_call):
    result = {}

    def worker():
        try:
            result["value"] = client_call()
        except Exception as exc:
            result["error"] = exc

    thread = threading.Thread(target=worker)
    thread.start()
    deadline = time.monotonic() + 2.0
    while thread.is_alive() and time.monotonic() < deadline:
        service.process_pending(limit=4)
        thread.join(0.002)
    thread.join(timeout=0.1)
    if "error" in result:
        raise result["error"]
    return result["value"]


def test_service_system_commands_and_client(capsys) -> None:
    owner_thread = threading.get_ident()
    service = AutomationService(
        application_version="2.2.0",
        state_provider=lambda: {"mounted_method": None},
        port=0,
    )
    port = service.start()
    try:
        client = AutomationClient(port=port, timeout=1.0)
        health = execute_with_gui_pump(service, lambda: client.call("system.health"))
        assert health["result"]["value"]["ready"] is True
        assert health["result"]["value"]["features"]["batch_file_timing"] is True
        assert health["result"]["value"]["execution_thread_id"] == owner_thread
        capabilities = execute_with_gui_pump(
            service,
            lambda: client.call("system.capabilities"),
        )
        names = [item["name"] for item in capabilities["result"]["value"]["commands"]]
        assert names == sorted(names)
        assert "system.health" in names

        exit_code = execute_with_gui_pump(
            service,
            lambda: main(["--port", str(port), "system.version"]),
        )
        captured = capsys.readouterr()
        assert exit_code == 0
        cli_response = json.loads(captured.out)
        assert cli_response["ok"] is True
        assert cli_response["result"]["command"] == "system.version"
        assert ">>> Sending smICA command: system.version" in captured.err
    finally:
        service.close()


def test_remote_shutdown_is_disabled_by_default() -> None:
    service = AutomationService(
        application_version="test",
        state_provider=dict,
    )
    assert "system.shutdown" not in service.registry.names()
    service.close()
