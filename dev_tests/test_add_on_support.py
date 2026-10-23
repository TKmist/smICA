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

import json
import os
import sys


REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIRECTORY = os.path.join(REPOSITORY_ROOT, "src")
if SOURCE_DIRECTORY not in sys.path:
    sys.path.insert(0, SOURCE_DIRECTORY)

from smICA.Required.mode_plugins import (  # noqa: E402
    discover_mode_directories,
    load_mode_definition,
    synchronize_repository_modes,
)


def _create_mode(parent_directory, name, complete=True):
    mode_directory = os.path.join(parent_directory, name)
    os.makedirs(mode_directory, exist_ok=True)
    definition = {
        "LAYOUT": "Example_layout.py",
        "INIT": "Example_INIT.py",
        "ANAL_MENU_ITEM": "Example_menu_item.py",
        "menu_class_func": "Example_menu_F",
    }
    with open(
        os.path.join(mode_directory, "Example_config.json"),
        "w",
        encoding="utf-8",
    ) as config_stream:
        json.dump(definition, config_stream)
    filenames = ["__init__.py", "Example_INIT.py", "Example_menu_item.py"]
    if complete:
        filenames.append("Example_layout.py")
    for filename in filenames:
        with open(
            os.path.join(mode_directory, filename),
            "w",
            encoding="utf-8",
        ) as source_stream:
            source_stream.write("# Test fixture.\n")
    return mode_directory


def test_mode_discovery_requires_every_declared_file(tmp_path):
    modes_directory = os.path.join(str(tmp_path), "Modes")
    valid = _create_mode(modes_directory, "Valid_mode")
    invalid = _create_mode(modes_directory, "Incomplete_mode", complete=False)

    assert load_mode_definition(valid) is not None
    assert load_mode_definition(invalid) is None
    assert discover_mode_directories(modes_directory) == [valid]


def test_updater_installs_official_modes_and_preserves_local_modes(tmp_path):
    root = str(tmp_path)
    repository_modes = os.path.join(root, "repository", "src", "smICA", "Modes")
    application_directory = os.path.join(root, "application")
    installed_modes = os.path.join(application_directory, "Modes")
    _create_mode(repository_modes, "Official_mode")
    _create_mode(repository_modes, "Incomplete_mode", complete=False)
    local_mode = _create_mode(installed_modes, "Local_mode")

    summary = synchronize_repository_modes(
        os.path.join(root, "repository"),
        application_directory,
    )

    assert summary == {
        "installed": ["Official_mode"],
        "updated": [],
        "skipped": ["Incomplete_mode"],
    }
    assert os.path.isdir(os.path.join(installed_modes, "Official_mode"))
    assert os.path.isdir(local_mode)

    second_summary = synchronize_repository_modes(
        os.path.join(root, "repository"),
        application_directory,
    )
    assert second_summary["updated"] == ["Official_mode"]
    assert os.path.isdir(local_mode)


def test_repository_template_satisfies_mode_contract():
    template_directory = os.path.join(
        REPOSITORY_ROOT,
        "templates",
        "add_on_template",
    )
    assert load_mode_definition(template_directory) is not None
