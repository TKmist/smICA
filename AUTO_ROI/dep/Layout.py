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

#########################################################################
'''Items image windows'''
#########################################################################
dpg.add_text('Channel 1',tag='Img_1_window_text_title',parent='image_window_1')
dpg.add_separator(tag ='IMAGE_CH1_top_sep',show=True,parent='image_window_1')
    
dpg.add_image(init.tex_1_name,
                  uv_min=(0,0),
                  uv_max=(1,1),
                  tag = 'texture_CH_1',
                  parent='image_window_1')

dpg.add_text('Channel 2',tag='Img_2_window_text_title',parent='image_window_2')
dpg.add_separator(tag ='IMAGE_CH2_top_sep',show=True,parent='image_window_2')
    
dpg.add_image(init.tex_2_name,
                  uv_min=(0,0),
                  uv_max=(1,1),
                  tag = 'texture_CH_2',
                  parent='image_window_2')



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
                    modal=False
                   )
