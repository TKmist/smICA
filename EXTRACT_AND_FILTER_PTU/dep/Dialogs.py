with dpg.file_dialog(directory_selector=False,
                    label = 'Select PTU files',
                    width = 1000,
                    height = 800,
                    show=False,
                    file_count=5,
                    
                    default_path='samples',
                    callback=callback_open_folder,
                    cancel_callback=callback_empty,
                    tag="Open_file_dialog",
                    modal=False
                   ):
    
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    dpg.add_file_extension(".ptu", color=(0, 255, 0, 255))
    
    
dpg.add_file_dialog(directory_selector=True,
                    label = 'Select PTU folder',
                    width = 1000,
                    height = 800,
                    show=False,
                    file_count=5,
                    
                    default_path='samples',
                    callback=callback_open_folder,
                    cancel_callback=callback_empty,
                    tag="PTU_dir_dialog",
                    modal=False
                   )
    
    
    
    
