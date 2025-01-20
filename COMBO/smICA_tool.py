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
import warnings
import Required.INIT as inits
warnings.filterwarnings('ignore')
def callback_none():
    pass

basf = inits._basicF()

inV=inits._init_varaibles()
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


dpg.create_viewport(title='smICA',width=viewport['width'], height=viewport['height'],x_pos=viewport['pos'][0],y_pos  =viewport['pos'][1]) 
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
    lprint(path)
    execfile(path)

# print(vars(menu))




dpg.start_dearpygui()
dpg.destroy_context()