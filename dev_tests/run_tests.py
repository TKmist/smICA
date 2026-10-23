#!/usr/bin/env python3

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


"""Run the repository-level pytest suite from any working directory.

Additional command-line arguments are forwarded to pytest. For example,
``python dev_tests/run_tests.py -q`` selects compact output.
"""

import os
import subprocess
import sys


SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
REPOSITORY_ROOT = os.path.dirname(SCRIPT_DIRECTORY)


def main() -> int:
    """Execute all developer tests and return the pytest exit status."""
    try:
        import pytest  # noqa: F401
    except ImportError:
        print(
            "pytest is required. Install it with: python -m pip install pytest",
            file=sys.stderr,
        )
        return 2

    command = [
        sys.executable,
        "-m",
        "pytest",
        SCRIPT_DIRECTORY,
        "-v",
        *sys.argv[1:],
    ]
    environment = os.environ.copy()
    source_paths = [
        os.path.join(REPOSITORY_ROOT, "src"),
        os.path.join(REPOSITORY_ROOT, "src", "smICA"),
    ]
    existing_pythonpath = environment.get("PYTHONPATH")
    if existing_pythonpath:
        source_paths.append(existing_pythonpath)
    environment["PYTHONPATH"] = os.pathsep.join(source_paths)
    return subprocess.call(command, cwd=REPOSITORY_ROOT, env=environment)


if __name__ == "__main__":
    raise SystemExit(main())
