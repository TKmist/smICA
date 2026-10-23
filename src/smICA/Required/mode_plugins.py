'''
This file is part of the smICA repository that is distributed under the MIT license; see below.


############################################################################

MIT License

Copyright (c) 2026 Tomasz Kalwarczyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import json
import os
import shutil


MODE_CONFIG_SUFFIX = "_config.json"
MODE_CONFIG_KEYS = ("LAYOUT", "INIT", "ANAL_MENU_ITEM", "menu_class_func")


def load_mode_definition(mode_directory):
    """Return a validated analytical-mode definition or ``None``."""
    if not os.path.isdir(mode_directory):
        return None

    config_files = sorted(
        filename
        for filename in os.listdir(mode_directory)
        if filename.endswith(MODE_CONFIG_SUFFIX)
    )
    if len(config_files) != 1:
        return None

    config_path = os.path.join(mode_directory, config_files[0])
    try:
        with open(config_path, encoding="utf-8") as config_stream:
            definition = json.load(config_stream)
    except (OSError, ValueError, TypeError):
        return None

    if not isinstance(definition, dict):
        return None
    if any(not isinstance(definition.get(key), str) for key in MODE_CONFIG_KEYS):
        return None
    if any(not definition[key].strip() for key in MODE_CONFIG_KEYS):
        return None

    for key in ("LAYOUT", "INIT", "ANAL_MENU_ITEM"):
        filename = definition[key]
        if os.path.basename(filename) != filename:
            return None
        if not os.path.isfile(os.path.join(mode_directory, filename)):
            return None

    if not os.path.isfile(os.path.join(mode_directory, "__init__.py")):
        return None

    return definition


def discover_mode_directories(modes_directory):
    """Find complete analytical modes in deterministic directory order."""
    if not os.path.isdir(modes_directory):
        return []

    return [
        os.path.join(modes_directory, name)
        for name in sorted(os.listdir(modes_directory))
        if load_mode_definition(os.path.join(modes_directory, name)) is not None
    ]


def synchronize_repository_modes(repository_root, application_directory):
    """Install or update valid repository modes without removing local ones."""
    source_directory = os.path.join(repository_root, "src", "smICA", "Modes")
    target_directory = os.path.join(application_directory, "Modes")
    summary = {"installed": [], "updated": [], "skipped": []}

    if not os.path.isdir(source_directory):
        return summary

    os.makedirs(target_directory, exist_ok=True)
    valid_sources = set(discover_mode_directories(source_directory))

    for name in sorted(os.listdir(source_directory)):
        source = os.path.join(source_directory, name)
        if not os.path.isdir(source):
            continue
        if source not in valid_sources:
            summary["skipped"].append(name)
            continue

        target = os.path.join(target_directory, name)
        action = "updated" if os.path.isdir(target) else "installed"
        shutil.copytree(
            source,
            target,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", ".ipynb_checkpoints"),
        )
        summary[action].append(name)

    return summary
