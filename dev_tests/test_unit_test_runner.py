# This file is part of the smICA repository that is distributed under the MIT license.

"""Regression tests for the standalone calculation unit test runner."""

import importlib.util
import os


REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNER_PATH = os.path.join(REPOSITORY_ROOT, "calc_tests", "unit_test", "run_all.py")


def load_runner():
    """Load the runner as a module without executing its test suite."""
    specification = importlib.util.spec_from_file_location("smica_unit_test_runner", RUNNER_PATH)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def test_importing_runner_does_not_start_subprocesses(monkeypatch) -> None:
    def fail_if_called(*args, **kwargs):
        raise AssertionError("Importing run_all.py started a subprocess")

    monkeypatch.setattr("subprocess.run", fail_if_called)
    load_runner()


def test_runner_discovers_only_executable_test_scripts() -> None:
    runner = load_runner()
    test_directory = os.path.dirname(RUNNER_PATH)

    discovered_names = [
        os.path.basename(path) for path in runner.discover_test_files(test_directory)
    ]

    assert discovered_names == [
        "test_frame_data.py",
        "test_phot2conc_math.py",
        "test_roi_mask.py",
        "test_weighted_lifetime.py",
    ]
