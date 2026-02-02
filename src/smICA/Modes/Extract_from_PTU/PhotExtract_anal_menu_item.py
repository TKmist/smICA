'''
This file is part of the smICA repository that is distributed under the MIT license; see below.


############################################################################

MIT License

Copyright (c) 2024 Tomasz Kalwarczyk

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
    
class _PHOTEXTR_mounting_functions:
    
    def unmount_me(self, mounted_items):
        for item in reversed(mounted_items):
            dpg.delete_item(item)

        dpg.set_viewport_resize_callback(callback_none)
        self.is_mounted = False
        inV.mounted_method = None


    def mount_me(self):
        dpg.add_menu_item(
            label="Open PTU directory",
            tag="Open_PTU_menu_item",
            parent="menu_file_dropout",
            before="menu_item_exit",
        )

        globalITEMS.windows.extend(["Open_PTU_menu_item"])

        
        
class _PHOTEXTR_menu_functions:
    
    def __init__(self):
        self.is_mounted = False
        self.mnt = _PHOTEXTR_mounting_functions()
        
    
    def unmnt_evthn(self, items, MTHD_conf):
        for item in reversed(items):
            dpg.delete_item(item)

        exec(MTHD_conf["menu_class_func"] + ".is_mounted = False")
        dpg.set_viewport_resize_callback(callback_none)
        self.is_mounted = False
        inV.mounted_method = None
        print(globalITEMS.last_directory)
        globalITEMS.windows = []


    def callback_PHOTEXTR_menu(self):
        if self.is_mounted:
            self.mnt.unmount_me(globalITEMS.windows)
            globalITEMS.windows = []
        else:
            if inV.mounted_method is not None:
                othm_conf = basf.method_config_dict(inV.mounted_method)
                self.unmnt_evthn(globalITEMS.windows, othm_conf)

        self.mnt.mount_me()
        self.is_mounted = True
        inV.mounted_method = "Modes/Extract_from_PTU"

        path_to_layout = os.path.join(
            "Modes/Extract_from_PTU",
            basf.path_to_method_anal_layout("Modes/Extract_from_PTU"),
        )
        execfile(path_to_layout)
        mode_cmn.define_file_menu_callbacks()

        
        
        
        
        
PE_manu_F = _PHOTEXTR_menu_functions()

