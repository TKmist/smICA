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
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from smICA.Required.automation_client import AutomationClient
from smICA.Required.automation_dispatcher import GuiThreadAutomationDispatcher
from smICA.Required.automation_registry import AutomationCommandRegistry
from smICA.Required.automation_server import AutomationTCPServer


def encode_request(request_id="id", command="test.echo", parameters=None, token=None):
    value = {
        "protocol_version": 1,
        "request_id": request_id,
        "command": command,
        "parameters": parameters or {},
    }
    if token is not None:
        value["authentication_token"] = token
    return (json.dumps(value) + "\n").encode("utf-8")


class GuiPump:
    def __init__(self, *, queue_size=32):
        self.queue_size = queue_size
        self.ready = threading.Event()
        self.stop_requested = threading.Event()
        self.thread = threading.Thread(target=self._run, name="test-gui-thread")
        self.thread.start()
        assert self.ready.wait(2.0)

    def _run(self):
        registry = AutomationCommandRegistry()
        registry.register(
            "test.echo",
            lambda parameters: parameters,
            validator=lambda parameters: parameters,
            description="Echo.",
        )
        registry.register(
            "test.thread",
            lambda parameters: {"thread_id": threading.get_ident()},
            description="Thread identity.",
        )
        registry.register(
            "test.delay",
            lambda parameters: (time.sleep(parameters["seconds"]), {"done": True})[1],
            validator=lambda parameters: {"seconds": float(parameters["seconds"])},
            description="Delay.",
        )
        registry.register(
            "test.fail",
            lambda parameters: (_ for _ in ()).throw(RuntimeError("private details")),
            description="Fail inside a command handler.",
        )
        self.dispatcher = GuiThreadAutomationDispatcher(
            registry,
            queue_size=self.queue_size,
            owner_thread_id=threading.get_ident(),
        )
        self.thread_id = threading.get_ident()
        self.ready.set()
        while not self.stop_requested.is_set():
            self.dispatcher.process_pending(limit=4)
            self.stop_requested.wait(0.001)
        self.dispatcher.close()

    def close(self):
        self.stop_requested.set()
        self.thread.join(timeout=2.0)


@pytest.fixture
def running_server():
    pump = GuiPump()
    server = AutomationTCPServer(
        pump.dispatcher,
        port=0,
        read_timeout=0.5,
    )
    server.start()
    yield pump, server
    server.stop()
    pump.close()


def exchange(port, messages):
    with socket.create_connection(("127.0.0.1", port), timeout=2.0) as connection:
        stream = connection.makefile("rwb")
        for message in messages:
            stream.write(message)
            stream.flush()
        return [json.loads(stream.readline()) for _ in messages]


def test_fragmented_request_executes_on_gui_thread(running_server) -> None:
    pump, server = running_server
    payload = encode_request(command="test.thread")
    with socket.create_connection(("127.0.0.1", server.port), timeout=2.0) as connection:
        stream = connection.makefile("rwb")
        stream.write(payload[:9])
        stream.flush()
        stream.write(payload[9:])
        stream.flush()
        response = json.loads(stream.readline())
    assert response["ok"] is True
    assert response["result"]["command"] == "test.thread"
    assert response["result"]["value"]["thread_id"] == pump.thread_id


def test_multiple_requests_share_one_connection(running_server) -> None:
    _, server = running_server
    responses = exchange(
        server.port,
        [
            encode_request("one", parameters={"value": 1}),
            encode_request("two", parameters={"value": 2}),
        ],
    )
    assert [response["request_id"] for response in responses] == ["one", "two"]
    assert [response["result"]["value"]["value"] for response in responses] == [1, 2]


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        (b"{broken}\n", "MALFORMED_JSON"),
        (b"\xff\n", "INVALID_ENCODING"),
        (encode_request(command="missing.command"), "UNKNOWN_COMMAND"),
    ],
)
def test_server_returns_stable_protocol_errors(running_server, payload, code) -> None:
    _, server = running_server
    response = exchange(server.port, [payload])[0]
    assert response["ok"] is False
    assert response["error"]["code"] == code


def test_internal_error_identifies_failed_command(running_server) -> None:
    _, server = running_server
    response = exchange(
        server.port,
        [encode_request(command="test.fail")],
    )[0]
    assert response["ok"] is False
    assert response["error"]["code"] == "INTERNAL_ERROR"
    assert response["error"]["details"] == {"command": "test.fail"}
    assert "private details" not in json.dumps(response)


def test_oversized_request_closes_connection_after_error() -> None:
    pump = GuiPump()
    server = AutomationTCPServer(pump.dispatcher, port=0, max_request_bytes=256)
    server.start()
    try:
        response = exchange(server.port, [b"x" * 257 + b"\n"])[0]
        assert response["error"]["code"] == "REQUEST_TOO_LARGE"
    finally:
        server.stop()
        pump.close()


def test_authentication_success_and_failure() -> None:
    pump = GuiPump()
    server = AutomationTCPServer(
        pump.dispatcher,
        port=0,
        authentication_token="secret-value",
    )
    server.start()
    try:
        failed = exchange(server.port, [encode_request()])[0]
        passed = exchange(server.port, [encode_request(token="secret-value")])[0]
        assert failed["error"]["code"] == "AUTHENTICATION_FAILED"
        assert "secret-value" not in json.dumps(failed)
        assert passed["ok"] is True
    finally:
        server.stop()
        pump.close()


def test_concurrent_clients_receive_their_results(running_server) -> None:
    _, server = running_server

    def call(value):
        client = AutomationClient(port=server.port, timeout=2.0)
        return client.call("test.echo", {"value": value})

    with ThreadPoolExecutor(max_workers=8) as pool:
        responses = list(pool.map(call, range(12)))
    assert sorted(response["result"]["value"]["value"] for response in responses) == list(range(12))


def test_client_waits_for_gui_command_longer_than_connection_timeout() -> None:
    pump = GuiPump()
    server = AutomationTCPServer(pump.dispatcher, port=0)
    server.start()
    try:
        client = AutomationClient(port=server.port, timeout=0.02)
        response = client.call("test.delay", {"seconds": 0.1})
        assert response["ok"] is True
        assert response["result"]["value"] == {"done": True}
    finally:
        server.stop()
        pump.close()


def test_disconnect_does_not_stop_server(running_server) -> None:
    _, server = running_server
    connection = socket.create_connection(("127.0.0.1", server.port), timeout=2.0)
    connection.sendall(encode_request(parameters={"discard": True}))
    connection.close()
    time.sleep(0.03)
    response = exchange(server.port, [encode_request("after")])[0]
    assert response["ok"] is True


def test_graceful_stop_closes_listener(running_server) -> None:
    pump, server = running_server
    port = server.port
    server.stop()
    with pytest.raises(OSError):
        socket.create_connection(("127.0.0.1", port), timeout=0.1)
    assert pump.thread.is_alive()
