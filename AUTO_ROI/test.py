import dearpygui.dearpygui as dpg
import numpy as np
import cv2
import os
from dep.automated_roi_TK import ImageROIProcessor

dpg.create_context()

def create_rgba_texture(image_data):
    # Ensure the image data is 2D (grayscale)
    if image_data.ndim != 2:
        raise ValueError("Image data should be a 2D array.")
    
    # Convert to a 3D RGB array (3 channels)
    rgba_data = np.stack([image_data] * 3, axis=-1)  # Duplicate grayscale data for RGB channels
    rgba_data = np.concatenate([rgba_data, np.ones((image_data.shape[0], image_data.shape[1], 1), dtype=np.uint8) * 255], axis=-1)  # Add alpha channel (fully opaque)
    
    # Flatten the RGBA array into a 1D list for the dynamic texture
    return rgba_data.flatten().tolist()



im_size=[500,500]


# Create and register the dynamic texture
input_path = os.path.join('samples/npy/','cell-201-01200_INT_ch_2.npy')
processor = ImageROIProcessor(input_path, input_path, False)

processor.load_image()

image_data = processor.image
print(type(processor.image))

image_data =(image_data* (255 / image_data.max())).astype(np.uint8)



processor.roi_image = processor.detect_cell_roi(processor.image,1.)
cell_roi = processor.roi_image
image_data = np.multiply(image_data, cell_roi)
image_data = cv2.resize(image_data, (im_size[0], im_size[1]), interpolation=cv2.INTER_CUBIC)
texture_data = create_rgba_texture(image_data/255)

# with dpg.texture_registry(show=True):
#     dpg.add_dynamic_texture(width=image_data.shape[1], height=image_data.shape[0], default_value=texture_data, tag="texture_tag")

# Update texture dynamically using NumPy (when the color picker changes)
def _update_dynamic_textures(sender, app_data):
    find_nucleus = dpg.get_value('find_nucl_chk')
    cell_rat = dpg.get_value('cell_tresh_ratio')
    nucl_rat = dpg.get_value('nucl_tresh_ratio')
    # print(cell_rat)
    image_data = processor.image


    image_data =(image_data* (255 / image_data.max())).astype(np.uint8)
    processor.roi_image = processor.detect_cell_roi(processor.image,cell_rat)

    cell_roi = processor.roi_image
    if not find_nucleus:
        

        
        full_mask = cell_roi
        # image_data = cv2.resize(image_data, (im_size[0], im_size[1]), interpolation=cv2.INTER_CUBIC)
        # new_texture_data = create_rgba_texture(image_data/255)
    else:
        nucleus_roi = processor.detect_nucleus_roi(processor.image, cell_roi, nucl_rat)
        full_mask = processor.make_full_roi(cell_roi, nucleus_roi)
        # image_data = np.multiply(image_data, full_mask)
    # resized_image = cv2.resize(image_data, (im_size[0], im_size[1]), interpolation=cv2.INTER_CUBIC)
    # resized_mask = cv2.resize(full_mask, (im_size[0], im_size[1]), interpolation=cv2.INTER_CUBIC)
    # image_data = cv2.resize(image_data, (im_size[0], im_size[1]), interpolation=cv2.INTER_CUBIC)
    print(5)
    rgba_image = np.zeros((image_data.shape[1], image_data.shape[0], 4), dtype=np.uint8)
    rgba_image[..., 0] = image_data  # Red channel
    rgba_image[..., 1] = image_data  # Green channel
    rgba_image[..., 2] = image_data  # Blue channel
    rgba_image[..., 3] = 255

    overlay_alpha = 128  # Transparency level (0-255, where 255 is fully opaque)
    rgba_image[full_mask > 0, 0] = 255  # Red channel set to max for mask
    rgba_image[full_mask > 0, 1] = image_data[full_mask > 0]  # Blend green
    rgba_image[full_mask > 0, 2] = image_data[full_mask > 0]  # Blend blue
    rgba_image[full_mask > 0, 3] = overlay_alpha

    rgba_image  =cv2.resize(rgba_image, (im_size[0], im_size[1]), interpolation=cv2.INTER_CUBIC)
    rgba_image=rgba_image/255
    # new_texture_data = create_rgba_texture(image_data/255)
    # new_texture_data = image_data.flatten().tolist()
    print(6)
    new_texture_data = rgba_image.flatten().tolist()    

    
    dpg.set_value("texture_tag", new_texture_data)



# texture_data = []
# for i in range(0, 100 * 100):
#     texture_data.append(255 / 255)
#     texture_data.append(0)
#     texture_data.append(255 / 255)
#     texture_data.append(255 / 255)

with dpg.texture_registry(show=False):
    dpg.add_dynamic_texture(width=image_data.shape[0], height=image_data.shape[1], default_value=texture_data, tag="texture_tag")


# def _update_dynamic_textures(sender, app_data, user_data):
#     new_color = dpg.get_value(sender)
#     new_color[0] = new_color[0] / 255
#     new_color[1] = new_color[1] / 255
#     new_color[2] = new_color[2] / 255
#     new_color[3] = new_color[3] / 255

#     new_texture_data = []
#     for i in range(0, 100 * 100):
#         new_texture_data.append(new_color[0])
#         new_texture_data.append(new_color[1])
#         new_texture_data.append(new_color[2])
#         new_texture_data.append(new_color[3])

#     dpg.set_value("texture_tag", new_texture_data)


with dpg.window(label="Tutorial"):
    dpg.add_image("texture_tag")
    # dpg.add_color_picker((255, 0, 255, 255), label="Texture",
    #                      no_side_preview=True, alpha_bar=True, width=200,
    #                      callback=_update_dynamic_textures)
    dpg.add_drag_float(tag='cell_tresh_ratio',default_value =1.0,max_value=2.,min_value=0.0,speed=0.01,callback=_update_dynamic_textures)
    dpg.add_checkbox(label='find nucleus', tag='find_nucl_chk',default_value=False,callback = _update_dynamic_textures)
    dpg.add_drag_float(tag='nucl_tresh_ratio',default_value =1.5,max_value=3.,min_value=0.0,speed=0.01,callback = _update_dynamic_textures)
_update_dynamic_textures('cell_tresh_ratio',1.)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()