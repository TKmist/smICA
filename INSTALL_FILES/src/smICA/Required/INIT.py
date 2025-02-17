import os
import numpy as np
from numpy import log10#, sqrt, exp, log, pi
import dearpygui.dearpygui as dpg
import json
import webbrowser
import inspect

class _basicF:
    
    
    def __init__(self):
        pass
    
    
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

    def add_font_to_registry(self,font_size):
        font_path = os.path.join('res','Fonts','DejaVuSansCondensed.ttf')
        with dpg.font_registry(tag='Font_registry'):
            '''Add a font registry.'''
            
            with dpg.font(font_path, font_size,tag='DejaVu') as font_18:
                dpg.add_font_range(0x0300, 0x03ff)
                dpg.add_font_range(0x0200, 0x02ff)
                dpg.add_font_range(0x2080, 0x209C)
                dpg.add_font_range(0x2190, 0x2193)
                default_font = font_18
            dpg.bind_font(default_font)
        

    def remove_font_from_registry(self):
        font = 'DejaVu'
        dpg.delete_item(font)
        dpg.delete_item('Font_registry')
        
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

    def search_for_methods(self):
        path = 'Modes'
        methods = os.listdir(path)
        ind = []
        methods = [os.path.join(path,ad) for ad in methods if os.path.isdir(os.path.join(path,ad))]
        for i, method in enumerate(methods):
            met_files = os.listdir(method)
            met_files = [f for f in met_files if f.endswith('_config.json')]
            if len(met_files) == 1:
                ind.append(i)
        methods = list(np.array(methods)[ind])
        return methods
    def ifso(self,f):
            if type(f)  == bytes:
                f = f.decode("utf-8")
            else:
                pass
            return f
    
    def path_to_method_anal_menu_item(self,method_dir):
        met_files = os.listdir(method_dir)
        
        
            
            
        
        met_files = [ self.ifso(f) for f in met_files]
        # print(met_files)
        met_files = [f for f in met_files if f.endswith('_config.json')]
        # print(met_files,met_files[0],type(met_files[0]))
        met_file = met_files[0]
        path = os.path.join(method_dir,met_file)

        with open(path) as json_settings:
            method_tree = json.load(json_settings)

        return method_tree['ANAL_MENU_ITEM']

    def method_config_dict(self,method_dir):
        met_files = os.listdir(method_dir)
        
            
            
        
        met_files = [ self.ifso(f) for f in met_files]
        met_files = [str(f) for f in met_files if str(f).endswith('_config.json')]
        # print(met_files)
        met_file = met_files[0]
        # print('met_file',met_file)
        path = os.path.join(method_dir,met_file)
        # print('path',path)
        with open(path) as json_settings:
            method_tree = json.load(json_settings)

        return method_tree
    
    
    def path_to_method_anal_layout(self,method_dir):
        # print('method_dir',method_dir)
        met_files = os.listdir(method_dir)
        # print(met_files)
        
            
            
        
        met_files = [ self.ifso(f) for f in met_files]
        # print(met_files,met_files[0],type(met_files[0]))
        met_files = [f for f in met_files if f.endswith('_config.json')]
        # print(met_files)
        # print(met_files,met_files[0],type(met_files[0]))
        met_file = met_files[0]
        # print('met_file',met_file)
        path = os.path.join(method_dir,met_file)
        # print('path',path)
        with open(path) as json_settings:
            method_tree = json.load(json_settings)

        return method_tree['LAYOUT']
    
    
    def split_path_into_folders(self,path):
        folders = []
        while True:
            path, folder = os.path.split(path)
            if folder != "":
                folders.append(folder)
            else:
                if path != "":
                    folders.append(path)
                break
        folders.reverse()
        return folders
    
    
    
    
    
    
    
        
    
    
