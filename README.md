# single-molecule Image to Concentration Analyser
This repository provides a workflow for calculations of fluorophores' concentrations from the FLIM images stored as the PicoQuant PTU files.   

## About
The Workflow consists of three steps; each has its subfolder with the scripts corresponding to a given task. Read the README.md files in each folder to learn more about the script usage. The steps are as follows:   
1. **EXTRACT_AND_FILTER_PTU**; In this step, you can extract the raw data from the PTU files obtained utilizing the SymPhoTime software (PicoQuant). You will also be able to filter the raw data using the time gating method or filter out background noise or autofluorescence using the statistical filters based on the fluorescence lifetime decay pattern.
2. **REWRITE_ROI**; This step is necessary if you wish to use region of interest (ROI) for further analysis of your FLIM data.
3. **Phot2Conc**; Here, you can calculate the mean number of particles or concentrations of fluorophores based on the maps of photons extracted from PTU files in the first step. Very useful for analysis of file series.

## !!! BEFORE FIRST USE !!!

1. Clone or download a git repository for reading the PTU files: *readPTU_FLIM*. **Make sure** you are downloading the correct branch of the repository called **NIKON_correction**. Use the following link for cloning the repository: https://github.com/TKmist/readPTU_FLIM/tree/NIKON_correction or download the _.zip_ file using the following link: https://github.com/TKmist/readPTU_FLIM/archive/refs/heads/NIKON_correction.zip
2. From the readPTU_FLIM repository copy the file readPTU_FLIM.py to the EXTRACT_AND_FILTER_PTU\dep\ folder.
3. Check for required packages:   
All three substeps of the workflow require [Dear PyGui](https://github.com/hoffstadt/DearPyGui), which you can install by typing the following command in your Python environment.   
    
    ``pip install dearpygui``
    
Other required packages are following:    
numpy, pandas, json, matplotlib, PIL, pyautogui, lmfit, scipy, sympy    
### Licence

Each element of this workflow is distributed under the MIT License.    
### Acknowledgement
This work was funded by the Polish Science Fund within the framework of the Virtual Research Institute; grant WIB-1/2020-O11 - WIB_HERO.