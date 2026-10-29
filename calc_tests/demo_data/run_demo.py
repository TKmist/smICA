#!/usr/bin/env python3
"""Run the bundled smICA demonstration from PTU extraction to concentration."""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


DEMO_DIRECTORY = Path(__file__).resolve().parent
DEXTRAN_60_DIRECTORY = DEMO_DIRECTORY / "in_vitro" / "dextran_60nm"
DEXTRAN_80_DIRECTORY = DEMO_DIRECTORY / "in_vitro" / "dextran_80nm"
CELL_NEW_DIRECTORY = DEMO_DIRECTORY / "in_cellulo" / "cells_without_mrna" / "imaging_new_ptu"
CELL_IMAGING2_DIRECTORY = DEMO_DIRECTORY / "in_cellulo" / "cells_without_mrna" / "imaging2_17_07_23"


class DemoError(RuntimeError):
    """An actionable demo execution failure."""


def send_command(client: Any, command: str, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
    """Print and execute one explicit smICA automation command."""

    request_parameters = dict(parameters or {})
    print(f"\n>>> {command} {json.dumps(request_parameters, ensure_ascii=False)}", flush=True)
    response = client.call(command, request_parameters)
    if response.get("ok") is not True:
        raise DemoError(
            f"Command {command!r} failed:\n"
            f"{json.dumps(response, indent=2, ensure_ascii=False)}"
        )
    print("    OK", flush=True)
    return response


def run_analysis(client: Any, demo_directory: Path = DEMO_DIRECTORY) -> None:
    """Execute the complete demonstration as an intentionally explicit command list."""

    dextran_60 = demo_directory / "in_vitro" / "dextran_60nm"
    dextran_80 = demo_directory / "in_vitro" / "dextran_80nm"
    cell_new = demo_directory / "in_cellulo" / "cells_without_mrna" / "imaging_new_ptu"
    cell_imaging2 = demo_directory / "in_cellulo" / "cells_without_mrna" / "imaging2_17_07_23"

    send_command(client, "system.health")

    # PTU extraction: 60 nM dextran.
    send_command(client, "gui.select_mode", {"mode": "extract"})
    send_command(client, "extract.load_directory", {"directory": str(dextran_60)})
    send_command(client, "extract.set_rows_to_skip", {"enabled": False, "rows": 15})
    send_command(client, "extract.set_statistical_filter", {"channel": 1, "enabled": False})
    send_command(client, "extract.apply_all")

    # PTU extraction: 80 nM dextran.
    send_command(client, "extract.load_directory", {"directory": str(dextran_80)})
    send_command(client, "extract.set_rows_to_skip", {"enabled": False, "rows": 15})
    send_command(client, "extract.set_statistical_filter", {"channel": 1, "enabled": False})
    send_command(client, "extract.apply_all")

    # TCSPC-filtered PTU extraction: dual-channel in-cellulo measurement, newer acquisition.
    send_command(client, "extract.load_directory", {"directory": str(cell_new)})
    send_command(client, "extract.set_rows_to_skip", {"enabled": True, "rows": 15})
    send_command(client, "extract.set_statistical_filter", {"channel": 1, "enabled": True})
    send_command(client, "extract.open_filter_setup", {"channel": 1})
    send_command(client, "extract.set_background_range", {"channel": 1, "enabled": True})
    send_command(client, "extract.calculate_filters", {"channel": 1})
    send_command(client, "extract.accept_filters", {"channel": 1})
    send_command(client, "extract.select_filter", {"channel": 1, "name": "Current decay; CH 1"})
    send_command(client, "extract.set_statistical_filter", {"channel": 2, "enabled": True})
    send_command(client, "extract.open_filter_setup", {"channel": 2})
    send_command(client, "extract.set_background_range", {"channel": 2, "enabled": True})
    send_command(client, "extract.calculate_filters", {"channel": 2})
    send_command(client, "extract.accept_filters", {"channel": 2})
    send_command(client, "extract.select_filter", {"channel": 2, "name": "Current decay; CH 2"})
    send_command(client, "extract.apply_all")

    # TCSPC-filtered PTU extraction: dual-channel in-cellulo measurement, imaging2 acquisition.
    send_command(client, "extract.load_directory", {"directory": str(cell_imaging2)})
    send_command(client, "extract.set_rows_to_skip", {"enabled": True, "rows": 15})
    send_command(client, "extract.set_statistical_filter", {"channel": 1, "enabled": True})
    send_command(client, "extract.open_filter_setup", {"channel": 1})
    send_command(client, "extract.set_background_range", {"channel": 1, "enabled": True})
    send_command(client, "extract.calculate_filters", {"channel": 1})
    send_command(client, "extract.accept_filters", {"channel": 1})
    send_command(client, "extract.select_filter", {"channel": 1, "name": "Current decay; CH 1"})
    send_command(client, "extract.set_statistical_filter", {"channel": 2, "enabled": True})
    send_command(client, "extract.open_filter_setup", {"channel": 2})
    send_command(client, "extract.set_background_range", {"channel": 2, "enabled": True})
    send_command(client, "extract.calculate_filters", {"channel": 2})
    send_command(client, "extract.accept_filters", {"channel": 2})
    send_command(client, "extract.select_filter", {"channel": 2, "name": "Current decay; CH 2"})
    send_command(client, "extract.apply_all")

    # Concentration calculation: 60 nM dextran with its calibration.
    send_command(client, "gui.select_mode", {"mode": "phot2conc"})
    send_command(client, "phot2conc.set_error_mode", {"sem": False})
    send_command(client, "phot2conc.load_directory", {"directory": str(dextran_60)})
    send_command(client, "phot2conc.set_roi_source", {"source": "none"})
    send_command(client, "phot2conc.load_calibration", {"path": str(dextran_60 / "calibration.json")})
    send_command(client, "phot2conc.calculate_all")
    send_command(client, "phot2conc.export_results", {"path": str(dextran_60 / "results.csv")})

    # Concentration calculation: 80 nM dextran with its calibration.
    send_command(client, "phot2conc.load_directory", {"directory": str(dextran_80)})
    send_command(client, "phot2conc.set_roi_source", {"source": "none"})
    send_command(client, "phot2conc.load_calibration", {"path": str(dextran_80 / "calibration.json")})
    send_command(client, "phot2conc.calculate_all")
    send_command(client, "phot2conc.export_results", {"path": str(dextran_80 / "results.csv")})

    # Concentration calculation: TCSPC-filtered newer dual-channel cell acquisition.
    send_command(client, "phot2conc.load_directory", {"directory": str(cell_new)})
    send_command(client, "phot2conc.load_calibration", {"path": str(cell_new / "calibration.json")})
    send_command(client, "phot2conc.set_roi_source", {"source": "auto"})
    send_command(client, "phot2conc.select_file", {"filename": "cell-108-01252-400nm_8.ptu"})
    send_command(client, "phot2conc.set_auto_roi", {"channel": 1, "cell_threshold": 1})
    send_command(client, "phot2conc.set_auto_roi", {"channel": 2, "cell_threshold": 1})
    send_command(client, "phot2conc.calculate")
    send_command(client, "phot2conc.add_result")
    send_command(
        client,
        "phot2conc.export_results",
        {"path": str(cell_new / "results_tcspc.csv")},
    )

    # Concentration calculation: imaging2 dual-channel cell acquisition.
    send_command(client, "phot2conc.load_directory", {"directory": str(cell_imaging2)})
    send_command(client, "phot2conc.load_calibration", {"path": str(cell_imaging2 / "calibration.json")})
    send_command(client, "phot2conc.set_roi_source", {"source": "auto"})
    send_command(client, "phot2conc.select_file", {"filename": "cell-604-02105.ptu"})
    send_command(client, "phot2conc.set_auto_roi", {"channel": 2, "cell_threshold": 1})
    send_command(client, "phot2conc.set_auto_roi", {"channel": 1, "copy_from_other": True})
    send_command(
        client,
        "phot2conc.set_auto_roi",
        {"channel": 1, "roi_mode": "subtract dark", "object_threshold": 1.036},
    )
    send_command(client, "phot2conc.calculate")
    send_command(client, "phot2conc.add_result")
    send_command(client, "phot2conc.export_results", {"path": str(cell_imaging2 / "results.csv")})

    # Standard PIE-gated extraction: repeat the selected newer cell measurement.
    send_command(client, "gui.select_mode", {"mode": "extract"})
    send_command(client, "extract.load_directory", {"directory": str(cell_new)})
    send_command(client, "extract.set_rows_to_skip", {"enabled": True, "rows": 15})
    send_command(client, "extract.set_statistical_filter", {"channel": 1, "enabled": False})
    send_command(client, "extract.set_statistical_filter", {"channel": 2, "enabled": False})
    # Loading a dual-channel PIE file initializes the standard channel gates.
    send_command(client, "extract.apply_all")

    # Concentration calculation: gated variant of the selected cell measurement.
    send_command(client, "gui.select_mode", {"mode": "phot2conc"})
    send_command(client, "phot2conc.set_error_mode", {"sem": False})
    send_command(client, "phot2conc.load_directory", {"directory": str(cell_new)})
    send_command(client, "phot2conc.load_calibration", {"path": str(cell_new / "calibration.json")})
    send_command(client, "phot2conc.set_roi_source", {"source": "auto"})
    send_command(client, "phot2conc.select_file", {"filename": "cell-108-01252-400nm_8.ptu"})
    send_command(client, "phot2conc.set_auto_roi", {"channel": 1, "cell_threshold": 1})
    send_command(client, "phot2conc.set_auto_roi", {"channel": 2, "cell_threshold": 1})
    send_command(client, "phot2conc.calculate")
    send_command(client, "phot2conc.add_result")
    send_command(
        client,
        "phot2conc.export_results",
        {"path": str(cell_new / "results_gating.csv")},
    )


def find_application(explicit_path: str | None = None) -> Path:
    """Find the application in an installed release or a source checkout."""

    if explicit_path:
        candidates = [Path(explicit_path).expanduser().resolve()]
    else:
        payload_root = DEMO_DIRECTORY.parents[1]
        candidates = [
            payload_root / "smICA" / "smICA_tool.py",
            payload_root / "src" / "smICA" / "smICA_tool.py",
        ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    checked = "\n".join(f"  - {candidate}" for candidate in candidates)
    raise DemoError(f"The smICA application entry point was not found. Checked:\n{checked}")


def select_port(requested_port: int) -> int:
    """Return the requested loopback port or select a currently free one."""

    if requested_port:
        return requested_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def load_client_class() -> Any:
    """Load the client from an installation or directly from the source tree."""

    source_directory = DEMO_DIRECTORY.parents[1] / "src"
    if source_directory.is_dir():
        sys.path.insert(0, str(source_directory))
    from smICA.Required.automation_client import AutomationClient

    return AutomationClient


def wait_until_ready(client: Any, process: subprocess.Popen[Any], timeout: float) -> None:
    """Wait for the GUI event loop and automation server to become ready."""

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise DemoError(f"smICA exited before the demo started (exit code {process.returncode}).")
        try:
            response = client.call("system.health", {})
            if response.get("ok") is True:
                return
        except Exception:
            pass
        time.sleep(0.25)
    raise DemoError(f"smICA did not start its automation server within {timeout:g} seconds.")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the bundled smICA demo from PTU extraction to concentration results."
    )
    parser.add_argument("--app", help="Override the path to smICA_tool.py.")
    parser.add_argument("--port", type=int, default=0, help="Loopback port; 0 selects a free port.")
    parser.add_argument("--startup-timeout", type=float, default=120.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_argument_parser().parse_args(argv)
    process: subprocess.Popen[Any] | None = None
    client: Any = None
    try:
        application = find_application(arguments.app)
        port = select_port(arguments.port)
        client_class = load_client_class()
        client = client_class(port=port, timeout=2.0)
        command = [
            sys.executable,
            str(application),
            "--automation-server",
            "--automation-port",
            str(port),
            "--automation-allow-shutdown",
        ]
        print(f"Starting smICA demo server on 127.0.0.1:{port}", flush=True)
        process = subprocess.Popen(command, cwd=str(application.parent))
        wait_until_ready(client, process, arguments.startup_timeout)
        run_analysis(client)
        print("\nDemo completed successfully.", flush=True)
        print(f"Results: {DEXTRAN_60_DIRECTORY / 'results.csv'}", flush=True)
        print(f"Results: {DEXTRAN_80_DIRECTORY / 'results.csv'}", flush=True)
        print(f"Results: {CELL_NEW_DIRECTORY / 'results_tcspc.csv'}", flush=True)
        print(f"Results: {CELL_NEW_DIRECTORY / 'results_gating.csv'}", flush=True)
        print(f"Results: {CELL_IMAGING2_DIRECTORY / 'results.csv'}", flush=True)
        return 0
    except (DemoError, OSError, ValueError) as exc:
        print(f"smICA demo: {exc}", file=sys.stderr, flush=True)
        return 1
    except KeyboardInterrupt:
        print("\nsmICA demo interrupted.", file=sys.stderr, flush=True)
        return 130
    finally:
        if process is not None and process.poll() is None:
            if client is not None:
                try:
                    send_command(client, "system.shutdown")
                except Exception as exc:
                    print(f"Could not request a clean smICA shutdown: {exc}", file=sys.stderr)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == "__main__":
    raise SystemExit(main())
