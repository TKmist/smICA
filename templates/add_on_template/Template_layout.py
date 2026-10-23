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

from Modes.add_on_template.Template_INIT import _Template_common, _Template_init


def Template_resizer(sender, app_data):
    """Recalculate and apply the example mode geometry."""
    ratio = {
        "width": round(app_data[0] / inV.VIEWPORT_prop["width"], 4),
        "height": round(app_data[1] / inV.VIEWPORT_prop["height"], 4),
    }
    inV.init_size_ratio = ratio
    mode_init.__init__(
        ratio,
        inV.init_left_indent,
        inV.init_internal_indent,
        inV.init_right_indent,
        inV.init_bottom_indent,
        inV.init_top_indent,
        inV.init_group_spacer,
        inV.init_font_size,
        globalITEMS.last_directory,
    )
    for properties in (mode_init.control_window, mode_init.output_window):
        dpg.configure_item(
            properties["name"],
            width=properties["width"],
            height=properties["height"],
            pos=properties["pos"],
        )


mode_init = _Template_init(
    inV.init_size_ratio,
    inV.init_left_indent,
    inV.init_internal_indent,
    inV.init_right_indent,
    inV.init_bottom_indent,
    inV.init_top_indent,
    inV.init_group_spacer,
    inV.init_font_size,
    globalITEMS.last_directory,
)
mode_cmn = _Template_common(mode_init, basf, globalITEMS)
dpg.set_viewport_resize_callback(Template_resizer)

with dpg.window(
    label="Template controls",
    tag=mode_init.control_window["name"],
    width=mode_init.control_window["width"],
    height=mode_init.control_window["height"],
    pos=mode_init.control_window["pos"],
    no_move=True,
    no_close=True,
    no_resize=True,
):
    dpg.add_text(
        "Selected directory: " + mode_cmn.last_directory,
        tag="Template_selected_directory",
        wrap=mode_init.control_window["width"] - 20,
    )
    dpg.add_button(
        label="Run example calculation",
        tag=mode_init.run_button["name"],
        width=mode_init.run_button["width"],
        height=mode_init.run_button["height"],
        callback=mode_cmn.calculate_example,
    )

with dpg.window(
    label="Template output",
    tag=mode_init.output_window["name"],
    width=mode_init.output_window["width"],
    height=mode_init.output_window["height"],
    pos=mode_init.output_window["pos"],
    no_move=True,
    no_close=True,
    no_resize=True,
):
    dpg.add_text("Ready.", tag="Template_status_text", wrap=-1)

dpg.add_file_dialog(
    directory_selector=True,
    label="Select input directory",
    tag=mode_init.directory_dialog["name"],
    width=mode_init.directory_dialog["width"],
    height=mode_init.directory_dialog["height"],
    default_path=mode_cmn.last_directory,
    callback=mode_cmn.select_directory,
    cancel_callback=callback_none,
    show=False,
    modal=False,
)

globalITEMS.windows.extend(
    [
        mode_init.control_window["name"],
        mode_init.output_window["name"],
        mode_init.directory_dialog["name"],
    ]
)
