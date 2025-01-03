import dearpygui.dearpygui as dpg
import nunmpy as np
import os
import cv2

image_data = np.load(os.path.join('samples/npy/','cell-201-01200_INT_ch_2.npy'))
image_data =(image_data* (255 / image_data.max())).astype(np.uint8)

image_data = cv2.resize(image_data, (500, 500), interpolation=cv2.INTER_CUBIC)
dpg.create_context()

texture_data = []
for i in range(0, 500 * 500):
    texture_data.append(255 / 255)
    texture_data.append(0)
    texture_data.append(255 / 255)
    texture_data.append(255 / 255)

with dpg.texture_registry(show=True):
    dpg.add_dynamic_texture(width=500, height=500, default_value=texture_data, tag="texture_tag")


def _update_dynamic_textures(sender, app_data, user_data):
    new_color = dpg.get_value(sender)
    new_color[0] = new_color[0] / 255
    new_color[1] = new_color[1] / 255
    new_color[2] = new_color[2] / 255
    new_color[3] = new_color[3] / 255

    new_texture_data = []
    for i in range(0, 500 * 500):
        new_texture_data.append(new_color[0])
        new_texture_data.append(new_color[1])
        new_texture_data.append(new_color[2])
        new_texture_data.append(new_color[3])

    dpg.set_value("texture_tag", new_texture_data)


with dpg.window(label="Tutorial"):
    dpg.add_image("texture_tag")
    dpg.add_color_picker((255, 0, 255, 255), label="Texture",
                         no_side_preview=True, alpha_bar=True, width=600,
                         callback=_update_dynamic_textures)


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()