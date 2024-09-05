dpg.add_file_dialog(directory_selector=True,
                    label = 'Select source ROI folder',
                    width =400,
                    height=300,
                    
                    show=False,
                    file_count=5,

                    callback=callback_open_source_folder,
                    cancel_callback=callback_empty,
                    tag="Source_file_dialog",
                    modal=False
                   )


dpg.add_file_dialog(directory_selector=True,
                    label = 'Select target ROI folder',
                    show=False,
                    width =400,
                    height=300,

                    file_count=5,

                    callback=callback_open_target_folder,
                    cancel_callback=callback_empty,
                    tag="Target_file_dialog",
                    modal=False
                   )
