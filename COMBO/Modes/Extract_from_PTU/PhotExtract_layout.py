from Modes.Extract_from_PTU.PhotExtract_INIT import _PhotExtr_init, _PhotExtr_vars_funct
import numpy as np
import cv2

def PhotExtr_resizer(sender,app_data):

    hidden_items = ['load_ind_win','loading_title','loading_butt','loading_status','loading_cnt_butt','loading_status_text']
    init_resizable_items = []
    cmn_resizable_items = []
    obj_var = [eval('mode_init.'+str(m)) for m in vars(mode_init)]
    for m in obj_var:
        if type(m) == dict:
            if 'name' in m.keys():
                if m['name'] not in hidden_items:
                    init_resizable_items.append(m['name'])
                else:
                    pass
        else:
            pass
    obj_var = [eval('mode_cmn.'+str(m)) for m in vars(mode_cmn)]
    for m in obj_var:
        if type(m) == dict:
            if 'name' in m.keys():
                cmn_resizable_items.append(m['name'])
        else:
            pass    
        

    ratio = {'width': np.round(app_data[0]/inV.VIEWPORT_prop['width'],4),
             'height': np.round(app_data[1]/inV.VIEWPORT_prop['height'],4)} 

    inV.init_size_ratio = ratio

    forbiden_list = ['self',
                     'size_ratio',
                     'font_size',
                     'last_directory'
                     
                    ]
    temp_inits = mode_init.__init__.__code__.co_varnames

    
    temp_inits = [v for v in temp_inits if v not in forbiden_list]
    temp_inits_values  = {}
    for v in temp_inits:
        temp_inits_values[v] = eval('mode_init.'+v)
        
    mode_init.__init__(inV.init_size_ratio,
                         inV.init_left_indent,
                         inV.init_internal_indent,
                         inV.init_right_indent,
                         inV.init_bottom_indent,
                         inV.init_top_indent,
                         inV.init_group_spacer,
                         inV.init_font_size,
                         globalITEMS.last_directory,
                        globalITEMS.windows)
    
    
    for item in init_resizable_items:
        
        props =eval('mode_init.'+item) 
        # print(item)
            
        if 'width' in props.keys():
            dpg.configure_item(item,width=props['width'])
        if 'height' in props.keys():
            dpg.configure_item(item,height=props['height'])
        if 'pos' in props.keys():
            dpg.configure_item(item,pos=props['pos'])
    
    
    
        
        

dpg.set_viewport_resize_callback(PhotExtr_resizer)


mode_init = _PhotExtr_init(inV.init_size_ratio,
                             inV.init_left_indent,
                             inV.init_internal_indent,
                             inV.init_right_indent,
                             inV.init_bottom_indent,
                             inV.init_top_indent,
                             inV.init_group_spacer,
                             inV.init_font_size,
                             globalITEMS.last_directory,
                             globalITEMS.windows,
                            )


mode_cmn = _PhotExtr_vars_funct(mode_init,
                                     globalITEMS.last_directory,
                                     basf
                                    )
# method_cmn.mount_fcs_handlers()


