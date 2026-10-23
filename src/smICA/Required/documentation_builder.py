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


"""Build and publish the HTML documentation bundled with smICA."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile


JUPYTER_BOOK_REQUIREMENT = "jupyter-book==2.1.2"


def _absolute_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(os.fspath(path)))


def _remove_path(path: str) -> None:
    if os.path.islink(path) or os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def ensure_jupyter_book(
    python_executable: str | None = None,
    *,
    install_missing: bool = False,
) -> None:
    """Ensure that Jupyter Book is importable by the selected interpreter."""

    executable = python_executable or sys.executable
    import_check = subprocess.run(
        [executable, "-c", "import jupyter_book"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if import_check.returncode == 0:
        return
    if not install_missing:
        raise RuntimeError(
            f"{JUPYTER_BOOK_REQUIREMENT} is required to build the documentation."
        )
    subprocess.run(
        [
            executable,
            "-m",
            "pip",
            "install",
            JUPYTER_BOOK_REQUIREMENT,
            "--disable-pip-version-check",
        ],
        check=True,
    )


def _publish_directory(build_directory: str, target_directory: str) -> None:
    """Replace the bundled help only after a complete build is available."""

    target_parent = os.path.dirname(target_directory)
    os.makedirs(target_parent, exist_ok=True)
    staging_directory = tempfile.mkdtemp(
        prefix=".smica-help-staging-",
        dir=target_parent,
    )
    backup_directory = target_directory + ".previous"
    target_was_moved = False
    try:
        shutil.copytree(build_directory, staging_directory, dirs_exist_ok=True)
        _remove_path(backup_directory)
        if os.path.lexists(target_directory):
            os.replace(target_directory, backup_directory)
            target_was_moved = True
        try:
            os.replace(staging_directory, target_directory)
        except Exception:
            if target_was_moved and not os.path.lexists(target_directory):
                os.replace(backup_directory, target_directory)
            raise
        _remove_path(backup_directory)
    finally:
        _remove_path(staging_directory)


def build_documentation(
    source_directory: str,
    target_directory: str,
    *,
    python_executable: str | None = None,
    install_missing: bool = False,
) -> str:
    """Build all notebook pages and publish a clean bundled HTML directory."""

    source_directory = _absolute_path(source_directory)
    target_directory = _absolute_path(target_directory)
    configuration = os.path.join(source_directory, "myst.yml")
    if not os.path.isfile(configuration):
        raise FileNotFoundError(
            f"Jupyter Book configuration was not found: {configuration}"
        )

    executable = python_executable or sys.executable
    ensure_jupyter_book(executable, install_missing=install_missing)
    subprocess.run(
        [
            executable,
            "-m",
            "jupyter_book",
            "clean",
            "--html",
            "--site",
            "--temp",
            "--yes",
        ],
        cwd=source_directory,
        check=True,
    )
    subprocess.run(
        [executable, "-m", "jupyter_book", "build", "--html"],
        cwd=source_directory,
        check=True,
    )

    build_directory = os.path.join(source_directory, "_build", "html")
    index_file = os.path.join(build_directory, "index.html")
    if not os.path.isfile(index_file):
        raise RuntimeError(
            f"Jupyter Book did not create the expected file: {index_file}"
        )
    _publish_directory(build_directory, target_directory)
    return target_directory


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build and publish the HTML documentation bundled with smICA."
    )
    parser.add_argument("--source", required=True, help="Directory containing myst.yml")
    parser.add_argument("--target", required=True, help="Bundled HTML destination")
    parser.add_argument(
        "--install-missing",
        action="store_true",
        help="Install the pinned Jupyter Book dependency when it is unavailable.",
    )
    arguments = parser.parse_args(argv)
    target = build_documentation(
        arguments.source,
        arguments.target,
        install_missing=arguments.install_missing,
    )
    print(f"Documentation published to: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
