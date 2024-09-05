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
warnings.filterwarnings('ignore')

logfile=os.path.join('Logs','log.log')

def log_it(text_to_log,mode):
    global logfile
    logf = open(logfile, mode)
    
    logf.write(text_to_log+'\n')
    
    logf.close()
    
    
def _trace(f, *args, **kwrds):
    
    
    
    
    
    log_it('\t\tExecuting function: '+f.__name__,'a')
    
    
    
    
    
    
    
    
    
    return f(*args, **kwrds)





log_it("STARTED on "+str(datetime.datetime.now()),'w') 


print(line)
print(line,end='\n\n')
print(Licence)
print('\n')
print('VERSION = ',VERSION,end='\n')
print(line)
print(line,end='\n\n')


execfile(os.path.join('dep','Modules.py'))           


execfile(os.path.join('dep','Functions.py'))          
inf_w,inf_h=pyautogui.size()[0],pyautogui.size()[1]   




dpg.create_context()                        
execfile(os.path.join('dep','init.py'))               

execfile(os.path.join('dep','Themes.py'))             
execfile(os.path.join('dep','Fonts.py'))              

execfile(os.path.join('dep','Handlers.py'))           
execfile(os.path.join('dep','Texture_registry.py'))   











dpg.create_viewport(title='PTU2CONC   ver:'+VERSION,width=init_widths['VIEWPORT'], height=init_heights['VIEWPORT'],x_pos=10,y_pos  =10)    



execfile(os.path.join('dep','Menu_bar.py'))           





dpg.setup_dearpygui()


execfile(os.path.join('dep','Dialogs.py'))                     

execfile(os.path.join('dep','Files_window.py'))
execfile(os.path.join('dep','PTU_DATA.py'))
execfile(os.path.join('dep','Image_window.py'))
execfile(os.path.join('dep','FCS_window.py'))
execfile(os.path.join('dep','histograms_window.py'))
execfile(os.path.join('dep','Results_window.py'))












VP_w = dpg.get_viewport_width() -dif_vp0_width           
VP_h = dpg.get_viewport_height()           
dpg.set_viewport_resize_callback(callback_auto_adjust)
dpg.maximize_viewport()       



# print(inf_w,inf_h,VP_w,VP_h)

# dpg.set_viewport_resize_callback(None)















    

dpg.show_viewport()
dpg.set_viewport_width(init_widths['VIEWPORT'])
dpg.set_viewport_height(init_heights['VIEWPORT'])
dpg.start_dearpygui()
# dpg.set_viewport_resizable(False)
print('line:164',dpg.get_viewport_width(),dpg.get_viewport_height())



dpg.destroy_context



log_it('FINISHED on '+str(datetime.datetime.now()),'a')
