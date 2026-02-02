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
import os
import json
import pandas as pd
import numpy as np
from numpy import log10, sqrt, exp, log, pi
import time
import pickle
import cv2
from Required.Third_party.readPTU_FLIM import PTUreader
from numpy.linalg import inv, det,cond,pinv


import Required.INIT as inits

bf = inits._basicF()

lprint = bf.lnprint
###############################################################################
###############################################################################
''' Inits'''
###############################################################################
###############################################################################



class _PhotExtr_init:
    
    
    def __init__(self,
                 size_ratio,
                 left_indent,
                 internal_indent,
                 right_indent,
                 bottom_indent,
                 top_indent,
                 group_spacer,
                 font_size,
                 last_directory,
                 GI
                ):
        '''General variables'''
        self.last_directory = last_directory
   
        
        
        
        
        '''Layout variables'''
        self.size_ratio = size_ratio
        self.left_indent = int(left_indent*self.size_ratio['width'])
        self.internal_indent = int(internal_indent*self.size_ratio['width'])
        self.right_indent = int(right_indent*self.size_ratio['width'])
        self.bottom_indent = int(bottom_indent*self.size_ratio['width'])
        self.top_indent = int(top_indent*self.size_ratio['width'])
        self.group_spacer = int(group_spacer*self.size_ratio['width'])
        self.fnt_ratio = (self.size_ratio['width']+self.size_ratio['height'])/2
        self.font_size = int(np.round(font_size*self.fnt_ratio,0))
        self.drag_line_thickness = int(3.*self.size_ratio['width'])
        self.files =[]
        self.GI=GI

        
        dpg.set_global_font_scale(self.fnt_ratio)
        
        self.plot_window_ch1 = {'name':'plot_window_ch1',
                                'width':int(((3*dpg.get_viewport_width()/4)-self.left_indent-2*self.internal_indent)/2),
                                'height':int(dpg.get_viewport_height()-self.top_indent-self.bottom_indent),
                                'pos':(self.left_indent,self.top_indent)
                               }
        self.plot_window_ch2 = {'name':'plot_window_ch2',
                                'width':self.plot_window_ch1['width'],
                                'height':self.plot_window_ch1['height'],
                                'pos':(self.plot_window_ch1['pos'][0]+self.plot_window_ch1['width']+self.internal_indent,self.top_indent)
                               }
        self.Options = {'name':'Options',
                        'width':dpg.get_viewport_width()-(self.plot_window_ch2['pos'][0]+self.plot_window_ch2['width']+self.internal_indent+self.right_indent),
                        
                            'height':int(120*self.size_ratio['height']),
                            'pos':(self.plot_window_ch2['pos'][0]+self.plot_window_ch2['width']+self.internal_indent,self.top_indent)
                            }

        self.Files_window = {'name':'Files_window',
                            'width':self.Options['width'],
                        
                            'height':int(dpg.get_viewport_height()-self.Options['pos'][1]-self.Options['height']-self.internal_indent-self.bottom_indent),
                            'pos':(self.Options['pos'][0],self.Options['pos'][1]+self.Options['height']+self.internal_indent)
                            }
       
        self.Open_file_dialog = {'name':'Open_file_dialog',
                            'width':int(1000*self.size_ratio['width']),
                            'height':int(800*self.size_ratio['height'])
                                }
        self.PTU_dir_dialog = {'name':'PTU_dir_dialog',
                            'width':int(1000*self.size_ratio['width']),
                            'height':int(800*self.size_ratio['height']),
                              }

        self.BG_removal_window = {'name':'BG_removal_window',
                            'width':int(1350*self.size_ratio['width']),
                            'height':int(800*self.size_ratio['height']),
                            'pos':(self.left_indent,int(dpg.get_viewport_height()/2-800*self.size_ratio['height']/2))
                            }

        self.plt_1_ch_1 = {'name':'plt_1_ch_1',
                           'width':-1,
                            'height':int(300*self.size_ratio['width']),
                            }
        
        self.L_dline_ch1 = {'name':'L_dline_ch1',
                            'thickness':self.drag_line_thickness,
                            'color':[255, 100, 0, 255],
                            'default_value': 0.0,
                            }
        self.U_dline_ch1 = {'name':'U_dline_ch1',
                            'thickness':self.drag_line_thickness,
                            'color':[255, 0, 100, 255],
                            'default_value': 1.0,
                            }
        self.plt_2_ch_1 = {'name':'plt_2_ch_1',
                           'width':-1,
                            'height':int(300*self.size_ratio['width']),
                            }
        self.LIMITS_ch_1_table_col1 = {'name':'LIMITS_ch_1_table_col1',
                            'width':int(self.plot_window_ch1['width']/3)
                                 }
        self.LIMITS_ch_1_table_col2 = {'name':'LIMITS_ch_1_table_col2',
                            'width':int(self.plot_window_ch1['width']/3)
                                 }
        self.LIMITS_ch_1_table_col3 = {'name':'LIMITS_ch_1_table_col3',
                            'width':int(self.plot_window_ch1['width']/3)
                                 }

        self.bottom_limit_ch1 = {'name':'bottom_limit_ch1',
                            'width':-1
                                 }
        self.upper_limit_ch1 = {'name':'upper_limit_ch1',
                            'width':-1
                                 }
        self.reset_button_ch1 = {'name':'reset_button_ch1',
                            'width':-1
                                 }
        self.Remove_bgd_butt_ch_1 = {'name':'Remove_bgd_butt_ch_1',
                            'width':-1
                                 }
        self.filters_ch_1_tab_list_tag = {'name':'filters_ch_1_tab_list_tag',
                            'width':-1,
                            'height':int(120*self.size_ratio['height'])
                                 }

        self.plt_1_ch_2 = {'name':'plt_1_ch_2',
                           'width':-1,
                            'height':int(300*self.size_ratio['width']),
                            }
        
        self.L_dline_ch2 = {'name':'L_dline_ch2',
                            'thickness':self.drag_line_thickness,
                            'color':[255, 100, 0, 255],
                            'default_value': 0.0,
                            }
        self.U_dline_ch2 = {'name':'U_dline_ch2',
                            'thickness':self.drag_line_thickness,
                            'color':[255, 0, 100, 255],
                            'default_value': 1.0,
                            }
        self.plt_2_ch_2 = {'name':'plt_2_ch_2',
                           'width':-1,
                            'height':int(300*self.size_ratio['width']),
                            }
        self.LIMITS_ch_2_table_col1 = {'name':'LIMITS_ch_2_table_col1',
                            'width':int(self.plot_window_ch2['width']/3)
                                 }
        self.LIMITS_ch_2_table_col2 = {'name':'LIMITS_ch_2_table_col2',
                            'width':int(self.plot_window_ch2['width']/3)
                                 }
        self.LIMITS_ch_2_table_col3 = {'name':'LIMITS_ch_2_table_col3',
                            'width':int(self.plot_window_ch2['width']/3)
                                 }

        self.bottom_limit_ch2 = {'name':'bottom_limit_ch2',
                            'width':-1
                                 }
        self.upper_limit_ch2 = {'name':'upper_limit_ch2',
                            'width':-1
                                 }
        self.reset_button_ch2 = {'name':'reset_button_ch2',
                            'width':-1
                                 }
        self.Remove_bgd_butt_ch_2 = {'name':'Remove_bgd_butt_ch_2',
                            'width':-1
                                 }
        self.filters_ch_2_tab_list_tag = {'name':'filters_ch_2_tab_list_tag',
                            'width':-1,
                            'height':int(120*self.size_ratio['height'])
                                 }

        self.file_box = {'name':'file_box',
                         'width':-1,
                         'lines':int(22*self.size_ratio['height'])
                                 }
        self.apply_to_file = {'name':'apply_to_file',
                            'width':-1
                                 }
        self.apply_to_all = {'name':'apply_to_all',
                            'width':-1
                                 }
        self.decays_tab_list_tag = {'name':'decays_tab_list_tag',
                         'width':self.file_box['width'],
                         'height':int(215*self.size_ratio['height'])
                                   }
        
        self.Add_decay_to_lib = {'name':'Add_decay_to_lib',
                            'width':int(174*self.size_ratio['width'])
                                 }
        self.Add_decay_from_lib = {'name':'Add_decay_from_lib',
                            'width':int(174*self.size_ratio['width'])
                                 }
        self.Calculate_filters = {'name':'Calculate_filters',
                            'width':int(350*self.size_ratio['width']),
                            'height':int(25*self.size_ratio['height'])
                                 }

        self.decays_tab_list_tag = {'name':'decays_tab_list_tag',
                         'width':int(482*self.size_ratio['width']),
                         'height':int(300*self.size_ratio['height'])
                         
                                 }
        self.fltr_plot = {'name':'fltr_plot',
                         'width':int(482*self.size_ratio['width']),
                         'height':int(300*self.size_ratio['height'])
                         
                                 }
        
        self.Background_level_line = {'name':'Background_level_line',
                                      'thickness':self.drag_line_thickness,
                            'color':[100, 255, 100, 255],
                            'default_value': 0.0,
                            }
        self.Background_RLL_line = {'name':'Background_RLL_line',
                                    'thickness':self.drag_line_thickness,
                            'color':[100, 255, 100, 255],
                            'default_value': 0.0,
                            }
        self.Background_RUL_line = {'name':'Background_RUL_line',
                                    'thickness':self.drag_line_thickness,
                            'color':[100, 190, 100, 255],
                            'default_value': 0.0,
                            }
        self.fltr_filters_plot = {'name':'fltr_filters_plot',
                         'width':int(482*self.size_ratio['width']),
                         'height':int(300*self.size_ratio['height'])
                         
                                 }
        self.Decline_filters = {'name':'Decline_filters',
                            'width':int(174*self.size_ratio['width'])
                                 }
        self.Accept_filters = {'name':'Accept_filters',
                            'width':int(174*self.size_ratio['width'])
                                 }
        self.get_name = {'name':'get_name',
                            'width':int(350*self.size_ratio['width'])
                                 }
        self.get_wavelength = {'name':'get_wavelength',
                            'width':int(100*self.size_ratio['width'])
                                 }
        self.Cancel_decay_submission = {'name':'Cancel_decay_submission',
                            'width':int(116*self.size_ratio['width'])
                                 }
        self.Proceed_decay_submission = {'name':'Proceed_decay_submission',
                            'width':int(116*self.size_ratio['width'])
                                 }
        self.get_decay_description = {'name':'get_decay_description',
                            'width':int(482*self.size_ratio['width'])
                                 }
        self.decays_tab_lib_list_tag = {'name':'decays_tab_lib_list_tag',
                         'width':int((350+482)*self.size_ratio['width']+self.group_spacer*5),
                         'height':int(150*self.size_ratio['height'])
                         
                                 }
        self.Cancel_library_import = {'name':'Cancel_library_import',
                            'width':int(116*self.size_ratio['width'])
                                 }
        self.Proceed_library_import = {'name':'Proceed_library_import',
                            'width':int(116*self.size_ratio['width'])
                                 }
        self.OK_button = {'name':'OK_button',
                            'width':int(116*self.size_ratio['width'])
                                 }

        self.load_ind_win = {'name':'load_ind_win',
                            'width':int(450*self.size_ratio['width']),
                            'height':int(250*self.size_ratio['width']),
                            'pos':(int(dpg.get_viewport_width()/2-int(450*self.size_ratio['width'])/2),
                                   int(dpg.get_viewport_height()/2-int(250*self.size_ratio['width'])/2))
                            }
        self.loading_title = {'name':'loading_title',
                            'width':self.load_ind_win['width']
                                 }
        self.loading_butt = {'name':'loading_butt',
                            'width':self.load_ind_win['width']
                                 }
        self.loading_status = {'name':'loading_status',
                            'width':self.load_ind_win['width']
                                 }
        self.loading_cnt_butt = {'name':'loading_cnt_butt',
                            'width':self.load_ind_win['width']
                                 }
        self.loading_status_text = {'name':'loading_status_text',
                            'width':self.load_ind_win['width']
                                 }
        


                                 
###############################################################################
###############################################################################
''' Variables'''
###############################################################################
###############################################################################

