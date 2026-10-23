# <h1 align="center">smICA</h1>

<p align="center">single-molecule Image to Concentration Analyser</p>

<h1></h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white" style="display:inline-block; margin:0 2px; vertical-align:middle;">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey" style="display:inline-block; margin:0 2px; vertical-align:middle;">
  <img src="https://img.shields.io/badge/license-MIT-blue" style="display:inline-block; margin:0 2px; vertical-align:middle;">

  </p>
<p align="center">

  <img src="https://img.shields.io/badge/version-v2.2.0-green" style="display:inline-block; margin:0 2px; vertical-align:middle;">
  <a href="https://github.com/TKmist/smICA/releases/latest">
    <img src="https://img.shields.io/github/v/release/TKmist/smICA?label=download" style="display:inline-block; margin:0 2px; vertical-align:middle;">
  </a>
  <a href="https://zenodo.org/records/20134967">
    <img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20134967-blue" style="display:inline-block; margin:0 2px; vertical-align:middle;">
  </a>
</p>


<p align="center">
  <a href="#information">Information</a> •
  <a href="#installation">Installation</a> •
  <a href="#testing">Testing</a> •
  <a href="#developing-analytical-add-ons">Developing add-ons</a> •
  <a href="#release-notes">Release notes</a> •
  <a href="#license">License</a>
</p>
<h1></h1>

