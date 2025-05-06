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
from Required.automated_roi import ImageROIProcessor
from scipy.stats import median_abs_deviation
import pickle
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.gridspec as gridspec
# from matplotlib.transforms import Bbox
# import matplotlib.pyplot as plt

# from sympy.parsing.sympy_parser import parse_expr
# from sympy import latex
# from io import BytesIO
# from PIL import Image

# from lmfit import Model, Parameters
# import ast

import Required.INIT as inits

bf = inits._basicF()
# inV=inits._init_varaibles()
lprint = bf.lnprint
globalITEMS = inits._common_VARIABLES()
###############################################################################
###############################################################################
''' Inits'''


###############################################################################
###############################################################################


class _Phot2conc_init:

    def __init__(self,
                 size_ratio,
                 left_indent,
                 internal_indent,
                 right_indent,
                 bottom_indent,
                 top_indent,
                 group_spacer,
                 font_size,
                 last_directory, GI):
        '''General variables'''
        self.last_directory = last_directory

        self.GI = GI

        '''Layout variables'''
        self.size_ratio = size_ratio
        self.left_indent = int(left_indent * self.size_ratio['width'])
        self.internal_indent = int(internal_indent * self.size_ratio['width'])
        self.right_indent = int(right_indent * self.size_ratio['width'])
        self.bottom_indent = int(bottom_indent * self.size_ratio['width'])
        self.top_indent = int(top_indent * self.size_ratio['width'])
        self.group_spacer = int(group_spacer * self.size_ratio['width'])
        self.fnt_ratio = (self.size_ratio['width'] + self.size_ratio['height']) / 2
        self.font_size = int(np.round(font_size * self.fnt_ratio, 0))
        self.im_scaller = int(32)  # 1.1
        self.files = []

        # print(self.right_indent,self.bottom_indent)
        self.NO_IMAGE_INTENSITY = np.load(os.path.join('res', 'img', 'NO_image_INT.npy'))

        self.ROI_mode_items = ['',
                               'Find dark',
                               'Find bright'
                              ]

        bf.remove_font_from_registry()
        bf.add_font_to_registry(self.font_size)

        self.img_border = 60

        self.PTU_DATA_window = {'name': 'PTU_DATA_window',
                                'width': int(380 * self.size_ratio['width']),
                                'height': int(175 * self.size_ratio['height']),
                                # 'height':int(315*self.size_ratio['height']),
                                'pos': (self.left_indent, self.top_indent)
                                }

        self.file_window = {'name': 'file_window',
                            'width': int(380 * self.size_ratio['width']),
                            'height': dpg.get_viewport_height() - (self.top_indent + self.PTU_DATA_window[
                                'height'] + self.internal_indent + self.bottom_indent),
                            'pos': (
                                self.left_indent,
                                self.top_indent + self.PTU_DATA_window['height'] + self.internal_indent)
                            }
        self.image_window_ch1 = {'name': 'image_window_ch1',
                                 'width': int(386 * self.size_ratio['width']),
                                 'height': int((392 * self.size_ratio['width'] + (self.img_border))),
                                 'pos': (self.left_indent + self.PTU_DATA_window['width'] + self.internal_indent,
                                         self.top_indent)
                                 }
        self.image_window_ch2 = {'name': 'image_window_ch2',
                                 'width': int(386 * self.size_ratio['width']),
                                 'height': int(392 * self.size_ratio['width'] + self.img_border),
                                 'pos': (self.image_window_ch1['pos'][0] + self.image_window_ch1[
                                     'width'] + self.internal_indent,
                                         self.top_indent)
                                 }
        self.tex_1_name = 'texture_tag_chan_1'
        self.tex_2_name = 'texture_tag_chan_2'

        if 'texture_reg' in dpg.get_aliases():
            pass
        else:
            dpg.add_texture_registry(show=False, tag='texture_reg')

            self.GI.extend(['texture_reg'])

            self.processor_1 = ImageROIProcessor()
            self.processor_1.image = np.clip((self.NO_IMAGE_INTENSITY), 0, 1).astype(np.float64)
            self.processor_2 = ImageROIProcessor()
            self.processor_2.image = np.clip((self.NO_IMAGE_INTENSITY), 0, 1).astype(np.float64)

            self.rgba_image_1 = self.im_to_rgbim(self.processor_1.image)
            self.rgba_image_2 = self.im_to_rgbim(self.processor_2.image)

            self.rgba_image_1 = cv2.resize(self.rgba_image_1,
                                           (int(self.image_window_ch1['width'] - self.im_scaller),
                                            int(self.image_window_ch1['width'] - self.im_scaller)),
                                           interpolation=cv2.INTER_LINEAR)
            self.rgba_image_2 = cv2.resize(self.rgba_image_2,
                                           (int(self.image_window_ch2['width'] - self.im_scaller),
                                            int(self.image_window_ch2['width'] - self.im_scaller)),
                                           interpolation=cv2.INTER_LINEAR)

            dpg_image_1 = (self.rgba_image_1.astype(np.float64) / np.max(self.rgba_image_1)).flatten().tolist()
            dpg_image_2 = (self.rgba_image_2.astype(np.float64) / np.max(self.rgba_image_2)).flatten().tolist()

            dpg.add_dynamic_texture(width=int(self.image_window_ch1['width'] - self.im_scaller),
                                    height=int(self.image_window_ch1['width'] - self.im_scaller),
                                    default_value=dpg_image_1,
                                    tag=self.tex_1_name,
                                    parent='texture_reg')
            dpg.add_dynamic_texture(width=int(self.image_window_ch2['width'] - self.im_scaller),
                                    height=int(self.image_window_ch2['width'] - self.im_scaller),
                                    default_value=dpg_image_2,
                                    tag=self.tex_2_name,
                                    parent='texture_reg')

        # if self.size_ratio['width']>=1:
        #     self.shift=int((self.image_window_ch1['width']/self.size_ratio['width']-dpg.get_item_width(self.tex_1_name))/4)
        # else:
        #     self.shift=int((self.image_window_ch1['width']-dpg.get_item_width(self.tex_1_name))/4)
        self.shift = 8
        # lprint(self.size_ratio['width'],self.shift)
        self.hist_window_ch1 = {'name': 'hist_window_ch1',
                                # 'width':dpg.get_item_width(self.tex_1_name)+int(1.5*self.internal_indent),
                                'width': self.image_window_ch1['width'],
                                # 'height':dpg.get_viewport_height()-(2*self.top_indent+dpg.get_item_height(self.tex_1_name)*self.hist_scaller+int(4.5*self.internal_indent)+self.bottom_indent),
                                'height': dpg.get_viewport_height() - (
                                        self.image_window_ch1['pos'][1] + self.image_window_ch1[
                                    'height'] + self.internal_indent + self.bottom_indent),
                                # 'pos':(self.left_indent+self.internal_indent+self.PTU_DATA_window['width'],
                                #        2*self.top_indent+dpg.get_item_height(self.tex_1_name)*self.hist_scaller+int(4.5*self.internal_indent))
                                'pos': (self.image_window_ch1['pos'][0],
                                        self.image_window_ch1['pos'][1] + self.image_window_ch1[
                                            'height'] + self.internal_indent)
                                }

        self.hist_window_ch2 = {'name': 'hist_window_ch2',
                                # 'width':dpg.get_item_width(self.tex_2_name)+int(1.5*self.internal_indent),
                                'width': self.image_window_ch2['width'],
                                # 'height':dpg.get_viewport_height()-(2*self.top_indent+dpg.get_item_height(self.tex_2_name)*self.hist_scaller+int(4.5*self.internal_indent)+self.bottom_indent),
                                # 'pos':(self.left_indent+self.internal_indent+self.PTU_DATA_window['width']+dpg.get_item_width(self.tex_1_name)+2*self.internal_indent,
                                #        2*self.top_indent+dpg.get_item_height(self.tex_2_name)*self.hist_scaller+int(4.5*self.internal_indent))
                                'height': dpg.get_viewport_height() - (
                                        self.image_window_ch2['pos'][1] + self.image_window_ch2[
                                    'height'] + self.internal_indent + self.bottom_indent),

                                'pos': (self.image_window_ch2['pos'][0],
                                        self.image_window_ch2['pos'][1] + self.image_window_ch2[
                                            'height'] + self.internal_indent)
                                }

        self.FCS_window = {'name': 'FCS_window',
                           # 'width':int(380*self.size_ratio['width']),
                           'width': dpg.get_viewport_width() - (self.image_window_ch2['pos'][0] + self.image_window_ch2[
                               'width'] + self.internal_indent + self.right_indent),

                           'height': int(406 * self.size_ratio['height']),
                           'pos': (self.left_indent + self.PTU_DATA_window['width'] + self.internal_indent +
                                   self.image_window_ch1['width'] + int(self.internal_indent) + self.image_window_ch2[
                                       'width'] + int(self.internal_indent),
                                   self.top_indent)
                           }

        self.results_window = {'name': 'results_window',
                               'width': self.FCS_window['width'],
                               'height': int(360 * self.size_ratio['height']),
                               'pos': (self.FCS_window['pos'][0],
                                       self.top_indent + self.FCS_window['height'] + self.internal_indent)
                               }

        self.Resolution_output = {'name': 'Resolution_output',
                                  'width': -1
                                  }

        self.Pixel_size_output = {'name': 'Pixel_size_output',
                                  'width': -1
                                  }
        self.Nframes_output = {'name': 'Nframes_output',
                               'width': -1
                               }
        self.Pixel_dwell_output = {'name': 'Pixel_dwell_output',
                                   'width': -1
                                   }
        self.Resol_Pix_size_table_col1 = {'name': 'Resol_Pix_size_table_col1',
                                          'width': int(self.PTU_DATA_window['width'] / 2)
                                          }
        self.Resol_Pix_size_table_col2 = {'name': 'Resol_Pix_size_table_col2',
                                          'width': int(self.PTU_DATA_window['width'] / 2)
                                          }
        self.ROI_table_col1 = {'name': 'ROI_table_col1',
                               'width': int(self.PTU_DATA_window['width'] / 3)
                               }
        self.ROI_table_col2 = {'name': 'ROI_table_col2',
                               'width': int(self.PTU_DATA_window['width'] / 3)
                               }
        self.ROI_table_col3 = {'name': 'ROI_table_col3',
                               'width': int(self.PTU_DATA_window['width'] / 3)
                               }

        self.auto_ROI_ch_table_col1 = {'name': 'auto_ROI_ch_table_col1',
                                       'width': int(2*self.PTU_DATA_window['width'] / 8)
                                       }
        self.auto_ROI_ch_table_col2 = {'name': 'auto_ROI_ch_table_col2',
                                       'width': int(3 * self.PTU_DATA_window['width'] / 8)
                                       }
        self.auto_ROI_ch_table_col3 = {'name': 'auto_ROI_ch_table_col3',
                                       'width': int(3 * self.PTU_DATA_window['width'] / 8)
                                       }
        self.ROI_mode_1 = {'name': 'ROI_mode_1',
                           'width': -1,
                           'items': self.ROI_mode_items

                           }
        self.ROI_mode_2 = {'name': 'ROI_mode_2',
                           'width': -1,
                           'items': self.ROI_mode_items

                           }
        self.file_box = {'name': 'file_box',
                         'width': -1,
                         'num_items': 17,
                         'items': self.files

                         }
        self.Calculate_button = {'name': 'Calculate_button',
                                 'width': -1

                                 }
        self.add_to_res_single_button = {'name': 'add_to_res_single_button',
                                         'width': -1

                                         }
        self.Calculate_all_button = {'name': 'Calculate_all_button',
                                     'width': -1

                                     }
        self.EXPORT_ops_table_col1 = {'name': 'EXPORT_ops_table_col1',
                                      'width': int(self.file_window['width'] / 2)
                                      }
        self.EXPORT_ops_table_col2 = {'name': 'EXPORT_ops_table_col2',
                                      'width': int(self.file_window['width'] / 2)
                                      }

        self.Export_all_button = {'name': 'Export_all_button',
                                  'width': -1

                                  }

        # self.img_win_1_table_col1 = {'name':'img_win_1_table_col1',
        #                     'width':int(self.image_window_ch1['width']/4)
        #                          }
        # self.img_win_1_table_col2 = {'name':'img_win_1_table_col2',
        #                     'width':int(self.image_window_ch1['width']/4)
        #                          }
        # self.img_win_1_table_col3 = {'name':'img_win_1_table_col3',
        #                     'width':int(self.image_window_ch1['width']/4)
        #                          }
        # self.img_win_1_table_col4 = {'name':'img_win_1_table_col4',
        #                     'width':int(self.image_window_ch1['width']/4)
        #                          }
        self.cell_thres_ratio_1 = {'name': 'cell_thres_ratio_1',
                                   'width': -1

                                   }

        self.nucl_thres_ratio_1 = {'name': 'nucl_thres_ratio_1',
                                   'width': -1

                                   }
        self.img_win_1_table_2_col1 = {'name': 'img_win_1_table_2_col1',
                                       'width': int(self.image_window_ch1['width'] / 3)
                                       }
        self.img_win_1_table_2_col2 = {'name': 'img_win_1_table_2_col2',
                                       'width': int(self.image_window_ch1['width'] / 3)
                                       }
        self.img_win_1_table_2_col3 = {'name': 'img_win_1_table_2_col3',
                                       'width': int(self.image_window_ch1['width'] / 3)
                                       }
        self.img_contrast_1 = {'name': 'img_contrast_1',
                               'width': -1

                               }
        self.img_Brightness_1 = {'name': 'img_Brightness_1',
                                 'width': -1

                                 }
        self.img_roi_alpha_1 = {'name': 'img_roi_alpha_1',
                                'width': -1

                                }
        # self.img_win_2_table_col1 = {'name':'img_win_2_table_col1',
        #                     'width':int(self.image_window_ch2['width']/4)
        #                          }
        # self.img_win_2_table_col2 = {'name':'img_win_2_table_col2',
        #                     'width':int(self.image_window_ch2['width']/4)
        #                          }
        # self.img_win_2_table_col3 = {'name':'img_win_2_table_col3',
        #                     'width':int(self.image_window_ch2['width']/4)
        #                             }
        # self.img_win_2_table_col4 = {'name':'img_win_2_table_col4',
        #                     'width':int(self.image_window_ch2['width']/4)
        #                             }
        self.cell_thres_ratio_2 = {'name': 'cell_thres_ratio_2',
                                   'width': -1

                                   }

        self.nucl_thres_ratio_2 = {'name': 'nucl_thres_ratio_2',
                                   'width': -1

                                   }
        self.img_win_2_table_2_col1 = {'name': 'img_win_2_table_2_col1',
                                       'width': int(self.image_window_ch2['width'] / 3)
                                       }
        self.img_win_2_table_2_col2 = {'name': 'img_win_2_table_2_col2',
                                       'width': int(self.image_window_ch2['width'] / 3)
                                       }
        self.img_win_2_table_2_col3 = {'name': 'img_win_2_table_2_col3',
                                       'width': int(self.image_window_ch2['width'] / 3)
                                       }
        self.img_contrast_2 = {'name': 'img_contrast_2',
                               'width': -1

                               }
        self.img_Brightness_2 = {'name': 'img_Brightness_2',
                                 'width': -1

                                 }
        self.img_roi_alpha_2 = {'name': 'img_roi_alpha_2',
                                'width': -1

                                }
        self.hist_conc_plot_ch1 = {'name': 'hist_conc_plot_ch1',
                                   'width': -1,
                                   'height': -1

                                   }
        self.hist_np_plot_ch1 = {'name': 'hist_np_plot_ch1',
                                 'width': -1,
                                 'height': -1

                                 }
        self.hist_phot_plot_ch1 = {'name': 'hist_phot_plot_ch1',
                                   'width': -1,
                                   'height': -1

                                   }
        self.hist_conc_plot_ch2 = {'name': 'hist_conc_plot_ch2',
                                   'width': -1,
                                   'height': -1

                                   }
        self.hist_np_plot_ch2 = {'name': 'hist_np_plot_ch2',
                                 'width': -1,
                                 'height': -1

                                 }
        self.hist_phot_plot_ch2 = {'name': 'hist_phot_plot_ch2',
                                   'width': -1,
                                   'height': -1

                                   }
        self.Load_calib_button = {'name': 'Load_calib_button',
                                  'width': -1

                                  }

        self.Save_calib_button = {'name': 'Save_calib_button',
                                  'width': -1

                                  }
        self.FCS_win_CH1_table_col1 = {'name': 'FCS_win_CH1_table_col1',
                                       'width': int(2 * self.FCS_window['width'] / 3)
                                       }
        self.FCS_win_CH1_table_col2 = {'name': 'FCS_win_CH1_table_col2',
                                       'width': int(self.FCS_window['width'] / 3)
                                       }
        self.omega_input_ch_1 = {'name': 'omega_input_ch_1',
                                 'width': -1

                                 }
        self.omega_err_input_ch_1 = {'name': 'omega_err_input_ch_1',
                                     'width': -1

                                     }

        self.kappa_input_ch_1 = {'name': 'kappa_input_ch_1',
                                 'width': -1

                                 }
        self.kappa_err_input_ch_1 = {'name': 'kappa_err_input_ch_1',
                                     'width': -1

                                     }

        self.focal_vol_input_ch_1 = {'name': 'focal_vol_input_ch_1',
                                     'width': -1

                                     }
        self.focal_vol_err_input_ch_1 = {'name': 'focal_vol_err_input_ch_1',
                                         'width': -1

                                         }
        self.Brightness_input_ch_1 = {'name': 'Brightness_input_ch_1',
                                      'width': -1,
                                      'default_value': 1000
                                      }
        self.Brightness_err_input_ch_1 = {'name': 'Brightness_err_input_ch_1',
                                          'width': -1,
                                          'default_value': 100
                                          }

        self.FCS_win_CH2_table_col1 = {'name': 'FCS_win_CH2_table_col1',
                                       'width': int(2 * self.FCS_window['width'] / 3)
                                       }
        self.FCS_win_CH2_table_col2 = {'name': 'FCS_win_CH2_table_col2',
                                       'width': int(self.FCS_window['width'] / 3)
                                       }
        self.omega_input_ch_2 = {'name': 'omega_input_ch_2',
                                 'width': -1

                                 }
        self.omega_err_input_ch_2 = {'name': 'omega_err_input_ch_2',
                                     'width': -1

                                     }

        self.kappa_input_ch_2 = {'name': 'kappa_input_ch_2',
                                 'width': -1

                                 }
        self.kappa_err_input_ch_2 = {'name': 'kappa_err_input_ch_2',
                                     'width': -1

                                     }

        self.focal_vol_input_ch_2 = {'name': 'focal_vol_input_ch_2',
                                     'width': -1

                                     }
        self.focal_vol_err_input_ch_2 = {'name': 'focal_vol_err_input_ch_2',
                                         'width': -1

                                         }
        self.Brightness_input_ch_2 = {'name': 'Brightness_input_ch_2',
                                      'width': -1,
                                      'default_value': 1000
                                      }
        self.Brightness_err_input_ch_2 = {'name': 'Brightness_err_input_ch_2',
                                          'width': -1,
                                          'default_value': 100
                                          }

        self.RES_win_CH1_table_col1 = {'name': 'RES_win_CH1_table_col1',
                                       'width': int(2 * self.FCS_window['width'] / 3)
                                       }
        self.RES_win_CH1_table_col2 = {'name': 'RES_win_CH1_table_col2',
                                       'width': int(self.FCS_window['width'] / 3)
                                       }

        self.sinle_phot_output_ch_1 = {'name': 'sinle_phot_output_ch_1',
                                       'width': -1

                                       }
        self.sinle_phot_err_output_ch_1 = {'name': 'sinle_phot_err_output_ch_1',
                                           'width': -1

                                           }
        self.sinle_mols_output_ch_1 = {'name': 'sinle_mols_output_ch_1',
                                       'width': -1

                                       }
        self.sinle_mols_err_output_ch_1 = {'name': 'sinle_mols_err_output_ch_1',
                                           'width': -1

                                           }

        self.single_conc_output_ch_1 = {'name': 'single_conc_output_ch_1',
                                        'width': -1

                                        }
        self.single_conc_err_output_ch_1 = {'name': 'single_conc_err_output_ch_1',
                                            'width': -1

                                            }
        self.RES_win_CH2_table_col1 = {'name': 'RES_win_CH2_table_col1',
                                       'width': int(2 * self.FCS_window['width'] / 3)
                                       }
        self.RES_win_CH2_table_col2 = {'name': 'RES_win_CH2_table_col2',
                                       'width': int(self.FCS_window['width'] / 3)
                                       }
        self.sinle_phot_output_ch_2 = {'name': 'sinle_phot_output_ch_2',
                                       'width': -1

                                       }
        self.sinle_phot_err_output_ch_2 = {'name': 'sinle_phot_err_output_ch_2',
                                           'width': -1

                                           }
        self.sinle_mols_output_ch_2 = {'name': 'sinle_mols_output_ch_2',
                                       'width': -1

                                       }
        self.sinle_mols_err_output_ch_2 = {'name': 'sinle_mols_err_output_ch_2',
                                           'width': -1

                                           }

        self.single_conc_output_ch_2 = {'name': 'single_conc_output_ch_2',
                                        'width': -1

                                        }
        self.single_conc_err_output_ch_2 = {'name': 'single_conc_err_output_ch_2',
                                            'width': -1

                                            }
        self.ROI_folder_dialog_id = {'name': 'ROI_folder_dialog_id',
                                     'width': int(900 * self.size_ratio['width']),
                                     'height': int(600 * self.size_ratio['width'])

                                     }
        self.file_dialog_id = {'name': 'file_dialog_id',
                               'width': int(900 * self.size_ratio['width']),
                               'height': int(600 * self.size_ratio['width'])

                               }
        self.PTU_file_dialog_id = {'name': 'PTU_file_dialog_id',
                                   'width': int(900 * self.size_ratio['width']),
                                   'height': int(600 * self.size_ratio['width'])

                                   }
        self.Select_ROI_dialog = {'name': 'Select_ROI_dialog',
                                  'width': int(900 * self.size_ratio['width']),
                                  'height': int(600 * self.size_ratio['width'])

                                  }
        self.file_dialog_export = {'name': 'file_dialog_export',
                                   'width': int(900 * self.size_ratio['width']),
                                   'height': int(600 * self.size_ratio['width'])

                                   }
        self.Calib_file_dialog_id = {'name': 'Calib_file_dialog_id',
                                     'width': int(900 * self.size_ratio['width']),
                                     'height': int(600 * self.size_ratio['width'])

                                     }

        self.ROI_names_combo_tag = {'name': 'ROI_names_combo_tag',
                                     'width': -1,
                                     'items': ['ROI_0']
                                     }

    def im_to_rgbim(self, im):
        '''Converts grayscale image into rgba(float) image.'''
        rgba_image = np.zeros((im.shape[0], im.shape[1], 4), dtype=np.float64)
        rgba_image[..., 0] = im
        rgba_image[..., 1] = im
        rgba_image[..., 2] = im
        rgba_image[..., 3] = 1

        return rgba_image


