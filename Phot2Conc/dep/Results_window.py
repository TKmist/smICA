log_it('Results_window - loaded on '+str(datetime.datetime.now()),'a')

with dpg.window(label='',
                pos=init_position['results_window'],
                width=init_widths['results_window'],
                height=init_heights['results_window'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='results_window',
                show=True
               ):
    '''Window containing Results'''
    dpg.add_text(default_value='RESULTS',show=True,tag='RES_pm')
    
    dpg.add_separator(tag ='RESULTS_top_sep',show=True)
    
    
    dpg.add_text(default_value='Channel 1',show=True,tag='RES_pm_ch_1')
    with dpg.group(tag='single_phot_group_ch_1',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='sinle_phot_output_ch_1',
                          width = init_widths['sinle_phot_output_ch_1'],
                         default_value = 0,
                         format = 'Photons per pixel = %.1f',
                         
                         
                         
                        
                         enabled=False
                         
                        )
        with dpg.tooltip('sinle_phot_output_ch_1'):
            dpg.add_text("Mean number of photons per pixel.")
        dpg.add_drag_float(label='',
                          tag='sinle_phot_err_output_ch_1',
                          width = init_widths['sinle_phot_err_output_ch_1'],
                         default_value = 0,
                         format = '\u00B1 %.3f',
                         
                         
                         
                        
                         enabled=False
                         
                        )
        with dpg.tooltip('sinle_phot_err_output_ch_1'):
            dpg.add_text("SD of number of photons per pixel.")
    
    with dpg.group(tag='single_mols_group_ch_1',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='sinle_mols_output_ch_1',
                          width = init_widths['sinle_mols_output_ch_1'],
                         default_value = 0,
                         format = '<N_p> per pixel = %.3f',
                         
                         
                         
                        
                         enabled=False
                         
                        )
        with dpg.tooltip('sinle_mols_output_ch_1'):
            dpg.add_text("Mean number of molecules per pixel.")
        dpg.add_drag_float(label='',
                          tag='sinle_mols_err_output_ch_1',
                          width = init_widths['sinle_mols_err_output_ch_1'],
                         default_value = 0,
                         format = '\u00B1 %.3f',
                         
                         
                         
                        
                         enabled=False
                         
                        )
        with dpg.tooltip('sinle_mols_err_output_ch_1'):
            dpg.add_text("SD of number of molecules per pixel.")
        
    with dpg.group(tag='single_conc_group_ch_1',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='single_conc_output_ch_1',
                          width = init_widths['single_conc_output_ch_1'],
                         default_value =0,
                         format = '<C> = %.3f',
                         
                         
                         
                        enabled=False
                         
                        )
        with dpg.tooltip('single_conc_output_ch_1'):
            dpg.add_text("Mean concentration. Average over entire image/ROI.")
        dpg.add_drag_float(label='',
                          tag='single_conc_err_output_ch_1',
                          width = init_widths['single_conc_err_output_ch_1'],
                         default_value =0,
                         format = '\u00B1 %.3f [nM]',
                         
                         
                         
                        enabled=False
                         
                        )
        with dpg.tooltip('single_conc_err_output_ch_1'):
            dpg.add_text("SD of concentration. Average over entire image/ROI.")
    with dpg.group(tag='empty_group_ch_1',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='empty_output_ch_1',
                          width = init_widths['empty_output_ch_1'],
                         default_value =0,
                         format = '',
                         
                         
                         
                        enabled=False
                         
                        )
        dpg.add_drag_float(label='',
                          tag='empty_err_output_ch_1',
                          width = init_widths['empty_err_output_ch_1'],
                         default_value =0,
                         format = '',
                         
                         
                         
                        enabled=False
                         
                        )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

                              
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    dpg.add_separator(tag ='RESULTS_mid_sep_1',show=True)
    
    
    dpg.add_text(default_value='Channel 2',show=True,tag='Bright_pm_ch_2')
    
    with dpg.group(tag='single_phot_group_ch_2',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='sinle_phot_output_ch_2',
                          width = init_widths['sinle_phot_output_ch_2'],
                         default_value = 0,
                         format = 'Photons per pixel = %.1f',
                         
                         
                         
                        
                         enabled=False
                         
                        )
        with dpg.tooltip('sinle_phot_output_ch_2'):
            dpg.add_text("Mean number of photons per pixel.")
        dpg.add_drag_float(label='',
                          tag='sinle_phot_err_output_ch_2',
                          width = init_widths['sinle_phot_err_output_ch_2'],
                         default_value = 0,
                         format = '\u00B1 %.3f',
                         
                         
                         
                        
                         enabled=False
                         
                        )
        with dpg.tooltip('sinle_phot_err_output_ch_2'):
            dpg.add_text("SD of number of photons per pixel.")
    
    with dpg.group(tag='single_mols_group_ch_2',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='sinle_mols_output_ch_2',
                          width = init_widths['sinle_mols_output_ch_2'],
                         default_value = 0,
                         format = '<N_p> per pixel = %.3f',
                         
                         
                         
                        
                         enabled=False
                         
                        )
        with dpg.tooltip('sinle_mols_output_ch_2'):
            dpg.add_text("Mean number of molecules per pixel.")
        dpg.add_drag_float(label='',
                          tag='sinle_mols_err_output_ch_2',
                          width = init_widths['sinle_mols_err_output_ch_2'],
                         default_value = 0,
                         format = '\u00B1 %.3f',
                         
                         
                         
                        
                         enabled=False
                         
                        )
        with dpg.tooltip('sinle_mols_err_output_ch_2'):
            dpg.add_text("SD of number of molecules per pixel.")
        
    with dpg.group(tag='single_conc_group_ch_2',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='single_conc_output_ch_2',
                          width = init_widths['single_conc_output_ch_2'],
                         default_value =0,
                         format = '<C> = %.3f',
                         
                         
                         
                        enabled=False
                         
                        )
        with dpg.tooltip('single_conc_output_ch_2'):
            dpg.add_text("Mean concentration. Average over entire image/ROI.")
        dpg.add_drag_float(label='',
                          tag='single_conc_err_output_ch_2',
                          width = init_widths['single_conc_err_output_ch_2'],
                         default_value =0,
                         format = '\u00B1 %.3f [nM]',
                         
                         
                         
                        enabled=False
                         
                        )
        with dpg.tooltip('single_conc_err_output_ch_2'):
            dpg.add_text("SD of concentration. Average over entire image/ROI.")
    with dpg.group(tag='empty_group_ch_2',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='empty_output_ch_2',
                          width = init_widths['empty_output_ch_2'],
                         default_value =0,
                         format = '',
                         
                         
                         
                        enabled=False
                         
                        )
        dpg.add_drag_float(label='',
                          tag='empty_err_output_ch_2',
                          width = init_widths['empty_err_output_ch_2'],
                         default_value =0,
                         format = '',
                         
                         
                         
                        enabled=False
                         
                        )
    dpg.add_separator(tag ='RESULTS_bott2_sep',show=True)
    dpg.add_checkbox(label='Errors as SD', tag='Error_type_checkbox',default_value = False,callback=callback_calculate)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

                              
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    

    
    
    