## Information
This repository provides software for calculating fluorophore concentrations from FLIM images stored in the PTU format (PicoQuant, Germany). The software allows the extraction of information about registered photons from the _.ptu_ file, filtering them using statistical filters based on fluorescence decay time and autodetection of the region of interest (ROI), and finally creating a map of the absolute concentration of the fluorophore. The GUI is powered by [Dear PyGui](https://github.com/hoffstadt/DearPyGui).   

The software was developed and tested on PTU files created with the PicoHarp 300 TTTR system (PicoQuant, Germany). Further development to include other file formats is possible depending on the data availability. If you think this program might be useful in your studies but your system is not yet supported, feel free to contact the [author](mailto:tkalwarczyk@ichf.edu.pl). The list of supported hardware is provided [here](https://tkmist.github.io/smICA/supported-equipment/).

## Installation

The software is written in Python, and its graphical interface is based on [Dear PyGui](https://github.com/hoffstadt/DearPyGui). It is highly recommended to install Python 3.11 or 3.12. Follow the steps below to install the software.

1. Go to the project's [releases](https://github.com/TKmist/smICA/releases/latest). Choose your OS version (Windows or Linux), download the proper *smICA_(version)_(OS)* file and extract it to the desired location.

2. Go to the extracted directory and run the installation script:

    1. On Linux in a terminal, run the bash script by typing:
   
       ./install.sh
       
    2. On Windows, double-click the _install_win.bat_ executable script. The Windows installation files are distributed together with the Python Embedded Distribution for Windows. Make sure you are not using a VPN, as it may block the installation of PIP in the Python embedded distribution. 
  
The installation script will download all required packages, create the run_smICA script or run_smICA.bat (on Windows), and create the shortcuts. 

All project-owned launchers and command-line clients are plain Python, Bash, or
Windows Batch scripts. The bundled third-party `python_embedded` runtime is the
only repository exception to the no-executable-binaries rule.

By default, smICA uses dark theme. The light theme can be activated by modifying the [settings.json](https://github.com/TKmist/smICA/tree/main/src/smICA/res/settings.json) file. To do that replace *'dark'* with '*light'*.


## Testing

The repository provides two complementary test suites.

### Developer tests

The `dev_tests` directory contains lightweight `pytest` regression tests for
the PTU reader, frame-resolved calculations, automatic ROI handling,
documentation builder, installers, and TCP/GUI automation infrastructure.
These tests validate the source repository and are not part of the installed
end-user validation command.

From the repository root, install pytest and run the cross-platform test
launcher:

```bash
python -m pip install pytest
python dev_tests/run_tests.py
```

Additional pytest arguments can be appended, for example:

```bash
python dev_tests/run_tests.py -q
python dev_tests/run_tests.py -k tcp
```

### Calculation and end-to-end tests

The `calc_tests` directory contains standalone numerical unit tests, reference
PTU measurements, calibration files, ROI definitions, expected results, and a
complete TCP-driven end-to-end analytical workflow. The source dataset
directories located directly under `calc_tests/REFERENCE_DATA` contain the
unprocessed PTU measurements and their calibration JSON files. Working copies
under `calc_tests/REFERENCE_DATA/TypeOfFiltering` are organized by analysis
variant and contain only PTU files, calibration JSON files, and ROI
directories. The neutral reference output is stored as
`calc_tests/REFERENCE_DATA/REFERENCE_output/reference_results.csv`.

Run all numerical unit tests directly from a source checkout:

```bash
python calc_tests/unity_test/run_all.py
```

The same numerical tests are available after installation:

```bash
# Linux
./run_smICA --test
```

```bat
:: Windows
smICA.bat --test
```

To run the complete end-to-end reference analysis, first start the installed
application with its automation server in one terminal:

```bash
./run_smICA --automation-server --automation-port 8765
```

Then run the workflow from a second terminal at the repository root:

```bash
bash calc_tests/run_Analytical_workflow_TCP.sh
```

On Windows, run the application with
`smICA.bat --automation-server --automation-port 8765`. The installed TCP
client is the text script `v_smICA_env\Scripts\smica-call.bat`; smICA does not
install a compiled client launcher. If the client is not available in `PATH`,
use its full script path. Run the native end-to-end test with
`calc_tests\run_Analytical_workflow_TCP.bat`. The workflow processes the datasets under
`calc_tests/REFERENCE_DATA`, exports `results.csv` files, and stops immediately
if any TCP command fails.


## Developing analytical add-ons

Directory-based analytical methods can be created from
[`templates/add_on_template`](templates/add_on_template). A complete method
copied to `src/smICA/Modes` is discovered automatically and added to the
**Analysis** menu. The updater also installs new valid modes distributed by the
official repository while preserving local modes that are not part of the
update.

The built-in manual contains a separate **For developers** chapter covering
the mode contract, file responsibilities, GUI lifecycle, updater behavior,
testing, and optional TCP automation.


## Release notes
#### v2.2.0
- Added a phconvert reader for PicoHarp 300 T3 measurements, marker validation and integration of every reconstructed frame. Unsupported record types retain an explicit fallback to readPTU_FLIM.
- Introduced version-2 PKL output with integrated foreground, background and fluorescence-lifetime maps plus sparse frame-resolved foreground/background products.
- Added export-only frame columns for weighted counts, background, molecule number and concentration. Frame-wise information is intentionally not displayed in the GUI.
- Added foreground-intensity, background-intensity and foreground-lifetime display modes. Automatic ROI detection uses foreground intensity.
- Added a versioned loopback TCP/JSON server and `smica-call` client. Commands call the same Dear PyGui callbacks as manual controls, including native **Apply to all** and **Calculate all** operations with GUI progress feedback. Batch responses also expose per-PTU file size and measured wall time for reproducibility and performance reporting.
- Added commands for automatic background-range selection, decay-library import and accepted foreground-filter selection.
- Improved error responses for automated TCP/JSON communication, so an internal failure identifies the command in `message` and `details.command`, while the traceback remains in the local application log.
- Added resumable workflows and a final report containing processed/reused counts, elapsed time and machine information.
- Added installed numerical tests available through `--test`; reports show expected values, calculated values, units and tolerances.
- Added `calc_tests/REFERENCE_DATA` containing raw PTU data, results obtained from those data, and a workflow to reproduce the results.
- Added a validated analytical add-on template, automatic updater support for official add-ons, and a developer guide for new analytical methods.
 - See [Changelog.md](Changelog.md) for the complete list of changes.
#### V2.1.2
 - Fixed problems with the Python embedded folder.
#### V2.1.1
 - Added _Settings_ item in the menu bar to simplify theme changes
 - Added the ROI mixer tool.
#### V2.1.0
 - Updated built-in help
 - Light theme added.
 - Modified documentation and integration with GitHub pages.
 - The _REWRITE_ROI_ script is integrated into smICA as a tool in the **Tool** menu.
 - Add global font scaling to the resize function in the initial window
 - Added a handler for the arrow up and down keys. 
#### v2.0.1
 - Modified README.md file
#### v2.0.0
1. Integration of the previously separate scripts (_EXTRACT_AND_FILTER_PTU_ and _Phot2Conc_) into a single unified script. At startup, the user can select the operation mode (EXTRACT from PTU and FILTER or Phot2Conc).
2. The _REWRITE_ROI_ script remains available, allowing users to load externally generated ROI files (text image format). As external ROI files are not essential for the standard analysis workflow, the script is located in the _src_ directory. After installation, the _REWRITE_ROI_ script is available in the _smICA_ folder within the installation path.
3. Complete refactoring and codebase cleanup.
4. In the Phot2Conc mode, an automatic ROI feature was added, enabling:
    - automatic cell detection,
    - nucleus exclusion from detected cells,
    - copying ROIs between channels.
5. Support for multiple external ROI files.
6. Minor graphical improvements and overall code stability enhancements.
7. Automatic update availability checking.
8. Installation setup added for:
   - Linux (tested on Fedora 40),
   - Windows (tested on Windows 10 and 11).




## License

This project is licensed under the MIT license.
See the [LICENSE](LICENSE) file for the full license text.

This program is distributed WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

### Third-party components


During installation, this program may optionally download the `readPTU_FLIM.py`
component from an [external repository](https://github.com/TKmist/readPTU_FLIM/tree/NIKON_correction).

This component is licensed under the MIT License and is not distributed with this repository.

---

This software includes the Python Embedded Distribution for Windows,
which is licensed under the Python Software Foundation License (PSF).
License information is provided within the embedded distribution.

---

This repository includes DejaVu Sans Condensed font files (TTF),
which are distributed under their own license.
Please refer to the font files or accompanying license information for details.

---

### Academic use

If you use the FcsIT software or any part of it in your academic work, citation of the relevant publications listed below is appreciated. 

1. Kalwarczyk, T., Bubak, G., Michalski, J., Lis, A., Kwapiszewska, K., Pilz, M., Mamot, A., Perzanowska, O., Kowalska, J., Jemielity, J., & Hołyst, R. (2024). smICA: Open-Source Software for Quantitative, Lifetime-Resolved Mapping of Absolute Fluorophore Concentrations in Living Cells. arXiv. 10.48550/ARXIV.2410.00532
2. Kalwarczyk, T. (2026). smICA - single-molecule Image to Concentration Analyser. Zenodo. 10.5281/ZENODO.20134967
