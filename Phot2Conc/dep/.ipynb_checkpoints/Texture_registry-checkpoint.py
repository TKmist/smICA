
log_it('Texture_registry - loaded on '+str(datetime.datetime.now()),'a')
tex_1_name = 'texture_tag_chan_1'
tex_2_name = 'texture_tag_chan_2'

def update_texture(np_imgage_input):
    global _fin_im_size 
    global ratio_w,dif_vp0_width

   
    
    # if dpg.get_value('INT_checkbox') and dpg.get_value('LT_checkbox'):
    #         pass
    # elif dpg.get_value('INT_checkbox') and not dpg.get_value('LT_checkbox'):
    #     np_imgage_input = (np_imgage_input[0],None)
    # elif not dpg.get_value('INT_checkbox') and dpg.get_value('LT_checkbox'):
    #     np_imgage_input = (None,np_imgage_input[1])
    # else:
    #     pass
    # if isinstance(np_imgage_input[0],np.ndarray) and isinstance(np_imgage_input[1],np.ndarray):
    #     width = np_imgage_input[0].shape[0]
    #     height = np_imgage_input[0].shape[1]
        
    # elif isinstance(np_imgage_input[0],np.ndarray) and not isinstance(np_imgage_input[1],np.ndarray):
    #     width = np_imgage_input[0].shape[0]
    #     height = np_imgage_input[0].shape[1]
    # elif not isinstance(np_imgage_input[0],np.ndarray) and isinstance(np_imgage_input[1],np.ndarray):
    #     width = np_imgage_input[1].shape[0]
    #     height = np_imgage_input[1].shape[1]
    # else:
    #     pass
    
    
    
    

    
    
    
    
    
    
    w = (dpg.get_viewport_width()-left_indent-dpg.get_item_width('PTU_DATA_window')-5*internal_indent-init_widths['FCS_window']*ratio_w)//2
    h = w
    
    # image=image_INT_LT(np_imgage_input,w,h)
    image=plot_IMAGE(np_imgage_input,w,h)
    
    _fin_im_size=image.shape
    
    # print('image',image._size)
    dpg_image = convert_to_texture(image)
    # dpg_image = []
    # for i in range(0, image._size[1]):
    #     for j in range(0, image._size[0]):
    #         pixel = image.getpixel((j, i))
            
    #         dpg_image.append(pixel[0]/255)
    #         dpg_image.append(pixel[1]/255)
    #         dpg_image.append(pixel[2]/255)
    #         dpg_image.append(255/255)
    return dpg_image
    
def convert_to_texture(img):
    height, width, channels = img.shape
    
    # Ensure the image is in range [0, 255]
    if img.max() <= 1.0:  # If the image is in range [0, 1]
        img = (img * 255).astype(np.uint8)
    
    # Add alpha channel (255) to every pixel
    alpha_channel = np.full((height, width, 1), 255, dtype=np.uint8)  # Full opacity
    img_rgba = np.concatenate((img, alpha_channel), axis=2)  # (H, W, 4)
    
    # Normalize pixel values from [0, 255] to [0, 1] (convert to float32)
    img_rgba_normalized = img_rgba.astype(np.float32) / 255.0
    
    # Flatten the array into a 1D list for DearPyGui
    return img_rgba_normalized.flatten().tolist()    
    
    
dpg.add_texture_registry(show=False,tag='texture_reg')










w=init_widths['image_window_ch1']
h =init_heights['image_window_ch1']

NO_IMAGE_INTENSITY = np.load(os.path.join('res','NO_image_INT.npy'))
# NO_IMAGE_LIFETIME = np.load(os.path.join('res','NO_image_LT.npy'))


global Current_image_1,Current_image_2





# Current_image_1 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
# Current_image_2 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
Current_image_1 = NO_IMAGE_INTENSITY
Current_image_2 = NO_IMAGE_INTENSITY


processor_1 = ImageROIProcessor()
processor_1.image=(NO_IMAGE_INTENSITY*255).astype(np.uint8)

processor_2 = ImageROIProcessor()
processor_2.image=(NO_IMAGE_INTENSITY*255).astype(np.uint8)

rgba_image_1 = im_to_rgbim(processor_1.image.astype(np.uint8))
rgba_image_2 = im_to_rgbim(processor_2.image.astype(np.uint8))

rgba_image_1  =cv2.resize(rgba_image_1, (w, h), interpolation=cv2.INTER_CUBIC)
rgba_image_2  =cv2.resize(rgba_image_2, (w, h), interpolation=cv2.INTER_CUBIC)


dpg_image_1=(rgba_image_1.astype(np.float32) /np.max(processor_1.image.astype(np.uint8))).flatten().tolist()
dpg_image_2=(rgba_image_2.astype(np.float32) /np.max(processor_2.image.astype(np.uint8))).flatten().tolist()

# dpg.set_value(tex_name, new_texture_data)

# _update_textures_both_roi('ch1',None)
# _update_textures_both_roi('ch2',None)

# image_1=image_INT_LT(Current_image_1,w,h)
# image_2=image_INT_LT(Current_image_2,w,h)

# image_1=plot_IMAGE(Current_image_1,w,h)
# image_2=plot_IMAGE(Current_image_2,w,h)



# dpg_image_1 = convert_to_texture(image_1)
# dpg_image_1 = []
# for i in range(0, image_1._size[1]):
#     for j in range(0, image_1._size[0]):
#         pixel = image_1.getpixel((j, i))
        
#         dpg_image_1.append(pixel[0]/255)
#         dpg_image_1.append(pixel[1]/255)
#         dpg_image_1.append(pixel[2]/255)
#         dpg_image_1.append(255/255)
        
# dpg_image_2 = []
# for i in range(0, image_2._size[1]):
#     for j in range(0, image_2._size[0]):
#         pixel = image_2.getpixel((j, i))
        
#         dpg_image_2.append(pixel[0]/255)
#         dpg_image_2.append(pixel[1]/255)
#         dpg_image_2.append(pixel[2]/255)
#         dpg_image_2.append(255/255)

# dpg_image_2 = convert_to_texture(image_2)











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


