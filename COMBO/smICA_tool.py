with open('../LICENSE', 'r') as file:
    Licence = file.read()
with open('../VERSION', 'r') as file:
    VERSION = file.read()
line='=============================================================================='

def execfile(filepath, globals=globals(), locals=None):
    '''Import module allowing execution of external python scripts as part of the main code. This part of the code is based on the following source: https://stackoverflow.com/a/41658338 '''
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)



import platform
import os
if platform.system().upper() == "LINUX":
    os.environ["__GLVND_DISALLOW_PATCHING"] = "1"
from decorator import decorator 
import dearpygui.dearpygui as dpg
# import os
import datetime
import numpy as np
import warnings
import Required.INIT as inits
warnings.filterwarnings('ignore')
def callback_none():
    pass

basf = inits._basicF()

inV=inits._init_varaibles()
def basic_resizer(sender,app_data):
    ratio = {'width': np.round(app_data[0]/inV.VIEWPORT_prop['width'],4),
             'height': np.round(app_data[1]/inV.VIEWPORT_prop['height'],4)}

    inV.init_size_ratio = ratio
    inV.initial_window = {'name':'initial_window',
                            'width':int(ratio['width']*450),
                            'height':int(ratio['height']*250),
                            'pos':(int(app_data[0]/2-int(ratio['width']*450)/2),
                                   int(app_data[1]/2-int(ratio['height']*250)/2))
                            }
    inV.EXTRACT_FROM_PTU_INIT_BUTTON = {'name':'EXTRACT_FROM_PTU_INIT_BUTTON',
                                             'width':-1,
                                             'height':int(inV.initial_window['height']/2.2),
                                             }
    inV.Phot_2_Conc_INIT_BUTTON = {'name':'Phot_2_Conc_INIT_BUTTON',
                                             'width':-1,
                                             'height':int(inV.initial_window['height']/2.2),
                                             }
    items = ['initial_window','EXTRACT_FROM_PTU_INIT_BUTTON','Phot_2_Conc_INIT_BUTTON']
    
    for item in items:
        props =eval('inV.'+item)
        try:
            dpg.configure_item(item,width=props['width'])
        except:
            pass
        try:
            dpg.configure_item(item,height=props['height'])
        except:
            pass
        try:
            dpg.configure_item(item,pos=props['pos'])
        except:
            pass
    
viewport = inV.VIEWPORT_prop
menu = inits._init_Menu(VERSION=VERSION)

lprint=basf.lnprint







print(line)
print(line,end='\n\n')
print(Licence)
print('\n')
print('VERSION = ',VERSION,end='\n')
print(line)
print(line,end='\n\n')


execfile('Required/Required.py')           # Import required python packages

# inf_w,inf_h=pyautogui.size()[0],pyautogui.size()[1]
inf_w, inf_h = get_monitors()[0].width, get_monitors()[0].height

dpg.create_context()
execfile('Required/Themes.py')             # Load the themes definitions.
execfile('Required/Fonts.py') 
# execfile('dep/Handlers.py') 


dpg.create_viewport(title='smICA',small_icon = inV.icopath(),width=viewport['width'], height=viewport['height'],x_pos=viewport['pos'][0],y_pos  =viewport['pos'][1]) 
dpg.setup_dearpygui()
dpg.show_viewport()
globalITEMS = inits._common_VARIABLES()
  

VP_w = dpg.get_viewport_width()            # get initial width of the viewport
VP_h = dpg.get_viewport_height()           # get initial height of the viewport
# dpg.maximize_viewport() 
menu.mount_main_Menu_bar()

inV.METHODS = basf.search_for_methods()


for method in inV.METHODS:
    lprint(method)
    path =os.path.join(method,basf.path_to_method_anal_menu_item(method))
    # lprint(path)
    execfile(path)

dpg.set_viewport_resize_callback(basic_resizer)
with dpg.window(tag = 'initial_window',
                        width = inV.initial_window['width'],
                        height = inV.initial_window['height'],
                        pos = inV.initial_window['pos'],
                        menubar=False,
                        autosize=False,
                        no_title_bar=True,
                        no_move=True,
                        no_resize=True,
                        no_background=True,
                        modal=False,
                        show=True
                       ):
    dpg.add_button(label="EXTRACT from PTU",
               callback='',
               width = inV.EXTRACT_FROM_PTU_INIT_BUTTON['width'],
               height = inV.EXTRACT_FROM_PTU_INIT_BUTTON['height'],
               tag='EXTRACT_FROM_PTU_INIT_BUTTON',
               show=True,enabled=True
              )
    dpg.bind_item_theme('EXTRACT_FROM_PTU_INIT_BUTTON', 'fit_button_theme')
    dpg.add_button(label="Phot 2 Conc",
               callback='',
               width = inV.Phot_2_Conc_INIT_BUTTON['width'],
               height = inV.Phot_2_Conc_INIT_BUTTON['height'],
               tag='Phot_2_Conc_INIT_BUTTON',
               show=True,enabled=True
              )
    dpg.bind_item_theme('Phot_2_Conc_INIT_BUTTON', 'fit_button_theme')


# dpg.add_menu_item(label="Phot2Conc",
#                           parent ='menu_analysis_method_dropout' ,
#                           tag='Analysis_submenu_item_Phot2conc',
#                           callback=P2C_manu_F.callback_PHOT2CONC_menu)
# dpg.add_menu_item(label="Extract from PTU",
#                           parent ='menu_analysis_method_dropout' ,
#                           tag='Analysis_submenu_item_PhotExtract',
#                           callback=PE_manu_F.callback_PHOTEXTR_menu)

# print(P2C_manu_F,PE_manu_F)
# print(vars(menu))




dpg.start_dearpygui()
dpg.destroy_context()