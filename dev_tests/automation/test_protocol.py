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

import pytest

from smICA.Required.automation_protocol import (
    AutomationProtocolError,
    decode_request,
    encode_response,
    error_response,
    success_response,
)


def request_bytes(**changes):
    value = {
        "protocol_version": 1,
        "request_id": "request-1",
        "command": "system.health",
        "parameters": {},
    }
    value.update(changes)
    return (json.dumps(value) + "\n").encode("utf-8")


def test_decode_valid_request() -> None:
    request = decode_request(request_bytes())
    assert request.request_id == "request-1"
    assert request.command == "system.health"
    assert request.parameters == {}


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        (b"\xff\n", "INVALID_ENCODING"),
        (b"{broken}\n", "MALFORMED_JSON"),
        (b'{"protocol_version":1,"protocol_version":1}\n', "MALFORMED_JSON"),
        (b'{"value":NaN}\n', "MALFORMED_JSON"),
        (b"{}", "INCOMPLETE_REQUEST"),
        (b"[]\n", "INVALID_ENVELOPE"),
        (request_bytes(protocol_version=2), "UNSUPPORTED_PROTOCOL_VERSION"),
        (request_bytes(command="bad command"), "INVALID_ENVELOPE"),
        (request_bytes(parameters=[]), "INVALID_ENVELOPE"),
        (request_bytes(extra=True), "INVALID_ENVELOPE"),
    ],
)
def test_decode_rejects_invalid_messages(payload: bytes, code: str) -> None:
    with pytest.raises(AutomationProtocolError) as raised:
        decode_request(payload)
    assert raised.value.code == code


def test_decode_enforces_encoded_size() -> None:
    with pytest.raises(AutomationProtocolError) as raised:
        decode_request(request_bytes(parameters={"text": "x" * 100}), max_request_bytes=64)
    assert raised.value.code == "REQUEST_TOO_LARGE"


def test_response_helpers_encode_one_line() -> None:
    success = success_response("id", {"ready": True})
    failure = error_response("id", "INVALID_PARAMETERS", "Invalid parameters.")
    assert json.loads(encode_response(success)) == success
    assert json.loads(encode_response(failure)) == failure
    assert encode_response(success).endswith(b"\n")
    assert encode_response(success).count(b"\n") == 1
