# smICA - single-molecule Image to Concentration Analyser
This repository provides software for calculations of fluorophores' concentrations from the FLIM images stored in the PTU format (PicoQuant - Germany).   

## About
The Software allows the extraction of the information about registered photons from the _.ptu_ file, filtering them using statistical filters based on fluorescence decay time, autodetect region of interest (ROI), and finally, creating the map of the absolute concentration of the fluorophore.

## List of changes

1. The two previously separated scripts (_EXTRACT_AND_FILTER_PTU_ and _Phot2Conc_) has been inegrated into one script. At the startup, the user can choose the operation mode (EXTRACT from PTU and FILTER or Phot 2 Conc). The _REWRITE_ROI_ script<a name="REWRITEROI"></a> is still available as the users still have a chance to load the ROI file that was created externally as the text image. Since the external ROI file is not crucial in the analysis, the script is in the _src_ folder. After installation, the _REWRITE_ROI_ script is located in the _smICA_ folder at the installation path.
2. The code was modified and polished
3. In the Phot 2 Conc mode, the automatic ROI feature was added, automatically detecting cells, removing the nucleus from the cell, or copying the ROI between channels.
4. multiple ROI files for externall ROI files was included.
5. Minor graphical and code stability modifications and adjustments.
6. Automatic checking the updates avilability.
7. Installation setup for Linux (tested on Fedora 40) and Windows (tested on Windows 10 and 11).

## Installation guide

1. Go to Realese/Latest folder and download the _smICA-install-windows_V?.?.?.zip_, or  _smICA-install-linux_V?.?.?.zip_ file and extract in the desired location.

2. Run the installation script:


    1. On Linux, run the _install.sh_, shell script by typing (if necessery run: chmod +x install.sh):
   
       ./install.sh
       
    2. On Windows, double-click the _install_win.bat_ executable script. 
The installation can take a while as all required packages must be downloaded and compilled.
  

## User guide
The workflow for mapping the fluorophore's concentration in living cells can be divided into two to three steps, depending on the user preferences. 
1. Extract the information about photons from the binary _.ptu_ file and filter the data to eliminate background or unwanted influence of autofluorescence or other fluorophores.
2. (OPTIONAL) Create the ROI file using external software, for example, ImageJ, to create a binary text image containing a selection of the pixels that should be included in the analysis. This step is optional because the third step has an option for automatic detection of the cells. A detailed description of using the _REWRITE_ROI_ script can be found in the _README_ file in the script's folder.
3. Calculate the map of the fluorophore concentration based on fluorescence intensity data and calibration data.


