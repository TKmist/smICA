

# def resizer(sender,app_data):
#     def font_size(sender,app_data):
#         font = 'DejaVu'
#         inf_w = dpg.get_viewport_width()
#         inf_h = dpg.get_viewport_height()
#         ratio_w = inf_w/inV.VIEWPORT_prop['width']
#         ratio_h = inf_h/inV.VIEWPORT_prop['height']
#         ratio = 1
#         if ratio_w < ratio_h:
#             ratio = ratio_w
#         else:
#             ratio = ratio_h
        
#         new_font_size = int(init_font_size*ratio)
#         current_font_size = new_font_size
        
#         dpg.delete_item(font)
#         dpg.delete_item('Font_registry')
#         add_font_to_registry(current_font_size)
    
#     # print('resizing')
#     init_resizable_items = []
#     cmn_resizable_items = []
#     obj_var = [eval('method_init.'+str(m)) for m in vars(method_init)]
#     for m in obj_var:
#         if type(m) == dict:
#             if 'name' in m.keys():
#                 init_resizable_items.append(m['name'])
#         else:
#             pass
#     obj_var = [eval('method_cmn.'+str(m)) for m in vars(method_cmn)]
#     for m in obj_var:
#         if type(m) == dict:
#             if 'name' in m.keys():
#                 cmn_resizable_items.append(m['name'])
#         else:
#             pass    
        
        
    
#     ratio = {'width': np.round(app_data[0]/inV.VIEWPORT_prop['width'],4),
#              'height': np.round(app_data[1]/inV.VIEWPORT_prop['height'],4)} 
#     # print(ratio)
#     inV.init_size_ratio = ratio
#     # print('==============================================================')
#     # print(method_init.__init__.__code__.co_varnames)
    
#     temp_inits = method_init.__init__.__code__.co_varnames
#     temp_inits = [v for v in temp_inits if v != 'self']
#     temp_inits = [v for v in temp_inits if v != 'size_ratio']
#     font_size(sender,app_data)
#     temp_inits_values  = {}
#     for v in temp_inits:
#         temp_inits_values[v] = eval('method_init.'+v)
    
#     method_init.__init__(inV.init_size_ratio,
#                          inV.init_left_indent,
#                          inV.init_internal_indent,
#                          inV.init_right_indent,
#                          inV.init_bottom_indent,
#                          inV.init_top_indent,
#                          inV.init_group_spacer,
#                          globalITEMS.last_directory)
    
#     for item in init_resizable_items:
#         # print(item)
#         props =eval('method_init.'+item) 
#         if 'width' in props.keys():
#             dpg.configure_item(item,width=props['width'])
#         if 'height' in props.keys():
#             dpg.configure_item(item,height=props['height'])
#         if 'pos' in props.keys():
#             dpg.configure_item(item,pos=props['pos'])
    
#     dpg.delete_item('draw_image_')
#     dpg.delete_item('drawlist1')
#     dpg.delete_item('image_id1')
#     dpg.delete_item('texture_reg1')
#     method_cmn.dpg_image1 = []
#     method_cmn.image_width1 = method_init.image_1['width']
#     method_cmn.image_height1 = method_init.image_1['height']
    
#     for i in range(0, method_cmn.image_width1):
#         for j in range(0, method_cmn.image_height1):
#             method_cmn.dpg_image1.append(80/255)
#             method_cmn.dpg_image1.append(80/255)
#             method_cmn.dpg_image1.append(80/255)
#             method_cmn.dpg_image1.append(255/255)




#     if dpg.get_item_configuration('Add_model_window')['show'] and dpg.get_value('model_input_text1') !='':
#         method_cmn.callback_stringtest1('model_input_text1',dpg.get_value('model_input_text1'))
#         with dpg.texture_registry(tag = 'texture_reg1'):
#             dpg.add_dynamic_texture(method_cmn.image_width1,
#                                     method_cmn.image_height1,
#                                     dpg_image1,
#                                     tag="image_id1"
#                                    )
#         with dpg.drawlist(width=method_cmn.image_width1,
#                           height=method_cmn.image_height1,
#                           parent = 'Add_model_window',
#                           before = 'List_all_variables_text',
#                           tag='drawlist1'
#                          ):
#             dpg.draw_image("image_id1",
#                            [0, 0],
#                            [method_cmn.image_width1,method_cmn.image_height1],
#                            parent='drawlist1',
#                            show=True,
#                            tag='draw_image_'
#                           )
#     else:
#         with dpg.texture_registry(tag = 'texture_reg1'):
#             dpg.add_dynamic_texture(method_cmn.image_width1,
#                                     method_cmn.image_height1,
#                                     method_cmn.dpg_image1,
#                                     tag="image_id1"
#                                    )
#         with dpg.drawlist(width=method_cmn.image_width1,
#                           height=method_cmn.image_height1,
#                           parent = 'Add_model_window',
#                           before = 'List_all_variables_text',
#                           tag='drawlist1'
#                          ):
#             dpg.draw_image("image_id1",
#                            [0, 0],
#                            [method_cmn.image_width1,method_cmn.image_height1],
#                            parent='drawlist1',
#                            show=True,
#                            tag='draw_image_'
#                           )
    
    
        
        

