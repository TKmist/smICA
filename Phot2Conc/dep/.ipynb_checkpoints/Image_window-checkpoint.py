log_it('Image_window.py - loaded on '+str(datetime.datetime.now()),'a')

width_1=init_widths['image_window_ch1']
height_1 =init_heights['image_window_ch1']
position_1 = init_position['image_window_ch1']
width_2=init_widths['image_window_ch2']
height_2 =init_heights['image_window_ch2']
position_2 = init_position['image_window_ch2']

with dpg.window(label = 'Channel 1',
                tag='image_window_ch1',
                width = width_1,
                height = height_1,
                pos = position_1,
                autosize=True,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_move=True,
                no_bring_to_front_on_focus=True,
                show=True
               ):
    
    dpg.add_separator(tag ='IMAGE_CH1_top_sep',show=True)
    
    dpg.add_image(tex_1_name,
                  uv_min=(0,0),
                  uv_max=(1,1),
                  tag = 'texture_CH_1',before='img_win_1_table')

    dpg.add_separator(tag ='IMAGE_CH1_top_sep_2',show=True,parent='image_window_ch1')
    
    
    with dpg.table(header_row=False, width=-1,borders_innerH=False, 
                                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                                   no_pad_innerX=False,no_pad_outerX=True,no_host_extendX=True,
                                   no_clip=True,tag='img_win_1_table',parent='image_window_1'):
            # Add headers
        dpg.add_table_column(label="",tag='img_win_1_table_col1', width = int(width_1/3))
        dpg.add_table_column(label="",tag='img_win_1_table_col2', width = int(width_1/3))
        dpg.add_table_column(label="",tag='img_win_1_table_col3', width = int(width_1/3))

        # Add rows and columns
        with dpg.table_row(tag='img_win_1_table_row1'):
            dpg.add_drag_float(tag='cell_tresh_ratio_1',
                               default_value =1.0,
                               max_value=2.,
                               min_value=0.0,
                               speed=0.01,
                               enabled=False,
                               width=-1,
                               callback=_update_textures_both_roi
                              )


            
            # with dpg.group(tag='log_checkbox_group', horizontal=True,
            #    horizontal_spacing=init.group_spacer,
            #    show=True):
            dpg.add_checkbox(label='Find nucleus', 
                             tag='nucleus_search_1',
                             default_value = False,
                             enabled=False,
                             # width=-1,
                             callback=_update_textures_both_roi,
                             # parent='image_window_1'
                            )
            dpg.add_drag_float(tag='nucl_tresh_ratio_1',
                               default_value =1.5,
                               max_value=3.,
                               min_value=0.0,
                               speed=0.01,
                               width=-1,
                               enabled=False,
                               callback = _update_textures_both_roi
                              )
            
    with dpg.table(header_row=False, width=-1,borders_innerH=False, 
                                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                                   no_pad_innerX=False,no_pad_outerX=True,no_host_extendX=True,
                                   no_clip=True,tag='img_win_1_table_2',parent='image_window_1',before='texture_CH_1'):
            # Add headers
            dpg.add_table_column(label="",tag='img_win_1_table_2_col1', width = int(width_1/3))
            dpg.add_table_column(label="",tag='img_win_1_table_2_col2', width = int(width_1/3))
            dpg.add_table_column(label="",tag='img_win_1_table_2_col3', width = int(width_1/3))
            with dpg.table_row(tag='img_win_1_table_2_row1'):
            
                dpg.add_drag_float(tag='img_contrast_1',
                                   format ='Contrast: %.1f',
                                   default_value =1.0,
                                   max_value=5.,
                                   min_value=0.1,
                                   speed=0.1,
                                   enabled=True,
                                   width=-1,
                                   callback=_update_textures_both_roi
                                  )
                
            #     dpg.add_text('',tag='img_contrast_text_1')

                dpg.add_drag_float(tag='img_Brightness_1',
                                   # label="Brightness",
                                   format ='Brightness: %.1f',
                                   default_value =0.0,
                                   max_value=100.,
                                   min_value=-100,
                                   speed=1,
                                   enabled=True,
                                   width=-1,
                                   callback=_update_textures_both_roi
                                  )
                dpg.add_drag_int(tag='img_roi_alpha_1',
                                   # label="Brightness",
                                   format ='ROI alpha: %.d\u0025',
                                   default_value =33,
                                   max_value=100.,
                                   min_value=0,
                                   speed=1,
                                   enabled=True,
                                   width=-1,
                                   callback=_update_textures_both_roi
                                  )
    
    
                
                # with dpg.group(tag='log_checkbox_group', horizontal=True,
                #    horizontal_spacing=init.group_spacer,
                #    show=True):
                # dpg.add_checkbox(label='Find nucleus', 
                #                  tag='nucleus_search_1',
                #                  default_value = False,
                #                  enabled=False,
                #                  # width=-1,
                #                  callback=_update_textures__dynamic_roi,
                #                  # parent='image_window_1'
                #                 )
                # dpg.add_drag_float(tag='nucl_tresh_ratio_1',
                #                    default_value =1.5,
                #                    max_value=3.,
                #                    min_value=0.0,
                #                    speed=0.01,
                #                    width=-1,
                #                    enabled=False,
                #                    callback = _update_textures__dynamic_roi
                #                   )
    
