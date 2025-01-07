with dpg.window(label='',
                width=init.file_window['width'],
                height=init.file_window['height'],
                pos=init.file_window['pos'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='file_window',
                show=True
               ):
    pass

with dpg.window(label='',
                width=init.image_window_1['width'],
                height=init.image_window_1['height'],
                pos=init.image_window_1['pos'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='image_window_1',
                show=True
               ):
    pass

with dpg.window(label='',
                width=init.image_window_2['width'],
                height=init.image_window_2['height'],
                pos=init.image_window_2['pos'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='image_window_2',
                show=True
               ):
    pass





#########################################################################
'''Items in the left panel'''
#########################################################################

dpg.add_text('FILES',tag='FILES_window_text_title',parent='file_window')
dpg.add_separator(tag ='sep_left_1',parent='file_window')
'''Window containing file selection panel.'''
list_box = dpg.add_listbox(items=callback.files,
                       width=init.file_box['width'],
                       num_items=init.file_box['num_items'],
                       tag='file_box',
                           parent='file_window',
                           callback=callback.callback_listbox

                      )
dpg.add_separator(tag ='sep_left_2',parent='file_window')
dpg.add_button(label="Save single roi",
                               tag='save_roi_button',
                               parent = 'file_window',
                               width = init.save_roi_button['width'],
                               callback=callback.callback_save_single_roi,
               enabled=False
                              )
# with dpg.tooltip('save_roi_button',tag='save_roi_button_tooltip'):
#     dpg.add_text('This button is enabled only if the output directory is defined. Open "File" -> "Open output directory"',tag='Correlate_all_button_tooltip_text')
dpg.bind_item_theme('save_roi_button', 'fit_button_theme')

dpg.add_button(label="Save all roi",
                               tag='save_all_roi_button',
                               parent = 'file_window',
                               width = init.save_roi_button['width'],
                               callback=callback.callback_save_all_roi,
               enabled=False
                              )
dpg.bind_item_theme('save_all_roi_button', 'fit_button_theme')
#########################################################################
'''Items image windows'''
#########################################################################
dpg.add_text('Channel 1',tag='Img_1_window_text_title',parent='image_window_1')
dpg.add_separator(tag ='IMAGE_CH1_top_sep',show=True,parent='image_window_1')
    
dpg.add_image(init.tex_1_name,
                  uv_min=(0,0),
                  uv_max=(1,1),
                  tag = 'texture_CH_1',
                  parent='image_window_1',before='IMAGE_CH1_top_sep_2')
dpg.add_separator(tag ='IMAGE_CH1_top_sep_2',show=True,parent='image_window_1')


with dpg.table(header_row=False, width=-1,borders_innerH=False, 
                               borders_outerH=False, borders_innerV=False, borders_outerV=False,
                               no_pad_innerX=False,no_pad_outerX=True,no_host_extendX=True,
                               no_clip=True,tag='img_win_1_table',parent='image_window_1'):
        # Add headers
        dpg.add_table_column(label="",tag='img_win_1_table_col1', width = int(init.image_window_1['width']/3))
        dpg.add_table_column(label="",tag='img_win_1_table_col2', width = int(init.image_window_1['width']/3))
        dpg.add_table_column(label="",tag='img_win_1_table_col3', width = int(init.image_window_1['width']/3))

        # Add rows and columns
        with dpg.table_row(tag='img_win_1_table_row1'):
            dpg.add_drag_float(tag='cell_tresh_ratio_1',
                               default_value =1.0,
                               max_value=2.,
                               min_value=0.0,
                               speed=0.01,
                               width=-1,
                               callback=callback._update_textures_roi
                              )


            
            # with dpg.group(tag='log_checkbox_group', horizontal=True,
            #    horizontal_spacing=init.group_spacer,
            #    show=True):
            dpg.add_checkbox(label='Find nucleus', 
                             tag='nucleus_search_1',
                             default_value = False,
                             # width=-1,
                             callback=callback._update_textures_roi,
                             # parent='image_window_1'
                            )
            dpg.add_drag_float(tag='nucl_tresh_ratio_1',
                               default_value =1.5,
                               max_value=3.,
                               min_value=0.0,
                               speed=0.01,
                               width=-1,
                               callback = callback._update_textures_roi
                              )
            



# dpg.add_checkbox(label='Search for nucleus', tag='nucleus_search_1',default_value = False,callback=None,parent='image_window_1')

dpg.add_text('Channel 2',tag='Img_2_window_text_title',parent='image_window_2')
dpg.add_separator(tag ='IMAGE_CH2_top_sep',show=True,parent='image_window_2')
dpg.add_image(init.tex_2_name,
                  uv_min=(0,0),
                  uv_max=(1,1),
                  tag = 'texture_CH_2',
                  parent='image_window_2',before='IMAGE_CH2_top_sep_2')
dpg.add_separator(tag ='IMAGE_CH2_top_sep_2',show=True,parent='image_window_2')

with dpg.table(header_row=False, width=-1,borders_innerH=False, 
                               borders_outerH=False, borders_innerV=False, borders_outerV=False,
                               no_pad_innerX=False,no_pad_outerX=True,no_host_extendX=True,
                               no_clip=True,tag='img_win_2_table',parent='image_window_2'):
        # Add headers
        dpg.add_table_column(label="",tag='img_win_2_table_col1', width = int(init.image_window_2['width']/3))
        dpg.add_table_column(label="",tag='img_win_2_table_col2', width = int(init.image_window_2['width']/3))
        dpg.add_table_column(label="",tag='img_win_2_table_col3', width = int(init.image_window_2['width']/3))

        # Add rows and columns
        with dpg.table_row(tag='img_win_2_table_row1'):
            dpg.add_drag_float(tag='cell_tresh_ratio_2',
                               default_value =1.0,
                               max_value=2.,
                               min_value=0.0,
                               speed=0.01,
                               width=-1,
                               callback=callback._update_textures_roi
                              )


            
            # with dpg.group(tag='log_checkbox_group', horizontal=True,
            #    horizontal_spacing=init.group_spacer,
            #    show=True):
            dpg.add_checkbox(label='Find nucleus', 
                             tag='nucleus_search_2',
                             default_value = False,
                             # width=-1,
                             callback=callback._update_textures_roi,
                             # parent='image_window_1'
                            )
            dpg.add_drag_float(tag='nucl_tresh_ratio_2',
                               default_value =1.5,
                               max_value=3.,
                               min_value=0.0,
                               speed=0.01,
                               width=-1,
                               callback = callback._update_textures_roi
                              )

#########################################################################
'''Items dialog windows'''
#########################################################################


dpg.add_file_dialog(directory_selector=True,
                    label = 'Select working directory',
                    width = init.file_dialog_id['width'],
                    height = init.file_dialog_id['height'],
                    show=False,
                    file_count=5,
                    default_path=callback.last_directory,
                    callback=callback.callback_directory_select,
                    cancel_callback=callback.callback_empty,
                    tag="file_dialog_id",
                    modal=False,
                   )