###############################################################################
###############################################################################
''' Variables'''


###############################################################################
###############################################################################

class _Phot2conc_vars_funct:
    def __init__(self,
                 INIT,
                 last_directory,
                 basf,
                      _globalITEMS):
        self.mode_init = INIT
        self.basf = basf
        self.last_directory = last_directory
        self._GI = _globalITEMS
        self.size_ratio = self.mode_init.size_ratio
        self.Sing_Results_DF = pd.DataFrame()
        self.initialize_res_df()
        self.anal_file = ''
        self.tex_1_name = self.mode_init.tex_1_name
        self.tex_2_name = self.mode_init.tex_2_name

        self.pck_list = []
        self.Channels = ''
        self.mean_Molecules_ch_1 = None
        self.std_Molecules_ch_1 = None
        self.mean_Concentration_ch_1 = None
        self.std_Concentration_ch_1 = None
        self.std_err_Concentration_ch_1 = None
        self.median_C_ch_1 = None
        self.median_err_C_ch_1 = None
        self.mean_Molecules_err_ch_1 = None
        self.mean_Concentration_err_ch_1 = None
        self.mean_Photons_ch_1 = None
        self.mean_Photons_err_ch_1 = None
        self.mean_Molecules_ch_2 = None
        self.std_Molecules_ch_2 = None
        self.mean_Concentration_ch_2 = None
        self.std_Concentration_ch_2 = None
        self.std_err_Concentration_ch_2 = None
        self.median_C_ch_2 = None
        self.median_err_C_ch_2 = None
        self.mean_Molecules_err_ch_2 = None
        self.mean_Concentration_err_ch_2 = None
        self.mean_Photons_ch_2 = None
        self.mean_Photons_err_ch_2 = None

        self.FCS_results_ch_1 = pd.DataFrame()
        self.FCS_results_ch_2 = pd.DataFrame()

        self.mean_brightness_err_ch_1 = 1
        self.mean_brightness_err_ch_2 = 1
        self.mean_brightness_ch_1 = 1
        self.mean_brightness_ch_2 = 1

        self.files = []
        self.pck_files = []
        self.PTU_directory = ''
        self.ROI_directory = ''
        self.calib_directory = ''
        self.sync_rate = None
        self.pixel_dwell = None
        self.number_of_frames = None

        self.DF = pd.DataFrame()
        self.DF2 = pd.DataFrame()

        self.PTU_N_frames = None
        self.PTU_Px_dwell = None
        self.PTU_Resolution = None
        self.PTU_Px_size = None
        self.image_1_times_roi = None
        self.image_2_times_roi = None

        self.pkl = None

        self.roi_1 = None
        self.roi_2 = None

        self.img_height_shift = {'name': 'img_height_shift',
                                 'shift': int(24 * self.size_ratio['height'])

                                 }

        self.NO_IMAGE_INTENSITY = self.mode_init.NO_IMAGE_INTENSITY
        self.processor_1 = self.mode_init.processor_1
        self.processor_2 = self.mode_init.processor_2
        self.Current_image_1 = self.processor_1.image
        self.Current_image_2 = self.processor_2.image

        self.pkl_data = None

        self.im_to_rgbim = self.mode_init.im_to_rgbim

        self.ROIS_state = {'File roi':False,
                           'Auto roi':{
                               'state':False,
                               'subs':{
                                   'cell_thres_ratio_1':1.0,
                                   'nucl_thres_ratio_1':1.5,
                                   'ROI_mode_1':'',
                                   'cp_roi_1':False,
                                   'cell_thres_ratio_2':1.0,
                                   'nucl_thres_ratio_2':1.5,
                                   'ROI_mode_2':'',
                                   'cp_roi_2':False,
                                   }
                               }
                           }




    

    
    def get_roi_state(self):
        self.ROIS_state = {'File roi':dpg.get_value('FILE_ROI_checkbox'),
                           'Auto roi':{
                               'state':dpg.get_value('Auto_ROI_checkbox'),
                               'subs':{
                                   'cell_thres_ratio_1':dpg.get_value('cell_thres_ratio_1'),
                                   'nucl_thres_ratio_1':dpg.get_value('nucl_thres_ratio_1'),
                                   'ROI_mode_1':dpg.get_value('ROI_mode_1'),
                                   'cp_roi_1':dpg.get_value('cp_roi_1'),
                                   'cell_thres_ratio_2':dpg.get_value('cell_thres_ratio_2'),
                                   'nucl_thres_ratio_2':dpg.get_value('nucl_thres_ratio_2'),
                                   'ROI_mode_2':dpg.get_value('ROI_mode_2'),
                                   'cp_roi_2':dpg.get_value('cp_roi_2'),
                                   }
                               }
                           }
        # lprint(self.ROIS_state)

    def set_roi_state(self):
        # lprint(self.ROIS_state)
        dpg.set_value('FILE_ROI_checkbox',self.ROIS_state['File roi'])
        dpg.set_value('Auto_ROI_checkbox',self.ROIS_state['Auto roi']['state'])
        for key in self.ROIS_state['Auto roi']['subs'].keys():
            dpg.set_value(key,self.ROIS_state['Auto roi']['subs'][key])
                
        
    
    def define_file_menu_callbacks(self):

        dpg.configure_item('Open_PTU_menu_item', callback=lambda: dpg.show_item("PTU_file_dialog_id"))
        dpg.configure_item('Open_ROI_menu_item', callback=lambda: dpg.show_item("ROI_folder_dialog_id"))
        dpg.configure_item('Reset_results_menu_item', callback=self.callback_reset_results_DF)
        # dpg.configure_item('Export_settings_menu_item',callback=self.callback_exportsettings)

    # def callback_reset_results_DF(self):
    #     pass
    # def callback_exportsettings(self):
    #     pass
    def VEFF(self, w, k, w_err, k_err):

        V = (pi ** (3 / 2)) * (w ** 3) * k
        V_err = sqrt(9 * (k ** 2) * (pi ** 3) * (w ** 4) * (w_err ** 2) + (k_err ** 2) * (pi ** 3) * (w ** 6))
        return V, V_err

    def CONC(self, N, V, N_err, V_err):

        Na = 6.022e23
        C = N / (Na * V)
        C_err = sqrt(((N ** 2) * (V_err ** 2)) / ((Na ** 2) * (V ** 4)) + (N_err ** 2) / ((Na ** 2) * (V ** 2)))
        return C, C_err

    def Export_result_dataframe_to_file(self, sender, app_data):
        # global directory, new_directory,last_directory

        self.directory = app_data['current_path']
        self.new_directory = self.directory
        self.last_directory = self.directory
        self.update_dialogs_default_directory(self.last_directory)

        # global Sing_Results_DF

        filtr = app_data['current_filter']

        if filtr == '':
            fnam = app_data['file_name']
            filtr = '.' + fnam.split('.')[1]

        if filtr == '.xlsx':
            path = app_data['file_path_name']
            self.Sing_Results_DF.to_excel(path, index=False)

        elif filtr == '.dat':
            path = app_data['file_path_name']
            self.Sing_Results_DF.to_csv(path, sep='\t', index=False)

        elif filtr == '.csv':
            path = app_data['file_path_name']
            self.Sing_Results_DF.to_csv(path, index=False)

        else:
            path = app_data['file_path_name']
            self.Sing_Results_DF.to_pickle(path)

    def Exception(self, tried):
        function_name = sys._getframe(0).f_code.co_name
        print('Exception in function ' + str(function_name) + ' while trying: ' + tried)

    def Load_Save_Calib_file(self, sender, app_data, user_data):
        # global directory, new_directory,last_directory,calib_directory

        self.directory = app_data['current_path']
        self.new_directory = self.directory
        self.last_directory = self.directory
        self.update_dialogs_default_directory(self.last_directory)

        if user_data == 'Load_calib_button':
            path_to_json_file = app_data['file_path_name']
            calib_directory = path_to_json_file

            with open(path_to_json_file) as json_file:
                data = json.load(json_file)
            json_file.close()

            for k0 in data.keys():
                try:
                    len_kappa = len(data[k0]['kappa'])
                except:
                    self.Exception("len_kappa = len(data[k0]['kappa'])")

                try:
                    len_omega = len(data[k0]['omega'])
                except:
                    self.Exception("len_omega = len(data[k0]['omega'])")

                try:
                    len_V0 = len(data[k0]['V0'])
                except:
                    self.Exception("len_V0= len(data[k0]['V0'])")

                try:
                    len_Bright = len(data[k0]['Mol.Brightness'])
                except:
                    self.Exception("len_Bright= len(data[k0]['Mol.Brightness'])")

                if (len_kappa == 2) and (len_omega == 2) and (len_V0 == 2) and (len_Bright == 2):

                    if k0 == 'Channel_1':
                        dpg.set_value('omega_input_ch_1', data[k0]['omega'][0])
                        dpg.set_value('omega_err_input_ch_1', data[k0]['omega'][1])

                        dpg.set_value('kappa_input_ch_1', data[k0]['kappa'][0])
                        dpg.set_value('kappa_err_input_ch_1', data[k0]['kappa'][1])

                        dpg.set_value('focal_vol_input_ch_1', data[k0]['V0'][0])
                        dpg.set_value('focal_vol_err_input_ch_1', data[k0]['V0'][1])

                        dpg.set_value('Brightness_input_ch_1', data[k0]['Mol.Brightness'][0])
                        dpg.set_value('Brightness_err_input_ch_1', data[k0]['Mol.Brightness'][1])

                    elif k0 == 'Channel_2':

                        dpg.set_value('omega_input_ch_2', data[k0]['omega'][0])
                        dpg.set_value('omega_err_input_ch_2', data[k0]['omega'][1])

                        dpg.set_value('kappa_input_ch_2', data[k0]['kappa'][0])
                        dpg.set_value('kappa_err_input_ch_2', data[k0]['kappa'][1])

                        dpg.set_value('focal_vol_input_ch_2', data[k0]['V0'][0])
                        dpg.set_value('focal_vol_err_input_ch_2', data[k0]['V0'][1])

                        dpg.set_value('Brightness_input_ch_2', data[k0]['Mol.Brightness'][0])
                        dpg.set_value('Brightness_err_input_ch_2', data[k0]['Mol.Brightness'][1])

                    else:
                        pass
                elif (len_kappa == 0) and (len_omega == 0) and (len_V0 == 0) and (len_Bright == 0):
                    pass

                else:
                    pass

        elif user_data == 'Save_calib_button':
            path_to_json_file = app_data['file_path_name']
            calib_directory = path_to_json_file
            omega_1 = [dpg.get_value('omega_input_ch_1'), dpg.get_value('omega_err_input_ch_1')]
            kappa_1 = [dpg.get_value('kappa_input_ch_1'), dpg.get_value('kappa_err_input_ch_1')]
            V0_1 = [dpg.get_value('focal_vol_input_ch_1'), dpg.get_value('focal_vol_err_input_ch_1')]
            bright_1 = [dpg.get_value('Brightness_input_ch_1'), dpg.get_value('Brightness_err_input_ch_1')]

            omega_2 = [dpg.get_value('omega_input_ch_2'), dpg.get_value('omega_err_input_ch_2')]
            kappa_2 = [dpg.get_value('kappa_input_ch_2'), dpg.get_value('kappa_err_input_ch_2')]
            V0_2 = [dpg.get_value('focal_vol_input_ch_2'), dpg.get_value('focal_vol_err_input_ch_2')]
            bright_2 = [dpg.get_value('Brightness_input_ch_2'), dpg.get_value('Brightness_err_input_ch_2')]

            output_dict = {'Channel_1': {'omega': omega_1,
                                         'kappa': kappa_1,
                                         'V0': V0_1,
                                         'Mol.Brightness': bright_1
                                         },
                           'Channel_2': {'omega': omega_2,
                                         'kappa': kappa_2,
                                         'V0': V0_2,
                                         'Mol.Brightness': bright_2
                                         }
                           }

            with open(path_to_json_file, 'w') as f:
                json.dump(output_dict, f, indent=4, sort_keys=False)

    def add_single_result_to_DF(self, sender, app_data):

        # stored_results = self.Sing_Results_DF.File.values
        # if self.anal_file in stored_results:
        #     self.Sing_Results_DF.File = self.Sing_Results_DF.File.where(self.Sing_Results_DF.File != self.anal_file)
        #     self.Sing_Results_DF.dropna(inplace=True)
        # else:
        #     pass

        stored_results = self.Sing_Results_DF.File.values
        if self.anal_file in stored_results:
            for index, row in self.Sing_Results_DF.iterrows():
                if row['File'] == self.anal_file and row['ROI_name'] == dpg.get_value('ROI_name_tag'):
                    self.Sing_Results_DF.at[index, 'File'] = np.nan
                    self.Sing_Results_DF.at[index, 'ROI_name'] = np.nan

            self.Sing_Results_DF.dropna(inplace=True)
        else:
            pass

        if dpg.get_value('Auto_ROI_checkbox'):
            roiname = dpg.get_value('ROI_name_tag')
        elif dpg.get_value('FILE_ROI_checkbox'):
            roiname = dpg.get_value('ROI_names_combo_tag')
        else:
            roiname = dpg.get_value('ROI_name_tag')
        if len(self.Channels) == 1:

            if '1' in self.Channels[0]:
                self.Sing_Results_DF_tmp = pd.DataFrame([[self.anal_file,
                                                          roiname,
                                                          1,
                                                          self.mean_Photons_ch_1,
                                                          self.mean_Photons_err_ch_1,
                                                          self.mean_Molecules_ch_1,
                                                          self.mean_Molecules_err_ch_1,
                                                          self.mean_Concentration_ch_1,
                                                          self.mean_Concentration_err_ch_1,
                                                          self.median_C_ch_1,
                                                          self.median_err_C_ch_1
                                                          ]],
                                                        columns=self.Sing_Results_DF.columns)
            elif '2' in self.Channels[0]:
                self.Sing_Results_DF_tmp = pd.DataFrame([[self.anal_file,
                                                          roiname,
                                                          2,
                                                          self.mean_Photons_ch_2,
                                                          self.mean_Photons_err_ch_2,
                                                          self.mean_Molecules_ch_2,
                                                          self.mean_Molecules_err_ch_2,
                                                          self.mean_Concentration_ch_2,
                                                          self.mean_Concentration_err_ch_2,
                                                          self.median_C_ch_2, self.median_err_C_ch_2
                                                          ]],
                                                        columns=self.Sing_Results_DF.columns)
            else:
                pass
        if len(self.Channels) == 2:
            self.Sing_Results_DF_tmp = pd.DataFrame([[self.anal_file,
                                                      roiname,
                                                      1,
                                                      self.mean_Photons_ch_1,
                                                      self.mean_Photons_err_ch_1,
                                                      self.mean_Molecules_ch_1,
                                                      self.mean_Molecules_err_ch_1,
                                                      self.mean_Concentration_ch_1,
                                                      self.mean_Concentration_err_ch_1,
                                                      self.median_C_ch_1,
                                                      self.median_err_C_ch_1],
                                                     [self.anal_file,
                                                      roiname,
                                                      2,
                                                      self.mean_Photons_ch_2,
                                                      self.mean_Photons_err_ch_2,
                                                      self.mean_Molecules_ch_2,
                                                      self.mean_Molecules_err_ch_2,
                                                      self.mean_Concentration_ch_2,
                                                      self.mean_Concentration_err_ch_2,
                                                      self.median_C_ch_2, self.median_err_C_ch_2
                                                      ]], columns=self.Sing_Results_DF.columns)

        self.Sing_Results_DF = pd.concat([self.Sing_Results_DF,
                                          self.Sing_Results_DF_tmp]).reset_index(drop=True)

        self._pkl_file()

    def calc_molecules(self, DF, PTU_Px_dwell, PTU_N_frames, brightness, brightness_err):

        PTU_Px_dwell = PTU_Px_dwell * 1e-6
        MOL = (DF * (1 / (PTU_Px_dwell * PTU_N_frames))) / brightness
        part_BR = -DF / (PTU_N_frames * PTU_Px_dwell * (brightness ** 2))
        MOL_err = sqrt((part_BR ** 2) * (brightness_err ** 2))
        return MOL, MOL_err

    def callback_Brightness_err_input(self, sender, app_data):

        if sender == 'Brightness_err_input_ch_1':
            self.mean_brightness_err_ch_1 = app_data
            self.FCS_results_ch_1 = pd.DataFrame()

            for alias in dpg.get_aliases():
                if alias.startswith('ch_1_results_show_'):
                    try:

                        dpg.delete_item(alias)
                    except:
                        pass
                if alias.startswith('ch_1_results_delete_'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            for alias in dpg.get_aliases():
                if alias.startswith('ch_1_row_results_show'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass

            try:
                dpg.delete_item('column_results_show_del_ch_1')
                dpg.delete_item('column_results_show_Brightness_ch_1')
                dpg.delete_item('column_results_show_N_p_ch_1')
                dpg.delete_item('column_results_show_file_ch_1')
                dpg.delete_item('table_results_show_ch_1')
                dpg.delete_item('remove_button_results_ch_1')
                dpg.delete_item('close_button_results_ch_1')
                dpg.delete_item('group_close_results_table_ch_1')
                dpg.delete_item('show_TT_res_win_ch_1')
            except:
                pass
        elif sender == 'Brightness_err_input_ch_2':
            mean_brightness_err_ch_2 = app_data
            FCS_results_ch_2 = pd.DataFrame()

            for alias in dpg.get_aliases():
                if alias.startswith('ch_2_results_show_'):
                    try:

                        dpg.delete_item(alias)
                    except:
                        pass
                if alias.startswith('ch_2_results_delete_'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            for alias in dpg.get_aliases():
                if alias.startswith('ch_2_row_results_show'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass

            try:
                dpg.delete_item('column_results_show_del_ch_2')
                dpg.delete_item('column_results_show_Brightness_ch_2')
                dpg.delete_item('column_results_show_N_p_ch_2')
                dpg.delete_item('column_results_show_file_ch_2')
                dpg.delete_item('table_results_show_ch_2')
                dpg.delete_item('remove_button_results_ch_2')
                dpg.delete_item('close_button_results_ch_2')
                dpg.delete_item('group_close_results_table_ch_2')
                dpg.delete_item('show_TT_res_win_ch_2')
            except:
                pass
        else:
            pass

    def callback_Brightness_input(self, sender, app_data):

        if sender == 'Brightness_input_ch_1':
            self.mean_brightness_ch_1 = app_data
            self.FCS_results_ch_1 = pd.DataFrame()

            for alias in dpg.get_aliases():
                if alias.startswith('ch_1_results_show_'):
                    try:

                        dpg.delete_item(alias)
                    except:
                        pass
                if alias.startswith('ch_1_results_delete_'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            for alias in dpg.get_aliases():
                if alias.startswith('ch_1_row_results_show'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            try:
                dpg.delete_item('column_results_show_del_ch_1')
                dpg.delete_item('column_results_show_Brightness_ch_1')
                dpg.delete_item('column_results_show_N_p_ch_1')
                dpg.delete_item('column_results_show_file_ch_1')
                dpg.delete_item('table_results_show_ch_1')
                dpg.delete_item('remove_button_results_ch_1')
                dpg.delete_item('close_button_results_ch_1')
                dpg.delete_item('group_close_results_tabl_ch_1')
                dpg.delete_item('show_TT_res_win_ch_1')
            except:
                pass
        elif sender == 'Brightness_input_ch_2':
            self.mean_brightness_ch_2 = app_data
            self.FCS_results_ch_2 = pd.DataFrame()

            for alias in dpg.get_aliases():
                if alias.startswith('ch_2_results_show_'):
                    try:

                        dpg.delete_item(alias)
                    except:
                        pass
                if alias.startswith('ch_2_results_delete_'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            for alias in dpg.get_aliases():
                if alias.startswith('ch_2_row_results_show'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            try:
                dpg.delete_item('column_results_show_del_ch_2')
                dpg.delete_item('column_results_show_Brightness_ch_2')
                dpg.delete_item('column_results_show_N_p_ch_2')
                dpg.delete_item('column_results_show_file_ch_2')
                dpg.delete_item('table_results_show_ch_2')
                dpg.delete_item('remove_button_results_ch_2')
                dpg.delete_item('close_button_results_ch_2')
                dpg.delete_item('group_close_results_tabl_ch_2')
                dpg.delete_item('show_TT_res_win_ch_2')
            except:
                pass

        else:
            pass

    def callback_Keyword_key(self, sender, app_data):
        files = dpg.get_item_configuration('file_box')['items']
        up_key = dpg.mvKey_Up
        down_key = dpg.mvKey_Down

        if len(files) != 0:
            def_val = dpg.get_value('file_box')
            index = files.index(def_val)

            if app_data == up_key:
                if index != 0:
                    index = index - 1
                    dpg.set_value('file_box', files[index])
                    self.callback_listbox('file_box', files[index])
                else:
                    pass
            if app_data == down_key:
                if index != len(files) - 1:
                    index = index + 1
                    dpg.set_value('file_box', files[index])
                    self.callback_listbox('file_box', files[index])
                else:
                    pass

    def initialize_res_df(self):
        self.Sing_Results_DF = pd.DataFrame(columns=['File',
                                                     'ROI_name',
                                                     'Channel',
                                                     '<Counts>',
                                                     'Counts_std',
                                                     '<N_p>',
                                                     'N_p_err',
                                                     '<C>',
                                                     'C_err',
                                                     'C_median',
                                                     'C_median_abs_err'])

    def callback_PTU_directory_select(self, sender, app_data):

        self.initialize_res_df()
        self.files = ()
        dpg.set_value('FILE_ROI_checkbox', False)
        self.directory = app_data['file_path_name']
        self.new_directory = self.directory
        self.PTU_directory = self.directory
        self.last_directory = self.directory
        self.update_dialogs_default_directory(self.last_directory)
        self.files = tuple(np.sort([f for f in os.listdir(self.PTU_directory) if f.endswith('.ptu')]))
        self.pck_files = list(np.sort([f for f in os.listdir(self.PTU_directory) if f.endswith('.pkl')]))
        dpg.configure_item('FILE_ROI_checkbox', enabled=True)
        dpg.configure_item('Auto_ROI_checkbox', enabled=True)

        try:
            self.hide_histograms()
        except:
            pass

        filenames = [f.replace('.ptu', '') for f in self.files]

        if len(self.files) == 0:
            self.show_error_no_files('No PTU files found.')
        else:
            stop = False
            for file in filenames:
                ptufile = file + '.ptu'
                for f in self.pck_files:
                    if file in f:
                        stop = True
                        ffile = file
                        break
                    else:
                        stop = False

                if stop:
                    pass
                else:
                    self.show_error_no_files(
                        'No .pck files found. Run the EXTRACT_AND_FILTER_PTU.py script and try again. Mising file: ' + ffile)
                    try:
                        pass

                    except:
                        pass

        if len(self.pck_files) != 0:
            self.update_flist(filenames)
            self.anal_file = filenames[0]
            dpg.configure_item('file_box', default_value=self.anal_file)
            self.callback_listbox('file_box', self.anal_file)
            # load_PTU_images(anal_file)

        else:
            self.show_error_no_files('No .pck files found. Run the EXTRACT_AND_FILTER_PTU.py script and try again.')

    def callback_ROI_directory_select(self, sender, app_data):
        self.ROI_directory = app_data['file_path_name']
        self.last_directory = self.ROI_directory
        self.update_dialogs_default_directory(self.last_directory)
        dpg.set_value('FILE_ROI_checkbox', True)
        self.callback_select_roi('FILE_ROI_checkbox', True)
        dpg.hide_item('ROI_folder_dialog_id')
        self.load_PTU_images(self.anal_file)

    def callback_add_ROI(self, sender, app_data):

        dpg.configure_item("Select_ROI_dialog", user_data=sender)
        dpg.show_item("Select_ROI_dialog")

    # def callback_auto_adjust(self,sender,app_data):

    #     self.callback_windows_size(sender,app_data)
    #     self.callback_font_size(sender,app_data)
    
    def callback_calculate(self, sender, app_data):
        cmap = 'afmhot'
        rect = 0.1, 0.1, 0.85, 0.9
        norm = None
        if len(self.Channels) == 1:
            if '1' in self.Channels[0]:
                brightness_ch_1 = dpg.get_value('Brightness_input_ch_1')
                brightness_err_ch_1 = dpg.get_value('Brightness_err_input_ch_1')
                Veff_ch_1 = 1e-15 * dpg.get_value('focal_vol_input_ch_1')
                Veff_err_ch_1 = 1e-15 * dpg.get_value('focal_vol_err_input_ch_1')
                # DF = Current_image_1
                if self.processor_1.all_masks is not None and dpg.get_value('Auto_ROI_checkbox'):
                    # lprint('in if1')
                    ROI = self.processor_1.all_masks[0].astype(np.uint8)
                    roi = np.where(ROI==0,np.nan,1)
                    img = self.processor_1.image
                    self.DF = img*roi
                else:
                    self.DF = self.image_1_times_roi
                Photons_1 = pd.DataFrame(self.DF)

                n_pixels_1 = Photons_1.stack().reset_index(drop=True).dropna().count()

                Molecules_ch_1 = self.calc_molecules(self.DF,
                                                     self.PTU_Px_dwell,
                                                     self.PTU_N_frames,
                                                     brightness_ch_1,
                                                     brightness_err_ch_1)[0]
                Molecules_err_ch_1 = self.calc_molecules(self.DF,
                                                         self.PTU_Px_dwell,
                                                         self.PTU_N_frames,
                                                         brightness_ch_1,
                                                         brightness_err_ch_1)[1]
                Concentration_ch_1 = 1e9 * self.CONC(Molecules_ch_1, Veff_ch_1, Molecules_err_ch_1, Veff_err_ch_1)[0]
                Concentration_err_ch_1 = 1e9 * self.CONC(Molecules_ch_1, Veff_ch_1, Molecules_err_ch_1, Veff_err_ch_1)[
                    1]
                self.mean_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().mean()
                self.mean_Photons_err_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(
                    drop=True).dropna().std() / sqrt(n_pixels_1)
                self.mean_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().mean()
                if not dpg.get_value('Error_type_checkbox'):
                    self.mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1).stack().reset_index(
                        drop=True).dropna().mean()
                else:
                    self.mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(
                        drop=True).dropna().std() / sqrt(n_pixels_1)

                self.mean_Concentration_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(
                    drop=True).dropna().mean()
                if not dpg.get_value('Error_type_checkbox'):
                    self.mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1).stack().reset_index(
                        drop=True).dropna().mean()
                else:
                    self.mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(
                        drop=True).dropna().std() / sqrt(n_pixels_1)

                self.median_C_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().median()
                self.median_err_C_ch_1 = median_abs_deviation(
                    pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna())

                dpg.set_value('sinle_phot_output_ch_1', self.mean_Photons_ch_1)

                dpg.set_value('sinle_phot_err_output_ch_1', self.mean_Photons_err_ch_1)
                dpg.set_value('sinle_mols_output_ch_1', self.mean_Molecules_ch_1)

                dpg.set_value('sinle_mols_err_output_ch_1', self.mean_Molecules_err_ch_1)
                dpg.set_value('single_conc_output_ch_1', self.mean_Concentration_ch_1)

                dpg.set_value('single_conc_err_output_ch_1', self.mean_Concentration_err_ch_1)
                Molecules_ch_1 = pd.DataFrame(Molecules_ch_1)
                Concentration_ch_1 = pd.DataFrame(Concentration_ch_1)

                Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1)
                Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1)
                Phot_hist_ch_1, Phot_bins_ch_1 = np.histogram(Photons_1.stack().reset_index(drop=True).dropna().values,
                                                              density=True, bins='auto')
                Phot_bins_ch_1 = Phot_bins_ch_1[:-1]
                median_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().median()

                Mols_hist_ch_1, Mols_bins_ch_1 = np.histogram(
                    pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().values
                    , density=True, bins='auto')
                Mols_bins_ch_1 = Mols_bins_ch_1[:-1]
                median_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().median()

                Conc_hist_ch_1, Conc_bins_ch_1 = np.histogram(
                    pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().values
                    , density=True, bins='auto')
                Conc_bins_ch_1 = Conc_bins_ch_1[:-1]

                ind = np.where(Conc_hist_ch_1 != 0)[0]

                Conc_hist_ch_1 = Conc_hist_ch_1[ind]
                Conc_bins_ch_1 = Conc_bins_ch_1[ind]

                ind = np.where(Mols_hist_ch_1 != 0)[0]

                Mols_hist_ch_1 = Mols_hist_ch_1[ind]
                Mols_bins_ch_1 = Mols_bins_ch_1[ind]

                ind = np.where(Phot_hist_ch_1 != 0)[0]

                Phot_hist_ch_1 = Phot_hist_ch_1[ind]
                Phot_bins_ch_1 = Phot_bins_ch_1[ind]

                dpg.set_value('c_dist_ser_ch_1', (Conc_bins_ch_1, Conc_hist_ch_1))
                dpg.set_value('c_mean_ser_ch_1',
                              (np.array([self.mean_Concentration_ch_1]), np.array([max(Conc_hist_ch_1)])))
                dpg.set_value('c_med_ser_ch_1', (np.array([self.median_C_ch_1]), np.array([max(Conc_hist_ch_1)])))
                dpg.set_axis_limits('hist_xc_axis_ch1', min(Conc_bins_ch_1), max(Conc_bins_ch_1))
                dpg.set_axis_limits('hist_yc_axis_ch1', 0, max(Conc_hist_ch_1))

                dpg.set_value('np_dist_ser_ch_1', (Mols_bins_ch_1, Mols_hist_ch_1))
                dpg.set_value('np_mean_ser_ch_1',
                              (np.array([self.mean_Molecules_ch_1]), np.array([max(Mols_hist_ch_1)])))
                dpg.set_value('np_med_ser_ch_1', (np.array([median_Molecules_ch_1]), np.array([max(Mols_hist_ch_1)])))
                dpg.set_axis_limits('hist_xnp_axis_ch1', min(Mols_bins_ch_1), max(Mols_bins_ch_1))
                dpg.set_axis_limits('hist_ynp_axis_ch1', 0, max(Mols_hist_ch_1))

                dpg.set_value('phot_dist_ser_ch_1', (Phot_bins_ch_1, Phot_hist_ch_1))
                dpg.set_value('phot_mean_ser_ch_1',
                              (np.array([self.mean_Photons_ch_1]), np.array([max(Phot_hist_ch_1)])))
                dpg.set_value('phot_med_ser_ch_1', (np.array([median_Photons_ch_1]), np.array([max(Phot_hist_ch_1)])))
                dpg.set_axis_limits('hist_xphot_axis_ch1', min(Phot_bins_ch_1), max(Phot_bins_ch_1))
                dpg.set_axis_limits('hist_yphot_axis_ch1', 0, max(Phot_hist_ch_1))

                dpg.configure_item('c_mean_ser_ch_1', label='Mean = ' + str(np.round(self.mean_Concentration_ch_1, 4)))
                dpg.configure_item('c_med_ser_ch_1', label='Median = ' + str(np.round(self.median_C_ch_1, 4)))

                dpg.configure_item('np_mean_ser_ch_1', label='Mean = ' + str(np.round(self.mean_Molecules_ch_1, 2)))
                dpg.configure_item('np_med_ser_ch_1', label='Median = ' + str(np.round(median_Molecules_ch_1, 2)))

                dpg.configure_item('phot_mean_ser_ch_1', label='Mean = ' + str(np.round(self.mean_Photons_ch_1, 1)))
                dpg.configure_item('phot_med_ser_ch_1', label='Median = ' + str(np.round(median_Photons_ch_1, 1)))

                try:
                    dpg.show_item('hist_conc_plot_ch1')
                except:
                    pass

                try:
                    dpg.show_item('hist_np_plot_ch1')
                except:
                    pass

                try:
                    dpg.show_item('hist_phot_plot_ch1')
                except:
                    pass

                if dpg.get_value('Photons_array_checkbox'):
                    phot_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Phot_ch_1.csv')

                    Photons_1.to_csv(phot_array_path_ch_1, index=False, sep=',', header=None)
                else:
                    pass

                if dpg.get_value('Np_array_checkbox'):
                    Np_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Np_ch_1.csv')

                    Molecules_ch_1.to_csv(Np_array_path_ch_1, index=False, sep=',', header=None)

                    Np_err_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Np_err_ch_1.csv')
                    Molecules_err_ch_1.to_csv(Np_err_array_path_ch_1, index=False, sep=',', header=None)

                else:
                    pass
                if dpg.get_value('C_array_checkbox'):
                    Conc_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_conc_ch_1.csv')

                    Concentration_ch_1.to_csv(Conc_array_path_ch_1, index=False, sep=',', header=None)

                    Conc_err_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_conc_err_ch_1.csv')
                    Concentration_err_ch_1.to_csv(Conc_err_array_path_ch_1, index=False, sep=',', header=None)

                else:
                    pass

                if dpg.get_value('Photons_Hmaps_checkbox'):
                    phot_hmap_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Phot_HM_ch_1.png')

                    fig = Figure(facecolor='white')

                    ax = fig.add_axes(rect)
                    norm = mpl.colors.Normalize(vmin=Photons_1.min().min(), vmax=Photons_1.max().max())
                    ax.imshow(Photons_1, cmap=cmap)

                    ax.axis('off')
                    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                    FigureCanvas(fig).print_png(phot_hmap_path_ch_1)

                else:
                    pass

                if dpg.get_value('Np_Hmaps_checkbox'):
                    Np_hmap_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Np_HM_ch_1.png')

                    fig = Figure(facecolor='white')

                    ax = fig.add_axes(rect)
                    norm = mpl.colors.Normalize(vmin=Molecules_ch_1.min().min(), vmax=Molecules_ch_1.max().max())
                    ax.imshow(Molecules_ch_1, cmap=cmap)

                    ax.axis('off')
                    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                    FigureCanvas(fig).print_png(Np_hmap_path_ch_1)

                else:
                    pass

                if dpg.get_value('C_Hmaps_checkbox'):
                    C_hmap_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_conc_HM_ch_1.png')
                    fig = Figure(facecolor='white')
                    ax = fig.add_axes(rect)
                    norm = mpl.colors.Normalize(vmin=Concentration_ch_1.min().min(),
                                                vmax=Concentration_ch_1.max().max())
                    ax.imshow(Concentration_ch_1, cmap=cmap)

                    ax.axis('off')
                    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                    FigureCanvas(fig).print_png(C_hmap_path_ch_1)

                else:
                    pass

            elif '2' in self.Channels[0]:
                brightness_ch_2 = dpg.get_value('Brightness_input_ch_2')
                brightness_err_ch_2 = dpg.get_value('Brightness_err_input_ch_2')
                Veff_ch_2 = 1e-15 * dpg.get_value('focal_vol_input_ch_2')
                Veff_err_ch_2 = 1e-15 * dpg.get_value('focal_vol_err_input_ch_2')
                # DF2 = Current_image_2

                if self.processor_2.all_masks is not None and dpg.get_value('Auto_ROI_checkbox'):
                    # lprint('in if2')
                    ROI = self.processor_2.all_masks[0].astype(np.uint8)
                    roi = np.where(ROI==0,np.nan,1)
                    img = self.processor_2.image
                    self.DF2 = img*roi
                    
                else:
                    self.DF2 = self.image_2_times_roi
                
                # self.DF2 = self.image_2_times_roi
                Photons_2 = pd.DataFrame(self.DF2)
                n_pixels_2 = Photons_2.stack().reset_index(drop=True).dropna().count()

                self.mean_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().mean()
                self.mean_Photons_err_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(
                    drop=True).dropna().std() / sqrt(n_pixels_2)
                Molecules_ch_2 = self.calc_molecules(self.DF2,
                                                     self.PTU_Px_dwell,
                                                     self.PTU_N_frames,
                                                     brightness_ch_2,
                                                     brightness_err_ch_2)[0]
                Molecules_err_ch_2 = self.calc_molecules(self.DF2,
                                                         self.PTU_Px_dwell,
                                                         self.PTU_N_frames,
                                                         brightness_ch_2,
                                                         brightness_err_ch_2)[1]

                Concentration_ch_2 = 1e9 * self.CONC(Molecules_ch_2, Veff_ch_2, Molecules_err_ch_2, Veff_err_ch_2)[0]
                Concentration_err_ch_2 = 1e9 * self.CONC(Molecules_ch_2, Veff_ch_2, Molecules_err_ch_2, Veff_err_ch_2)[
                    1]

                self.mean_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().mean()
                if not dpg.get_value('Error_type_checkbox'):
                    self.mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2).stack().reset_index(
                        drop=True).dropna().mean()
                else:
                    self.mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(
                        drop=True).dropna().std() / sqrt(n_pixels_2)

                self.mean_Concentration_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(
                    drop=True).dropna().mean()
                if not dpg.get_value('Error_type_checkbox'):
                    self.mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2).stack().reset_index(
                        drop=True).dropna().mean()
                else:
                    self.mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(
                        drop=True).dropna().std() / sqrt(n_pixels_2)

                self.median_C_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().median()
                self.median_err_C_ch_2 = median_abs_deviation(
                    pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna())
                dpg.set_value('sinle_phot_output_ch_2', self.mean_Photons_ch_2)

                dpg.set_value('sinle_phot_err_output_ch_2', self.mean_Photons_err_ch_2)
                dpg.set_value('sinle_mols_output_ch_2', self.mean_Molecules_ch_2)

                dpg.set_value('sinle_mols_err_output_ch_2', self.mean_Molecules_err_ch_2)
                dpg.set_value('single_conc_output_ch_2', self.mean_Concentration_ch_2)

                dpg.set_value('single_conc_err_output_ch_2', self.mean_Concentration_err_ch_2)
                Molecules_ch_2 = pd.DataFrame(Molecules_ch_2)
                Concentration_ch_2 = pd.DataFrame(Concentration_ch_2)

                Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2)
                Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2)
                Phot_hist_ch_2, Phot_bins_ch_2 = np.histogram(Photons_2.stack().reset_index(drop=True).dropna().values,
                                                              density=True, bins='auto')
                Phot_bins_ch_2 = Phot_bins_ch_2[:-1]
                median_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().median()

                Mols_hist_ch_2, Mols_bins_ch_2 = np.histogram(
                    pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().values
                    , density=True, bins='auto')
                Mols_bins_ch_2 = Mols_bins_ch_2[:-1]
                median_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().median()

                Conc_hist_ch_2, Conc_bins_ch_2 = np.histogram(
                    pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().values
                    , density=True, bins='auto')
                Conc_bins_ch_2 = Conc_bins_ch_2[:-1]

                ind = np.where(Conc_hist_ch_2 != 0)[0]

                Conc_hist_ch_2 = Conc_hist_ch_2[ind]
                Conc_bins_ch_2 = Conc_bins_ch_2[ind]

                ind = np.where(Mols_hist_ch_2 != 0)[0]

                Mols_hist_ch_2 = Mols_hist_ch_2[ind]
                Mols_bins_ch_2 = Mols_bins_ch_2[ind]

                ind = np.where(Phot_hist_ch_2 != 0)[0]

                Phot_hist_ch_2 = Phot_hist_ch_2[ind]
                Phot_bins_ch_2 = Phot_bins_ch_2[ind]

                dpg.set_value('c_dist_ser_ch_2', (Conc_bins_ch_2, Conc_hist_ch_2))
                dpg.set_value('c_mean_ser_ch_2',
                              (np.array([self.mean_Concentration_ch_2]), np.array([max(Conc_hist_ch_2)])))
                dpg.set_value('c_med_ser_ch_2', (np.array([self.median_C_ch_2]), np.array([max(Conc_hist_ch_2)])))
                dpg.set_axis_limits('hist_xc_axis_ch2', min(Conc_bins_ch_2), max(Conc_bins_ch_2))
                dpg.set_axis_limits('hist_yc_axis_ch2', 0, max(Conc_hist_ch_2))

                dpg.set_value('np_dist_ser_ch_2', (Mols_bins_ch_2, Mols_hist_ch_2))
                dpg.set_value('np_mean_ser_ch_2',
                              (np.array([self.mean_Molecules_ch_2]), np.array([max(Mols_hist_ch_2)])))
                dpg.set_value('np_med_ser_ch_2', (np.array([median_Molecules_ch_2]), np.array([max(Mols_hist_ch_2)])))
                dpg.set_axis_limits('hist_xnp_axis_ch2', min(Mols_bins_ch_2), max(Mols_bins_ch_2))
                dpg.set_axis_limits('hist_ynp_axis_ch2', 0, max(Mols_hist_ch_2))

                dpg.set_value('phot_dist_ser_ch_2', (Phot_bins_ch_2, Phot_hist_ch_2))
                dpg.set_value('phot_mean_ser_ch_2',
                              (np.array([self.mean_Photons_ch_2]), np.array([max(Phot_hist_ch_2)])))
                dpg.set_value('phot_med_ser_ch_2', (np.array([median_Photons_ch_2]), np.array([max(Phot_hist_ch_2)])))
                dpg.set_axis_limits('hist_xphot_axis_ch2', min(Phot_bins_ch_2), max(Phot_bins_ch_2))
                dpg.set_axis_limits('hist_yphot_axis_ch2', 0, max(Phot_hist_ch_2))

                dpg.configure_item('c_mean_ser_ch_2', label='Mean = ' + str(np.round(self.mean_Concentration_ch_2, 4)))
                dpg.configure_item('c_med_ser_ch_2', label='Median = ' + str(np.round(self.median_C_ch_2, 4)))

                dpg.configure_item('np_mean_ser_ch_2', label='Mean = ' + str(np.round(self.mean_Molecules_ch_2, 2)))
                dpg.configure_item('np_med_ser_ch_2', label='Median = ' + str(np.round(median_Molecules_ch_2, 2)))

                dpg.configure_item('phot_mean_ser_ch_2', label='Mean = ' + str(np.round(self.mean_Photons_ch_2, 1)))
                dpg.configure_item('phot_med_ser_ch_2', label='Median = ' + str(np.round(median_Photons_ch_2, 1)))

                try:
                    dpg.show_item('hist_conc_plot_ch2')
                except:
                    pass

                try:
                    dpg.show_item('hist_np_plot_ch2')
                except:
                    pass

                try:
                    dpg.show_item('hist_phot_plot_ch2')
                except:
                    pass

                if dpg.get_value('Photons_array_checkbox'):
                    phot_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Phot_ch_2.csv')

                    Photons_2.to_csv(phot_array_path_ch_2, index=False, sep=',', header=None)
                else:
                    pass

                if dpg.get_value('Np_array_checkbox'):
                    Np_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Np_ch_2.csv')

                    Molecules_ch_2.to_csv(Np_array_path_ch_2, index=False, sep=',', header=None)

                    Np_err_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Np_err_ch_2.csv')
                    Molecules_err_ch_2.to_csv(Np_err_array_path_ch_2, index=False, sep=',', header=None)
                else:
                    pass
                if dpg.get_value('C_array_checkbox'):
                    Conc_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_conc_ch_2.csv')

                    Concentration_ch_2.to_csv(Conc_array_path_ch_2, index=False, sep=',', header=None)

                    Conc_err_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_conc_err_ch_2.csv')
                    Concentration_err_ch_2.to_csv(Conc_err_array_path_ch_2, index=False, sep=',', header=None)


                else:
                    pass

                if dpg.get_value('Photons_Hmaps_checkbox'):
                    phot_hmap_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Phot_HM_ch_2.png')

                    fig = Figure(facecolor='white')

                    ax = fig.add_axes(rect)
                    norm = mpl.colors.Normalize(vmin=Photons_2.min().min(), vmax=Photons_2.max().max())
                    ax.imshow(Photons_2, cmap=cmap)

                    ax.axis('off')
                    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                    FigureCanvas(fig).print_png(phot_hmap_path_ch_2)

                else:
                    pass

                if dpg.get_value('Np_Hmaps_checkbox'):
                    Np_hmap_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Np_HM_ch_2.png')

                    fig = Figure(facecolor='white')

                    ax = fig.add_axes(rect)
                    norm = mpl.colors.Normalize(vmin=Molecules_ch_2.min().min(), vmax=Molecules_ch_2.max().max())
                    ax.imshow(Molecules_ch_2, cmap=cmap)

                    ax.axis('off')
                    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                    FigureCanvas(fig).print_png(Np_hmap_path_ch_2)

                else:
                    pass

                if dpg.get_value('C_Hmaps_checkbox'):
                    C_hmap_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_conc_HM_ch_2.png')
                    fig = Figure(facecolor='white')
                    ax = fig.add_axes(rect)
                    norm = mpl.colors.Normalize(vmin=Concentration_ch_2.min().min(),
                                                vmax=Concentration_ch_2.max().max())
                    ax.imshow(Concentration_ch_2, cmap=cmap)

                    ax.axis('off')
                    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                    FigureCanvas(fig).print_png(C_hmap_path_ch_2)

                else:
                    pass
            else:
                pass


        elif len(self.Channels) == 2:
            brightness_ch_1 = dpg.get_value('Brightness_input_ch_1')
            brightness_err_ch_1 = dpg.get_value('Brightness_err_input_ch_1')
            Veff_ch_1 = 1e-15 * dpg.get_value('focal_vol_input_ch_1')
            Veff_err_ch_1 = 1e-15 * dpg.get_value('focal_vol_err_input_ch_1')
            # DF = Current_image_1
            if self.processor_1.all_masks is not None and dpg.get_value('Auto_ROI_checkbox'):
                # lprint('in if1')
                ROI = self.processor_1.all_masks[0].astype(np.uint8)
                roi = np.where(ROI==0,np.nan,1)
                img = self.processor_1.image
                self.DF = img*roi
            else:
                self.DF = self.image_1_times_roi
            # self.DF = self.image_1_times_roi
            Photons_1 = pd.DataFrame(self.DF)
            n_pixels_1 = Photons_1.stack().reset_index(drop=True).dropna().count()

            # Photons_1t = pd.DataFrame(np.nan_to_num(image_1_times_roi, nan=0))
            # n_pixels_1test =  Photons_1t.stack().reset_index(drop=True).dropna().count()

            # lnprint('N pixel test', n_pixels_1,n_pixels_1test)

            Molecules_ch_1 = self.calc_molecules(self.DF,
                                                 self.PTU_Px_dwell,
                                                 self.PTU_N_frames,
                                                 brightness_ch_1,
                                                 brightness_err_ch_1)[0]
            Molecules_err_ch_1 = self.calc_molecules(self.DF,
                                                     self.PTU_Px_dwell,
                                                     self.PTU_N_frames,
                                                     brightness_ch_1,
                                                     brightness_err_ch_1)[1]
            Concentration_ch_1 = 1e9 * self.CONC(Molecules_ch_1, Veff_ch_1, Molecules_err_ch_1, Veff_err_ch_1)[0]
            Concentration_err_ch_1 = 1e9 * self.CONC(Molecules_ch_1, Veff_ch_1, Molecules_err_ch_1, Veff_err_ch_1)[1]

            self.mean_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().mean()
            self.mean_Photons_err_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().std() / sqrt(
                n_pixels_1)
            self.mean_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().mean()
            if not dpg.get_value('Error_type_checkbox'):
                self.mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1).stack().reset_index(
                    drop=True).dropna().mean()
            else:
                self.mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(
                    drop=True).dropna().std() / sqrt(n_pixels_1)

            self.mean_Concentration_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(
                drop=True).dropna().mean()
            if not dpg.get_value('Error_type_checkbox'):
                self.mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1).stack().reset_index(
                    drop=True).dropna().mean()
            else:
                self.mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(
                    drop=True).dropna().std() / sqrt(n_pixels_1)

            self.median_C_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().median()
            self.median_err_C_ch_1 = median_abs_deviation(
                pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna())
            dpg.set_value('sinle_phot_output_ch_1', self.mean_Photons_ch_1)

            dpg.set_value('sinle_phot_err_output_ch_1', self.mean_Photons_err_ch_1)
            dpg.set_value('sinle_mols_output_ch_1', self.mean_Molecules_ch_1)

            dpg.set_value('sinle_mols_err_output_ch_1', self.mean_Molecules_err_ch_1)
            dpg.set_value('single_conc_output_ch_1', self.mean_Concentration_ch_1)

            dpg.set_value('single_conc_err_output_ch_1', self.mean_Concentration_err_ch_1)
            Molecules_ch_1 = pd.DataFrame(Molecules_ch_1)
            Concentration_ch_1 = pd.DataFrame(Concentration_ch_1)

            Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1)
            Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1)

            Phot_hist_ch_1, Phot_bins_ch_1 = np.histogram(Photons_1.stack().reset_index(drop=True).dropna().values,
                                                          density=True, bins='auto')
            Phot_bins_ch_1 = Phot_bins_ch_1[:-1]
            median_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().median()

            Mols_hist_ch_1, Mols_bins_ch_1 = np.histogram(
                pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().values
                , density=True, bins='auto')
            Mols_bins_ch_1 = Mols_bins_ch_1[:-1]
            median_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().median()

            Conc_hist_ch_1, Conc_bins_ch_1 = np.histogram(
                pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().values
                , density=True, bins='auto')
            Conc_bins_ch_1 = Conc_bins_ch_1[:-1]

            ind = np.where(Conc_hist_ch_1 != 0)[0]

            Conc_hist_ch_1 = Conc_hist_ch_1[ind]
            Conc_bins_ch_1 = Conc_bins_ch_1[ind]

            ind = np.where(Mols_hist_ch_1 != 0)[0]

            Mols_hist_ch_1 = Mols_hist_ch_1[ind]
            Mols_bins_ch_1 = Mols_bins_ch_1[ind]

            ind = np.where(Phot_hist_ch_1 != 0)[0]

            Phot_hist_ch_1 = Phot_hist_ch_1[ind]
            Phot_bins_ch_1 = Phot_bins_ch_1[ind]

            dpg.set_value('c_dist_ser_ch_1', (Conc_bins_ch_1, Conc_hist_ch_1))
            dpg.set_value('c_mean_ser_ch_1',
                          (np.array([self.mean_Concentration_ch_1]), np.array([max(Conc_hist_ch_1)])))
            dpg.set_value('c_med_ser_ch_1', (np.array([self.median_C_ch_1]), np.array([max(Conc_hist_ch_1)])))
            dpg.set_axis_limits('hist_xc_axis_ch1', min(Conc_bins_ch_1), max(Conc_bins_ch_1))
            dpg.set_axis_limits('hist_yc_axis_ch1', 0, max(Conc_hist_ch_1))

            dpg.set_value('np_dist_ser_ch_1', (Mols_bins_ch_1, Mols_hist_ch_1))
            dpg.set_value('np_mean_ser_ch_1', (np.array([self.mean_Molecules_ch_1]), np.array([max(Mols_hist_ch_1)])))
            dpg.set_value('np_med_ser_ch_1', (np.array([median_Molecules_ch_1]), np.array([max(Mols_hist_ch_1)])))
            dpg.set_axis_limits('hist_xnp_axis_ch1', min(Mols_bins_ch_1), max(Mols_bins_ch_1))
            dpg.set_axis_limits('hist_ynp_axis_ch1', 0, max(Mols_hist_ch_1))

            dpg.set_value('phot_dist_ser_ch_1', (Phot_bins_ch_1, Phot_hist_ch_1))
            dpg.set_value('phot_mean_ser_ch_1', (np.array([self.mean_Photons_ch_1]), np.array([max(Phot_hist_ch_1)])))
            dpg.set_value('phot_med_ser_ch_1', (np.array([median_Photons_ch_1]), np.array([max(Phot_hist_ch_1)])))
            dpg.set_axis_limits('hist_xphot_axis_ch1', min(Phot_bins_ch_1), max(Phot_bins_ch_1))
            dpg.set_axis_limits('hist_yphot_axis_ch1', 0, max(Phot_hist_ch_1))

            dpg.configure_item('c_mean_ser_ch_1', label='Mean = ' + str(np.round(self.mean_Concentration_ch_1, 4)))
            dpg.configure_item('c_med_ser_ch_1', label='Median = ' + str(np.round(self.median_C_ch_1, 4)))

            dpg.configure_item('np_mean_ser_ch_1', label='Mean = ' + str(np.round(self.mean_Molecules_ch_1, 2)))
            dpg.configure_item('np_med_ser_ch_1', label='Median = ' + str(np.round(median_Molecules_ch_1, 2)))

            dpg.configure_item('phot_mean_ser_ch_1', label='Mean = ' + str(np.round(self.mean_Photons_ch_1, 1)))
            dpg.configure_item('phot_med_ser_ch_1', label='Median = ' + str(np.round(median_Photons_ch_1, 1)))

            try:
                dpg.show_item('hist_conc_plot_ch1')
            except:
                pass

            try:
                dpg.show_item('hist_np_plot_ch1')
            except:
                pass

            try:
                dpg.show_item('hist_phot_plot_ch1')
            except:
                pass

            if dpg.get_value('Photons_array_checkbox'):
                phot_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Phot_ch_1.csv')

                Photons_1.to_csv(phot_array_path_ch_1, index=False, sep=',', header=None)
            else:
                pass

            if dpg.get_value('Np_array_checkbox'):
                Np_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Np_ch_1.csv')

                Molecules_ch_1.to_csv(Np_array_path_ch_1, index=False, sep=',', header=None)

                Np_err_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Np_err_ch_1.csv')
                Molecules_err_ch_1.to_csv(Np_err_array_path_ch_1, index=False, sep=',', header=None)

            else:
                pass
            if dpg.get_value('C_array_checkbox'):
                Conc_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_conc_ch_1.csv')

                Concentration_ch_1.to_csv(Conc_array_path_ch_1, index=False, sep=',', header=None)

                Conc_err_array_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_conc_err_ch_1.csv')
                Concentration_err_ch_1.to_csv(Conc_err_array_path_ch_1, index=False, sep=',', header=None)

            else:
                pass

            if dpg.get_value('Photons_Hmaps_checkbox'):
                phot_hmap_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Phot_HM_ch_1.png')

                fig = Figure(facecolor='white')

                ax = fig.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Photons_1.min().min(), vmax=Photons_1.max().max())
                ax.imshow(Photons_1, cmap=cmap)

                ax.axis('off')
                fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                FigureCanvas(fig).print_png(phot_hmap_path_ch_1)

            else:
                pass

            if dpg.get_value('Np_Hmaps_checkbox'):
                Np_hmap_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_Np_HM_ch_1.png')

                fig1 = Figure(facecolor='white')

                ax = fig1.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Molecules_ch_1.min().min(), vmax=Molecules_ch_1.max().max())
                ax.imshow(Molecules_ch_1, cmap=cmap)

                ax.axis('off')
                fig1.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                FigureCanvas(fig1).print_png(Np_hmap_path_ch_1)

            else:
                pass

            if dpg.get_value('C_Hmaps_checkbox'):
                C_hmap_path_ch_1 = os.path.join(self.PTU_directory, self.anal_file + '_conc_HM_ch_1.png')
                fig1 = Figure(facecolor='white')
                ax = fig1.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Concentration_ch_1.min().min(), vmax=Concentration_ch_1.max().max())
                ax.imshow(Concentration_ch_1, cmap=cmap)

                ax.axis('off')
                fig1.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                FigureCanvas(fig1).print_png(C_hmap_path_ch_1)

            else:
                pass

            brightness_ch_2 = dpg.get_value('Brightness_input_ch_2')
            brightness_err_ch_2 = dpg.get_value('Brightness_err_input_ch_2')
            Veff_ch_2 = 1e-15 * dpg.get_value('focal_vol_input_ch_2')
            Veff_err_ch_2 = 1e-15 * dpg.get_value('focal_vol_err_input_ch_2')
            # DF2 = Current_image_2
            if self.processor_2.all_masks is not None and dpg.get_value('Auto_ROI_checkbox'):
                # lprint('in if2')
                ROI = self.processor_2.all_masks[0].astype(np.uint8)
                roi = np.where(ROI==0,np.nan,1)
                img = self.processor_2.image
                self.DF2 = img*roi
            else:
                self.DF2 = self.image_2_times_roi
            # self.DF2 = self.image_2_times_roi
            Photons_2 = pd.DataFrame(self.DF2)
            n_pixels_2 = Photons_2.stack().reset_index(drop=True).dropna().count()

            self.mean_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().mean()
            self.mean_Photons_err_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().std() / sqrt(
                n_pixels_2)
            Molecules_ch_2 = self.calc_molecules(self.DF2,
                                                 self.PTU_Px_dwell,
                                                 self.PTU_N_frames,
                                                 brightness_ch_2,
                                                 brightness_err_ch_2)[0]
            Molecules_err_ch_2 = self.calc_molecules(self.DF2,
                                                     self.PTU_Px_dwell,
                                                     self.PTU_N_frames,
                                                     brightness_ch_2,
                                                     brightness_err_ch_2)[1]

            Concentration_ch_2 = 1e9 * self.CONC(Molecules_ch_2, Veff_ch_2, Molecules_err_ch_2, Veff_err_ch_2)[0]
            Concentration_err_ch_2 = 1e9 * self.CONC(Molecules_ch_2, Veff_ch_2, Molecules_err_ch_2, Veff_err_ch_2)[1]

            self.mean_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().mean()
            if not dpg.get_value('Error_type_checkbox'):
                self.mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2).stack().reset_index(
                    drop=True).dropna().mean()
            else:
                self.mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(
                    drop=True).dropna().std() / sqrt(n_pixels_2)

            self.mean_Concentration_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(
                drop=True).dropna().mean()
            if not dpg.get_value('Error_type_checkbox'):
                self.mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2).stack().reset_index(
                    drop=True).dropna().mean()
            else:
                self.mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(
                    drop=True).dropna().std() / sqrt(n_pixels_2)

            self.median_C_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().median()
            self.median_err_C_ch_2 = median_abs_deviation(
                pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna())
            dpg.set_value('sinle_phot_output_ch_2', self.mean_Photons_ch_2)

            dpg.set_value('sinle_phot_err_output_ch_2', self.mean_Photons_err_ch_2)
            dpg.set_value('sinle_mols_output_ch_2', self.mean_Molecules_ch_2)

            dpg.set_value('sinle_mols_err_output_ch_2', self.mean_Molecules_err_ch_2)
            dpg.set_value('single_conc_output_ch_2', self.mean_Concentration_ch_2)

            dpg.set_value('single_conc_err_output_ch_2', self.mean_Concentration_err_ch_2)
            Molecules_ch_2 = pd.DataFrame(Molecules_ch_2)
            Concentration_ch_2 = pd.DataFrame(Concentration_ch_2)

            Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2)
            Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2)
            Phot_hist_ch_2, Phot_bins_ch_2 = np.histogram(Photons_2.stack().reset_index(drop=True).dropna().values,
                                                          density=True, bins='auto')
            Phot_bins_ch_2 = Phot_bins_ch_2[:-1]
            median_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().median()

            Mols_hist_ch_2, Mols_bins_ch_2 = np.histogram(
                pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().values
                , density=True, bins='auto')
            Mols_bins_ch_2 = Mols_bins_ch_2[:-1]
            median_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().median()

            Conc_hist_ch_2, Conc_bins_ch_2 = np.histogram(
                pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().values
                , density=True, bins='auto')
            Conc_bins_ch_2 = Conc_bins_ch_2[:-1]

            ind = np.where(Conc_hist_ch_2 != 0)[0]

            Conc_hist_ch_2 = Conc_hist_ch_2[ind]
            Conc_bins_ch_2 = Conc_bins_ch_2[ind]

            ind = np.where(Mols_hist_ch_2 != 0)[0]

            Mols_hist_ch_2 = Mols_hist_ch_2[ind]
            Mols_bins_ch_2 = Mols_bins_ch_2[ind]

            ind = np.where(Phot_hist_ch_2 != 0)[0]

            Phot_hist_ch_2 = Phot_hist_ch_2[ind]
            Phot_bins_ch_2 = Phot_bins_ch_2[ind]

            dpg.set_value('c_dist_ser_ch_2', (Conc_bins_ch_2, Conc_hist_ch_2))
            dpg.set_value('c_mean_ser_ch_2',
                          (np.array([self.mean_Concentration_ch_2]), np.array([max(Conc_hist_ch_2)])))
            dpg.set_value('c_med_ser_ch_2', (np.array([self.median_C_ch_2]), np.array([max(Conc_hist_ch_2)])))
            dpg.set_axis_limits('hist_xc_axis_ch2', min(Conc_bins_ch_2), max(Conc_bins_ch_2))
            dpg.set_axis_limits('hist_yc_axis_ch2', 0, max(Conc_hist_ch_2))

            dpg.set_value('np_dist_ser_ch_2', (Mols_bins_ch_2, Mols_hist_ch_2))
            dpg.set_value('np_mean_ser_ch_2', (np.array([self.mean_Molecules_ch_2]), np.array([max(Mols_hist_ch_2)])))
            dpg.set_value('np_med_ser_ch_2', (np.array([median_Molecules_ch_2]), np.array([max(Mols_hist_ch_2)])))
            dpg.set_axis_limits('hist_xnp_axis_ch2', min(Mols_bins_ch_2), max(Mols_bins_ch_2))
            dpg.set_axis_limits('hist_ynp_axis_ch2', 0, max(Mols_hist_ch_2))

            dpg.set_value('phot_dist_ser_ch_2', (Phot_bins_ch_2, Phot_hist_ch_2))
            dpg.set_value('phot_mean_ser_ch_2', (np.array([self.mean_Photons_ch_2]), np.array([max(Phot_hist_ch_2)])))
            dpg.set_value('phot_med_ser_ch_2', (np.array([median_Photons_ch_2]), np.array([max(Phot_hist_ch_2)])))
            dpg.set_axis_limits('hist_xphot_axis_ch2', min(Phot_bins_ch_2), max(Phot_bins_ch_2))
            dpg.set_axis_limits('hist_yphot_axis_ch2', 0, max(Phot_hist_ch_2))

            dpg.configure_item('c_mean_ser_ch_2', label='Mean = ' + str(np.round(self.mean_Concentration_ch_2, 4)))
            dpg.configure_item('c_med_ser_ch_2', label='Median = ' + str(np.round(self.median_C_ch_2, 4)))

            dpg.configure_item('np_mean_ser_ch_2', label='Mean = ' + str(np.round(self.mean_Molecules_ch_2, 2)))
            dpg.configure_item('np_med_ser_ch_2', label='Median = ' + str(np.round(median_Molecules_ch_2, 2)))

            dpg.configure_item('phot_mean_ser_ch_2', label='Mean = ' + str(np.round(self.mean_Photons_ch_2, 1)))
            dpg.configure_item('phot_med_ser_ch_2', label='Median = ' + str(np.round(median_Photons_ch_2, 1)))

            try:
                dpg.show_item('hist_conc_plot_ch2')
            except:
                pass

            try:
                dpg.show_item('hist_np_plot_ch2')
            except:
                pass

            try:
                dpg.show_item('hist_phot_plot_ch2')
            except:
                pass

            if dpg.get_value('Photons_array_checkbox'):
                phot_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Phot_ch_2.csv')

                Photons_2.to_csv(phot_array_path_ch_2, index=False, sep=',', header=None)
            else:
                pass

            if dpg.get_value('Np_array_checkbox'):
                Np_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Np_ch_2.csv')

                Molecules_ch_2.to_csv(Np_array_path_ch_2, index=False, sep=',', header=None)

                Np_err_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Np_err_ch_2.csv')
                Molecules_err_ch_2.to_csv(Np_err_array_path_ch_2, index=False, sep=',', header=None)
            else:
                pass
            if dpg.get_value('C_array_checkbox'):
                Conc_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_conc_ch_2.csv')

                Concentration_ch_2.to_csv(Conc_array_path_ch_2, index=False, sep=',', header=None)

                Conc_err_array_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_conc_err_ch_2.csv')
                Concentration_err_ch_2.to_csv(Conc_err_array_path_ch_2, index=False, sep=',', header=None)
            else:
                pass

            if dpg.get_value('Photons_Hmaps_checkbox'):
                phot_hmap_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Phot_HM_ch_2.png')

                fig = Figure(facecolor='white')

                ax = fig.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Photons_2.min().min(), vmax=Photons_2.max().max())
                ax.imshow(Photons_2, cmap=cmap)

                ax.axis('off')
                fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                FigureCanvas(fig).print_png(phot_hmap_path_ch_2)

            else:
                pass

            if dpg.get_value('Np_Hmaps_checkbox'):
                Np_hmap_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_Np_HM_ch_2.png')

                fig2 = Figure(facecolor='white')

                ax = fig2.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Molecules_ch_2.min().min(), vmax=Molecules_ch_2.max().max())
                ax.imshow(Molecules_ch_2, cmap=cmap)

                ax.axis('off')
                fig2.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                FigureCanvas(fig2).print_png(Np_hmap_path_ch_2)

            else:
                pass

            if dpg.get_value('C_Hmaps_checkbox'):
                C_hmap_path_ch_2 = os.path.join(self.PTU_directory, self.anal_file + '_conc_HM_ch_2.png')
                fig2 = Figure(facecolor='white')
                ax = fig2.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Concentration_ch_2.min().min(), vmax=Concentration_ch_2.max().max())
                ax.imshow(Concentration_ch_2, cmap=cmap)

                ax.axis('off')
                fig2.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
                FigureCanvas(fig2).print_png(C_hmap_path_ch_2)

            else:
                pass

        else:
            pass

    def callback_calculate_all(self, sender, app_data):
        self.initialize_res_df()
        # print(self.files)
        filenames = [f.replace('.ptu', '') for f in self.files]
        # print(filenames)
        if dpg.get_value('Auto_ROI_checkbox') or (not dpg.get_value('Auto_ROI_checkbox') and not dpg.get_value('FILE_ROI_checkbox')):
            roiname=dpg.get_value('ROI_name_tag')
            for cnt, an_file in enumerate(filenames):
                # print(cnt,an_file)
                self.anal_file = an_file
    
                dpg.configure_item('file_box', default_value=an_file)
                
                # self.load_PTU_images(an_file)
                # self.callback_calculate(sender,app_data)
                
                    
                self.callback_listbox('file_box',self.anal_file)
                if len(self.Channels) == 1:
                    if '1' in self.Channels[0]:
    
                        Sing_Results_DF_tmp = pd.DataFrame([[self.anal_file,
                                                             roiname,
                                                             1,
                                                             self.mean_Photons_ch_1,
                                                             self.mean_Photons_err_ch_1,
                                                             self.mean_Molecules_ch_1,
                                                             self.mean_Molecules_err_ch_1,
                                                             self.mean_Concentration_ch_1,
                                                             self.mean_Concentration_err_ch_1,
                                                             self.median_C_ch_1,
                                                             self.median_err_C_ch_1]],
                                                           columns=self.Sing_Results_DF.columns)
    
                    elif '2' in self.Channels[0]:
                        Sing_Results_DF_tmp = pd.DataFrame([[self.anal_file,
                                                             roiname,
                                                             2,
                                                             self.mean_Photons_ch_2,
                                                             self.mean_Photons_err_ch_2,
                                                             self.mean_Molecules_ch_2,
                                                             self.mean_Molecules_err_ch_2,
                                                             self.mean_Concentration_ch_2,
                                                             self.mean_Concentration_err_ch_2,
                                                             self.median_C_ch_2,
                                                             self.median_err_C_ch_2]],
                                                           columns=self.Sing_Results_DF.columns)
                    else:
                        pass
    
                if len(self.Channels) == 2:
                    Sing_Results_DF_tmp = pd.DataFrame([[self.anal_file,
                                                         roiname,
                                                         1,
                                                         self.mean_Photons_ch_1,
                                                         self.mean_Photons_err_ch_1,
                                                         self.mean_Molecules_ch_1,
                                                         self.mean_Molecules_err_ch_1,
                                                         self.mean_Concentration_ch_1,
                                                         self.mean_Concentration_err_ch_1,
                                                         self.median_C_ch_1,
                                                         self.median_err_C_ch_1],
                                                        [self.anal_file,
                                                         roiname,
                                                         2,
                                                         self.mean_Photons_ch_2,
                                                         self.mean_Photons_err_ch_2,
                                                         self.mean_Molecules_ch_2,
                                                         self.mean_Molecules_err_ch_2,
                                                         self.mean_Concentration_ch_2,
                                                         self.mean_Concentration_err_ch_2,
                                                         self.median_C_ch_2,
                                                         self.median_err_C_ch_2]],
                                                       columns=self.Sing_Results_DF.columns)
                self.Sing_Results_DF = pd.concat([self.Sing_Results_DF, Sing_Results_DF_tmp]).reset_index(drop=True)
                self._pkl_file()
        elif dpg.get_value('FILE_ROI_checkbox'):
            for cnt, an_file in enumerate(filenames):
                # print(cnt,an_file)
                self.anal_file = an_file
    
                dpg.configure_item('file_box', default_value=an_file)
                
                # self.load_PTU_images(an_file)
                # self.callback_calculate(sender,app_data)
                
                    
                # self.callback_listbox('file_box',self.anal_file)
            

                ROIS = dpg.get_item_configuration('ROI_names_combo_tag')['items']
                
                self.callback_listbox('file_box',self.anal_file)

                for ROI in ROIS:
                    self.callback_ROI_names_combo('ROI_names_combo_tag', ROI)
                    roiname = ROI
                    if len(self.Channels) == 1:
                        if '1' in self.Channels[0]:
        
                            Sing_Results_DF_tmp = pd.DataFrame([[self.anal_file,
                                                                 roiname,
                                                                 1,
                                                                 self.mean_Photons_ch_1,
                                                                 self.mean_Photons_err_ch_1,
                                                                 self.mean_Molecules_ch_1,
                                                                 self.mean_Molecules_err_ch_1,
                                                                 self.mean_Concentration_ch_1,
                                                                 self.mean_Concentration_err_ch_1,
                                                                 self.median_C_ch_1,
                                                                 self.median_err_C_ch_1]],
                                                               columns=self.Sing_Results_DF.columns)
        
                        elif '2' in self.Channels[0]:
                            Sing_Results_DF_tmp = pd.DataFrame([[self.anal_file,
                                                                 roiname,
                                                                 2,
                                                                 self.mean_Photons_ch_2,
                                                                 self.mean_Photons_err_ch_2,
                                                                 self.mean_Molecules_ch_2,
                                                                 self.mean_Molecules_err_ch_2,
                                                                 self.mean_Concentration_ch_2,
                                                                 self.mean_Concentration_err_ch_2,
                                                                 self.median_C_ch_2,
                                                                 self.median_err_C_ch_2]],
                                                               columns=self.Sing_Results_DF.columns)
                        else:
                            pass
        
                    elif len(self.Channels) == 2:
                        Sing_Results_DF_tmp = pd.DataFrame([[self.anal_file,
                                                             roiname,
                                                             1,
                                                             self.mean_Photons_ch_1,
                                                             self.mean_Photons_err_ch_1,
                                                             self.mean_Molecules_ch_1,
                                                             self.mean_Molecules_err_ch_1,
                                                             self.mean_Concentration_ch_1,
                                                             self.mean_Concentration_err_ch_1,
                                                             self.median_C_ch_1,
                                                             self.median_err_C_ch_1],
                                                            [self.anal_file,
                                                             roiname,
                                                             2,
                                                             self.mean_Photons_ch_2,
                                                             self.mean_Photons_err_ch_2,
                                                             self.mean_Molecules_ch_2,
                                                             self.mean_Molecules_err_ch_2,
                                                             self.mean_Concentration_ch_2,
                                                             self.mean_Concentration_err_ch_2,
                                                             self.median_C_ch_2,
                                                             self.median_err_C_ch_2]],
                                                           columns=self.Sing_Results_DF.columns)
                
                    self.Sing_Results_DF = pd.concat([self.Sing_Results_DF, Sing_Results_DF_tmp]).reset_index(drop=True)
                self._pkl_file()
            

            

    def callback_directory_select(self, sender, app_data):
        self.files = ()
        self.directory = app_data['file_path_name']
        self.PTU_directory = self.directory
        self.new_directory = self.directory
        self.last_directory = self.directory
        self.update_dialogs_default_directory(self.last_directory)
        self.files = tuple(np.sort([f for f in os.listdir(self.directory) if f.endswith('.ptu')]))

        if len(files) == 0:
            show_error_no_files('No PTU files found.')
        else:
            self.update_flist(self.files)

        self.anal_file = files[0]
        dpg.configure_item('file_box', default_value=self.anal_file)

    def callback_empty(self, sender, app_data):
        '''Empty function. Do nothing.'''
        pass

    def callback_kappa_err_input(self, sender, app_data):

        if sender == 'kappa_err_input_ch_1':
            omega = dpg.get_value('omega_input_ch_1')
            omega_err = dpg.get_value('omega_err_input_ch_1')
            kappa = dpg.get_value('kappa_input_ch_1')
            kappa_err = app_data
            foc_vol = self.VEFF(omega, kappa, omega_err, kappa_err)
            dpg.configure_item('focal_vol_input_ch_1', default_value=foc_vol[0])
            dpg.configure_item('focal_vol_err_input_ch_1', default_value=foc_vol[1])
        else:
            omega = dpg.get_value('omega_input_ch_2')
            omega_err = dpg.get_value('omega_err_input_ch_2')
            kappa = dpg.get_value('kappa_input_ch_2')
            kappa_err = app_data
            foc_vol = self.VEFF(omega, kappa, omega_err, kappa_err)
            dpg.configure_item('focal_vol_input_ch_2', default_value=foc_vol[0])
            dpg.configure_item('focal_vol_err_input_ch_2', default_value=foc_vol[1])

    def callback_kappa_input(self, sender, app_data):

        if sender == 'kappa_input_ch_1':
            omega = dpg.get_value('omega_input_ch_1')
            omega_err = dpg.get_value('omega_err_input_ch_1')
            kappa = app_data
            kappa_err = dpg.get_value('kappa_err_input_ch_1')
            foc_vol = self.VEFF(omega, kappa, omega_err, kappa_err)
            dpg.configure_item('focal_vol_input_ch_1', default_value=foc_vol[0])
            dpg.configure_item('focal_vol_err_input_ch_1', default_value=foc_vol[1])
        else:
            omega = dpg.get_value('omega_input_ch_2')
            omega_err = dpg.get_value('omega_err_input_ch_2')
            kappa = app_data
            kappa_err = dpg.get_value('kappa_err_input_ch_2')
            foc_vol = self.VEFF(omega, kappa, omega_err, kappa_err)
            dpg.configure_item('focal_vol_input_ch_2', default_value=foc_vol[0])
            dpg.configure_item('focal_vol_err_input_ch_2', default_value=foc_vol[1])

    def callback_listbox(self, sender, app_data):
        self.anal_file = app_data

        pkl_file = self.anal_file + '.rpk'
        pkl_path = os.path.join(self.PTU_directory, pkl_file)
        # lnprint(pkl_file)
        if os.path.exists(pkl_path):
            # lnprint('loading_pkl')
            self.pkl = self._load_pkl_file(pkl_path)

        else:
            self.pkl = {}

        self.load_PTU_images(self.anal_file)
        self.hide_histograms()
        self.callback_calculate(sender, app_data)

    def callback_no_files_dialog_close_only(self, sender, app_data):
        dpg.configure_item('No_data_files', show=False)
        dpg.delete_item('no_files_error_text')
        dpg.delete_item('no_files_error_butt')
        dpg.delete_item('No_data_files')

    def callback_omega_err_input(self, sender, app_data):

        if sender == 'omega_err_input_ch_1':
            omega = dpg.get_value('omega_input_ch_1')
            omega_err = app_data
            kappa = dpg.get_value('kappa_input_ch_1')
            kappa_err = dpg.get_value('kappa_err_input_ch_1')
            foc_vol = self.VEFF(omega, kappa, omega_err, kappa_err)
            dpg.configure_item('focal_vol_input_ch_1', default_value=foc_vol[0])
            dpg.configure_item('focal_vol_err_input_ch_1', default_value=foc_vol[1])
        else:
            omega = dpg.get_value('omega_input_ch_2')
            omega_err = app_data
            kappa = dpg.get_value('kappa_input_ch_2')
            kappa_err = dpg.get_value('kappa_err_input_ch_2')
            foc_vol = self.VEFF(omega, kappa, omega_err, kappa_err)
            dpg.configure_item('focal_vol_input_ch_2', default_value=foc_vol[0])
            dpg.configure_item('focal_vol_err_input_ch_2', default_value=foc_vol[1])

    def callback_omega_input(self, sender, app_data):

        if sender == 'omega_input_ch_1':
            omega = app_data
            omega_err = dpg.get_value('omega_err_input_ch_1')
            kappa = dpg.get_value('kappa_input_ch_1')
            kappa_err = dpg.get_value('kappa_err_input_ch_1')
            foc_vol = self.VEFF(omega, kappa, omega_err, kappa_err)
            dpg.configure_item('focal_vol_input_ch_1', default_value=foc_vol[0])
            dpg.configure_item('focal_vol_err_input_ch_1', default_value=foc_vol[1])
        else:
            omega = app_data
            omega_err = dpg.get_value('omega_err_input_ch_2')
            kappa = dpg.get_value('kappa_input_ch_2')
            kappa_err = dpg.get_value('kappa_err_input_ch_2')
            foc_vol = self.VEFF(omega, kappa, omega_err, kappa_err)
            dpg.configure_item('focal_vol_input_ch_2', default_value=foc_vol[0])
            dpg.configure_item('focal_vol_err_input_ch_2', default_value=foc_vol[1])

    def callback_remove_result_button(self, sender, app_data):
        if sender == 'remove_button_results_ch_1':
            ind_result_to_remove = []
            for i in self.FCS_results_ch_1.index:
                if dpg.get_value('ch_1_results_delete_' + str(i) + '_check_ch_1'):
                    ind_result_to_remove.append(i)

            self.FCS_results_ch_1.drop(self.FCS_results_ch_1.index[ind_result_to_remove], inplace=True)
            self.FCS_results_ch_1.reset_index(drop=True, inplace=True)

            self.mean_bright_input_ch_1()

            for alias in dpg.get_aliases():
                if alias.startswith('ch_1_results_show_'):
                    try:

                        dpg.delete_item(alias)
                    except:
                        pass
                if alias.startswith('ch_1_results_delete_'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            for alias in dpg.get_aliases():
                if alias.startswith('ch_1_row_results_show'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            for i in self.FCS_results_ch_1.index:
                with dpg.table_row(tag='ch_1_row_results_show_ch_1' + str(i),
                                   parent='table_results_show_ch_1'):
                    dpg.add_text(self.FCS_results_ch_1.at[i, 'file'],
                                 tag='ch_1_results_show_' + str(i) + '_name_ch_1')
                    dpg.add_text(np.round(self.FCS_results_ch_1.at[i, 'N_p'], 2),
                                 tag='ch_1_results_show_' + str(i) + '_N_p_value_ch_1')
                    dpg.add_text(self.FCS_results_ch_1.at[i, 'Brightness'],
                                 tag='ch_1_results_show_' + str(i) + '_Brightness_value_ch_1')
                    dpg.add_checkbox(label='',
                                     tag='ch_1_results_delete_' + str(i) + '_check_ch_1')
        else:
            ind_result_to_remove = []
            for i in self.FCS_results_ch_2.index:
                if dpg.get_value('ch_2_results_delete_' + str(i) + '_check_ch_2'):
                    ind_result_to_remove.append(i)
            self.FCS_results_ch_2.drop(self.FCS_results_ch_2.index[ind_result_to_remove], inplace=True)
            self.FCS_results_ch_2.reset_index(drop=True, inplace=True)

            self.mean_bright_input_ch_2()

            for alias in dpg.get_aliases():
                if alias.startswith('ch_2_results_show_'):
                    try:

                        dpg.delete_item(alias)
                    except:
                        pass
                if alias.startswith('ch_2_results_delete_'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            for alias in dpg.get_aliases():
                if alias.startswith('ch_2_row_results_show'):
                    try:
                        dpg.delete_item(alias)
                    except:
                        pass
            for i in self.FCS_results_ch_2.index:
                with dpg.table_row(tag='ch_2_row_results_show_ch_2' + str(i),
                                   parent='table_results_show_ch_2'):
                    dpg.add_text(self.FCS_results_ch_2.at[i, 'file'],
                                 tag='ch_2_results_show_' + str(i) + '_name_ch_2')
                    dpg.add_text(np.round(self.FCS_results_ch_2.at[i, 'N_p'], 2),
                                 tag='ch_2_results_show_' + str(i) + '_N_p_value_ch_2')
                    dpg.add_text(self.FCS_results_ch_2.at[i, 'Brightness'],
                                 tag='ch_2_results_show_' + str(i) + '_Brightness_value_ch_2')
                    dpg.add_checkbox(label='',
                                     tag='ch_2_results_delete_' + str(i) + '_check_ch_2')

    def callback_reset_results_DF(self):
        self.initialize_res_df()

        files = os.listdir(self.PTU_directory)
        files = [f for f in files if f.endswith('.rpk')]
        for f in files:
            os.remove(os.path.join(self.PTU_directory, f))

    def callback_select_lt_to_roi(self, sender, app_data):
        self.load_PTU_images(self.anal_file)

    def callback_select_roi(self, sender, app_data):

        
        
        if dpg.get_value(sender):
            dpg.set_value('Auto_ROI_checkbox', False)
            dpg.hide_item('ROI_name_tag')
            dpg.show_item('ROI_names_combo_tag')
            self.callback_select_autoroi('Auto_ROI_checkbox', False)
            # dpg.configure_item('cell_thres_ratio_1',enabled=False)
            # dpg.configure_item('nucleus_search_1',enabled=False)
            # dpg.configure_item('nucl_thres_ratio_1',enabled=False)
            # dpg.configure_item('cell_thres_ratio_2',enabled=False)
            # dpg.configure_item('nucleus_search_2',enabled=False)
            # dpg.configure_item('nucl_thres_ratio_2',enabled=False)
            # dpg.configure_item('cp_roi_1',enabled=False)
            # dpg.configure_item('cp_roi_2',enabled=False)
            if self.ROI_directory != None and len(self.ROI_directory)!=0 :
                
                try:
                    self.load_PTU_images(self.anal_file)
                except:
                    self.show_error_no_files('Seems there is no ROI folder selected. Try again.')

            else:
                dpg.show_item('ROI_folder_dialog_id')
        else:
            dpg.show_item('ROI_name_tag')
            dpg.hide_item('ROI_names_combo_tag')
            self.load_PTU_images(self.anal_file)

        self.get_roi_state()

    def callback_select_autoroi(self, sender, app_data):
        if dpg.get_value(sender):
            dpg.set_value('FILE_ROI_checkbox', False)
            dpg.show_item('ROI_name_tag')
            dpg.hide_item('ROI_names_combo_tag')
            dpg.show_item('auto_ROI_ch_table')
            dpg.configure_item('cell_thres_ratio_1', enabled=True)
            dpg.configure_item('nucl_thres_ratio_1', enabled=True)
            dpg.configure_item('ROI_mode_1', enabled=True)
            dpg.configure_item('cp_roi_1', enabled=True)

            dpg.configure_item('cell_thres_ratio_2', enabled=True)
            dpg.configure_item('nucl_thres_ratio_2', enabled=True)
            dpg.configure_item('ROI_mode_2', enabled=True)
            dpg.configure_item('cp_roi_2', enabled=True)
            self.mode_init.file_box['num_items'] = 8
            self.mode_init.PTU_DATA_window['height'] = int(315 * self.mode_init.size_ratio['height'])

            self.mode_init.file_window['pos'] = (self.mode_init.left_indent,
                                                 self.mode_init.top_indent + self.mode_init.PTU_DATA_window[
                                                     'height'] + self.mode_init.internal_indent)

            dpg.configure_item('file_box', num_items=self.mode_init.file_box['num_items'])
            dpg.configure_item('PTU_DATA_window', height=self.mode_init.PTU_DATA_window['height'])
            dpg.configure_item('file_window',
                               pos=self.mode_init.file_window['pos'])
            # lprint(dpg.get_item_height('PTU_DATA_window'))

            self.mode_init.file_window['height'] = dpg.get_viewport_height() - (
                    self.mode_init.top_indent + dpg.get_item_height(
                'PTU_DATA_window') + self.mode_init.internal_indent + self.mode_init.bottom_indent)
            dpg.configure_item('file_window',
                               height=self.mode_init.file_window['height'])
            # self.load_PTU_images(self.anal_file)


        else:
            # lprint(sender, dpg.get_value(sender))
            dpg.hide_item('auto_ROI_ch_table')
            dpg.configure_item('cell_thres_ratio_1', enabled=False)
            dpg.configure_item('nucl_thres_ratio_1', enabled=False)
            dpg.configure_item('ROI_mode_1', enabled=False)
            dpg.configure_item('cp_roi_1', enabled=False)

            dpg.configure_item('cell_thres_ratio_2', enabled=False)
            dpg.configure_item('nucl_thres_ratio_2', enabled=False)
            dpg.configure_item('ROI_mode_2', enabled=False)
            dpg.configure_item('cp_roi_2', enabled=False)
            self.mode_init.file_box['num_items'] = 11
            self.mode_init.PTU_DATA_window['height'] = int(175 * self.mode_init.size_ratio['height'])
            self.mode_init.file_window['pos'] = (self.mode_init.left_indent,
                                                 self.mode_init.top_indent + self.mode_init.PTU_DATA_window[
                                                     'height'] + self.mode_init.internal_indent)

            dpg.configure_item('file_box', num_items=self.mode_init.file_box['num_items'])
            dpg.configure_item('PTU_DATA_window', height=self.mode_init.PTU_DATA_window['height'])
            dpg.configure_item('file_window', pos=self.mode_init.file_window['pos'])
            # lprint(dpg.get_item_height('PTU_DATA_window'))
            self.mode_init.file_window['height'] = dpg.get_viewport_height() - (
                    self.mode_init.top_indent + dpg.get_item_height(
                'PTU_DATA_window') + self.mode_init.internal_indent + self.mode_init.bottom_indent)
            dpg.configure_item('file_window', height=self.mode_init.file_window['height'])
        self.get_roi_state()
        self.load_PTU_images(self.anal_file)
        
    def display_images(self, channel):

        if channel == 1:
            self._update_textures_both_roi('ch1', None)

        elif channel == 2:
            self._update_textures_both_roi('ch2', None)

        elif channel == 'both':
            self._update_textures_both_roi('ch1', None)
            self._update_textures_both_roi('ch2', None)

    def hide_histograms(self):
        dpg.set_value('c_dist_ser_ch_1', (np.empty(2), np.empty(2)))
        dpg.set_value('c_mean_ser_ch_1', (np.empty(2), np.empty(2)))
        dpg.set_value('c_med_ser_ch_1', (np.empty(2), np.empty(2)))
        dpg.set_value('np_dist_ser_ch_1', (np.empty(2), np.empty(2)))
        dpg.set_value('np_mean_ser_ch_1', (np.empty(2), np.empty(2)))
        dpg.set_value('np_med_ser_ch_1', (np.empty(2), np.empty(2)))
        dpg.set_value('phot_dist_ser_ch_1', (np.empty(2), np.empty(2)))
        dpg.set_value('phot_mean_ser_ch_1', (np.empty(2), np.empty(2)))
        dpg.set_value('phot_med_ser_ch_1', (np.empty(2), np.empty(2)))
        dpg.configure_item('c_mean_ser_ch_1', label='Mean = ')
        dpg.configure_item('c_med_ser_ch_1', label='Median = ')
        dpg.configure_item('np_mean_ser_ch_1', label='Mean = ')
        dpg.configure_item('np_med_ser_ch_1', label='Median = ')
        dpg.configure_item('phot_mean_ser_ch_1', label='Mean = ')
        dpg.configure_item('phot_med_ser_ch_1', label='Median = ')
        dpg.hide_item('hist_conc_plot_ch1')
        dpg.hide_item('hist_np_plot_ch1')
        dpg.hide_item('hist_phot_plot_ch1')

        dpg.set_value('c_dist_ser_ch_2', (np.empty(2), np.empty(2)))
        dpg.set_value('c_mean_ser_ch_2', (np.empty(2), np.empty(2)))
        dpg.set_value('c_med_ser_ch_2', (np.empty(2), np.empty(2)))
        dpg.set_value('np_dist_ser_ch_2', (np.empty(2), np.empty(2)))
        dpg.set_value('np_mean_ser_ch_2', (np.empty(2), np.empty(2)))
        dpg.set_value('np_med_ser_ch_2', (np.empty(2), np.empty(2)))
        dpg.set_value('phot_dist_ser_ch_2', (np.empty(2), np.empty(2)))
        dpg.set_value('phot_mean_ser_ch_2', (np.empty(2), np.empty(2)))
        dpg.set_value('phot_med_ser_ch_2', (np.empty(2), np.empty(2)))
        dpg.configure_item('c_mean_ser_ch_2', label='Mean = ')
        dpg.configure_item('c_med_ser_ch_2', label='Median = ')
        dpg.configure_item('np_mean_ser_ch_2', label='Mean = ')
        dpg.configure_item('np_med_ser_ch_2', label='Median = ')
        dpg.configure_item('phot_mean_ser_ch_2', label='Mean = ')
        dpg.configure_item('phot_med_ser_ch_2', label='Median = ')
        dpg.hide_item('hist_conc_plot_ch2')
        dpg.hide_item('hist_np_plot_ch2')
        dpg.hide_item('hist_phot_plot_ch2')

    def import_ROI(self, sender, app_data, user_data):

        # global DF, DF2,pck_list,roi_1,roi_2

        # global directory, new_directory,last_directory
        self.directory = app_data['file_path_name']
        self.new_directory = self.directory
        self.last_directory = self.directory
        self.update_dialogs_default_directory(self.last_directory)

        # # lnprint('import_ROI')
        roi = self.load_ROI(app_data['file_path_name'])

        if user_data == 'Add_ROI_1_button':
            try:
                self.roi_1 = roi.to_numpy()

                self.DF = self.DF * self.roi_1
                chan = 1

            except:
                self.show_error_no_files('PTU file loaded. Try again.')
        if user_data == 'Add_ROI_2_button':
            try:
                self.roi_2 = roi.to_numpy()
                self.DF2 = self.DF2 * self.roi_2
                chan = 2
            except:
                self.show_error_no_files('PTU file loaded. Try again.')

        if len(self.pck_list) == 2:
            chan = 'both'
            # self.display_images([self.DF,self.DF2],chan)
            self.display_images(chan)
        else:
            # self.display_images([self.DF],chan)
            self.display_images(chan)


    # 
    def check_for_roi_files(self,path_to_search, anfile):
        try:
            roi_files = os.listdir(path_to_search)
        except:
            self.show_error_no_files('Seems there is no ROI folder selected. Try again.')
            return 
        roi_files = [f for f in roi_files if anfile in f]
        rois = []
        
        for f in roi_files:
            roi_n = f.split('_')
            
            roi_n = [ r for r in roi_n if r.startswith('roi')]
            roicnt = roi_n[0].replace('roi','')
            if len(roicnt)!=0:
                roin = 'ROI_'+roicnt
            else:
                roin = 'ROI_'+str(0)
            # print(roin)
            rois.append(roin)
            # print(roin)
        roiset = list(set(rois))
        roiset.sort()
        # lprint(roiset)
        output = {k:{} for k in roiset}
        for rs in roiset:
            rn = rs[-1]
            chns=[]
            for f in roi_files:
                if 'roi'+rn in f:
                    ch = f.split('_ch_')
                    ch = [ r for r in ch if r.endswith('.dat')][0][0]
                    # print(ch)
                    # chns.append(ch)
            # for ch in chns:
                    output[rs]['ch_'+ch] = f
                    
        # lprint(rois)
        
        
        return output

    def callback_ROI_names_combo(self, sender, app_data):
        ROIn = app_data
        roin = ROIn.replace('ROI_','')
        # lprint(roin)
        if len(self.Channels) == 1:
            if '1' in self.Channels[0]:
                roi_1_path = os.path.join(self.ROI_directory, self.anal_file + '_roi'+roin+'_ch_1.dat')
                self.roi_1 = self.load_ROI(roi_1_path).to_numpy()
                self.processor_1.roi_image = self.roi_1
                self.image_1_times_roi = self.Current_image_1
                self.display_images('both')
            elif '2' in self.Channels[0]:
                roi_2_path = os.path.join(self.ROI_directory, self.anal_file + '_roi'+roin+'_ch_2.dat')
                self.roi_2 = self.load_ROI(roi_2_path).to_numpy()
                self.processor_2.roi_image = self.roi_2
                self.image_2_times_roi = self.Current_image_2
                self.display_images('both')
        elif len(self.Channels) == 2:
            roi_1_path = os.path.join(self.ROI_directory, self.anal_file + '_roi'+roin+'_ch_1.dat')
            self.roi_1 = self.load_ROI(roi_1_path).to_numpy()
            self.processor_1.roi_image = self.roi_1
            self.image_1_times_roi = self.Current_image_1

            roi_2_path = os.path.join(self.ROI_directory, self.anal_file + '_roi'+roin+'_ch_2.dat')
            self.roi_2 = self.load_ROI(roi_2_path).to_numpy()
            self.processor_2.roi_image = self.roi_2
            self.image_2_times_roi = self.Current_image_2

            self.display_images('both')
            
            
            
        
        
    
    def load_PTU_images(self, an_file):
        self.pkl_data = {}
        dpg.set_value('ROI_name_tag', 'ROI_0')
        pickle_file = os.path.join(self.PTU_directory, an_file + '.pkl')
        # lprint(pickle_file)
        with open(pickle_file, 'rb') as pcklf:
            pklf = pickle.load(pcklf)

        ptu_meta = pklf['File info']  # json.load(f)
        try:
            self.DF = self.DF2 = []
        except:
            pass

        self.PTU_Resolution = str(ptu_meta['Pixels per line']) + 'x' + str(ptu_meta['Number of lines'])
        self.PTU_Px_size = ptu_meta['Pixels size']
        self.PTU_N_frames = ptu_meta['Number of frames']
        self.PTU_Px_dwell = ptu_meta['Pixel dwell']
        # tau_resolution = ptu_meta['Lifetime resolution']

        dpg.set_value('Resolution_output', 'Resolution: ' + self.PTU_Resolution)
        dpg.set_value('Pixel_size_output', self.PTU_Px_size)
        dpg.set_value('Nframes_output', self.PTU_N_frames)
        dpg.set_value('Pixel_dwell_output', self.PTU_Px_dwell)

        dpg.set_value('sinle_phot_output_ch_1', 0)
        dpg.set_value('sinle_phot_err_output_ch_1', 0)
        dpg.set_value('sinle_mols_output_ch_1', 0)
        dpg.set_value('sinle_mols_err_output_ch_1', 0)
        dpg.set_value('single_conc_output_ch_1', 0)
        dpg.set_value('single_conc_err_output_ch_1', 0)
        dpg.set_value('sinle_phot_output_ch_2', 0)
        dpg.set_value('sinle_phot_err_output_ch_2', 0)
        dpg.set_value('sinle_mols_output_ch_2', 0)
        dpg.set_value('sinle_mols_err_output_ch_2', 0)
        dpg.set_value('single_conc_output_ch_2', 0)
        dpg.set_value('single_conc_err_output_ch_2', 0)

        # dpg.set_value('cell_thres_ratio_1',1.0)
        # dpg.set_value('cell_thres_ratio_2',1.0)
        # dpg.set_value('nucl_thres_ratio_1',1.5)
        # dpg.set_value('nucl_thres_ratio_2',1.5)

        if self.PTU_N_frames > 1:
            self.PTU_N_frames = self.PTU_N_frames - 1
        else:
            pass
        ptu_files = list(np.sort([f for f in os.listdir(self.PTU_directory) if f.endswith('.ptu')]))

        self.Channels = list(pklf.keys())
        self.Channels = [f for f in self.Channels if f.startswith('export_df')]
        self.Channels = [ch[-1] for ch in self.Channels]

        if dpg.get_value('FILE_ROI_checkbox'):
            Existing_Rois = self.check_for_roi_files(self.ROI_directory, an_file)
            dpg.configure_item('ROI_names_combo_tag',items=list(Existing_Rois.keys()))
            dpg.set_value('ROI_names_combo_tag',list(Existing_Rois.keys())[0])
        
            if len(self.Channels) == 1:
                if '1' in self.Channels[0]:
                    Intensity_1 = pklf['intensity_1']

                    Intensity_1 = Intensity_1
                    self.processor_1 = ImageROIProcessor()
                    self.processor_1.image = Intensity_1.astype(np.uint16)

                    
                        
                    
                    
                    
                    # except:
                    #     self.show_error_no_files('Seems there is no ROI folder selected. Try again.')

                    
                    roi_1_path = os.path.join(self.ROI_directory, an_file + '_roi_ch_1.dat')
                    if os.path.exists(roi_1_path):
                        pass
                    else:
                        roi_1_path = os.path.join(self.ROI_directory, an_file + '_roi0_ch_1.dat')
                    
                    self.roi_1 = self.load_ROI(roi_1_path).to_numpy()
                    self.processor_1.roi_image = self.roi_1
                    Intensity_1 = Intensity_1
                    channel = 'both'
                    # channel = 1

                    self.Current_image_1 = Intensity_1 / np.max(Intensity_1)
                    self.image_1_times_roi = self.Current_image_1
                    self.processor_2 = ImageROIProcessor()
                    self.processor_2.image = np.clip((self.NO_IMAGE_INTENSITY), 0, 1).astype(np.float64)
                    self.Current_image_2 = self.NO_IMAGE_INTENSITY
                    # self.display_images([self.Current_image_1,self.Current_image_2],channel)
                    self.display_images(channel)

                elif '2' in self.Channels[0]:
                    Intensity_2 = pklf['intensity_2']
                    Intensity_2 = Intensity_2

                    self.processor_2 = ImageROIProcessor()
                    self.processor_2.image = Intensity_2.astype(np.uint16)

                    roi_2_path = os.path.join(self.ROI_directory, an_file + '_roi_ch_2.dat')
                    
                    if os.path.exists(roi_2_path):
                        pass
                    else:
                        roi_2_path = os.path.join(self.ROI_directory, an_file + '_roi0_ch_2.dat')

                    
                    self.roi_2 = self.load_ROI(roi_2_path).to_numpy()
                    self.processor_2.roi_image = self.roi_2
                    channel = 'both'
                    # channel = 2
                    self.processor_1 = ImageROIProcessor()
                    self.processor_1.image = np.clip((self.NO_IMAGE_INTENSITY), 0, 1).astype(np.float64)
                    self.Current_image_1 = self.NO_IMAGE_INTENSITY
                    self.Current_image_2 = Intensity_2 / np.max(Intensity_2)
                    self.image_2_times_roi = self.Current_image_2
                    # self.display_images([self.Current_image_1,self.Current_image_2],channel)
                    self.display_images(channel)
                else:
                    pass

            elif len(self.Channels) == 2:

                Intensity_1 = pklf['intensity_1']
                Intensity_2 = pklf['intensity_2']

                self.processor_1 = ImageROIProcessor()
                self.processor_1.image = Intensity_1.astype(np.uint16)
                self.processor_2 = ImageROIProcessor()
                self.processor_2.image = Intensity_2.astype(np.uint16)
                roi_1_path = os.path.join(self.ROI_directory, an_file + '_roi_ch_1.dat')

                if os.path.exists(roi_1_path):
                    pass
                else:
                    roi_1_path = os.path.join(self.ROI_directory, an_file + '_roi0_ch_1.dat')
                
                self.roi_1 = self.load_ROI(roi_1_path).to_numpy()
                roi_2_path = os.path.join(self.ROI_directory, an_file + '_roi_ch_2.dat')

                if os.path.exists(roi_2_path):
                    pass
                else:
                    roi_2_path = os.path.join(self.ROI_directory, an_file + '_roi0_ch_2.dat')
                
                self.roi_2 = self.load_ROI(roi_2_path).to_numpy()
                self.processor_1.roi_image = self.roi_1
                self.processor_2.roi_image = self.roi_2
                channel = 'both'
                self.Current_image_1 = Intensity_1 / np.max(Intensity_1)
                self.Current_image_2 = Intensity_2 / np.max(Intensity_2)
                self.image_1_times_roi = self.Current_image_1
                self.image_2_times_roi = self.Current_image_2
                # self.display_images([self.Current_image_1,self.Current_image_2],channel)
                self.display_images(channel)

        elif dpg.get_value('Auto_ROI_checkbox'):

            if len(self.Channels) == 1:
                dpg.configure_item('cp_roi_1', enabled=False)
                dpg.configure_item('cp_roi_2', enabled=False)
                dpg.set_value('cp_roi_1', False)
                dpg.set_value('cp_roi_2', False)
                if '1' in self.Channels[0]:
                    Intensity_1 = pklf['intensity_1']
                    self.processor_1 = ImageROIProcessor()
                    self.processor_1.image = Intensity_1.astype(np.uint16)
                    channel = 'both'
                    # channel = 1
                    self.Current_image_1 = Intensity_1 / np.max(Intensity_1)
                    self.image_1_times_roi = self.Current_image_1
                    self.processor_2 = ImageROIProcessor()
                    self.processor_2.image = np.clip((self.NO_IMAGE_INTENSITY), 0, 1).astype(np.float64)
                    self.Current_image_2 = self.NO_IMAGE_INTENSITY
                    # self.display_images([self.Current_image_1,self.Current_image_2],channel)
                    self.display_images(channel)

                elif '2' in self.Channels[0]:
                    Intensity_2 = pklf['intensity_2']
                    self.processor_2 = ImageROIProcessor()
                    self.processor_2.image = Intensity_2.astype(np.uint16)
                    channel = 'both'
                    # channel = 2
                    self.processor_1 = ImageROIProcessor()
                    self.processor_1.image = np.clip((self.NO_IMAGE_INTENSITY), 0, 1).astype(np.float64)
                    self.Current_image_1 = self.NO_IMAGE_INTENSITY
                    self.Current_image_2 = Intensity_2 / np.max(Intensity_2)
                    self.image_2_times_roi = self.Current_image_2
                    # self.display_images([self.Current_image_1,self.Current_image_2],channel)
                    self.display_images(channel)

                else:
                    pass

            elif len(self.Channels) == 2:
                dpg.configure_item('cp_roi_1', enabled=True)
                dpg.configure_item('cp_roi_2', enabled=True)
                Intensity_1 = pklf['intensity_1']
                Intensity_2 = pklf['intensity_2']
                self.processor_1 = ImageROIProcessor()
                self.processor_1.image = Intensity_1.astype(np.uint16)
                self.processor_2 = ImageROIProcessor()
                self.processor_2.image = Intensity_2.astype(np.uint16)
                channel = 'both'
                self.Current_image_1 = Intensity_1 / np.max(Intensity_1)
                self.Current_image_2 = Intensity_2 / np.max(Intensity_2)
                self.image_1_times_roi = self.Current_image_1
                self.image_2_times_roi = self.Current_image_2
                # self.display_images([self.Current_image_1,self.Current_image_2],channel)
                self.display_images(channel)

        else:

            if len(self.Channels) == 1:
                if '1' in self.Channels[0]:
                    Intensity_1 = pklf['intensity_1']
                    self.processor_1 = ImageROIProcessor()
                    self.processor_1.image = Intensity_1.astype(np.uint16)
                    self.roi_1 = np.zeros(self.Current_image_1.shape)
                    channel = 'both'
                    # channel = 1
                    self.Current_image_1 = Intensity_1 / np.max(Intensity_1)
                    self.image_1_times_roi = self.Current_image_1
                    self.processor_2 = ImageROIProcessor()
                    self.processor_2.image = np.clip((self.NO_IMAGE_INTENSITY), 0, 1).astype(np.float64)
                    self.Current_image_2 = self.NO_IMAGE_INTENSITY
                    # self.display_images([self.Current_image_1,self.Current_image_2],channel)
                    self.display_images(channel)

                elif '2' in self.Channels[0]:
                    Intensity_2 = pklf['intensity_2']
                    self.processor_2 = ImageROIProcessor()
                    self.processor_2.image = Intensity_2.astype(np.uint16)
                    self.roi_2 = np.zeros(self.Current_image_2.shape)
                    self.image_2_times_roi = self.Current_image_2
                    channel = 'both'
                    # channel = 2
                    self.processor_1 = ImageROIProcessor()
                    self.processor_1.image = np.clip((self.NO_IMAGE_INTENSITY), 0, 1).astype(np.float64)
                    self.Current_image_1 = self.NO_IMAGE_INTENSITY
                    self.Current_image_2 = Intensity_2 / np.max(Intensity_2)
                    # self.display_images([self.Current_image_1,self.Current_image_2],channel)
                    self.display_images(channel)

                else:
                    pass

            elif len(self.Channels) == 2:

                Intensity_1 = pklf['intensity_1']
                Intensity_2 = pklf['intensity_2']
                self.roi_1 = np.zeros(self.Current_image_1.shape)
                self.roi_2 = np.zeros(self.Current_image_2.shape)
                self.processor_1 = ImageROIProcessor()
                self.processor_1.image = Intensity_1.astype(np.uint16)
                self.processor_2 = ImageROIProcessor()
                self.processor_2.image = Intensity_2.astype(np.uint16)
                channel = 'both'
                self.Current_image_1 = Intensity_1 / np.max(Intensity_1)
                self.Current_image_2 = Intensity_2 / np.max(Intensity_2)
                self.image_1_times_roi = self.Current_image_1
                self.image_2_times_roi = self.Current_image_2
                # self.display_images([self.Current_image_1,self.Current_image_2],channel)
                self.display_images(channel)

    def overlayrgba(self, im, rgba_image, mask_image, full_mask, ovrl):
        overlay_alpha = ovrl
        alpha_normalized = np.clip(overlay_alpha / 100.0, 0., 1.).astype(np.float64)
        if alpha_normalized == 1:
            mask_image[full_mask > 0, 0] = 1
        else:
            mask_image[full_mask > 0, 0] = (
                    im[full_mask > 0] * (1 - alpha_normalized) + 1 * alpha_normalized
            ).astype(np.float64)

        mask_image[full_mask > 0, 1] = im[full_mask > 0].astype(np.float64)
        mask_image[full_mask > 0, 2] = im[full_mask > 0].astype(np.float64)
        mask_image[full_mask > 0, 3] = (alpha_normalized).astype(np.float64)

        for i in range(3):
            rgba_image[..., i] = (rgba_image[..., i] * (1 - alpha_normalized) + mask_image[..., i] * alpha_normalized)

        rgba_image[..., 3] = np.maximum(rgba_image[..., 3], mask_image[..., 3])

        rgba_image = np.clip(rgba_image, 0, 1)

        return rgba_image

    def rgba_to_dpgtex(self, rgba_image, gs_im_max, tex_name):

        w = dpg.get_item_width(tex_name)
        h = dpg.get_item_height(tex_name)
        rgba_image = cv2.resize(rgba_image, (w, h), interpolation=cv2.INTER_LINEAR)
        rgba_image = rgba_image.astype(np.float64) / gs_im_max
        new_texture_data = rgba_image.flatten().tolist()
        dpg.set_value(tex_name, new_texture_data)

    def onHover(self, sender, app_data, user_data):

        dpg.focus_item(user_data)

        pass

    def get_ui_state(self, channel):
        """Get UI state parameters for a specific channel"""
        ui_state = {
            'auto_roi': dpg.get_value('Auto_ROI_checkbox'),
            'file_roi': dpg.get_value('FILE_ROI_checkbox'),
            'cp': dpg.get_value(f'cp_roi_{channel}'),
            'multiple_cells_checkbox': dpg.get_value(f'multiple_cells_checkbox_{channel}'),
            'processor': getattr(self, f'processor_{channel}'),
            'tex_name': getattr(self, f'tex_{channel}_name'),
            'image_times_roi': f'image_{channel}_times_roi',
            'contrast': dpg.get_value(f'img_contrast_{channel}'),
            'brightness': dpg.get_value(f'img_Brightness_{channel}') / 255,
            'ovrl': dpg.get_value(f'img_roi_alpha_{channel}'),
            'cell_thres_ratio': dpg.get_value(f'cell_thres_ratio_{channel}'),
            'nucl_thres_ratio': dpg.get_value(f'nucl_thres_ratio_{channel}'),
            'find_roi_mode': dpg.get_value(f'ROI_mode_{channel}')
            }

        return ui_state

    def _process_file_roi(self,channel, disp, ui_state):
        if dpg.get_value('FILE_ROI_checkbox'):

            processor = getattr(self, f'processor_{channel}')
            img = processor.image
            roi = processor.roi_image

            full_mask = np.nan_to_num(roi*255, nan=0)

            setattr(self, f'image_{channel}_times_roi',  img*roi)
            
            setattr(processor, 'all_masks',  [full_mask])

            self._update_texture(channel, disp, ui_state)

        else:

            self.process_channel(channel, self.get_ui_state(channel))
        
    
    def process_channel(self, channel, ui_state):
        """Process image channel using centralized UI state"""
        processor = ui_state['processor']
        disp = np.clip(processor.image / np.max(processor.image), 0, 1).astype(np.float64)

        if ui_state['auto_roi']:
            if len(self.Channels) == 1:
                if channel == self.Channels[0]:
                    self._process_auto_roi(channel, disp, ui_state)
                else:
                    pass
            else:
                self._process_auto_roi(channel, disp, ui_state)
        elif ui_state['file_roi']:
            if len(self.Channels) == 1:
                if channel == self.Channels[0]:
                    self._process_file_roi(channel, disp, ui_state)
                else:
                    pass
            else:   
                self._process_file_roi(channel, disp, ui_state)
        else:
            self._process_no_roi(channel, disp, ui_state)

    def _update_textures_both_roi(self, sender, app_data):
        """Handle texture updates with proper state management"""
        # lprint(self.Channels)
        # Determine which channels to update
        if sender.endswith(('1', '2')):

            channel = sender[-1]

            self.process_channel(channel, self.get_ui_state(channel))
        else:
            
            for channel in self.Channels:
                self.process_channel(channel, self.get_ui_state(channel))


        self.callback_calculate(sender, None)


    def _image_buttons_controller(self, sender):

        channel = sender[-1]


        ui_state = self.get_ui_state(channel)

        processor = ui_state['processor']

        disp = np.clip(processor.image / np.max(processor.image), 0, 1).astype(np.float64)

        self._update_texture(channel, disp, ui_state)



    def copy_roi_from_channel(self, sender):

        copy_to_channel = sender[-1]
        copy_from_channel = '2' if copy_to_channel == '1' else '1'
        with dpg.mutex():
                    if dpg.get_value(sender):
                        dpg.set_value(f'cp_roi_{copy_from_channel}', False)



        if dpg.get_value(sender):

            copy_from_processor = getattr(self, f'processor_{copy_from_channel}')
            copy_to_processor = getattr(self, f'processor_{copy_to_channel}')

            setattr(copy_to_processor, 'all_cells_masks', copy_from_processor.all_masks.copy())
            setattr(copy_to_processor, 'all_masks', copy_from_processor.all_masks.copy())
            setattr(copy_to_processor, 'all_contours', copy_from_processor.all_contours.copy())

            disp = np.clip(copy_to_processor.image / np.max(copy_to_processor.image), 0, 1).astype(np.float64)

            dpg.configure_item(f'cell_thres_ratio_{copy_to_channel}', enabled=False)

            self._update_texture(copy_to_channel, disp, self.get_ui_state(copy_to_channel))


        else:

            dpg.configure_item(f'cell_thres_ratio_{copy_to_channel}', enabled=True)
            self.process_channel(copy_to_channel, self.get_ui_state(copy_to_channel))

        self.callback_calculate(sender, None)

    def _process_auto_roi(self, channel, disp, ui_state):
        """Handle auto ROI processing using UI state"""
        processor = ui_state['processor']

        froi = np.clip(processor.image, 0, 255).astype(np.uint8)

        self._get_cell_roi(channel, froi, ui_state)

        self._update_texture(channel, disp, ui_state)

    def _get_cell_roi(self, channel, froi, ui_state):
        """Get cell ROI using parameters from UI state"""

        processor = ui_state['processor']

        processor.detect_cell_roi(froi, ui_state['cell_thres_ratio'])

        if not ui_state['multiple_cells_checkbox']:
            processor.all_cells_contours = [processor.all_cells_contours[0]]
            processor.all_cells_masks = [processor.all_cells_masks[0]]


        processor.all_masks = processor.all_cells_masks
        processor.all_contours = processor.all_cells_contours



    def _roi_mode(self, sender, app_data, user_data):


        channel = sender[-1]

        ui_state = self.get_ui_state(channel)

        processor = ui_state['processor']

        option_choosen = dpg.get_value(f'ROI_mode_{channel}')

        drag_float_value = dpg.get_value(f'nucl_thres_ratio_{channel}')


        if option_choosen == 'Find dark':

            processor.detect_dark_spot_inside_roi(drag_float_value)

        elif option_choosen == 'Find bright':

            processor.detect_bright_spot_inside_roi(drag_float_value)

        else:
            self.process_channel(channel, ui_state)

        disp = np.clip(processor.image / np.max(processor.image), 0, 1).astype(np.float64)
        self._update_texture(channel, disp, ui_state)
        self.callback_calculate(sender, None)



    def _update_texture(self, channel, disp, ui_state):
        """Update texture using parameters from UI state"""
        processor = ui_state['processor']
        rgba_image = self.im_to_rgbim(disp)
        adjusted_rgb = np.clip(rgba_image[..., :3] * ui_state['contrast'] + ui_state['brightness'], 0, 1)
        rgba_image[..., :3] = adjusted_rgb

        # Use contours from processor
        if hasattr(processor, 'all_masks') and processor.all_masks is not None:

            for cell_mask in processor.all_masks:
                rgba_image = self.overlayrgba(disp, rgba_image, rgba_image.copy(), cell_mask, ui_state['ovrl'])

        self.rgba_to_dpgtex(rgba_image, np.max(disp), ui_state['tex_name'])


    def _process_no_roi(self, channel, disp, ui_state):
        """Handle no ROI case using UI state"""
        processor = ui_state['processor']
        rgba_image = self.im_to_rgbim(disp)
        adjusted_rgb = np.clip(rgba_image[..., :3] * ui_state['contrast'] + ui_state['brightness'], 0, 1)
        rgba_image[..., :3] = adjusted_rgb
        setattr(self, ui_state['image_times_roi'], processor.image)
        self.rgba_to_dpgtex(rgba_image, np.max(disp), ui_state['tex_name'])

    def on_image_click(self, sender, app_data, user_data):
        """Handle image clicks to select specific cell contours"""

        image_tag, contours = user_data
        mouse_pos = dpg.get_mouse_pos()
        image_pos = dpg.get_item_pos(image_tag)
        channel = '1' if image_tag.endswith('_1') else '2'
        ui_state = self.get_ui_state(channel)
        processor = self.get_ui_state(channel)['processor']

        # Calculate positions and scaling
        displayed_w, displayed_h = dpg.get_item_width(image_tag), dpg.get_item_height(image_tag)
        original_h, original_w = processor.image.shape[:2]
        indent = dpg.get_item_configuration(image_tag)['indent']
        image_pos = (image_pos[0] + indent, image_pos[1] - self.img_height_shift['shift'])

        # Convert mouse coordinates to image space
        scale = (original_w / displayed_w, original_h / displayed_h)
        x, y = (int((mouse_pos[i] - image_pos[i]) * scale[i]) for i in (0, 1))

        # Check contours
        if hasattr(processor, 'all_contours') and processor.all_contours:
            for i, contour in enumerate(processor.all_contours):
                if cv2.pointPolygonTest(contour, (x, y), False) >= 0:


                    processor.all_contours = [contour]
                    processor.all_masks = [processor.all_masks[i]]

                    processor.all_cells_contours = [contour]
                    processor.all_cells_masks = processor.all_masks

                    dpg.set_value('ROI_name_tag', f'ROI_{i}')
                    dpg.set_value(f'multiple_cells_checkbox_{channel}', False)
                    break

            # Update display
            disp = np.clip(processor.image / np.max(processor.image), 0, 1).astype(np.float64)
            self._update_texture(channel, disp, ui_state)
            self.callback_calculate(sender, None)


    def load_ROI(self, path):
        df = pd.read_csv(path, sep='\t', header=None, skiprows=3, encoding='latin1')
        df = df.replace('-', -1.)
        try:
            df = df.astype(float)
        except:
            for i in df.index:
                try:
                    df.at[i, 0] = float(df.at[i, 0])

                except:

                    ind = i
                    break
            df = df[df.index < ind]
            df = df.astype(int)

        dfs = df[0].to_frame().applymap(np.isreal)

        if len(dfs.mask(dfs).dropna()) != 0:
            ind = int(dfs.mask(dfs).dropna().head(1).index.values)

            df = df[df.index < ind]
            df = df.astype(float)
            df = df.mask(df != -1, 1)
            df = df.where(df != -1, np.nan)

        else:
            df = df.astype(float)
            df = df.mask(df != -1, 1)
            df = df.where(df != -1, np.nan)

        return df

    def mean_bright_input_ch_1(self):
        self.mean_brightness_ch_1 = self.FCS_results_ch_1.Brightness.mean()
        self.mean_brightness_err_ch_1 = self.FCS_results_ch_1.Brightness.std(ddof=1)
        dpg.configure_item('Brightness_input_ch_1', default_value=self.mean_brightness_ch_1)
        dpg.configure_item('Brightness_err_input_ch_1', default_value=self.mean_brightness_err_ch_1)

    def mean_bright_input_ch_2(self):

        self.mean_brightness_ch_2 = self.FCS_results_ch_2.Brightness.mean()
        self.mean_brightness_err_ch_2 = self.FCS_results_ch_2.Brightness.std(ddof=1)
        dpg.configure_item('Brightness_input_ch_2', default_value=self.mean_brightness_ch_2)
        dpg.configure_item('Brightness_err_input_ch_2', default_value=self.mean_brightness_err_ch_2)

    def show_error_no_files(self, error_text):
        try:
            with dpg.window(pos=(400, 150),
                            label='Error!',
                            tag='No_data_files',

                            no_move=True,
                            no_close=False,
                            no_title_bar=False,
                            no_resize=True,
                            show=True,
                            modal=True
                            ):
                dpg.add_text(error_text, tag='no_files_error_text')

                dpg.add_button(label='Close',
                               tag='no_files_error_butt',
                               show=True,
                               callback=self.callback_no_files_dialog_close_only
                               )

                dpg.bind_item_theme('No_data_files', 'Error_window_theme')
        except:
            dpg.show_item('No_data_files')

    def update_dialogs_default_directory(self, last_directory):

        # dpg.configure_item('TT_file_dialog_id_ch_2',default_path=last_directory)
        # dpg.configure_item('TT_file_dialog_id_ch_1',default_path=last_directory)
        self._GI.last_directory = last_directory
        dpg.configure_item('ROI_folder_dialog_id', default_path=last_directory)
        dpg.configure_item('file_dialog_id', default_path=last_directory)
        dpg.configure_item('PTU_file_dialog_id', default_path=last_directory)
        dpg.configure_item('Select_ROI_dialog', default_path=last_directory)
        dpg.configure_item('file_dialog_export', default_path=last_directory)
        dpg.configure_item('Calib_file_dialog_id', default_path=last_directory)

    def update_flist(self, fs):
        '''Updates the filelist. '''

        if not len(fs) == 0:
            try:
                dpg.configure_item("file_box", items=fs)

                dpg.configure_item("file_box", default_value=fs[0])
            except:
                pass
        else:
            dpg.configure_item("file_box", items=())
            dpg.configure_item("file_box", default_value='')

            # def wdt_hgt_pos(self,item,wdth,hght,pos):

    def callback_exportsettings(self, sender, app_data):
        setts = {
            'Calib_data': {
                'Calib_file_path': self.calib_directory,
                'Ch_1_omega': dpg.get_value('omega_input_ch_1'),
                'Ch_1_omega_err': dpg.get_value('omega_err_input_ch_1'),
                'Ch_1_kappa': dpg.get_value('kappa_input_ch_1'),
                'Ch_1_kappa_err': dpg.get_value('kappa_err_input_ch_1'),
                'Ch_1_V0': dpg.get_value('focal_vol_input_ch_1'),
                'Ch_1_V0_err': dpg.get_value('focal_vol_err_input_ch_1'),
                'Ch_1_B': dpg.get_value('Brightness_input_ch_1'),
                'Ch_1_B_err': dpg.get_value('Brightness_err_input_ch_1'),
                'Ch_2_omega': dpg.get_value('omega_input_ch_2'),
                'Ch_2_omega_err': dpg.get_value('omega_err_input_ch_2'),
                'Ch_2_kappa': dpg.get_value('kappa_input_ch_2'),
                'Ch_2_kappa_err': dpg.get_value('kappa_err_input_ch_2'),
                'Ch_2_V0': dpg.get_value('focal_vol_input_ch_2'),
                'Ch_2_V0_err': dpg.get_value('focal_vol_err_input_ch_2'),
                'Ch_2_B': dpg.get_value('Brightness_input_ch_2'),
                'Ch_2_B_err': dpg.get_value('Brightness_err_input_ch_2'),

            },
            'PTU_files_dir': self.PTU_directory,
            'ROI_file_dir': self.ROI_directory,
            'Export_opts': {
                'Photons to array': dpg.get_value('Photons_array_checkbox'),
                'Photons to heatmap': dpg.get_value('Photons_Hmaps_checkbox'),
                'N_p to array': dpg.get_value('Np_array_checkbox'),
                'N_p to heatmap': dpg.get_value('Np_Hmaps_checkbox'),
                'Conc. to array': dpg.get_value('C_array_checkbox'),
                'Conc. to heatmap': dpg.get_value('C_Hmaps_checkbox')

            },
            'Error_notation': dpg.get_value('Error_type_checkbox')

        }

        # lnprint(setts)
        if self.PTU_directory != None:
            path_to_json_file = os.path.join(self.PTU_directory, 'workspace_info.json')
            with open(path_to_json_file, 'w') as f:
                json.dump(setts, f, indent=4, sort_keys=False)
        else:
            pass

    def _pkl_file(self):

        pkl = {
            'filename': self.anal_file,
            'ROI_mode': (dpg.get_value('FILE_ROI_checkbox'), dpg.get_value('Auto_ROI_checkbox')),
            'FCS_data': {
                'omega_1': dpg.get_value('omega_input_ch_1'),
                'omega_2': dpg.get_value('omega_input_ch_2'),
                'omega_err_1': dpg.get_value('omega_err_input_ch_1'),
                'omega_err_2': dpg.get_value('omega_err_input_ch_2'),
                'kappa_1': dpg.get_value('kappa_input_ch_1'),
                'kappa_2': dpg.get_value('kappa_input_ch_2'),
                'kappa_err_1': dpg.get_value('kappa_err_input_ch_1'),
                'kappa_err_2': dpg.get_value('kappa_err_input_ch_2'),
                'fv_1': dpg.get_value('focal_vol_input_ch_1'),
                'fv_2': dpg.get_value('focal_vol_input_ch_2'),
                'fv_err_1': dpg.get_value('focal_vol_err_input_ch_1'),
                'fv_err_2': dpg.get_value('focal_vol_err_input_ch_2'),
                'Br_1': dpg.get_value('Brightness_input_ch_1'),
                'Br_2': dpg.get_value('Brightness_input_ch_2'),
                'Br_err_1': dpg.get_value('Brightness_err_input_ch_1'),
                'Br_err_2': dpg.get_value('Brightness_err_input_ch_2'),
            },
            'autoroi_thres': {
                'cell_1': dpg.get_value('cell_thres_ratio_1'),
                'cell_2': dpg.get_value('cell_thres_ratio_2'),
                'nucl_1': dpg.get_value('nucl_thres_ratio_1'),
                'nucl_2': dpg.get_value('nucl_thres_ratio_2'),
                'ROI_mode_1': dpg.get_value('ROI_mode_1'),
                'ROI_mode_2': dpg.get_value('ROI_mode_2'),
                'cp_roi_1': dpg.get_value('cp_roi_1'),
                'cp_roi_2': dpg.get_value('cp_roi_2')

            }

        }
        # lnprint(pkl)
        pkl_path = os.path.join(self.PTU_directory, self.anal_file + '.rpk')
        with open(pkl_path, 'wb') as f:
            pickle.dump(pkl, f)

    def _load_pkl_file(self, path):
        with open(path, 'rb') as file:
            pkl = pickle.load(file)
        # lnprint(pkl)

        dpg.set_value('omega_input_ch_1', pkl['FCS_data']['omega_1'])
        dpg.set_value('omega_input_ch_2', pkl['FCS_data']['omega_2'])
        dpg.set_value('omega_err_input_ch_1', pkl['FCS_data']['omega_err_1'])
        dpg.set_value('omega_err_input_ch_2', pkl['FCS_data']['omega_err_2'])
        dpg.set_value('kappa_input_ch_1', pkl['FCS_data']['kappa_1'])
        dpg.set_value('kappa_input_ch_2', pkl['FCS_data']['kappa_2'])
        dpg.set_value('kappa_err_input_ch_1', pkl['FCS_data']['kappa_err_1'])
        dpg.set_value('kappa_err_input_ch_2', pkl['FCS_data']['kappa_err_2'])
        dpg.set_value('focal_vol_input_ch_1', pkl['FCS_data']['fv_1'])
        dpg.set_value('focal_vol_input_ch_2', pkl['FCS_data']['fv_2'])
        dpg.set_value('focal_vol_err_input_ch_1', pkl['FCS_data']['fv_err_1'])
        dpg.set_value('focal_vol_err_input_ch_2', pkl['FCS_data']['fv_err_2'])
        dpg.set_value('Brightness_input_ch_1', pkl['FCS_data']['Br_1'])
        dpg.set_value('Brightness_input_ch_2', pkl['FCS_data']['Br_2'])
        dpg.set_value('Brightness_err_input_ch_1', pkl['FCS_data']['Br_err_1'])
        dpg.set_value('Brightness_err_input_ch_2', pkl['FCS_data']['Br_err_2'])

        dpg.set_value('cell_thres_ratio_1', pkl['autoroi_thres']['cell_1'])
        dpg.set_value('cell_thres_ratio_2', pkl['autoroi_thres']['cell_2'])
        dpg.set_value('nucl_thres_ratio_1', pkl['autoroi_thres']['nucl_1'])
        dpg.set_value('nucl_thres_ratio_2', pkl['autoroi_thres']['nucl_2'])
        dpg.set_value('ROI_mode_1', pkl['autoroi_thres']['ROI_mode_1'])
        dpg.set_value('ROI_mode_2', pkl['autoroi_thres']['ROI_mode_2'])
        dpg.set_value('cp_roi_1', pkl['autoroi_thres']['cp_roi_1'])
        dpg.set_value('cp_roi_2', pkl['autoroi_thres']['cp_roi_2'])

        dpg.set_value('FILE_ROI_checkbox', pkl['ROI_mode'][0])
        dpg.set_value('Auto_ROI_checkbox', pkl['ROI_mode'][1])
        if pkl['ROI_mode'][1]:
            self.set_roi_state()
            self.callback_select_autoroi('Auto_ROI_checkbox', pkl['ROI_mode'][1])

        else:
            self.set_roi_state()
            # self.callback_select_autoroi('Auto_ROI_checkbox',pkl['ROI_mode'][1])
            self.callback_select_roi('FILE_ROI_checkbox', pkl['ROI_mode'][0])

        return pkl