##############################################################################    
class _init_varaibles:
    
    def __init__(self):
        
        self.init_size_ratio = {'width':1,
                          'height':1}
        self.init_top_indent = 24+11
        if os.name == 'posix':

            self.init_bottom_indent = 11
            self.init_right_indent = 11
        else:
            self.init_bottom_indent = 5*11
            self.init_right_indent = int(np.round(2.5*11))

        self.init_left_indent = 11
        
        self.init_internal_indent = 11
        self.init_group_spacer = 2
        self.init_font_size = 18
        self.VIEWPORT_prop = {'width':1585,
                              'height':950+2*11,
                              'pos':(0,0)
                                }
        self.mounted_method = None
        #self.icopath()
        
    def icopath(self):
        osname = os.name

        if osname == 'posix':

            ico_path=os.path.join('res','icons','smICA.png')
            
        else:
            ico_path=os.path.join('res','icons','smICA.ico')
            #self.init_bottom_indent = 2*11
            #self.init_right_indent = 2*11
        return ico_path

class _init_Menu:
    def __init__(self,VERSION):
        self.VERSION = VERSION

    
    def callback_license(self,sender,app_data):
        if not 'License_title' in dpg.get_aliases():
            with dpg.window(tag='License_win',width=dpg.get_viewport_width()/2,
                            height=dpg.get_viewport_height()/2,
                                pos = (dpg.get_viewport_width()/4,
                                       dpg.get_viewport_height()/4),
                                menubar=False,
                                autosize=False,
                                no_resize=True,
                                no_title_bar=False,
                                no_move=True,

                                modal=True,

                           show=True):
                dpg.add_button(tag='License_title',width=dpg.get_viewport_width()/2,label='LICENSE')

                dpg.bind_item_theme('License_title', 'transparent_theme')
                with open('../LICENSE', 'r') as file:
                    License = file.read()
                dpg.add_text(label='License',
                             tag='license_text',
                             default_value = License,
                             wrap = int(0.95*(dpg.get_viewport_width()/2)))
        else:
            dpg.delete_item('license_text')
            dpg.delete_item('License_title')
            dpg.delete_item('License_win')
            with dpg.window(tag='License_win',width=dpg.get_viewport_width()/2,
                            height=dpg.get_viewport_height()/2,
                                pos = (dpg.get_viewport_width()/4,
                                       dpg.get_viewport_height()/4),
                                menubar=False,
                                autosize=False,
                                no_resize=True,
                                no_title_bar=False,
                                no_move=True,

                                modal=True,

                           show=True):
                dpg.add_button(tag='License_title',width=dpg.get_viewport_width()/2,label='LICENSE')

                dpg.bind_item_theme('License_title', 'transparent_theme')
                with open('LICENSE', 'r') as file:
                    License = file.read()
                dpg.add_text(label='License',
                             tag='license_text',
                             default_value = License,
                             wrap = int(0.95*(dpg.get_viewport_width()/2)))

    
    def mount_main_Menu_bar(self):
    
        with dpg.viewport_menu_bar(tag="vieport's_menubar"):
            with dpg.menu(label="File",tag='menu_file_dropout'):
                dpg.add_menu_item(label="Exit",callback=lambda: dpg.stop_dearpygui(),tag='menu_item_exit')
            with dpg.menu(label="Mode",tag='menu_analysis_method_dropout'):
                pass
            # with dpg.menu(label="Settings",tag='menu_settings_dropout'):
                
            #     dpg.add_menu_item(label="Full Screen (F11)",tag='fullscreenclick',callback=self.callback_full_screen)

            with dpg.menu(label="About",tag='menu_about_dropout'):
                # dpg.add_menu_item(label="Help (F1)",tag='helpclick',callback=self.callback_help)
                dpg.add_menu_item(label='License',callback = self.callback_license)
                dpg.add_menu_item(label='Version: '+self.VERSION,enabled=False)




class _common_VARIABLES:
    def __init__(self):
        self.windows = []
        self.items = []
        self.last_directory = 'samples'
        self.directory = ''