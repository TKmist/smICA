
log_it('FCS_window - loaded on '+str(datetime.datetime.now()),'a')
with dpg.window(label='',
                pos=init_position['FCS_window'],
                width=init_widths['FCS_window'],
                height=init_heights['FCS_window'],
                no_move=True,
                no_close=True,
                no_collapse=True,
                no_title_bar=True,
                no_resize=True,
                tag='FCS_window',
                show=True
               ):
    dpg.add_text(default_value='FCS CALLIBRATION DATA',show=True,tag='FCS_CALLIB')
    
    dpg.add_separator(tag ='FCS_top_sep',show=True)
    
    dpg.add_button(label="Load callibration data",
                   callback=lambda: dpg.configure_item("Calib_file_dialog_id",show=True,user_data = 'Load_calib_button'),
                   width = init_widths['Load_calib_button'],
                   tag='Load_calib_button',
                   show=True,enabled=True
                  )
    dpg.bind_item_theme('Load_calib_button', 'fit_button_theme')
    dpg.add_button(label="Save callibration data",
                   callback=lambda: dpg.configure_item("Calib_file_dialog_id",show=True,user_data = 'Save_calib_button'),
                   width = init_widths['Save_calib_button'],
                   tag='Save_calib_button',
                   show=True,enabled=True
                  )
    dpg.bind_item_theme('Save_calib_button', 'fit_button_theme')
    dpg.add_separator(tag ='FCS_mid_sep_1',show=True)
    
    
    dpg.add_text(default_value='Channel 1',show=True,tag='FCS_pm_ch_1')
    
    with dpg.group(tag='Omega_Input_group_ch_1',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='omega_input_ch_1',
                          width = init_widths['omega_input_ch_1'],
                         default_value =0.2,
                         format = '\u03C9\u2080 = %.3f',
                         max_value = 0.5,
                         min_value = 0.1,
                         speed = 0.001,
                         callback = callback_omega_input
                        )
        with dpg.tooltip('omega_input_ch_1'):
            dpg.add_text("Value of the \u03C9\u2080 from the FCS callibration measurements.")
        
        dpg.add_drag_float(label='',
                          tag='omega_err_input_ch_1',
                          width = init_widths['omega_err_input_ch_1'],
                         default_value =0.02,
                         format = '\u00B1 %.3f [\u03BCm]',
                         max_value = 0.5,
                         min_value = 0.001,
                         speed = 0.001,
                         callback = callback_omega_err_input
                        )
        with dpg.tooltip('omega_err_input_ch_1'):
            dpg.add_text("Value of error for the \u03C9\u2080 from the FCS callibration measurements.")
            
    with dpg.group(tag='kappa_Input_group_ch_1',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='kappa_input_ch_1',
                          width = init_widths['kappa_input_ch_1'],
                         default_value =5.0,
                         format = '\u03BA = %.2f',
                         max_value = 20.5,
                         min_value = 2.5,
                         speed = 0.01,
                         callback = callback_kappa_input
                        )
        with dpg.tooltip('kappa_input_ch_1'):
            dpg.add_text("Value of the \u03BA from the FCS callibration measurements.")
        
        dpg.add_drag_float(label='',
                          tag='kappa_err_input_ch_1',
                          width = init_widths['kappa_err_input_ch_1'],
                         default_value =0.5,
                         format = '\u00B1 %.2f',
                         max_value = 20.5,
                         min_value = 0.01,
                         speed = 0.01,
                         callback = callback_kappa_err_input
                        )
        with dpg.tooltip('kappa_err_input_ch_1'):
            dpg.add_text("Value of error for the \u03BA from the FCS callibration measurements.")
    with dpg.group(tag='focal_vol_Input_group_ch_1',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='focal_vol_input_ch_1',
                          width = init_widths['focal_vol_input_ch_1'],
                         default_value =VEFF(dpg.get_value('omega_input_ch_1'),dpg.get_value('kappa_input_ch_1'),dpg.get_value('omega_err_input_ch_1'),dpg.get_value('kappa_err_input_ch_1'))[0],
                         format = 'V\u2080 = %.3f',
                         max_value = 2.5,
                         min_value = 0.05,
                         speed = 0.001,
                         enabled=False
                         
                        )
        with dpg.tooltip('focal_vol_input_ch_1'):
            dpg.add_text("Value of the V\u2080 calculated using \u03C9\u2080 and \u03BA. This field is read-only.")
        
        dpg.add_drag_float(label='',
                          tag='focal_vol_err_input_ch_1',
                          width = init_widths['focal_vol_err_input_ch_1'],
                         default_value =VEFF(dpg.get_value('omega_input_ch_1'),dpg.get_value('kappa_input_ch_1'),dpg.get_value('omega_err_input_ch_1'),dpg.get_value('kappa_err_input_ch_1'))[1],
                         format = '\u00B1 %.3f [fL]',
                         max_value = 2.5,
                         min_value = 0.05,
                         speed = 0.001,
                        enabled=False
                         
                        )
        with dpg.tooltip('focal_vol_err_input_ch_1'):
            dpg.add_text("Value of error for the V\u2080 calculated using \u03C9\u2080 and \u03BA. This field is read-only.")
    with dpg.group(tag='Brightness_Input_group_ch_1',horizontal=True,horizontal_spacing=group_spacer):
            dpg.add_drag_int(label='',
                              tag='Brightness_input_ch_1',
                              width = init_widths['Brightness_input_ch_1'],
                             default_value =1,
                             format = '<Mol. brightness> = %.d',
                             max_value = 1e5,
                             callback = callback_Brightness_input
                            )
            with dpg.tooltip('Brightness_input_ch_1'):
                dpg.add_text("Mean value of the molecular brightness. Optionally input your own known value.")
            
            dpg.add_drag_int(label='',
                              tag='Brightness_err_input_ch_1',
                              width = init_widths['Brightness_err_input_ch_1'],
                             default_value =1,
                             format = '\u00B1 %.d',
                             max_value = 1e5,
                             callback = callback_Brightness_err_input)
            with dpg.tooltip('Brightness_err_input_ch_1'):
                dpg.add_text("Standard deviation value of the molecular brightness. Optionally input your own known value.")
    
    dpg.add_separator(tag ='FCS_mid_sep_2',show=True)
    
    dpg.add_text(default_value='Channel 2',show=True,tag='FCS_pm_ch_2')
    with dpg.group(tag='Omega_Input_group_ch_2',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='omega_input_ch_2',
                          width = init_widths['omega_input_ch_2'],
                         default_value =0.2,
                         format = '\u03C9\u2080 = %.3f',
                         max_value = 0.5,
                         min_value = 0.1,
                         speed = 0.001,
                         callback = callback_omega_input
                        )
        with dpg.tooltip('omega_input_ch_2'):
            dpg.add_text("Value of the \u03C9\u2080 from the FCS callibration measurements.")
        
        dpg.add_drag_float(label='',
                          tag='omega_err_input_ch_2',
                          width = init_widths['omega_err_input_ch_2'],
                         default_value =0.02,
                         format = '\u00B1 %.3f [\u03BCm]',
                         max_value = 0.5,
                         min_value = 0.001,
                         speed = 0.001,
                         callback = callback_omega_err_input
                        )
        with dpg.tooltip('omega_err_input_ch_2'):
            dpg.add_text("Value of error for the \u03C9\u2080 from the FCS callibration measurements.")
            
    with dpg.group(tag='kappa_Input_group_ch_2',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='kappa_input_ch_2',
                          width = init_widths['kappa_input_ch_2'],
                         default_value =5.0,
                         format = '\u03BA = %.2f',
                         max_value = 20.5,
                         min_value = 2.5,
                         speed = 0.01,
                         callback = callback_kappa_input
                        )
        with dpg.tooltip('kappa_input_ch_2'):
            dpg.add_text("Value of the \u03BA from the FCS callibration measurements.")
        
        dpg.add_drag_float(label='',
                          tag='kappa_err_input_ch_2',
                          width = init_widths['kappa_err_input_ch_2'],
                         default_value =0.5,
                         format = '\u00B1 %.2f',
                         max_value = 20.5,
                         min_value = 0.01,
                         speed = 0.01,
                         callback = callback_kappa_err_input
                        )
        with dpg.tooltip('kappa_err_input_ch_2'):
            dpg.add_text("Value of error for the \u03BA from the FCS callibration measurements.")
    with dpg.group(tag='focal_vol_Input_group_ch_2',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='focal_vol_input_ch_2',
                          width = init_widths['focal_vol_input_ch_2'],
                         default_value =VEFF(dpg.get_value('omega_input_ch_2'),dpg.get_value('kappa_input_ch_2'),dpg.get_value('omega_err_input_ch_2'),dpg.get_value('kappa_err_input_ch_2'))[0],
                         format = 'V\u2080 = %.3f',
                         max_value = 2.5,
                         min_value = 0.05,
                         speed = 0.001,
                         enabled=False
                         
                        )
        with dpg.tooltip('focal_vol_input_ch_2'):
            dpg.add_text("Value of the V\u2080 calculated using \u03C9\u2080 and \u03BA. This field is read-only.")
        
        dpg.add_drag_float(label='',
                          tag='focal_vol_err_input_ch_2',
                          width = init_widths['focal_vol_err_input_ch_2'],
                         default_value =VEFF(dpg.get_value('omega_input_ch_2'),dpg.get_value('kappa_input_ch_2'),dpg.get_value('omega_err_input_ch_2'),dpg.get_value('kappa_err_input_ch_2'))[1],
                         format = '\u00B1 %.3f [fL]',
                         max_value = 2.5,
                         min_value = 0.05,
                         speed = 0.001,
                        enabled=False
                         
                        )
        with dpg.tooltip('focal_vol_err_input_ch_2'):
            dpg.add_text("Value of error for the V\u2080 calculated using \u03C9\u2080 and \u03BA. This field is read-only.")
    with dpg.group(tag='Brightness_Input_group_ch_2',horizontal=True,horizontal_spacing=group_spacer):
            dpg.add_drag_int(label='',
                              tag='Brightness_input_ch_2',
                              width = init_widths['Brightness_input_ch_2'],
                             default_value =1,
                             format = '<Mol. brightness> = %.d',
                             max_value = 1e5,
                             callback = callback_Brightness_input
                            )
            with dpg.tooltip('Brightness_input_ch_2'):
                dpg.add_text("Mean value of the molecular brightness. Optionally input your own known value.")
            
            dpg.add_drag_int(label='',
                              tag='Brightness_err_input_ch_2',
                              width = init_widths['Brightness_err_input_ch_2'],
                             default_value =1,
                             format = '\u00B1 %.d',
                             max_value = 1e5,
                             callback = callback_Brightness_err_input)
            with dpg.tooltip('Brightness_err_input_ch_2'):
                dpg.add_text("Standard deviation value of the molecular brightness. Optionally input your own known value.")
