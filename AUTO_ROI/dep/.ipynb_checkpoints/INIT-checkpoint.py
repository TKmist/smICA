import inspect
import dearpygui.dearpygui as dpg
import numpy as np
class _init_varaibles:
    def __init__(self):
        
        self.init_size_ratio = {'width':1,
                          'height':1}
        self.init_top_indent = 24+11
        self.init_bottom_indent = 11
        self.init_left_indent = 11
        self.init_right_indent = 11
        self.init_internal_indent = 11
        self.init_group_spacer = 2
        self.init_font_size  = 20
        self.VIEWPORT_prop = {'width':1523,
                              'height':940+2*11,
                              'pos':(0,0)
                                }
        self.last_directory = 'samples'
        
    
class inits:
    def __init__(self,
                 size_ratio,
                 left_indent,
                 internal_indent,
                 right_indent,
                 bottom_indent,
                 top_indent,
                 group_spacer,
                 font_size,
                 last_directory,
                ):
        self.size_ratio=size_ratio
        self.top_indent = int(top_indent*self.size_ratio['width'])
        self.bottom_indent  = int(bottom_indent*self.size_ratio['width'])
        self.left_indent  = int(left_indent*self.size_ratio['width'])
        self.right_indent  = int(right_indent*self.size_ratio['width'])
        self.internal_indent  = int(internal_indent*self.size_ratio['width'])
        self.fnt_ratio = (self.size_ratio['width']+self.size_ratio['height'])/2
        self.font_size  = int(np.round(font_size*self.fnt_ratio,0))
        self.group_spacer  = int(group_spacer*self.size_ratio['width'])
        
        
        self.items=[]
        self.last_directory = last_directory
        self.directory = ''


        self.file_window = {'name':'file_window',
                            'width':int(340*self.size_ratio['width']),
                            'height':dpg.get_viewport_height()-4*self.bottom_indent,
                            'pos':(self.left_indent,self.top_indent)
                            }

        self.image_window_1 = {'name':'image_window_1',
                            'width':(dpg.get_viewport_width()-self.file_window['width']-self.file_window['pos'][0]-2*self.internal_indent-self.right_indent)/2,
                            'height':(dpg.get_viewport_width()-self.file_window['width']-self.file_window['pos'][0]-2*self.internal_indent-self.right_indent)/2,
                            'pos':(self.left_indent+self.file_window['width']+self.internal_indent,
                                   self.top_indent)
                            }

        self.image_window_2 = {'name':'image_window_2',
                            'width':self.image_window_1['width'],
                            'height':self.image_window_1['height'],
                            'pos':(self.image_window_1['pos'][0]+self.image_window_1['width']+self.internal_indent,
                                   self.top_indent)
                            }
        
class _basicF:      
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

    def _hsv_to_rgb(self,h, s, v):
        '''Funtion converts HSV color notation to the RGB values'''
        if s == 0.0: return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
        if i == 0: return (255*v, 255*t, 255*p)
        if i == 1: return (255*q, 255*v, 255*p)
        if i == 2: return (255*p, 255*v, 255*t)
        if i == 3: return (255*p, 255*q, 255*v)
        if i == 4: return (255*t, 255*p, 255*v)
        if i == 5: return (255*v, 255*p, 255*q)
        
        
        
class _init_Menu:
    
    
    def __init__(self,VERSION):
        self.VERSION = VERSION
        
        
    
    
    
    
    
    def mount_main_Menu_bar(self):
    
        with dpg.viewport_menu_bar(tag="vieport's_menubar"):
            with dpg.menu(label="File",tag='menu_file_dropout'):
                dpg.add_menu_item(label="Open PTU folder",callback=None,tag='menu_item_open_ptu')
                dpg.add_menu_item(label="Open png folder",callback=None,tag='menu_item_open_p[ng')
                dpg.add_menu_item(label="Open csv folder",callback=None,tag='menu_item_open_csv')
                dpg.add_menu_item(label="Exit",callback=lambda: dpg.stop_dearpygui(),tag='menu_item_exit')
            

    