# #########################################################################
# '''Main windows of the method'''
# #########################################################################
'''Plot window items'''
with dpg.window(label="Lifetime Channel 1",
                width=mode_init.plot_window_ch1['width'],
                height=mode_init.plot_window_ch1['height'],
                pos=mode_init.plot_window_ch1['pos'],
                tag='plot_window_ch1',
                no_move=True,
                no_close=True,
                no_collapse=True,
                # no_title_bar=True,
                no_resize=True,
                show=True):
    with dpg.plot(no_title=True,
                  width=mode_init.plt_1_ch_1['width'],
                  height=mode_init.plt_1_ch_1['height'],
                  # callback=query_ch1,
                  query=False,
                  no_menus=True,
                  tag='plt_1_ch_1',
                  show=True):
        pass
        
        dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_chan1",log_scale=False)
        dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_chan1",log_scale=True)
        dpg.add_line_series(mode_cmn.sindatax1, mode_cmn.sindatay1, parent='yaxis_chan1',tag="tag_series_ch_1")
        dpg.bind_item_theme("tag_series_ch_1", "plot_theme")
        dpg.add_drag_line(label="Lower limit",
                          tag='L_dline_ch1' ,
                          color=mode_init.L_dline_ch1['color'],
                          default_value=mode_init.L_dline_ch1['default_value'],
                          callback=mode_cmn.callback_dragline,
                          show = False,
                          thickness = mode_init.L_dline_ch1['thickness']
                         )
        dpg.add_drag_line(label="Upper limit",
                          tag='U_dline_ch1',
                          color=mode_init.U_dline_ch1['color'],
                          default_value=mode_init.U_dline_ch1['default_value'],
                          callback=mode_cmn.callback_dragline,
                          show = False,
                          thickness = mode_init.U_dline_ch1['thickness']
                         )
    with dpg.plot(no_title=True,
                  width=mode_init.plt_2_ch_1['width'],
                  height=mode_init.plt_2_ch_1['height'],
                  no_menus=True,
                  tag='plt_2_ch_1',
                  show=True):
        dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_chan1_zoom",log_scale=False)
        dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_chan1_zoom",log_scale=True)
        dpg.add_line_series(mode_cmn.sindatax1, mode_cmn.sindatay1, parent="yaxis_chan1_zoom",tag="tag_series_ch_1_zoom")
        dpg.bind_item_theme("tag_series_ch_1_zoom", "plot_theme")
    with dpg.table(header_row=False, width=-1,borders_innerH=False, 
                                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                                   no_pad_innerX=False,no_pad_outerX=True,no_host_extendX=True,
                                   no_clip=True,tag='LIMITS_ch_1_table'):
        dpg.add_table_column(label="",tag='LIMITS_ch_1_table_col1', width = mode_init.LIMITS_ch_1_table_col1['width'])
        dpg.add_table_column(label="",tag='LIMITS_ch_1_table_col2', width = mode_init.LIMITS_ch_1_table_col2['width'])
        dpg.add_table_column(label="",tag='LIMITS_ch_1_table_col3', width = mode_init.LIMITS_ch_1_table_col3['width'])
        with dpg.table_row(tag='LIMITS_ch_1_table_row1'):

            dpg.add_drag_float(label='',
                               tag='bottom_limit_ch1',
                               width = mode_init.bottom_limit_ch1['width'],
                               format = 'Time > %.3f [ns]',
                               speed = 0.01,
                               callback = mode_cmn.callback_query,
                               enabled = False
                               )
            dpg.add_drag_float(label='',
                               tag='upper_limit_ch1',
                               width = mode_init.upper_limit_ch1['width'],
                               format = 'Time < %.3f [ns]',
                               speed = 0.01,
                               callback = mode_cmn.callback_query,
                               enabled = False
                               )
            dpg.add_button(label='RESET',
                           tag='reset_button_ch1',
                           width = mode_init.reset_button_ch1['width'],
                           callback = mode_cmn.callback_reset_range,
                           enabled = False
                           )
            dpg.bind_item_theme('reset_button_ch1', 'fit_button_theme')
            with dpg.tooltip('reset_button_ch1',tag='reset_button_ch1_tooltip'):
                dpg.add_text("Reset range.",tag='reset_button_ch1_tooltip_text')
        
    dpg.add_separator(tag ='CH_1_sep_1',show=True)
    dpg.add_checkbox(tag='use_as_statistical_filters_chkbx_ch_1',
                     label = 'Use statistical filters',
                     default_value=False,
                     show=True,
                     enabled=True,
                     callback=mode_cmn.calllback_use_stat_filters_chbx
                     )
    dpg.add_button(label='Calculate filters',
                   tag='Remove_bgd_butt_ch_1',
                   width = mode_init.Remove_bgd_butt_ch_1['width'],
                   callback = mode_cmn.show_br_fltr_wndw,
                   enabled = False,
                   show=False
                   # show=True
                   )
    dpg.bind_item_theme('Remove_bgd_butt_ch_1', 'fit_button_theme')
    with dpg.table(header_row=True,
                      width=mode_init.filters_ch_1_tab_list_tag['width'],#init_widths['List_of_filters_ch1'],
                      height=mode_init.filters_ch_1_tab_list_tag['height'],
                      scrollY=True,
                      policy=dpg.mvTable_SizingFixedFit,
                      borders_innerV =True,
                      tag='filters_ch_1_tab_list_tag',
                  show =False
                   # show =True
                  ):

        
        
        dpg.add_table_column(label = '#.',width_fixed=True,tag='filters_ch_1_tab_list_tag_col1')
        dpg.add_table_column(label = 'Filter name',width_stretch=True,tag='filters_ch_1_tab_list_tag_col2')
        dpg.add_table_column(label = '',width_fixed=True,tag='filters_ch_1_tab_list_tag_col3')

