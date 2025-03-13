import numpy as np

import dearpygui.dearpygui as dpg
import cv2
# Texture dimensions
image_width, image_height = 512, 512

# Function to create an image with contours and labels
def create_texture_with_contours(contours):
    # Create a white image
    opencv_image = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255  # White RGB
    
    # Iterate through contours to draw and label them
    for i, contour in enumerate(contours):
        cv2.drawContours(opencv_image, [contour], contourIdx=-1, color=(0, 0, 0), thickness=-1)  # Black shape
        
        # Compute centroid
        moments = cv2.moments(contour)
        centroid = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
        
        # Label shape
        label = str(i + 1)
        cv2.putText(opencv_image, label, centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)  # Red text
    
    # Add alpha channel
    opencv_image_with_alpha = np.dstack((opencv_image, np.full((image_height, image_width), 255, dtype=np.uint8)))
    return opencv_image_with_alpha

# Define contours for two different images
contours_1 = [
    np.array([[100, 100], [150, 120], [130, 170], [80, 150], [90, 120]], dtype=np.int32),
    np.array([[300, 100], [350, 150], [330, 200], [280, 180], [290, 150]], dtype=np.int32)
]

contours_2 = [
    np.array([[200, 300], [250, 350], [220, 400], [180, 380], [190, 350]], dtype=np.int32),
    np.array([[50, 50], [100, 75], [80, 130], [40, 100], [45, 70]], dtype=np.int32)
]

# Generate texture images
texture_data_1 = create_texture_with_contours(contours_1)
texture_data_2 = create_texture_with_contours(contours_2)

# Click handler function
def on_image_click(sender, app_data, user_data):
    image_tag, contours = user_data  # Unpack which texture and its contours
    mouse_pos = dpg.get_mouse_pos()
    image_pos = dpg.get_item_pos(image_tag)
    image_pos[0]=image_pos[0]+dpg.get_item_configuration(image_tag)['indent']
    # Compute relative click position
    relative_pos = (mouse_pos[0] - image_pos[0], mouse_pos[1] - image_pos[1])

    # Check if click is within image bounds
    if 0 <= relative_pos[0] < image_width and 0 <= relative_pos[1] < image_height:
        x, y = int(relative_pos[0]), int(relative_pos[1])
        
        # Determine which shape (if any) was clicked
        clicked_shape = None
        for i, contour in enumerate(contours):
            if cv2.pointPolygonTest(contour, (x, y), False) >= 0:
                clicked_shape = i + 1
                break
        
        if clicked_shape:
            print(f"Clicked inside Shape {clicked_shape} in {image_tag} at position: ({x}, {y})")
        else:
            print(f"Click was outside all shapes in {image_tag} at position: ({x}, {y})")
    else:
        print(f"Click was outside the image {image_tag}.")

# Setup Dear PyGui context
dpg.create_context()
dpg.create_viewport(title='Multiple Image Windows', width=1200, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
# Create texture registry
with dpg.texture_registry():
    dpg.add_dynamic_texture(image_width, image_height, texture_data_1.flatten(), tag="cnt_texture_CH_1")
    dpg.add_static_texture(image_width, image_height, texture_data_2.flatten(), tag="cnt_texture_CH_2")

# Create handler registries for each image
with dpg.item_handler_registry(tag="image_handler_1"):
    pass
    

with dpg.item_handler_registry(tag="image_handler_2"):
    pass
    

# Create two windows with images
with dpg.window(label="Image Window 1", tag="image_window_1", pos=(50, 50)):
    dpg.add_image("cnt_texture_CH_1", tag="texture_CH_1",uv_min=(0,0),
                  uv_max=(1,1),indent=8)
    # dpg.add_item_clicked_handler(callback=on_image_click, user_data=("texture_CH_1", contours_1),parent = 'image_handler_1')
    dpg.add_item_clicked_handler(callback=lambda: print('dupa'), user_data=("texture_CH_1", contours_1),parent = 'image_handler_1')
    dpg.bind_item_handler_registry("texture_CH_1", "image_handler_1")

with dpg.window(label="Image Window 2", tag="image_window_2", pos=(600, 50)):
    dpg.add_image("cnt_texture_CH_2", tag="texture_CH_2")
    dpg.add_item_clicked_handler(callback=on_image_click, user_data=("texture_CH_2", contours_2),parent = 'image_handler_2')
    dpg.bind_item_handler_registry("texture_CH_2", "image_handler_2")

# Set the viewport

dpg.start_dearpygui()
dpg.destroy_context()
