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
                  tag = 'texture_CH_1')
    
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
                  tag = 'texture_CH_2')















































