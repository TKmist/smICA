
log_it('PTU_an_window - loaded on '+str(datetime.datetime.now()),'a')
with dpg.window(label='',
                pos=init_position['PTU_DATA_window'],
                width=init_widths['PTU_DATA_window'],
                height=init_heights['PTU_DATA_window'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='PTU_DATA_window',
                show=True
               ):
        
    dpg.add_text(default_value='PTU metadata',show=True,tag='PTU_meta') 
    
    dpg.add_separator(tag ='PTU_DATA_mid_sep_1',show=True)
    
    with dpg.group(tag='Resol_Pix_size_group',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_input_text(label='',
                          tag='Resolution_output',
                          width = init_widths['Resolution_output'],
                         default_value ='Resolution: ',
                         
                         
                         
                         
                        readonly=True,
                         enabled=False
                         
                        )
        with dpg.tooltip('Resolution_output'):
            dpg.add_text("The resolution of the PTU image.")
        
        dpg.add_drag_int(label='',
                          tag='Pixel_size_output',
                          width = init_widths['Pixel_size_output'],
                         default_value =0,
                         format = 'Pixel size: %i [nm]',
                         
                         
                         
                        enabled=False
                         
                        )
        with dpg.tooltip('Pixel_size_output'):
            dpg.add_text("Size of the of the pixell.")
    with dpg.group(tag='Frames_and_PD_group',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_int(label='',
                          tag='Nframes_output',
                          width = init_widths['Nframes_output'],
                         default_value =0,
                         format = '# of frames: %i',
                         
                         
                         
                         enabled=False
                         
                        )
        with dpg.tooltip('Nframes_output'):
            dpg.add_text("Number of frames in the PTU file.")
        
        dpg.add_drag_float(label='',
                          tag='Pixel_dwell_output',
                          width = init_widths['Pixel_dwell_output'],
                         default_value =0,
                         format = 'Pixel dweel: %.2f [\u00B5s]',
                         
                         
                         
                        enabled=False
                         
                        )
        with dpg.tooltip('Pixel_dwell_output'):
            dpg.add_text("Value of the pixell dwell")
    
    dpg.add_text(default_value='Images',show=True,tag='PTU_roi')
    
    dpg.add_separator(tag ='PTU_DATA_mid_sep_2',show=True)
    
    
    with dpg.group(tag='ROI_check_sel_group',horizontal=True,horizontal_spacing=init_group_spacer+1):
        dpg.add_checkbox(label='ROI from files', tag='FILE_ROI_checkbox',default_value = False,callback=callback_select_roi,enabled=False)
        dpg.add_checkbox(label='Auto ROI', tag='Auto_ROI_checkbox',default_value = False,callback=callback_select_autoroi,enabled=False
                        )

    


rescalable_item.append(['PTU_DATA_window','Resolution_output','Pixel_size_output','Nframes_output'])
