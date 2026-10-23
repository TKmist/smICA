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


"""Explicit command allowlist for smICA automation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable

from .automation_protocol import AutomationProtocolError


CommandHandler = Callable[[dict[str, Any]], Any]
ParameterValidator = Callable[[dict[str, Any]], dict[str, Any]]
_COMMAND_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")


def reject_all_parameters(parameters: dict[str, Any]) -> dict[str, Any]:
    """Validate a command that accepts no parameters."""

    if parameters:
        raise AutomationProtocolError(
            "INVALID_PARAMETERS",
            "This command does not accept parameters.",
            details={"fields": sorted(parameters)},
        )
    return {}


@dataclass(frozen=True)
class RegisteredAutomationCommand:
    """One public command and its validation contract."""

    name: str
    handler: CommandHandler
    validator: ParameterValidator
    description: str
    result_description: str
    gui_thread_required: bool

    def describe(self) -> dict[str, Any]:
        """Return public metadata without exposing the handler."""

        return {
            "name": self.name,
            "description": self.description,
            "result": self.result_description,
            "gui_thread_required": self.gui_thread_required,
        }


class AutomationCommandRegistry:
    """Store the unique public commands accepted by smICA."""

    def __init__(self) -> None:
        self._commands: dict[str, RegisteredAutomationCommand] = {}

    def register(
        self,
        name: str,
        handler: CommandHandler,
        *,
        validator: ParameterValidator = reject_all_parameters,
        description: str,
        result_description: str = "A JSON-compatible result object.",
        gui_thread_required: bool = True,
    ) -> None:
        """Register one command and reject accidental replacement."""

        if not isinstance(name, str) or _COMMAND_PATTERN.fullmatch(name) is None:
            raise ValueError("Command names must use lower-case dotted notation.")
        if name in self._commands:
            raise ValueError(f"Command already registered: {name}")
        if not callable(handler) or not callable(validator):
            raise TypeError("Command handler and validator must be callable.")
        self._commands[name] = RegisteredAutomationCommand(
            name=name,
            handler=handler,
            validator=validator,
            description=description,
            result_description=result_description,
            gui_thread_required=gui_thread_required,
        )

    def resolve(self, name: str) -> RegisteredAutomationCommand:
        """Return a registered command or a stable unknown-command error."""

        try:
            return self._commands[name]
        except KeyError as exc:
            raise AutomationProtocolError(
                "UNKNOWN_COMMAND",
                "The requested command is not registered.",
                details={"command": name},
            ) from exc

    def validate(
        self,
        command: RegisteredAutomationCommand,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        """Validate parameters and normalize validator failures."""

        try:
            normalized = command.validator(dict(parameters))
        except AutomationProtocolError:
            raise
        except (TypeError, ValueError) as exc:
            raise AutomationProtocolError(
                "INVALID_PARAMETERS",
                str(exc),
            ) from exc
        if not isinstance(normalized, dict):
            raise TypeError("A parameter validator must return a dictionary.")
        return normalized

    def names(self) -> list[str]:
        """Return command names in deterministic order."""

        return sorted(self._commands)

    def capabilities(self) -> list[dict[str, Any]]:
        """Return deterministic public command metadata."""

        return [self._commands[name].describe() for name in self.names()]
