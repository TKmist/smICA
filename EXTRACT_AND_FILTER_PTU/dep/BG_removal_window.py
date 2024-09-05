



win_width = init_widths['BG_removal_window']
win_height = init_heights['BG_removal_window']
VP_w = dpg.get_viewport_width()
VP_h = dpg.get_viewport_height()
posit = (int(VP_w/2-win_width/2),int(VP_h/2-win_height/2))
global fl_bg_curves_dict
fl_bg_curves_dict ={}

with dpg.window(label="Lifetime background filtering", width=win_width,
                height=win_height,
                pos=posit,
                tag='BG_removal_window',
                autosize=True,
                no_collapse=True,
                modal=True,
                show=False):
    with dpg.group(tag='fl_bg_win_group',horizontal=True,horizontal_spacing=group_spacer*5):
        with dpg.group(tag='fl_bg_curves_group'):
        
        
        
        
        
                                  
            with dpg.table(header_row=True,
                      width=init_widths['file_box'],
                      height=215,
                      scrollY=True,
                      policy=dpg.mvTable_SizingFixedFit,
                      borders_innerV =True,
                      tag='decays_tab_list_tag'):

        
        
                dpg.add_table_column(label = '#.',width_fixed=True)
                dpg.add_table_column(label = 'Decay name',width_stretch=True)
                dpg.add_table_column(label = '',width_fixed=True)
                
                
            
            
            
            
            
            dpg.add_checkbox(tag='add_bg_range',
                             label = 'Set data range for background',
                         default_value=False,
                         callback=callback_Set_background_range
                            )
            with dpg.group(tag='fl_bg_win_butt_group',horizontal=True,horizontal_spacing=group_spacer):
                dpg.add_button(label='To library',
                              tag='Add_decay_to_lib',
                              width = init_widths['Add_decay_to_lib'],
                             
                             
                             
                             
                             
                             callback = callback_add_decay_to_lib,
                            
                       enabled = False
                            )
                dpg.add_button(label='From library',
                              tag='Add_decay_from_lib',
                              width = init_widths['Add_decay_from_lib'],
                             
                             
                             
                             
                             
                             callback = callback_import_from_library,
                            
                       enabled = True
                            )
            with dpg.group(tag='fl_bg_win_filtering_routine_group'):
                dpg.add_checkbox(tag='remove_afterpulsing_chkbx',
                             label = 'Remove afterpulsing',
                         default_value=True,
                         
                            )
                
                dpg.add_button(label='Calculate filters',
                              tag='Calculate_filters',
                              width = init_widths['Calculate_filters'],
                             
                             
                             
                             
                             
                             callback = callback_Calculate_filters,
                            
                       enabled = True
                            )    
        
        
        with dpg.group(tag='fl_bg_plt_group1'):
            with dpg.plot(no_title=True,
                          height=300,
                          callback='',
                          query=False,
                          no_menus=True,
                          width=482,
                          tag='fltr_plot',
                          
                          show=True):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_tltr",log_scale=False)
                dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_tltr",log_scale=True)
                dpg.add_scatter_series([], [], parent='yaxis_tltr',tag="tag_series_fltr")
                dpg.add_scatter_series([], [],
                                    parent='yaxis_tltr',tag="tag_series_fltr_subtr")
                dpg.add_drag_line(label="Background level",
                              tag='Background_level_line' ,
                              parent = 'fltr_plot',
                              color=[100, 255, 100, 255],
                              default_value=0,
                              callback=callback_drag_Background_level_line,
                              show = False,
                              vertical =False,
                              thickness = drag_line_thickness
                             )
                dpg.add_drag_line(label="Background range lower limit",
                              tag='Background_RLL_line' ,
                              parent = 'fltr_plot',
                              color=[100, 255, 100, 255],
                              default_value=0,
                              callback=callback_drag_Background_Range_line,
                              show = False,
                              vertical =True,
                              thickness = drag_line_thickness
                             )
                dpg.add_drag_line(label="Background range upper limit",
                              tag='Background_RUL_line' ,
                              parent = 'fltr_plot',
                              color=[100, 190, 100, 255],
                              default_value=0,
                              callback=callback_drag_Background_Range_line,
                              show = False,
                              vertical =True,
                              thickness = drag_line_thickness
                             )
                dpg.add_plot_legend(location=9)
        with dpg.group(tag='fl_bg_plt_group_fltrs'):    
            with dpg.plot(no_title=True,
                          height=300,
                          callback='',
                          query=False,
                          no_menus=True,
                          width=482,
                          tag='fltr_filters_plot',
                          

                          show=False):
                dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_tltr_fltr",log_scale=False)
                dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_tltr_fltr",log_scale=True)
                dpg.add_plot_legend(location=10)
            with dpg.group(tag='fl_accpet_filters_group',horizontal=True,horizontal_spacing=group_spacer,show=False):
                    dpg.add_button(label='Decline',
                                  tag='Decline_filters',
                                  width = init_widths['Decline_filters'],
                                 
                                 
                                 
                                 
                                 
                                 callback = callback_Decline_filters,
                                
                           show =False,
                           enabled = True
                                )
                    dpg.add_button(label='Accept',
                                  tag='Accept_filters',
                                  width = init_widths['Accept_filters'],
                                 
                                 
                                 
                                 
                                 
                                 
                                
                                   callback = callback_Accept_filters,
                           show =False,
                           enabled = True
                                )
    with dpg.group(tag='fl_bg_win_group_2',horizontal=True,horizontal_spacing=group_spacer*5,show=False):
        with dpg.group(tag='fl_decay_params_group'):
            dpg.add_input_text(default_value = 'Name (optional)', multiline=False,width=init_widths['get_name'],tag='get_name')
            dpg.add_input_text(label = 'Excitation wavelentgh (eg. 485)', multiline=False,width=100,tag='get_wavelength')
            dpg.add_text('get_channel',tag='get_channel')
            
            dpg.add_text('get_tcspc_resolution',tag='get_tcspc_resolution')
            with dpg.group(tag='fl_bg_win_submit_decay',horizontal=True,horizontal_spacing=group_spacer,show=False):
                dpg.add_button(label='Cancel',
                              tag='Cancel_decay_submission',
                              width = init_widths['Cancel_decay_submission'],
                             
                             
                             
                             
                             
                             callback = callback_cancel_submission,
                            
                       show =False,
                       enabled = True
                            )
                dpg.add_button(label='Submit',
                              tag='Proceed_decay_submission',
                              width = init_widths['Proceed_decay_submission'],
                             
                             
                             
                             
                             
                             
                            
                               callback = callback_proceed_submission,
                       show =False,
                       enabled = True
                            )
        dpg.add_input_text(default_value = 'Type descrption here (opitonal)',
                               multiline=True,
                               width=init_widths['get_decay_description'],
                               tag='get_decay_description',
                               show=False)
        
        
    with dpg.group(tag='fl_bg_win_group_3',show=False):
        dpg.add_text('The Library is empty',tag='empty_library_notiffication',show=False,color=(255,0,0))
        
        with dpg.table(header_row=True,
                  width=init_widths['decays_tab_lib_list_tag'],
                  height=init_heights['decays_tab_lib_list_tag'],
                  scrollY=True,
                  policy=dpg.mvTable_SizingFixedFit,
                  tag='decays_tab_lib_list_tag',
                borders_innerV =True,
                 show=False):
            dpg.add_table_column(label = '#',width_fixed=True)
            dpg.add_table_column(label = 'Name',width_stretch=True)
            dpg.add_table_column(label = '\u03BB Exc.',width_fixed=True)
            dpg.add_table_column(label = 'Description', width_stretch=True)
            dpg.add_table_column(label = 'TCSPC resolution', width_fixed=True)
            dpg.add_table_column(label = 'TCSPC channels', width_fixed=True)
            dpg.add_table_column(label = 'Select',width_fixed=True)
        dpg.add_text('',
                     tag='No_match_notiffication',color=(255, 0, 0),
                     
                     show=False)
        with dpg.group(tag='fl_bg_win_library_load_butt_group',horizontal=True,horizontal_spacing=group_spacer):
            dpg.add_button(label='Cancel',
                              tag='Cancel_library_import',
                              width = init_widths['Cancel_library_import'],
                             
                             
                             
                             
                             
                             callback = callback_Cancel_library_import,
                            
                       show =False,
                       enabled = True
                            )
            dpg.add_button(label='Import',
                              tag='Proceed_library_import',
                              width = init_widths['Proceed_library_import'],
                             
                             
                             
                             
                             
                             callback = callback_Proceed_library_import,
                            
                       show =False,
                       enabled = True
                            )
            
        
    with dpg.group(tag='fl_bg_win_group_4',show=False):
        dpg.add_text('There is no curves to calculate. Try to set the background level or add decay from library. ',tag='no_curves_notiffication',show=False,color=(255,0,0))
        dpg.add_button(label='OK',
                              tag='OK_button',
                              width = init_widths['Cancel_library_import'],
                             
                             
                             
                             
                             
                             callback = callback_ok_button,
                            
                       show =False,
                       enabled = True
                            )
        
        
        
        
        
        
        
        
        
        
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