globalITEMS.windows.extend(['plot_window_ch1',
                            'plt_1_ch_1',
                            'xaxis_chan1',
                            'yaxis_chan1',
                            'tag_series_ch_1',
                            'L_dline_ch1',
                            'U_dline_ch1',
                            'xaxis_chan1_zoom',
                            'yaxis_chan1_zoom',
                            'tag_series_ch_1_zoom',
                            'LIMITS_ch_1_table',
                            'LIMITS_ch_1_table_col1',
                            'LIMITS_ch_1_table_col2',
                            'LIMITS_ch_1_table_col3',
                            'LIMITS_ch_1_table_row1',
                            'bottom_limit_ch1',
                            'upper_limit_ch1',
                            'reset_button_ch1',
                            'reset_button_ch1_tooltip',
                            'reset_button_ch1_tooltip_text',
                            'CH_1_sep_1',
                            'use_as_statistical_filters_chkbx_ch_1',
                            'filters_ch_1_tab_list_tag',
                            'filters_ch_1_tab_list_tag_col1',
                            'filters_ch_1_tab_list_tag_col2',
                            'filters_ch_1_tab_list_tag_col3'
                            
                           ])

with dpg.window(label="Lifetime Channel 2",
                width=mode_init.plot_window_ch2['width'],
                height=mode_init.plot_window_ch2['height'],
                pos=mode_init.plot_window_ch2['pos'],
                tag='plot_window_ch2',
                no_move=True,
                no_close=True,
                no_collapse=True,
                # no_title_bar=True,
                no_resize=True,
                show=True):
    with dpg.plot(no_title=True,
                  width=mode_init.plt_1_ch_2['width'],
                  height=mode_init.plt_1_ch_2['height'],
                  callback=mode_cmn.query_ch1,
                  query=False,
                  no_menus=True,
                  tag='plt_1_ch_2',
                  show=True):
        
        
        dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_chan2",log_scale=False)
        dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_chan2",log_scale=True)
        dpg.add_line_series(mode_cmn.sindatax2, mode_cmn.sindatay2, parent='yaxis_chan2',tag="tag_series_ch_2")
        dpg.bind_item_theme("tag_series_ch_2", "plot_theme")
        dpg.add_drag_line(label="Lower limit",
                          tag='L_dline_ch2' ,
                          color=mode_init.L_dline_ch2['color'],
                          default_value=mode_init.L_dline_ch2['default_value'],
                          callback=mode_cmn.callback_dragline,
                          show = False,
                          thickness = mode_init.L_dline_ch2['thickness']
                         )
        dpg.add_drag_line(label="Upper limit",
                          tag='U_dline_ch2',
                          color=mode_init.U_dline_ch2['color'],
                          default_value=mode_init.U_dline_ch2['default_value'],
                          callback=mode_cmn.callback_dragline,
                          show = False,
                          thickness = mode_init.U_dline_ch2['thickness']
                         )
    with dpg.plot(no_title=True,
                  width=mode_init.plt_2_ch_2['width'],
                  height=mode_init.plt_2_ch_2['height'],
                  no_menus=True,
                  tag='plt_2_ch_2',
                  show=True):
        dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_chan2_zoom",log_scale=False)
        dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_chan2_zoom",log_scale=True)
        dpg.add_line_series(mode_cmn.sindatax2, mode_cmn.sindatay2, parent="yaxis_chan2_zoom",tag="tag_series_ch_2_zoom")
        dpg.bind_item_theme("tag_series_ch_2_zoom", "plot_theme")
    with dpg.table(header_row=False, width=-1,borders_innerH=False, 
                                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                                   no_pad_innerX=False,no_pad_outerX=True,no_host_extendX=True,
                                   no_clip=True,tag='LIMITS_ch_2_table'):
        dpg.add_table_column(label="",tag='LIMITS_ch_2_table_col1', width = mode_init.LIMITS_ch_2_table_col1['width'])
        dpg.add_table_column(label="",tag='LIMITS_ch_2_table_col2', width = mode_init.LIMITS_ch_2_table_col2['width'])
        dpg.add_table_column(label="",tag='LIMITS_ch_2_table_col3', width = mode_init.LIMITS_ch_2_table_col3['width'])
        with dpg.table_row(tag='LIMITS_ch_2_table_row1'):

            dpg.add_drag_float(label='',
                               tag='bottom_limit_ch2',
                               width = mode_init.bottom_limit_ch2['width'],
                               format = 'Time > %.3f [ns]',
                               speed = 0.01,
                               callback = mode_cmn.callback_query,
                               enabled = False
                               )
            dpg.add_drag_float(label='',
                               tag='upper_limit_ch2',
                               width = mode_init.upper_limit_ch2['width'],
                               format = 'Time < %.3f [ns]',
                               speed = 0.01,
                               callback = mode_cmn.callback_query,
                               enabled = False
                               )
            dpg.add_button(label='RESET',
                           tag='reset_button_ch2',
                           width = mode_init.reset_button_ch2['width'],
                           callback = mode_cmn.callback_reset_range,
                           enabled = False
                           )
            dpg.bind_item_theme('reset_button_ch2', 'fit_button_theme')
            with dpg.tooltip('reset_button_ch2',tag='reset_button_ch2_tooltip'):
                dpg.add_text("Reset range.",tag='reset_button_ch2_tooltip_text')
        
    dpg.add_separator(tag ='CH_1_sep_2',show=True)
    dpg.add_checkbox(tag='use_as_statistical_filters_chkbx_ch_2',
                     label = 'Use statistical filters',
                     default_value=False,
                     show=True,
                     enabled=True,
                     callback=mode_cmn.calllback_use_stat_filters_chbx
                     )
    dpg.add_button(label='Calculate filters',
                   tag='Remove_bgd_butt_ch_2',
                   width = mode_init.Remove_bgd_butt_ch_2['width'],
                   callback = mode_cmn.show_br_fltr_wndw,
                   enabled = False,
                   show=False
                   # show=True
                   )
    dpg.bind_item_theme('Remove_bgd_butt_ch_2', 'fit_button_theme')
    with dpg.table(header_row=True,
                      width=mode_init.filters_ch_2_tab_list_tag['width'],#init_widths['List_of_filters_ch1'],
                      height=mode_init.filters_ch_2_tab_list_tag['height'],
                      scrollY=True,
                      policy=dpg.mvTable_SizingFixedFit,
                      borders_innerV =True,
                      tag='filters_ch_2_tab_list_tag',
                  show =False
                   # show =True
                  ):

        
        
        dpg.add_table_column(label = '#.',width_fixed=True,tag='filters_ch_2_tab_list_tag_col1')
        dpg.add_table_column(label = 'Filter name',width_stretch=True,tag='filters_ch_2_tab_list_tag_col2')
        dpg.add_table_column(label = '',width_fixed=True,tag='filters_ch_2_tab_list_tag_col3')


