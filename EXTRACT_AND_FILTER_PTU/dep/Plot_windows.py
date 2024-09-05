
    



with dpg.window(label="Lifetime Channel 1", width=init_widths['plot_window'], height=init_heights['plot_window'],pos=init_position['plot_window_ch_1'],tag='plot_window_ch1',show=True):
    dpg.add_text("Click and drag the middle mouse button over the top plot!")

    



    
    with dpg.plot(no_title=True,height=300, callback=query_ch1, query=False, no_menus=True, width=482,tag='plt_1_ch_1',show=True):
        dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_chan1",log_scale=False)
        dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_chan1",log_scale=True)
        dpg.add_line_series(sindatax1, sindatay1, parent='yaxis_chan1',tag="tag_series_ch_1")
        dpg.add_drag_line(label="Lower limit",
                          tag='L_dline_ch1' ,
                          color=[255, 100, 0, 255],
                          default_value=0.0,
                          callback=callback_dragline,
                          show = False,
                          thickness = drag_line_thickness
                         )
        dpg.add_drag_line(label="Upper limit",
                          tag='U_dline_ch1',
                          color=[255, 0, 100, 255],
                          default_value=1.0,
                          callback=callback_dragline,
                          show = False,
                          thickness = drag_line_thickness
                         )
    
    
    with dpg.plot(no_title=True, height=300, no_menus=True, width=482,tag='plt_2_ch_1',show=True):
        dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_chan1_zoom",log_scale=False)
        dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_chan1_zoom",log_scale=True)
        dpg.add_line_series(sindatax1, sindatay1, parent="yaxis_chan1_zoom",tag="tag_series_ch_1_zoom")
        
    with dpg.group(tag='LIMITS_ch_1',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='bottom_limit_ch1',
                          width = init_widths['bottom_limit_ch1'],
                         
                         format = 'Time > %.3f [ns]',
                         
                         
                         speed = 0.01,
                         callback = callback_query,
                           enabled = False
                        
                        )
        dpg.add_drag_float(label='',
                          tag='upper_limit_ch1',
                          width = init_widths['upper_limit_ch1'],
                         
                         format = 'Time < %.3f [ns]',
                         
                         
                         speed = 0.01,
                         callback = callback_query, 
                           enabled = False
                        )
        dpg.add_button(label='RESET',
                          tag='reset_button_ch1',
                          width = init_widths['reset_button'],
                         
                         
                         
                         
                         
                         callback = callback_reset_range, 
                       enabled = False
                        )
    dpg.add_separator(tag ='CH_1_sep_1',show=True)
    
    dpg.add_checkbox(tag='use_as_statistical_filters_chkbx_ch_1',
                             label = 'Use statistical filters',
                         default_value=False,show=True,enabled=True,
                     callback=calllback_use_stat_filters_chbx
                            )
    dpg.add_button(label='Calculate filters',
                          tag='Remove_bgd_butt_ch_1',
                          width = init_widths['Remove_bgd_butt_ch_1'],
                         
                         
                         
                         
                         
                         callback = show_br_fltr_wndw,
                         enabled = False,
                   show=False
                        )
    
    
    
    
    
    with dpg.table(header_row=True,
                      width=init_widths['List_of_filters_ch1'],
                      height=init_heights['List_of_filters_ch1'],
                      scrollY=True,
                      policy=dpg.mvTable_SizingFixedFit,
                      borders_innerV =True,
                      tag='filters_ch_1_tab_list_tag',
                  show =False):

        
        
        dpg.add_table_column(label = '#.',width_fixed=True)
        dpg.add_table_column(label = 'Filter name',width_stretch=True)
        dpg.add_table_column(label = '',width_fixed=True)
        
        
