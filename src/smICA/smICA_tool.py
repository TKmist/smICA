'''
This file is part of the smICA repository that is distributed under the MIT license; see below.

This is the main script.

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
import platform
import os
import argparse
from decorator import decorator 
import dearpygui.dearpygui as dpg
import datetime
import numpy as np
import warnings
import json
import Required.INIT as inits
from Required.automation_panel import AutomationServerPanel
from Required.automation_runtime import AutomationService
from Required.automation_gui_commands import register_gui_commands
from screeninfo import get_monitors
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOCS_DIR = os.path.join(BASE_DIR , "doc" , "assets" , "help_html")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Start the smICA graphical application.")
    parser.add_argument(
        "--automation-server",
        action="store_true",
        help="Start the local automation server with smICA.",
    )
    parser.add_argument(
        "--automation-port",
        type=int,
        default=8765,
        help="Loopback TCP port for automation; use 0 to select a free port.",
    )
    parser.add_argument(
        "--automation-token-file",
        help="Read the optional automation authentication token from this file.",
    )
    parser.add_argument(
        "--automation-read-timeout",
        type=float,
        default=30.0,
        help="Maximum time to receive one complete request line.",
    )
    parser.add_argument(
        "--automation-max-request-bytes",
        type=int,
        default=1024 * 1024,
        help="Maximum encoded size of one automation request.",
    )
    parser.add_argument(
        "--automation-queue-size",
        type=int,
        default=32,
        help="Maximum number of commands waiting for the GUI thread.",
    )
    parser.add_argument(
        "--automation-commands-per-frame",
        type=int,
        default=4,
        help="Maximum automation commands processed during one GUI frame.",
    )
    parser.add_argument(
        "--automation-print-startup",
        action="store_true",
        help="Print one machine-readable record after the server starts.",
    )
    parser.add_argument(
        "--automation-allow-shutdown",
        action="store_true",
        help="Expose system.shutdown for explicitly controlled test processes.",
    )
    arguments = parser.parse_args()
    if not 0 <= arguments.automation_port <= 65535:
        parser.error("--automation-port must be between 0 and 65535")
    if arguments.automation_read_timeout <= 0:
        parser.error("--automation-read-timeout must be positive")
    if arguments.automation_max_request_bytes < 256:
        parser.error("--automation-max-request-bytes must be at least 256")
    if arguments.automation_queue_size < 1:
        parser.error("--automation-queue-size must be at least 1")
    if arguments.automation_commands_per_frame < 1:
        parser.error("--automation-commands-per-frame must be at least 1")
    return arguments, parser


def load_automation_token(token_file, parser):
    if token_file:
        try:
            token_path = os.path.abspath(os.path.expanduser(token_file))
            with open(token_path, encoding="utf-8") as token_stream:
                token = token_stream.read().strip()
        except OSError as exc:
            parser.error(f"cannot read --automation-token-file: {exc}")
        if not token:
            parser.error("--automation-token-file points to an empty file")
        return token
    return os.environ.get("SMICA_AUTOMATION_TOKEN", "").strip() or None


arguments, argument_parser = parse_arguments()
automation_token = load_automation_token(
    arguments.automation_token_file,
    argument_parser,
)

print(DOCS_DIR)

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

if platform.system().upper() == "LINUX":
    os.environ["__GLVND_DISALLOW_PATCHING"] = "1"

warnings.filterwarnings('ignore')
def callback_none():
    pass
with open(os.path.join('res','settings.json')) as settings:
    SETTINGS = json.load(settings)

docs_server = inits.LocalDocsServer(DOCS_DIR)
basf = inits._basicF()
updt = inits._updater(basf._hsv_to_rgb,VERSION)

inV=inits._init_varaibles()
    
viewport = inV.VIEWPORT_prop
menu = inits._init_Menu(updt.updater_state,
                        VERSION=VERSION,
                        docs_dir=DOCS_DIR,
                        docs_server=docs_server)

lprint=basf.lnprint

print(line)
print(line,end='\n\n')
print(Licence)
print('\n')
print('VERSION = ',VERSION,end='\n')
print(line)
print(line,end='\n\n')

inf_w, inf_h = get_monitors()[0].width, get_monitors()[0].height

dpg.create_context()
# execfile('Required/Themes.py')             # Load the themes definitions.
execfile('Required/Fonts.py') 
execfile('Required/Handlers.py')
execfile('Required/Themes.py')


dpg.create_viewport(title='smICA',small_icon = inV.icopath(),width=viewport['width'], height=viewport['height'],x_pos=viewport['pos'][0],y_pos  =viewport['pos'][1]) 
dpg.setup_dearpygui()
dpg.show_viewport()

globalITEMS = inits._common_VARIABLES()


VP_w = dpg.get_viewport_width()            # get initial width of the viewport
VP_h = dpg.get_viewport_height()           # get initial height of the viewport
 
menu.mount_main_Menu_bar()

rwroi = inits.rewrite_roi(viewport)
mxroi = inits.Roi_mixer(viewport,globalITEMS)

settwin = inits.sett_window(viewport,inV.init_left_indent,
                             inV.init_internal_indent,
                             inV.init_right_indent,
                             inV.init_bottom_indent,
                             inV.init_top_indent,
                             inV.init_group_spacer)



try:
   
    updt.run_updater()
    print('updt.updater_state =', updt.updater_state)
    
except:
    basf.some_fail()

inV.METHODS = basf.search_for_methods()

for method in inV.METHODS:

    path =os.path.join(method,basf.path_to_method_anal_menu_item(method))
    execfile(path)
    
basf.P2C_manu_F = P2C_manu_F
basf.PE_manu_F = PE_manu_F
basf.viewport = viewport
dpg.set_viewport_resize_callback(basf.basic_resizer)

THEME = settwin.OPTIONS['theme_choose']
# SETTINGS['Settings']['Theme']
build_themes(THEME)
basf.mount_inint_buttons()
mxroi.theme = THEME


def automation_state():
    return {
        "mounted_method": inV.mounted_method,
        "available_methods": list(inV.METHODS),
        "viewport": {
            "width": dpg.get_viewport_width(),
            "height": dpg.get_viewport_height(),
        },
    }


automation_service = AutomationService(
    application_version=VERSION,
    state_provider=automation_state,
    shutdown_callback=dpg.stop_dearpygui,
    allow_remote_shutdown=arguments.automation_allow_shutdown,
    queue_size=arguments.automation_queue_size,
    port=arguments.automation_port,
    authentication_token=automation_token,
    max_request_bytes=arguments.automation_max_request_bytes,
    read_timeout=arguments.automation_read_timeout,
)
automation_gui_commands = register_gui_commands(
    automation_service.registry,
    dpg,
    lambda: globals(),
)
automation_panel = AutomationServerPanel(
    automation_service,
    globalITEMS,
    default_port=arguments.automation_port,
)

if arguments.automation_server:
    try:
        automation_port = automation_service.start()
    except OSError as exc:
        automation_service.close()
        menu.on_exit()
        dpg.destroy_context()
        argument_parser.error(f"cannot start the automation server: {exc}")
    automation_panel.refresh()
    if arguments.automation_print_startup:
        print(json.dumps({
            "event": "automation_server_started",
            "protocol_version": 1,
            "host": "127.0.0.1",
            "port": automation_port,
        }, separators=(",", ":")), flush=True)

try:
    while dpg.is_dearpygui_running():
        automation_service.process_pending(arguments.automation_commands_per_frame)
        dpg.render_dearpygui_frame()
finally:
    automation_service.close()
    menu.on_exit()
    dpg.destroy_context()
