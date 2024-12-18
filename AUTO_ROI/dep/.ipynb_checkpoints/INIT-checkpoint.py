import inspect
import dearpygui.dearpygui as dpg
class inits:
    def __init__(self):
        
        self.init_top_indent = 24+11
        self.init_bottom_indent  = 11
        self.init_left_indent  = 11
        self.init_right_indent  = 11
        self.init_internal_indent  = 11
        self.init_font_size  = 18
        self.init_group_spacer  = 2
        self.current_font_size = self.init_font_size
        self.init_image_width1  = 1224
        self.init_image_height1  = 200
        self.init_var_def_group_1_spacer =20
        self.ratio_w =1
        self.ratio_h = 1
        self.dif_vp0_width =  380
        
        
        self.size_pos = {
                        'VIEWPORT':{'width':1205+self.dif_vp0_width,
                                   'height':950+self.init_bottom_indent + 11,
                                   'pos':(10,10)},
                        'file_window':380,
            
                        }
        
    def lnprint(self,*args, **kwargs):
     # Get the current frame's caller information (go one level up)
        caller_frame = inspect.currentframe().f_back
        line_number = caller_frame.f_lineno
        # Get the filename of the script
        file_name = caller_frame.f_code.co_filename
        function_name = caller_frame.f_code.co_name
        # Print the line number and filename first
        print(f"File {file_name}, Function '{function_name}', Line {line_number}: ", end="\n")

        # Pass all arguments and keyword arguments to the built-in print function
        print(*args, **kwargs)
        
        
        
class _init_Menu:
    
    
    def __init__(self,VERSION):
        self.VERSION = VERSION
        
        
    
    
    
    
    
    def mount_main_Menu_bar(self):
    
        with dpg.viewport_menu_bar(tag="vieport's_menubar"):
            with dpg.menu(label="File",tag='menu_file_dropout'):
                dpg.add_menu_item(label="Open PTU folder",callback=None,tag='menu_item_open_ptu')
                dpg.add_menu_item(label="Exit",callback=lambda: dpg.stop_dearpygui(),tag='menu_item_exit')
            

    