class _PhotExtr_vars_funct:
    def __init__(self,
                 INIT,
                last_directory,
                 basf,
                 _globalITEMS):
        self.mode_init=INIT
        self.GI = self.mode_init.GI
        self.files=self.mode_init.files
        self.basf=basf
        self.last_directory = last_directory
        self.size_ratio = self.mode_init.size_ratio 
        self.sindatax1 = []
        self.sindatay1 = []

        self.sindatax2 = []
        self.sindatay2 = []
        self.anal_file = ''
        self.fl_bg_curves_dict = {}
        self.tchanx1 = []
        self.tchany1 = []
        self.tchanx2 = []
        self.tchany2 = []
        
        self.Tchanx1 = []
        self.Tchany1 = []
        self.Tchanx2 = []
        self.Tchany2 = []
        self.Filters = {}
        self.bg_channel_marker = None
        self.tau_resolution = 1
        self.filtering_routine = None
        self.MODE = None
        self.tau_mid = 1
        self.B_limit_ch_1 = None
        self.U_limit_ch_1 = None
        self.B_limit_ch_2 = None
        self.U_limit_ch_2 = None
        self.Btch_limit_ch_1 = None
        self.Utch_limit_ch_1 = None
        self.Btch_limit_ch_2 = None
        self.Utch_limit_ch_2 = None
        self.curve_list = []
        self._GI=_globalITEMS
        
        
        
    def callback_empty(self,sender,app_data):
        '''Empty function. Do nothing.'''
        pass    

    def callback_open_folder(self,sender,app_data):
        '''Open the folder conatining the .PTU files, load the list of files, and reads the forst from this list.'''
        
        
        path = app_data['current_path']
        self.last_directory = path
        self._GI.last_directory = path
        fls = os.listdir(path)
        self.files = [f for f in fls if f.endswith('.ptu')]
        self.files.sort()
        dpg.configure_item('Files_window',show=True)
        dpg.configure_item('file_box',items=self.files)
        self.anal_file = os.path.join(self.last_directory,self.files[0])
        self.load_ptu(self.anal_file)
        dpg.configure_item('apply_to_all',enabled=True)
        dpg.configure_item('apply_to_file',enabled=True)
        dpg.configure_item('Open_file_dialog',default_path=self.last_directory)
        dpg.configure_item('PTU_dir_dialog',default_path=self.last_directory)

    def define_file_menu_callbacks(self):
        '''Function defines callbacks for menu items'''
        dpg.configure_item('Open_PTU_menu_item',callback=lambda: dpg.show_item("PTU_dir_dialog"))
        
    def mount_loading_status_window(self):
        '''Opens the transparent window informing about the status'''
        with dpg.window(tag = 'load_ind_win',
                        width = self.mode_init.load_ind_win['width'],
                        height = self.mode_init.load_ind_win['height'],
                        pos = self.mode_init.load_ind_win['pos'],
                        menubar=False,
                        autosize=False,
                        no_title_bar=True,
                        no_move=True,
                        no_background=True,
                        modal=True,
                        show=True
                       ):
                        
            dpg.add_button(tag='loading_title',
                           width=self.mode_init.loading_title['width'],
                           label='Please wait'
                          )
    
            dpg.bind_item_theme('loading_title', 'transparent_theme')
            dpg.add_button(tag='loading_butt',
                           width=self.mode_init.loading_butt['width'],
                           label='LOADING...'
                          )
            dpg.bind_item_theme('loading_butt', 'transparent_theme')
            
        
    def unmount_loading_status_window(self):
        dpg.configure_item('load_ind_win',show=False)
        try:
            dpg.delete_item('loading_butt')
            dpg.delete_item('loading_title')
            
            
        except:
            pass

        try: 
            dpg.delete_item('loading_cnt_butt')
            dpg.delete_item('loading_status')
            dpg.delete_item('loading_status_text')
        except:
            pass
        try:

            dpg.delete_item('load_ind_win')
        except:
            pass
    

    def load_ptu(self,file_path):
        '''Reads the .PTU file'''
        
        self.mount_loading_status_window()
        self.sindatax1 = np.empty(10)
        self.sindatay1 = np.empty(10)
        self.sindatax2 = np.empty(10)
        self.sindatay2 = np.empty(10)
        dpg.set_value('tag_series_ch_1', [self.sindatax1, self.sindatay1])
        dpg.fit_axis_data("xaxis_chan1")
        dpg.fit_axis_data("yaxis_chan1")
    
        dpg.set_value('tag_series_ch_1_zoom', [self.sindatax1, self.sindatay1])
        dpg.fit_axis_data("xaxis_chan1_zoom")
        dpg.fit_axis_data("yaxis_chan1_zoom")
        dpg.set_value('tag_series_ch_2', [self.sindatax2, self.sindatay2])
        dpg.fit_axis_data("xaxis_chan2")
        dpg.fit_axis_data("yaxis_chan2")
        dpg.set_value('tag_series_ch_2_zoom', [self.sindatax2, self.sindatay2])
        dpg.fit_axis_data("xaxis_chan2_zoom")
        dpg.fit_axis_data("yaxis_chan2_zoom")
        
        dpg.set_value('bottom_limit_ch1',0)
        dpg.set_value('upper_limit_ch1',1)
        dpg.set_value('L_dline_ch1',0)
        dpg.set_value('U_dline_ch1',1)
        
        dpg.set_value('bottom_limit_ch2',0)
        dpg.set_value('upper_limit_ch2',1)
        dpg.set_value('L_dline_ch2',0)
        dpg.set_value('U_dline_ch2',1)
        dpg.set_axis_limits("xaxis_chan1", 0 ,1)
        dpg.set_axis_limits("xaxis_chan1_zoom", 0 ,1)
        dpg.set_axis_limits("xaxis_chan2", 0 ,1)
        dpg.set_axis_limits("xaxis_chan2_zoom", 0 ,1)
        
        dpg.configure_item('bottom_limit_ch1',enabled=False)
        dpg.configure_item('upper_limit_ch1',enabled=False)
        dpg.configure_item('reset_button_ch1',enabled=False)
        dpg.configure_item('bottom_limit_ch2',enabled=False)
        dpg.configure_item('upper_limit_ch2',enabled=False)
        dpg.configure_item('reset_button_ch2',enabled=False)
        dpg.configure_item('Remove_bgd_butt_ch_1',enabled=False)
        dpg.configure_item('Remove_bgd_butt_ch_2',enabled=False)
        dpg.configure_item('L_dline_ch1',show=False)
        dpg.configure_item('U_dline_ch1',show=False)
        dpg.configure_item('L_dline_ch2',show=False)
        dpg.configure_item('U_dline_ch2',show=False)
        dpg.hide_item('use_as_statistical_filters_chkbx_ch_1')
        dpg.hide_item('use_as_statistical_filters_chkbx_ch_2')
        ptu_image  = PTUreader(file_path, print_header_data = False)
        
        self.tau_resolution = ptu_image.head["MeasDesc_Resolution"]*1e9  
        sync_rate = ptu_image.head['TTResult_SyncRate']
        
        if not dpg.get_value('skip_lines_check'):
    
            flim_data_stack, intensity_image_all_channels,special,sync,im_channels,tcspc = ptu_image.get_flim_data_stack()
        else:
            flim_data_stack, intensity_image_all_channels,special,sync,im_channels,tcspc = ptu_image.get_flim_data_stack_omit(dpg.get_value('skip_lines_drag'))
        
        self.ntchannels = flim_data_stack.shape[3]
        self.MODE = ptu_image.head['UsrPulseCfg']
        dpg.set_value('mode_text','MODE: '+self.MODE)
        if flim_data_stack.ndim == 4:
            number_of_channels = flim_data_stack.shape[2]
    
            Resolution = str(flim_data_stack.shape[0])+'x'+str(flim_data_stack.shape[1])
            ccnt =0
            channels = []
            for channel in range(number_of_channels):
    
                channel_data = np.sum(flim_data_stack[:,:,channel,:],axis=2)
                data_sum = channel_data.sum()
    
                if data_sum!=0:
                    ccnt +=1
    
                    channels.append(channel)
            number_of_channels = ccnt
        
            for channel in range(len(channels)):
                
                tau = np.linspace(0,self.ntchannels,self.ntchannels, dtype = int)*self.tau_resolution
                self.Tchanx1 = self.Tchanx2 = np.linspace(0,self.ntchannels,self.ntchannels, dtype = int)
                if self.MODE == 'PIE':
                    if len(channels)>1:
                        '''PIE MODE two channels'''
                        
                        dpg.configure_item('bottom_limit_ch1',enabled=True)
                        dpg.configure_item('upper_limit_ch1',enabled=True)
                        dpg.configure_item('reset_button_ch1',enabled=True)
                        dpg.configure_item('Remove_bgd_butt_ch_1',enabled=True)
                        dpg.configure_item('bottom_limit_ch2',enabled=True)
                        dpg.configure_item('upper_limit_ch2',enabled=True)
                        dpg.configure_item('reset_button_ch2',enabled=True)
                        dpg.configure_item('Remove_bgd_butt_ch_2',enabled=True)
                        dpg.configure_item('L_dline_ch1',show=True)
                        dpg.configure_item('U_dline_ch1',show=True)
                        dpg.configure_item('L_dline_ch2',show=True)
                        dpg.configure_item('U_dline_ch2',show=True)
    
                        self.midle_sep = self.ntchannels//2
                        
                        self.tau_mid =self.midle_sep*self.tau_resolution
    
                        if channels[channel] == 0:
                            
                            lifetime_data = flim_data_stack[:,:,channels[channel],self.midle_sep:]
                            ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                            ys = np.sum(ys, axis = 0).astype(float)
                            self.tchanx1 = self.Tchanx1[np.where(self.Tchanx1>self.midle_sep)[0]]
                            self.Tchany1 = ys
                            self.tchany1 = self.Tchany1[np.where(self.Tchanx1>self.midle_sep)[0]]
    
                            self.sindatax1, self.sindatay1 = tau,ys
                            dpg.set_value('tag_series_ch_1', [self.sindatax1, self.sindatay1])
                            dpg.fit_axis_data("xaxis_chan1")
                            dpg.fit_axis_data("yaxis_chan1")
                            dpg.set_axis_limits("xaxis_chan1", min(self.sindatax1) ,max(self.sindatax1))
                            dpg.set_value('tag_series_ch_1_zoom', [self.sindatax1, self.sindatay1])
                            dpg.fit_axis_data("xaxis_chan1_zoom")
                            dpg.fit_axis_data("yaxis_chan1_zoom")
                            
                            dpg.set_axis_limits("xaxis_chan1_zoom", self.tau_mid ,max(self.sindatax1))
                            dpg.set_value('bottom_limit_ch1',self.tau_mid)
                            dpg.set_value('upper_limit_ch1',max(self.sindatax1))
                            dpg.set_value('L_dline_ch1',self.tau_mid)
                            dpg.set_value('U_dline_ch1',max(self.sindatax1))
                            dpg.configure_item('bottom_limit_ch1',min_value=min(self.sindatax1))
                            dpg.configure_item('bottom_limit_ch1',max_value=max(self.sindatax1))
                            dpg.configure_item('upper_limit_ch1',min_value=min(self.sindatax1))
                            dpg.configure_item('upper_limit_ch1',max_value=max(self.sindatax1))
                            
                            self.B_limit_ch_1 = dpg.get_value('L_dline_ch1')
                            self.U_limit_ch_1 = dpg.get_value('U_dline_ch1')
                            
                            self.Btch_limit_ch_1 = self.B_limit_ch_1/self.tau_resolution
                            self.Utch_limit_ch_1 = self.U_limit_ch_1/self.tau_resolution
    
                            dpg.show_item('use_as_statistical_filters_chkbx_ch_1')
                            dpg.set_value('use_as_statistical_filters_chkbx_ch_1',False)
                            self.calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_1',False)
                            
                            
                        else:
                            self.tchanx2 = self.Tchanx2[np.where(self.Tchanx2<=self.midle_sep)[0]]
                            lifetime_data = flim_data_stack[:,:,channels[channel],:self.midle_sep]
                            ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                            ys = np.sum(ys, axis = 0).astype(float)
                            self.Tchany2 = ys
                            self.tchany2 = self.Tchany2[np.where(self.Tchanx2<=self.midle_sep)[0]]
                            self.sindatax2, self.sindatay2 = tau,ys
                            dpg.set_value('tag_series_ch_2', [self.sindatax2, self.sindatay2])
                            dpg.fit_axis_data("xaxis_chan2")
                            dpg.fit_axis_data("yaxis_chan2")
                            dpg.set_axis_limits("xaxis_chan2", min(self.sindatax2) ,max(self.sindatax2))
                            dpg.set_value('tag_series_ch_2_zoom', [self.sindatax2, self.sindatay2])
                            dpg.fit_axis_data("xaxis_chan2_zoom")
                            dpg.fit_axis_data("yaxis_chan2_zoom")
                            
                            dpg.set_axis_limits("xaxis_chan2_zoom", min(self.sindatax2) ,self.tau_mid)
                            dpg.set_value('bottom_limit_ch2',min(self.sindatax2))
                            dpg.set_value('upper_limit_ch2',self.tau_mid)
                            dpg.set_value('L_dline_ch2',min(self.sindatax2))
                            dpg.set_value('U_dline_ch2',self.tau_mid)
                            dpg.configure_item('bottom_limit_ch2',min_value=min(self.sindatax2))
                            dpg.configure_item('bottom_limit_ch2',max_value=max(self.sindatax2))
                            dpg.configure_item('upper_limit_ch2',min_value=min(self.sindatax2))
                            dpg.configure_item('upper_limit_ch2',max_value=max(self.sindatax2))
                            
                            self.B_limit_ch_2 = dpg.get_value('L_dline_ch2')
                            self.U_limit_ch_2 = dpg.get_value('U_dline_ch2')
                            
                            self.Btch_limit_ch_2 = self.B_limit_ch_2/self.tau_resolution
                            self.Utch_limit_ch_2 = self.U_limit_ch_2/self.tau_resolution
    
                            dpg.show_item('use_as_statistical_filters_chkbx_ch_2')
                            dpg.set_value('use_as_statistical_filters_chkbx_ch_2',False)
                            self.calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_2',False)
                            
                    else:
                        '''PIE MODE one channels'''
                        
                        self.midle_sep = self.ntchannels//2
                        
                        self.tau_mid =self.midle_sep*self.tau_resolution
                        if channels[channel] == 0:
                            
                            dpg.configure_item('bottom_limit_ch1',enabled=True)
                            dpg.configure_item('upper_limit_ch1',enabled=True)
                            dpg.configure_item('reset_button_ch1',enabled=True)
                            dpg.configure_item('Remove_bgd_butt_ch_1',enabled=True)
                            dpg.configure_item('bottom_limit_ch2',enabled=False)
                            dpg.configure_item('upper_limit_ch2',enabled=False)
                            dpg.configure_item('reset_button_ch2',enabled=False)
                            dpg.configure_item('Remove_bgd_butt_ch_2',enabled=False)
                            
                            dpg.configure_item('L_dline_ch1',show=True)
                            dpg.configure_item('U_dline_ch1',show=True)
                            dpg.configure_item('L_dline_ch2',show=False)
                            dpg.configure_item('U_dline_ch2',show=False)
                            
                            lifetime_data = flim_data_stack[:,:,channels[channel],:]
                            ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                
                            ys = np.sum(ys, axis = 0).astype(float)
                            self.tchanx1 = self.Tchanx1[np.where(self.Tchanx1>self.midle_sep)[0]]
                            self.Tchany1 = ys
                            self.tchany1 = self.Tchany1[np.where(self.Tchanx1>self.midle_sep)[0]]
                            
                            self.sindatax1, self.sindatay1 = tau,ys
                            dpg.set_value('tag_series_ch_1', [self.sindatax1, self.sindatay1])
                            dpg.fit_axis_data("xaxis_chan1")
                            dpg.fit_axis_data("yaxis_chan1")
                            dpg.set_axis_limits("xaxis_chan1", min(self.sindatax1) ,max(self.sindatax1))
                            dpg.set_value('tag_series_ch_1_zoom', [self.sindatax1, self.sindatay1])
                            dpg.fit_axis_data("xaxis_chan1_zoom")
                            dpg.fit_axis_data("yaxis_chan1_zoom")
                            dpg.set_axis_limits("xaxis_chan1_zoom", self.tau_mid ,max(self.sindatax1))
                            dpg.set_value('bottom_limit_ch1',self.tau_mid)
                            dpg.set_value('upper_limit_ch1',max(self.sindatax1))
                            dpg.set_value('L_dline_ch1',self.tau_mid)
                            dpg.set_value('U_dline_ch1',max(self.sindatax1))
                            dpg.configure_item('bottom_limit_ch1',min_value=min(self.sindatax1))
                            dpg.configure_item('bottom_limit_ch1',max_value=max(self.sindatax1))
                            dpg.configure_item('upper_limit_ch1',min_value=min(self.sindatax1))
                            dpg.configure_item('upper_limit_ch1',max_value=max(self.sindatax1))
    
                            self.B_limit_ch_1 = dpg.get_value('L_dline_ch1')
                            self.U_limit_ch_1 = dpg.get_value('U_dline_ch1')
                            self.Btch_limit_ch_1 = self.B_limit_ch_1/self.tau_resolution
                            self.Utch_limit_ch_1 = self.U_limit_ch_1/self.tau_resolution
                            
                            dpg.show_item('use_as_statistical_filters_chkbx_ch_1')
                            dpg.set_value('use_as_statistical_filters_chkbx_ch_1',False)
                            self.calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_1',False)
                            
                        else:
                            
                            dpg.configure_item('bottom_limit_ch1',enabled=False)
                            dpg.configure_item('upper_limit_ch1',enabled=False)
                            dpg.configure_item('reset_button_ch1',enabled=False)
                            dpg.configure_item('Remove_bgd_butt_ch_1',enabled=False)
                            dpg.configure_item('bottom_limit_ch2',enabled=True)
                            dpg.configure_item('upper_limit_ch2',enabled=True)
                            dpg.configure_item('reset_button_ch2',enabled=True)
                            dpg.configure_item('Remove_bgd_butt_ch_2',enabled=True)
                            dpg.configure_item('L_dline_ch1',show=False)
                            dpg.configure_item('U_dline_ch1',show=False)
                            dpg.configure_item('L_dline_ch2',show=True)
                            dpg.configure_item('U_dline_ch2',show=True)
                            
                            lifetime_data = flim_data_stack[:,:,channels[channel],:]
                            ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                
                            ys = np.sum(ys, axis = 0).astype(float)
                            
                            self.tchanx2 = self.Tchanx2[np.where(self.Tchanx2<=self.midle_sep)[0]]
                            self.Tchany2 = ys
                            self.tchany2 = self.Tchany2[np.where(self.Tchanx2<=self.midle_sep)[0]]
                            self.sindatax2, self.sindatay2 = tau,ys
                            dpg.set_value('tag_series_ch_2', [self.sindatax2, self.sindatay2])
                            dpg.fit_axis_data("xaxis_chan2")
                            dpg.fit_axis_data("yaxis_chan2")
                            dpg.set_axis_limits("xaxis_chan2", min(self.sindatax2) ,max(self.sindatax2))
                            dpg.set_value('tag_series_ch_2_zoom', [self.sindatax2, self.sindatay2])
                            dpg.fit_axis_data("xaxis_chan2_zoom")
                            dpg.fit_axis_data("yaxis_chan2_zoom")
                            dpg.set_axis_limits("xaxis_chan2_zoom", min(self.sindatax2) ,self.tau_mid)
                            dpg.set_value('bottom_limit_ch2',min(self.sindatax2))
                            dpg.set_value('upper_limit_ch2',self.tau_mid)
                            dpg.set_value('L_dline_ch2',min(self.sindatax2))
                            dpg.set_value('U_dline_ch2',self.tau_mid)
                            dpg.configure_item('bottom_limit_ch2',min_value=min(self.sindatax2))
                            dpg.configure_item('bottom_limit_ch2',max_value=max(self.sindatax2))
                            dpg.configure_item('upper_limit_ch2',min_value=min(self.sindatax2))
                            dpg.configure_item('upper_limit_ch2',max_value=max(self.sindatax2))
    
                            self.B_limit_ch_2 = dpg.get_value('L_dline_ch2')
                            self.U_limit_ch_2 = dpg.get_value('U_dline_ch2')
                            self.Btch_limit_ch_2 = self.B_limit_ch_2/self.tau_resolution
                            self.Utch_limit_ch_2 = self.U_limit_ch_2/self.tau_resolution
                            
                            dpg.show_item('use_as_statistical_filters_chkbx_ch_2')
                            dpg.set_value('use_as_statistical_filters_chkbx_ch_2',False)
                            self.calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_2',False)
                        
                else:   
                    
                    if len(channels)>1:
                        
                        dpg.configure_item('bottom_limit_ch1',enabled=True)
                        dpg.configure_item('upper_limit_ch1',enabled=True)
                        dpg.configure_item('reset_button_ch1',enabled=True)
                        dpg.configure_item('Remove_bgd_butt_ch_1',enabled=True)
                        dpg.configure_item('bottom_limit_ch2',enabled=True)
                        dpg.configure_item('upper_limit_ch2',enabled=True)
                        dpg.configure_item('reset_button_ch2',enabled=True)
                        dpg.configure_item('Remove_bgd_butt_ch_2',enabled=True)
                        dpg.configure_item('L_dline_ch1',show=True)
                        dpg.configure_item('U_dline_ch1',show=True)
                        dpg.configure_item('L_dline_ch2',show=True)
                        dpg.configure_item('U_dline_ch2',show=True)
                    
                        if channels[channel] == 0:
    
                            lifetime_data = flim_data_stack[:,:,channels[channel],:]
    
                            ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                
                            ys = np.sum(ys, axis = 0).astype(float)
                            
                            self.tchanx1 = self.Tchanx1
                            self.Tchany1 = ys
                            self.tchany1 = self.Tchany1
                            self.sindatax1, self.sindatay1 = tau,ys
                            dpg.set_value('tag_series_ch_1', [self.sindatax1, self.sindatay1])
                            dpg.fit_axis_data("xaxis_chan1")
                            dpg.fit_axis_data("yaxis_chan1")
                            dpg.set_axis_limits("xaxis_chan1", min(self.sindatax1) ,max(self.sindatax1))
                            dpg.set_value('tag_series_ch_1_zoom', [self.sindatax1, self.sindatay1])
                            dpg.fit_axis_data("xaxis_chan1_zoom")
                            dpg.fit_axis_data("yaxis_chan1_zoom")
                            
                            dpg.set_axis_limits("xaxis_chan1_zoom", min(self.sindatax1) ,max(self.sindatax1))
                            dpg.set_value('bottom_limit_ch1',min(self.sindatax1))
                            dpg.set_value('upper_limit_ch1',max(self.sindatax1))
                            dpg.set_value('L_dline_ch1',min(self.sindatax1))
                            dpg.set_value('U_dline_ch1',max(self.sindatax1))
                            dpg.configure_item('bottom_limit_ch1',min_value=min(self.sindatax1))
                            dpg.configure_item('bottom_limit_ch1',max_value=max(self.sindatax1))
                            dpg.configure_item('upper_limit_ch1',min_value=min(self.sindatax1))
                            dpg.configure_item('upper_limit_ch1',max_value=max(self.sindatax1))
                            
                            self.B_limit_ch_1 = dpg.get_value('L_dline_ch1')
                            self.U_limit_ch_1 = dpg.get_value('U_dline_ch1')
                            
                            self.Btch_limit_ch_1 = self.B_limit_ch_1/self.tau_resolution
                            self.Utch_limit_ch_1 = self.U_limit_ch_1/self.tau_resolution
                            
                            dpg.show_item('use_as_statistical_filters_chkbx_ch_1')
                            dpg.set_value('use_as_statistical_filters_chkbx_ch_1',False)
                            self.calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_1',False)
                            
                        else:
                            lifetime_data = flim_data_stack[:,:,channels[channel],:]
                            ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                
                            ys = np.sum(ys, axis = 0).astype(float)
                            self.tchanx2 = self.Tchanx2
                            self.Tchany2 = ys
                            self.tchany2 = self.Tchany2
                            self.sindatax2, self.sindatay2 = tau,ys
                            dpg.set_value('tag_series_ch_2', [self.sindatax2, self.sindatay2])
                            dpg.fit_axis_data("xaxis_chan2")
                            dpg.fit_axis_data("yaxis_chan2")
                            dpg.set_axis_limits("xaxis_chan2", min(self.sindatax2) ,max(self.sindatax2))
                            dpg.set_value('tag_series_ch_2_zoom', [self.sindatax2, self.sindatay2])
                            dpg.fit_axis_data("xaxis_chan2_zoom")
                            dpg.fit_axis_data("yaxis_chan2_zoom")
                            
                            dpg.set_axis_limits("xaxis_chan2_zoom", min(self.sindatax2) ,max(self.sindatax2))
                            dpg.set_value('bottom_limit_ch2',min(self.sindatax2))
                            dpg.set_value('upper_limit_ch2',max(self.sindatax2))
                            dpg.set_value('L_dline_ch2',min(self.sindatax2))
                            dpg.set_value('U_dline_ch2',max(self.sindatax2))
                            dpg.configure_item('bottom_limit_ch2',min_value=min(self.sindatax2))
                            dpg.configure_item('bottom_limit_ch2',max_value=max(self.sindatax2))
                            dpg.configure_item('upper_limit_ch2',min_value=min(self.sindatax2))
                            dpg.configure_item('upper_limit_ch2',max_value=max(self.sindatax2))
                            
                            self.B_limit_ch_2 = dpg.get_value('L_dline_ch2')
                            self.U_limit_ch_2 = dpg.get_value('U_dline_ch2')
                            
                            self.Btch_limit_ch_2 = self.B_limit_ch_2/self.tau_resolution
                            self.Utch_limit_ch_2 = self.U_limit_ch_2/self.tau_resolution
                            
                            dpg.show_item('use_as_statistical_filters_chkbx_ch_2')
                            dpg.set_value('use_as_statistical_filters_chkbx_ch_2',False)
                            self.calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_2',False)
                    
                    else:
                    
                        if channels[channel] == 0:
                            dpg.configure_item('bottom_limit_ch1',enabled=True)
                            dpg.configure_item('upper_limit_ch1',enabled=True)
                            dpg.configure_item('reset_button_ch1',enabled=True)
                            dpg.configure_item('Remove_bgd_butt_ch_1',enabled=True)
                            dpg.configure_item('bottom_limit_ch2',enabled=False)
                            dpg.configure_item('upper_limit_ch2',enabled=False)
                            dpg.configure_item('reset_button_ch2',enabled=False)
                            dpg.configure_item('Remove_bgd_butt_ch_2',enabled=False)
                            dpg.configure_item('L_dline_ch1',show=True)
                            dpg.configure_item('U_dline_ch1',show=True)
                            dpg.configure_item('L_dline_ch2',show=False)
                            dpg.configure_item('U_dline_ch2',show=False)
                            
                            lifetime_data = flim_data_stack[:,:,channels[channel],:]
                            ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                
                            ys = np.sum(ys, axis = 0).astype(float)
                    
                            self.tchanx1 = self.Tchanx1
                            self.Tchany1 = ys
                            self.tchany1 = self.Tchany1
    
                            self.sindatax1, self.sindatay1 = tau,ys
                            dpg.set_value('tag_series_ch_1', [self.sindatax1, self.sindatay1])
                            dpg.fit_axis_data("xaxis_chan1")
                            dpg.fit_axis_data("yaxis_chan1")
                            dpg.set_axis_limits("xaxis_chan1", min(self.sindatax1) ,max(self.sindatax1))
                            dpg.set_axis_limits("xaxis_chan1_zoom", min(self.sindatax1) ,max(self.sindatax1))
                            dpg.set_value('tag_series_ch_1_zoom', [self.sindatax1, self.sindatay1])
                            dpg.fit_axis_data("xaxis_chan1_zoom")
                            dpg.fit_axis_data("yaxis_chan1_zoom")
                            dpg.set_value('bottom_limit_ch1',min(self.sindatax1))
                            dpg.set_value('upper_limit_ch1',max(self.sindatax1))
                            dpg.set_value('L_dline_ch1',min(self.sindatax1))
                            dpg.set_value('U_dline_ch1',max(self.sindatax1))
                            dpg.configure_item('bottom_limit_ch1',min_value=min(self.sindatax1))
                            dpg.configure_item('bottom_limit_ch1',max_value=max(self.sindatax1))
                            dpg.configure_item('upper_limit_ch1',min_value=min(self.sindatax1))
                            dpg.configure_item('upper_limit_ch1',max_value=max(self.sindatax1))
    
                            self.B_limit_ch_1 = dpg.get_value('L_dline_ch1')
                            self.U_limit_ch_1 = dpg.get_value('U_dline_ch1')
                            
                            self.Btch_limit_ch_1 =self.B_limit_ch_1/self.tau_resolution
                            self.Utch_limit_ch_1 = self.U_limit_ch_1/self.tau_resolution
                            
                            dpg.show_item('use_as_statistical_filters_chkbx_ch_1')
                            dpg.set_value('use_as_statistical_filters_chkbx_ch_1',False)
                            self.calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_1',False)
    
    
                        else:
                            dpg.configure_item('bottom_limit_ch1',enabled=False)
                            dpg.configure_item('upper_limit_ch1',enabled=False)
                            dpg.configure_item('reset_button_ch1',enabled=False)
                            dpg.configure_item('Remove_bgd_butt_ch_1',enabled=False)
                            dpg.configure_item('bottom_limit_ch2',enabled=True)
                            dpg.configure_item('upper_limit_ch2',enabled=True)
                            dpg.configure_item('reset_button_ch2',enabled=True)
                            dpg.configure_item('Remove_bgd_butt_ch_2',enabled=True)
                            dpg.configure_item('L_dline_ch1',show=False)
                            dpg.configure_item('U_dline_ch1',show=False)
                            dpg.configure_item('L_dline_ch2',show=True)
                            dpg.configure_item('U_dline_ch2',show=True)
                            
                            lifetime_data = flim_data_stack[:,:,channels[channel],:]
                            ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                
                            ys = np.sum(ys, axis = 0).astype(float)
                            self.tchanx2 = self.Tchanx2
                            self.Tchany2 = ys
                            self.tchany2 =self.Tchany2
                            self.sindatax2, self.sindatay2 = tau,ys
                            dpg.set_value('tag_series_ch_2', [self.sindatax2, self.sindatay2])
                            dpg.fit_axis_data("xaxis_chan2")
                            dpg.fit_axis_data("yaxis_chan2")
                            dpg.set_axis_limits("xaxis_chan2", min(self.sindatax2) ,max(self.sindatax2))
                            dpg.set_axis_limits("xaxis_chan2_zoom", min(self.sindatax2) ,max(self.sindatax2))
                            dpg.set_value('tag_series_ch_2_zoom', [self.sindatax2, self.sindatay2])
                            dpg.fit_axis_data("xaxis_chan2_zoom")
                            dpg.fit_axis_data("yaxis_chan2_zoom")
                            dpg.set_value('bottom_limit_ch2',min(self.sindatax2))
                            dpg.set_value('upper_limit_ch2',max(self.sindatax2))
                            dpg.set_value('L_dline_ch2',min(self.sindatax2))
                            dpg.set_value('U_dline_ch2',max(self.sindatax2))
                            dpg.configure_item('bottom_limit_ch2',min_value=min(self.sindatax2))
                            dpg.configure_item('bottom_limit_ch2',max_value=max(self.sindatax2))
                            dpg.configure_item('upper_limit_ch2',min_value=min(self.sindatax2))
                            dpg.configure_item('upper_limit_ch2',max_value=max(self.sindatax2))
    
                            self.B_limit_ch_2 = dpg.get_value('L_dline_ch2')
                            self.U_limit_ch_2 = dpg.get_value('U_dline_ch2')
                            
                            self.Btch_limit_ch_2 = self.B_limit_ch_2/self.tau_resolution
                            self.Utch_limit_ch_2 = self.U_limit_ch_2/self.tau_resolution
                            
                            dpg.show_item('use_as_statistical_filters_chkbx_ch_2')
                            dpg.set_value('use_as_statistical_filters_chkbx_ch_2',False)
                            self.calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_2',False)
        
        if_Tchany1 = len(self.Tchany1)!=0
        if_Tchany2 = len(self.Tchany2)!=0
        
        if_routine_ch_1 = dpg.get_value('use_as_group_routine_chkbx_ch_1')
        if_routine_ch_2 = dpg.get_value('use_as_group_routine_chkbx_ch_2')
        
        if if_routine_ch_1 and if_routine_ch_2:
            pass
        elif if_routine_ch_1 and not if_routine_ch_2:
            
            self.filtering_routine['Channel 2']={ 'BG':False}
        elif not if_routine_ch_1 and  if_routine_ch_2:
            self.filtering_routine['Channel 1']={ 'BG':False}
        elif not if_routine_ch_1 and not if_routine_ch_2:
            self.filtering_routine={'Channel 1':
                       {'BG':False
                       },
                       'Channel 2':
                       {'BG':False
                       }
                      }
        else:
            pass
        
        if if_routine_ch_1:
            dpg.show_item('filters_ch_1_tab_list_tag')
    
        else:
            dpg.hide_item('filters_ch_1_tab_list_tag')
            self.unmount_filter_list_table(1)
            
        if if_routine_ch_2:
    
            dpg.show_item('filters_ch_2_tab_list_tag')
        else:
            dpg.hide_item('filters_ch_2_tab_list_tag')
            self.unmount_filter_list_table(2)
            
        self.unmount_loading_status_window()


    def callback_dragline(self,sender,app_data):     
        
        if str(sender).isdigit():
            
            sender = dpg.get_item_alias(sender)
        else:
            pass
        
        value = dpg.get_value(sender)
        
        if sender == 'L_dline_ch1':
            if value >= dpg.get_value('U_dline_ch1'):
                value = dpg.get_value('U_dline_ch1')
                dpg.set_value(sender,value)
            elif value < min(self.sindatax1):
                value = min(self.sindatax1)
                dpg.set_value(sender,value)
            else:
                pass
            
            dpg.set_axis_limits("xaxis_chan1_zoom", value, dpg.get_value('U_dline_ch1'))
            dpg.set_value('bottom_limit_ch1',value)
            dpg.set_value('upper_limit_ch1',dpg.get_value('U_dline_ch1'))
            self.B_limit_ch_1 = dpg.get_value('L_dline_ch1')
            self.Btch_limit_ch_1 = int(self.B_limit_ch_1/self.tau_resolution)
            self.Utch_limit_ch_1 = int(dpg.get_value('U_dline_ch1')/self.tau_resolution)
            self.tchanx1 = self.Tchanx1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
            self.tchany1 = self.Tchany1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
    
        elif sender == 'U_dline_ch1':
            if value <= dpg.get_value('L_dline_ch1'):
                value = dpg.get_value('L_dline_ch1')
                dpg.set_value(sender,value)
            elif value > max(self.sindatax1):
                value = max(self.sindatax1)
                dpg.set_value(sender,value)
            else:
                pass
            dpg.set_axis_limits("xaxis_chan1_zoom",dpg.get_value('L_dline_ch1') , value)
            dpg.set_value('bottom_limit_ch1',dpg.get_value('L_dline_ch1'))
            dpg.set_value('upper_limit_ch1',value)
            self.U_limit_ch_1 = dpg.get_value('U_dline_ch1')
            
            self.Btch_limit_ch_1 = int(dpg.get_value('L_dline_ch1')/self.tau_resolution)
            self.Utch_limit_ch_1 = int(self.U_limit_ch_1/self.tau_resolution)
            self.tchanx1 = self.Tchanx1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
            self.tchany1 = self.Tchany1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
        elif sender == 'L_dline_ch2':
            if value >= dpg.get_value('U_dline_ch2'):
                value = dpg.get_value('U_dline_ch2')
                dpg.set_value(sender,value)
            elif value < min(self.sindatax2):
                value = min(self.sindatax2)
                dpg.set_value(sender,value)
            else:
                pass
            dpg.set_axis_limits("xaxis_chan2_zoom", value, dpg.get_value('U_dline_ch2'))
            dpg.set_value('bottom_limit_ch2',value)
            dpg.set_value('upper_limit_ch2',dpg.get_value('U_dline_ch2'))
            B_limit_ch_2 = dpg.get_value('L_dline_ch2')
            
            self.Btch_limit_ch_2 = int(self.B_limit_ch_2/self.tau_resolution)
            self.Utch_limit_ch_2 = int(dpg.get_value('U_dline_ch2')/self.tau_resolution)
            self.tchanx2 = self.Tchanx2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
            self.tchany2 = self.Tchany2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
        elif sender == 'U_dline_ch2':
            if value <= dpg.get_value('L_dline_ch2'):
                value = dpg.get_value('L_dline_ch2')
                dpg.set_value(sender,value)
            elif value > max(self.sindatax2):
                value = max(self.sindatax2)
                dpg.set_value(sender,value)
            else:
                pass
            dpg.set_axis_limits("xaxis_chan2_zoom",dpg.get_value('L_dline_ch2') , value)
            dpg.set_value('bottom_limit_ch2',dpg.get_value('L_dline_ch2'))
            dpg.set_value('upper_limit_ch2',value)
            self.U_limit_ch_2 = dpg.get_value('U_dline_ch2')
            
            self.Btch_limit_ch_2 = int(dpg.get_value('L_dline_ch2')/self.tau_resolution)
            self.Utch_limit_ch_2 = int(self.U_limit_ch_2/self.tau_resolution)
            self.tchanx2 = self.Tchanx2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
            self.tchany2 = self.Tchany2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]


    def callback_query(self,sender,app_data):
        
        if sender == 'bottom_limit_ch1':
            dpg.set_axis_limits("xaxis_chan1_zoom", app_data, dpg.get_value('upper_limit_ch1'))
            dpg.set_value('L_dline_ch1',app_data)
            dpg.set_value('U_dline_ch1',dpg.get_value('upper_limit_ch1'))
            self.B_limit_ch_1 = app_data
            
            self.Btch_limit_ch_1 = int(self.B_limit_ch_1/self.tau_resolution)
            self.Utch_limit_ch_1 = int(dpg.get_value('upper_limit_ch1')/self.tau_resolution)
            self.tchanx1 = self.Tchanx1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
            self.tchany1 = self.Tchany1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
    
        elif sender == 'upper_limit_ch1':
            dpg.set_axis_limits("xaxis_chan1_zoom", dpg.get_value('bottom_limit_ch1'),app_data)
            dpg.set_value('L_dline_ch1',dpg.get_value('bottom_limit_ch1'))
            dpg.set_value('U_dline_ch1',app_data)
            self.U_limit_ch_1 = app_data
            
            self.Btch_limit_ch_1 = int(dpg.get_value('bottom_limit_ch1')/self.tau_resolution)
            self.Utch_limit_ch_1 = int(self.U_limit_ch_1/self.tau_resolution)
            self.tchanx1 = self.Tchanx1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
            self.tchany1 = self.Tchany1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
            
        elif sender == 'bottom_limit_ch2':
            dpg.set_axis_limits("xaxis_chan2_zoom", app_data, dpg.get_value('upper_limit_ch2'))
            dpg.set_value('L_dline_ch2',app_data)
            dpg.set_value('U_dline_ch2',dpg.get_value('upper_limit_ch2'))
            self.B_limit_ch_2 = app_data
            
            self.Btch_limit_ch_2 = int(self.B_limit_ch_2/self.tau_resolution)
            self.Utch_limit_ch_2 = int(dpg.get_value('upper_limit_ch2')/self.tau_resolution)
            self.tchanx2 = self.Tchanx2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
            self.tchany2 = self.Tchany2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
            
        elif sender == 'upper_limit_ch2':
            dpg.set_axis_limits("xaxis_chan2_zoom", dpg.get_value('bottom_limit_ch2'),app_data)
            dpg.set_value('L_dline_ch2',dpg.get_value('bottom_limit_ch2'))
            dpg.set_value('U_dline_ch2',app_data)
            self.U_limit_ch_2 = app_data
            
            self.Btch_limit_ch_2 = int(dpg.get_value('bottom_limit_ch2')/self.tau_resolution)
            self.Utch_limit_ch_2 = int(self.U_limit_ch_2/self.tau_resolution)
            self.tchanx2 = self.Tchanx2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
            self.tchany2 = self.Tchany2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
        else:
            pass


    def query_ch1(self,sender,app_data,user_data):
        
        if app_data[0]<min(self.sindatax1) and app_data[1]<max(self.sindatax1):
            
            dpg.set_axis_limits("xaxis_chan1_zoom", min(self.sindatax1), app_data[1])
            dpg.set_value('bottom_limit_ch1',min(self.sindatax1))
            dpg.set_value('upper_limit_ch1',app_data[1])
        elif app_data[0]<min(self.sindatax1) and app_data[1]>max(self.sindatax1):
            dpg.set_axis_limits("xaxis_chan1_zoom", min(self.sindatax1), max(self.sindatax1))
            dpg.set_value('bottom_limit_ch1',min(self.sindatax1))
            dpg.set_value('upper_limit_ch1',max(self.sindatax1))
        elif app_data[0]>=min(self.sindatax1) and app_data[1]>max(self.sindatax1):
            dpg.set_axis_limits("xaxis_chan1_zoom", app_data[0], max(self.sindatax1))
            dpg.set_value('bottom_limit_ch1',app_data[0])
            dpg.set_value('upper_limit_ch1',max(self.sindatax1))
        elif app_data[0]>=min(self.sindatax1) and app_data[1]<=max(self.sindatax1):
            dpg.set_axis_limits("xaxis_chan1_zoom", app_data[0], app_data[1])
            dpg.set_value('bottom_limit_ch1',app_data[0])
            dpg.set_value('upper_limit_ch1',app_data[1])
        else:
            pass
        
    def query_ch2(self,sender,app_data,user_data):
            
            if app_data[0]<min(self.sindatax2) and app_data[1]<max(self.sindatax2):
                
                dpg.set_axis_limits("xaxis_chan2_zoom", min(self.sindatax2), app_data[1])
                dpg.set_value('bottom_limit_ch2',min(self.sindatax2))
                dpg.set_value('upper_limit_ch2',app_data[1])
            elif app_data[0]<min(self.sindatax2) and app_data[1]>max(self.sindatax2):
                dpg.set_axis_limits("xaxis_chan2_zoom", min(self.sindatax2), max(self.sindatax2))
                dpg.set_value('bottom_limit_ch2',min(self.sindatax2))
                dpg.set_value('upper_limit_ch2',max(self.sindatax2))
            elif app_data[0]>=min(self.sindatax2) and app_data[1]>max(self.sindatax2):
                dpg.set_axis_limits("xaxis_chan2_zoom", app_data[0], max(self.sindatax2))
                dpg.set_value('bottom_limit_ch2',app_data[0])
                dpg.set_value('upper_limit_ch2',max(self.sindatax2))
            elif app_data[0]>=min(self.sindatax2) and app_data[1]<=max(self.sindatax2):
                dpg.set_axis_limits("xaxis_chan2_zoom", app_data[0], app_data[1])
                dpg.set_value('bottom_limit_ch2',app_data[0])
                dpg.set_value('upper_limit_ch2',app_data[1])
            else:
                pass

    def show_br_fltr_wndw(self,sender):
        
        dpg.set_value('tag_series_fltr', [[], []])
        dpg.set_value('tag_series_fltr_subtr', [[], []])
        dpg.configure_item("tag_series_fltr", label = '')
        dpg.configure_item("tag_series_fltr_subtr", label = '')
        
        dpg.hide_item("Background_RLL_line")
        dpg.hide_item("Background_RUL_line")
        dpg.hide_item('fltr_filters_plot')
        
        self.unmount_decay_table()
        self.unmount_LIB_decay_table()
        self.callback_Cancel_library_import('Cancel_library_import',None)
        self.remove_imported_curves_from_plot()
        self.remove_existing_filter_plots()
        
        dpg.set_value('add_bg_range', False)
        dpg.set_axis_limits("xaxis_tltr", 0 ,1)
        if sender == 'Remove_bgd_butt_ch_1':
            
            self.bg_channel_marker = 1
            the_channel = 'Channel 1'
            self.filtering_routine[the_channel] = {}
            self.fl_bg_curves_dict[the_channel] = {self.anal_file:{
                                                 'name':'(Ch1) '+self.anal_file.split('/')[-1],
                                                 'file_path':self.anal_file,
                                                'TCSPC_resolution':int(np.round(self.tau_resolution*1e-9*1e12)),
                                                'TCSPC_channels':self.ntchannels,
                                                 'Tchanx1' : self.Tchanx1,
                                                 'Tchany1' : self.Tchany1,
                                                 'tchanx1' : self.tchanx1,
                                                 'tchany1' : self.tchany1,
                                                 'Btch_limit_ch_1': self.Btch_limit_ch_1,
                                                 'Utch_limit_ch_1': self.Utch_limit_ch_1,
                                                 'subtract_bg':{
                                                      'tchanx1' : [],
                                                      'tchany1' : []
                                                                 }
                                                         }
                                              
                                             }
            
    
            dpg.set_value('get_channel',the_channel)
            dpg.set_value('get_tcspc_resolution',int(np.round(self.tau_resolution*1e-9*1e12)))
    
    
            
            ys = self.tchany1/np.sum(self.tchany1)
    
    
            minimum = min(abs(ys[np.where(ys!=0)[0]]))/2
            
            dpg.set_value('tag_series_fltr', [self.tchanx1*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0], ys])
            dpg.set_axis_limits("xaxis_tltr", self.Btch_limit_ch_1*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0] ,self.Utch_limit_ch_1*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0])
            dpg.set_axis_limits("yaxis_tltr", minimum ,max(ys)*2)
            
    
            self.curve_list =[]
            for k in self.fl_bg_curves_dict['Channel 1'].keys():
                name = self.fl_bg_curves_dict['Channel 1'][k]['name']
                len_subtr_y = len(self.fl_bg_curves_dict['Channel 1'][k]['tchany1'])
                
                if name == 'Subtracted':
                    if len_subtr_y == 0:
                        pass
                else:
                    self.curve_list.append(name)
                    
            
            self.mount_decay_table(self.curve_list)
            
        elif sender == 'Remove_bgd_butt_ch_2':
            self.bg_channel_marker = 2
            the_channel = 'Channel 2'
            self.filtering_routine[the_channel] = {}
            self.fl_bg_curves_dict[the_channel] = {self.anal_file:{
                                             'name':'(Ch2) '+self.anal_file.split('/')[-1],
                                             'file_path':self.anal_file,
                                            'TCSPC_resolution':int(np.round(self.tau_resolution*1e-9*1e12)),
                                            'TCSPC_channels':self.ntchannels,
                                             'Tchanx2' : self.Tchanx2,
                                             'Tchany2' : self.Tchany2,
                                             'tchanx2' : self.tchanx2,
                                             'tchany2' : self.tchany2,
                                             'Btch_limit_ch_2': self.Btch_limit_ch_2,
                                             'Utch_limit_ch_2': self.Utch_limit_ch_2,
                                            'subtract_bg':{
                                                  'tchanx2' : [],
                                                  'tchany2' : []
                                                             }
                                                    }
                                              
                                             }
            dpg.set_value('get_channel',the_channel)
            dpg.set_value('get_tcspc_resolution',int(np.round(self.tau_resolution*1e-9*1e12)))
            ys = self.tchany2/np.sum(self.tchany2)
            minimum = min(abs(ys[np.where(ys!=0)[0]]))/2
            dpg.set_value('tag_series_fltr', [self.tchanx2*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0], ys])
            dpg.set_axis_limits("xaxis_tltr", self.Btch_limit_ch_2*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0] ,self.Utch_limit_ch_2*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0])
            dpg.set_axis_limits("yaxis_tltr", minimum ,max(ys)*2)
            self.curve_list =[]
            for k in self.fl_bg_curves_dict['Channel 2'].keys():
                name = self.fl_bg_curves_dict['Channel 2'][k]['name']
                len_subtr_y = len(self.fl_bg_curves_dict['Channel 2'][k]['tchany2'])
                
                if name == 'Subtracted':
                    if len_subtr_y == 0:
                        pass
                else:
                    self.curve_list.append(name)
            self.mount_decay_table(self.curve_list)
        self.callback_Set_background_range('add_bg_range',False)     
        self.unmount_filter_list_table(self.bg_channel_marker)
        dpg.configure_item("tag_series_fltr", label = 'Decay')
        dpg.show_item('BG_removal_window')
        
    
    def calllback_use_stat_filters_chbx(self,sender,app_data):
    
        if_value=app_data 
        if if_value:
            if sender == 'use_as_statistical_filters_chkbx_ch_1':
                dpg.show_item('Remove_bgd_butt_ch_1')
                self.callback_reset_range('reset_button_ch1',None)
                dpg.hide_item('L_dline_ch1')
                dpg.hide_item('U_dline_ch1')
                
                
            if sender == 'use_as_statistical_filters_chkbx_ch_2':
                dpg.show_item('Remove_bgd_butt_ch_2')
                self.callback_reset_range('reset_button_ch2',None)
                dpg.hide_item('L_dline_ch2')
                dpg.hide_item('U_dline_ch2')
        else:
            if sender == 'use_as_statistical_filters_chkbx_ch_1':
                dpg.hide_item('Remove_bgd_butt_ch_1')
                self.callback_reset_range('reset_button_ch1',None)
                dpg.show_item('L_dline_ch1')
                dpg.show_item('U_dline_ch1')
                self.unmount_filter_list_table(1)
                
                
            if sender == 'use_as_statistical_filters_chkbx_ch_2':
                dpg.hide_item('Remove_bgd_butt_ch_2')
                self.callback_reset_range('reset_button_ch2',None)
                dpg.show_item('L_dline_ch2')
                dpg.show_item('U_dline_ch2')
                self.unmount_filter_list_table(2)

    def unmount_filter_list_table(self,channel):
        rows = dpg.get_aliases()
        rows = [r for r in rows if r.startswith('filters_ch_'+str(channel)+'_tab_list_row_')]
        for r in rows:
            dpg.delete_item(r)
        if channel == 1:
            dpg.hide_item('filters_ch_1_tab_list_tag')
        elif channel == 2:
            dpg.hide_item('filters_ch_2_tab_list_tag')
        else:
            pass
        

    
    def callback_reset_range(self,sender,app_data):

    
        if self.MODE == 'PIE':
        
            if sender == 'reset_button_ch1':
                
                dpg.set_axis_limits("xaxis_chan1_zoom", self.tau_mid ,max(self.sindatax1))
                dpg.set_value('L_dline_ch1',self.tau_mid)
                dpg.set_value('U_dline_ch1',max(self.sindatax1))
                dpg.set_value('bottom_limit_ch1',self.tau_mid)
                dpg.set_value('upper_limit_ch1',max(self.sindatax1))
                self.B_limit_ch_1 = self.tau_mid
                self.U_limit_ch_1 = max(self.sindatax1)
                self.Btch_limit_ch_1 = int(self.B_limit_ch_1/self.tau_resolution)
                self.Utch_limit_ch_1 = int(self.U_limit_ch_1/self.tau_resolution)
                self.tchanx1 = self.Tchanx1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
    
                self.tchany1 = self.Tchany1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
    
            elif sender == 'reset_button_ch2':
                dpg.set_axis_limits("xaxis_chan2_zoom", min(self.sindatax2), self.tau_mid)
                dpg.set_value('L_dline_ch2',min(self.sindatax2))
                dpg.set_value('U_dline_ch2',self.tau_mid)
                dpg.set_value('bottom_limit_ch2',min(self.sindatax2))
                dpg.set_value('upper_limit_ch2',self.tau_mid)
                self.B_limit_ch_2 = min(self.sindatax2)
                self.U_limit_ch_2 = self.tau_mid
                self.Btch_limit_ch_2 = int(self.B_limit_ch_2/self.tau_resolution)
                self.Utch_limit_ch_2 = int(self.U_limit_ch_2/self.tau_resolution)
                self.tchanx2 = self.Tchanx2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
                self.tchany2 = self.Tchany2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
            else:
                pass
            
        else:
            if sender == 'reset_button_ch1':
                dpg.set_axis_limits("xaxis_chan1_zoom", min(self.sindatax1), max(self.sindatax1))
                
                dpg.set_value('L_dline_ch1',min(self.sindatax1))
                dpg.set_value('U_dline_ch1',max(self.sindatax1))
                dpg.set_value('bottom_limit_ch1',min(self.sindatax1))
                dpg.set_value('upper_limit_ch1',max(self.sindatax1))
                self.B_limit_ch_1 = min(self.sindatax1)
                self.U_limit_ch_1 = max(self.sindatax1)
                self.Btch_limit_ch_1 = int(self.B_limit_ch_1/self.tau_resolution)
                self.Utch_limit_ch_1 = int(self.U_limit_ch_1/self.tau_resolution)
                self.tchanx1 = self.Tchanx1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
                self.tchany1 = self.Tchany1[np.where((self.Tchanx1>self.Btch_limit_ch_1) & (self.Tchanx1<=self.Utch_limit_ch_1))[0]]
            elif sender == 'reset_button_ch2':
                dpg.set_axis_limits("xaxis_chan2_zoom", min(self.sindatax2), max(self.sindatax2))
                dpg.set_value('L_dline_ch2',min(self.sindatax2))
                dpg.set_value('U_dline_ch2',max(self.sindatax2))
                dpg.set_value('bottom_limit_ch2',min(self.sindatax2))
                dpg.set_value('upper_limit_ch2',max(self.sindatax2))
                self.B_limit_ch_2 = min(self.sindatax2)
                self.U_limit_ch_2 = max(self.sindatax2)
                self.Btch_limit_ch_2 = int(self.B_limit_ch_2/self.tau_resolution)
                self.Utch_limit_ch_2 = int(self.U_limit_ch_2/self.tau_resolution)
                self.tchanx2 = self.Tchanx2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
                self.tchany2 = self.Tchany2[np.where((self.Tchanx2>self.Btch_limit_ch_2) & (self.Tchanx2<=self.Utch_limit_ch_2))[0]]
            else:
                pass
    
    def adjust_curves(self,imported_data,original_time_data):
        '''Adjcust two decays to have the same X scale'''
        
        original_time_data.columns=['time']
        imported_data=pd.concat([imported_data,original_time_data], ignore_index=True)
        imported_data = imported_data.sort_values(by='time')
        imported_data=imported_data.reset_index(drop=True).interpolate(method='cubicspline')
        joined_df = imported_data[imported_data['time'].isin(original_time_data.time)]
        joined_df['dif']=joined_df.loc[:,('time')].diff()
        joined_df.dropna(inplace=True)
        joined_df=joined_df.reset_index(drop=True)
        joined_df.at[0,'dif']=-1
        joined_df=joined_df.where(joined_df.dif!=0).dropna()
        
        return joined_df

    def calculate_filters_from_routine(self,routine):
        '''Calulates filter matrix'''
    
        channel = None
        if self.bg_channel_marker == None:
            pass
        elif self.bg_channel_marker == 1:
            channel = 1
            rawx = self.tchanx1
            rawdatax_t = self.tchanx1*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            rawy = self.tchany1
            Btch_limit= self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['Btch_limit_ch_1']*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            Utch_limit= self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['Utch_limit_ch_1']*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            
            
            cname = 'Current decay; CH 1'
            
        elif self.bg_channel_marker == 2:
            channel = 2
            rawx = self.tchanx2
            rawdatax_t = self.tchanx2*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
            rawy = self.tchany2
            Btch_limit= self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['Btch_limit_ch_2']*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
            Utch_limit= self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['Utch_limit_ch_2']*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
            cname = 'Current decay; CH 2'
        else:
            pass
    
        jsn_file = 'TCSPC_decay_library.json'
        jsn_path = os.path.join('res','Lib','json',jsn_file)
        with open(jsn_path) as json_library:
            jsn_dict = json.load(json_library)
        
        curve_names = routine['Channel '+str(channel)].keys()
        curve_names = [c for c in curve_names if c!='BG']
        curve_names = [c for c in curve_names if c!='BG_rng']
        
        
        CURVES={}
    
    
        if_BG = routine['Channel '+str(channel)]['BG']
        
        if_afterpulse = dpg.get_value('remove_afterpulsing_chkbx')
        if not if_BG and len(curve_names)==0:
            dpg.show_item('fl_bg_win_group_4')
            dpg.show_item('no_curves_notiffication')
            dpg.show_item('OK_button')
            dpg.configure_item('Calculate_filters',enabled=False)
        elif not if_BG and len(curve_names)>0:
            for curv in curve_names:
                curve = np.load(routine['Channel '+str(channel)][curv])
    
                df = pd.DataFrame(curve.T,columns=['time','ydata'])
                df.ydata = df.ydata/df.ydata.sum()
    
                adjusted = self.adjust_curves(df, pd.Series(rawdatax_t).to_frame())
    
                
                curve=adjusted.ydata.values
    
    
                CURVES[curv]=curve
                
            if if_afterpulse:
    
                afterpulse = 1/np.unique(rawx).size
                afterpulse = np.array([afterpulse for i in CURVES[curve_names[0]]])
                CURVES['Afterpulsing and background']=afterpulse
                
            else:
                pass
            
        
            
        elif if_BG and len(curve_names)==0:
            xs = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]
            ys = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]
            norma = np.sum(ys)
            CURVES[cname] = ys/norma
            
            if if_afterpulse:
    
                afterpulse = 1/np.unique(xs).size
                afterpulse = np.array([afterpulse for i in CURVES[cname]])
                CURVES['Afterpulsing and background']=afterpulse
            else:
                pass
        else:
            xs = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]
            ys = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]
            norma = np.sum(ys)
    
            CURVES[cname] = ys/norma
            
            
            for curv in curve_names:
                curve = np.load(routine['Channel '+str(channel)][curv])
    
                df = pd.DataFrame(curve.T,columns=['time','ydata'])
                df.ydata = df.ydata/df.ydata.sum()
    
                adjusted = self.adjust_curves(df, pd.Series(rawdatax_t).to_frame())
    
                
                curve=adjusted.ydata.values
                
    
    
                
                CURVES[curv]=curve
            if if_afterpulse:
                afterpulse = 1/np.unique(rawx).size
                afterpulse = np.array([afterpulse for i in CURVES[cname]])
                CURVES['Afterpulsing and background']=afterpulse
            else:
                pass
    
        
        
        self.Filters['Channel '+str(channel)] = self.calculate_stat_filter(CURVES,rawy)
    
        
        minlist=[]
        self.remove_existing_filter_plots()
        for F_name in self.Filters['Channel '+str(channel)].keys():
            
            F = self.Filters['Channel '+str(channel)][F_name]
            F = F/np.max(F)
    
            fcurve_tag="tag_series_F_"+F_name
            dpg.add_scatter_series(rawdatax_t, F, parent='yaxis_tltr_fltr',tag=fcurve_tag,label=F_name)
            
            minlist.append(min(abs(F[np.where(F!=0)[0]]))/2)
        minimum = min(minlist)
        maximum =2
        dpg.set_axis_limits("xaxis_tltr_fltr", Btch_limit ,Utch_limit)
        dpg.set_axis_limits("yaxis_tltr_fltr", minimum ,maximum)
        dpg.show_item('fltr_filters_plot')
        dpg.show_item('fl_accpet_filters_group')
        
        dpg.show_item('Decline_filters')
        dpg.show_item('Accept_filters')

    def calculate_stat_filter(self,Pure_components_dict,raw_signal):

        pure_components = []
        for c in Pure_components_dict.keys():
            pure_components.append(Pure_components_dict[c])
                
        M = np.concatenate(pure_components).reshape((len(pure_components),
                                                     len(pure_components[-1]))).T
    
        I = raw_signal
        diagI=np.diag(I)
        try:
            DET = det(diagI)
        except:
            DET = 0
            
        if DET==0 or np.isinf(DET):
            invdiag = pinv(diagI)
        else:
            invdiag = inv(diagI)
        
        if det(np.dot(np.dot(M.T,invdiag),M)) ==0:   
            F = np.dot(pinv(np.dot(np.dot(M.T,invdiag),M)),np.dot(M.T,invdiag))
        else:
            F = np.dot(inv(np.dot(np.dot(M.T,invdiag),M)),np.dot(M.T,invdiag))
            
        FILTERS_dict = {}
        for i,c in enumerate(Pure_components_dict.keys()):
            FILTERS_dict[c]=F[i]
        return FILTERS_dict


    def callback_Accept_filters(self):
        channel = None
        if self.bg_channel_marker == None:
            pass
        elif self.bg_channel_marker == 1:
            channel = 1
            
        elif self.bg_channel_marker == 2:
            channel = 2
        else:
            pass
        dpg.hide_item('fltr_filters_plot')
        dpg.hide_item('Decline_filters')
        dpg.hide_item('fl_accpet_filters_group')
        dpg.hide_item('Accept_filters')
        self.unmount_decay_table()
        self.unmount_LIB_decay_table()
        self.remove_imported_curves_from_plot()
        dpg.hide_item('BG_removal_window')
        dpg.set_value('use_as_statistical_filters_chkbx_ch_'+str(channel),True)
        dpg.show_item('filters_ch_'+str(channel)+'_tab_list_tag')
        self.mount_filter_list_table(channel)
        self.Filters ['Channel '+str(channel)] = {}

        
    def callback_Calculate_filters(self,sender,app_data):
        
        jsn_file = 'TCSPC_decay_library.json'
        jsn_path = os.path.join('res','Lib','json',jsn_file)
        with open(jsn_path) as json_library:
            jsn_dict = json.load(json_library)
        
        channel = None
        if self.bg_channel_marker == None:
            pass
        elif self.bg_channel_marker == 1:
            channel = 1
            rawx = self.tchanx1*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            rawy = self.tchany1
            xs = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]
            ys = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]
            Btch_limit= self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['Btch_limit_ch_1']*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            Utch_limit= self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['Utch_limit_ch_1']*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            
            
        elif self.bg_channel_marker == 2:
            channel = 2
            rawx = self.tchanx2*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
            rawy = self.tchany2
            xs = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]
            ys = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]
            Btch_limit= self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['Btch_limit_ch_2']*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
            Utch_limit= self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['Utch_limit_ch_2']*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
        else:
            pass
        curves = dpg.get_aliases()
        curves = [c for c in curves if c.startswith('decays_tab_row_')]
        curves = [c for c in curves if c.endswith('_cell b_chk')]
        curves = [c for c in curves if c != 'decays_tab_row_0_cell b_chk']
        curves = [c for c in curves if dpg.get_value(c)]
        for c in curves:
            c_ind = int(c.split('_')[3])
            c_name = dpg.get_value('decays_tab_row_'+str(c_ind)+'_cell a_text')
            cnpy = jsn_dict['Channel '+str(channel)][c_name]['npy_path']
            self.filtering_routine['Channel '+str(channel)][c_name]=cnpy
            
        self.calculate_filters_from_routine(self.filtering_routine)


    def callback_Cancel_library_import(self,sender,app_data):
        dpg.hide_item('Cancel_library_import')
        dpg.hide_item('decays_tab_lib_list_tag')
        dpg.hide_item('Proceed_library_import')
        dpg.hide_item('empty_library_notiffication')
        self.unmount_LIB_decay_table()
        tmp_series = dpg.get_aliases()
        tmp_series = [r for r in tmp_series if 'tag_series_fltr_temp_import' in r]
    
        for r in tmp_series:
            dpg.delete_item(r)
        to_import_list = dpg.get_aliases()
        to_import_list = [s for s in to_import_list if s.startswith('decays_lib_tab_row_')]
        to_import_list = [s for s in to_import_list if s.endswith('_cell e_chk')]
        for marked_decay in to_import_list:
            dpg.set_value(marked_decay,False)

    def callback_Decline_filters(self):
        channel = None
        if self.bg_channel_marker == None:
            pass
        elif self.bg_channel_marker == 1:
            channel = 1
            
        elif self.bg_channel_marker == 2:
            channel = 2
        else:
            pass
        self.remove_existing_filter_plots()
        dpg.hide_item('fltr_filters_plot')
        dpg.hide_item('Decline_filters')
        dpg.hide_item('fl_accpet_filters_group')
        dpg.hide_item('Accept_filters')
        self.Filters ['Channel '+str(channel)] = {}

    def callback_ERROR_dialog_close(self,sender,app_data):
        dpg.configure_item('ERROR',show=False)
        dpg.delete_item('ERROR_text')
        dpg.delete_item('ERROR_butt')
        dpg.delete_item('ERROR')

    def callback_Proceed_library_import(self,sender,app_data):

        channel = None
        if self.bg_channel_marker == None:
                pass
        elif self.bg_channel_marker == 1:
            channel = 'Channel 1'
            
        elif self.bg_channel_marker == 2:
            channel = 'Channel 2'
    
        else:
            pass
        to_import_list = dpg.get_aliases()
        to_import_list = [s for s in to_import_list if s.startswith('decays_lib_tab_row_')]
        to_import_list = [s for s in to_import_list if s.endswith('_cell e_chk')]
        to_import_indexes=[]
        for marked_decay in to_import_list:
            cond = dpg.get_value(marked_decay)
            if cond:
                to_import_indexes.append(int(marked_decay.split('_')[4]))
        to_import_indexes.sort()
        jsn_file = 'TCSPC_decay_library.json'
        jsn_path = os.path.join('res','Lib','json',jsn_file)
        with open(jsn_path) as json_library:
            jsn_dict = json.load(json_library)
        for i in to_import_indexes:
            name = dpg.get_value('decays_lib_tab_row_'+str(i)+'_cell a_text')
            decay_npy_data = np.load(jsn_dict[channel][name]['npy_path'] )
            if not name in self.curve_list:
                self.curve_list.append(name)
            else:
                pass
        self.unmount_decay_table()
        self.mount_decay_table(self.curve_list)
        for marked_decay in to_import_list:
            dpg.set_value(marked_decay,False)
        tmp_series = dpg.get_aliases()
        tmp_series = [r for r in tmp_series if 'tag_series_fltr_temp_import' in r]
    
        for r in tmp_series:
            dpg.delete_item(r)
    
        checked_decays = dpg.get_aliases()
        checked_decays = [d for d in checked_decays if d.startswith('decays_tab_row_')]
        checked_decays = [d for d in checked_decays if d.endswith('_cell b_chk')]
        checked_decays.sort()
    
        for i, d in enumerate(checked_decays):
            if i!=0:
                self.callback_chkbox_decay_table_mark(d)
            else:
                pass
        self.callback_Cancel_library_import('Cancel_library_import',None)
        
    def callback_Set_background_level(self,sender,app_data):
        channel = None
        if self.bg_channel_marker == None:
            pass
        elif self.bg_channel_marker == 1:
    
            channel = 1
            xs = self.tchanx1
            ys = self.tchany1
    
    
        elif self.bg_channel_marker == 2:
            channel = 2
            xs = self.tchanx2
            ys = self.tchany2
    
        else:
            pass
    
        bg_df_val = np.quantile(ys/np.sum(ys),0.3)
        if app_data:
            if dpg.get_value('add_bg_range'):
                dpg.set_value('add_bg_range',False)
                dpg.configure_item('Background_RLL_line',default_value=0)
                dpg.configure_item('Background_RUL_line',default_value=0)
                dpg.hide_item('Background_RLL_line')
                dpg.hide_item('Background_RUL_line')
    
            dpg.show_item('Background_level_line')
            noise_LVL = dpg.get_value('Background_level_line')
            substracted_tchany = (ys/np.sum(ys))-noise_LVL
            self.make_smooth(subtr,substracted_tchany)
            dpg.set_value('tag_series_fltr_subtr', [xs, substracted_tchany])
            dpg.configure_item("tag_series_fltr_subtr", label = 'Subtracted')
            minimum = min(abs(substracted_tchany[np.where(substracted_tchany!=0)[0]]))/2
            if bg_df_val<= minimum:
                bg_df_val = 1.1*minimum
            dpg.configure_item('Background_level_line',default_value=bg_df_val)
            dpg.set_axis_limits("yaxis_tltr", minimum ,max(substracted_tchany)*2)
            self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]=xs
            self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]=substracted_tchany*np.sum(ys)
            dpg.configure_item('Add_decay_to_lib',enabled=True)
            dpg.set_value('decays_tab_row_'+str(0)+'_cell b_chk',True)
            self.filtering_routine['Channel '+str(channel)]['BG']=True
    
        else:
            dpg.hide_item('Background_level_line')
            dpg.configure_item('Background_level_line',default_value=0)
            dpg.set_value('tag_series_fltr_subtr', [[], []])
            dpg.configure_item("tag_series_fltr_subtr", label = '')
            self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]=[]
            self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]=[]
            ys=ys/np.sum(ys)
            minimum = min(abs(ys[np.where(ys!=0)[0]]))/2
            dpg.set_axis_limits("yaxis_tltr", minimum ,max(ys)*2)
            dpg.set_value('decays_tab_row_'+str(0)+'_cell b_chk',False)
            self.filtering_routine['Channel '+str(channel)]['BG']=False
            dpg.configure_item('Add_decay_to_lib',enabled=False)


    def callback_Set_background_range(self,sender,app_data):
        
        channel = None
        if self.bg_channel_marker == None:
            pass
        elif self.bg_channel_marker == 1:
            channel = 1
            xs = self.tchanx1*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            ys = self.tchany1
    
    
        elif self.bg_channel_marker == 2:
            channel = 2
            xs = self.tchanx2*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
            ys = self.tchany2
    
    
        else:
            pass
        bgrl_df_val = max(xs)-2*(max(xs)-min(xs))/5
        bgru_df_val = max(xs)
        if app_data:
            dpg.configure_item('Background_RLL_line',default_value=bgrl_df_val)
            dpg.configure_item('Background_RUL_line',default_value=bgru_df_val)
            dpg.show_item('Background_RLL_line')
            dpg.show_item('Background_RUL_line')
            noise_LVL = np.mean((ys/np.sum(ys))[np.where((xs>=bgrl_df_val) & (xs<=bgru_df_val))[0]])
            substracted_tchany = (ys/np.sum(ys))-noise_LVL
            subtr = self.make_smooth(xs,substracted_tchany)
            dpg.set_value('tag_series_fltr_subtr', [subtr['xs'].values, subtr.smth.values])
            dpg.configure_item("tag_series_fltr_subtr", label = 'Subtracted')
            minimum = min(abs(substracted_tchany[np.where(substracted_tchany!=0)[0]]))
            dpg.set_axis_limits("yaxis_tltr", minimum/2 ,max(substracted_tchany)*2)
            self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]=xs
            self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]=subtr.smth.values*np.sum(ys)
            dpg.configure_item('Add_decay_to_lib',enabled=True)
            dpg.set_value('decays_tab_row_'+str(0)+'_cell b_chk',True)
            self.filtering_routine['Channel '+str(channel)]['BG']=True
            self.filtering_routine['Channel '+str(channel)]['BG_rng']=(bgrl_df_val,bgru_df_val)
    
    
        else:
            dpg.configure_item('Background_RLL_line',default_value=0)
            dpg.configure_item('Background_RUL_line',default_value=0)
            dpg.hide_item('Background_RLL_line')
            dpg.hide_item('Background_RUL_line')
            dpg.set_value('tag_series_fltr_subtr', [[], []])
            dpg.configure_item("tag_series_fltr_subtr", label = '')
            self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]=[]
            self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]=[]
            ys=ys/np.sum(ys)
            minimum = min(abs(ys[np.where(ys!=0)[0]]))/2
            dpg.set_axis_limits("yaxis_tltr", minimum ,max(ys)*2)
            dpg.set_value('decays_tab_row_'+str(0)+'_cell b_chk',False)
            dpg.configure_item('Add_decay_to_lib',enabled=False)
            self.filtering_routine['Channel '+str(channel)]['BG']=False
    

    def callback_add_decay_to_lib(self,sender,app_data):
        
        dpg.show_item('fl_bg_win_group_2')
        dpg.show_item('fl_decay_params_group')
        dpg.show_item('get_wavelength')
        dpg.show_item('get_channel')
        dpg.show_item('get_name')
        dpg.show_item('get_tcspc_resolution')
        dpg.show_item('get_decay_description')
        dpg.show_item('fl_bg_win_submit_decay')
        dpg.show_item('Cancel_decay_submission')
        dpg.show_item('Proceed_decay_submission')

    def callback_apply_to_all_ptus(self):
        
        self.mount_status_modal()
        for i,an_file in enumerate(self.files):
            perc = int(np.round(i/len(self.files)*100))
        
            dpg.configure_item('loading_butt',label=an_file)
            dpg.configure_item('loading_cnt_butt',label=str(perc)+'%')
            self.extract_from_ptu(self.last_directory,
                                  an_file,
                                  self.B_limit_ch_1,
                                  self.U_limit_ch_1,
                                  self.B_limit_ch_2,
                                  self.U_limit_ch_2)
   
    
        dpg.configure_item('loading_cnt_butt',label=str(100)+'%')
        self.unmount_status_modal()
    



    def callback_apply_to_files(self):
    
        dpg.configure_item('PTU_dir_dialog',show=True)
    
        
    def callback_apply_to_single_ptus(self):
        
        an_file = self.anal_file.split('/')[-1]   
        self.mount_status_modal()
        dpg.configure_item('loading_butt',label=an_file)
        self.extract_from_ptu(self.last_directory,
                              an_file,
                              self.B_limit_ch_1,
                              self.U_limit_ch_1,
                              self.B_limit_ch_2,
                              self.U_limit_ch_2)
        
    
        dpg.configure_item('loading_cnt_butt',label=str(100)+'%')
    
        self.unmount_status_modal()
    
    
    def callback_cancel_submission(self,sender,app_data):

        dpg.hide_item('fl_bg_win_group_2')
        dpg.hide_item('fl_decay_params_group')
        dpg.hide_item('get_wavelength')
        dpg.hide_item('get_channel')
        dpg.hide_item('get_name')
        dpg.hide_item('get_tcspc_resolution')
        dpg.hide_item('get_decay_description')
        dpg.hide_item('fl_bg_win_submit_decay')
        dpg.hide_item('Cancel_decay_submission')
        dpg.hide_item('Proceed_decay_submission') 
    
    
    
    def callback_check_lib_decay(self,sender,app_data):
        
        channel = None
        if self.bg_channel_marker == None:
                pass
        elif self.bg_channel_marker == 1:
            channel = 'Channel 1'
            rawx = self.tchanx1
            rawy = self.tchany1
    
    
        elif self.bg_channel_marker == 2:
            channel = 'Channel 2'
            rawx = self.tchanx2
            rawy = self.tchany2
    
        else:
            pass
    
    
    
        jsn_file = 'TCSPC_decay_library.json'
        jsn_path = os.path.join('res','Lib','json',jsn_file)
        with open(jsn_path) as json_library:
            jsn_dict = json.load(json_library)
        i = int(sender.split('_')[4])
    
        name = dpg.get_value('decays_lib_tab_row_'+str(i)+'_cell a_text')
        anal_file_tscpc_res = str(self.fl_bg_curves_dict[channel][self.anal_file]['TCSPC_resolution'])
        anal_file_tscpc_chan = str(self.fl_bg_curves_dict[channel][self.anal_file]['TCSPC_channels'])
        loaded_tcspc_res = jsn_dict[channel][name]['TCSPC_resolution']
        loaded_tcspc_chan = jsn_dict[channel][name]['TCSPC_channels']
        org_axis_limits = dpg.get_axis_limits('yaxis_tltr')
        org_y = rawy/np.sum(rawy)
        if dpg.get_value(sender):
            if anal_file_tscpc_res != loaded_tcspc_res:
                dpg.show_item('No_match_notiffication')
                dpg.set_value('No_match_notiffication',
                              'TCSPC resolution of the main file ('+str(anal_file_tscpc_res)+' ps) does not match the resolution of the selected decay ('+str(loaded_tcspc_res)+' ps).')
                dpg.hide_item('Proceed_library_import')
            elif str(anal_file_tscpc_chan) != str(loaded_tcspc_chan):
                dpg.show_item('No_match_notiffication')
                dpg.set_value('No_match_notiffication',
                              'Number of TCSPC channels of the main file ('+str(anal_file_tscpc_chan)+') does not match the number of channels in the selected decay ('+str(loaded_tcspc_chan)+').')
                dpg.hide_item('Proceed_library_import')
            else:
    
    
                dpg.show_item('Proceed_library_import')
    
                decay_npy_data = np.load(jsn_dict[channel][name]['npy_path'] )
    
                tmp_xs = decay_npy_data[0]*self.tau_resolution-(decay_npy_data[0]*self.tau_resolution)[0]
                tmp_ys = decay_npy_data[1]/np.sum(decay_npy_data[1])
                dpg.add_scatter_series(tmp_xs, tmp_ys,
                                        parent='yaxis_tltr',
                                    tag="tag_series_fltr_temp_import"+str(i),
                                    label='To be imported (#'+str(i+1)+')')
                dpg.bind_item_theme("tag_series_fltr_temp_import"+str(i), "plot_bg_filter_theme")
                minimum = min(abs(tmp_ys[np.where(tmp_ys!=0)[0]]))/2
                dpg.set_axis_limits("yaxis_tltr", minimum ,max(tmp_ys)*2)
        else:
    
            dpg.show_item('Proceed_library_import')
            dpg.hide_item('No_match_notiffication')
            dpg.set_value('No_match_notiffication','')
    
            tmp_series = dpg.get_aliases()
    
            tmp_series = [r for r in tmp_series if 'tag_series_fltr_temp_import'+str(i) in r]
    
            for r in tmp_series:
                dpg.delete_item(r)
    
            minimum = min(abs(org_y[np.where(org_y!=0)[0]]))/2
            dpg.set_axis_limits("yaxis_tltr", minimum ,max(org_y)*2)
    
    
    def callback_chkbox_decay_table_mark(self,sender):
        
        channel = None
        if self.bg_channel_marker == None:
                pass
        elif self.bg_channel_marker == 1:
            channel = 'Channel 1'
            self.tchanx1 = self.fl_bg_curves_dict[channel][self.anal_file]['tchanx1']
            rawdatax_t = self.tchanx1*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            rawdatay = self.fl_bg_curves_dict[channel][self.anal_file]['tchany1']
            subtry = self.fl_bg_curves_dict[channel][self.anal_file]['subtract_bg']['tchany1']
    
    
        elif self.bg_channel_marker == 2:
            channel = 'Channel 2'
            self.tchanx2 = self.fl_bg_curves_dict[channel][self.anal_file]['tchanx2']
            rawdatax_t = self.tchanx2*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
            rawdatay = self.fl_bg_curves_dict[channel][self.anal_file]['tchany2']
            subtry = self.fl_bg_curves_dict[channel][self.anal_file]['subtract_bg']['tchany2']
    
        else:
            pass
        jsn_file = 'TCSPC_decay_library.json'
        jsn_path = os.path.join('res','Lib','json',jsn_file)
        with open(jsn_path) as json_library:
            jsn_dict = json.load(json_library)
    
    
        value = dpg.get_value(sender)
    
        if not value:
    
            rm_imp_ser = dpg.get_aliases()
    
            rm_imp_ser = [r for r in rm_imp_ser if r.startswith('tag_series_fltr_imported')]
    
            for r in rm_imp_ser:
                dpg.delete_item(r)
            decay_index = int(sender.split('_')[3])
            decay_name = dpg.get_value('decays_tab_row_'+str(decay_index)+'_cell a_text')
            try:
                
                del self.filtering_routine[channel][decay_name]
    
            except:
                pass
    
        else:
    
            decay_index = int(sender.split('_')[3])
            if decay_index == 0:
                pass
            else:
                decay_name = dpg.get_value('decays_tab_row_'+str(decay_index)+'_cell a_text')
    
                nppath = jsn_dict[channel][decay_name]['npy_path']
                npdata = np.load(nppath)
                df = pd.DataFrame(npdata.T,columns=['time','ydata'])
                df.ydata = df.ydata/df.ydata.sum()
    
                adjusted = self.adjust_curves(df, pd.Series(rawdatax_t).to_frame())
    
                npdata_X=adjusted.time.values
                npdata_Y=adjusted.ydata.values
    
                minlist=[]
                maxlist=[]
                npdata_min = abs(adjusted.ydata.where(adjusted.ydata!=0).dropna()).min()/2
                npdata_max = adjusted.ydata.max()*2
                minlist.append(npdata_min)
                maxlist.append(npdata_max)
                rawdatay = rawdatay/np.sum(rawdatay)
    
                raw_min = min(abs(rawdatay[np.where(rawdatay!=0)[0]]))/2
                raw_max = max(rawdatay)*2
                minlist.append(raw_min)
                maxlist.append(raw_max)
                if len(subtry)!=0:
                    subtry = subtry/np.sum(subtry)
                    substr_min = min(abs(subtry[np.where(subtry!=0)[0]]))/2
                    substr_max = max(subtry)*2
                    minlist.append(substr_min)
                    maxlist.append(substr_max)
                else:
                    pass
    
    
    
                minimum = raw_min/100
                maximum = max(maxlist)
    
    
                dpg.add_scatter_series(npdata_X, npdata_Y,
                                            parent='yaxis_tltr',tag="tag_series_fltr_imported_"+decay_name,label=decay_name[:5])
                dpg.bind_item_theme("tag_series_fltr_imported_"+decay_name, "plot_bg_filter_theme")
                dpg.set_axis_limits("yaxis_tltr", minimum ,maximum)
    

    def callback_drag_Background_Range_line(self,sender,app_data):
        
        channel = None
        if self.bg_channel_marker == None:
            pass
        elif self.bg_channel_marker == 1:
            channel = 1
            xs = self.tchanx1*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            ys = self.tchany1
    
        elif self.bg_channel_marker == 2:
            channel = 2
            xs = self.tchanx2*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
            ys = self.tchany2
        else:
            pass
    
    
        if str(sender).isdigit():
    
            sender = dpg.get_item_alias(sender)
        else:
            pass
    
    
        if sender == 'Background_RLL_line':
            lower_range = int(dpg.get_value('Background_RLL_line'))
            upper_range = int(dpg.get_value('Background_RUL_line'))
            if lower_range>upper_range:
                lower_range=upper_range
                dpg.set_value('Background_RLL_line',lower_range)
        elif sender == 'Background_RUL_line':
            lower_range = int(dpg.get_value('Background_RLL_line'))
            upper_range = int(dpg.get_value('Background_RUL_line'))
            if upper_range<lower_range:
                upper_range=lower_range
                dpg.set_value('Background_RUL_line',upper_range)
    
        noise_LVL = np.mean((ys/np.sum(ys))[np.where((xs>=lower_range) & (xs<=upper_range))[0]])
    
    
        substracted_tchany = (ys/np.sum(ys))-noise_LVL
    
        subtr = self.make_smooth(xs,substracted_tchany)
        dpg.set_value('tag_series_fltr_subtr', [subtr['xs'].values, subtr.smth.values])
        dpg.configure_item("tag_series_fltr_subtr", label = 'Subtracted')
        self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]=subtr['xs'].values
        self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]=subtr.smth.values*np.sum(ys)
    
        minimum = min(subtr.smth.where(subtr.smth!=0).dropna())/2
        dpg.set_axis_limits("yaxis_tltr", minimum ,subtr.smth.max()*2)

    def callback_drag_Background_level_line(self,sender,app_data):
        
        channel = None
        if self.bg_channel_marker == None:
            pass
        elif self.bg_channel_marker == 1:
            channel = 1
            xs = self.tchanx1*self.tau_resolution-(self.tchanx1*self.tau_resolution)[0]
            ys = self.tchany1
    
        elif self.bg_channel_marker == 2:
            channel = 2
            xs = self.tchanx2*self.tau_resolution-(self.tchanx2*self.tau_resolution)[0]
            ys = self.tchany2
        else:
            pass
    
        noise_LVL = dpg.get_value(sender)
    
        substracted_tchany = (ys/np.sum(ys))-noise_LVL
    
        subtr = self.make_smooth(xs,substracted_tchany)
    
        dpg.set_value('tag_series_fltr_subtr', [subtr['xs'].values, subtr.smth.values])
    
    
        self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]=xs
        self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]=subtr.smth.values*np.sum(ys)


    def callback_import_from_library(self,sender,app_data):
        
        self.unmount_LIB_decay_table()
        dpg.show_item('fl_bg_win_group_3')
    
        jsn_file = 'TCSPC_decay_library.json'
        jsn_path = os.path.join('res','Lib','json',jsn_file)
        channel = None
        if self.bg_channel_marker == None:
                pass
        elif self.bg_channel_marker == 1:
            channel = 'Channel 1'
    
    
        elif self.bg_channel_marker == 2:
            channel = 'Channel 2'
    
        else:
            pass
    
        if os.path.exists(jsn_path):
            with open(jsn_path) as json_library:
                jsn_dict = json.load(json_library)
    
            try:
                decay_list = jsn_dict[channel].keys()
                dpg.show_item('decays_tab_lib_list_tag')
                dpg.show_item('Proceed_library_import')
                dpg.show_item('Cancel_library_import')
                self.mount_LIB_decay_table(decay_list,jsn_dict[channel])
            except:
                dpg.show_item('empty_library_notiffication')
                dpg.show_item('Cancel_library_import')
    
        else:
            dpg.show_item('Cancel_library_import')
            dpg.show_item('empty_library_notiffication')
    

    def callback_listbox(self,sender,app_data):
        self.fl_bg_curves_dict ={}
        self.anal_file = os.path.join(self.last_directory,app_data)
        self.load_ptu(self.anal_file)


    def callback_ok_button(self,sender):
        dpg.hide_item('fl_bg_win_group_4')
        dpg.hide_item('no_curves_notiffication')
        dpg.hide_item('OK_button')
        dpg.configure_item('Calculate_filters',enabled=True)


    def callback_proceed_submission(self,sender,app_data):
        wavelength = dpg.get_value('get_wavelength')
        if wavelength == '' or wavelength == 'ERROR!!!':
    
            dpg.set_value('get_wavelength','ERROR!!!')
        else:
            channel_name = dpg.get_value('get_channel')
            TCSPC_resolution = dpg.get_value('get_tcspc_resolution')
            channel = None
            if self.bg_channel_marker == None:
                pass
            elif self.bg_channel_marker == 1:
                channel = 1
                xs = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]
                ys = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]
    
            elif self.bg_channel_marker == 2:
                channel = 2
                xs = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchanx'+str(channel)]
                ys = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['subtract_bg']['tchany'+str(channel)]
            else:
                pass
    
            data_array = np.concatenate([xs,ys]).reshape((len([xs,ys]),len([xs,ys][-1])))
            if dpg.get_value('get_name') == '' or dpg.get_value('get_name') == 'Name (optional)':
                name = self.fl_bg_curves_dict['Channel '+str(channel)][self.anal_file]['name']
            else:
                name = dpg.get_value('get_name')
    
    
            if dpg.get_value('get_decay_description') == '' or dpg.get_value('get_decay_description') == 'Type descrption here (opitonal)':
                describe = ''
            else:
                describe = dpg.get_value('get_decay_description')
    
            jsn_file = 'TCSPC_decay_library.json'
            jsn_path = os.path.join('res','Lib','json',jsn_file)
            npy_file = name+'.npy'
            npy_path = os.path.join('res','Lib','npy',npy_file)
            if os.path.exists(jsn_path):
    
                with open(jsn_path) as json_library:
                    jsn_dict = json.load(json_library)
    
                jsn_dict[channel_name][name]={
                        'EXC-wavelength':wavelength,
                        'TCSPC_resolution':TCSPC_resolution,
                        'TCSPC_channels':self.ntchannels,
                        'Description':describe,
                        'npy_path':npy_path
                        }
            else:
    
                jsn_dict = {
                    channel_name:{
                        name:{
                        'EXC-wavelength':wavelength,
                        'TCSPC_resolution':TCSPC_resolution,
                        'TCSPC_channels':self.ntchannels,
                        'Description':describe,
                        'npy_path':npy_path
                        }
    
                    }
    
                }
    
            np.save(npy_path,data_array)
            with open(jsn_path, 'w') as f:
                json.dump(jsn_dict, f, indent=4, sort_keys=False)
                f.close()
    
            dpg.hide_item('fl_bg_win_group_2')
            dpg.hide_item('fl_decay_params_group')
            dpg.hide_item('get_wavelength')
            dpg.hide_item('get_channel')
            dpg.hide_item('get_tcspc_resolution')
            dpg.hide_item('get_name')
            dpg.hide_item('fl_bg_win_submit_decay')
            dpg.hide_item('Cancel_decay_submission')
            dpg.hide_item('Proceed_decay_submission')
            dpg.hide_item('get_decay_description')


    def callback_select_filter_for_batch(self,sender,app_data):
    
        value=app_data
        channel = int(sender.split('_')[2])
    
        checkboxes = dpg.get_aliases()
        checkboxes = [ch for ch in checkboxes if ch.startswith('filters_ch_'+str(channel)+'_tab_list_row_')]
        checkboxes = [ch for ch in checkboxes if ch.endswith('_cell b_chk')]
        checkboxes = [ch for ch in checkboxes if ch != sender]
    
        if value:
            for ch in checkboxes:
                dpg.set_value(ch,False)

    def callback_skip_lines_check(self,sender,app_data):

        if app_data:
            dpg.configure_item('skip_lines_drag',enabled=True)
        else:
            dpg.configure_item('skip_lines_drag',enabled=False)

    def make_afterpulsing_weight(self,filters_dict,channel):
        F = filters_dict['Afterpulsing and background']
        
        weight = F/max(F)
        weight = np.where(weight>0,weight,0)
        
        return weight

    def extract_from_ptu(self,folder,ptu_file,LLim_ch_1,ULim_ch_1,LLim_ch_2,ULim_ch_2):
        dpg.configure_item('loading_status',label='Loading')
    
        np.seterr(divide='ignore')
        file=ptu_file.replace('.ptu','')
        path_to_file = os.path.join(folder,ptu_file)
        ptu_image  = PTUreader(path_to_file, print_header_data = False)
        mode = ptu_image.head['UsrPulseCfg']
        self.tau_resolution = ptu_image.head["MeasDesc_Resolution"]*1e9
        tcspc_reolution = int(np.round(self.tau_resolution*1e-9*1e12))
        sync_rate = ptu_image.head['TTResult_SyncRate']
    
    
        if not LLim_ch_1 == None:
            LLim_ch_1 = int(np.floor(LLim_ch_1/self.tau_resolution))
        else:
            pass
        if not ULim_ch_1 == None:
            ULim_ch_1 = int(np.ceil(ULim_ch_1/self.tau_resolution))
        else:
            pass
        if not LLim_ch_2 == None:
            LLim_ch_2 = int(np.floor(LLim_ch_2/self.tau_resolution))
        else:
            pass
        if not ULim_ch_2 == None:
            ULim_ch_2 = int(np.ceil(ULim_ch_2/self.tau_resolution))
        else:
            pass
    
        if not dpg.get_value('skip_lines_check'):
    
            flim_data_stack, intensity_image_all_channels,special,sync,im_channels,tcspc = ptu_image.get_flim_data_stack()
        else:
    
            flim_data_stack, intensity_image_all_channels,special,sync,im_channels,tcspc = ptu_image.get_flim_data_stack_omit(dpg.get_value('skip_lines_drag'))
    
        number_of_frames = int(pd.Series(special).where(pd.Series(special)==4).dropna().count())
    
    
        line_width = ptu_image.head['ImgHdr_PixX']
        number_of_lines = ptu_image.head['ImgHdr_PixY']
        pixel_size = 1e3*ptu_image.head['ImgHdr_PixResol']
        special_markers = pd.DataFrame(special,columns=['marker'])
        special_markers['sync'] = sync
        special_markers['channel'] = im_channels
        special_markers['tcspc'] = tcspc*tcspc_reolution
        special_markers['event'] = sync/sync_rate
        special_markers['dif'] = special_markers.where(special_markers.marker!=0).where(special_markers.marker!=4).dropna().event.diff()
        pixel_dwell = float(np.round(1e6*(special_markers.dropna().where(special_markers.marker==2).dropna().dif.to_frame()/line_width).mean().values,2))
        if flim_data_stack.ndim == 4:
            number_of_channels = flim_data_stack.shape[2]
            Resolution = str(flim_data_stack.shape[0])+'x'+str(flim_data_stack.shape[1])
            ccnt =0
            channels = []
            for channel in range(number_of_channels):
                channel_data = np.sum(flim_data_stack[:,:,channel,:],axis=2)
                data_sum = channel_data.sum()
    
                if data_sum!=0:
                    ccnt +=1
    
                    channels.append(channel)
            number_of_channels = ccnt
    
        info_dict = {
                    'L_file':ptu_file,
                    'Pixels per line': int(line_width),
                    'Number of lines': int(number_of_lines),
                    'Pixels size': int(pixel_size),
                    'Number of frames': int(number_of_frames),
                    'Pixel dwell':float(pixel_dwell),
                    'Lifetime resolution':float(self.tau_resolution)}
        infoname = file+'.info'
    
        self.ntchannels = flim_data_stack.shape[3]
        json_pickle_all = {'File info':info_dict
                          }
    
    
        for channel in range(number_of_channels):
    
    
            tau_pickle_name = file+'_taus_ch_'+str(channels[channel]+1)+'.pck'
            full_tau_pickle_name = file+'_fulltaus_ch_'+str(channels[channel]+1)+'.pck'
            pickle_name = file+'_ch_'+str(channels[channel]+1)+'.pck'
            png_name = file+'_ch_'+str(channels[channel]+1)+'.png'
            png_FC_name = file+'_ch_'+str(channels[channel]+1)+'_FC.png'
            csv_name = file+'_ch_'+str(channels[channel]+1)+'.csv'
            np_LT_name = file+'_LT_ch_'+str(channels[channel]+1)
            np_int_name = file+'_INT_ch_'+str(channels[channel]+1)
    
    
    
            if mode == 'PIE':
    
    
    
                tau = np.linspace(0,self.ntchannels,self.ntchannels, dtype = int)*self.tau_resolution
                XS = np.linspace(0,self.ntchannels,self.ntchannels, dtype = int)
                self.midle_sep = self.ntchannels//2
                if channels[channel] == 0:
                    if not flim_data_stack.shape[3] % 2 == 0:
                        lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_1+1:ULim_ch_1]
                        xs = XS[np.where(XS>LLim_ch_1)[0]]
                    else:
                        lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_1:ULim_ch_1]
                        
                        xs = XS[np.where(XS>=LLim_ch_1)[0]]
                        
                    ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                    
                    ys = np.sum(ys, axis = 0).astype(float)
                    fYS = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                    fYS = np.sum(fYS, axis = 0).astype(float)
                    if not flim_data_stack.shape[3] % 2 == 0:
                        ys = ys[np.where(XS>LLim_ch_1)[0]]
                    else:
                        ys = ys[np.where(XS>=LLim_ch_1)[0]]
                    if dpg.get_value('use_as_statistical_filters_chkbx_ch_1'):
                        dpg.configure_item('loading_status',label='Calculating filters channel 1')
                        filtering_decays_ch_1 = self.prepare_input_to_calculate_filters_from_routine(xs,ys,self.ntchannels,tcspc_reolution,self.filtering_routine,1)
    
                        FILTRY_ch_1 = self.calculate_stat_filter(filtering_decays_ch_1,ys)
    
                        dpg.configure_item('loading_status',label='Calculating weights channel 1')
                        FWeight = filter_weight_ch_1 = self.make_weight_from_filters(FILTRY_ch_1,1)
                        afterpulsing_weight = self.make_afterpulsing_weight(FILTRY_ch_1,1)
                        dpg.configure_item('loading_status',label='Filtering channel 1')
                        filtered_image_data=np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
                        afterpulsing_data =np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
    
    
                        for j in range(lifetime_data.shape[2]):
                            filtered_image_data[:,:,j] = lifetime_data[:,:,j]*filter_weight_ch_1[j]
                            afterpulsing_data[:,:,j] = lifetime_data[:,:,j]*afterpulsing_weight[j]
                        lifetime_data = filtered_image_data
                        background = afterpulsing_data

                        
                        filtered_taus = np.sum(lifetime_data, axis=0)
                        filtered_taus = np.sum(filtered_taus, axis = 0).astype(float)
                        filtered_taus = np.atleast_1d(filtered_taus)
        
    
                    else:
                        background = np.zeros_like(lifetime_data)
                        FWeight = afterpulsing_weight = None
                        filtered_taus = np.sum(np.zeros_like(xs), axis=0)
                        filtered_taus = np.sum(filtered_taus, axis = 0).astype(float)
                        
                        filtered_taus = np.atleast_1d(filtered_taus)
                        
                        pass
    
    
    
                else:
                    
                    
                    if not flim_data_stack.shape[3] % 2 == 0:
                        
                        lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_2:ULim_ch_2+1]
                        xs = XS[np.where(XS<=ULim_ch_2)[0]]
                    else:
                        lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_2:ULim_ch_2]
                        xs = XS[np.where(XS<ULim_ch_2)[0]]
                    
                    ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                    ys = np.sum(ys, axis = 0).astype(float)
                    fYS = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                    fYS = np.sum(fYS, axis = 0).astype(float)
                    if not flim_data_stack.shape[3] % 2 == 0:
                        ys = ys[np.where(XS<=ULim_ch_2)[0]]
                    else:
                        ys = ys[np.where(XS<ULim_ch_2)[0]]
                    if dpg.get_value('use_as_statistical_filters_chkbx_ch_2'):
                        dpg.configure_item('loading_status',label='Calculating filters channel 2')
                        filtering_decays_ch_2 = self.prepare_input_to_calculate_filters_from_routine(xs,ys,self.ntchannels,tcspc_reolution,self.filtering_routine,2)
    
                        FILTRY_ch_2 = self.calculate_stat_filter(filtering_decays_ch_2,ys)
    
                        dpg.configure_item('loading_status',label='Calculating weights channel 1')
                        FWeight = filter_weight_ch_2 = self.make_weight_from_filters(FILTRY_ch_2,2)
                        afterpulsing_weight = self.make_afterpulsing_weight(FILTRY_ch_2,2)
                        dpg.configure_item('loading_status',label='Filtering channel 2')
                        filtered_image_data=np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
                        afterpulsing_data =np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
    
                        for j in range(lifetime_data.shape[2]):
                            filtered_image_data[:,:,j] = lifetime_data[:,:,j]*filter_weight_ch_2[j]
                            afterpulsing_data[:,:,j] = lifetime_data[:,:,j]*afterpulsing_weight[j]
                        lifetime_data = filtered_image_data
                        background = afterpulsing_data

                        filtered_taus = np.sum(lifetime_data, axis=0)
                        filtered_taus = np.sum(filtered_taus, axis = 0).astype(float)
                        filtered_taus = np.atleast_1d(filtered_taus)
    
                    else:
                        background = np.zeros_like(lifetime_data)
                        FWeight = afterpulsing_weight = None
                        filtered_taus = np.sum(np.zeros_like(xs), axis=0)
                        filtered_taus = np.sum(filtered_taus, axis = 0).astype(float)
                        filtered_taus = np.atleast_1d(filtered_taus)
                        pass
            else:
                NT_channels = flim_data_stack.shape[3]
    
                tau = np.linspace(0,self.ntchannels,self.ntchannels, dtype = int)*self.tau_resolution
                XS = np.linspace(0,self.ntchannels,self.ntchannels, dtype = int)
    
                if ULim_ch_1<NT_channels:
                    
                    ULim_ch_1 = NT_channels
                else:
                    pass
                if channels[channel] == 0:
    
                    lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_1:ULim_ch_1]
                    xs=XS
                    ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                    ys = np.sum(ys, axis = 0).astype(float)
                    fYS = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                    fYS = np.sum(fYS, axis = 0).astype(float)
                    if dpg.get_value('use_as_statistical_filters_chkbx_ch_1'):
                        dpg.configure_item('loading_status',label='Calculating filters channel 1')
                        filtering_decays_ch_1 = self.prepare_input_to_calculate_filters_from_routine(xs,ys,self.ntchannels,tcspc_reolution,self.filtering_routine,1)
                        FILTRY_ch_1 = self.calculate_stat_filter(filtering_decays_ch_1,ys)
    
                        dpg.configure_item('loading_status',label='Calculating weights channel 1')
                        FWeight = filter_weight_ch_1 = self.make_weight_from_filters(FILTRY_ch_1,1)
                        afterpulsing_weight = self.make_afterpulsing_weight(FILTRY_ch_1,1)
                        dpg.configure_item('loading_status',label='Filtering channel 1')
                        filtered_image_data=np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
                        afterpulsing_data =np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
                        for j in range(lifetime_data.shape[2]):
                            filtered_image_data[:,:,j] = lifetime_data[:,:,j]*filter_weight_ch_1[j]
                            afterpulsing_data[:,:,j] = lifetime_data[:,:,j]*afterpulsing_weight[j]
                        lifetime_data = filtered_image_data
                        background = afterpulsing_data

                        filtered_taus = np.sum(lifetime_data, axis=0)
                        filtered_taus = np.sum(filtered_taus, axis = 0).astype(float)
                        filtered_taus = np.atleast_1d(filtered_taus)
    
                    else:
                        background = np.zeros_like(lifetime_data)
                        FWeight = afterpulsing_weight = None
                        filtered_taus = np.sum(np.zeros_like(xs), axis=0)
                        filtered_taus = np.sum(filtered_taus, axis = 0).astype(float)
                        filtered_taus = np.atleast_1d(filtered_taus)
                        pass
    
                else:
                    lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_2:ULim_ch_2]
                    xs=XS
                    ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
    
                    ys = np.sum(ys, axis = 0).astype(float)
                    fYS = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                    fYS = np.sum(fYS, axis = 0).astype(float)
                    if dpg.get_value('use_as_statistical_filters_chkbx_ch_2'):
                        dpg.configure_item('loading_status',label='Calculating filters channel 2')
                        filtering_decays_ch_2 = self.prepare_input_to_calculate_filters_from_routine(xs,ys,self.ntchannels,tcspc_reolution,self.filtering_routine,2)
                        FILTRY_ch_2 = self.calculate_stat_filter(filtering_decays_ch_2,ys)
    
                        dpg.configure_item('loading_status',label='Calculating weights channel 2')
                        FWeight = filter_weight_ch_2 = self.make_weight_from_filters(FILTRY_ch_2,2)
                        afterpulsing_weight = self.make_afterpulsing_weight(FILTRY_ch_2,2)
                        dpg.configure_item('loading_status',label='Filtering channel 2')
                        filtered_image_data=np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
                        afterpulsing_data =np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
                        for j in range(lifetime_data.shape[2]):
                            filtered_image_data[:,:,j] = lifetime_data[:,:,j]*filter_weight_ch_2[j]
                            afterpulsing_data[:,:,j] = lifetime_data[:,:,j]*afterpulsing_weight[j]
    
                        lifetime_data = filtered_image_data
                        background = afterpulsing_data

                        filtered_taus = np.sum(lifetime_data, axis=0)
                        filtered_taus = np.sum(filtered_taus, axis = 0).astype(float)
                        filtered_taus = np.atleast_1d(filtered_taus)
    
                    else:
                        background = np.zeros_like(lifetime_data)
                        FWeight = afterpulsing_weight = None
                        filtered_taus = np.sum(np.zeros_like(xs), axis=0)
                        filtered_taus = np.sum(filtered_taus, axis = 0).astype(float)
                        filtered_taus = np.atleast_1d(filtered_taus)
                        pass
    
            taus = pd.DataFrame(xs,columns = ['Tau'])
            fulltaus = pd.DataFrame(XS,columns = ['Tau'])
    
    
            taus['Intensity'] = ys
            fulltaus['Intensity'] = fYS

            if len(xs) != len(filtered_taus):
            
                if len(xs) > len(filtered_taus):
                    
                    xs = xs[:len(filtered_taus)]
                else:
                    
                    filtered_taus = filtered_taus[:len(xs)]
            
            filtered_taus_DF = pd.DataFrame(xs, columns=['Tau'])
            filtered_taus_DF['Intensity'] = filtered_taus
            
            filtered_taus_DF = pd.DataFrame(xs,columns = ['Tau'])
            
            filtered_taus_DF['Intensity'] = filtered_taus
    
    
    
    
            intensity = np.sum(lifetime_data, axis = 2)
            bgrnd = np.sum(background, axis = 2)
            lifetime = np.zeros(lifetime_data.shape)
    
            if channels[channel] == 0:
                lt_chan_range = range(LLim_ch_1,ULim_ch_1,1)
    
                if lifetime_data.shape[2]<len(lt_chan_range):
                    lt_chan_range = range(0,lifetime_data.shape[2],1)
    
                else:
    
                    pass
    
                for k,t_chan in enumerate(lt_chan_range):
    
    
    
    
                    lifetime[:,:,k]=lifetime_data[:,:,k]*t_chan*self.tau_resolution
    
            else:
                lt_chan_range = range(LLim_ch_2,ULim_ch_2,1)
    
    
                if lifetime_data.shape[2]<len(lt_chan_range):
                    lt_chan_range = range(0,lifetime_data.shape[2],1)
                else:
                    pass
    
                for k,t_chan in enumerate(lt_chan_range):
    
    
    
                    lifetime[:,:,k]=lifetime_data[:,:,k]*t_chan*self.tau_resolution
    
            inv_intensity = np.where(intensity.astype(int)!=0,1/intensity.astype(int),np.nan)
            lifetimes = np.sum(lifetime, axis = 2)*inv_intensity
    
            channel_data = np.sum(flim_data_stack[:,:,channels[channel],:],axis=2)
    
            dpg.configure_item('loading_status',label='Exporting data to png - Channel '+str(channel+1))
    
    
            to_png = (channel_data / np.max(channel_data) * 255).astype(np.uint8)
            colormap = cv2.COLORMAP_JET
    
            colored_image = cv2.applyColorMap(to_png, colormap)
    
            cv2.imwrite(os.path.join(folder, png_FC_name), colored_image)
    
            cv2.imwrite(os.path.join(folder, png_name), to_png)
    
    
            export_df = pd.DataFrame(channel_data)
                
    
            json_pickle_all['export_df_'+str(channels[channel]+1)]=export_df
            json_pickle_all['taus_'+str(channels[channel]+1)]=taus
            json_pickle_all['fulltaus_'+str(channels[channel]+1)]=fulltaus
            json_pickle_all['lifetimes_'+str(channels[channel]+1)]=lifetimes
            json_pickle_all['intensity_'+str(channels[channel]+1)]=intensity
            json_pickle_all['bgrnd_'+str(channels[channel]+1)]=bgrnd
            json_pickle_all['filter_weight_'+str(channels[channel]+1)]= FWeight
            json_pickle_all['filter_afterpulsing_weight_'+str(channels[channel]+1)] = afterpulsing_weight
            json_pickle_all['special_markers_'+str(channels[channel]+1)] = special_markers
            json_pickle_all['filtered_taus_'+str(channels[channel]+1)] = filtered_taus_DF
           
            
            
        with open(os.path.join(folder,file+'.pkl'), 'wb') as pklf:
            pickle.dump(json_pickle_all, pklf)
    
    def make_smooth(self,xs,substracted_tchany):
        subtr = pd.DataFrame(xs,columns=['xs'])
        subtr['ys']= substracted_tchany
        subtr['ys'] = subtr['ys'].where(subtr['ys']>=0,0)
        rol_win = len(substracted_tchany)//50
    
        subtr['smth'] = subtr.ys.rolling(rol_win,center=True).median().fillna(0)
    
        return subtr

    def make_weight_from_filters(self,filters_dict,channel):

        available_filters = dpg.get_aliases()
        available_filters = [af for af in available_filters if af.startswith('filters_ch_'+str(channel)+'_tab_list_row_')]
        available_filters = [af for af in available_filters if af.endswith('_cell b_chk')]
        available_filters.sort()
        filter_name = None
        for i,af in enumerate(available_filters):
    
            if dpg.get_value(af):
                filter_name = dpg.get_value('filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell a_text')
    
                break
    
        if filter_name == None:
            
            raise ValueError("No filters selected - ignoring")

        else:
            F = filters_dict[filter_name]
            
            weight = F/max(F)
            weight = np.where(weight>0,weight,0)
        return weight
    def mount_LIB_decay_table(self,decay_list,_dict):

        for i,decay in enumerate(decay_list):
            EXC_wavelength = _dict[decay]['EXC-wavelength']
            TCSPC_resolution = _dict[decay]['TCSPC_resolution']
            TCSPC_channels = _dict[decay]['TCSPC_channels']
            Description = _dict[decay]['Description']
            with dpg.table_row(tag ='decays_lib_tab_row_'+str(i),parent='decays_tab_lib_list_tag'):
                self.GI.extend(['decays_lib_tab_row_'+str(i)])
                with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell null'):
                    dpg.add_text(i+1,tag = 'decays_lib_tab_row_'+str(i)+'_cell null_text')
                    self.GI.extend(['decays_lib_tab_row_'+str(i)+'_cell null',
                                            'decays_lib_tab_row_'+str(i)+'_cell null_text'])
                with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell a'):
                    dpg.add_text(decay,tag = 'decays_lib_tab_row_'+str(i)+'_cell a_text')
                    self.GI.extend(['decays_lib_tab_row_'+str(i)+'_cell a',
                                           'decays_lib_tab_row_'+str(i)+'_cell a_text'])
                with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell b'):
                    dpg.add_text(EXC_wavelength,tag = 'decays_lib_tab_row_'+str(i)+'_cell b_text')
                    self.GI.extend(['decays_lib_tab_row_'+str(i)+'_cell b',
                                            'decays_lib_tab_row_'+str(i)+'_cell b_text'
                                           ])
                with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell c'):
                    dpg.add_text(Description,tag = 'decays_lib_tab_row_'+str(i)+'_cell c_text')
                    self.GI.extend(['decays_lib_tab_row_'+str(i)+'_cell c',
                                           'decays_lib_tab_row_'+str(i)+'_cell c_text'])
                with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell d'):
                    dpg.add_text(TCSPC_resolution,tag = 'decays_lib_tab_row_'+str(i)+'_cell d_text')
                    self.GI.extend(['decays_lib_tab_row_'+str(i)+'_cell d',
                                           'decays_lib_tab_row_'+str(i)+'_cell d_text'])
                with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell f'):
                    dpg.add_text(TCSPC_channels,tag = 'decays_lib_tab_row_'+str(i)+'_cell f_text')
                    self.GI.extend(['decays_lib_tab_row_'+str(i)+'_cell f',
                                           'decays_lib_tab_row_'+str(i)+'_cell f_text'])
                with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell e'):
                    dpg.add_checkbox(
                             default_value=False,
                        enabled=True,
                        tag = 'decays_lib_tab_row_'+str(i)+'_cell e_chk',
    
                                )
                    self.GI.extend(['decays_lib_tab_row_'+str(i)+'_cell e','decays_lib_tab_row_'+str(i)+'_cell e_chk'])
    
    
    def mount_decay_table(self,decay_list):
        
        channel = None
        if self.bg_channel_marker == None:
                pass
        elif self.bg_channel_marker == 1:
            channel = 'Channel 1'
            if_substracted = len(self.fl_bg_curves_dict[channel][self.anal_file]['subtract_bg']['tchanx1'])>0
    
        elif self.bg_channel_marker == 2:
            channel = 'Channel 2'
            if_substracted = len(self.fl_bg_curves_dict[channel][self.anal_file]['subtract_bg']['tchanx2'])>0
    
        else:
            pass
    
    
    
        for i,decay in enumerate(decay_list):
            self.GI.extend(['decays_tab_row_'+str(i),
                               'decays_tab_row_'+str(i)+'_cell #',
                              'decays_tab_row_'+str(i)+'_cell #_text',
                              'decays_tab_row_'+str(i)+'_cell a',
                              'decays_tab_row_'+str(i)+'_cell a_text',
                              'decays_tab_row_'+str(i)+'_cell b'])
            with dpg.table_row(tag ='decays_tab_row_'+str(i),parent='decays_tab_list_tag'):
                with dpg.table_cell(tag = 'decays_tab_row_'+str(i)+'_cell #'):
                    dpg.add_text(str(i+1),tag = 'decays_tab_row_'+str(i)+'_cell #_text')
                with dpg.table_cell(tag = 'decays_tab_row_'+str(i)+'_cell a'):
                    dpg.add_text(decay,tag = 'decays_tab_row_'+str(i)+'_cell a_text')
                with dpg.table_cell(tag = 'decays_tab_row_'+str(i)+'_cell b'):
                    if i!=0:
                        dpg.add_checkbox(
                             default_value=True,
                             enabled=True,
                             tag = 'decays_tab_row_'+str(i)+'_cell b_chk',
                             callback=self.callback_chkbox_decay_table_mark
                                )
                        self.GI.extend(['decays_tab_row_'+str(i)+'_cell b_chk'])
                    else:
    
                        if if_substracted:
                            dpg.add_checkbox(
                                 default_value=True,
                                enabled=False,
                                tag = 'decays_tab_row_'+str(i)+'_cell b_chk',
                                callback=self.callback_chkbox_decay_table_mark
                                    )
                            self.GI.extend(['decays_tab_row_'+str(i)+'_cell b_chk'])
                        else:
                            dpg.add_checkbox(
                                 default_value=False,
                                enabled=False,
                                tag = 'decays_tab_row_'+str(i)+'_cell b_chk',
                                callback=self.callback_chkbox_decay_table_mark
                                    )
                            self.GI.extend(['decays_tab_row_'+str(i)+'_cell b_chk'])
        
    def mount_filter_list_table(self,channel):
        
        for i,F in enumerate(self.Filters['Channel '+str(channel)].keys()):
    
            
    
            with dpg.table_row(tag ='filters_ch_'+str(channel)+'_tab_list_row_'+str(i),
                               parent='filters_ch_'+str(channel)+'_tab_list_tag'):
                self.GI.extend(['filters_ch_'+str(channel)+'_tab_list_row_'+str(i)])
                with dpg.table_cell(tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell #'):
                    dpg.add_text(str(i+1),tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell #_text')
                    self.GI.extend(['filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell #',
                                            'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell #_text'
                                           ])
                with dpg.table_cell(tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell a'):
                    dpg.add_text(F,tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell a_text')
                    self.GI.extend(['filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell a',
                                            'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell a_text'])
                with dpg.table_cell(tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell b'):
                    if F == 'Current decay; CH '+str(channel):
                        self.GI.extend(['filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell b'])
                        dpg.add_checkbox(
                                     default_value=True,
                            enabled=True,
                            tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell b_chk',
                            callback=self.callback_select_filter_for_batch
                                        )
                        self.GI.extend(['filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell b_chk'])
                    else:
                        dpg.add_checkbox(
                                     default_value=False,
                            enabled=True,
                            tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell b_chk',
                            callback=self.callback_select_filter_for_batch
                                        )
                        self.GI.extend(['filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell b_chk'])
    def mount_status_modal(self):
        self.mount_loading_status_window()
        
        dpg.configure_item('loading_title',label='Processing file:')
            
        dpg.configure_item('loading_butt',label='')
            
        
        dpg.add_button(tag='loading_status_text',
                       width=self.mode_init.loading_status_text['width'],
                       label='Status:',parent='load_ind_win')
        dpg.bind_item_theme('loading_status_text', 'transparent_theme')
        
        dpg.add_button(tag='loading_status',
                       width=self.mode_init.loading_status['width'],
                       label='Extracting',parent='load_ind_win')
        dpg.bind_item_theme('loading_status', 'transparent_theme')
        
        dpg.add_button(tag='loading_cnt_butt',
                       width=self.mode_init.loading_cnt_butt['width'],
                       label='',parent='load_ind_win')
        dpg.bind_item_theme('loading_cnt_butt', 'transparent_theme')
        

        
    def prepare_input_to_calculate_filters_from_routine(self,XS,YS,TCSPC_SIZE,TCSPC_RESOLUTION,routine,channel):
        XS = XS*self.tau_resolution-(XS*self.tau_resolution)[0]
        curve_names = routine['Channel '+str(channel)].keys()
        curve_names = [c for c in curve_names if c!='BG']
        curve_names = [c for c in curve_names if c!='BG_rng']
        cname = 'Current decay; CH '+str(channel)
        jsn_file = 'TCSPC_decay_library.json'
        jsn_path = os.path.join('res','Lib','json',jsn_file)
        with open(jsn_path) as json_library:
            jsn_dict = json.load(json_library)
    
        CURVES={}
        if_BG = routine['Channel '+str(channel)]['BG']
    
        if_afterpulse = dpg.get_value('remove_afterpulsing_chkbx')
        
        if not if_BG and len(curve_names)==0:
            print('Failure: no filters selected')
            
        elif not if_BG and len(curve_names)>0:
            for curv in curve_names:
                curve = np.load(routine['Channel '+str(channel)][curv])
    
                df = pd.DataFrame(curve.T,columns=['time','ydata'])
                df.ydata = df.ydata/df.ydata.sum()
    
                adjusted = self.adjust_curves(df, pd.Series(XS).to_frame())
                curve=adjusted.ydata.values
                CURVES[curv]=curve
            if if_afterpulse:
    
                afterpulse = 1/np.unique(XS).size
                afterpulse = np.array([afterpulse for i in CURVES[curve_names[0]]])
                CURVES['Afterpulsing and background']=afterpulse
    
            else:
                pass
    
    
    
        elif if_BG and len(curve_names)==0:
            bg_range = routine['Channel '+str(channel)]['BG_rng']
    
            xs = XS
            ys = YS
            noise_LVL = np.mean((ys)[np.where((xs>=bg_range[0]) & (xs<=bg_range[1]))[0]])
    
            ys = ys - noise_LVL
            norma = np.sum(ys)
            CURVES[cname] = ys/norma
            if if_afterpulse:
                afterpulse = 1/np.unique(xs).size
    
                afterpulse = np.array([afterpulse for i in CURVES[cname]])
    
                CURVES['Afterpulsing and background']=afterpulse
            else:
                pass
    
        else:
    
    
            bg_range = routine['Channel '+str(channel)]['BG_rng']
            xs = XS
            ys = YS
            noise_LVL = np.mean((ys)[np.where((xs>=bg_range[0]) & (xs<=bg_range[1]))[0]])
            ys = ys - noise_LVL
            norma = np.sum(ys)
    
            CURVES[cname] = ys/norma
            for curv in curve_names:
    
    
                FILTER_TCSPC_RESOLUTION = jsn_dict['Channel '+str(channel)][curv]['TCSPC_resolution']
                FILTER_TCSPC_SIZE = jsn_dict['Channel '+str(channel)][curv]['TCSPC_channels']
    
                curve = np.load(routine['Channel '+str(channel)][curv])
    
                df = pd.DataFrame(curve.T,columns=['time','ydata'])
                df.ydata = df.ydata/df.ydata.sum()
    
                adjusted = self.adjust_curves(df, pd.Series(XS).to_frame())
                curve=adjusted.ydata.values
                CURVES[curv]=curve
            if if_afterpulse:
                afterpulse = 1/np.unique(xs).size
                afterpulse = np.array([afterpulse for i in CURVES[cname]])
                CURVES['Afterpulsing and background']=afterpulse
            else:
                pass
    
        return CURVES

    def print_val(self,sender):
        pass

    def remove_existing_filter_plots(self):
        existing_filter_plots = dpg.get_aliases()
        existing_filter_plots = [p for p in existing_filter_plots if p.startswith('tag_series_F_')]
        for p in existing_filter_plots:
            dpg.delete_item(p)
    
    
    
    def remove_imported_curves_from_plot(self):
        cur = dpg.get_aliases()
        cur = [c for c in cur if 'tag_series_fltr_imported_' in c]
    
        for c in cur:
            dpg.delete_item(c)

    def show_error(self,TEXT):
        try:
            dpg.add_window(pos=(400,150),
                           label='Error!',
                               tag='ERROR',
                               autosize=True,
                               no_move=True,
                                no_close=True,
                                no_title_bar=False,
                                no_resize=True,
                               show=True,
                               modal=False
                              )
            dpg.add_text(TEXT,tag='ERROR_text',
                     parent='ERROR')
            dpg.add_button(label='Close',
                           parent='ERROR',
                           tag='ERROR_butt',
                           callback=self.callback_ERROR_dialog_close
                          )
            dpg.bind_item_theme('No_data_files', 'Error_window_theme')
        except:
            dpg.show_item('ERROR')
    

    def unmount_LIB_decay_table(self):
        rows = dpg.get_aliases()
    
        rows = [r for r in rows if r.startswith('decays_lib_tab_row_')]
    
    
        for r in rows:
            dpg.delete_item(r)
        dpg.hide_item('decays_tab_lib_list_tag')


    def unmount_decay_table(self):
    
        rows = dpg.get_aliases()
    
        rows = [r for r in rows if r.startswith('decays_tab_row_')]
    
        for r in rows:
            dpg.delete_item(r)

    def unmount_status_modal(self):
        dpg.configure_item('load_ind_win',show=False)
        try:
            dpg.delete_item('loading_butt')
            dpg.delete_item('loading_status_text')
            dpg.delete_item('loading_status')
    
            dpg.delete_item('loading_cnt_butt')
            dpg.delete_item('loading_title')
            dpg.delete_item('load_ind_win')
    
    
        except:
            pass
    