globalITEMS.windows.extend(['plot_window_ch2',
                            'plt_1_ch_2',
                            'xaxis_chan2',
                            'yaxis_chan2',
                            'tag_series_ch_2',
                            'L_dline_ch2',
                            'U_dline_ch2',
                            'xaxis_chan2_zoom',
                            'yaxis_chan2_zoom',
                            'tag_series_ch_2_zoom',
                            'LIMITS_ch_2_table',
                            'LIMITS_ch_2_table_col1',
                            'LIMITS_ch_2_table_col2',
                            'LIMITS_ch_2_table_col3',
                            'LIMITS_ch_2_table_row1',
                            'bottom_limit_ch2',
                            'upper_limit_ch2',
                            'reset_button_ch2',
                            'reset_button_ch2_tooltip',
                            'reset_button_ch2_tooltip_text',
                            'CH_2_sep_1',
                            'use_as_statistical_filters_chkbx_ch_2',
                            'filters_ch_2_tab_list_tag',
                            'filters_ch_2_tab_list_tag_col1',
                            'filters_ch_2_tab_list_tag_col2',
                            'filters_ch_2_tab_list_tag_col3'
                           ])

with dpg.window(label="Options",
                width=mode_init.Options['width'],
                height=mode_init.Options['height'],
                pos=mode_init.Options['pos'],
                tag='Options',
                no_move=True,
                no_close=True,
                no_collapse=True,
                # no_title_bar=True,
                no_resize=True,
                show=True):
    dpg.add_text('MODE:',tag='mode_text')
    dpg.add_text('Remove additional lines?',tag='rm_lines_mode_text')
    with dpg.group(tag='line_skip_group',horizontal=True,horizontal_spacing=mode_init.group_spacer):
        dpg.add_checkbox(tag='skip_lines_check',
                         default_value=True,
                         callback=mode_cmn.callback_skip_lines_check
                        )
        dpg.add_drag_int(label='',
                         tag='skip_lines_drag',
                         width = -1,
                         default_value =15,
                         speed = 1,
                         enabled = True
                        )

