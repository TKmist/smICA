import numpy as np

import dearpygui.dearpygui as dpg
import cv2
# Texture dimensions
image_width, image_height = 512, 512

# Create a white texture
texture_data = np.ones((image_height, image_width, 4), dtype=np.uint8) * 255  # White RGBA

# List of contours (irregular shapes)
contours = [
    np.array([[100, 100], [150, 120], [130, 170], [80, 150], [90, 120]], dtype=np.int32),
    np.array([[300, 100], [350, 150], [330, 200], [280, 180], [290, 150]], dtype=np.int32),
    np.array([[200, 300], [250, 350], [220, 400], [180, 380], [190, 350]], dtype=np.int32)
]

# Create an OpenCV-compatible image (without alpha channel)
opencv_image = np.ones((image_height, image_width, 3), dtype=np.uint8) * 255  # White RGB

# Draw the contours as filled black shapes and add labels
font_scale = 0.5  # Font size
font_thickness = 1  # Font thickness

# Iterate through the contours to draw and label them
for i, contour in enumerate(contours):
    # Draw the contour (black)
    cv2.drawContours(opencv_image, [contour], contourIdx=-1, color=(0, 0, 0), thickness=-1)
    
    # Calculate the centroid of the contour for label placement
    moments = cv2.moments(contour)
    centroid = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
    
    # Label the contour with an integer label (1, 2, 3, ...)
    label = str(i + 1)
    cv2.putText(opencv_image, label, centroid, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), font_thickness)  # Red label

# Add an alpha channel to the OpenCV image
opencv_image_with_alpha = np.dstack((opencv_image, np.full((image_height, image_width), 255, dtype=np.uint8)))

# Update texture_data with the OpenCV image
texture_data[:] = opencv_image_with_alpha

# Callback to get pixel position and value and limit click to shapes
def on_image_click(sender, app_data, user_data):

    print('ok')

    # Get the global mouse position
    mouse_pos = dpg.get_mouse_pos()
    
    # Get the image's position and size
    image_pos = dpg.get_item_pos(user_data)  # user_data contains the image tag
    relative_pos = (mouse_pos[0] - image_pos[0], mouse_pos[1] - image_pos[1])
    
    # Check if the click is within the image bounds
    if 0 <= relative_pos[0] < image_width and 0 <= relative_pos[1] < image_height:
        x = int(relative_pos[0])
        y = int(relative_pos[1])
        
        # Iterate through the contours to check if the clicked point is inside any of the shapes
        clicked_shape = None
        for i, contour in enumerate(contours):

            print(contour)
            # Check if the point is inside the current shape using pointPolygonTest
            if cv2.pointPolygonTest(contour, (x, y), False) >= 0:
                clicked_shape = i + 1  # Label of the clicked shape (1-indexed)
                break
        
        if clicked_shape:
            print(f"Clicked inside Shape {clicked_shape} at position: ({x}, {y})")
        else:
            print(f"Click was outside all shapes at position: ({x}, {y})")
    else:
        print("Click was outside the image.")

# Setup Dear PyGui context
dpg.create_context()
# Set the viewport
dpg.create_viewport(title='Pixel Click Example with Multiple Shapes and Labels', width=600, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
# Create a texture registry and add the modified texture
with dpg.texture_registry():
    dpg.add_static_texture(image_width, image_height, texture_data.flatten(), tag="contours_texture")

# Create an item handler registry
with dpg.item_handler_registry(tag="image_handler"):
    dpg.add_item_clicked_handler(callback=on_image_click, user_data="texture_CH_2")

# Create a simple window with an image
with dpg.window(label="Image Window", tag="image_window_2"):
    pass
    dpg.add_image("contours_texture", tag="texture_CH_2")
    # Attach the item handler to the image
    dpg.bind_item_handler_registry("texture_CH_2", "image_handler")


dpg.start_dearpygui()
dpg.destroy_context()