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

import os
import subprocess

import pytest

from smICA.Required import documentation_builder


def test_build_documentation_replaces_stale_help(monkeypatch, tmp_path) -> None:
    source_directory = os.path.join(os.fspath(tmp_path), "docs")
    target_directory = os.path.join(os.fspath(tmp_path), "help_html")
    os.makedirs(source_directory)
    os.makedirs(target_directory)
    with open(os.path.join(source_directory, "myst.yml"), "w", encoding="utf-8") as stream:
        stream.write("version: 1\n")
    with open(os.path.join(target_directory, "stale.html"), "w", encoding="utf-8") as stream:
        stream.write("stale")

    commands = []

    def fake_run(command, **kwargs):
        commands.append((command, kwargs))
        if "build" in command:
            build_directory = os.path.join(source_directory, "_build", "html")
            os.makedirs(build_directory, exist_ok=True)
            with open(os.path.join(build_directory, "index.html"), "w", encoding="utf-8") as stream:
                stream.write("current")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(documentation_builder.subprocess, "run", fake_run)
    result = documentation_builder.build_documentation(
        source_directory,
        target_directory,
        python_executable="python-for-test",
    )

    assert result == os.path.abspath(target_directory)
    assert os.path.isfile(os.path.join(target_directory, "index.html"))
    assert not os.path.exists(os.path.join(target_directory, "stale.html"))
    assert commands[0][0] == ["python-for-test", "-c", "import jupyter_book"]
    assert commands[1][0][-5:] == ["clean", "--html", "--site", "--temp", "--yes"]
    assert commands[2][0][-2:] == ["build", "--html"]


def test_build_documentation_requires_myst_configuration(tmp_path) -> None:
    with pytest.raises(FileNotFoundError, match="myst.yml"):
        documentation_builder.build_documentation(
            os.path.join(os.fspath(tmp_path), "missing-docs"),
            os.path.join(os.fspath(tmp_path), "help_html"),
        )
