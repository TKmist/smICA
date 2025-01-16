import dearpygui.dearpygui as dpg

def adjust_column_ratios(sender, app_data, user_data):
    # Get the width of the parent window containing the table
    window_width = dpg.get_item_width(user_data)
    
    # Calculate the column widths based on the 2:1 ratio
    column1_width = (2 / 3) * window_width
    column2_width = (1 / 3) * window_width
    
    # Adjust the table column widths
    dpg.set_table_column_width("MyTable", 0, int(column1_width))
    dpg.set_table_column_width("MyTable", 1, int(column2_width))

# Create the main application
dpg.create_context()

with dpg.window(label="Main Window", tag="MainWindow"):
    # Create a table with auto-adjustable width
    with dpg.table(label="My Table", tag="MyTable", resizable=False, borders_innerH=True, borders_innerV=True):
        # Add table headers
        dpg.add_table_column(label="Column 1")
        dpg.add_table_column(label="Column 2")
        
        # Add rows with data
        with dpg.table_row():
            dpg.add_text("Row 1, Col 1")
            dpg.add_text("Row 1, Col 2")
        with dpg.table_row():
            dpg.add_text("Row 2, Col 1")
            dpg.add_text("Row 2, Col 2")

# Attach a resize handler to dynamically adjust column widths
with dpg.handler_registry():
    dpg.add_resize_handler("MainWindow", callback=adjust_column_ratios, user_data="MainWindow")

dpg.create_viewport(title="Table with Column Ratios", width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