with dpg.window(label = 'Channel 2',
                tag='image_window_ch2',
                width = width_2,
                height = height_2,
                pos = position_2,
                autosize=True,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_move=True,
                no_bring_to_front_on_focus=True,
                show=True
                
               ):
    
    dpg.add_separator(tag ='IMAGE_CH2_top_sep',show=True)
    
    dpg.add_image(tex_2_name,
                  uv_min=(0,0),
                  uv_max=(1,1),
                  tag = 'texture_CH_2',before='img_win_2_table')

    dpg.add_separator(tag ='IMAGE_CH2_top_sep_2',show=True,parent='image_window_ch2')
    
    
    with dpg.table(header_row=False, width=-1,borders_innerH=False, 
                                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                                   no_pad_innerX=False,no_pad_outerX=True,no_host_extendX=True,
                                   no_clip=True,tag='img_win_2_table',parent='image_window_ch2'):
            # Add headers
        dpg.add_table_column(label="",tag='img_win_2_table_col1', width = int(width_2/3))
        dpg.add_table_column(label="",tag='img_win_2_table_col2', width = int(width_2/3))
        dpg.add_table_column(label="",tag='img_win_2_table_col3', width = int(width_2/3))

        # Add rows and columns
        with dpg.table_row(tag='img_win_2_table_row1'):
            dpg.add_drag_float(tag='cell_tresh_ratio_2',
                               default_value =1.0,
                               max_value=2.,
                               min_value=0.0,
                               speed=0.01,
                               width=-1,
                               enabled=False,
                               callback=_update_textures_both_roi
                              )


            
            # with dpg.group(tag='log_checkbox_group', horizontal=True,
            #    horizontal_spacing=init.group_spacer,
            #    show=True):
            dpg.add_checkbox(label='Find nucleus', 
                             tag='nucleus_search_2',
                             default_value = False,
                             enabled=False,
                             # width=-1,
                             callback=_update_textures_both_roi,
                             # parent='image_window_1'
                            )
            dpg.add_drag_float(tag='nucl_tresh_ratio_2',
                               default_value =1.5,
                               max_value=3.,
                               min_value=0.0,
                               speed=0.01,
                               width=-1,
                               enabled=False,
                               callback = _update_textures_both_roi
                              )












    with dpg.table(header_row=False, width=-1,borders_innerH=False, 
                                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                                   no_pad_innerX=False,no_pad_outerX=True,no_host_extendX=True,
                                   no_clip=True,tag='img_win_2_table_2_2',parent='image_window_2',before='texture_CH_2'):
            # Add headers
            dpg.add_table_column(label="",tag='img_win_2_table_2_col1', width = int(width_2/3))
            dpg.add_table_column(label="",tag='img_win_2_table_2_col2', width = int(width_2/3))
            dpg.add_table_column(label="",tag='img_win_2_table_2_col3', width = int(width_2/3))
            with dpg.table_row(tag='img_win_2_table_2_row1'):
            
                dpg.add_drag_float(tag='img_contrast_2',
                                   format ='Contrast: %.1f',
                                   default_value =1.0,
                                   max_value=5.,
                                   min_value=0.1,
                                   speed=0.1,
                                   enabled=True,
                                   width=-1,
                                   callback=_update_textures_both_roi
                                  )
                
            #     dpg.add_text('',tag='img_contrast_text_1')

                dpg.add_drag_float(tag='img_Brightness_2',
                                   # label="Brightness",
                                   format ='Brightness: %.1f',
                                   default_value =0.0,
                                   max_value=100.,
                                   min_value=-100,
                                   speed=1,
                                   enabled=True,
                                   width=-1,
                                   callback=_update_textures_both_roi
                                  )
                dpg.add_drag_int(tag='img_roi_alpha_2',
                                   # label="Brightness",
                                   format ='ROI alpha: %.d\u0025',
                                   default_value =33,
                                   max_value=100.,
                                   min_value=0,
                                   speed=1,
                                   enabled=True,
                                   width=-1,
                                   callback=_update_textures_both_roi
                                  )


































