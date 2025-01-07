import numpy as np
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


def _resizer(sender,app_data):
    import numpy as np
    
    init_resizable_items = []
    # cmn_resizable_items = []
    obj_var = [eval('init.'+str(m)) for m in vars(init)]
    for m in obj_var:
        if type(m) == dict:
            if 'name' in m.keys():
                init_resizable_items.append(m['name'])
        else:
            pass
    # obj_var = [eval('method_cmn.'+str(m)) for m in vars(method_cmn)]
    # for m in obj_var:
    #     if type(m) == dict:
    #         if 'name' in m.keys():
    #             cmn_resizable_items.append(m['name'])
    #     else:
    #         pass    
        
        
    
    ratio = {'width': np.round(app_data[0]/inV.VIEWPORT_prop['width'],4),
             'height': np.round(app_data[1]/inV.VIEWPORT_prop['height'],4)} 
    # print(ratio)
    # inV.init_size_ratio = ratio
    fnt_ratio = (ratio['width']+ratio['height'])/2
    new_font_size=int(np.round(inV.init_font_size*fnt_ratio,0))
    # print('==============================================================')
    # print(method_init.__init__.__code__.co_varnames)
    
    temp_inits = init.__init__.__code__.co_varnames
    temp_inits = [v for v in temp_inits if v != 'self']
    temp_inits = [v for v in temp_inits if v != 'size_ratio']
    temp_inits = [v for v in temp_inits if v != 'font_size']
    temp_inits = [v for v in temp_inits if v != 'callbacks']
    
    temp_inits = [v for v in temp_inits if v != 'tex_1_name']
    temp_inits = [v for v in temp_inits if v != 'tex_2_name']
    
    
    temp_inits_values  = {}
    for v in temp_inits:
        print(v)
        temp_inits_values[v] = eval('init.'+v)
    last_dir = callback.last_directory
    init.__init__(ratio,
        # inV.init_size_ratio,
                         inV.init_left_indent,
                         inV.init_internal_indent,
                         inV.init_right_indent,
                         inV.init_bottom_indent,
                         inV.init_top_indent,
                         inV.init_group_spacer,
                          inV.init_font_size,
                         last_dir,
                         inV.tex_1_name,
                         inV.tex_2_name)
    ot = oth(basf,inV)
    for item in init_resizable_items:
        # print(item)
        props =eval('init.'+item) 
        if 'width' in props.keys():
            dpg.configure_item(item,width=props['width'])
        if 'height' in props.keys():
            dpg.configure_item(item,height=props['height'])
        if 'pos' in props.keys():
            dpg.configure_item(item,pos=props['pos'])
    dpg.delete_item('DejaVu')
    dpg.delete_item('Font_registry')
    # lprint(inV.init_font_size,init.font_size)
    add_font_to_registry(init.font_size)
    w = int(np.round(dpg.get_item_width('image_window_1')))-15*ratio['width']
    h = w
    dpg_image_1 = ot.update_texture(callback.Current_image_1)
    if init.tex_1_name in dpg.get_aliases():
        dpg.delete_item(init.tex_1_name)
        
        dpg.remove_alias(init.tex_1_name)
        # print('line 2639','img1_passed0')
        dpg.delete_item('texture_CH_1')
        # print('line 2641','img1_passed')
        # if 'new' in init.tex_1_name:
        #     new = 'texture_tag_chan_1-new_'+str(int(tex_1_name.split('-')[1].split('_')[1])+1)
        #     init.tex_1_name =new
            
            
            
        # else:
            
        #     init.tex_1_name = 'texture_tag_chan_1-new_1'
        
        dpg.add_dynamic_texture(width=w,
                        height=h,
                        default_value=dpg_image_1,
                        tag=init.tex_1_name,
                        parent = 'texture_reg')
        
        dpg.add_image(init.tex_1_name,parent = 'image_window_1'
                              ,uv_min=(0,0),uv_max=(1,1),tag = 'texture_CH_1',before='IMAGE_CH1_top_sep_2')
        
    dpg_image_2 = ot.update_texture(callback.Current_image_2)
    if init.tex_2_name in dpg.get_aliases():
        dpg.delete_item(init.tex_2_name)
        
        dpg.remove_alias(init.tex_2_name)
        # print('line 2639','img1_passed0')
        dpg.delete_item('texture_CH_2')
        # print('line 2641','img1_passed')
        # if 'new' in init.tex_2_name:
        #     new = 'texture_tag_chan_2-new_'+str(int(tex_1_name.split('-')[1].split('_')[1])+1)
        #     init.tex_2_name =new
            
            
            
        # else:
            
        #     init.tex_2_name = 'texture_tag_chan_2-new_1'
        
        dpg.add_dynamic_texture(width=w,
                        height=h,
                        default_value=dpg_image_2,
                        tag=init.tex_2_name,
                        parent = 'texture_reg')
        
        dpg.add_image(init.tex_2_name,parent = 'image_window_2'
                              ,uv_min=(0,0),uv_max=(1,1),tag = 'texture_CH_2',before='IMAGE_CH2_top_sep_2')

    


import platform
import os
if platform.system().upper() == "LINUX":
    os.environ["__GLVND_DISALLOW_PATCHING"] = "1"

import dearpygui.dearpygui as dpg
# import os
import datetime

from dep.INIT import inits, _init_Menu,_init_varaibles,_basicF,callbacks,oth



inV=_init_varaibles()
viewport = inV.VIEWPORT_prop

basf = _basicF()

menu = _init_Menu(VERSION,inV)

# globalITEMS = init.items

    
lprint=basf.lnprint
callback = callbacks(inV.last_directory,basf,inV)




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

execfile(os.path.join('dep','Themes.py'))             
execfile(os.path.join('dep','Fonts.py'))              

# execfile(os.path.join('dep','Handlers.py'))           
 








dpg.create_viewport(title='AutoROI   ver:'+VERSION,
                    width=viewport['width'],
                    height=viewport['height'],
                    x_pos=viewport['pos'][0],
                    y_pos  =viewport['pos'][1])    

dpg.set_viewport_resize_callback(_resizer)
# lprint(dpg.get_viewport_height())
   


# execfile(os.path.join('dep','Menu_bar.py'))           





dpg.setup_dearpygui()
dpg.show_viewport()

menu.mount_main_Menu_bar()
init = inits(inV.init_size_ratio,
                 inV.init_left_indent,
                 inV.init_internal_indent,
                 inV.init_right_indent,
                 inV.init_bottom_indent,
                 inV.init_top_indent,
                 inV.init_group_spacer,
                 inV.init_font_size,
                 callback,
                 inV.tex_1_name,
                 inV.tex_2_name,
            )

execfile(os.path.join('dep','Texture_registry.py'))  
execfile(os.path.join('dep','Layout.py'))
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











# lprint('4')



    


# dpg.set_viewport_width(init_widths['VIEWPORT'])
# dpg.set_viewport_height(init_heights['VIEWPORT'])
dpg.start_dearpygui()
# dpg.set_viewport_resizable(False)




dpg.destroy_context()



# log_it('FINISHED on '+str(datetime.datetime.now()),'a')