# dpg.set_viewport_resize_callback(resizer)

from Modes.Phot2conc.Phot2conc_INIT import _Phot2conc_init, _Phot2conc_vars_funct

mode_init = _Phot2conc_init(inV.init_size_ratio,
                             inV.init_left_indent,
                             inV.init_internal_indent,
                             inV.init_right_indent,
                             inV.init_bottom_indent,
                             inV.init_top_indent,
                             inV.init_group_spacer,
                             inV.init_font_size,
                             globalITEMS.last_directory,
                            )


method_cmn = _Phot2conc_vars_funct(method_init.size_ratio,
                                     method_init.group_spacer,
                                     globalITEMS.last_directory,
                                     basf
                                    )
# method_cmn.mount_fcs_handlers()

# #########################################################################
# '''Main windows of the method'''
# #########################################################################

with dpg.window(label='',
                pos=mode_init.PTU_DATA_window['pos'],
                width=mode_init.PTU_DATA_window['width'],
                height=mode_init.PTU_DATA_window['height'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='PTU_DATA_window',
                show=True
               ):
    pass

with dpg.window(label='',
                pos=mode_init.file_window['pos'],
                width=mode_init.file_window['width'],
                height=mode_init.file_window['height'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='file_window',
                show=True
               ):
    pass

with dpg.window(label = 'Channel 1',
                tag='image_window_ch1',
                width = mode_init.image_window_ch1['width'],
                height = mode_init.image_window_ch1['height'],
                pos = mode_init.image_window_ch1['pos'],
                autosize=True,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_move=True,
                no_bring_to_front_on_focus=True,
                show=True
               ):
    pass

with dpg.window(label = 'Channel 2',
                tag='image_window_ch2',
                width = mode_init.image_window_ch2['width'],
                height = mode_init.image_window_ch2['height'],
                pos = mode_init.image_window_ch2['pos'],
                autosize=True,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_move=True,
                no_bring_to_front_on_focus=True,
                show=True
               ):
    pass

with dpg.window(label = 'Results channel 1',
                tag='hist_window_ch1',
                width = mode_init.hist_window_ch1['width'],
                height = mode_init.hist_window_ch1['height'],
                pos = mode_init.hist_window_ch1['pos'],
                autosize=False,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_bring_to_front_on_focus=True,
                no_move=True,
                show=True
               ):
    pass

with dpg.window(label = 'Results channel 2',
                tag='hist_window_ch2',
                width = mode_init.hist_window_ch2['width'],
                height = mode_init.hist_window_ch2['height'],
                pos = mode_init.hist_window_ch2['pos'],
                autosize=False,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_bring_to_front_on_focus=True,
                no_move=True,
                show=True
               ):
    pass

with dpg.window(label='',
                pos=mode_init.FCS_window['pos'],
                width=mode_init.FCS_window['width'],
                height=mode_init.FCS_window['height'],
                no_move=True,
                no_close=True,
                no_collapse=True,
                no_title_bar=True,
                no_resize=True,
                tag='FCS_window',
                show=True
               ):
    pass

with dpg.window(label='',
                pos=mode_init.results_window['pos'],
                width=mode_init.results_window['width'],
                height=mode_init.results_window['height'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='results_window',
                show=True
               ):
    pass

# # print('file_window -mounted')

# with dpg.window(tag="Model_selection_panel",
#                     width=method_init.Model_selection_panel['width'],
#                 height=method_init.Model_selection_panel['height'],
#                 pos=method_init.Model_selection_panel['pos'],
#                     no_move=True,
#                     no_close=True,
#                     no_title_bar=True,
#                     no_resize=True,
#                     show=True
#                    ):
#     pass

# with dpg.window(label='Add model',tag="Add_model_window",
#                     width=method_init.Add_model_window['width'],
#                 height=method_init.Add_model_window['height'],
#                 pos=method_init.Add_model_window['pos'],
                    
#                     no_move=False,
#                     no_collapse=True,
#                     no_title_bar=True,
#                     no_resize=True,
#                     show=False,
#                     modal=False

#                    ):
#     pass

# # print('Add_model_window -mounted')

# with dpg.window(label = "",
#                     tag = "plot_win",
#                     width=method_init.plot_win['width'],
#                 height=method_init.plot_win['height'],
#                 pos=method_init.plot_win['pos'],
#                     no_move = True,
#                     no_close = True,
#                     no_title_bar = True,
#                     no_resize = True,
#                     show = True
#                    ):
#     pass

# # print('plot_win - mounted')


# globalITEMS.windows.extend(['file_window',
#                             'Model_selection_panel',
#                             'Add_model_window',
#                             'plot_win'])

# # print('Main windows of the method - mounted')

# #########################################################################
# '''Dialog windows of the method'''
# #########################################################################




# dpg.add_file_dialog(directory_selector=True,
#                     label = 'Select working directory',
#                     width = method_init.file_dialog_id1['width'],
#                     height = method_init.file_dialog_id1['height'],
#                     show=False,
#                     file_count=2,
#                     default_path=method_cmn.last_directory,
#                     callback=method_cmn.callback_directory_select,
#                     cancel_callback=callback_none,
#                     tag="file_dialog_id1",
#                     modal=False
#                    )
# with dpg.file_dialog(directory_selector=False,
#                     label = 'Select multicolumn file',
#                     width = method_init.multi_file_dialog_id['width'],
#                     height = method_init.multi_file_dialog_id['height'],
#                     show=False,
#                     file_count=5,
#                     default_filename ='*',
#                     default_path=method_cmn.last_directory,
#                     callback=method_cmn.callback_directory_select,
#                     cancel_callback=callback_none,
#                     tag="multi_file_dialog_id",
#                     modal=False
#                    ):
#     dpg.add_file_extension("")
#     dpg.add_file_extension(".dat", color=(150, 255, 150, 255))






# with dpg.file_dialog(directory_selector=True,
#                     show=False,
#                     file_count=15,
#                     default_path=method_init.last_directory,
#                     width = method_init.file_dialog_plot_all['width'],
#                     height = method_init.file_dialog_plot_all['height'],
#                     callback=method_cmn.callback_plot_all_to_files,
#                     cancel_callback=callback_none,
#                     tag="file_dialog_plot_all",
#                     modal=False):
#     '''Dialog window for exporting the results of the fitting.'''
#     dpg.add_file_extension("", color=(150, 255, 150, 255))
    
# '''Export results window'''

# with dpg.file_dialog(directory_selector=False,
#                     show=False,
#                     file_count=15,
#                     default_path=method_init.last_directory,
#                     width = method_init.file_dialog_export['width'],
#                     height = method_init.file_dialog_export['height'],
#                     callback=method_cmn.callback_directory_export,
#                     cancel_callback=callback_none,
#                     tag="file_dialog_export",
#                     modal=False):
#     '''Dialog window for exporting the results of the fitting.'''
#     dpg.add_file_extension("", color=(150, 255, 150, 255))
#     dpg.add_file_extension("{.xlsx,.csv,.dat}")
#     dpg.add_file_extension(".xlsx", color=(255, 0, 255, 255), custom_text="[Excel]")
#     dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[CSV]")
#     dpg.add_file_extension(".pickle", color=(0, 255, 255, 255), custom_text="[Pandas]")

    
    
# globalITEMS.windows.extend(['file_dialog_id1',
#                             'multi_file_dialog_id',
#                             'file_dialog_plot_all',
#                             'file_dialog_export'])


# # print('Dialog windows of the method - mounted')

# #########################################################################
# '''Items in the left panel'''
# #########################################################################

# dpg.add_text('FILES',tag='FILES_window_text_title',parent='file_window')
# dpg.add_separator(tag ='sep_left_1',parent='file_window')
# '''Window containing file selection panel.'''
# list_box = dpg.add_listbox(items=method_cmn.files,
#                        width=method_init.file_box['width'],
#                        num_items=method_init.file_box['num_items'],
#                        tag='file_box',
#                            parent='file_window',

#                       )
                           
# globalITEMS.windows.extend(['FILES_window_text_title',
#                             'sep_left_1',
#                             'file_box'])                           
                           
# #########################################################################
# '''Items in the middle panel'''
# #########################################################################                           
                           
# with dpg.group(tag='model_choice_group',
#                        horizontal=True,
#                        horizontal_spacing=method_init.group_spacer,
#                        show=True,
#                        parent = 'Model_selection_panel'
#                       ):
#     dpg.add_combo(method_cmn.Models,
#                                          label="",
#                   width=method_init.model_choose['width'],
#                                          height_mode=dpg.mvComboHeight_Large,
#                                          tag='model_choose',
#                                          default_value=method_cmn.init_model,
#                                          callback=method_cmn.callback_models,
#                                           # callback=self._something,
#                                           enabled=False
#                                         )

#     with dpg.tooltip('model_choose'):
#         dpg.add_text("Select the model.")
#     dpg.add_button(label="Add model",
#                                tag='Add_model_button',
#                                width = method_init.Add_model_button['width'],
#                                callback=lambda: dpg.configure_item('Add_model_window', show=True)
#                               )
#     dpg.bind_item_theme('Add_model_button', 'fit_button_theme')    
#     with dpg.tooltip('Add_model_button'):
#         dpg.add_text("Add user-defined model. Opens a new window where the user can input and save the new model.")
# dpg.add_separator(tag ='sep_mid_1',show=True,parent='Model_selection_panel')
# with dpg.table(header_row=False,tag='CNTR_bright_table',width=-1,borders_innerH=False, 
#                                borders_outerH=False, borders_innerV=False, borders_outerV=False,
#                                no_pad_innerX=False,no_pad_outerX=True,no_host_extendX=True,
#                                no_clip=True, policy=dpg.mvTable_SizingStretchSame,parent ='Model_selection_panel'):
#     dpg.add_table_column(tag='CNTR_bright_table_col0',width=method_init.internal_width_middle_panel/2)
#     dpg.add_table_column(tag='CNTR_bright_table_col1',width=method_init.internal_width_middle_panel/2)
#     with dpg.table_row(tag='CNTR_bright_table_row0'):
# # with dpg.group(tag='CNTR_bright_group',
# #                horizontal=True,
# #                horizontal_spacing=method_init.group_spacer,
# #                show=True,
# #                parent ='Model_selection_panel'):
#         dpg.add_drag_float(label='', width=method_init.CNTR['width'],
#                             tag='CNTR',
#                             show=True,
#                             default_value=0,
#                            enabled=True,
#                            min_value=0,
#                            max_value=1e5,
#                           format="CNTR (Hz) =%.1f",
#                          callback=method_cmn.callback_calculate_mol_bright
                           
#                            )
#         dpg.add_drag_float(label='', width=method_init.BRIGHT['width'],
#                             tag='BRIGHT',
#                             show=True,
#                             default_value=0,
#                            enabled=False,
#                           format="B (Hz/MOL) =%.0f",
#                          # callback=method_cmn.callback_Xunits
#                            )
# dpg.add_separator(tag ='sep_mid_2',show=True,parent='Model_selection_panel')
                           
                           
# globalITEMS.windows.extend(['model_choice_group',
#                             'model_choose',
#                             'Add_model_button',
#                             'sep_mid_1',
#                             'sep_mid_2',
#                             'CNTR_bright_table_row0',
#                             'CNTR_bright_table_col1',
#                             'CNTR_bright_table_col0',
#                             'CNTR_bright_table',
#                             'CNTR',
#                             'BRIGHT'
#                            ])

# # print('Items in the left panel - mounted')

# #########################################################################
# '''Items in the right panel'''
# ######################################################################### 

# with dpg.group(tag='log_checkbox_group', horizontal=True,
#                horizontal_spacing=method_init.group_spacer,
#                show=True,
#                parent ='plot_win'):
#     dpg.add_drag_float(label='',
#                        width=method_init.Xunits['width'],
#                         tag='Xunits',
#                         show=True,
#                         default_value=0.00100000000,
#                       format='Time units: %.0e [s]',
#                      callback=method_cmn.callback_Xunits
#                        )
#     with dpg.tooltip('Xunits'):
#                 dpg.add_text("Default value is 10\u02C9\u00B3 s. If your data file has different units modify this value. Otherwise keep the default value.")

#     dpg.add_drag_float(label='', width=method_init.Yunits['width'],
#                         tag='Yunits',
#                         show=True,
#                         default_value=1,
#                       format="%.0e \u00D7 G("+'\u03C4'+")",
#                      callback=method_cmn.callback_Xunits
#                        )
#     with dpg.tooltip('Yunits'):
#                 dpg.add_text("Default value is 1mc. If your data file has different units modify this value. Otherwise keep the default value.")
#     dpg.add_text('',show=True,tag='chi_sqr')

# with dpg.group(tag='df_range_group',
#                horizontal=True,
#                horizontal_spacing=method_init.group_spacer,
#                show=True,
#                parent ='plot_win'):
#     dpg.add_drag_float(label='',
#                        width=method_init.df_min['width'],
#                        tag='df_min',
#                        show=True,#,False,
#                        min_value=-1e312,
#                        max_value=-1e312,
#                        callback=method_cmn.callback_df_range,
#                        format='\u03C4'+' (min)  [ms] = %.4f',
#                       )
#     with dpg.tooltip('df_min'):
#                 dpg.add_text("Define lowest value of lag time to plot.")
#     dpg.add_drag_float(label='',
#                        width=method_init.df_max['width'],
#                        tag='df_max',
#                        show=True,#,False,
#                        min_value=-1e312,
#                        max_value=-1e312,
#                        callback=method_cmn.callback_df_range,
#                        format='\u03C4'+' (max) [ms] = %.1f',
#                       )
#     with dpg.tooltip('df_max'):
#                 dpg.add_text("Define highest value of lag time to plot.")
#     dpg.add_button(label='Reset range',
#                      width=method_init.Reset_range['width'],
#                      tag='Reset_range',
#                       show=True,#False,
#                        enabled=True,
#                      callback=method_cmn.callback_reset_df_range
#                      )
#     dpg.bind_item_theme('Reset_range', 'fit_button_theme')   
#     dpg.configure_item('Reset_range',enabled=False)   

# with dpg.subplots(3,1,height=method_init.subplots['height'], width=method_init.subplots['width'],row_ratios=[3.0,3.0, 1.0],link_all_x=True,tag='subplots',show=True,parent='plot_win') as subplot_id:
#     # pass

#     with dpg.plot(no_title=True,tag='plot_1',show=True):
#         acf_plt_x = dpg.add_plot_axis(dpg.mvXAxis, label="", tag='acf_x',log_scale=True)
#         acf_plt_y = dpg.plot_axis(dpg.mvYAxis, label="G("+'\u03C4'+")",tag='acf_y',log_scale=False)
#         with acf_plt_y:
#             dpg.add_scatter_series([], [],tag='ACF_plot')
#             dpg.add_line_series([], [],tag='ACF_fit')

#             dpg.bind_item_theme("ACF_plot", "plot_theme")
#             dpg.bind_item_theme("ACF_fit", "plot_theme")
#     with dpg.plot(no_title=True,tag='plot_2',show=True):
#         acf_plt_x = dpg.add_plot_axis(dpg.mvXAxis, label="", tag='acf_x_log',log_scale=True)
#         acf_plt_y = dpg.plot_axis(dpg.mvYAxis, label="Log(G("+'\u03C4'+"))",tag='acf_y_log',log_scale=True)
#         with acf_plt_y:
#             dpg.add_scatter_series([], [],tag='ACF_plot_log')
#             dpg.add_line_series([], [],tag='ACF_fit_log')

#             dpg.bind_item_theme("ACF_plot_log", "plot_theme")
#             dpg.bind_item_theme("ACF_fit_log", "plot_theme")  
#     with dpg.plot(no_title=True,tag='plot_3',show=True):
#         dpg.configure_item('Xunits', format='Time units: %.0e [s]')
#         dpg.add_plot_axis(dpg.mvXAxis, label="Lag time, "+'\u03C4'+" [ms]",tag='res_x',log_scale=True)
#         with dpg.plot_axis(dpg.mvYAxis,
#                            label="Residues",
#                            tag='res_y'):
#             dpg.add_line_series([], [],
#                                 tag='RES_plot')
#             dpg.bind_item_theme("RES_plot", "plot_theme")
#         dpg.set_axis_limits_auto('res_y')
        
        
        
# globalITEMS.windows.extend(['log_checkbox_group',
#                             'Xunits',
#                             'Yunits',
#                             'df_range_group',
#                             'df_min',
#                             'df_max',
#                             'Reset_range',
#                            'subplots',
#                             'plot_1',
#                             'acf_x',
#                             'acf_y',
#                             'ACF_plot',
#                             'ACF_fit',
#                             'plot_2',
#                             'acf_x_log',
#                             'acf_y_log',
#                             'ACF_plot_log',
#                             'ACF_fit_log',
#                             'plot_3',
#                             'res_x',
#                             'res_y',
#                             'RES_plot'
#                            ])


# # print('Items in the right panel - mounted')

# #########################################################################
# '''Items in the Add_model window'''
# ######################################################################### 





# with dpg.group(tag='var_def_group_1',
#                horizontal=True,
#                horizontal_spacing=method_init.group_spacer,
#                parent = 'Add_model_window'
#               ):
#     dpg.add_button(label="Close",
#                    tag='Close_Add_model_button',
#                    width = method_init.Close_Add_model_button['width'],
#                    callback=method_cmn.callback_close_new_model_window
#                   )
#     dpg.add_button(label="Save model",
#                    tag='Save_model_button',
#                    width = method_init.Save_model_button['width'],
#                    show=False,
#                    callback=method_cmn.callback_save_variables_to_json
#                   )
#     dpg.bind_item_theme('Close_Add_model_button', 'fit_button_theme') 
#     dpg.bind_item_theme('Save_model_button', 'fit_button_theme') 
# dpg.add_input_text(label="",
#                    default_value="Enter the name of the model.",
#                    tag='model_input_name',
#                    on_enter=True,
#                    enabled=True,
#                    width=method_init.model_input_name['width'],
#                    parent = 'Add_model_window'
#                   )
# dpg.add_input_text(label="",
#                    default_value="Enter the model description.",
#                    tag='model_input_describe',
#                    on_enter=True,
#                    enabled=True,
#                    multiline=True,
#                    width=method_init.model_input_describe['width'],
#                    parent = 'Add_model_window'
#                   )
# dpg.add_text('Input the function. Avoid using a single capital N letter as varibale. Use x character for independent variable.',parent = 'Add_model_window',tag='add_model_text_1')

# dpg_image1 = []
# for i in range(0, method_init.image_1['height']):
#     for j in range(0, method_init.image_1['width']):
#         dpg_image1.append(80/255)
#         dpg_image1.append(80/255)
#         dpg_image1.append(80/255)
#         dpg_image1.append(255/255)

# dpg.add_input_text(label="",
#                    default_value="",
#                    tag='model_input_text1',
#                    on_enter=False,
#                    enabled=True,
#                    multiline=True,
#                    callback=method_cmn.callback_stringtest1,
#                    width=method_init.model_input_text1['width'],parent = 'Add_model_window')

# with dpg.texture_registry(tag = 'texture_reg1'):
#     dpg.add_dynamic_texture(method_init.image_1['width'],
#                             method_init.image_1['height'],
#                             dpg_image1,
#                             tag="image_id1"
#                            )
# with dpg.drawlist(width=method_init.drawlist1['width'],
#                   height=method_init.drawlist1['height'],
#                   tag='drawlist1',parent = 'Add_model_window'
#                  ):
#     dpg.draw_image("image_id1",
#                    [0, 0],
#                    [method_init.image_1['width'],method_init.image_1['height']],
#                    parent='drawlist1',
#                    show=True,
#                    tag='draw_image_'
#                   )
# dpg.add_text('List all variables, without x variable. Use coma to separate the symbols. Avoid doubles. Confirm with ENTER.',tag='List_all_variables_text',parent = 'Add_model_window')
# dpg.add_input_text(label="",
#                    default_value="",
#                    tag='model_input_variables',
#                    on_enter=True,
#                    enabled=True,
#                    callback=method_cmn.callback_new_var_string,
#                    width=method_init.model_input_variables['width'],
#                    parent = 'Add_model_window'
#                   )
# dpg.add_group(tag='vars_group', show=False,parent = 'Add_model_window')
# dpg.add_text('Enter the minimal, the default, and the maximal values of variables. Press "Save" to finish.',tag='vars_min_def_max',parent='vars_group')

# globalITEMS.windows.extend(['var_def_group_1',
#                             'Close_Add_model_button',
#                             'Save_model_button',
#                             'model_input_name',
#                             'model_input_describe',
#                             'add_model_text_1',
#                             'model_input_text1',
#                             'texture_reg1',
#                             'image_id1',
#                             'drawlist1',
#                             'draw_image_',
#                             'add_model_text_2',
#                             'model_input_variables',
#                             'vars_group',
#                             'vars_min_def_max'
#                            ])


# print('Items in the Add_model window - mounted')