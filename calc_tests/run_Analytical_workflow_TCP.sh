#!/usr/bin/env bash

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


# Execute the TCP analytical workflow stored in the accompanying text file.

set -euo pipefail

SCRIPT_DIRECTORY="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COMMAND_FILE="$SCRIPT_DIRECTORY/Analytical_workflow_TCP_commands.txt"
SMICA_INSTALLATION="${1:-${SMICA_HOME:-}}"

if [[ ! -r "$COMMAND_FILE" ]]; then
    printf 'Command file is not readable: %s\n' "$COMMAND_FILE" >&2
    exit 1
fi

resolve_smica_call() {
    if [[ -n "${SMICA_CALL:-}" ]]; then
        if [[ -x "$SMICA_CALL" ]]; then
            printf '%s\n' "$SMICA_CALL"
            return 0
        fi
        printf 'SMICA_CALL does not identify an executable file: %s\n' "$SMICA_CALL" >&2
        return 1
    fi

    if [[ -n "$SMICA_INSTALLATION" ]]; then
        local installation_candidate
        local installation_candidates=(
            "$SMICA_INSTALLATION/v_smICA_env/bin/smica-call"
            "$SMICA_INSTALLATION/bin/smica-call"
        )
        for installation_candidate in "${installation_candidates[@]}"; do
            if [[ -x "$installation_candidate" ]]; then
                printf '%s\n' "$installation_candidate"
                return 0
            fi
        done
        printf 'The selected smICA installation does not contain smica-call: %s\n' \
            "$SMICA_INSTALLATION" >&2
        return 1
    fi

    local path_client
    path_client="$(type -P smica-call || true)"
    if [[ -n "$path_client" ]]; then
        printf '%s\n' "$path_client"
        return 0
    fi

    local candidate
    local candidates=(
        "$SCRIPT_DIRECTORY/../../v_smICA_env/bin/smica-call"
        "$SCRIPT_DIRECTORY/../v_smICA_env/bin/smica-call"
    )
    for candidate in "${candidates[@]}"; do
        if [[ -x "$candidate" ]]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    printf '%s\n' 'Cannot locate smica-call.' >&2
    printf '%s\n' 'Pass the smICA installation directory as the first argument:' >&2
    printf '%s\n' '  ./run_Analytical_workflow_TCP.sh /path/to/smICA-installation' >&2
    return 1
}

SMICA_CALL_EXECUTABLE="$(resolve_smica_call)"
export SMICA_CALL_EXECUTABLE
PYTHON_EXECUTABLE="$(dirname "$SMICA_CALL_EXECUTABLE")/python"
export PYTHON_EXECUTABLE

# Export the command expected by Analytical_workflow_TCP_commands.txt.
smica-call() {
    "$SMICA_CALL_EXECUTABLE" "$@"
}
export -f smica-call

printf 'Running commands from: %s\n' "$COMMAND_FILE"
printf 'TCP client: %s\n' "$SMICA_CALL_EXECUTABLE"
printf 'TCP port: %s\n' "${SMICA_AUTOMATION_PORT:-8765}"

# The command file uses "set -e", so execution stops at the first failed TCP call.
exec bash "$COMMAND_FILE"
