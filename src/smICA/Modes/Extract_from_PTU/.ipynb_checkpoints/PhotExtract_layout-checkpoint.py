'''
This file is part of the smICA repository that is distributed under the MIT license; see below.


############################################################################

MIT License

Copyright (c) 2024 Tomasz Kalwarczyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


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
                                     basf,
                                    globalITEMS
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
                no_resize=True,
                show=True):
    with dpg.plot(no_title=True,
                  width=mode_init.plt_1_ch_1['width'],
                  height=mode_init.plt_1_ch_1['height'],
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
                               height = mode_init.Calculate_filters['height'],
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
                dpg.add_scatter_series([], [],
                                    parent='yaxis_tltr',tag="tag_series_fltr_subtr")
                
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


