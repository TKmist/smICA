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

import dearpygui.dearpygui as dpg
# import os
import datetime

from dep.INIT import inits, _init_Menu


init = inits()

menu = _init_Menu(VERSION)


    
lprint=init.lnprint





print(line)
print(line,end='\n\n')
print(Licence)
print('\n')
print('VERSION = ',VERSION,end='\n')
print(line)
print(line,end='\n\n')


execfile(os.path.join('dep','Required.py'))           


# execfile(os.path.join('dep','Functions.py'))          
# inf_w,inf_h=pyautogui.size()[0],pyautogui.size()[1]   




dpg.create_context()                        
# execfile(os.path.join('dep','init.py'))               

# execfile(os.path.join('dep','Themes.py'))             
execfile(os.path.join('dep','Fonts.py'))              

# execfile(os.path.join('dep','Handlers.py'))           
# execfile(os.path.join('dep','Texture_registry.py'))   







lprint('1')

lprint(init.size_pos['VIEWPORT'])

dpg.create_viewport(title='AutoROI   ver:'+VERSION,
                    width=init.size_pos['VIEWPORT']['width'], 
                    height=init.size_pos['VIEWPORT']['height'],
                    x_pos=init.size_pos['VIEWPORT']['pos'][0],
                    y_pos  =init.size_pos['VIEWPORT']['pos'][1])    




lprint('2')
# execfile(os.path.join('dep','Menu_bar.py'))           





dpg.setup_dearpygui()
dpg.show_viewport()
lprint('3')
menu.mount_main_Menu_bar()

# execfile(os.path.join('dep','Dialogs.py'))                     

# execfile(os.path.join('dep','Files_window.py'))
# execfile(os.path.join('dep','PTU_DATA.py'))
# execfile(os.path.join('dep','Image_window.py'))
# execfile(os.path.join('dep','FCS_window.py'))
# execfile(os.path.join('dep','histograms_window.py'))
# execfile(os.path.join('dep','Results_window.py'))












# VP_w = dpg.get_viewport_width() -dif_vp0_width           
# VP_h = dpg.get_viewport_height()           
# dpg.set_viewport_resize_callback(callback_auto_adjust)
# dpg.maximize_viewport()       



# print(inf_w,inf_h,VP_w,VP_h)

# dpg.set_viewport_resize_callback(None)











lprint('4')



    


# dpg.set_viewport_width(init_widths['VIEWPORT'])
# dpg.set_viewport_height(init_heights['VIEWPORT'])
dpg.start_dearpygui()
# dpg.set_viewport_resizable(False)




dpg.destroy_context()



# log_it('FINISHED on '+str(datetime.datetime.now()),'a')