globalITEMS.windows.extend(['Options',
                            'mode_text',
                            'rm_lines_mode_text',
                            'line_skip_group',
                            'skip_lines_check',
                            'skip_lines_drag'
                           ])

with dpg.window(label="Files",
                width=mode_init.Files_window['width'],
                height=mode_init.Files_window['height'],
                pos=mode_init.Files_window['pos'],
                tag='Files_window',
                no_move=True,
                no_close=True,
                no_collapse=True,
                # no_title_bar=True,
                no_resize=True,
                show=True):
    list_box = dpg.add_listbox(items=mode_init.files,
                               width=mode_init.file_box['width'],
                               num_items=mode_init.file_box['lines'],
                               tag='file_box',
                               callback=mode_cmn.callback_listbox
                              )
    dpg.add_button(label='Apply to single PTU file',
                   tag='apply_to_file',
                   width = mode_init.apply_to_file['width'],
                   callback = mode_cmn.callback_apply_to_single_ptus,
                   user_data = dpg.get_value('file_box'),
                   enabled = False
                        )
    dpg.bind_item_theme('apply_to_file', 'fit_button_theme')
    dpg.add_button(label='Apply to extract from all PTU files',
                   tag='apply_to_all',
                   width = mode_init.apply_to_all['width'],
                   callback = mode_cmn.callback_apply_to_all_ptus,
                   enabled = False
                   )
    dpg.bind_item_theme('apply_to_all', 'fit_button_theme')
    dpg.add_separator(tag ='FW_sep_1',show=True)

globalITEMS.windows.extend(['Files_window',
                            'file_box',
                            'apply_to_file',
                            'apply_to_all',
                            'FW_sep_1'
                           ])



'''Dialog windows'''
with dpg.file_dialog(directory_selector=False,
                    label = 'Select PTU files',
                    width = mode_init.Open_file_dialog['width'],
                    height = mode_init.Open_file_dialog['height'],
                    show=False,
                    file_count=5,
                     default_path=mode_cmn.last_directory,
                    callback=mode_cmn.callback_open_folder,
                    cancel_callback=mode_cmn.callback_empty,
                    tag="Open_file_dialog",
                    modal=False
                   ):
    
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    dpg.add_file_extension(".ptu", color=(0, 255, 0, 255))
    
    
dpg.add_file_dialog(directory_selector=True,
                    label = 'Select PTU folder',
                    width = mode_init.PTU_dir_dialog['width'],
                    height = mode_init.PTU_dir_dialog['height'],
                    show=False,
                    file_count=5,
                    
                    default_path=mode_cmn.last_directory,
                    callback=mode_cmn.callback_open_folder,
                    cancel_callback=mode_cmn.callback_empty,
                    tag="PTU_dir_dialog",
                    modal=False
                   )


globalITEMS.windows.extend(['Open_file_dialog',
                            'PTU_dir_dialog'
                           ])
