


log_it('Files_window - loaded on '+str(datetime.datetime.now()),'a')
    
    
    
with dpg.window(label='',
                pos=init_position['file_window'],
                width=init_widths['file_window'],
                height=init_heights['file_window'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='file_window',
                show=True
               ):        
    
    
    
    
    list_box = dpg.add_listbox(items=files,
                               width=init_widths['file_box'],
                               num_items=11,
                               tag='file_box',
                               callback=callback_listbox
                              )
    
    dpg.add_separator(tag ='sep_left_6',show=True)
    
    
    dpg.add_text(default_value='CALCULATE',show=True,tag='single_calc') 
    
    dpg.add_separator(tag ='FILES_mid_sep_1',show=True)
    
     
    dpg.add_button(label="Calculate single",
               callback=callback_calculate,
               width = init_widths['Calculate_button'],
               tag='Calculate_button',
               show=True,enabled=True
              )
    dpg.bind_item_theme('Calculate_button', 'fit_button_theme')
    with dpg.tooltip('Calculate_button'):
        dpg.add_text("Press to make calculation on single file.")
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
            
            
            
    dpg.add_button(label="Add to Results",
               callback=add_single_result_to_DF,
               width = init_widths['add_to_res_single_button'],
               tag='add_to_res_single_button',
               show=True,enabled=True
              )
    dpg.bind_item_theme('add_to_res_single_button', 'fit_button_theme')
    with dpg.tooltip('add_to_res_single_button'):
        dpg.add_text("Press to add current calculation to dataframe.") 
    

    dpg.add_text(default_value='CALCULATE ALL',show=True,tag='All_calc') 
    
    dpg.add_separator(tag ='FILES_mid_sep_2',show=True)
    
    dpg.add_button(label="Calculate all",
               callback=callback_calculate_all,
               width = init_widths['Calculate_all_button'],
               tag='Calculate_all_button',
               show=True,enabled=True
              )
    dpg.bind_item_theme('Calculate_all_button', 'fit_button_theme')
    with dpg.tooltip('Calculate_all_button'):
        dpg.add_text("Press to make calculation on all files.")
    
        
    
    
    
    dpg.add_text(default_value='EXPORT',show=True,tag='export_text') 
    
    dpg.add_separator(tag ='FILES_mid_sep_3',show=True)
    
    dpg.add_text(default_value='Export Images as arrays',show=True,tag='exp_data_to_img_csv')
    with dpg.group(tag='save_Photons_arrays_chekcs_group',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_checkbox(label='Photons to array.', tag='Photons_array_checkbox',default_value = True)
        dpg.add_checkbox(label='Photons to heatmap.', tag='Photons_Hmaps_checkbox',default_value = False)
        
    with dpg.group(tag='save_arrays_chekcs_group',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_checkbox(label='N_p to array.', tag='Np_array_checkbox',default_value = True)
        dpg.add_checkbox(label='N_p to heatmap.', tag='Np_Hmaps_checkbox',default_value = False)
        
    with dpg.group(tag='save_Hmaps_chekcs_group',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_checkbox(label='Conc. to array.', tag='C_array_checkbox',default_value = True)
        dpg.add_checkbox(label='Conc. to heatmap.', tag='C_Hmaps_checkbox',default_value = False)
    dpg.add_button(label="Export all data",
               callback=lambda: dpg.show_item('file_dialog_export'),
               width = init_widths['Export_all_button'],
               tag='Export_all_button',
               show=True,enabled=True
              )
    dpg.bind_item_theme('Export_all_button', 'fit_button_theme')
    with dpg.tooltip('Export_all_button'):
        dpg.add_text("Press to make calculation on all files.")
        
        

