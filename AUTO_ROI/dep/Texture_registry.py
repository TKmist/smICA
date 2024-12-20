# def update_texture(np_imgage_input):
#     # global ratio_w,dif_vp0_width
    
#     ratio_w = init.size_ratio['width']
#     width = np_imgage_input.shape[0]
#     height = np_imgage_input.shape[1]
    
#     w = int(np.round(dpg.get_item_width('image_window_1')))-15*ratio_w
#     h = w
    
#     image=basf.plot_IMAGE(np_imgage_input,w,h)
#     lprint(type(image))
    
#     image_array = np.array(image, dtype=np.float32) / 255
    
#     lprint(image_array.shape)


#     dpg_image = image_array[:, :, [0, 1, 2, 3]].reshape(-1).tolist()

#     return dpg_image
    
    
    
    
dpg.add_texture_registry(show=False,tag='texture_reg')


w = int(np.round(init.image_window_1['width']))-15
h = w
# lprint(w,h)
callback.NO_IMAGE_TEXTURE= np.load(os.path.join('res','NO_image_INT.npy'))


callback.Current_image_1 = callback.NO_IMAGE_TEXTURE
callback.Current_image_2 = callback.NO_IMAGE_TEXTURE





dpg_image_1,dpg_image_2 = basf.create_textures(callback.Current_image_1,callback.Current_image_2,w,h)
















dpg.add_dynamic_texture(width=w,
                        height=h,
                        default_value=dpg_image_1,
                        tag=init.tex_1_name,
                        parent = 'texture_reg')
dpg.add_dynamic_texture(width=w,
                        height=h,
                        default_value=dpg_image_2,
                        tag=init.tex_2_name,
                        parent = 'texture_reg')