'''BG_removal_window'''
with dpg.window(label="Lifetime background filtering",
                width=mode_init.BG_removal_window['width'],
                height = mode_init.BG_removal_window['height'],
                pos=mode_init.BG_removal_window['pos'],
                tag='BG_removal_window',
                autosize=True,
                no_collapse=True,
                modal=True,
                show=False):
    with dpg.group(tag='fl_bg_win_group',
                   horizontal=True,
                   horizontal_spacing=mode_init.group_spacer*5):
        with dpg.group(tag='fl_bg_curves_group'):
        
        
        
        
        
                                  
            with dpg.table(header_row=True,
                      width=mode_init.decays_tab_list_tag['width'],
                      height=mode_init.decays_tab_list_tag['height'],
                      scrollY=True,
                      policy=dpg.mvTable_SizingFixedFit,
                      borders_innerV =True,
                      tag='decays_tab_list_tag'):

        
        
                dpg.add_table_column(label = '#.',
                                     width_fixed=True,
                                     tag='decays_tab_list_tag_col1')
                dpg.add_table_column(label = 'Decay name',
                                     width_stretch=True,
                                     tag='decays_tab_list_tag_col2')
                dpg.add_table_column(label = '',
                                     width_fixed=True,
                                     tag='decays_tab_list_tag_col3')

            dpg.add_checkbox(tag='add_bg_range',
                             label = 'Set data range for background',
                             default_value=False,
                             callback=mode_cmn.callback_Set_background_range
                             )
            with dpg.group(tag='fl_bg_win_butt_group',
                           horizontal=True,
                           horizontal_spacing=mode_init.group_spacer):
                dpg.add_button(label='To library',
                               tag='Add_decay_to_lib',
                               width = mode_init.Add_decay_to_lib['width'],
                               callback = mode_cmn.callback_add_decay_to_lib,
                               enabled = False
                               )
                dpg.bind_item_theme('Add_decay_to_lib', 'fit_button_theme')
                
                dpg.add_button(label='From library',
                               tag='Add_decay_from_lib',
                               width = mode_init.Add_decay_from_lib['width'],
                               callback = mode_cmn.callback_import_from_library,
                               enabled = True
                               )
                dpg.bind_item_theme('Add_decay_from_lib', 'fit_button_theme')
                
            with dpg.group(tag='fl_bg_win_filtering_routine_group'):
                dpg.add_checkbox(tag='remove_afterpulsing_chkbx',
                                 label = 'Remove afterpulsing',
                                 default_value=True,
                                 )
                
                dpg.add_button(label='Calculate filters',
                               tag='Calculate_filters',
                               width = mode_init.Calculate_filters['width'],
                               callback = mode_cmn.callback_Calculate_filters,
                               enabled = True
                               )
                dpg.bind_item_theme('Calculate_filters', 'fit_button_theme')

        
        with dpg.group(tag='fl_bg_plt_group1'):
            with dpg.plot(no_title=True,
                          width=mode_init.fltr_plot['width'],
                          height=mode_init.fltr_plot['height'],
                          callback='',
                          query=False,
                          no_menus=True,
                          tag='fltr_plot',
                          show=True):
                
                dpg.add_plot_axis(dpg.mvXAxis, label="Time [ns]", tag="xaxis_tltr",log_scale=False)
                dpg.add_plot_axis(dpg.mvYAxis, label="Intensity", tag="yaxis_tltr",log_scale=True)
                dpg.add_scatter_series([], [], parent='yaxis_tltr',tag="tag_series_fltr")
                # dpg.bind_item_theme("tag_series_fltr", "plot_theme")
                dpg.add_scatter_series([], [],
                                    parent='yaxis_tltr',tag="tag_series_fltr_subtr")
                # dpg.bind_item_theme("tag_series_fltr_subtr", "plot_bg_filter_theme")
                dpg.add_drag_line(label="Background level",
                              tag='Background_level_line' ,
                              parent = 'fltr_plot',
                              color=mode_init.Background_level_line['color'],
                              default_value=mode_init.Background_level_line['default_value'],
                              callback=mode_cmn.callback_drag_Background_level_line,
                              show = False,
                              vertical =False,
                              thickness = mode_init.Background_level_line['thickness']
                             )
                dpg.add_drag_line(label="Background range lower limit",
                              tag='Background_RLL_line' ,
                              parent = 'fltr_plot',
                              color=mode_init.Background_RLL_line['color'],
                              default_value=mode_init.Background_RLL_line['default_value'],
                              callback=mode_cmn.callback_drag_Background_Range_line,
                              show = False,
                              vertical =True,
                              thickness = mode_init.Background_RLL_line['thickness']
                             )
                dpg.add_drag_line(label="Background range upper limit",
                              tag='Background_RUL_line' ,
                              parent = 'fltr_plot',
                              color=mode_init.Background_RUL_line['color'],
                              default_value=mode_init.Background_RUL_line['default_value'],
                              callback=mode_cmn.callback_drag_Background_Range_line,
                              show = False,
                              vertical =True,
                              thickness = mode_init.Background_RUL_line['thickness']
                             )
                dpg.add_plot_legend(location=9,tag='Background_legend')


        with dpg.group(tag='fl_bg_plt_group_fltrs'):    
            with dpg.plot(no_title=True,
                          width=mode_init.fltr_filters_plot['width'],
                          height=mode_init.fltr_filters_plot['height'],
                          callback='',
                          query=False,
                          no_menus=True,
                          tag='fltr_filters_plot',
                          show=False):
                dpg.add_plot_axis(dpg.mvXAxis,
                                  label="Time [ns]",
                                  tag="xaxis_tltr_fltr",
                                  log_scale=False
                                 )
                dpg.add_plot_axis(dpg.mvYAxis,
                                  label="Intensity",
                                  tag="yaxis_tltr_fltr",
                                  log_scale=True)
                dpg.add_plot_legend(location=10,tag='fltr_filters_plot_legend')
            with dpg.group(tag='fl_accpet_filters_group',
                           horizontal=True,
                           horizontal_spacing=mode_init.group_spacer,
                           show=False):
                    dpg.add_button(label='Decline',
                                  tag='Decline_filters',
                                  width = mode_init.Decline_filters['width'],
                                   callback = mode_cmn.callback_Decline_filters,
                                   show =True,
                                   enabled = True
                                   )
                    dpg.bind_item_theme('Decline_filters', 'fit_button_theme')
                    dpg.add_button(label='Accept',
                                  tag='Accept_filters',
                                  width = mode_init.Accept_filters['width'],
                                   callback = mode_cmn.callback_Accept_filters,
                                   show =True,
                                   enabled = True
                                   )
                    dpg.bind_item_theme('Accept_filters', 'fit_button_theme')

    
    with dpg.group(tag='fl_bg_win_group_2',
                   horizontal=True,
                   horizontal_spacing=mode_init.group_spacer*5,
                   show=False):
        with dpg.group(tag='fl_decay_params_group'):
            dpg.add_input_text(default_value = 'Name (optional)',
                               multiline=False,
                               width=mode_init.get_name['width'],
                               tag='get_name'
                              )
            dpg.add_input_text(label = 'Excitation wavelentgh (eg. 485)',
                               multiline=False,
                               width=mode_init.get_wavelength['width'],
                               tag='get_wavelength'
                              )
            dpg.add_text('get_channel',tag='get_channel')
            
            dpg.add_text('get_tcspc_resolution',tag='get_tcspc_resolution')
            with dpg.group(tag='fl_bg_win_submit_decay',
                           horizontal=True,
                           horizontal_spacing=mode_init.group_spacer,
                           show=False
                          ):
                dpg.add_button(label='Cancel',
                               tag='Cancel_decay_submission',
                               width = mode_init.Cancel_decay_submission['width'],
                               callback = mode_cmn.callback_cancel_submission,
                               show =False,
                               enabled = True
                               )
                dpg.bind_item_theme('Cancel_decay_submission', 'fit_button_theme')
                dpg.add_button(label='Submit',
                               tag='Proceed_decay_submission',
                               width = mode_init.Proceed_decay_submission['width'],
                               callback = mode_cmn.callback_proceed_submission,
                               show =False,
                               enabled = True
                               )
                dpg.bind_item_theme('Proceed_decay_submission', 'fit_button_theme')
        dpg.add_input_text(default_value = 'Type descrption here (opitonal)',
                           multiline=True,
                           width=mode_init.get_decay_description['width'],
                           tag='get_decay_description',
                           show=False
                          )
        
        
    with dpg.group(tag='fl_bg_win_group_3',show=False):
        dpg.add_text('The Library is empty',
                     tag='empty_library_notiffication',
                     show=False,
                     color=(255,0,0)
                    )
        
        with dpg.table(header_row=True,
                       width=mode_init.decays_tab_lib_list_tag['width'],
                       height=mode_init.decays_tab_lib_list_tag['height'],
                       scrollY=True,
                       policy=dpg.mvTable_SizingFixedFit,
                       tag='decays_tab_lib_list_tag',
                       borders_innerV =True,
                       show=False
                      ):
            dpg.add_table_column(label = '#',
                                 width_fixed=True,
                                 tag='decays_tab_lib_list_tag_1')
            dpg.add_table_column(label = 'Name',
                                 width_stretch=True,
                                 tag='decays_tab_lib_list_tag_2')
            dpg.add_table_column(label = '\u03BB Exc.',
                                 width_fixed=True,
                                 tag='decays_tab_lib_list_tag_3')
            dpg.add_table_column(label = 'Description',
                                 width_stretch=True,
                                 tag='decays_tab_lib_list_tag_4')
            dpg.add_table_column(label = 'TCSPC resolution',
                                 width_fixed=True,
                                 tag='decays_tab_lib_list_tag_5')
            dpg.add_table_column(label = 'TCSPC channels',
                                 width_fixed=True,
                                 tag='decays_tab_lib_list_tag_6')
            dpg.add_table_column(label = 'Select',
                                 width_fixed=True,
                                 tag='decays_tab_lib_list_tag_7')
        dpg.add_text('',
                     tag='No_match_notiffication',
                     color=(255, 0, 0),
                     show=False
                    )
        with dpg.group(tag='fl_bg_win_library_load_butt_group',
                       horizontal=True,
                       horizontal_spacing=mode_init.group_spacer):
            dpg.add_button(label='Cancel',
                           tag='Cancel_library_import',
                           width = mode_init.Cancel_library_import['width'],
                           callback = mode_cmn.callback_Cancel_library_import,
                           show =False,
                           enabled = True
                           )
            dpg.bind_item_theme('Cancel_library_import', 'fit_button_theme')
            dpg.add_button(label='Import',
                           tag='Proceed_library_import',
                           width = mode_init.Proceed_library_import['width'],
                           callback = mode_cmn.callback_Proceed_library_import,
                           show =False,
                           enabled = True
                           )
            dpg.bind_item_theme('Proceed_library_import', 'fit_button_theme')
        
    with dpg.group(tag='fl_bg_win_group_4',show=False):
        dpg.add_text('There is no curves to calculate. Try to set the background level or add decay from library. ',
                     tag='no_curves_notiffication',
                     show=False,color=(255,0,0)
                    )
        dpg.add_button(label='OK',
                       tag='OK_button',
                       width = mode_init.OK_button['width'],
                       callback = mode_cmn.callback_ok_button,
                       show =False,
                       enabled = True
                       )
        dpg.bind_item_theme('OK_button', 'fit_button_theme')

