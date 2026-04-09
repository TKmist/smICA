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
import numpy as np
import pandas as pd
from numpy import log10
import dearpygui.dearpygui as dpg
import json
import webbrowser
import inspect
import time
import re
import requests
import tempfile
import zipfile
import shutil

from pathlib import Path

class _updater:
    
    _VERSION_RE = re.compile(r"^\s*[vV]?(\d+)\.(\d+)\.(\d+)(?:rc(\d+)|([A-Za-z]))?\s*$")
   

    def __init__(self, hsv, version: str):
        """
        :param version: local application version, e.g. '1.1.0' or '1.1.0a'
        """
        self.VERSION = version
        self.version = version.strip()
        self.updater_state = False
        self.hsv = hsv

        self.owner = "TKmist"
        self.repo = "smICA"
        self.branch = "many_cells_auto_roi"
        self.path = "VERSION"

    def _parse_version(self, ver: str):
        
        m = self._VERSION_RE.match(ver)
        if not m:
            raise ValueError(
                f"Invalid version format: {ver!r}. Expected e.g. 'v1.2.3', 'v1.2.3rc1', 'v1.2.3a'."
            )
    
        major, minor, patch = map(int, m.group(1, 2, 3))
        rc_num = m.group(4)     # digits after 'rc', e.g. '1'
        letter = m.group(5)     # single letter, e.g. 'a'
    
        if rc_num is None and letter is None:
            stage_rank = 3   # final
            detail_rank = 0
        elif rc_num is not None:
            stage_rank = 2   # rc
            detail_rank = int(rc_num)   # rc2 > rc1
        else:
            stage_rank = 1   # pre-release letter
            s = letter.lower()
            if not ("a" <= s <= "z"):
                raise ValueError(f"Invalid version suffix: {letter!r}")
            detail_rank = 26 - (ord(s) - ord("a"))  # a newest among letters
    
        return (major, minor, patch, stage_rank, detail_rank)

    def _raw_version_url(
        self, owner: str, repo: str, branch: str, path: str = "VERSION"
    ) -> str:
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

    def check_remote_version(
        self,
        owner: str,
        repo: str,
        branch: str,
        *,
        path: str = "VERSION",
        token: str | None = None,
        timeout: float = 10.0,
    ) -> tuple[bool, str | None]:
        """
        Checks whether the version on GitHub (VERSION file on a given branch)
        is newer than the local self.version.

        :param owner: GitHub repository owner
        :param repo: repository name
        :param branch: branch name (e.g. 'develop', 'release/2.0')
        :param path: path to the version file (default: 'VERSION')
        :param token: optional GitHub token for private repositories
        :param timeout: HTTP request timeout
        :return: (is_newer, remote_version)
        """
        url = self._raw_version_url(owner, repo, branch, path)
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code != 200:
                print(f"[Updater] Failed to download VERSION from {url} ({resp.status_code})")
                return (False, None)
            
            remote_txt = resp.text.strip()
            

        except requests.RequestException as e:
            print(f"[Updater] Network error: {e}")
            return (False, None)

        try:
            

            remote_tuple = self._parse_version(remote_txt)
            local_tuple = self._parse_version(self.version)
        except ValueError as e:
            print(f"[Updater] Version parsing error: {e}")
            return (False, remote_txt)
        
        is_newer = remote_tuple > local_tuple
        
        return (is_newer, remote_txt)

    def proceed_update_window(self):
        window_width, window_height = 400, 400
        viewport_width, viewport_height = (
            dpg.get_viewport_client_width(),
            dpg.get_viewport_client_height(),
        )
        pos_x = (viewport_width - window_width) // 2
        pos_y = (viewport_height - window_height) // 2
        try:
            with dpg.window(
                pos=(pos_x, pos_y),
                label="Update now?",
                tag="proceed_to_update_window",
                no_move=True,
                no_close=False,
                no_title_bar=False,
                show=True,
                modal=True,
                autosize=True,
                no_scrollbar=True,
            ):
                dpg.add_text(
                    "Press OK to install the files and close the program.",
                    tag="proceed_to_update_window_text",
                )
                dpg.bind_item_font("proceed_to_update_window_text", "DejaVu_bold")
                with dpg.group(tag="proceed_to_update_window_group", horizontal=True):
                    dpg.add_button(
                        label="OK",
                        tag="proceed_to_update_window_ok_butt",
                        show=True,
                        callback=self.proceed_window_OK,
                    )

                    dpg.add_button(
                        label="Close",
                        tag="proceed_to_update_window_close_butt",
                        show=True,
                        callback=self.proceed_window_close,
                    )

                dpg.bind_item_theme("proceed_to_update_window_ok_butt", "button_theme")
                dpg.bind_item_theme("proceed_to_update_window_close_butt", "Error_window_theme")

        except Exception:
            dpg.show_item("No_data_files")

    def proceed_window_close(self):
        dpg.configure_item("proceed_to_update_window", show=False)
        dpg.delete_item("proceed_to_update_window_text")
        dpg.delete_item("proceed_to_update_window_ok_butt")
        dpg.delete_item("proceed_to_update_window_close_butt")
        dpg.delete_item("proceed_to_update_window_group")
        dpg.delete_item("proceed_to_update_window")

    def proceed_window_OK(self):
        # print("proceed_window_OK")
        window_size = dpg.get_item_rect_size("proceed_to_update_window")

        dpg.delete_item("proceed_to_update_window_ok_butt")
        dpg.delete_item("proceed_to_update_window_close_butt")
        dpg.delete_item("proceed_to_update_window_group")

        dpg.add_loading_indicator(
            parent="proceed_to_update_window",
            width=50,
            tag="tag_load_ind_update",
            pos=(
                dpg.get_item_width("proceed_to_update_window") / 2
                - (int(dpg.get_global_font_scale() * 25)),
                1 * dpg.get_item_height("proceed_to_update_window")
                - dpg.get_global_font_scale() * 25,
            ),
            color=self.hsv(2 / 7.0, 0.6, 0.6),
            secondary_color=self.hsv(0.223, 0.404, 0.846),
        )
        dpg.add_button(
            label="",
            tag="progress_button",
            show=True,
            pos=(
                0,
                1 * dpg.get_item_height("proceed_to_update_window")
                + dpg.get_global_font_scale() * 50,
            ),
            parent="proceed_to_update_window",
            width=window_size[0],
        )

        dpg.bind_item_theme("progress_button", "transparent_theme")
        dpg.set_item_label("progress_button", "Downloading files")

        self.download_update(owner=self.owner, repo=self.repo, branch=self.branch)
        self.backup_old_files()

        self.Copying_new_files()

        for i in range(3, -1, -1):
            dpg.set_item_label(
                "progress_button",
                "Finished. smICA closes in: " + str(i) + " sec.",
            )
            time.sleep(1)

        dpg.delete_item("progress_button")
        dpg.delete_item("tag_load_ind_update")

        self.proceed_window_close()

        dpg.delete_item("proceed_to_update_window")
        dpg.stop_dearpygui()

    def backup_old_files(self):
        current_dir = os.path.abspath(os.getcwd())

        bckp_dir = os.path.join(current_dir, "..", "old_backup")

        if os.path.exists(bckp_dir):
            # print("[Updater] Removing old backup directory...")
            dpg.set_item_label("progress_button", "Removing old backup files")
            shutil.rmtree(bckp_dir, ignore_errors=True)

        os.makedirs(bckp_dir, exist_ok=True)
        metafiles = ["LICENSE", "README.md", "VERSION"]
        FoldersToBackup = ["REWRITE_ROI", "smICA"]

        for f in metafiles:
            # print("[Updater] Removing old backup directory...")
            dpg.set_item_label("progress_button", "Backing up meta files")
            source = os.path.join(current_dir, "..", f)
            target = os.path.join(bckp_dir, f)
            shutil.copy2(source, target)

        for d in FoldersToBackup:
            dpg.set_item_label("progress_button", "Backing up software directories")
            source = os.path.join(current_dir, "..", d)
            target = os.path.join(bckp_dir, d)
            shutil.copytree(
                source,
                target,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    "*updt_tmp", "__pycache__", ".ipynb_checkpoints"
                ),
            )

    def Copying_new_files(self):
        current_dir = os.path.abspath(os.getcwd())
        tmp_dir = os.path.join(current_dir, "..", "updt_tmp")
        zip = os.listdir(tmp_dir)
        zip = [f for f in zip if f.endswith(".zip")][0]
        dpg.set_item_label("progress_button", "Unzipping update")
        zip_path = os.path.join(tmp_dir, zip)
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(tmp_dir)
        except zipfile.BadZipFile:
            return None

        subfolders = [
            d for d in os.listdir(tmp_dir)
            if os.path.isdir(os.path.join(tmp_dir, d))
        ]

        if not subfolders:
            return None

        extracted_dir = subfolders[0]
        updt_dir = os.path.join(tmp_dir, extracted_dir)
        metafiles = ["LICENSE", "README.md", "VERSION"]
        for f in metafiles:
            print("[Updater] Removing old backup directory...")
            dpg.set_item_label("progress_button", "Updating meta files")
            source = os.path.join(updt_dir, f)
            target = os.path.join(current_dir, "..", f)
            shutil.copy(source, target)

        FoldersToBackup = ["REWRITE_ROI", "smICA"]
        for d in FoldersToBackup:
            dpg.set_item_label("progress_button", "Updating software directories")
            source = os.path.join(updt_dir, "src", d)
            target = os.path.join(current_dir, "..", d)
            shutil.copytree(
                source,
                target,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(
                    "*updt_tmp", "__pycache__", ".ipynb_checkpoints"
                ),
            )

        dpg.set_item_label("progress_button", "Removing temporary files")
        shutil.rmtree(tmp_dir, ignore_errors=True)

    def download_update(
        self,
        owner: str,
        repo: str,
        branch: str,
        *,
        token: str | None = None,
        timeout: float = 30.0,
    ) -> str | None:
        """
        Downloads the current program files as a ZIP archive from the GitHub repository
        and saves them into the temporary directory 'updt_tmp'.

        :param owner: GitHub repository owner
        :param repo: repository name
        :param branch: branch name (e.g. 'develop', 'main')
        :param token: optional GitHub token (for private repositories)
        :param timeout: timeout in seconds
        :return: path to the temporary directory with downloaded/unpacked files, or None on error
        """
        current_dir = os.path.abspath(os.getcwd())

        tmp_dir = os.path.join(current_dir, "..", "updt_tmp")
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
        os.makedirs(tmp_dir, exist_ok=True)

        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        zip_path = os.path.join(tmp_dir, f"{repo}-{branch}.zip")

        try:
            with requests.get(zip_url, headers=headers, timeout=timeout, stream=True) as r:
                r.raise_for_status()
                with open(zip_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        except requests.RequestException:
            return None

    def run_updater(self):
        is_newer, remote = self.check_remote_version(
            owner=self.owner,
            repo=self.repo,
            branch=self.branch,
            path=self.path,
        )
        theme_tag = dpg.get_item_theme("menu_about_dropout")

        if is_newer:
            self.updater_state = True
            dpg.bind_item_theme("menu_about_dropout", "menu_update_available")
            children = dpg.get_item_children("menu_about_dropout", 1)  # slot 1 = normal children

            for child in children:
                if str(child).isdigit():
                    child = dpg.get_item_alias(child)

                if child == "menu_Version_dropout_item":
                    dpg.bind_item_theme(child, "menu_update_available")
                    dpg.set_item_label(child, label="Current version: " + self.VERSION + " !")
                    dpg.bind_item_font(child, "DejaVu_bold")
                    dpg.add_menu_item(
                        label="New version: " + remote + " available, click to update now",
                        enabled=True,
                        tag="menu_Version_dropout_item_new",
                        parent="menu_about_dropout",
                        callback=self.proceed_update_window,
                    )
                    dpg.bind_item_theme("menu_Version_dropout_item_new", "menu_update_available_new")
                    dpg.bind_item_font("menu_Version_dropout_item_new", "DejaVu_bold")
                else:
                    dpg.bind_item_theme(child, "menu_normal")
        else:
            self.updater_state = False



class _basicF:
    
    
    def __init__(self):
        pass
    
    
    
    def lnprint(self,*args, **kwargs):
     
        caller_frame = inspect.currentframe().f_back
        line_number = caller_frame.f_lineno
        
        file_name = caller_frame.f_code.co_filename
        function_name = caller_frame.f_code.co_name
        
        print(f"File {file_name}, Function '{function_name}', Line {line_number}: ", end="\n")

        
        print(*args, **kwargs)
    @staticmethod
    def some_fail():
        caller_frame = inspect.currentframe().f_back
        line_number = caller_frame.f_lineno
        
        file_name = caller_frame.f_code.co_filename
        function_name = caller_frame.f_code.co_name
        print('Coś się zdupcyło \U0001F633','\n',end='\n')
        print(f"File:\n \t{file_name},\n Function: \t'{function_name}',\n Line: \t{line_number} ", end="\n")
        
    def add_font_to_registry(self,font_size):
        font_path = os.path.join('res','Fonts','DejaVuSansCondensed.ttf')
        bold_font_path = os.path.join('res','Fonts','DejaVuSansCondensed-Bold.ttf')
        with dpg.font_registry(tag='Font_registry'):
            '''Add a font registry.'''
            
            with dpg.font(font_path, font_size,tag='DejaVu') as font_18:
                dpg.add_font_range(0x0300, 0x03ff)
                dpg.add_font_range(0x0200, 0x02ff)
                dpg.add_font_range(0x2080, 0x209C)
                dpg.add_font_range(0x2190, 0x2193)
                default_font = font_18

            with dpg.font(bold_font_path, font_size,tag='DejaVu_bold') as bold_font_18:
                dpg.add_font_range(0x0300, 0x03ff)
                dpg.add_font_range(0x0200, 0x02ff)
                dpg.add_font_range(0x2080, 0x209C)
                dpg.add_font_range(0x2190, 0x2193)
                
            dpg.bind_font(default_font)
        

    def remove_font_from_registry(self):
        font = 'DejaVu'
        dpg.delete_item(font)
        dpg.delete_item('Font_registry')
        
    def _hsv_to_rgb(self,h, s, v):
        '''Funtion converts HSV color notation to the RGB values'''
        if s == 0.0: return (v, v, v)
        i = int(h*6.) 
        f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
        if i == 0: return (255*v, 255*t, 255*p)
        if i == 1: return (255*q, 255*v, 255*p)
        if i == 2: return (255*p, 255*v, 255*t)
        if i == 3: return (255*p, 255*q, 255*v)
        if i == 4: return (255*t, 255*p, 255*v)
        if i == 5: return (255*v, 255*p, 255*q)

    def search_for_methods(self):
        path = 'Modes'
        methods = os.listdir(path)
        ind = []
        methods = [os.path.join(path,ad) for ad in methods if os.path.isdir(os.path.join(path,ad))]
        for i, method in enumerate(methods):
            met_files = os.listdir(method)
            met_files = [f for f in met_files if f.endswith('_config.json')]
            if len(met_files) == 1:
                ind.append(i)
        methods = list(np.array(methods)[ind])
        return methods
    def ifso(self,f):
            if type(f)  == bytes:
                f = f.decode("utf-8")
            else:
                pass
            return f
    
    def path_to_method_anal_menu_item(self,method_dir):
        met_files = os.listdir(method_dir)
        
        
            
            
        
        met_files = [ self.ifso(f) for f in met_files]
        met_files = [f for f in met_files if f.endswith('_config.json')]
        met_file = met_files[0]
        path = os.path.join(method_dir,met_file)

        with open(path) as json_settings:
            method_tree = json.load(json_settings)

        return method_tree['ANAL_MENU_ITEM']

    def method_config_dict(self,method_dir):
        met_files = os.listdir(method_dir)
        met_files = [ self.ifso(f) for f in met_files]
        met_files = [str(f) for f in met_files if str(f).endswith('_config.json')]
        met_file = met_files[0]
        path = os.path.join(method_dir,met_file)
        with open(path) as json_settings:
            method_tree = json.load(json_settings)

        return method_tree
    
    
    def path_to_method_anal_layout(self,method_dir):
        
        met_files = os.listdir(method_dir)
            
            
        
        met_files = [ self.ifso(f) for f in met_files]
        met_files = [f for f in met_files if f.endswith('_config.json')]
        met_file = met_files[0]
        path = os.path.join(method_dir,met_file)
        with open(path) as json_settings:
            method_tree = json.load(json_settings)

        return method_tree['LAYOUT']
    
    
    def split_path_into_folders(self,path):
        folders = []
        while True:
            path, folder = os.path.split(path)
            if folder != "":
                folders.append(folder)
            else:
                if path != "":
                    folders.append(path)
                break
        folders.reverse()
        return folders
    
    
   
        
    
    def callback_init_buttons(self,sender,app_data):
        
        if sender == 'EXTRACT_FROM_PTU_INIT_BUTTON':
            self.PE_manu_F.callback_PHOTEXTR_menu()  
             

        elif sender == 'Phot_2_Conc_INIT_BUTTON':
            self.P2C_manu_F.callback_PHOT2CONC_menu()  
        
        self.unmount_inint_buttons()

        dpg.add_menu_item(label="Extract from PTU",
                          parent ='menu_analysis_method_dropout' ,
                          tag='Analysis_submenu_item_PhotExtract',
                          callback=self.PE_manu_F.callback_PHOTEXTR_menu)
        
        dpg.add_menu_item(label="Phot2Conc",
                          parent ='menu_analysis_method_dropout' ,
                          tag='Analysis_submenu_item_Phot2conc',
                          callback=self.P2C_manu_F.callback_PHOT2CONC_menu)
        
        dpg.maximize_viewport()

    def unmount_inint_buttons(self):
        dpg.hide_item('initial_window')
        dpg.delete_item('Phot_2_Conc_INIT_BUTTON')
        dpg.delete_item('EXTRACT_FROM_PTU_INIT_BUTTON')
        dpg.delete_item('initial_window')
        
    def basic_resizer(self,sender, app_data):
        self.unmount_inint_buttons()

        ratio = {'width': np.round(app_data[0] / self.viewport['width'], 4),
             'height': np.round(app_data[1] / self.viewport['height'], 4)}

        fnt_ratio = (ratio['width'] + ratio['height']) / 2
        font_scale = np.round(fnt_ratio, 3)
        dpg.set_global_font_scale(font_scale)
        
        self.mount_inint_buttons()
        
    
    def mount_inint_buttons(self):

        VP = {'width':dpg.get_viewport_width(),
             'height':dpg.get_viewport_height()}

        initial_window = {'name':'initial_window',
                            'width':int(VP['width']/3),
                            'height':int(VP['height']/3),
                            'pos':(int(VP['width']/2-(VP['width']/3)/2),
                                   int(VP['height']/2-(VP['height']/3)/2))
                            }
        EXTRACT_FROM_PTU_INIT_BUTTON = {'name':'EXTRACT_FROM_PTU_INIT_BUTTON',
                                             'width':-1,
                                             'height':int(initial_window['height']/2.2),
                                             }
        Phot_2_Conc_INIT_BUTTON = {'name':'Phot_2_Conc_INIT_BUTTON',
                                             'width':-1,
                                             'height':int(initial_window['height']/2.2),
                                             }

        

        
        with dpg.window(tag = 'initial_window',
                                width = initial_window['width'],
                                height = initial_window['height'],
                                pos = initial_window['pos'],
                                menubar=False,
                                autosize=False,
                                no_title_bar=True,
                                no_move=True,
                                no_resize=True,
                                no_background=True,
                                modal=False,
                                show=True
                               ):
            dpg.add_button(label="EXTRACT from PTU and FILTER",
                       callback=self.callback_init_buttons,
                       width = EXTRACT_FROM_PTU_INIT_BUTTON['width'],
                       height = EXTRACT_FROM_PTU_INIT_BUTTON['height'],
                       tag='EXTRACT_FROM_PTU_INIT_BUTTON',
                       show=True,enabled=True
                      )
            dpg.bind_item_theme('EXTRACT_FROM_PTU_INIT_BUTTON', 'button_theme')
            dpg.add_button(label="Phot 2 Conc",
                       callback=self.callback_init_buttons,
                       width = Phot_2_Conc_INIT_BUTTON['width'],
                       height = Phot_2_Conc_INIT_BUTTON['height'],
                       tag='Phot_2_Conc_INIT_BUTTON',
                       show=True,enabled=True
                      )
            dpg.bind_item_theme('Phot_2_Conc_INIT_BUTTON', 'button_theme')
        
    
    
##############################################################################    
class _init_varaibles:
    
    def __init__(self):
        
        self.init_size_ratio = {'width':1,
                          'height':1}
        self.init_top_indent = 24+11
        if os.name == 'posix':

            self.init_bottom_indent = 11
            self.init_right_indent = 11
        else:
            self.init_bottom_indent = 5*11
            self.init_right_indent = int(np.round(2.5*11))

        self.init_left_indent = 11
        
        self.init_internal_indent = 11
        self.init_group_spacer = 2
        self.init_font_size = 18
        self.VIEWPORT_prop = {'width':1585,
                              'height':950+2*11,
                              'pos':(0,0)
                                }
        self.mounted_method = None
        self.main_last_directory = None


        
        
    def icopath(self):
        osname = os.name

        if osname == 'posix':

            ico_path=os.path.join('res','icons','smICA.png')
            
        else:
            ico_path=os.path.join('res','icons','smICA.ico')
            
        return ico_path

class _init_Menu:
    def __init__(self,upd_st,VERSION):
        self.VERSION = VERSION
        self.theme = 'dark'
        
        self.upd_st = upd_st
    def callback_license(self,sender,app_data):
        if not 'License_title' in dpg.get_aliases():
            with dpg.window(tag='License_win',width=dpg.get_viewport_width()/2,
                            height=dpg.get_viewport_height()/2,
                                pos = (dpg.get_viewport_width()/4,
                                       dpg.get_viewport_height()/4),
                                menubar=False,
                                autosize=False,
                                no_resize=True,
                                no_title_bar=False,
                                no_move=True,

                                modal=True,

                           show=True):
                dpg.add_button(tag='License_title',width=dpg.get_viewport_width()/2,label='LICENSE')

                dpg.bind_item_theme('License_title', 'transparent_theme')
                with open('../LICENSE', 'r') as file:
                    License = file.read()
                dpg.add_text(label='License',
                             tag='license_text',
                             default_value = License,
                             wrap = int(0.95*(dpg.get_viewport_width()/2)))
        else:
            dpg.delete_item('license_text')
            dpg.delete_item('License_title')
            dpg.delete_item('License_win')
            with dpg.window(tag='License_win',width=dpg.get_viewport_width()/2,
                            height=dpg.get_viewport_height()/2,
                                pos = (dpg.get_viewport_width()/4,
                                       dpg.get_viewport_height()/4),
                                menubar=False,
                                autosize=False,
                                no_resize=True,
                                no_title_bar=False,
                                no_move=True,

                                modal=True,

                           show=True):
                dpg.add_button(tag='License_title',width=dpg.get_viewport_width()/2,label='LICENSE')

                dpg.bind_item_theme('License_title', 'transparent_theme')
                with open('../LICENSE', 'r') as file:
                    License = file.read()
                dpg.add_text(label='License',
                             tag='license_text',
                             default_value = License,
                             wrap = int(0.95*(dpg.get_viewport_width()/2)))

    def callback_help(self,sender,app_data):
        url = os.path.join('Docs','README.html')
        webbrowser.open(url,new=2)

        
    def mount_main_Menu_bar(self):
    
        with dpg.viewport_menu_bar(tag="vieport's_menubar"):
            with dpg.menu(label="File",tag='menu_file_dropout'):
                dpg.add_menu_item(label="Exit",callback=lambda: dpg.stop_dearpygui(),tag='menu_item_exit')
            dpg.bind_item_theme('menu_file_dropout', "menu_normal")
            with dpg.menu(label="Mode",tag='menu_analysis_method_dropout'):
                pass
            dpg.bind_item_theme('menu_analysis_method_dropout', "menu_normal")
            
            
            with dpg.menu(label="About",tag='menu_about_dropout'):
                dpg.add_menu_item(label="Help",tag='helpclick',callback=self.callback_help)
                dpg.add_menu_item(label='License',
                                  callback = self.callback_license,
                                  tag='menu_License_dropout_item')
               
                dpg.add_menu_item(label='Version: '+self.VERSION,enabled=False,tag='menu_Version_dropout_item')
                    
                
            dpg.bind_item_theme('menu_about_dropout', "menu_normal")

class _common_VARIABLES:
    def __init__(self):
        self.windows = []
        self.items = []
        self.last_directory = ''
        self.directory = ''
        


class rewrite_roi:
    def __init__(self,viewport):
        self.rwroiItems=[]
        self.load_RWroi_into_menu()
        self.source_type = None
        self.viewport = viewport
        self.data_files = None
        self._path = ''
    
    def unmount_rewriteROI(self):
        for item in reversed(self.rwroiItems):
            dpg.delete_item(item)
        self.rwroiItems = []
        
        
    def mount_rewriteROI(self):
        
        size_ratio = {'width':dpg.get_viewport_width()/self.viewport['width'],
                      'height':dpg.get_viewport_height()/self.viewport['height']}
        win_width = 600*size_ratio['width'] 
        win_height = 700*size_ratio['height'] 
        win_pos = (int(dpg.get_viewport_width()/2-int(600*size_ratio['width'])/2),
                   int(dpg.get_viewport_height()/2-int(700*size_ratio['height'])/2))

        with dpg.window(label='Rewrite ROI',
                        width=win_width,
                        height=win_height,
                        pos = win_pos,
                        no_move=False,
                        no_close=False,
                        no_title_bar=False,
                        no_scrollbar=True,
                        no_resize=False,
                        no_collapse=True,
                        tag='rewrite_window',
                        autosize=True,
                        show=True,
                        on_close = self.callbac_rw_win_closed
                        ):
            dpg.add_button(label='Open ROI folder',
                           tag='open_roi_folder',
                           width=win_width,
                           callback=lambda: dpg.show_item('ROISource_file_dialog')
                          )
            dpg.bind_item_theme('open_roi_folder', 'button_theme')
            dpg.add_text('',tag='tag_source_path',wrap=win_width)
            with dpg.group(tag='resolution_group', horizontal=True):
                dpg.add_input_text(tag='add_text_width',width=int(288*size_ratio['width']))
                dpg.add_text('x',tag='tag_x')
                dpg.add_input_text(tag='add_text_height',width=int(289*size_ratio['width']))
            dpg.add_button(label='Target ROI folder',
                           tag='target_roi_folder',
                           width=win_width,
                           callback=lambda: dpg.show_item('ROITarget_file_dialog')
                          )
            dpg.bind_item_theme('target_roi_folder', 'button_theme')
            dpg.add_text('',tag='tag_target_path',wrap=win_width)
           
            dpg.add_listbox(items=[],
                            width=win_width,
                            tag='ROIfile_box'
                           )
            
            dpg.add_button(label='Proceded',tag='ROIRun_script',width=win_width,callback=self.callback_proceed_ROI)
            dpg.bind_item_theme('ROIRun_script', 'button_theme')

        dpg.add_file_dialog(directory_selector=True,
                            label = 'Select source ROI folder',
                            width =win_width*2,
                            height=win_height,
                            default_path = self._path,
                            show=False,
                            file_count=5,
        
                            callback=self.callback_open_source_folder,
                            cancel_callback=self.callback_empty,
                            tag="ROISource_file_dialog",
                            modal=False
                           )
        
        
        dpg.add_file_dialog(directory_selector=True,
                            label = 'Select target ROI folder',
                            show=False,
                            width =win_width*2,
                            height=win_height,
                            default_path = self._path,
                            file_count=5,
        
                            callback=self.callback_open_target_folder,
                            cancel_callback=self.callback_empty,
                            tag="ROITarget_file_dialog",
                            modal=False
                           )
        self.rwroiItems.extend(['rewrite_window',
                           'open_roi_folder',
                           'tag_source_path',
                           'add_text_height',
                           'tag_x',
                           'add_text_width',
                           'resolution_group',
                           'target_roi_folder',
                           'tag_target_path',
                           'ROIfile_box',
                           'ROIRun_script',
                           'ROISource_file_dialog',
                           'ROITarget_file_dialog'])
        
    
    
    def rewrite_tool(self,sender,app_data):
        rwrt_win = 'rewrite_window'
        if dpg.does_item_exist(rwrt_win):
            
            self.mount_rewriteROI()
            
        else:
            self.mount_rewriteROI()

    def load_RWroi_into_menu(self):
        with dpg.menu(label="Tools",
                      tag='menu_analysis_tool_dropout',
                      parent="vieport's_menubar",
                      before='menu_about_dropout'):
            dpg.add_menu_item(label="Rewrite ROI",tag='Rewrite_ROI',callback=self.rewrite_tool)

    def callbac_rw_win_closed(self):
        # print('closed')
        self.unmount_rewriteROI()
        rwrt_win = 'rewrite_window'



    def callback_open_source_folder(self,sender,app_data):
    
        # global source_type, _path
        source_type = None
        path = app_data['file_path_name']
        self._path = path
        dpg.set_value('tag_source_path',path)
        
        files = os.listdir(path)
        csv_files = [f for f in files if f.endswith('.csv')]
        dat_files = [f for f in files if f.endswith('.txt')]
        
        
        if len(csv_files)!=0:
            self.data_files = csv_files
            dpg.configure_item('ROIfile_box',items=self.data_files)
            self.source_type = 'csv'
    
    
                
    
        elif len(dat_files)!=0:
            self.data_files = dat_files
            dpg.configure_item('ROIfile_box',items=self.data_files)
            self.source_type = 'txt'
    
    
    
        else:
            pass
        
        dpg.configure_item('ROITarget_file_dialog',default_path=self._path)
        
    def callback_open_target_folder(self,sender,app_data):
        
        path = app_data['file_path_name']
        
        dpg.set_value('tag_target_path',app_data['file_path_name'])
        

    def callback_empty(self,sender,app_data):
        '''Empty function. Do nothing.'''
        pass

    def callback_no_files_dialog_close_only(self,sender,app_data):
        dpg.configure_item('No_data_files',show=False)
        dpg.delete_item('no_files_error_text')
        dpg.delete_item('no_files_error_butt')
        dpg.delete_item('No_data_files')
    
    def show_error_no_files(self,error_text):

        size_ratio = {'width':dpg.get_viewport_width()/self.viewport['width'],
                      'height':dpg.get_viewport_height()/self.viewport['height']}
        win_width = 200*size_ratio['width'] 
        win_height = 80*size_ratio['height'] 
        win_pos = (int(dpg.get_item_pos('rewrite_window')[0])+int(dpg.get_item_width('rewrite_window')/2)-int(win_width/2),
                   int(dpg.get_item_pos('rewrite_window')[1])+int(dpg.get_item_height('rewrite_window')/2)-int(win_height/2))
        
        try:
            with dpg.window(
                            label='Error!',
                            tag='No_data_files',
                            width=win_width,
                            height=win_height,
                            pos = win_pos,
                            no_move=False,
                            no_close=False,
                            no_title_bar=False,
                            no_scrollbar=True,
                            no_resize=False,
                            on_close=self.callback_no_files_dialog_close_only,
                            show=True,
                            modal=True
                            ):
                dpg.add_text(error_text,tag='no_files_error_text')
                
    
                dpg.add_button(label='Close',
                               tag='no_files_error_butt',
                               show=True,
                               callback=self.callback_no_files_dialog_close_only
                              )
                
                dpg.bind_item_theme('No_data_files', 'Error_window_theme')
        except:
            dpg.show_item('No_data_files')
    
    
    def show_done(self,error_text):

        size_ratio = {'width':dpg.get_viewport_width()/self.viewport['width'],
                      'height':dpg.get_viewport_height()/self.viewport['height']}
        win_width = 50*size_ratio['width'] 
        win_height = 80*size_ratio['height'] 
        win_pos = (int(dpg.get_item_pos('rewrite_window')[0])+int(dpg.get_item_width('rewrite_window')/2)-int(win_width/2),
                   int(dpg.get_item_pos('rewrite_window')[1])+int(dpg.get_item_height('rewrite_window')/2)-int(win_height/2))
        
        try:
            with dpg.window(
                            label='',
                            tag='No_data_files',
                            width=win_width,
                            height=win_height,
                            pos = win_pos,
                            no_move=False,
                            no_close=False,
                            no_title_bar=False,
                            no_scrollbar=True,
                            no_resize=False,
                            on_close = self.callback_no_files_dialog_close_only,
                            show=True,
                            modal=True
                            ):
                dpg.add_text(error_text,tag='no_files_error_text')
                
    
                dpg.add_button(label='Close',
                               tag='no_files_error_butt',
                               show=True,
                               callback=self.callback_no_files_dialog_close_only
                              )
                
                dpg.bind_item_theme('No_data_files', 'Error_window_theme')
        except:
            dpg.show_item('No_data_files')


    def callback_proceed_ROI(self,sender,app_data):
        
        
        
        try:
            width = int(dpg.get_value('add_text_width'))
        except:
            width = 'dupa'
        try:
            height = int(dpg.get_value('add_text_height'))
        except:
            height = 'dupa'
        if isinstance(width, int) and isinstance(height, int):
            
            resolution = (int(dpg.get_value('add_text_width')),int(dpg.get_value('add_text_height')))
            if len(self.data_files) == 0:
                self.show_error_no_files('No files selected')
            else:
                input_folder = dpg.get_value('tag_source_path')
                ROI_folder = dpg.get_value('tag_target_path')
                if input_folder != '':
                    if ROI_folder != '':
                        error = False
                        for file in self.data_files:
    
                            dpg.configure_item('ROIfile_box',default_value=file)
        
        
                            if self.source_type == 'csv':
                                self.rewrtie_roi_csv(file,input_folder,ROI_folder,resolution)
    
                            elif self.source_type == 'txt':
                                self.rewrtie_roi_txt(file,input_folder,ROI_folder,resolution)
                            else:
                                
                                error = True
                        if error == True:
                            self.show_error_no_files('Something gone wrong!')
                        else:
                            self.show_done('DONE')
                    else:
                        self.show_error_no_files('Select target folder!')
                else:
                    self.show_error_no_files('Select source folder!')
                    
            
            
        else:
            self.show_error_no_files('Wrong resolution')



    def rewrtie_roi_csv(self,file,input_folder,output_roi_path,shape):
        infile = os.path.join(input_folder,file)
        df = pd.read_csv(infile)
        
        new_file = file.replace('.csv','.tmp')
        final_roi = new_file.split('/')[-1]
        zeros = np.zeros(shape)
        zeros = pd.DataFrame(zeros)
        if df.columns[1].startswith('X'): 
            for col in df.columns:
                if col.startswith('X'):
                    zero_column = int(col.replace('X',''))
                    for i in df.index:
                        zero_row = int(df.at[i,' '].replace('Y',''))
                        zero_value = df.at[i,col]
                        if zero_value !=0: 
                            zero_value=(zero_value/zero_value)*255
                        else:
                            pass
                        zeros.at[zero_row,zero_column]=zero_value
        else:
            for col in df.columns:
                if col.startswith('X'):
                    zero_column = int(col.replace('X',''))
                    for i in df.index:
                        zero_row = int(df.at[i,' .1'].replace('Y',''))
                        zero_value = df.at[i,col]
                        if zero_value !=0: 
                            zero_value=(zero_value/zero_value)*255
                        else:
                            pass
                        zeros.at[zero_row,zero_column]=zero_value
        zeros=zeros.astype(int)
        zeros = zeros.where(zeros!=0,'-')
        zeros.to_csv(new_file, sep = '\t',index=False,header=False)        
        
        roi_file = final_roi
        
        nf = file.replace('.csv', '.dat')
        output_roi_file = os.path.join(output_roi_path,nf)
        f = open(output_roi_file, "w")
        f.write("Events[Cnts]\n")
        f.write("(x0 | y0) = (0.000[ m] | 0.000[ m])\n")
        f.write("(x1 | y1) = (51.200[ m] | 51.200[ m])\n")
        f.close()
        with open(new_file) as reader:
            red_file = reader.read()
            reader.close()
        f = open(output_roi_file, "a")
        f.write(red_file)
        f.close()
        tmp_files = os.listdir()
        tmp_files = [f for f in tmp_files if f.endswith('.tmp')]
        for tmp in tmp_files:
            os.remove(tmp)
        
        
    def rewrtie_roi_txt(self,file,input_folder,output_roi_path,shape):
        infile = os.path.join(input_folder,file)
        df = pd.read_csv(infile,sep='\t',header=None)
        new_file = file.replace('.txt','.tmp')
        df=df.astype(int)
        df = df.where(df!=0,'-')
        df.to_csv(new_file, sep = '\t',index=False,header=False)
        nf = file.replace('.txt', '.dat')
        output_roi_file = os.path.join(output_roi_path,nf)
        f = open(output_roi_file, "w")
        f.write("Events[Cnts]\n")
        f.write("(x0 | y0) = (0.000[ m] | 0.000[ m])\n")
        f.write("(x1 | y1) = (51.200[ m] | 51.200[ m])\n")
        f.close()
        with open(new_file) as reader:
            red_file = reader.read()
            reader.close()
        f = open(output_roi_file, "a")
        f.write(red_file)
        f.close()
        tmp_files = os.listdir()
        tmp_files = [f for f in tmp_files if f.endswith('.tmp')]
        for tmp in tmp_files:
            os.remove(tmp)