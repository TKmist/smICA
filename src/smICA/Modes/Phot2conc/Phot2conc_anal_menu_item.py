'''
This file is part of the smICA repository that is distributed under the MIT license; see below.


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


import dearpygui.dearpygui as dpg
    
class _PHOT2CONC_mounting_functions:
    
    def unmount_me(self,fcs_items):
        
        for item in reversed(fcs_items):
            dpg.delete_item(item)

        dpg.delete_item('texture_reg')
        dpg.set_viewport_resize_callback(callback_none)
        self.is_mounted = False
        inV.mounted_method = None        
    def mount_me(self):
        dpg.add_menu_item(label="Open PTU directory",
                  tag='Open_PTU_menu_item',
                  parent = 'menu_file_dropout',
                  before = 'menu_item_exit',
                         )
        dpg.add_menu_item(label="Open ROI directory",
                  tag='Open_ROI_menu_item',
                  parent = 'menu_file_dropout',
                  before = 'menu_item_exit',
                         )
        dpg.add_separator(tag ='File_menu_sep_1',show=True,
                  parent = 'menu_file_dropout',
                  before = 'menu_item_exit')
        dpg.add_menu_item(label="Reset results",
                  tag='Reset_results_menu_item',
                  parent = 'menu_file_dropout',
                  before = 'menu_item_exit',
                         )
            
        globalITEMS.windows.extend(['Open_PTU_menu_item',
                                    'Open_ROI_menu_item',
                                    'File_menu_sep_1',
                                    'Reset_results_menu_item'
                                   ])

####################################################################
############ end of _PHOT2CONC_mounting_functions class ############
####################################################################        
        
class _PHOT2CONC_menu_functions:
    
    def __init__(self):
        self.is_mounted = False
        self.mnt = _PHOT2CONC_mounting_functions()
        
    
    def unmnt_evthn(self,items,MTHD_conf):
        for item in reversed(items):
            dpg.delete_item(item)
        
        
        exec(MTHD_conf['menu_class_func']+'.is_mounted = False')
        dpg.set_viewport_resize_callback(callback_none)
        self.is_mounted = False
        inV.mounted_method = None
        print(globalITEMS.last_directory)
        globalITEMS.windows=[]
        
    def callback_PHOT2CONC_menu(self):

        if self.is_mounted:
            self.mnt.unmount_me(globalITEMS.windows)
            globalITEMS.windows=[]
        else:
            if inV.mounted_method != None:
                
                othm_conf = basf.method_config_dict(inV.mounted_method)
                self.unmnt_evthn(globalITEMS.windows,othm_conf)
            else:
                pass
                
        self.mnt.mount_me()
        
        self.is_mounted = True
        inV.mounted_method = 'Modes/Phot2conc'
        path_to_layout = os.path.join('Modes/Phot2conc',basf.path_to_method_anal_layout('Modes/Phot2conc'))
        execfile(path_to_layout)
        mode_cmn.define_file_menu_callbacks()
        
####################################################################
############## end of _PHOT2CONC_menu_functions class ##############
####################################################################
        
P2C_manu_F = _PHOT2CONC_menu_functions()