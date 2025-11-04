# smICA - single-molecule Image to Concentration Analyser
This repository provides software for calculations of fluorophores' concentrations from the FLIM images stored in the PTU format (PicoQuant - Germany).   

## About
The Software allows the extraction of the information about registered photons from the _.ptu_ file, filtering them using statistical filters based on fluorescence decay time, autodetect region of interest (ROI), and finally, creating the map of the absolute concentration of the fluorophore.

## List of changes

1. The two previously separated scripts (_EXTRACT_AND_FILTER_PTU_ and _Phot2Conc_) has been inegrated into one script. At the startup, the user can choose the operation mode (EXTRACT from PTU and FILTER or Phot 2 Conc). The _REWRITE_ROI_ script is still available as the users still have a chance to load the ROI file that was created externally as the text image. Since the external ROI file is not crucial in the analysis, the script is in the _src_ folder. After installation, the _REWRITE_ROI_ script is located in the _smICA_ folder at the installation path.
2. The code was modified and polished
3. In the Phot 2 Conc mode, the automatic ROI feature was added, automatically detecting cells, removing the nucleus from the cell, or copying the ROI between channels.
4. Minor graphical modifications and adjustments.
5. Installation setup for Linux (tested on Fedora 40) and Windows (tested on Windows 10 and 11).

## Installation guide

1. Download the _smICA_installation_files.zip_ file and extract in the desired location.

2. Run the installation script:


    1. On Linux, run the _install.sh_, shell script by typing:
   
       ./install.sh
       
    2. On Windows, double-click the _install_win.bat_ executable script. 
The installation can take a while as all required packages must be downloaded.
  

## User guide

At the startup the a


### Acknowledgement
This work was funded by the Polish Science Fund within the framework of the Virtual Research Institute; grant WIB-1/2020-O11 - WIB_HERO.