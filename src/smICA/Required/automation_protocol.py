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


"""Versioned newline-delimited JSON protocol for smICA automation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


PROTOCOL_VERSION = 1
DEFAULT_MAX_REQUEST_BYTES = 1024 * 1024
_COMMAND_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")
_REQUEST_FIELDS = {
    "protocol_version",
    "request_id",
    "command",
    "parameters",
    "authentication_token",
}


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"Non-standard JSON constant: {value}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON object field: {key}")
        result[key] = value
    return result


class AutomationProtocolError(Exception):
    """A stable protocol error that can be returned to a client."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        request_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.request_id = request_id
        self.details = details


@dataclass(frozen=True)
class AutomationRequest:
    """One validated version-1 request envelope."""

    request_id: str
    command: str
    parameters: dict[str, Any]
    authentication_token: str | None = None


def decode_request(
    raw_message: bytes,
    *,
    max_request_bytes: int = DEFAULT_MAX_REQUEST_BYTES,
    require_newline: bool = True,
) -> AutomationRequest:
    """Decode and validate one complete request line."""

    if len(raw_message) > max_request_bytes:
        raise AutomationProtocolError(
            "REQUEST_TOO_LARGE",
            "The request exceeds the configured size limit.",
        )
    if require_newline and not raw_message.endswith(b"\n"):
        raise AutomationProtocolError(
            "INCOMPLETE_REQUEST",
            "The request must end with a newline.",
        )
    payload = raw_message[:-1] if raw_message.endswith(b"\n") else raw_message
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AutomationProtocolError(
            "INVALID_ENCODING",
            "The request is not valid UTF-8.",
        ) from exc
    try:
        value = json.loads(
            text,
            parse_constant=_reject_json_constant,
            object_pairs_hook=_unique_object,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        details = {}
        if isinstance(exc, json.JSONDecodeError):
            details = {"line": exc.lineno, "column": exc.colno}
        raise AutomationProtocolError(
            "MALFORMED_JSON",
            "The request is not valid JSON.",
            details=details,
        ) from exc
    return validate_request(value)


def validate_request(value: Any) -> AutomationRequest:
    """Validate a decoded request without transport-specific behaviour."""

    if not isinstance(value, dict):
        raise AutomationProtocolError(
            "INVALID_ENVELOPE",
            "The request must be a JSON object.",
        )
    request_id = value.get("request_id")
    if not isinstance(request_id, str) or not request_id or len(request_id) > 128:
        raise AutomationProtocolError(
            "INVALID_ENVELOPE",
            "request_id must be a non-empty string of at most 128 characters.",
        )
    unknown_fields = sorted(set(value) - _REQUEST_FIELDS)
    if unknown_fields:
        raise AutomationProtocolError(
            "INVALID_ENVELOPE",
            "The request contains unknown fields.",
            request_id=request_id,
            details={"fields": unknown_fields},
        )
    if value.get("protocol_version") != PROTOCOL_VERSION:
        raise AutomationProtocolError(
            "UNSUPPORTED_PROTOCOL_VERSION",
            "The requested protocol version is not supported.",
            request_id=request_id,
            details={"supported_versions": [PROTOCOL_VERSION]},
        )
    command = value.get("command")
    if (
        not isinstance(command, str)
        or len(command) > 96
        or _COMMAND_PATTERN.fullmatch(command) is None
    ):
        raise AutomationProtocolError(
            "INVALID_ENVELOPE",
            "command must be a valid dotted command name.",
            request_id=request_id,
        )
    parameters = value.get("parameters")
    if not isinstance(parameters, dict):
        raise AutomationProtocolError(
            "INVALID_ENVELOPE",
            "parameters must be a JSON object.",
            request_id=request_id,
        )
    token = value.get("authentication_token")
    if token is not None and (
        not isinstance(token, str) or not token or len(token) > 4096
    ):
        raise AutomationProtocolError(
            "INVALID_ENVELOPE",
            "authentication_token must contain from 1 through 4096 characters.",
            request_id=request_id,
        )
    return AutomationRequest(request_id, command, dict(parameters), token)


def success_response(
    request_id: str,
    result: Any,
    *,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    """Build a successful response envelope."""

    response = {
        "protocol_version": PROTOCOL_VERSION,
        "request_id": request_id,
        "ok": True,
        "result": result,
    }
    if warnings:
        response["warnings"] = list(warnings)
    return response


def error_response(
    request_id: str | None,
    code: str,
    message: str,
    *,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an error response without exposing local tracebacks."""

    error = {"code": code, "message": message}
    if details:
        error["details"] = details
    return {
        "protocol_version": PROTOCOL_VERSION,
        "request_id": request_id or "unknown",
        "ok": False,
        "error": error,
    }


def encode_response(response: dict[str, Any]) -> bytes:
    """Encode one response as compact UTF-8 newline-delimited JSON."""

    return (
        json.dumps(
            response,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ) + "\n"
    ).encode("utf-8")
