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


import dearpygui.dearpygui as dpg
import os
import pandas as pd
import numpy as np

print(line)
print(line,end='\n\n')
print(Licence)
print('\n')
print('VERSION = ',VERSION,end='\n')
print(line)
print(line,end='\n\n')





execfile(os.path.join('dep','Functions.py'))          





dpg.create_context()                        
execfile(os.path.join('dep','init.py'))               

execfile(os.path.join('dep','Themes.py'))             
execfile(os.path.join('dep','Fonts.py'))              














dpg.create_viewport(title='Rewrite roi GUI' ,
                    width=800,
                    height=400,
                    x_pos=0,
                    y_pos  =0,
                    resizable=True)    


execfile(os.path.join('dep','Menu_bar_functions.py')) 
execfile(os.path.join('dep','Menu_bar.py'))           





dpg.setup_dearpygui()




        
        
     

        
        
  
    
    
dpg.show_viewport(maximized=False)    


with dpg.window(label='',
                pos = (init_left_indent,init_top_indent),
                no_move=False,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='file_window',
                autosize=True,
                show=True
               ):
    dpg.add_button(label='Open ROI folder',tag='open_roi_folder',width=600,callback=lambda: dpg.show_item('Source_file_dialog'))
    dpg.add_text('',tag='tag_source_path',wrap=600)
    with dpg.group(tag='resolution_group', horizontal=True):
        dpg.add_input_text(tag='add_text_width',width=288)
        dpg.add_text('x',tag='tag_x')
        dpg.add_input_text(tag='add_text_height',width=289)
    dpg.add_button(label='Target ROI folder',tag='target_roi_folder',width=600,callback=lambda: dpg.show_item('Target_file_dialog'))
    dpg.add_text('',tag='tag_target_path',wrap=600)
   
    dpg.add_listbox(items=[],
                               width=600,
    
                               tag='file_box',

                              )
    
    dpg.add_button(label='Proceded',tag='Run_script',width=600,callback=callback_proceed)























execfile(os.path.join('dep','Dialogs.py'))                     






























    

dpg.start_dearpygui()




dpg.destroy_context

