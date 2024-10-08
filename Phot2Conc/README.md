# Phot2Conc
A GUI Software for analysis of the concentration of fluorescent molecules inside living cells from single-molecule FLIM imaging data.
The script can read the files created with the _EXTRACT_FROM_PTU_FLIM.py_ script containing the data extracted from the _.ptu_ files. __Note _Phot2Conc_ script does not read the _.ptu_ files directly. It is necessary to use _EXTRACT_FROM_PTU_FLIM.py_ first!__

Alternatively to GUI script, one can use the [command line tool](#HTU_CLI) Phot2Conc_CLI.py.
<a id='HTU_GUI'></a>
## HOW TO USE

1. To run the script, type in the command line:

            python Phot2Conc.py    

    It will start the graphical interface that will help to navigate through the process,    
    ![image info](./docs/figures/Phot2Conc_init.png)
    
2. At the very beginning, we suggest inputting the calibration values either from the file    

    ![image info](./docs/figures/Phot2Conc_calib_load.png)
    
    or manually.    
    
    ![image info](./docs/figures/Phot2Conc_calib_manual_input.png)
    
    __Note. When you load the file, it needs to have a proper structure.__ For more details check the Calliberation_exmaple files (_.json_) in the smaples folder.
   The calibration values provided manually can be saved by pressing the save button

   ![image info](./docs/figures/Phot2Conc_calib_save.png)
    
4. <a id='PTU_folder'></a> Browse for the folder containing the _.ptu_ files (should be the same folder where the output files of the _EXTRACT_FROM_PTU_FLIM.py_ script were created).   

    ![image info](./docs/figures/Phot2Conc_Browse_for_ptu.png)
    
    This will load all data stored in the given folder. __Note. The folder should contain only _.ptu_ files and those created by the _EXTRACT_FROM_PTU_FLIM.py_ script. Other files can break the script!__    
    
    When the data are loaded, the list of files will appear:    
    
    ![image info](./docs/figures/Phot2Conc_data_loaded_files.png)
    
    The metadata of each file is shown in the _PTU metadata_ panel:    
    
    ![image info](./docs/figures/Phot2Conc_data_metadata.png)
    
    The image from each channel is shown in the corresponding windows:    
    
    ![image info](./docs/figures/Phot2Conc_data_image.png)
    
    In this example, the file contains data only for Channel 2.    
  
7. You may wish to limit the image analysis to a given region of interest (created in the SymPhoTime software or ImageJ and rewritten with the _REWRITE_ROI.py_ script). For this purpose, press the 'Browse for the ROI folder' button:    

    ![image info](./docs/figures/Phot2Conc_data_ROI.png)
    
    Resulting in cutting off unwanted image areas,    
    
    ![image info](./docs/figures/Phot2Conc_image_ROI.png)
    
5.<a id='HT_export'></a> If you wish to export the settings of the workspace to run the command line tool press Menu and click Export settings:

   ![image info](./docs/figures/Phot2Conc_settings_export.png)
   
   This will produce a _workspace_info.json_ file located in the [folder containing PTU files](#PTU_folder).
   
9. To analyze the images and calculate concentrations for a single image, press 'Calculate single',    

    ![image info](./docs/figures/Phot2Conc_caluclate_single.png)
    
    The result will be displayed in these tables:   
    
    ![image info](./docs/figures/Phot2Conc_results_tab.png)
    
    and presented in the form of concentration, N_p, or photon distribution:
    
    ![image info](./docs/figures/Phot2Conc_results_dist.png)

10. The errors displayed in the RESULTS window can be calculated in two ways. Errors as SD switch changes between them:

    ![image info](./docs/figures/Phot2Conc_SD_Error.png)
       
   In the first way (unmarked checkbox), the error is returned as the mean over the maximal errors calculated for each pixel. Those errors include errors for $V_0$ and the molecular brightness.

   The second error calculation method (marked checkbox) returns the standard deviation $SD$, calculated from all pixels, and divided by the square root of the number of all pixels.

   
11. Press 'Add to results' to store the results in the memory.    
    
    ![image info](./docs/figures/Phot2Conc_add_to_results.png)
    
12. Alternatively, one can perform automatic analysis for all listed files by pressing 'Calculate all':    

    ![image info](./docs/figures/Phot2Conc_caluclate_all.png)
    
    In this mode, results will be stored automatically in the memory.
13. During calculation, the data will be automatically exported according to rules marked in the export panel.   
    
    ![image info](./docs/figures/Phot2Conc_results_export.png)
    
    "to array" means that it will create the file containing the array (size of the image) containing a number of photons, molecules, or concentration in a given pixel.    
    "to heatmap" means that the heatmap will be exported as the _.png_ file.   

14. To export the averaged data as a table, press the "Export all data" button.

    ![image info](./docs/figures/Phot2Conc_results_export_all.png)

<a id='HTU_CLI'></a>

## HOW TO USE Phot2Conc_CLI.py

To run the script, type in the command line:

            python Phot2Conc_CLI.py ARG1 ARG2 ARG3

`ARG1` is the path to JSON workspace file. An example of the JSON workspace file is located in: samples/PTU/workspace_info.json
The file can be also generated using the [GUI](#HTU_GUI), by clicking the [Export settings](#HT_export) in the Menu.    

`ARG2` is the path to output folder where the result file, in the format "%Y%m%d_%H%M_results", will be saved.   

`ARG3` is the format in which the result file will be saved. There are four formats allowed: Excel (.xlsx), data, (.dat), csv (.csv), and pickle (.pickle - binary file for pandas DataFrame).


