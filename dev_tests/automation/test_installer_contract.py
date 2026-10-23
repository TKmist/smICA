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
import stat
import subprocess


REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_linux_installer_exists_is_executable_and_forwards_launcher_arguments() -> None:
    installer = os.path.join(REPOSITORY_ROOT, "install.sh")
    assert os.path.isfile(installer)
    assert os.stat(installer).st_mode & stat.S_IXUSR
    with open(installer, encoding="utf-8") as installer_stream:
        source = installer_stream.read()
    assert 'python "$PWD/smICA/smICA/smICA_tool.py" "\\$@"' in source
    assert "run_smICA --automation-server" in source
    assert "documentation_builder.py" in source
    assert "--source docs" in source
    assert "--target src/smICA/doc/assets/help_html" in source
    assert 'bin/smica-call"' in source
    assert "smICA.Required.automation_client" in source


def test_windows_installer_forwards_launcher_arguments() -> None:
    installer = os.path.join(REPOSITORY_ROOT, "install_win.bat")
    assert os.path.isfile(installer)
    with open(installer, encoding="utf-8") as installer_stream:
        source = installer_stream.read()
    assert "%*" in source
    assert "--automation-server" in source
    assert "documentation_builder.py" in source
    assert '--source "docs"' in source
    assert '--target "src\\smICA\\doc\\assets\\help_html"' in source
    assert "smica-call.bat" in source
    assert "smICA.Required.automation_client" in source


def test_setup_installs_the_documentation_builder_dependency() -> None:
    setup_file = os.path.join(REPOSITORY_ROOT, "setup.py")
    with open(setup_file, encoding="utf-8") as setup_stream:
        source = setup_stream.read()
    assert '"jupyter-book==2.1.2"' in source
    assert "console_scripts" not in source
    assert "smica-call=smICA.Required.automation_client:main" not in source


def test_repository_has_no_project_owned_executable_binaries() -> None:
    tracked_files = subprocess.check_output(
        ["git", "ls-files"],
        cwd=REPOSITORY_ROOT,
        text=True,
    ).splitlines()
    executable_binary_extensions = (".exe", ".dll", ".pyd", ".so", ".bin")
    unexpected_binaries = [
        path
        for path in tracked_files
        if path.lower().endswith(executable_binary_extensions)
        and not path.startswith("python_embedded/")
    ]
    assert unexpected_binaries == []


def test_updater_rebuilds_bundled_documentation() -> None:
    updater_file = os.path.join(
        REPOSITORY_ROOT,
        "src",
        "smICA",
        "Required",
        "INIT.py",
    )
    with open(updater_file, encoding="utf-8") as updater_stream:
        source = updater_stream.read()
    assert "build_documentation(" in source
    assert "install_missing=True" in source


def test_reference_workflows_accept_an_installation_directory() -> None:
    linux_workflow = os.path.join(
        REPOSITORY_ROOT,
        "calc_tests",
        "run_Analytical_workflow_TCP.sh",
    )
    windows_workflow = os.path.join(
        REPOSITORY_ROOT,
        "calc_tests",
        "run_Analytical_workflow_TCP.bat",
    )
    with open(linux_workflow, encoding="utf-8") as workflow_stream:
        linux_source = workflow_stream.read()
    with open(windows_workflow, encoding="utf-8") as workflow_stream:
        windows_source = workflow_stream.read()

    assert 'SMICA_INSTALLATION="${1:-${SMICA_HOME:-}}"' in linux_source
    assert '"$SMICA_INSTALLATION/v_smICA_env/bin/smica-call"' in linux_source
    assert 'set "SMICA_INSTALLATION=%~1"' in windows_source
    assert "%SMICA_INSTALLATION%\\v_smICA_env\\Scripts\\activate.bat" in windows_source
    assert "poligon" not in linux_source.lower()
    assert "poligon" not in windows_source.lower()


def test_release_builders_use_root_installers_and_include_docs() -> None:
    for filename in ("build_release.sh", "build_release_with_docs.sh"):
        script = os.path.join(REPOSITORY_ROOT, ".scripts", filename)
        with open(script, encoding="utf-8") as script_stream:
            source = script_stream.read()

        assert '$ROOT_DIR/install.sh' in source
        assert '$ROOT_DIR/install_win.bat' in source
        assert "scripts/linux/install.sh" not in source
        assert "scripts/windows/install_win.bat" not in source
        assert "copy_documentation_sources" in source
        assert 'destination="$1/docs"' in source
