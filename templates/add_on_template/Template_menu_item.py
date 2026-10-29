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

import os

import dearpygui.dearpygui as dpg


class _Template_mounting_functions:
    """Create and remove GUI elements owned by the example mode."""

    def unmount_me(self, mounted_items):
        for item in reversed(mounted_items):
            if dpg.does_item_exist(item):
                dpg.delete_item(item)
        dpg.set_viewport_resize_callback(callback_none)
        Template_menu_F.is_mounted = False
        inV.mounted_method = None

    def mount_me(self):
        dpg.add_menu_item(
            label="Open input directory",
            tag="Template_open_directory_menu_item",
            parent="menu_file_dropout",
            before="menu_item_exit",
        )
        globalITEMS.windows.append("Template_open_directory_menu_item")


class _Template_menu_functions:
    """Switch from the active analytical mode to the example mode."""

    def __init__(self):
        self.is_mounted = False
        self.mnt = _Template_mounting_functions()

    def unmount_other_mode(self, mounted_items, mode_definition):
        for item in reversed(mounted_items):
            if dpg.does_item_exist(item):
                dpg.delete_item(item)
        menu_controller = globals().get(mode_definition["menu_class_func"])
        if menu_controller is not None:
            menu_controller.is_mounted = False
        dpg.set_viewport_resize_callback(callback_none)
        inV.mounted_method = None
        globalITEMS.windows = []

    def callback_Template_menu(self, sender=None, app_data=None, user_data=None):
        if self.is_mounted:
            self.mnt.unmount_me(globalITEMS.windows)
            globalITEMS.windows = []
        elif inV.mounted_method is not None:
            definition = basf.method_config_dict(inV.mounted_method)
            self.unmount_other_mode(globalITEMS.windows, definition)

        self.mnt.mount_me()
        self.is_mounted = True
        inV.mounted_method = os.path.join("Modes", "add_on_template")
        layout_path = os.path.join(
            inV.mounted_method,
            basf.path_to_method_anal_layout(inV.mounted_method),
        )
        execfile(layout_path)
        mode_cmn.define_file_menu_callbacks()


Template_menu_F = _Template_menu_functions()

dpg.add_menu_item(
    label="Template analysis",
    parent="menu_analysis_method_dropout",
    tag="Analysis_submenu_item_Template",
    callback=Template_menu_F.callback_Template_menu,
)
