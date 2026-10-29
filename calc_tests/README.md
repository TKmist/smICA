# smICA calculation and end-to-end tests

This directory contains calculation unit tests and a reference analytical
workflow that exercises smICA through its public TCP automation interface.

## Directory layout

- `unit_test` contains small standalone unit tests. They do not start the
  GUI and do not require pytest.
- `REFERENCE_DATA` contains source PTU measurements, calibration JSON files,
  ROI definitions, working datasets grouped by filtering method, and the
  reference result table.
- `Analytical_workflow.ipynb` documents the analytical procedure.
- `Analytical_workflow_TCP_commands.txt` implements that procedure with public
  TCP commands and is intentionally readable as a template for custom workflows.
- `run_Analytical_workflow_TCP.sh` locates the TCP client and runs the complete
  command sequence on Linux.
- `run_Analytical_workflow_TCP.bat` is the equivalent native Windows CMD
  workflow and does not require PowerShell, Git Bash, or WSL.
- `workflow_state.txt` is a visible text record of completed extraction and
  calculation batches. `workflow_report.txt` is created after each run.

## Reference data archives

Each source dataset located directly under `REFERENCE_DATA` also has a separate
ZIP archive. Every archive contains its complete top-level dataset directory,
including PTU measurements and calibration files. The
`REFERENCE_DATA/TypeOfFiltering` tree is intentionally not compressed.

The source directories are already present in the repository working tree. If
only the archives are available, restore all source datasets on Linux with:

```bash
cd calc_tests/REFERENCE_DATA
for archive in *.zip; do unzip -o "$archive"; done
```

On Windows, use the standard Command Prompt from the repository root:

```bat
cd calc_tests\REFERENCE_DATA
for %F in (*.zip) do tar -xf "%F"
```

## Calculation unit tests

Run all standalone calculation unit tests from the repository root:

```bash
python calc_tests/unit_test/run_all.py
```

The runner executes every `test_*.py` file in a deterministic order and prints
the purpose, expected value, calculated value, unit, tolerance, and result for
each numerical check. A non-zero exit status means that at least one test
failed.

After installing smICA, the same tests can be run through the generated
launcher.

Linux:

```bash
./run_smICA --test
```

Windows:

```bat
smICA.bat --test
```

## End-to-end TCP test

The end-to-end workflow runs extraction, filtering, Phot2conc calculations,
ROI-based analysis, and result export. It operates on
`REFERENCE_DATA/TypeOfFiltering` and requires an installed smICA application
with the automation server running.

### Linux

Start smICA in the first terminal:

```bash
./run_smICA --automation-server --automation-port 8765
```

Keep the GUI open. From the repository root in a second terminal, run:

```bash
bash calc_tests/run_Analytical_workflow_TCP.sh
```

If `smica-call` is not available in `PATH`, provide its full path:

```bash
SMICA_CALL=/path/to/v_smICA_env/bin/smica-call \
    bash calc_tests/run_Analytical_workflow_TCP.sh
```

### Windows

Start smICA in Command Prompt:

```bat
smICA.bat --automation-server --automation-port 8765
```

Keep the GUI open and run the native CMD workflow from the repository root:

```bat
calc_tests\run_Analytical_workflow_TCP.bat
```

The default TCP port is `8765`. It can be changed consistently for the server
and workflow by setting `SMICA_AUTOMATION_PORT`. The workflow stops at the first
failed command. Generated PKL files and exported `results.csv` files are written
inside the appropriate `TypeOfFiltering` dataset directories.

Resume mode is enabled by default. Extraction batches listed in
`workflow_state.txt` are skipped. A Phot2conc calculation is skipped only when
its state entry and a non-empty `results.csv` both exist. Set
`RESUME_WORKFLOW=false` to force all batches to run again. The state and report
are ordinary visible files; the workflow creates no hidden progress files.

To adapt the example, copy the workflow, replace the paths in the explicit
dataset calls, and keep the same sequence: select a GUI mode, load a directory,
set its processing options, run the native batch callback, load the calibration
JSON in Phot2conc, calculate, and export. Avoid embedding calibration constants
in a workflow when a calibration JSON accompanies the data.

The consolidated reference table is stored at:

```text
calc_tests/REFERENCE_DATA/REFERENCE_output/reference_results.csv
```
