
log_it('Dialog - loaded on '+str(datetime.datetime.now()),'a')
dpg.add_file_dialog(directory_selector=True,
                    label = 'Select time trace directory',
                    width = init_widths['TT_file_dialog_id_ch_1'],
                    height = init_heights['TT_file_dialog_id_ch_1'],
                    show=False,
                    file_count=5,
                    default_path=last_directory,
                    callback=callback_TT_directory_select,
                    cancel_callback=callback_empty,
                    tag="TT_file_dialog_id_ch_1",
                    modal=False
                   )
dpg.add_file_dialog(directory_selector=True,
                    label = 'Select time trace directory',
                    width = init_widths['TT_file_dialog_id_ch_2'],
                    height = init_heights['TT_file_dialog_id_ch_2'],
                    show=False,
                    file_count=5,
                    default_path=last_directory,
                    callback=callback_TT_directory_select,
                    cancel_callback=callback_empty,
                    tag="TT_file_dialog_id_ch_2",
                    modal=False
                   )
dpg.add_file_dialog(directory_selector=True,
                    label = 'Select ROI',
                    width = init_widths['ROI_folder_dialog_id'],
                    height = init_heights['ROI_folder_dialog_id'],
                    show=False,
                    file_count=5,
                    default_path=last_directory,
                    callback=callback_ROI_directory_select,
                    cancel_callback=callback_empty,
                    tag="ROI_folder_dialog_id",
                    modal=False
                   )



dpg.add_file_dialog(directory_selector=True,
                    label = 'Select working directory',
                    width = init_widths['file_dialog_id'],
                    height = init_heights['file_dialog_id'],
                    show=False,
                    file_count=5,
                    default_path=last_directory,
                    callback=callback_directory_select,
                    cancel_callback=callback_empty,
                    tag="file_dialog_id",
                    modal=False
                   )


dpg.add_file_dialog(directory_selector=True,
                    label = 'Select PTU folder to extract',
                    width = init_widths['file_dialog_id'],
                    height = init_heights['file_dialog_id'],
                    show=False,
                    file_count=5,
                    default_path=last_directory,
                    callback=callback_PTU_directory_select,
                    cancel_callback=callback_empty,
                    tag="PTU_file_dialog_id",
                    modal=False
                   )


with dpg.file_dialog(directory_selector=False,
                    label = 'Select ROI',
                    default_filename = '*.dat',
                    width = init_widths['file_dialog_id'],
                    height = init_heights['file_dialog_id'],
                    show=False,
                    file_count=10,
                    default_path=last_directory,
                    callback=import_ROI,
                    cancel_callback=callback_empty,
                    tag="Select_ROI_dialog",
                    modal=False
                   ):
    dpg.add_file_extension("{.dat}")
    
with dpg.file_dialog(directory_selector=False,
                    show=False,
                    file_count=15,
                    default_path=last_directory,
                    width = init_widths['file_dialog_export'],
                    height = init_heights['file_dialog_export'],
                    callback=Export_result_dataframe_to_file,
                    cancel_callback=callback_empty,
                    tag="file_dialog_export",
                    modal=False):
    '''Dialog window for exporting the results of the fitting.'''
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    dpg.add_file_extension("{.xlsx,.csv,.dat}")
    dpg.add_file_extension(".xlsx", color=(255, 0, 255, 255), custom_text="[Excel]")
    dpg.add_file_extension(".dat", color=(255, 255, 0, 255), custom_text="[DAT]")
    dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[CSV]")
    dpg.add_file_extension(".pickle", color=(0, 255, 255, 255), custom_text="[Pandas]")
    
    

    
with dpg.file_dialog(directory_selector=False,
                    label = 'Select callibration file',
                    default_filename = '.',
                    width = init_widths['Calib_file_dialog_id'],
                    height = init_heights['Calib_file_dialog_id'],
                    show=False,
                    file_count=10,
                    default_path=last_directory,
                    callback=Load_Save_Calib_file,
                    cancel_callback=callback_empty,
                    tag="Calib_file_dialog_id",
                    modal=False
                   ):
    
    
    dpg.add_file_extension(".json", color=(0, 255, 0, 255), custom_text="[JSON]")
    

