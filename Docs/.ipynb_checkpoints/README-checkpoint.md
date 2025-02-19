# smICA - single-molecule Image to Concentration Analyser
This repository provides a software for calculations of fluorophores' concentrations from the FLIM images stored in the PTU format (PicoQuant - Germany).   

## About
The Software allows to extract the information about registered photons from the _.ptu_ file, filter them using statistical filters based on fluorescence decay time, autodetect region of interest (ROI) and finaly create the map of absolute concentration of the fluorophore.

## List of changes

1. The two previously separated scripts (EXTRACT_AND_FILTER_PTU and Phot2Conc) has been inegrated into one script. At the startup the user can chose the operation mode (EXTRACT from PTU and FILTER or Phot 2 Conc).
2. The code was modified and polished
3. In the Phot 2 Conc mode the automatic ROI feature was added allowing to automatic detection of cells, removing the nucleus from the cell, or copy the ROI between channels.
4. Minor graphical modifications and adjustments.
5. Installation setup for Linux (tested on Fedora 40) and for Windows (tested on Windows 10 and 11).

## Installation guide

1. Download the _smICA_installation_files.zip_ file and extarct in the desired location.

2. Run the installation script:


    1. On Linux run the _install.sh_ shell scirpt by typing:
   
       ./install.sh
       
    2. On Windows double click the _install_win.bat_ executable scirpt. 
The installation can take a while as all required packages need to be download.
  

## User guide


    
### Acknowledgement
This work was funded by the Polish Science Fund within the framework of the Virtual Research Institute; grant WIB-1/2020-O11 - WIB_HERO.