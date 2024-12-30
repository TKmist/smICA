import dearpygui.dearpygui as dpg

# Example image dimensions (replace with your actual dimensions)
image_width = 512
image_height = 512

# Callback to get click position
def get_pixel_position(sender, app_data, user_data):
    # Get the global mouse position
    mouse_pos = dpg.get_mouse_pos()
    
    # Get the image's position
    image_pos = dpg.get_item_pos("texture_CH_2")
    
    # Calculate relative position
    relative_pos = (mouse_pos[0] - image_pos[0], mouse_pos[1] - image_pos[1])
    
    # Clamp the position to the image boundaries
    x = max(0, min(relative_pos[0], image_width))
    y = max(0, min(relative_pos[1], image_height))
    
    print(f"Clicked position in pixels: ({int(x)}, {int(y)})")

# Setup Dear PyGui context
dpg.create_context()

# Create a simple window with an image
with dpg.window(label="Image Window", tag="image_window_2"):
    dpg.add_image("your_texture_tag", tag="texture_CH_2")

# Add a mouse click handler
with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=get_pixel_position)

# Set the viewport
dpg.create_viewport(title='Pixel Click Example', width=600, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()