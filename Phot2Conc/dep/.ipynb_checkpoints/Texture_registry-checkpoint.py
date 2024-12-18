
log_it('Texture_registry - loaded on '+str(datetime.datetime.now()),'a')
tex_1_name = 'texture_tag_chan_1'
tex_2_name = 'texture_tag_chan_2'

def update_texture(np_imgage_input):
    global ratio_w,dif_vp0_width
    
    if dpg.get_value('INT_checkbox') and dpg.get_value('LT_checkbox'):
            pass
    elif dpg.get_value('INT_checkbox') and not dpg.get_value('LT_checkbox'):
        np_imgage_input = (np_imgage_input[0],None)
    elif not dpg.get_value('INT_checkbox') and dpg.get_value('LT_checkbox'):
        np_imgage_input = (None,np_imgage_input[1])
    else:
        pass
    if isinstance(np_imgage_input[0],np.ndarray) and isinstance(np_imgage_input[1],np.ndarray):
        width = np_imgage_input[0].shape[0]
        height = np_imgage_input[0].shape[1]
        
    elif isinstance(np_imgage_input[0],np.ndarray) and not isinstance(np_imgage_input[1],np.ndarray):
        width = np_imgage_input[0].shape[0]
        height = np_imgage_input[0].shape[1]
    elif not isinstance(np_imgage_input[0],np.ndarray) and isinstance(np_imgage_input[1],np.ndarray):
        width = np_imgage_input[1].shape[0]
        height = np_imgage_input[1].shape[1]
    else:
        pass
    
    
    
    

    
    
    
    
    
    
    w = (dpg.get_viewport_width()-left_indent-dpg.get_item_width('PTU_DATA_window')-5*internal_indent-init_widths['FCS_window']*ratio_w)//2
    h = w
    
    image=image_INT_LT(np_imgage_input,w,h)
    
    
    
    dpg_image = []
    for i in range(0, image._size[1]):
        for j in range(0, image._size[0]):
            pixel = image.getpixel((j, i))
            
            dpg_image.append(pixel[0]/255)
            dpg_image.append(pixel[1]/255)
            dpg_image.append(pixel[2]/255)
            dpg_image.append(255/255)
    return dpg_image
    
    
    
    
dpg.add_texture_registry(show=False,tag='texture_reg')










w=init_widths['image_window_ch1']
h =init_heights['image_window_ch1']

NO_IMAGE_INTENSITY = np.load(os.path.join('res','NO_image_INT.npy'))
NO_IMAGE_LIFETIME = np.load(os.path.join('res','NO_image_LT.npy'))


global Current_image_1,Current_image_2





Current_image_1 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
Current_image_2 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)








image_1=image_INT_LT(Current_image_1,w,h)
image_2=image_INT_LT(Current_image_2,w,h)






dpg_image_1 = []
for i in range(0, image_1._size[1]):
    for j in range(0, image_1._size[0]):
        pixel = image_1.getpixel((j, i))
        
        dpg_image_1.append(pixel[0]/255)
        dpg_image_1.append(pixel[1]/255)
        dpg_image_1.append(pixel[2]/255)
        dpg_image_1.append(255/255)
        
dpg_image_2 = []
for i in range(0, image_2._size[1]):
    for j in range(0, image_2._size[0]):
        pixel = image_2.getpixel((j, i))
        
        dpg_image_2.append(pixel[0]/255)
        dpg_image_2.append(pixel[1]/255)
        dpg_image_2.append(pixel[2]/255)
        dpg_image_2.append(255/255)













dpg.add_dynamic_texture(width=w,
                        height=h,
                        default_value=dpg_image_1,
                        tag=tex_1_name,
                        parent = 'texture_reg')
dpg.add_dynamic_texture(width=w,
                        height=h,
                        default_value=dpg_image_2,
                        tag=tex_2_name,
                        parent = 'texture_reg')


