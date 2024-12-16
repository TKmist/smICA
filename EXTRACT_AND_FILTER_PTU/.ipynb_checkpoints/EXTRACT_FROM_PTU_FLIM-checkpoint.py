with open('../LICENSE', 'r') as file:
    Licence = file.read()
with open('../VERSION', 'r') as file:
    VERSION = file.read()
line='=============================================================================='
import os
import datetime

from decorator import decorator 
logfile=os.path.join('Logs','log.log')
def execfile(filepath, globals=globals(), locals=None):
    '''Import module allowing execution of external python scripts as part of the main code. This part of the code is based on the following source: https://stackoverflow.com/a/41658338 '''
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)
        
def log_it(text_to_log,mode):
    global logfile
    logf = open(logfile, mode)
    
    logf.write(text_to_log+'\n')
    
    logf.close()
    
    
def _trace(f, *args, **kwrds):
    
    
    
    
    
    log_it('Executing function: '+f.__name__,'a')
    
    
    
    
    
    
    
    
    
    return f(*args, **kwrds)

def trace(f):
    return decorator(_trace, f)


log_it("STARTED on "+str(datetime.datetime.now()),'w')  

print(line)
print(line,end='\n\n')
print(Licence)
print('\n')
print('VERSION = ',VERSION,end='\n')
print(line)
print(line,end='\n\n')
import dearpygui.dearpygui as dpg




from dep.readPTU_FLIM import PTUreader




execfile(os.path.join('dep','Modules.py'))           

execfile(os.path.join('dep','Functions.py'))           
log_it('Functions loaded','a') 







dpg.create_context()                        
execfile(os.path.join('dep','init.py'))
log_it('Init parameters loaded','a')              

execfile(os.path.join('dep','Themes.py'))             
log_it('Themes loaded','a')
execfile(os.path.join('dep','Fonts.py'))              
log_it('Fonts loaded','a')















dpg.create_viewport(title='LifeTime filtering',
                    width=init_widths['VIEWPORT'],
                    height=init_heights['VIEWPORT'])    


execfile(os.path.join('dep','Menu_bar.py'))           
log_it('Menu bar created','a')




dpg.setup_dearpygui()
dpg.show_viewport(maximized=False)

execfile(os.path.join('dep','Dialogs.py'))     
log_it('Dialogs created','a')



execfile(os.path.join('dep','Plot_windows.py'))


execfile(os.path.join('dep','BG_removal_window.py'))





























    

dpg.start_dearpygui()




dpg.destroy_context

log_it('FINISHED on '+str(datetime.datetime.now()),'a')



