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

import os
import numpy as np
from numpy import log10#, sqrt, exp, log, pi
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
    _VERSION_RE = re.compile(r"^\s*(\d+)\.(\d+)\.(\d+)([A-Za-z])?\s*$")
    
    def __init__(self, hsv,version: str):
        """
        :param version: lokalna wersja programu, np. '1.1.0' lub '1.1.0a'
        """
        self.VERSION = version
        self.version = version.strip()
        self.updater_state = False
        self.hsv = hsv

        self.owner="TKmist"          # np. "psf"
        self.repo="smICA"         # np. "requests"
        self.branch="many_cells_auto_roi"      # dowolna gałąź
        self.path="VERSION" 

    # --- Prywatne metody pomocnicze ---

    def _parse_version(self, ver: str):
        """
        Parsuje wersję w formacie 1.2.3 lub 1.2.3a
        Litery: a > b > c > ... (czyli 'a' to najnowsza)
        """
        m = self._VERSION_RE.match(ver)
        if not m:
            raise ValueError(f"Nieprawidłowy format wersji: {ver!r}. Oczekiwano np. '1.2.3' lub '1.2.3a'.")

        major, minor, patch = map(int, m.groups()[:3])
        suffix = m.group(4)

        if suffix:
            s = suffix.lower()
            if not ('a' <= s <= 'z'):
                raise ValueError(f"Niedozwolony sufiks wersji: {suffix!r}")
            # a > b > ... => 'a' ma najwyższy priorytet
            suffix_rank = 26 - (ord(s) - ord('a'))
        else:
            suffix_rank = 0  # brak litery = najniższy priorytet

        return (major, minor, patch, suffix_rank)

    def _raw_version_url(self, owner: str, repo: str, branch: str, path: str = "VERSION") -> str:
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

    # --- Publiczna metoda ---

    def check_remote_version(
        self,
        owner: str,
        repo: str,
        branch: str,
        *,
        path: str = "VERSION",
        token: str | None = None,
        timeout: float = 10.0
    ) -> tuple[bool, str | None]:
        """
        Sprawdza, czy wersja na GitHubie (w pliku VERSION w danej gałęzi)
        jest nowsza niż lokalna self.version.

        :param owner: właściciel repozytorium GitHub
        :param repo: nazwa repozytorium
        :param branch: gałąź (np. 'develop', 'release/2.0')
        :param path: ścieżka do pliku z wersją (domyślnie 'VERSION')
        :param token: opcjonalny GitHub token dla repo prywatnych
        :param timeout: limit czasu dla requestu HTTP
        :return: (is_newer, remote_version)
        """
        url = self._raw_version_url(owner, repo, branch, path)
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code != 200:
                print(f"[Updater] Błąd pobierania VERSION z {url} ({resp.status_code})")
                return (False, None)
            remote_txt = resp.text.strip()
        except requests.RequestException as e:
            print(f"[Updater] Błąd sieci: {e}")
            return (False, None)

        try:
            remote_tuple = self._parse_version(remote_txt)
            local_tuple = self._parse_version(self.version)
        except ValueError as e:
            print(f"[Updater] Błąd parsowania wersji: {e}")
            return (False, remote_txt)

        is_newer = remote_tuple > local_tuple
        return (is_newer, remote_txt)
    def proceed_update_window(self):
        window_width,window_height = 400,400
        viewport_width, viewport_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        pos_x = (viewport_width - window_width) // 2
        pos_y = (viewport_height - window_height) // 2
        try:
            with dpg.window(pos=(pos_x, pos_y),
                            label='Update now?',
                            tag='proceed_to_update_window',

                            no_move=True,
                            no_close=False,
                            no_title_bar=False,
                            # no_resize=True,
                            show=True,
                            modal=True,
                            autosize=True,
                            no_scrollbar=True
                            ):
                dpg.add_text('Press ok to install the files and close the program.', tag='proceed_to_update_window_text')
                dpg.bind_item_font('proceed_to_update_window_text','DejaVu_bold')
                with dpg.group(tag='proceed_to_update_window_group',horizontal=True):
                    dpg.add_button(label='OK',
                                   tag='proceed_to_update_window_ok_butt',
                                   show=True,
                                   callback=self.proceed_window_OK
                                   )
                    
                    dpg.add_button(label='Close',
                                   tag='proceed_to_update_window_close_butt',
                                   show=True,
                                   callback=self.proceed_window_close
                                   )
                
                dpg.bind_item_theme('proceed_to_update_window_ok_butt', 'fit_button_theme')
                dpg.bind_item_theme('proceed_to_update_window_close_butt', 'Error_window_theme')
                
        except:
            dpg.show_item('No_data_files')

    

    def proceed_window_close(self):
        dpg.configure_item('proceed_to_update_window', show=False)
        dpg.delete_item('proceed_to_update_window_text')
        dpg.delete_item('proceed_to_update_window_ok_butt')
        dpg.delete_item('proceed_to_update_window_close_butt')
        dpg.delete_item('proceed_to_update_window_group')
        dpg.delete_item('proceed_to_update_window')

    def proceed_window_OK(self):
        # print('proceed_window_OK')
        window_size = dpg.get_item_rect_size("proceed_to_update_window")
        
        
        dpg.delete_item('proceed_to_update_window_ok_butt')
        dpg.delete_item('proceed_to_update_window_close_butt')
        dpg.delete_item('proceed_to_update_window_group')
        
        dpg.add_loading_indicator(parent='proceed_to_update_window',width=50,
                                  tag = 'tag_load_ind_update',
                                  pos=(dpg.get_item_width('proceed_to_update_window')/2-(int(dpg.get_global_font_scale()*25)),1*dpg.get_item_height('proceed_to_update_window')-dpg.get_global_font_scale()*25),
                                 color=self.hsv(2/7.0, 0.6, 0.6),
                                 secondary_color = self.hsv(0.223, 0.404, 0.846),)
        dpg.add_button(label='',
                                   tag='progress_button',
                                   show=True,
                                   pos=(0,1*dpg.get_item_height('proceed_to_update_window')+dpg.get_global_font_scale()*50),
                                   # callback=self.proceed_window_close
                                   parent = 'proceed_to_update_window',
                       width = window_size[0]
                                   )
        # print(dpg.get_item_width('tag_load_ind_update'))
        dpg.bind_item_theme('progress_button', 'transparent_theme')
        dpg.set_item_label('progress_button','Downloading files')
        
        self.download_update(owner=self.owner,repo=self.repo, branch=self.branch)
        self.backup_old_files()
        
        self.Copying_new_files()
        # time.sleep(0.5)
        for i in range(3, -1, -1):
            
            dpg.set_item_label('progress_button','Finished. smICA closes in: '+str(i)+ ' sec.')
            time.sleep(1)
        dpg.delete_item('progress_button')
        dpg.delete_item('tag_load_ind_update')
        
        
        self.proceed_window_close()
        
        dpg.delete_item('proceed_to_update_window')
        dpg.stop_dearpygui()
        
    def backup_old_files(self):
        current_dir = os.path.abspath(os.getcwd())
        # print(f"[Updater] Aktualny katalog: {current_dir}")
        bckp_dir = os.path.join(current_dir,'..' ,"old_backup")
        # print(f"[Updater] Aktualny katalog: {bckp_dir}")
        if os.path.exists(bckp_dir):
                print("[Updater] Usuwam stary katalog backup...")
                dpg.set_item_label('progress_button','Removing old backup files')
                shutil.rmtree(bckp_dir, ignore_errors=True)
        os.makedirs(bckp_dir, exist_ok=True)
        metafiles = ['LICENSE','README.md','VERSION']
        FoldersToBackup = ['REWRITE_ROI','smICA']
        # time.sleep(1.5)
        for f in metafiles:
            print("[Updater] Usuwam stary katalog backup...")
            dpg.set_item_label('progress_button','Backing up meta files')
            source = os.path.join(current_dir,'..' ,f)
            target = os.path.join(bckp_dir ,f)
            # print(source)
            # print(target)
            shutil.copy2(source,target)
        # time.sleep(1.5)
        for d in FoldersToBackup:
            dpg.set_item_label('progress_button','Backing up software directories')
            source = os.path.join(current_dir,'..' ,d)
            target = os.path.join(bckp_dir ,d)
            # print(source)
            # print(target)
            shutil.copytree(
                source,
                target,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("*updt_tmp", "__pycache__",'.ipynb_checkpoints')
                )
    def Copying_new_files(self):
        current_dir = os.path.abspath(os.getcwd())
        tmp_dir = os.path.join(current_dir,'..', "updt_tmp")
        zip = os.listdir(tmp_dir)
        zip = [f for f in zip if f.endswith('.zip')][0]
        print(zip)
        dpg.set_item_label('progress_button','unzipping update')
        zip_path = os.path.join(tmp_dir,zip)
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(tmp_dir)
        except zipfile.BadZipFile:
            # print("[Updater] Błąd: uszkodzone archiwum ZIP.")
            return None
        subfolders = [d for d in os.listdir(tmp_dir) if os.path.isdir(os.path.join(tmp_dir,d))]
        print(subfolders)
        
        if not subfolders:
            # print("[Updater] Brak rozpakowanego katalogu w archiwum!")
            return None
        
        extracted_dir = subfolders[0]
        updt_dir = os.path.join(tmp_dir,extracted_dir)
        # print(f"[Updater] Aktualizacja pobrana do: {updt_dir}")
        metafiles = ['LICENSE','README.md','VERSION']
        for f in metafiles:
            print("[Updater] Usuwam stary katalog backup...")
            dpg.set_item_label('progress_button','Updating meta files')
            source = os.path.join(updt_dir,f)
            target = os.path.join(current_dir ,'..' ,f)
            # print(source)
            # print(target)
            shutil.copy(source,target)
        FoldersToBackup = ['REWRITE_ROI','smICA']
        for d in FoldersToBackup:
            dpg.set_item_label('progress_button','Updating software directories')
            source = os.path.join(updt_dir,'src' ,d)
            target = os.path.join(current_dir,'..' ,d)
            # print(source)
            # print(target)
            shutil.copytree(
                source,
                target,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("*updt_tmp", "__pycache__",'.ipynb_checkpoints')
                )
        dpg.set_item_label('progress_button','Removing temporary files')
        shutil.rmtree(tmp_dir, ignore_errors=True)
        
        
        
    def download_update(
            self,
            owner: str,
            repo: str,
            branch: str,
            *,
            token: str | None = None,
            timeout: float = 30.0
        ) -> str | None:
            """
            Pobiera aktualne pliki programu w formie ZIP-a z repozytorium GitHub
            i zapisuje w katalogu tymczasowym 'updt_tmp'.
    
            :param owner: właściciel repozytorium GitHub
            :param repo: nazwa repozytorium
            :param branch: gałąź (np. 'develop', 'main')
            :param token: opcjonalny GitHub token (dla repo prywatnych)
            :param timeout: czas oczekiwania w sekundach
            :return: ścieżka do katalogu tymczasowego z rozpakowanymi plikami, lub None jeśli błąd
            """
    
            # 1️⃣ Bieżąca ścieżka programu
            current_dir = os.path.abspath(os.getcwd())
            # print(f"[Updater] Aktualny katalog: {current_dir}")
    
            # 2️⃣ Katalog tymczasowy
            tmp_dir = os.path.join(current_dir,'..', "updt_tmp")
            if os.path.exists(tmp_dir):
                # print("[Updater] Usuwam stary katalog tymczasowy...")
                shutil.rmtree(tmp_dir, ignore_errors=True)
            os.makedirs(tmp_dir, exist_ok=True)
    
            # 3️⃣ Pobranie archiwum ZIP
            zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
            headers = {}
            if token:
                headers["Authorization"] = f"token {token}"
    
            zip_path = os.path.join(tmp_dir, f"{repo}-{branch}.zip")
            # print(f"[Updater] Pobieram ZIP z {zip_url} -> {zip_path}")
    
            try:
                with requests.get(zip_url, headers=headers, timeout=timeout, stream=True) as r:
                    r.raise_for_status()
                    with open(zip_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
            except requests.RequestException as e:
                # print(f"[Updater] Błąd pobierania: {e}")
                return None
    

    
    def run_updater(self):
        
        is_newer, remote = self.check_remote_version(
            owner=self.owner,          # np. "psf"
            repo=self.repo,          # np. "requests"
            branch=self.branch,      # dowolna gałąź
            path=self.path         # nazwa pliku w repo
        )
        theme_tag = dpg.get_item_theme('menu_about_dropout')
        # print('theme:',theme_tag)
        
        if is_newer:
            self.updater_state = True
            # print(f"🟢 Dostępna nowa wersja: {remote} (lokalna: {self.version})")

            
            
            dpg.bind_item_theme("menu_about_dropout", "menu_update_available")
            children = dpg.get_item_children("menu_about_dropout", 1)  # slot 1 = normalne dzieci
            # print(children)

            
            for child in children:
                # print(child)
                if str(child).isdigit():
                    # print(dpg.get_item_alias(child))
                    child = dpg.get_item_alias(child)
                else:
                    pass
                # print()
                if child == "menu_Version_dropout_item":
                    # print(child,'menu_update_available')
                    dpg.bind_item_theme(child, "menu_update_available")
                    
                    # dpg.add_menu_item(label='Version: '+self.VERSION,enabled=False,tag=child)
                    # dpg.add_menu_item(label='Version: '+self.VERSION,enabled=False,tag=child)
                    
                    # print(child)
                    dpg.set_item_label(child,label='Current version: '+self.VERSION+' !')
                    dpg.bind_item_font(child,'DejaVu_bold')
                    dpg.add_menu_item(label='New version: '+remote+ ' available, click to update now',
                                      enabled=True,
                                      tag='menu_Version_dropout_item_new',
                                      parent='menu_about_dropout',
                                      callback = self.proceed_update_window)
                    dpg.bind_item_theme('menu_Version_dropout_item_new', "menu_update_available_new")
                    dpg.bind_item_font('menu_Version_dropout_item_new','DejaVu_bold')
                    
                else:
                    print(child,'menu_normal')
                    dpg.bind_item_theme(child, "menu_normal")
                    # dpg.bind_item_font(child,'DejaVu')
                    
            # dpg.bind_item_theme("menu_License_dropout_item", 'update_available')
            # print("Menu theme:", dpg.get_item_alias(dpg.get_item_theme("menu_about_dropout")))
            # print("License theme:", dpg.get_item_alias(dpg.get_item_theme("menu_License_dropout_item")))
            # print("Version theme:", dpg.get_item_alias(dpg.get_item_theme("menu_Version_dropout_item")))

            
        else:
            self.updater_state = False
            # print(f"🔵 Brak aktualizacji. Najnowsza wersja to {remote}.")
    


class _basicF:
    
    
    def __init__(self):
        pass
    
    
    
    def lnprint(self,*args, **kwargs):
     # Get the current frame's caller information (go one level up)
        caller_frame = inspect.currentframe().f_back
        line_number = caller_frame.f_lineno
        # Get the filename of the script
        file_name = caller_frame.f_code.co_filename
        function_name = caller_frame.f_code.co_name
        # Print the line number and filename first
        print(f"File {file_name}, Function '{function_name}', Line {line_number}: ", end="\n")

        # Pass all arguments and keyword arguments to the built-in print function
        print(*args, **kwargs)
    @staticmethod
    def some_fail():
        caller_frame = inspect.currentframe().f_back
        line_number = caller_frame.f_lineno
        # Get the filename of the script
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
                # default_font = font_18
            dpg.bind_font(default_font)
        

    def remove_font_from_registry(self):
        font = 'DejaVu'
        dpg.delete_item(font)
        dpg.delete_item('Font_registry')
        
    def _hsv_to_rgb(self,h, s, v):
        '''Funtion converts HSV color notation to the RGB values'''
        if s == 0.0: return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
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
        # print(met_files)
        met_files = [f for f in met_files if f.endswith('_config.json')]
        # print(met_files,met_files[0],type(met_files[0]))
        met_file = met_files[0]
        path = os.path.join(method_dir,met_file)

        with open(path) as json_settings:
            method_tree = json.load(json_settings)

        return method_tree['ANAL_MENU_ITEM']

    def method_config_dict(self,method_dir):
        met_files = os.listdir(method_dir)
        
            
            
        
        met_files = [ self.ifso(f) for f in met_files]
        met_files = [str(f) for f in met_files if str(f).endswith('_config.json')]
        # print(met_files)
        met_file = met_files[0]
        # print('met_file',met_file)
        path = os.path.join(method_dir,met_file)
        # print('path',path)
        with open(path) as json_settings:
            method_tree = json.load(json_settings)

        return method_tree
    
    
    def path_to_method_anal_layout(self,method_dir):
        # print('method_dir',method_dir)
        met_files = os.listdir(method_dir)
        # print(met_files)
        
            
            
        
        met_files = [ self.ifso(f) for f in met_files]
        # print(met_files,met_files[0],type(met_files[0]))
        met_files = [f for f in met_files if f.endswith('_config.json')]
        # print(met_files)
        # print(met_files,met_files[0],type(met_files[0]))
        met_file = met_files[0]
        # print('met_file',met_file)
        path = os.path.join(method_dir,met_file)
        # print('path',path)
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
            # print('EXTRACT_FROM_PTU_INIT_BUTTON')
            self.PE_manu_F.callback_PHOTEXTR_menu()  
            # 

        elif sender == 'Phot_2_Conc_INIT_BUTTON':
            # print('Phot_2_Conc_INIT_BUTTON')
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
        
    def basic_resizer(self):
        self.unmount_inint_buttons()
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
            dpg.bind_item_theme('EXTRACT_FROM_PTU_INIT_BUTTON', 'fit_button_theme')
            dpg.add_button(label="Phot 2 Conc",
                       callback=self.callback_init_buttons,
                       width = Phot_2_Conc_INIT_BUTTON['width'],
                       height = Phot_2_Conc_INIT_BUTTON['height'],
                       tag='Phot_2_Conc_INIT_BUTTON',
                       show=True,enabled=True
                      )
            dpg.bind_item_theme('Phot_2_Conc_INIT_BUTTON', 'fit_button_theme')
        
    
    
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
            #self.init_bottom_indent = 2*11
            #self.init_right_indent = 2*11
        return ico_path

class _init_Menu:
    def __init__(self,upd_st,VERSION):
        self.VERSION = VERSION

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
            # with dpg.menu(label="Settings",tag='menu_settings_dropout'):
                
            #     dpg.add_menu_item(label="Full Screen (F11)",tag='fullscreenclick',callback=self.callback_full_screen)

            with dpg.menu(label="About",tag='menu_about_dropout'):
                # dpg.add_menu_item(label="Help (F1)",tag='helpclick',callback=self.callback_help)
                dpg.add_menu_item(label="Help",tag='helpclick',callback=self.callback_help)
                dpg.add_menu_item(label='License',callback = self.callback_license,tag='menu_License_dropout_item')
               
                dpg.add_menu_item(label='Version: '+self.VERSION,enabled=False,tag='menu_Version_dropout_item')
                    
                
            dpg.bind_item_theme('menu_about_dropout', "menu_normal")


class _common_VARIABLES:
    def __init__(self):
        self.windows = []
        self.items = []
        self.last_directory = 'samples'
        self.directory = ''