globalITEMS.windows.extend(['BG_removal_window',
                            'fl_bg_win_group',
                            'fl_bg_curves_group',
                            'decays_tab_list_tag',
                            'decays_tab_list_tag_col1',
                            'decays_tab_list_tag_col2',
                            'decays_tab_list_tag_col3',
                            'add_bg_range',
                            'fl_bg_win_butt_group',
                            'Add_decay_to_lib',
                            'Add_decay_from_lib',
                            'fl_bg_win_filtering_routine_group',
                            'remove_afterpulsing_chkbx',
                            'Calculate_filters',
                            'fl_bg_plt_group1',
                            'fltr_plot',
                            'xaxis_tltr',
                            'yaxis_tltr',
                            'tag_series_fltr',
                            'tag_series_fltr_subtr',
                            'Background_level_line',
                            'Background_RLL_line',
                            'Background_RUL_line',
                            'Background_legend',
                            'fl_bg_plt_group_fltrs',
                            'fltr_filters_plot',
                            'xaxis_tltr_fltr',
                            'yaxis_tltr_fltr',
                            'fl_bg_win_group_2',
                            'fl_decay_params_group',
                            'get_name',
                            'get_wavelength',
                            'get_channel',
                            'get_tcspc_resolution',
                            'fl_bg_win_submit_decay',
                            'Cancel_decay_submission',
                            'Proceed_decay_submission',
                            'get_decay_description',
                            'fl_bg_win_group_3',
                            'empty_library_notiffication',
                            'decays_tab_lib_list_tag',
                            'decays_tab_lib_list_tag_1',
                            'decays_tab_lib_list_tag_2',
                            'decays_tab_lib_list_tag_3',
                            'decays_tab_lib_list_tag_4',
                            'decays_tab_lib_list_tag_5',
                            'decays_tab_lib_list_tag_6',
                            'decays_tab_lib_list_tag_7',
                            'No_match_notiffication',
                            'fl_bg_win_library_load_butt_group',
                            'Cancel_library_import',
                            'Proceed_library_import',
                            'no_curves_notiffication',
                            'OK_button'
                        
                           ])



# BG_removal_window
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