At the startup, the user can choose between two modes: [EXTRACT from PTU and FILTER](#EXTRACTandFILTER) or [Phot 2 Conc](#Phot2Conc).
![image info](./docs/img/init_options.png)
The first option is to extract raw data from the _.ptu_ files, filter the data using time gating, or apply statistical filters based on the fluorescence decay pattern.The second option provides a GUI to map the concentration of fluorescent molecules inside living cells.
Below is a detailed description of each mode.
You can also switch between modes by selcecting the proper option from the Mode menu.

![image info](./docs/img/mode_menu.png)


#### **EXTRACT from PTU and FILTER**<a name="EXTRACTandFILTER"></a>

First, click "File" and "Open PTU directory" to select the folder storing your _.ptu_ files.   

![image info](./docs/img/extract/click-file.png)

Keeping the _.ptu_ from different experiments in separate folders is suggested.    
The script recognizes the mode in which the measurement was performed (standard or PIE). If two detectors are used in the measurement, the signal will be automatically split and displayed as Channel 1 and Channel 2. The lifetime analysis can be performed for each channel separately.     

Simple time gating can be realized by selecting the region of the fluorescence decay pattern by moving the orange and red drag lines displayed in the upper plots<a name="upper-plots"></a>.

![image info](./docs/img/extract/imported_PTU.png)  
Only the signal corresponding to the lower plots <a name="lower-plots"></a> will be used for analysis.    
**Important!** Some older hardware based on NIKON A1 and LSM upgrade kits from PicoQuant may experience a hardware bug occurring during the crosstalk between the A1 controller and the SymPhoTime software for the _.ptu_ files acquisition. The bug occurs as additional lines in the figure are collected by SymPhoTime, resulting in a seared-like image at the top of the picture. The panel displayed below, located at the top right corner of the main window, allows you to correct the additional lines. 
![image info](./docs/img/extract/Additional_lines.png)   

##### **Apply filtering and extract** <a name="apply-procedure"></a>
The panel displayed below shows the files located in the analyzed folder. Press "Apply to single PTU file" to analyze a single file. Pressing "Apply to extract from all PTU files" applies the selected analysis procedure (time gates or statistical filters) to all files from the list.    

![image info](./docs/img/extract/Files_panel.png)

##### **Statistical filters**
Checking the "Use statistical filters" checkbox under each channel deactivates draglines and activates the "Calculate filters" button. This button opens the window (see below) where you can calculate statistical filters for background or fluorescence decay patterns imported from the library.     
![image info](./docs/img/extract/started_Stat_filters_window.png)  

##### **Removing background and afterpulsing**  <a name="remove-background"></a>
On the left of the above window is a list of decay patterns. Initially, only one pattern appears, corresponding to the pattern extracted from the image at a given channel; the one is displayed in the plot.    
Selecting the "Set data range for background" checkbox activates draglines, allowing one to select the background region of the pattern, usually the plateau at the highest times of the decay pattern. Based on the selected region, the mean value of the background signal is calculated and subtracted from the original decay data. The subtracted data is further used for calculation of the statistical filter or stored in the library by pressing "To library"; [procedure will be described later](#to-library).    
Pressing the "Calculate filters" button will calculate the proper weights according to the procedure described in the literature.[<sup>1</sup>](#ref_1)<sup>, </sup>[<sup>2</sup>](#ref_2) After that a new plot will appear. On the plot, one can see all the weights calculated for the curves in the left table, together with the background and afterpulsing signal.  To accept the current set of weights, press "Accept"; to reject and recalculate, press "Decline".    

![image info](./docs/img/extract/show_weights.png)   

##### **Export the decay pattern to library** <a name="to-library"></a>
Instead of filter calculation, one can store the given decay pattern in the library for further use. For this purpose, instead of "Calculate filters," press "To library".     

![image info](./docs/img/extract/To_lib_1.png)     

Below The "Calculate filters" button, you will see the new fields required to store the data.     

![image info](./docs/img/extract/To_lib_2.png)     

Although some fields are optional, the more details you provide, the easier you will find the proper decay. To store the data, press "Submit".

##### **Import the decay pattern from library** <a name="from-library"></a>
You can import stored decay data by pressing the "Form library" button.    

![image info](./docs/img/extract/From_library_1.png)     

Below the "Calculate filters" button, you will see the table containing all the stored decay patterns. Marking the dacay and pressing "Import" will load the dacay pattern.    

![image info](./docs/img/extract/From_library_2.png)     

Note you can select many decay patterns, but they do not need to be physically justified.

![image info](./docs/img/extract/From_library_3.png)     

You may also want to subtract the background (see [above](#remove-background)). Pressing "Calculate filters" will open the plot with calculated weights. Note the calculations can take some time. When you select many patterns, you should be sure which weight you would like to use for further analysis.
Assuming that we are interested in detecting only the photons that originate from the imported decay here noted as _c_11317_, for further analysis, you will use the weight of the same name.

##### **Filtering**<a name="filtering"></a>

Pressing the "Accept" button will close the window, and you can select the weights for analysis.

![image info](./docs/img/extract/filtering.png)     

The same procedure can be repeated for Channel 2. Next, you can [apply](#apply-procedure) the filtering to the data.

##### **OUTPUT**
As an output, for each _.ptu_ file, the script will generate several files required for further procedure steps.
Assuming that the name of your file is _some-file.ptu_. The script will generate:   
1. _some-file.pkl_  - The binary file containing experimental data. The fole is necesery to generate the concentration map.   
2. Two _.png_ files per channel.

The _.pkl_ file is pickle file containing the python dictionary. The structure of the file is described in the table below.

|   Keys   | Value description                        |
|----------|------------------------------------------|
| File info| The python dictionary containing: |
|          |  'L_file' : name of the _.ptu_file_                                       |
|          |  'Pixels per line' : number of pixel in line in the image                                       |
|          |  'Number of lines' : number of lines in the image                                      |
|          |  'Pixels size' : size of the single pixel (nm)                                      |
|          |  'Number of frames' : number of frames acquired during the single measurement |
|          |  'Pixel dwell' : The time in $\mu$s that is spend to illuminate a single pixel |
|          |  'Lifetime resolution' : The temporal resolution of the fluorescence decay (ns) |
| export_df_1| The pandas DataFrame containing the number of photons registered in channel 1 for each pixel  |
| export_df_2| The pandas DataFrame containing the number of photons registered in channel 1 for each pixel  |
| taus_1| The pandas DataFrame containing the TCSPC histogram registered in channel 1. The [time-gated](#lower-plots) signal|
| taus_2| The pandas DataFrame containing the TCSPC histogram registered in channel 2. The [time-gated](#lower-plots) signal|
| fulltaus_1| The pandas DataFrame containing the [full](#upper-plots) TCSPC histogram registered in channel 1. |
| fulltaus_2| The pandas DataFrame containing the [full](#upper-plots) TCSPC histogram registered in channel 2. |
| lifetimes_1| Numpy array containing the fluorescence lifiteime for each pixel registered in channel 1. Signal after time-gating/filtration. |
| lifetimes_2| Numpy array containing the fluorescence lifiteime for each pixel registered in channel 2. Signal after time-gating/filtration. |
| intensity_1| Numpy array containing the number of photons for each pixel registered in channel 1. Signal after time-gating/filtration. |
| intensity_2| Numpy array containing the number of photons for each pixel registered in channel 2. Signal after time-gating/filtration. |
| bgrnd_1| Numpy array containing the filtered background registered for channel 1. |
| bgrnd_2| Numpy array containing the filtered background registered for channel 2. |
| filter_weight_1| Numpy array containing the weights for each TCSPC channel calculated for channel 1. |
| filter_weight_2| Numpy array containing the weights for each TCSPC channel calculated for channel 2. |
| filter_afterpulsing_weight_1| Numpy array containing the weights for each TCSPC channel calculated for the background for channel 1. |
| filter_afterpulsing_weight_2| Numpy array containing the weights for each TCSPC channel calculated for the background for channel 2. |
| special_markers_1| Pandas dataframe containing full TCSPC information for both channels. |
| special_markers_2| Duplicated from special_markers_1|
| filtered_taus_1 | Pandas dataframe containing the TVSPC histogram after the TCSPC filtration procedure for channel 2. |
| filtered_taus_1 | Pandas dataframe containing the TVSPC histogram after the TCSPC filtration procedure for channel 2. |
The minimal python script to get the pickled data is below.

        import os
        import pickle
        import pandas as pd
        import numpy as np
        path = '<path-to-file>/<file-name>.pkl'

        with open(path, 'rb') as file:
            pkl = pickle.load(file)

        file_info = pkl['File info']
        print(file_info)

        DF_1 = pkl['export_df_1']
        DF_2 = pkl['export_df_2']
        print(DF_1)
        print(DF_2)

        DF_taus_1 = pkl['taus_1']
        DF_taus_2 = pkl['taus_2']
        
        print(DF_taus_1)
        print(DF_taus_2)
        
        DF_ftaus_1 = pkl['fulltaus_1']
        DF_ftaus_2 = pkl['fulltaus_2']
        
        print(DF_ftaus_1)
        print(DF_ftaus_2)
        
        lifetimes_1 = pkl['lifetimes_1']
        lifetimes_2 = pkl['lifetimes_2']
        
        print(lifetimes_1)
        print(lifetimes_2)
        
        intensity_1 = pkl['intensity_1']
        intensity_2 = pkl['intensity_2']
        
        print(intensity_1)
        print(intensity_2)

        bgrnd_1 = pkl['bgrnd_1']
        bgrnd_2 = pkl['bgrnd_2']
        
        print(bgrnd_1)
        print(bgrnd_2)

        filter_weight_1 = pkl['filter_weight_1']
        filter_weight_2 = pkl['filter_weight_2']
        
        print(filter_weight_1)
        print(filter_weight_2)

        filter_afterpulsing_weight_1 = pkl['filter_afterpulsing_weight_1']
        filter_afterpulsing_weight_2 = pkl['filter_afterpulsing_weight_2']
        
        print(filter_afterpulsing_weight_1)
        print(filter_afterpulsing_weight_2)

        special_markers_1 = pkl['special_markers_1']
        special_markers_2 = pkl['special_markers_2']
        
        print(special_markers_1)
        print(special_markers_2)

        filtered_taus_1 = pkl['filtered_taus_1']
        filtered_taus_2 = pkl['filtered_taus_2']
        
        print(filtered_taus_1)
        print(filtered_taus_2)


#### **Phot 2 Conc** <a name="Phot2Conc"></a>

This mode allow to map the concentration of fluorescent molecules using single-molecule FLIM imaging data.
The script requires the _.pkl_ files created in the [EXTRACT from PTU and FILTER](#EXTRACTandFILTER) mode. __Important! This script does not read the _.ptu_ files directly. It is necessary to use the [EXTRACT from PTU and FILTER](#EXTRACTandFILTER) mode first!__

The GUI is divided into several sections.
1. PTU metadata containing the information about image acquiisition.
2. ROI containing the selction panel for coosing the metod for the region of interest. It also allow to controll the automatic ROI [see bellow](#autoroi).
3. The list of files for analysis that are located in the PTU folder.
4. Buttons starting the claculations and export oppitons.
5. Analysed image - 5' for channel 1 and 5'' for channel 2.
6. Histograms of the conentration numberof molecules or mubmber of photons per pixel - 6' for channel 1 and 6'' for channel 2.
7. The FCS callibration data
8. Mean results.
   
![image info](./docs/img/phot/GUI.png) 

##### **Loading files and callibration data**<a name="will calculate the results for a single file "></a>

The folder cotaining files for analysis can be selected by using File menu.
![image info](./docs/img/phot/PTU_folder.png)

__Note.__ The folder should contain only _.ptu_ files and the corresponding _.pkl_ files.  

After loading the list of files it is recommended to load or input the FCS callibration data and molecular brightness of the fluorophore required for proper calcualtaion of the number of molecules and concentration.
![image info](./docs/img/phot/Phot2Conc_calib_load.png)
    
or manually.    
    
![image info](./docs/img/phot/Phot2Conc_calib_manual_input.png)
    
__Note. When you load the file it needs to have a proper structure.__ For more details check the Calliberation_exmaple files (_.json_) in the smaples folder.
   The calibration values provided manually can be saved by pressing the save button

   ![image info](./docs/img/phot/Phot2Conc_calib_save.png)

The analysed image is displayed in windows corrresponding to channel 1, 2 or both.
Above the images the user is able to adjust the visibility of the image by changing contrast and brightness or the overlaying ROI's alpha channel; [see ROI section](#ROI). 
   ![image info](./docs/img/phot/Phot2Conc_image_adjust.png)
**The adjustment** is performed only on the displayed image (channel 1 or channel 2) and **does not infliuence the results**.

##### **Selecting the ROI**<a name="ROI"></a>
The region of interest is a part of the image that will be considered during the image analysis. It is marked as the red area on the image. The software has two options for ROI definition: "ROI from files" or "Auto ROI".
![image info](./docs/img/phot/ROIs.png)
The "ROI from files" option requires externally created roi files. The examples of externally created ROI files (using ImageJ) are given in the samples/ROI folder. The files should be rewritten with the _REWRITE_ROI.py_   [script](#REWRITEROI) before import. Note that (i) each channel's ROI file is created separately. (ii) the filename of the ROI file should have the same structure as the PTU file with an additional string at the end of the filename, according to the example given below.    
_file_name.ptu_    
_file_name_roi0_ch_1.dat_ - (ROI file for channel 1)    
_file_name_roi0_ch_2.dat_ - (ROI file for channel 2)    
The ROI files will automatically load the given _.ptu_ file. To import the ROI files, the user must specify the folder where the files are located by selecting the path using the "Open ROI directory" from the File menu. It is possible to have many ROI files per _.ptu_ file. The multiple ROI files are identified by numeration in the _roiX_ part of the ROI's file name.
![image info](./docs/img/phot/ROI_folder.png)

<a name="autoroi"></a>The second option for selecting the region of interest is the automatic mode. Selecting the Auto ROI checkbox displays the control panel for the ROI in both channels and the ROI on the image as a red field.
 ![image info](./docs/img/phot/Phot2Conc_autoroi_control.png)

At this moment, the automatic ROI option offers: automatic detection of single cell, automatic detection of more than one cell and selection of the ROI of interest (clicking on the image), copying ROI between channels, finding dark or brights area, subtracting dark or bright area, finding and subracting many bright spots.
 ![image info](./docs/img/phot/Phot2Conc_autoroi_detect_mode.png)
All modes use the OTSU thresholding method. The user can independently shift the original OTSU thresholding level by changing the corresponding sliders in each channel.

Copying the ROI between the cannels is performed only for the "detect cell" mode. Note that when the checkbox is selected, the thresholding levels can be regulated only in the original channel. For example,: selecting "Channel 1->2" will copy the ROI from channel 1 to channel 2. 

##### **Calculate results**

To correctly calculate concentration maps, the user must provide or import the calibration data obtained from FCS measurements, including the width of the focal volume $\omega_0$, the structure parameter $\kappa$, and the mean molecular brightness; [see above](#loadingfiles). 
Pressing "Calculate single" will display the results for a single file. Press the "Add to results" button to store the results and remember the Auto ROI settings for a given file. The calculate all button will automatically calculate and store the data for all files, one by one.
 ![image info](./docs/img/phot/Phot2Conc_calculate.png)

The result will be displayed in these tables:   

![image info](./docs/img/phot/Phot2Conc_results_tab.png)

and presented in the form of concentration, N_p, or photon distribution:

![image info](./docs/img/phot/Phot2Conc_results_dist.png)

The errors displayed in the RESULTS window can be calculated in two ways. Errors as SD switch changes between them:

![image info](./docs/img/phot/Phot2Conc_SD_Error.png)
       
   In the first way (unmarked checkbox), the error is returned as the mean over the maximal errors calculated for each pixel. Those errors include errors for $V_0$ and the molecular brightness.

   The second error calculation method (marked checkbox) returns the standard deviation $SD$, calculated from all pixels, and divided by the square root of the number of all pixels.

##### **Export results**

During calculation, the data will be automatically exported according to rules marked in the export panel.   
    
![image info](./docs/img/phot/Phot2Conc_results_export.png)

"to array" means that it will create the file containing the array (size of the image) containing a number of photons, molecules, or concentration in a given pixel.    
"to heatmap" means that the heatmap will be exported as the _.png_ file.   

To export the averaged data as a table, press the "Export all data" button.

![image info](./docs/img/phot/Phot2Conc_results_export_all.png)

## References
[1]<a name="ref_1"></a> Enderlein, Jörg, and Ingo Gregor. "[Using fluorescence lifetime for discriminating detector afterpulsing in fluorescence-correlation spectroscopy](https://doi.org/10.1063/1.1863399)." Review of scientific instruments 76.3 (2005).     
[2]<a name="ref_2"></a> Kapusta, Peter, et al. "[Fluorescence lifetime correlation spectroscopy](https://doi.org/10.1007/s10895-006-0145-1)." Journal of Fluorescence 17 (2007): 43-48.

### Acknowledgement
This work was funded by the Polish Science Fund within the framework of the Virtual Research Institute; grant WIB-1/2020-O11 - WIB_HERO.
