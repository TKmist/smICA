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


"""Small helpers shared by the standalone unit-test scripts."""

import os
import sys
import tempfile

import numpy as np


def prepare_imports():
    """Make smICA importable from a repository or an installed application."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    source = os.path.join(root, "src", "smICA")
    if not os.path.isdir(source):
        source = os.path.join(root, "smICA")

    sys.path.insert(0, os.path.dirname(source))
    sys.path.insert(0, source)
    os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())


def _format(value):
    """Format scalars and arrays consistently for a readable test report."""
    array = np.asarray(value)
    if array.ndim == 0:
        return str(array.item())
    return np.array2string(array, precision=8, suppress_small=False)


def _print_value(name, value):
    """Print multiline arrays as indented blocks instead of inline text."""
    formatted = _format(value)
    if "\n" not in formatted:
        print(f"    {name:<11} {formatted}")
        return

    print(f"    {name}")
    for line in formatted.splitlines():
        print(f"      {line}")


def report_close(label, expected, calculated, unit="", rtol=1e-7, atol=1e-12):
    """Print and validate a numerical comparison with explicit tolerances."""
    print(f"  {label}")
    _print_value("Expected:", expected)
    _print_value("Calculated:", calculated)
    if unit:
        print(f"    Unit:        {unit}")
    print(f"    Tolerance:  rtol={rtol:g}, atol={atol:g}")
    np.testing.assert_allclose(calculated, expected, rtol=rtol, atol=atol, equal_nan=True)
    print("    Result:     PASS")
    print()


def report_equal(label, expected, calculated, unit=""):
    """Print and validate an exact comparison."""
    print(f"  {label}")
    _print_value("Expected:", expected)
    _print_value("Calculated:", calculated)
    if unit:
        print(f"    Unit:        {unit}")
    print("    Tolerance:  exact match")
    np.testing.assert_array_equal(calculated, expected)
    print("    Result:     PASS")
    print()
