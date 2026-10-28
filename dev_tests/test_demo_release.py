from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEMO_DIRECTORY = REPOSITORY_ROOT / "calc_tests" / "demo_data"
RUN_DEMO = DEMO_DIRECTORY / "run_demo.py"


def load_demo_module() -> Any:
    specification = importlib.util.spec_from_file_location("smica_demo", RUN_DEMO)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class RecordingClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def call(self, command: str, parameters: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((command, parameters))
        return {"ok": True, "result": {}}


def test_demo_contains_four_partitioned_ptu_files_and_calibrations() -> None:
    in_vitro = sorted((DEMO_DIRECTORY / "in_vitro").rglob("*.ptu"))
    in_cellulo = sorted((DEMO_DIRECTORY / "in_cellulo").rglob("*.ptu"))
    assert len(in_vitro) == 2
    assert len(in_cellulo) == 2
    assert len(list(DEMO_DIRECTORY.rglob("*.ptu"))) == 4
    assert len(list(DEMO_DIRECTORY.rglob("calibration.json"))) == 4
    assert all("mrna" not in path.name.lower() for path in in_cellulo)
    assert {path.name for path in in_cellulo} == {
        "cell-108-01252-400nm_8.ptu",
        "cell-604-02105.ptu",
    }


def test_demo_analysis_uses_an_explicit_command_sequence() -> None:
    tree = ast.parse(RUN_DEMO.read_text(encoding="utf-8"))
    run_analysis = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "run_analysis"
    )
    assert not any(isinstance(node, (ast.For, ast.While)) for node in ast.walk(run_analysis))

    module = load_demo_module()
    client = RecordingClient()
    module.run_analysis(client, DEMO_DIRECTORY)

    commands = [command for command, _parameters in client.calls]
    assert commands.count("extract.apply_all") == 5
    assert commands.count("extract.open_filter_setup") == 4
    assert commands.count("extract.set_background_range") == 4
    assert commands.count("extract.calculate_filters") == 4
    assert commands.count("extract.accept_filters") == 4
    assert commands.count("extract.select_filter") == 4
    assert commands.count("extract.set_gate") == 0
    assert commands.count("phot2conc.load_calibration") == 5
    assert commands.count("phot2conc.export_results") == 5
    assert commands.count("phot2conc.calculate_all") == 2
    assert commands.count("phot2conc.calculate") == 3
    assert commands.count("phot2conc.add_result") == 3
    assert commands[0] == "system.health"

    statistical_filter_parameters = [
        parameters
        for command, parameters in client.calls
        if command == "extract.set_statistical_filter"
    ]
    assert statistical_filter_parameters == [
        {"channel": 1, "enabled": False},
        {"channel": 1, "enabled": False},
        {"channel": 1, "enabled": True},
        {"channel": 2, "enabled": True},
        {"channel": 1, "enabled": True},
        {"channel": 2, "enabled": True},
        {"channel": 1, "enabled": False},
        {"channel": 2, "enabled": False},
    ]

    selected_filters = [
        parameters
        for command, parameters in client.calls
        if command == "extract.select_filter"
    ]
    assert selected_filters == [
        {"channel": 1, "name": "Current decay; CH 1"},
        {"channel": 2, "name": "Current decay; CH 2"},
        {"channel": 1, "name": "Current decay; CH 1"},
        {"channel": 2, "name": "Current decay; CH 2"},
    ]

    exported_paths = [
        parameters["path"]
        for command, parameters in client.calls
        if command == "phot2conc.export_results"
    ]
    selected_cell_directory = (
        DEMO_DIRECTORY
        / "in_cellulo"
        / "cells_without_mrna"
        / "imaging_new_ptu"
    )
    assert str(selected_cell_directory / "results_tcspc.csv") in exported_paths
    assert str(selected_cell_directory / "results_gating.csv") in exported_paths

    tcspc_export_index = next(
        index
        for index, (command, parameters) in enumerate(client.calls)
        if command == "phot2conc.export_results"
        and parameters["path"] == str(selected_cell_directory / "results_tcspc.csv")
    )
    selected_cell_extraction_indices = [
        index
        for index, (command, parameters) in enumerate(client.calls)
        if command == "extract.load_directory"
        and parameters["directory"] == str(selected_cell_directory)
    ]
    gating_export_index = next(
        index
        for index, (command, parameters) in enumerate(client.calls)
        if command == "phot2conc.export_results"
        and parameters["path"] == str(selected_cell_directory / "results_gating.csv")
    )
    assert len(selected_cell_extraction_indices) == 2
    assert (
        selected_cell_extraction_indices[0]
        < tcspc_export_index
        < selected_cell_extraction_indices[1]
        < gating_export_index
    )


def test_demo_finds_the_application_in_a_source_checkout() -> None:
    module = load_demo_module()
    assert module.find_application() == REPOSITORY_ROOT / "src" / "smICA" / "smICA_tool.py"
