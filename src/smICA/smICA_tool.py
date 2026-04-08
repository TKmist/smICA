'''
This file is part of the smICA repository that is distributed under the MIT license; see below.

This is the main script.

############################################################################

MIT License

Copyright (c) 2026 Tomasz Kalwarczyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''
import platform
import os
from decorator import decorator 
import dearpygui.dearpygui as dpg
import datetime
import numpy as np
import warnings
import Required.INIT as inits
from screeninfo import get_monitors


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

if platform.system().upper() == "LINUX":
    os.environ["__GLVND_DISALLOW_PATCHING"] = "1"

warnings.filterwarnings('ignore')
def callback_none():
    pass

basf = inits._basicF()
updt = inits._updater(basf._hsv_to_rgb,VERSION)

inV=inits._init_varaibles()
    
viewport = inV.VIEWPORT_prop
menu = inits._init_Menu(updt.updater_state,VERSION=VERSION)

lprint=basf.lnprint

print(line)
print(line,end='\n\n')
print(Licence)
print('\n')
print('VERSION = ',VERSION,end='\n')
print(line)
print(line,end='\n\n')

inf_w, inf_h = get_monitors()[0].width, get_monitors()[0].height

dpg.create_context()
execfile('Required/Themes.py')             # Load the themes definitions.
execfile('Required/Fonts.py') 
execfile('Required/Handlers.py')


dpg.create_viewport(title='smICA',small_icon = inV.icopath(),width=viewport['width'], height=viewport['height'],x_pos=viewport['pos'][0],y_pos  =viewport['pos'][1]) 
dpg.setup_dearpygui()
dpg.show_viewport()
globalITEMS = inits._common_VARIABLES()
  

VP_w = dpg.get_viewport_width()            # get initial width of the viewport
VP_h = dpg.get_viewport_height()           # get initial height of the viewport
 
menu.mount_main_Menu_bar()
rwroi = inits.rewrite_roi(viewport)
try:
   
    updt.run_updater()
    print('updt.updater_state =', updt.updater_state)
    
except:
    basf.some_fail()

inV.METHODS = basf.search_for_methods()

for method in inV.METHODS:

    path =os.path.join(method,basf.path_to_method_anal_menu_item(method))
    execfile(path)
    
basf.P2C_manu_F = P2C_manu_F
basf.PE_manu_F = PE_manu_F
basf.viewport = viewport
dpg.set_viewport_resize_callback(basf.basic_resizer)
basf.mount_inint_buttons()

dpg.start_dearpygui()
dpg.destroy_context()
