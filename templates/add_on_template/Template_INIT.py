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


class _Template_init:
    """Store geometry and initial state for the example analytical mode."""

    def __init__(
        self,
        size_ratio,
        left_indent,
        internal_indent,
        right_indent,
        bottom_indent,
        top_indent,
        group_spacer,
        font_size,
        last_directory,
    ):
        self.size_ratio = size_ratio
        self.last_directory = last_directory or os.getcwd()
        self.left_indent = int(left_indent * size_ratio["width"])
        self.internal_indent = int(internal_indent * size_ratio["width"])
        self.right_indent = int(right_indent * size_ratio["width"])
        self.bottom_indent = int(bottom_indent * size_ratio["height"])
        self.top_indent = int(top_indent * size_ratio["height"])
        self.group_spacer = int(group_spacer * size_ratio["width"])
        self.font_size = font_size

        available_width = (
            dpg.get_viewport_width() - self.left_indent - self.right_indent
        )
        available_height = (
            dpg.get_viewport_height() - self.top_indent - self.bottom_indent
        )
        self.control_window = {
            "name": "Template_control_window",
            "width": max(280, int(available_width * 0.3)),
            "height": max(240, available_height),
            "pos": (self.left_indent, self.top_indent),
        }
        self.output_window = {
            "name": "Template_output_window",
            "width": max(
                320,
                available_width
                - self.control_window["width"]
                - self.internal_indent,
            ),
            "height": max(240, available_height),
            "pos": (
                self.left_indent
                + self.control_window["width"]
                + self.internal_indent,
                self.top_indent,
            ),
        }
        self.run_button = {
            "name": "Template_run_button",
            "width": -1,
            "height": int(40 * size_ratio["height"]),
        }
        self.directory_dialog = {
            "name": "Template_directory_dialog",
            "width": max(640, int(dpg.get_viewport_width() * 0.75)),
            "height": max(480, int(dpg.get_viewport_height() * 0.75)),
        }


class _Template_common:
    """Hold callbacks and analytical functions for the example mode."""

    def __init__(self, mode_init, basic_functions, global_items):
        self.mode_init = mode_init
        self.basf = basic_functions
        self.global_items = global_items
        self.last_directory = mode_init.last_directory
        self.dialog_windows = [mode_init.directory_dialog["name"]]

    def calculate_example(self, sender=None, app_data=None, user_data=None):
        """Replace this callback with the analytical operation."""
        dpg.set_value(
            "Template_status_text",
            "The example callback completed. Add the analytical result here.",
        )

    def open_directory_dialog(self, sender=None, app_data=None, user_data=None):
        dpg.show_item(self.mode_init.directory_dialog["name"])

    def select_directory(self, sender, app_data, user_data=None):
        self.last_directory = app_data["current_path"]
        self.global_items.last_directory = self.last_directory
        for dialog in self.dialog_windows:
            dpg.configure_item(dialog, default_path=self.last_directory)
        dpg.set_value(
            "Template_selected_directory",
            "Selected directory: " + self.last_directory,
        )

    def define_file_menu_callbacks(self):
        dpg.configure_item(
            "Template_open_directory_menu_item",
            callback=self.open_directory_dialog,
        )