with dpg.window(label="Lifetime Channel 2", width=init_widths['plot_window'], height=init_heights['plot_window'],pos=init_position['plot_window_ch_2'],tag='plot_window_ch2',show=True):
    dpg.add_text("Click and drag the middle mouse button over the top plot!")


    
        
        
        


    
    with dpg.plot(no_title=True, height=300, callback=query_ch2, query=False, no_menus=True, width=482,tag='plt_1_ch_2',show=True):
        dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_chan2",log_scale=False)
        dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_chan2",log_scale=True)
        dpg.add_line_series(sindatax2, sindatay2, parent='yaxis_chan2',tag="tag_series_ch_2")
        dpg.add_drag_line(label="Lower limit",
                          tag='L_dline_ch2' ,
                          color=[255, 100, 0, 255],
                          default_value=0.0,
                          callback=callback_dragline,
                          show = False,
                          thickness = drag_line_thickness
                         )
        dpg.add_drag_line(label="Upper limit",
                          tag='U_dline_ch2',
                          color=[255, 0, 100, 255],
                          default_value=1.0,
                          callback=callback_dragline,
                          show = False,
                          thickness = drag_line_thickness
                         )
        

    
    with dpg.plot(no_title=True, height=300, no_menus=True, width=482,tag='plt_2_ch_2',show=True):
        dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_chan2_zoom",log_scale=False)
        dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_chan2_zoom",log_scale=True)
        dpg.add_line_series(sindatax2, sindatay2, parent="yaxis_chan2_zoom",tag="tag_series_ch_2_zoom")
        
    with dpg.group(tag='LIMITS_ch_2',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_drag_float(label='',
                          tag='bottom_limit_ch2',
                          width = init_widths['bottom_limit_ch2'],
                         
                         format = 'Time > %.3f [ns]',
                         
                         
                         speed = 0.01,
                         callback = callback_query, 
                           enabled = False
                        )
        dpg.add_drag_float(label='',
                          tag='upper_limit_ch2',
                          width = init_widths['upper_limit_ch2'],
                         
                         format = 'Time < %.3f [ns]',
                         
                         
                         speed = 0.01,
                         callback = callback_query, enabled = False
                        )
        dpg.add_button(label='RESET',
                          tag='reset_button_ch2',
                          width = init_widths['reset_button'],
                         
                         
                         
                         
                         
                         callback = callback_reset_range, enabled = False
                        )
    dpg.add_separator(tag ='CH_2_sep_1',show=True)
    dpg.add_checkbox(tag='use_as_statistical_filters_chkbx_ch_2',
                             label = 'Use statistical filters',
                         default_value=False,show=True,enabled=True,
                     callback=calllback_use_stat_filters_chbx
                            )
    dpg.add_button(label='Calculate filters',
                          tag='Remove_bgd_butt_ch_2',
                          width = init_widths['Remove_bgd_butt_ch_2'],
                         
                         
                         
                         
                         
                         callback = show_br_fltr_wndw,
                         enabled = False,
                   show=False
                        )
    
    
    
    
    
    with dpg.table(header_row=True,
                      width=init_widths['List_of_filters_ch2'],
                      height=init_heights['List_of_filters_ch1'],
                      scrollY=True,
                      policy=dpg.mvTable_SizingFixedFit,
                      borders_innerV =True,
                      tag='filters_ch_2_tab_list_tag',
                  show =False):

        
        
        dpg.add_table_column(label = '#.',width_fixed=True)
        dpg.add_table_column(label = 'Filter name',width_stretch=True)
        dpg.add_table_column(label = '',width_fixed=True)

with dpg.window(label="Options", width=init_widths['Options'], height=init_heights['Options'],pos=init_position['Options'],tag='Options',show=True,no_close =True):
    dpg.add_text('MODE:',tag='mode_text')
    dpg.add_text('Remove additional lines?')
    
    with dpg.group(tag='line_skip_group',horizontal=True,horizontal_spacing=group_spacer):
        dpg.add_checkbox(tag='skip_lines_check',
                         default_value=True,
                         callback=callback_skip_lines_check)
        dpg.add_drag_int(label='',
                          tag='skip_lines_drag',
                          width = -1,
                         default_value =15,
                         
                         
                         
                         speed = 1,
                         
                           enabled = True
                        )
        
        
with dpg.window(label="Files", width=init_widths['Files_window'], height=init_heights['Files_window'],pos=init_position['Files_window'],tag='Files_window',show=True):
    
    list_box = dpg.add_listbox(items=files,
                               width=init_widths['file_box'],
                               num_items=22,
                               tag='file_box',
                               callback=callback_listbox
                              )
    dpg.add_button(label='Apply to single PTU file',
                          tag='apply_to_file',
                          width = init_widths['apply_button'],
                         
                         
                         
                         
                         
                         callback = callback_apply_to_single_ptus,
                        user_data = dpg.get_value('file_box'),
                   enabled = False
                        )
    dpg.add_button(label='Apply to extract from all PTU files',
                          tag='apply_to_all',
                          width = init_widths['apply_button'],
                         
                         
                         
                         
                         
                         callback = callback_apply_to_all_ptus, enabled = False
                        )
    dpg.add_separator(tag ='FW_sep_1',show=True)
    

