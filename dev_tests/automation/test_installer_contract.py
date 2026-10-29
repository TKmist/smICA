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
    assert 'if [ "\\${1:-}" = "--demo" ]; then' in source
    assert 'smICA/calc_tests/demo_data/run_demo.py' in source
    assert 'python "$PWD/smICA/calc_tests/unit_test/run_all.py"' in source
    assert "unity_test" not in source
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
    assert 'if "%%~1"=="--demo" goto RUN_DEMO' in source
    assert 'smICA\\calc_tests\\demo_data\\run_demo.py' in source
    assert "documentation_builder.py" in source
    assert '--source "docs"' in source
    assert '--target "src\\smICA\\doc\\assets\\help_html"' in source
    assert "smica-call.bat" in source
    assert "smICA.Required.automation_client" in source
    assert 'cd /d "%~dp0"' in source
    assert "An existing smICA installation was found" in source
    assert 'set "SMICA_INSTALLATION=%%~dp0"' in source
    assert 'set "SMICA_PYTHON=%%SMICA_INSTALLATION%%v_smICA_env\\Scripts\\python.exe"' in source
    assert "The smICA Python environment was not found" in source
    assert 'set "SMICA_TEST_RUNNER=%%SMICA_INSTALLATION%%smICA\\calc_tests\\unit_test\\run_all.py"' in source
    assert '"%%SMICA_PYTHON%%" "%%SMICA_TEST_RUNNER%%"' in source
    assert "The smICA application entry point was not found" in source
    assert "for /d %%d in (*) do (" in source
    assert "for /f \"delims=\" %%f in ('dir /b /a-d') do (" in source
    assert "Failed to move directory %%d to smICA" in source
    assert 'virtualenv --copies "%~dp0%VENV_DIR%"' in source
    assert 'attrib -r -s -h "python_embedded\\*" /s /d' in source
    assert "smICA Python environment verified:" in source
    assert 'set "SMICA_TEST_RUNNER=%%SMICA_INSTALLATION%%calc_tests\\unit_test\\run_all.py"' not in source
    assert "unity_test" not in source


def test_setup_installs_the_documentation_builder_dependency() -> None:
    setup_file = os.path.join(REPOSITORY_ROOT, "setup.py")
    with open(setup_file, encoding="utf-8") as setup_stream:
        source = setup_stream.read()
    assert '"jupyter-book==2.1.2"' in source
    assert "console_scripts" not in source
    assert "smica-call=smICA.Required.automation_client:main" not in source
    assert "SMICA_DOWNLOAD_READPTU_FLIM" not in source
    assert "urlretrieve" not in source


def test_installers_treat_readptu_as_an_optional_legacy_fallback() -> None:
    for filename in ("install.sh", "install_win.bat"):
        installer = os.path.join(REPOSITORY_ROOT, filename)
        with open(installer, encoding="utf-8") as installer_stream:
            source = installer_stream.read()

        assert "Optional legacy PTU reader: readPTU_FLIM.py" in source
        assert "smICA uses phconvert for supported PicoHarp 300 T3 files." in source
        assert "Only unsupported legacy PTU record types will be unavailable." in source
        assert "SMICA_DOWNLOAD_READPTU_FLIM" not in source
        assert "WILL NOT work correctly" not in source


def test_documentation_builder_allows_managed_node_installation() -> None:
    builder = os.path.join(
        REPOSITORY_ROOT,
        "src",
        "smICA",
        "Required",
        "documentation_builder.py",
    )
    with open(builder, encoding="utf-8") as builder_stream:
        source = builder_stream.read()
    assert 'JUPYTER_BOOK_NODEENV_PERMISSION = "JB_ALLOW_NODEENV"' in source
    assert 'build_environment[JUPYTER_BOOK_NODEENV_PERMISSION] = "1"' in source


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
