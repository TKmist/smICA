# <h1 align="center">smICA</h1>

<p align="center">single-molecule Image to Concentration Analyser</p>

<h1></h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white" style="display:inline-block; margin:0 2px; vertical-align:middle;">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey" style="display:inline-block; margin:0 2px; vertical-align:middle;">
  <img src="https://img.shields.io/badge/license-MIT-blue" style="display:inline-block; margin:0 2px; vertical-align:middle;">

  </p>
<p align="center">

  <img src="https://img.shields.io/badge/version-v2.1.1-green" style="display:inline-block; margin:0 2px; vertical-align:middle;">
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
  <a href="#release-notes">Release notes</a> •
  <a href="#license">License</a>
</p>
<h1></h1>

## Information
This repository provides software for calculating fluorophore concentrations from FLIM images stored in the PTU format (PicoQuant, Germany). The software allows the extraction of information about registered photons from the _.ptu_ file, filtering them using statistical filters based on fluorescence decay time and autodetection of the region of interest (ROI), and finally creating a map of the absolute concentration of the fluorophore. The GUI is powered by [Dear PyGui](https://github.com/hoffstadt/DearPyGui).   



## Installation

The software is written in Python, and its graphical interface is based on [Dear PyGui](https://github.com/hoffstadt/DearPyGui). It is highly recommended to install Python 3.11 or 3.12. Follow the steps below to install the software.

1. Go to the project's [releases](https://github.com/TKmist/smICA/releases/latest). Choose your OS version (Windows or Linux), download the proper *smICA_(version)_(OS)* file and extract it to the desired location.

2. Go to the extracted directory and run the installation script:

    1. On Linux in a terminal, run the bash script by typing:
   
       ./install.sh
       
    2. On Windows, double-click the _install_win.bat_ executable script. The Windows installation files are distributed together with the Python Embedded Distribution for Windows. Make sure you are not using a VPN, as it may block the installation of PIP in the Python embedded distribution. 
  
The installation script will download all required packages, create the run_smICA script or run_smICA.bat (on Windows), and create the shortcuts. 

By default, smICA uses dark theme. The light theme can be activated by modifying the [settings.json](https://github.com/TKmist/smICA/tree/main/src/smICA/res/settings.json) file. To do that replace *'dark'* with '*light'*.


## Release notes
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
