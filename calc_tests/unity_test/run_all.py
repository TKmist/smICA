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


"""Run every standalone smICA unit-test script."""

import os
import subprocess
import sys


test_directory = os.path.dirname(os.path.abspath(__file__))
test_files = sorted(
    os.path.join(test_directory, name)
    for name in os.listdir(test_directory)
    if name.startswith("test_") and name.endswith(".py") and name != "test_support.py"
)

for test_file in test_files:
    print("=" * 72, flush=True)
    print(f"Running {os.path.basename(test_file)}", flush=True)
    print("=" * 72, flush=True)
    subprocess.run([sys.executable, "-B", test_file], check=True)
    print(flush=True)

print("=" * 72)
print(f"FINAL RESULT: all {len(test_files)} unit-test scripts passed.")
