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

from Modes.Phot2conc.Phot2conc_INIT import _Phot2conc_init, _Phot2conc_vars_funct
import numpy as np
import cv2
#import dearpygui as dpg


def Phot2conc_resizer(sender, app_data):
    init_resizable_items = []
    cmn_resizable_items = []
    obj_var = [eval('mode_init.' + str(m)) for m in vars(mode_init)]
    for m in obj_var:
        if type(m) == dict:
            if 'name' in m.keys():
                init_resizable_items.append(m['name'])
        else:
            pass
    obj_var = [eval('mode_cmn.' + str(m)) for m in vars(mode_cmn)]
    for m in obj_var:
        if type(m) == dict:
            if 'name' in m.keys():
                cmn_resizable_items.append(m['name'])
        else:
            pass

    ratio = {'width': np.round(app_data[0] / inV.VIEWPORT_prop['width'], 4),
             'height': np.round(app_data[1] / inV.VIEWPORT_prop['height'], 4)}

    inV.init_size_ratio = ratio

    forbiden_list = ['self',
                     'size_ratio',
                     'font_size',
                     'last_directory',
                     'dpg_image_1',
                     'dpg_image_2'
                     ]
    temp_inits = mode_init.__init__.__code__.co_varnames

    temp_inits = [v for v in temp_inits if v not in forbiden_list]

    temp_inits_values = {}
    for v in temp_inits:
        temp_inits_values[v] = eval('mode_init.' + v)

    current_image_1 = mode_init.processor_1.image
    current_image_2 = mode_init.processor_2.image

    mode_init.__init__(inV.init_size_ratio,
                       inV.init_left_indent,
                       inV.init_internal_indent,
                       inV.init_right_indent,
                       inV.init_bottom_indent,
                       inV.init_top_indent,
                       inV.init_group_spacer,
                       inV.init_font_size,
                       globalITEMS.last_directory,
                       globalITEMS.windows)

    mode_init.processor_1.image = current_image_1
    mode_init.processor_2.image = current_image_2

    mode_init.rgba_image_1 = mode_init.im_to_rgbim(mode_init.processor_1.image)
    mode_init.rgba_image_2 = mode_init.im_to_rgbim(mode_init.processor_2.image)

    mode_init.rgba_image_1 = cv2.resize(mode_init.rgba_image_1,
                                        (mode_init.image_window_ch1['width'] - mode_init.im_scaller,
                                         mode_init.image_window_ch1['width'] - mode_init.im_scaller),
                                        interpolation=cv2.INTER_LINEAR)
    mode_init.rgba_image_2 = cv2.resize(mode_init.rgba_image_2,
                                        (mode_init.image_window_ch2['width'] - mode_init.im_scaller,
                                         mode_init.image_window_ch2['width'] - mode_init.im_scaller),
                                        interpolation=cv2.INTER_LINEAR)
    dpg_image_1 = (mode_init.rgba_image_1.astype(np.float64) / np.max(mode_init.rgba_image_1)).flatten().tolist()
    dpg_image_2 = (mode_init.rgba_image_2.astype(np.float64) / np.max(mode_init.rgba_image_2)).flatten().tolist()

    if mode_init.tex_1_name in dpg.get_aliases():
        dpg.delete_item(mode_init.tex_1_name)

        dpg.remove_alias(mode_init.tex_1_name)
        dpg.delete_item('texture_CH_1')

    if mode_init.tex_2_name in dpg.get_aliases():
        dpg.delete_item(mode_init.tex_2_name)

        dpg.remove_alias(mode_init.tex_2_name)
        dpg.delete_item('texture_CH_2')

    dpg.add_dynamic_texture(width=mode_init.image_window_ch1['width'] - mode_init.im_scaller,
                            height=mode_init.image_window_ch1['width'] - mode_init.im_scaller,
                            default_value=dpg_image_1,
                            tag=mode_init.tex_1_name,
                            parent='texture_reg')

    dpg.add_image(mode_init.tex_1_name, parent='image_window_ch1'
                  , uv_min=(0, 0), uv_max=(1, 1), tag='texture_CH_1', indent=mode_init.shift)

    dpg.bind_item_handler_registry("texture_CH_1", "handler_image_1")

    dpg.add_dynamic_texture(width=mode_init.image_window_ch2['width'] - mode_init.im_scaller,
                            height=mode_init.image_window_ch2['width'] - mode_init.im_scaller,
                            default_value=dpg_image_2,
                            tag=mode_init.tex_2_name,
                            parent='texture_reg')

    dpg.add_image(mode_init.tex_2_name, parent='image_window_ch2'
                  , uv_min=(0, 0), uv_max=(1, 1), tag='texture_CH_2', indent=mode_init.shift)

    dpg.bind_item_handler_registry("texture_CH_2", "handler_image_2")

    mode_cmn.img_height_shift['shift'] = int(np.round(24 * mode_init.size_ratio['height']))

    for item in init_resizable_items:
        # lprint(item)
        props = eval('mode_init.' + item)

        if 'width' in props.keys():
            dpg.configure_item(item, width=props['width'])
        if 'height' in props.keys():
            dpg.configure_item(item, height=props['height'])
        if 'pos' in props.keys():
            dpg.configure_item(item, pos=props['pos'])


dpg.set_viewport_resize_callback(Phot2conc_resizer)

mode_init = _Phot2conc_init(inV.init_size_ratio,
                            inV.init_left_indent,
                            inV.init_internal_indent,
                            inV.init_right_indent,
                            inV.init_bottom_indent,
                            inV.init_top_indent,
                            inV.init_group_spacer,
                            inV.init_font_size,
                            globalITEMS.last_directory,
                            globalITEMS.windows
                            )

mode_cmn = _Phot2conc_vars_funct(mode_init,
                                 globalITEMS.last_directory,
                                 basf,
                      globalITEMS
                                 )
# method_cmn.mount_fcs_handlers()

# #########################################################################
# '''Main windows of the method'''
# #########################################################################
'''PTU window items'''
with dpg.window(label='',
                pos=mode_init.PTU_DATA_window['pos'],
                width=mode_init.PTU_DATA_window['width'],
                height=mode_init.PTU_DATA_window['height'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='PTU_DATA_window',
                show=True
                ):
    dpg.add_text(default_value='PTU metadata', show=True, tag='PTU_meta')
    dpg.add_separator(tag='PTU_DATA_mid_sep_1', show=True)
    with dpg.table(header_row=False, width=-1, borders_innerH=False,
                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                   no_pad_innerX=False, no_pad_outerX=True, no_host_extendX=True,
                   no_clip=True, tag='Resol_Pix_size_table', parent='PTU_DATA_window'):
        dpg.add_table_column(label="", tag='Resol_Pix_size_table_col1',
                             width=mode_init.Resol_Pix_size_table_col1['width'])
        dpg.add_table_column(label="", tag='Resol_Pix_size_table_col2',
                             width=mode_init.Resol_Pix_size_table_col2['width'])
        with dpg.table_row(tag='Resol_Pix_size_table_row1'):
            dpg.add_input_text(label='',
                               tag='Resolution_output',
                               width=mode_init.Resolution_output['width'],
                               default_value='Resolution: ',
                               readonly=True,
                               enabled=False,

                               )
            with dpg.tooltip('Resolution_output', tag='Resolution_output_tooltip'):
                dpg.add_text("The resolution of the PTU image.", tag='Resolution_output_tooltip_text')
            dpg.add_drag_int(label='',
                             tag='Pixel_size_output',
                             width=mode_init.Pixel_size_output['width'],
                             default_value=0,
                             format='Pixel size: %i [nm]',
                             enabled=False
                             )
            with dpg.tooltip('Pixel_size_output', tag='Pixel_size_output_tooltip'):
                dpg.add_text("Size of the of the pixell.", tag='Pixel_size_output_tooltip_text')

        with dpg.table_row(tag='Resol_Pix_size_table_row2'):
            dpg.add_drag_int(label='',
                             tag='Nframes_output',
                             width=mode_init.Nframes_output['width'],
                             default_value=0,
                             format='# of frames: %i',
                             enabled=False
                             )
            with dpg.tooltip('Nframes_output', tag='Nframes_output_tooltip'):
                dpg.add_text("Number of frames in the PTU file.", tag='Nframes_output_tooltip_text')

            dpg.add_drag_float(label='',
                               tag='Pixel_dwell_output',
                               width=mode_init.Pixel_dwell_output['width'],
                               default_value=0,
                               format='Pixel dwell: %.2f [\u00B5s]',
                               enabled=False
                               )
            with dpg.tooltip('Pixel_dwell_output', tag='Pixel_dwell_output_tooltip'):
                dpg.add_text("Value of the pixell dwell", tag='Pixel_dwell_output_tooltip_text')

    dpg.add_text(default_value='ROI', show=True, tag='PTU_roi')

    dpg.add_separator(tag='PTU_DATA_mid_sep_2', show=True)
    with dpg.table(header_row=False, width=-1, borders_innerH=False,
                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                   no_pad_innerX=False, no_pad_outerX=True, no_host_extendX=True,
                   no_clip=True, tag='ROI_table', parent='PTU_DATA_window'):
        dpg.add_table_column(label="", tag='ROI_table_col1', width=mode_init.ROI_table_col1['width'])
        dpg.add_table_column(label="", tag='ROI_table_col2', width=mode_init.ROI_table_col2['width'])
        dpg.add_table_column(label="",tag='ROI_table_col3', width = mode_init.ROI_table_col3['width'])
        with dpg.table_row(tag='ROI_table_row1'):
            dpg.add_checkbox(label='ROI from files', tag='FILE_ROI_checkbox', default_value=False,
                             callback=mode_cmn.callback_select_roi,
                             enabled=False)
            dpg.add_checkbox(label='Auto ROI', tag='Auto_ROI_checkbox', default_value=False,
                             callback=mode_cmn.callback_select_autoroi,
                             enabled=False)
            with dpg.group(tag='roi_name_group'):
                dpg.add_input_text(tag='ROI_name_tag',default_value='ROI_0',on_enter=True,multiline=False,width=-1)
                dpg.add_combo(tag='ROI_names_combo_tag',
                              items=mode_init.ROI_names_combo_tag['items'],
                              default_value=mode_init.ROI_names_combo_tag['items'][0],
                              width=mode_init.ROI_names_combo_tag['width'],
                              callback = mode_cmn.callback_ROI_names_combo,
                              show=False)
    with dpg.table(header_row=False,
                   width=-1,
                   borders_innerH=False,
                   borders_outerH=False,
                   borders_innerV=False,
                   borders_outerV=False,
                   no_pad_innerX=False,
                   no_pad_outerX=True,
                   no_host_extendX=True,
                   no_clip=True,
                   policy=dpg.mvTable_SizingFixedFit,
                   tag='auto_ROI_ch_table',
                   parent='PTU_DATA_window',
                   show=False):


        dpg.add_table_column(label="", tag='auto_ROI_ch_table_col1', width=mode_init.auto_ROI_ch_table_col1['width'],
                             width_fixed=True)
        dpg.add_table_column(label="", tag='auto_ROI_ch_table_col2', width=mode_init.auto_ROI_ch_table_col2['width'],
                             width_stretch=True)
        dpg.add_table_column(label="", tag='auto_ROI_ch_table_col3', width=mode_init.auto_ROI_ch_table_col3['width'],
                             width_stretch=True)
        with dpg.table_row(tag='auto_ROI_ch_table_row0'):
            dpg.add_text("", tag='auto_ROI_ch_table_row0_text_1')
            dpg.add_text("ROI channel 1", tag='auto_ROI_ch_table_row1_text_2')
            dpg.add_text("ROI channel 2", tag='auto_ROI_ch_table_row1_text_3')
            # dpg.add_checkbox(label='Multiple Cells', tag='multiple_cells_checkbox', default_value=False, callback=mode_cmn._update_textures_both_roi)
        with dpg.table_row(tag='auto_ROI_ch_table_row1'):
            
            dpg.add_text("Many cells:", tag='auto_ROI_ch_table_row1_text_1')
            dpg.add_checkbox(label='', tag='multiple_cells_checkbox', default_value=False, callback=mode_cmn._update_textures_both_roi)
            dpg.add_checkbox(label='', tag='multiple_cells_checkbox_ch2', default_value=False, callback=mode_cmn._update_textures_both_roi)
            # dpg.add_text("ROI channel 1", tag='auto_ROI_ch_table_row1_text_2')
            # dpg.add_text("ROI channel 2", tag='auto_ROI_ch_table_row1_text_3')
        with dpg.table_row(tag='auto_ROI_ch_table_row2'):
            dpg.add_text("Thres. Cell:", tag='auto_ROI_ch_table_row2_text_1')
            dpg.add_drag_float(tag='cell_thres_ratio_1',
                               default_value=1.0,
                               max_value=5.,
                               min_value=0.0,
                               speed=0.001,
                               enabled=False,
                               width=mode_init.cell_thres_ratio_1['width'],
                               format='%.3f',
                               callback=mode_cmn._update_textures_both_roi
                               )
            with dpg.tooltip('cell_thres_ratio_1', tag='cell_thres_ratio_1_tooltip'):
                dpg.add_text("Set threshold to detect cell.", tag='cell_thres_ratio_1_tooltip_text')

            dpg.add_drag_float(tag='cell_thres_ratio_2',
                               default_value=1.0,
                               max_value=5.,
                               min_value=0.0,
                               speed=0.001,
                               width=mode_init.cell_thres_ratio_2['width'],
                               enabled=False,
                               format='%.3f',
                               callback=mode_cmn._update_textures_both_roi
                               )
            with dpg.tooltip('cell_thres_ratio_2', tag='cell_thres_ratio_2_tooltip'):
                dpg.add_text("Set threshold to detect cell.", tag='cell_thres_ratio_2_tooltip_text')

        with dpg.table_row(tag='auto_ROI_ch_table_row5'):
            dpg.add_text("Copy cell ROI:", tag='auto_ROI_ch_table_row5_text_1')

            dpg.add_checkbox(label='Channel 2 \u2192 1',
                             tag='cp_roi_1',
                             default_value=False,
                             enabled=False,
                             # width=-1,
                             callback=mode_cmn.copy_roi_from_channel,
                             # parent='image_window_1'
                             )
            dpg.add_checkbox(label='Channel 1 \u2192 2',
                             tag='cp_roi_2',
                             default_value=False,
                             enabled=False,
                             # width=-1,
                             callback=mode_cmn.copy_roi_from_channel,
                             # parent='image_window_1'
                             )
        with dpg.table_row(tag='auto_ROI_ch_table_row4'):
            dpg.add_text("ROI mode:", tag='auto_ROI_ch_table_row4_text_1')
            dpg.add_combo(tag='ROI_mode_1',
                          width=mode_init.ROI_mode_1['width'],
                          items=mode_init.ROI_mode_1['items'],
                          default_value=mode_init.ROI_mode_1['items'][0],
                          callback=mode_cmn._update_textures_both_roi,
                          enabled=False,
                          )
            dpg.add_combo(tag='ROI_mode_2',
                          width=mode_init.ROI_mode_2['width'],
                          items=mode_init.ROI_mode_2['items'],
                          default_value=mode_init.ROI_mode_2['items'][0],
                          callback=mode_cmn._update_textures_both_roi,
                          enabled=False,
                          )
        with dpg.table_row(tag='auto_ROI_ch_table_row3'):
            dpg.add_text("Thres. Nucl.:", tag='auto_ROI_ch_table_row3_text_1')

            dpg.add_drag_float(tag='nucl_thres_ratio_1',
                               default_value=1.5,
                               max_value=5.,
                               min_value=0.0,
                               speed=0.001,
                               width=mode_init.nucl_thres_ratio_1['width'],
                               enabled=False,
                               format='%.3f',
                               callback=mode_cmn._update_textures_both_roi
                               )
            with dpg.tooltip('nucl_thres_ratio_1', tag='nucl_thres_ratio_1_tooltip'):
                dpg.add_text("Set threshold to subtract nucleus.", tag='nucl_thres_ratio_1_tooltip_text')

            dpg.add_drag_float(tag='nucl_thres_ratio_2',
                               default_value=1.5,
                               max_value=5.,
                               min_value=0.0,
                               speed=0.001,
                               width=mode_init.nucl_thres_ratio_2['width'],
                               enabled=False,
                               format='%.3f',
                               callback=mode_cmn._update_textures_both_roi
                               #callback=mode_cnm._nucleus_thres_ratio
                               )
            with dpg.tooltip('nucl_thres_ratio_2', tag='nucl_thres_ratio_2_tooltip'):
                dpg.add_text("Set threshold to subtract nucleus.", tag='nucl_thres_ratio_2_tooltip_text')
        

globalITEMS.windows.extend(['PTU_DATA_window',
                            'PTU_meta',
                            'PTU_DATA_mid_sep_1',
                            'Resol_Pix_size_table',
                            'Resol_Pix_size_table_col1',
                            'Resol_Pix_size_table_col2',
                            'Resol_Pix_size_table_row1',
                            'Resolution_output',
                            'Resolution_output_tooltip',
                            'Resolution_output_tooltip_text'

                            'Pixel_size_output',
                            'Pixel_size_output_tooltip',
                            'Pixel_size_output_tooltip_text',
                            'Resol_Pix_size_table_row2',
                            'Nframes_output',
                            'Nframes_output_tooltip',
                            'Nframes_output_tooltip_text',
                            'Pixel_dwell_output',
                            'Pixel_dwell_output_tooltip',
                            'Pixel_dwell_output_tooltip_text',
                            'PTU_roi',
                            'roi_name_group'
                            'PTU_DATA_mid_sep_2',
                            'ROI_table',
                            'ROI_table_col1',
                            'ROI_table_col2',
                            'ROI_table_col3',
                            'ROI_table_row1',
                            'ROI_names_combo_tag'
                            'auto_ROI_ch_table',
                            'auto_ROI_ch_table_row0',
                            'auto_ROI_ch_table_row0_text_1',
                            'auto_ROI_ch_table_col1',
                            'auto_ROI_ch_table_col2',
                            'auto_ROI_ch_table_col3',
                            'auto_ROI_ch_table_row1',
                            'auto_ROI_ch_table_row1_text_1',
                            'auto_ROI_ch_table_row1_text_2',
                            'auto_ROI_ch_table_row1_text_3',
                            'auto_ROI_ch_table_row2',
                            'auto_ROI_ch_table_row2_text_1',
                            'cell_thres_ratio_1',
                            'cell_thres_ratio_1_tooltip',
                            'cell_thres_ratio_1_tooltip_text',
                            'cell_thres_ratio_2',
                            'cell_thres_ratio_2_tooltip',
                            'cell_thres_ratio_2_tooltip_text',
                            'auto_ROI_ch_table_row3',
                            'auto_ROI_ch_table_row3_text_1',
                            'nucl_thres_ratio_1',
                            'nucl_thres_ratio_1_tooltip',
                            'nucl_thres_ratio_1_tooltip_text',
                            'nucl_thres_ratio_2',
                            'nucl_thres_ratio_2_tooltip',
                            'nucl_thres_ratio_2_tooltip_text',
                            'auto_ROI_ch_table_row4',
                            'auto_ROI_ch_table_row4_text_1',
                            'ROI_mode_1',
                            'ROI_mode_2',
                            'auto_ROI_ch_table_row5',
                            'auto_ROI_ch_table_row5_text_1',
                            'cp_roi_1',
                            'cp_roi_2',
                            'FILE_ROI_checkbox',
                            'Auto_ROI_checkbox',
                            'ROI_name_tag',
                            'multiple_cells_checkbox',
                            'multiple_cells_checkbox_ch2'

                            ])
# lprint(globalITEMS.windows)

'''Files window items'''
with dpg.window(label='',
                pos=mode_init.file_window['pos'],
                width=mode_init.file_window['width'],
                height=mode_init.file_window['height'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='file_window',
                show=True
                ):
    list_box = dpg.add_listbox(items=mode_init.file_box['items'],
                               width=mode_init.file_box['width'],
                               num_items=mode_init.file_box['num_items'],
                               tag='file_box',
                               callback=mode_cmn.callback_listbox
                               )
    dpg.add_separator(tag='sep_left_6', show=True)

    dpg.add_text(default_value='CALCULATE', show=True, tag='single_calc')

    dpg.add_separator(tag='FILES_mid_sep_1', show=True)

    dpg.add_button(label="Calculate single",
                   callback=mode_cmn.callback_calculate,
                   width=mode_init.Calculate_button['width'],
                   tag='Calculate_button',
                   show=True, enabled=True
                   )
    dpg.bind_item_theme('Calculate_button', 'fit_button_theme')
    with dpg.tooltip('Calculate_button', tag='Calculate_button_tooltip'):
        dpg.add_text("Press to make calculation on single file.", tag='Calculate_button_tooltip_text')

    dpg.add_button(label="Add to results",
                   callback=mode_cmn.add_single_result_to_DF,
                   width=mode_init.add_to_res_single_button['width'],
                   tag='add_to_res_single_button',
                   show=True, enabled=True
                   )
    dpg.bind_item_theme('add_to_res_single_button', 'fit_button_theme')
    with dpg.tooltip('add_to_res_single_button', tag='add_to_res_single_button_tooltip'):
        dpg.add_text("Press to add current calculation to dataframe.", tag='add_to_res_single_button_tooltip_text')

    dpg.add_text(default_value='CALCULATE ALL', show=True, tag='All_calc')

    dpg.add_separator(tag='FILES_mid_sep_2', show=True)

    dpg.add_button(label="Calculate all",
                   callback=mode_cmn.callback_calculate_all,
                   width=mode_init.Calculate_all_button['width'],
                   tag='Calculate_all_button',
                   show=True, enabled=True
                   )
    dpg.bind_item_theme('Calculate_all_button', 'fit_button_theme')
    with dpg.tooltip('Calculate_all_button', tag='Calculate_all_button_tooltip'):
        dpg.add_text("Press to make calculation on all files.", tag='Calculate_all_button_tooltip_text')

    dpg.add_text(default_value='EXPORT', show=True, tag='export_text')

    dpg.add_separator(tag='FILES_mid_sep_3', show=True)

    dpg.add_text(default_value='Export Images as arrays', show=True, tag='exp_data_to_img_csv')

    with dpg.table(header_row=False,
                   width=-1,
                   borders_innerH=False,
                   borders_outerH=False,
                   borders_innerV=False,
                   borders_outerV=False,
                   no_pad_innerX=False,
                   no_pad_outerX=True,
                   no_host_extendX=True,
                   no_clip=True,
                   tag='EXPORT_ops_table', parent='file_window'):
        dpg.add_table_column(label="", tag='EXPORT_ops_table_col1', width=mode_init.EXPORT_ops_table_col1['width'])
        dpg.add_table_column(label="", tag='EXPORT_ops_table_col2', width=mode_init.EXPORT_ops_table_col2['width'])
        with dpg.table_row(tag='EXPORT_ops_table_row1'):
            dpg.add_checkbox(label='Photons to array.', tag='Photons_array_checkbox', default_value=True)
            dpg.add_checkbox(label='Photons to heatmap.', tag='Photons_Hmaps_checkbox', default_value=False)
        with dpg.table_row(tag='EXPORT_ops_table_row2'):
            dpg.add_checkbox(label='N_p to array.', tag='Np_array_checkbox', default_value=True)
            dpg.add_checkbox(label='N_p to heatmap.', tag='Np_Hmaps_checkbox', default_value=False)
        with dpg.table_row(tag='EXPORT_ops_table_row3'):
            dpg.add_checkbox(label='Conc. to array.', tag='C_array_checkbox', default_value=True)
            dpg.add_checkbox(label='Conc. to heatmap.', tag='C_Hmaps_checkbox', default_value=False)

    dpg.add_button(label="Export all data",
                   callback=lambda: dpg.show_item('file_dialog_export'),
                   width=mode_init.Export_all_button['width'],
                   tag='Export_all_button',
                   show=True, enabled=True
                   )
    dpg.bind_item_theme('Export_all_button', 'fit_button_theme')
    with dpg.tooltip('Export_all_button', tag='Export_all_button_tooltip'):
        dpg.add_text("Press to make calculation on all files.", tag='Export_all_button_tooltip_text')

globalITEMS.windows.extend(['file_window',
                            'file_box',
                            'sep_left_6',
                            'single_calc',
                            'FILES_mid_sep_1',
                            'Calculate_button',
                            'Calculate_button_tooltip',
                            'Calculate_button_tooltip_text',
                            'add_to_res_single_button',
                            'add_to_res_single_button_tooltip',
                            'add_to_res_single_button_tooltip_text',
                            'All_calc',
                            'FILES_mid_sep_2',
                            'Calculate_all_button',
                            'Calculate_all_button_tooltip',
                            'Calculate_all_button_tooltip_text',
                            'export_text',
                            'FILES_mid_sep_3',
                            'exp_data_to_img_csv',
                            'EXPORT_ops_table',
                            'EXPORT_ops_table_col1',
                            'EXPORT_ops_table_col2',
                            'EXPORT_ops_table_row1',
                            'Photons_array_checkbox',
                            'Photons_Hmaps_checkbox',
                            'EXPORT_ops_table_row2',
                            'Np_array_checkbox',
                            'Np_Hmaps_checkbox',
                            'EXPORT_ops_table_row3',
                            'C_array_checkbox',
                            'C_Hmaps_checkbox',
                            'Export_all_button',
                            'Export_all_button_tooltip',
                            'Export_all_button_tooltip_text'

                            ])

'''Image 1 window items'''



with dpg.window(label='Channel 1',
                tag='image_window_ch1',
                width=mode_init.image_window_ch1['width'],
                height=mode_init.image_window_ch1['height'],
                pos=mode_init.image_window_ch1['pos'],
                autosize=False,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_move=True,
                no_bring_to_front_on_focus=True,
                show=True
                ):
    pass

    dpg.add_separator(tag='IMAGE_CH1_top_sep', show=True)


    with dpg.table(header_row=False, width=-1, borders_innerH=False,
                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                   no_pad_innerX=False, no_pad_outerX=True, no_host_extendX=True,
                   no_clip=True, tag='img_win_1_table_2', parent='image_window_ch1'):
        dpg.add_table_column(label="", tag='img_win_1_table_2_col1', width=mode_init.img_win_1_table_2_col1['width'])
        dpg.add_table_column(label="", tag='img_win_1_table_2_col2', width=mode_init.img_win_1_table_2_col2['width'])
        dpg.add_table_column(label="", tag='img_win_1_table_2_col3', width=mode_init.img_win_1_table_2_col3['width'])
        with dpg.table_row(tag='img_win_1_table_2_row1'):
            dpg.add_drag_float(tag='img_contrast_1',
                               format='Contrast: %.1f',
                               default_value=1.0,
                               max_value=10.,
                               min_value=0.1,
                               speed=0.01,
                               enabled=True,
                               width=mode_init.img_contrast_1['width'],
                               callback=mode_cmn._update_textures_both_roi
                               )
            dpg.add_drag_float(tag='img_Brightness_1',
                               # label="Brightness",
                               format='Brightness: %.1f',
                               default_value=0.0,
                               max_value=100.,
                               min_value=-100,
                               speed=.1,
                               enabled=True,
                               width=mode_init.img_Brightness_1['width'],
                               callback=mode_cmn._update_textures_both_roi
                               )
            dpg.add_drag_int(tag='img_roi_alpha_1',
                             # label="Brightness",
                             format='ROI alpha: %.d\u0025',
                             default_value=50,
                             max_value=100,
                             min_value=1,
                             speed=1,
                             enabled=True,
                             width=mode_init.img_roi_alpha_1['width'],
                             callback=mode_cmn._update_textures_both_roi
                             )
    dpg.add_separator(tag='IMAGE_CH1_top_sep_2', show=True, parent='image_window_ch1', before='texture_CH_1')


    dpg.add_image(mode_init.tex_1_name,
                  uv_min=(0, 0),
                  uv_max=(1, 1),
                  tag='texture_CH_1', indent=mode_init.shift)

    dpg.add_item_hover_handler(tag='img1_hover_hand', callback=mode_cmn.onHover, user_data="texture_CH_1",
                               parent='handler_image_1')

    dpg.add_item_clicked_handler(tag='img1_click_hand', callback=mode_cmn.on_image_click,
                                 user_data=('texture_CH_1', None), parent='handler_image_1')

    dpg.bind_item_handler_registry("texture_CH_1", "handler_image_1")
    # shift=(dpg.get_item_width('image_window_ch1')-dpg.get_item_width(mode_init.tex_1_name))






# lprint(dpg.get_item_width('image_window_ch1'),dpg.get_item_width(mode_init.tex_1_name),shift)


globalITEMS.windows.extend(['image_window_ch1',
                            'IMAGE_CH1_top_sep',
                            'texture_CH_1',
                            'IMAGE_CH1_top_sep_2',
                            # 'img_win_1_table',
                            # 'img_win_1_table_col1',
                            # 'img_win_1_table_col2',
                            # 'img_win_1_table_col3',
                            # 'img_win_1_table_col4',
                            # 'img_win_1_table_row1',
                            # 'cell_thres_ratio_1',
                            # 'cell_thres_ratio_1_tooltip',
                            # 'cell_thres_ratio_1_tooltip_text',
                            # 'nucleus_search_1',
                            # 'cp_roi_1',
                            # 'nucl_thres_ratio_1',
                            # 'nucl_thres_ratio_1_tooltip',
                            # 'nucl_thres_ratio_1_tooltip_text',
                            'img_win_1_table_2',
                            'img_win_1_table_2_col1',
                            'img_win_1_table_2_col1',
                            'img_win_1_table_2_col1',
                            'img_win_1_table_2_row1',
                            'img_contrast_1',
                            'img_Brightness_1',
                            'img_roi_alpha_1',
                            'img1_hover_hand',
                            'img1_click_hand'

                            ])
'''Image 2 window items'''
with dpg.window(label='Channel 2',
                tag='image_window_ch2',
                width=mode_init.image_window_ch2['width'],
                height=mode_init.image_window_ch2['height'],
                pos=mode_init.image_window_ch2['pos'],
                autosize=False,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_move=True,
                no_bring_to_front_on_focus=True,
                show=True
                ):
    pass
    dpg.add_separator(tag='IMAGE_CH2_top_sep', show=True)

    with dpg.table(header_row=False, width=-1, borders_innerH=False,
                   borders_outerH=False, borders_innerV=False, borders_outerV=False,
                   no_pad_innerX=False, no_pad_outerX=True, no_host_extendX=True,
                   no_clip=True, tag='img_win_2_table_2_2', parent='image_window_ch2'):
        # Add headers
        dpg.add_table_column(label="", tag='img_win_2_table_2_col1', width=mode_init.img_win_2_table_2_col1['width'])
        dpg.add_table_column(label="", tag='img_win_2_table_2_col2', width=mode_init.img_win_2_table_2_col2['width'])
        dpg.add_table_column(label="", tag='img_win_2_table_2_col3', width=mode_init.img_win_2_table_2_col3['width'])
        with dpg.table_row(tag='img_win_2_table_2_row1'):
            dpg.add_drag_float(tag='img_contrast_2',
                               format='Contrast: %.1f',
                               default_value=1.0,
                               max_value=10.,
                               min_value=0.1,
                               speed=0.01,
                               enabled=True,

                               width=mode_init.img_contrast_2['width'],
                               callback=mode_cmn._update_textures_both_roi
                               )

            #     dpg.add_text('',tag='img_contrast_text_1')

            dpg.add_drag_float(tag='img_Brightness_2',
                               # label="Brightness",
                               format='Brightness: %.1f',
                               default_value=0.0,
                               max_value=100.,
                               min_value=-100,
                               speed=.1,
                               enabled=True,
                               width=mode_init.img_Brightness_2['width'],
                               callback=mode_cmn._update_textures_both_roi
                               )
            dpg.add_drag_int(tag='img_roi_alpha_2',
                             # label="Brightness",
                             format='ROI alpha: %.d\u0025',
                             default_value=50,
                             max_value=100.,
                             min_value=1,
                             speed=1,
                             enabled=True,
                             width=mode_init.img_roi_alpha_2['width'],
                             callback=mode_cmn._update_textures_both_roi
                             )
    dpg.add_separator(tag='IMAGE_CH2_top_sep_2', show=True, parent='image_window_ch2', before='texture_CH_2')
    dpg.add_image(mode_init.tex_2_name,
                  uv_min=(0, 0),
                  uv_max=(1, 1),
                  tag='texture_CH_2', indent=mode_init.shift
                  # before='img_win_2_table'
                  )

    dpg.add_item_hover_handler(tag='img2_hover_hand', callback=mode_cmn.onHover, user_data="texture_CH_2",
                               parent='handler_image_2')

    dpg.add_item_clicked_handler(tag='img2_click_hand', callback=mode_cmn.on_image_click, user_data=('texture_CH_2',None), parent='handler_image_2')
    dpg.bind_item_handler_registry("texture_CH_2", "handler_image_2")

globalITEMS.windows.extend(['image_window_ch2',
                            'IMAGE_CH2_top_sep',
                            'texture_CH_2',
                            'IMAGE_CH2_top_sep_2',
                            # 'img_win_2_table',
                            # 'img_win_2_table_col1',
                            # 'img_win_2_table_col2',
                            # 'img_win_2_table_col3',
                            # 'img_win_2_table_row1',
                            # 'cell_thres_ratio_2',
                            # 'cell_thres_ratio_2_tooltip',
                            # 'cell_thres_ratio_2_tooltip_text',
                            # 'nucleus_search_2',
                            # 'cp_roi_2',
                            # 'nucl_thres_ratio_2',
                            # 'nucl_thres_ratio_2_tooltip',
                            # 'nucl_thres_ratio_2_tooltip_text',
                            'img_win_2_table_2',
                            'img_win_2_table_2_col1',
                            'img_win_2_table_2_col1',
                            'img_win_2_table_2_col1',
                            'img_win_2_table_2_row1',
                            'img_contrast_2',
                            'img_Brightness_2',
                            'img_roi_alpha_2',
                            'img2_hover_hand',
                            'img2_click_hand'

                            ])
'''Histogram 1 window items'''
with dpg.window(label='Results channel 1',
                tag='hist_window_ch1',
                width=mode_init.hist_window_ch1['width'],
                height=mode_init.hist_window_ch1['height'],
                pos=mode_init.hist_window_ch1['pos'],
                autosize=False,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_bring_to_front_on_focus=True,
                no_move=True,
                show=True
                ):
    dpg.add_separator(tag='HIST_CH1_top_sep', show=True)
    with dpg.tab_bar(tag='tab_bar_h1'):
        with dpg.tab(label="Concentration/pixel", tag='tab_bar_conc_h1'):
            with dpg.plot(label="",
                          height=mode_init.hist_conc_plot_ch1['height'],
                          width=mode_init.hist_conc_plot_ch1['width'],
                          no_menus=True,
                          no_box_select=True, no_mouse_pos=True,
                          tag='hist_conc_plot_ch1',
                          show=False):
                dpg.add_plot_legend(outside=True, location=dpg.mvPlot_Location_South, tag='hist_conc_plot_legend_ch1')
                dpg.add_plot_axis(dpg.mvXAxis, label="Concentration per pixel [nM]", no_gridlines=True,
                                  tag="hist_xc_axis_ch1")
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_yc_axis_ch1")
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xc_axis_ch1',
                                    label='Cocnentration per pixel distribution', tag='c_dist_ser_ch_1')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xc_axis_ch1', label='Mean = ',
                                    tag='c_mean_ser_ch_1')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xc_axis_ch1', label='Median = ',
                                    tag='c_med_ser_ch_1')
        with dpg.tab(label="N_p/pixel", tag='tab_bar_Np_h1'):
            with dpg.plot(label="",
                          height=mode_init.hist_np_plot_ch1['height'],
                          width=mode_init.hist_np_plot_ch1['width'],
                          no_menus=True,
                          no_box_select=True, no_mouse_pos=True,
                          tag='hist_np_plot_ch1',
                          show=False):
                dpg.add_plot_legend(outside=True, location=dpg.mvPlot_Location_South, tag='hist_Np_plot_legend_ch1')
                dpg.add_plot_axis(dpg.mvXAxis, label="Number of molecules per pixel", no_gridlines=True,
                                  tag="hist_xnp_axis_ch1")
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_ynp_axis_ch1")
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xnp_axis_ch1',
                                    label='N_p per pixel distribution', tag='np_dist_ser_ch_1')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xnp_axis_ch1', label='Mean = ',
                                    tag='np_mean_ser_ch_1')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xnp_axis_ch1', label='Median = ',
                                    tag='np_med_ser_ch_1')
        with dpg.tab(label="Photons/pixel", tag='tab_bar_phot_h1'):
            with dpg.plot(label="",
                          height=mode_init.hist_phot_plot_ch1['height'],
                          width=mode_init.hist_phot_plot_ch1['width'],
                          no_menus=True,
                          no_box_select=True, no_mouse_pos=True,
                          tag='hist_phot_plot_ch1',
                          show=False):
                dpg.add_plot_legend(outside=True, location=dpg.mvPlot_Location_South, tag='hist_phot_plot_legend_ch1')
                dpg.add_plot_axis(dpg.mvXAxis, label="Photons per pixel", no_gridlines=True, tag="hist_xphot_axis_ch1")
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_yphot_axis_ch1")
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xphot_axis_ch1',
                                    label='Photons per pixel distribution', tag='phot_dist_ser_ch_1')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xphot_axis_ch1', label='Mean = ',
                                    tag='phot_mean_ser_ch_1')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xphot_axis_ch1', label='Median = ',
                                    tag='phot_med_ser_ch_1')

globalITEMS.windows.extend(['hist_window_ch1',
                            'HIST_CH1_top_sep',
                            'tab_bar_h1',
                            'tab_bar_conc_h1',
                            'hist_conc_plot_ch1',
                            'hist_conc_plot_legend_ch1',
                            'hist_xc_axis_ch1',
                            'hist_yc_axis_ch1',
                            'c_dist_ser_ch_1',
                            'c_mean_ser_ch_1',
                            'c_med_ser_ch_1',
                            'tab_bar_Np_h1',
                            'hist_np_plot_ch1',
                            'hist_Np_plot_legend_ch1',
                            'hist_xnp_axis_ch1',
                            'hist_ynp_axis_ch1',
                            'np_dist_ser_ch_1',
                            'np_mean_ser_ch_1',
                            'np_med_ser_ch_1',
                            'tab_bar_phot_h1',
                            'hist_phot_plot_ch1',
                            'hist_phot_plot_legend_ch1',
                            'hist_xphot_axis_ch1',
                            'hist_yphot_axis_ch1',
                            'phot_dist_ser_ch_1',
                            'phot_mean_ser_ch_1',
                            'phot_med_ser_ch_1'
                            ])

'''Histogram 2 window items'''
with dpg.window(label='Results channel 2',
                tag='hist_window_ch2',
                width=mode_init.hist_window_ch2['width'],
                height=mode_init.hist_window_ch2['height'],
                pos=mode_init.hist_window_ch2['pos'],
                autosize=False,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_bring_to_front_on_focus=True,
                no_move=True,
                show=True
                ):
    dpg.add_separator(tag='HIST_CH2_top_sep', show=True)
    with dpg.tab_bar(tag='tab_bar_h2'):
        with dpg.tab(label="Concentration/pixel", tag='tab_bar_conc_h2'):
            with dpg.plot(label="",
                          height=mode_init.hist_conc_plot_ch2['height'],
                          width=mode_init.hist_conc_plot_ch2['width'],
                          no_menus=True,
                          no_box_select=True, no_mouse_pos=True,
                          tag='hist_conc_plot_ch2',
                          show=False):
                dpg.add_plot_legend(outside=True, location=dpg.mvPlot_Location_South, tag='hist_conc_plot_legend_ch2')
                dpg.add_plot_axis(dpg.mvXAxis, label="Concentration per pixel [nM]", no_gridlines=True,
                                  tag="hist_xc_axis_ch2")
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_yc_axis_ch2")
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xc_axis_ch2',
                                    label='Cocnentration per pixel distribution', tag='c_dist_ser_ch_2')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xc_axis_ch2', label='Mean = ',
                                    tag='c_mean_ser_ch_2')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xc_axis_ch2', label='Median = ',
                                    tag='c_med_ser_ch_2')
        with dpg.tab(label="N_p/pixel", tag='tab_bar_Np_h2'):
            with dpg.plot(label="",
                          height=mode_init.hist_np_plot_ch2['height'],
                          width=mode_init.hist_np_plot_ch2['width'],
                          no_menus=True,
                          no_box_select=True, no_mouse_pos=True,
                          tag='hist_np_plot_ch2',
                          show=False):
                dpg.add_plot_legend(outside=True, location=dpg.mvPlot_Location_South, tag='hist_Np_plot_legend_ch2')
                dpg.add_plot_axis(dpg.mvXAxis, label="Number of molecules per pixel", no_gridlines=True,
                                  tag="hist_xnp_axis_ch2")
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_ynp_axis_ch2")
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xnp_axis_ch2',
                                    label='N_p per pixel distribution', tag='np_dist_ser_ch_2')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xnp_axis_ch2', label='Mean = ',
                                    tag='np_mean_ser_ch_2')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xnp_axis_ch2', label='Median = ',
                                    tag='np_med_ser_ch_2')
        with dpg.tab(label="Photons/pixel", tag='tab_bar_phot_h2'):
            with dpg.plot(label="",
                          height=mode_init.hist_phot_plot_ch2['height'],
                          width=mode_init.hist_phot_plot_ch2['width'],
                          no_menus=True,
                          no_box_select=True, no_mouse_pos=True,
                          tag='hist_phot_plot_ch2',
                          show=False):
                dpg.add_plot_legend(outside=True, location=dpg.mvPlot_Location_South, tag='hist_phot_plot_legend_ch2')
                dpg.add_plot_axis(dpg.mvXAxis, label="Photons per pixel", no_gridlines=True, tag="hist_xphot_axis_ch2")
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_yphot_axis_ch2")
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xphot_axis_ch2',
                                    label='Photons per pixel distribution', tag='phot_dist_ser_ch_2')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xphot_axis_ch2', label='Mean = ',
                                    tag='phot_mean_ser_ch_2')
                dpg.add_stem_series(np.empty(10), np.empty(10), parent='hist_xphot_axis_ch2', label='Median = ',
                                    tag='phot_med_ser_ch_2')
globalITEMS.windows.extend(['hist_window_ch2',
                            'HIST_CH2_top_sep',
                            'tab_bar_h2',
                            'tab_bar_conc_h2',
                            'hist_conc_plot_ch2',
                            'hist_conc_plot_legend_ch2',
                            'hist_xc_axis_ch2',
                            'hist_yc_axis_ch2',
                            'c_dist_ser_ch_2',
                            'c_mean_ser_ch_2',
                            'c_med_ser_ch_2',
                            'tab_bar_Np_h2',
                            'hist_np_plot_ch2',
                            'hist_Np_plot_legend_ch2',
                            'hist_xnp_axis_ch2',
                            'hist_ynp_axis_ch2',
                            'np_dist_ser_ch_2',
                            'np_mean_ser_ch_2',
                            'np_med_ser_ch_2',
                            'tab_bar_phot_h2',
                            'hist_phot_plot_ch2',
                            'hist_phot_plot_legend_ch2',
                            'hist_xphot_axis_ch2',
                            'hist_yphot_axis_ch2',
                            'phot_dist_ser_ch_2',
                            'phot_mean_ser_ch_2',
                            'phot_med_ser_ch_2'
                            ])

'''FCS window items'''
with dpg.window(label='',
                pos=mode_init.FCS_window['pos'],
                width=mode_init.FCS_window['width'],
                height=mode_init.FCS_window['height'],
                no_move=True,
                no_close=True,
                no_collapse=True,
                no_title_bar=True,
                no_resize=True,
                tag='FCS_window',
                show=True
                ):
    dpg.add_text(default_value='FCS CALLIBRATION DATA', show=True, tag='FCS_CALLIB')

    dpg.add_separator(tag='FCS_top_sep', show=True)

    dpg.add_button(label="Load callibration data",
                   callback=lambda: dpg.configure_item("Calib_file_dialog_id", show=True,
                                                       user_data='Load_calib_button'),
                   width=mode_init.Load_calib_button['width'],
                   tag='Load_calib_button',
                   show=True, enabled=True
                   )
    dpg.bind_item_theme('Load_calib_button', 'fit_button_theme')
    dpg.add_button(label="Save callibration data",
                   callback=lambda: dpg.configure_item("Calib_file_dialog_id", show=True,
                                                       user_data='Save_calib_button'),
                   width=mode_init.Save_calib_button['width'],
                   tag='Save_calib_button',
                   show=True, enabled=True
                   )
    dpg.bind_item_theme('Save_calib_button', 'fit_button_theme')
    dpg.add_separator(tag='FCS_mid_sep_1', show=True)

    dpg.add_text(default_value='Channel 1', show=True, tag='FCS_pm_ch_1')

    with dpg.table(header_row=False,
                   width=-1,
                   borders_innerH=False,
                   borders_outerH=False,
                   borders_innerV=False,
                   borders_outerV=False,
                   no_pad_innerX=False,
                   no_pad_outerX=True,
                   no_host_extendX=True,
                   no_clip=True,
                   policy=dpg.mvTable_SizingFixedFit,
                   tag='FCS_win_CH1_table',
                   parent='FCS_window'):
        # Add headers
        dpg.add_table_column(label="",
                             tag='FCS_win_CH1_table_col1',
                             width_stretch=True,
                             init_width_or_weight=mode_init.FCS_win_CH1_table_col1['width'],
                             # width = table_col[mode_init.FCS_win_CH1_table_col1['width']
                             )
        dpg.add_table_column(label="",
                             tag='FCS_win_CH1_table_col2',
                             width_stretch=True,
                             init_width_or_weight=mode_init.FCS_win_CH1_table_col2['width'],
                             # width = mode_init.FCS_win_CH1_table_col2['width']
                             )

        # Add rows and columns
        with dpg.table_row(tag='FCS_win_CH1_table_row1'):
            dpg.add_drag_float(label='',
                               tag='omega_input_ch_1',
                               width=mode_init.omega_input_ch_1['width'],
                               default_value=0.2,
                               format='\u03C9\u2080 = %.3f',
                               max_value=0.5,
                               min_value=0.1,
                               speed=0.001,
                               callback=mode_cmn.callback_omega_input
                               )
            with dpg.tooltip('omega_input_ch_1', tag='omega_input_ch_1_tooltip'):
                dpg.add_text("Value of the \u03C9\u2080 from the FCS callibration measurements.",
                             tag='omega_input_ch_1_tooltip_text')

            dpg.add_drag_float(label='',
                               tag='omega_err_input_ch_1',
                               width=mode_init.omega_err_input_ch_1['width'],
                               default_value=0.02,
                               format='\u00B1 %.3f [\u03BCm]',
                               max_value=0.5,
                               min_value=0.001,
                               speed=0.001,
                               callback=mode_cmn.callback_omega_err_input
                               )
            with dpg.tooltip('omega_err_input_ch_1', tag='omega_err_input_ch_1_tooltip'):
                dpg.add_text("Value of error for the \u03C9\u2080 from the FCS callibration measurements.",
                             tag='omega_err_input_ch_1_tooltip_text')

        with dpg.table_row(tag='FCS_win_CH1_table_row2'):
            dpg.add_drag_float(label='',
                               tag='kappa_input_ch_1',
                               width=mode_init.kappa_input_ch_1['width'],
                               default_value=5.0,
                               format='\u03BA = %.2f',
                               max_value=20.5,
                               min_value=2.5,
                               speed=0.01,
                               callback=mode_cmn.callback_kappa_input
                               )
            with dpg.tooltip('kappa_input_ch_1', tag='kappa_input_ch_1_tooltip'):
                dpg.add_text("Value of the \u03BA from the FCS callibration measurements.",
                             tag='kappa_input_ch_1_tooltip_text')

            dpg.add_drag_float(label='',
                               tag='kappa_err_input_ch_1',
                               width=mode_init.kappa_err_input_ch_1['width'],
                               default_value=0.5,
                               format='\u00B1 %.2f',
                               max_value=20.5,
                               min_value=0.01,
                               speed=0.01,
                               callback=mode_cmn.callback_kappa_err_input
                               )
            with dpg.tooltip('kappa_err_input_ch_1', tag='kappa_err_input_ch_1_tooltip'):
                dpg.add_text("Value of error for the \u03BA from the FCS callibration measurements.",
                             tag='kappa_err_input_ch_1_tooltip_text')
        with dpg.table_row(tag='FCS_win_CH1_table_row3'):
            dpg.add_drag_float(label='',
                               tag='focal_vol_input_ch_1',
                               width=mode_init.focal_vol_input_ch_1['width'],
                               default_value=
                               mode_cmn.VEFF(dpg.get_value('omega_input_ch_1'), dpg.get_value('kappa_input_ch_1'),
                                             dpg.get_value('omega_err_input_ch_1'),
                                             dpg.get_value('kappa_err_input_ch_1'))[0],
                               format='V\u2080 = %.3f',
                               max_value=2.5,
                               min_value=0.05,
                               speed=0.001,
                               enabled=False

                               )
            with dpg.tooltip('focal_vol_input_ch_1', tag='focal_vol_input_ch_1_tooltip'):
                dpg.add_text("Value of the V\u2080 calculated using \u03C9\u2080 and \u03BA. This field is read-only.",
                             tag='focal_vol_input_ch_1_tooltip_text')

            dpg.add_drag_float(label='',
                               tag='focal_vol_err_input_ch_1',
                               width=mode_init.focal_vol_err_input_ch_1['width'],
                               default_value=
                               mode_cmn.VEFF(dpg.get_value('omega_input_ch_1'), dpg.get_value('kappa_input_ch_1'),
                                             dpg.get_value('omega_err_input_ch_1'),
                                             dpg.get_value('kappa_err_input_ch_1'))[1],
                               format='\u00B1 %.3f [fL]',
                               max_value=2.5,
                               min_value=0.05,
                               speed=0.001,
                               enabled=False

                               )
            with dpg.tooltip('focal_vol_err_input_ch_1', tag='focal_vol_err_input_ch_1_tooltip'):
                dpg.add_text(
                    "Value of error for the V\u2080 calculated using \u03C9\u2080 and \u03BA. This field is read-only.",
                    tag='focal_vol_err_input_ch_1_tooltip_text')
        with dpg.table_row(tag='FCS_win_CH1_table_row4'):
            dpg.add_drag_int(label='',
                             tag='Brightness_input_ch_1',
                             width=mode_init.Brightness_input_ch_1['width'],
                             default_value=mode_init.Brightness_input_ch_1['default_value'],

                             format='<Mol. brightness> = %.d',
                             max_value=1e5,
                             callback=mode_cmn.callback_Brightness_input
                             )
            with dpg.tooltip('Brightness_input_ch_1', tag='Brightness_input_ch_1_tooltip'):
                dpg.add_text("Mean value of the molecular brightness. Optionally input your own known value.",
                             tag='Brightness_input_ch_1_tooltip_text')

            dpg.add_drag_int(label='',
                             tag='Brightness_err_input_ch_1',
                             width=mode_init.Brightness_err_input_ch_1['width'],
                             default_value=mode_init.Brightness_err_input_ch_1['default_value'],
                             format='\u00B1 %.d',
                             max_value=1e5,
                             callback=mode_cmn.callback_Brightness_err_input
                             )
            with dpg.tooltip('Brightness_err_input_ch_1', tag='Brightness_err_input_ch_1_tooltip'):
                dpg.add_text(
                    "Standard deviation value of the molecular brightness. Optionally input your own known value.",
                    tag='Brightness_err_input_ch_1_tooltip_text')
    dpg.add_separator(tag='FCS_mid_sep_2', show=True)

    dpg.add_text(default_value='Channel 2', show=True, tag='FCS_pm_ch_2')

    with dpg.table(header_row=False,
                   width=-1,
                   borders_innerH=False,
                   borders_outerH=False,
                   borders_innerV=False,
                   borders_outerV=False,
                   no_pad_innerX=False,
                   no_pad_outerX=True,
                   no_host_extendX=True,
                   no_clip=True,
                   policy=dpg.mvTable_SizingFixedFit,
                   tag='FCS_win_CH2_table',
                   parent='FCS_window'):
        # Add headers
        dpg.add_table_column(label="",
                             tag='FCS_win_CH2_table_col1',
                             width_stretch=True,
                             init_width_or_weight=mode_init.FCS_win_CH2_table_col1['width'],
                             # width = mode_init.FCS_win_table_col1['width']
                             )
        dpg.add_table_column(label="",
                             tag='FCS_win_CH2_table_col2',
                             width_stretch=True,
                             init_width_or_weight=mode_init.FCS_win_CH2_table_col2['width'],
                             # width = mode_init.FCS_win_table_col2['width']
                             )

        # Add rows and columns
        with dpg.table_row(tag='FCS_win_CH2_table_row1'):
            dpg.add_drag_float(label='',
                               tag='omega_input_ch_2',
                               width=mode_init.omega_input_ch_2['width'],
                               default_value=0.2,
                               format='\u03C9\u2080 = %.3f',
                               max_value=0.5,
                               min_value=0.1,
                               speed=0.001,
                               callback=mode_cmn.callback_omega_input
                               )
            with dpg.tooltip('omega_input_ch_2', tag='omega_input_ch_2_tooltip'):
                dpg.add_text("Value of the \u03C9\u2080 from the FCS callibration measurements.",
                             tag='omega_input_ch_2_tooltip_text')

            dpg.add_drag_float(label='',
                               tag='omega_err_input_ch_2',
                               width=mode_init.omega_err_input_ch_2['width'],
                               default_value=0.02,
                               format='\u00B1 %.3f [\u03BCm]',
                               max_value=0.5,
                               min_value=0.001,
                               speed=0.001,
                               callback=mode_cmn.callback_omega_err_input
                               )
            with dpg.tooltip('omega_err_input_ch_2', tag='omega_err_input_ch_2_tooltip'):
                dpg.add_text("Value of error for the \u03C9\u2080 from the FCS callibration measurements.",
                             tag='omega_err_input_ch_2_tooltip_text')

        with dpg.table_row(tag='FCS_win_CH2_table_row2'):
            dpg.add_drag_float(label='',
                               tag='kappa_input_ch_2',
                               width=mode_init.kappa_input_ch_2['width'],
                               default_value=5.0,
                               format='\u03BA = %.2f',
                               max_value=20.5,
                               min_value=2.5,
                               speed=0.01,
                               callback=mode_cmn.callback_kappa_input
                               )
            with dpg.tooltip('kappa_input_ch_2', tag='kappa_input_ch_2_tooltip'):
                dpg.add_text("Value of the \u03BA from the FCS callibration measurements.",
                             tag='kappa_input_ch_2_tooltip_text')

            dpg.add_drag_float(label='',
                               tag='kappa_err_input_ch_2',
                               width=mode_init.kappa_err_input_ch_2['width'],
                               default_value=0.5,
                               format='\u00B1 %.2f',
                               max_value=20.5,
                               min_value=0.01,
                               speed=0.01,
                               callback=mode_cmn.callback_kappa_err_input
                               )
            with dpg.tooltip('kappa_err_input_ch_2', tag='kappa_err_input_ch_2_tooltip'):
                dpg.add_text("Value of error for the \u03BA from the FCS callibration measurements.",
                             tag='kappa_err_input_ch_2_tooltip_text')
        with dpg.table_row(tag='FCS_win_CH2_table_row3'):
            dpg.add_drag_float(label='',
                               tag='focal_vol_input_ch_2',
                               width=mode_init.focal_vol_input_ch_2['width'],
                               default_value=
                               mode_cmn.VEFF(dpg.get_value('omega_input_ch_2'), dpg.get_value('kappa_input_ch_2'),
                                             dpg.get_value('omega_err_input_ch_2'),
                                             dpg.get_value('kappa_err_input_ch_2'))[0],
                               format='V\u2080 = %.3f',
                               max_value=2.5,
                               min_value=0.05,
                               speed=0.001,
                               enabled=False

                               )
            with dpg.tooltip('focal_vol_input_ch_2', tag='focal_vol_input_ch_2_tooltip'):
                dpg.add_text("Value of the V\u2080 calculated using \u03C9\u2080 and \u03BA. This field is read-only.",
                             tag='focal_vol_input_ch_2_tooltip_text')

            dpg.add_drag_float(label='',
                               tag='focal_vol_err_input_ch_2',
                               width=mode_init.focal_vol_err_input_ch_2['width'],
                               default_value=
                               mode_cmn.VEFF(dpg.get_value('omega_input_ch_2'), dpg.get_value('kappa_input_ch_2'),
                                             dpg.get_value('omega_err_input_ch_2'),
                                             dpg.get_value('kappa_err_input_ch_2'))[1],
                               format='\u00B1 %.3f [fL]',
                               max_value=2.5,
                               min_value=0.05,
                               speed=0.001,
                               enabled=False

                               )
            with dpg.tooltip('focal_vol_err_input_ch_2', tag='focal_vol_err_input_ch_2_tooltip'):
                dpg.add_text(
                    "Value of error for the V\u2080 calculated using \u03C9\u2080 and \u03BA. This field is read-only.",
                    tag='focal_vol_err_input_ch_2_tooltip_text')
        with dpg.table_row(tag='FCS_win_CH2_table_row4'):
            dpg.add_drag_int(label='',
                             tag='Brightness_input_ch_2',
                             width=mode_init.Brightness_input_ch_2['width'],
                             default_value=mode_init.Brightness_input_ch_2['default_value'],
                             format='<Mol. brightness> = %.d',
                             max_value=1e5,
                             callback=mode_cmn.callback_Brightness_input
                             )
            with dpg.tooltip('Brightness_input_ch_2', tag='Brightness_input_ch_2_tooltip'):
                dpg.add_text("Mean value of the molecular brightness. Optionally input your own known value.",
                             tag='Brightness_input_ch_2_tooltip_text')

            dpg.add_drag_int(label='',
                             tag='Brightness_err_input_ch_2',
                             width=mode_init.Brightness_err_input_ch_2['width'],
                             default_value=mode_init.Brightness_err_input_ch_2['default_value'],
                             format='\u00B1 %.d',
                             max_value=1e5,
                             callback=mode_cmn.callback_Brightness_err_input
                             )
            with dpg.tooltip('Brightness_err_input_ch_2', tag='Brightness_err_input_ch_2_tooltip'):
                dpg.add_text(
                    "Standard deviation value of the molecular brightness. Optionally input your own known value.",
                    tag='Brightness_err_input_ch_2_tooltip_text')

globalITEMS.windows.extend(['FCS_window',
                            'FCS_CALLIB',
                            'FCS_top_sep',
                            'Load_calib_button',
                            'Save_calib_button',
                            'FCS_mid_sep_1',
                            'FCS_win_CH1_table',
                            'FCS_win_CH1_table_col1',
                            'FCS_win_CH1_table_col2',
                            'FCS_win_CH1_table_row1',
                            'omega_input_ch_1',
                            'omega_input_ch_1_tooltip',
                            'omega_input_ch_1_tooltip_text'
                            'omega_err_input_ch_1',
                            'omega_err_input_ch_1_tooltip',
                            'omega_err_input_ch_1_tooltip_text',
                            'FCS_win_CH1_table_row2',
                            'kappa_input_ch_1',
                            'kappa_input_ch_1_tooltip',
                            'kappa_input_ch_1_tooltip_text',
                            'kappa_err_input_ch_1',
                            'kappa_err_input_ch_1_tooltip',
                            'kappa_err_input_ch_1_tooltip_text',
                            'FCS_win_CH1_table_row3',
                            'focal_vol_input_ch_1',
                            'focal_vol_input_ch_1_tooltip',
                            'focal_vol_input_ch_1_tooltip_text',
                            'focal_vol_err_input_ch_1',
                            'focal_vol_err_input_ch_1_tooltip',
                            'focal_vol_err_input_ch_1_tooltip_text',
                            'FCS_win_CH1_table_row4',
                            'Brightness_input_ch_1',
                            'Brightness_input_ch_1_tooltip',
                            'Brightness_err_input_ch_1_tooltip_text',
                            'FCS_mid_sep_2',
                            'FCS_pm_ch_2',
                            'FCS_win_CH2_table',
                            'FCS_win_CH2_table_col1',
                            'FCS_win_CH2_table_col2',
                            'FCS_win_CH2_table_row1',
                            'omega_input_ch_2',
                            'omega_input_ch_2_tooltip',
                            'omega_input_ch_2_tooltip_text'
                            'omega_err_input_ch_2',
                            'omega_err_input_ch_2_tooltip',
                            'omega_err_input_ch_2_tooltip_text',
                            'FCS_win_CH2_table_row2',
                            'kappa_input_ch_2',
                            'kappa_input_ch_2_tooltip',
                            'kappa_input_ch_2_tooltip_text',
                            'kappa_err_input_ch_2',
                            'kappa_err_input_ch_2_tooltip',
                            'kappa_err_input_ch_2_tooltip_text',
                            'FCS_win_CH2_table_row3',
                            'focal_vol_input_ch_2',
                            'focal_vol_input_ch_2_tooltip',
                            'focal_vol_input_ch_2_tooltip_text',
                            'focal_vol_err_input_ch_2',
                            'focal_vol_err_input_ch_2_tooltip',
                            'focal_vol_err_input_ch_2_tooltip_text',
                            'FCS_win_CH2_table_row4',
                            'Brightness_input_ch_2',
                            'Brightness_input_ch_2_tooltip',
                            'Brightness_err_input_ch_2_tooltip_text',

                            ]
                           )

'''Results window items'''
with dpg.window(label='',
                pos=mode_init.results_window['pos'],
                width=mode_init.results_window['width'],
                height=mode_init.results_window['height'],
                no_move=True,
                no_close=True,
                no_title_bar=True,
                no_resize=True,
                tag='results_window',
                show=True
                ):
    dpg.add_text(default_value='RESULTS', show=True, tag='RES_pm')

    dpg.add_separator(tag='RESULTS_top_sep', show=True)

    dpg.add_text(default_value='Channel 1', show=True, tag='RES_pm_ch_1')

    with dpg.table(header_row=False,
                   width=-1,
                   borders_innerH=False,
                   borders_outerH=False,
                   borders_innerV=False,
                   borders_outerV=False,
                   no_pad_innerX=False,
                   no_pad_outerX=True,
                   no_host_extendX=True,
                   no_clip=True,
                   policy=dpg.mvTable_SizingFixedFit,
                   tag='RES_win_CH1_table',
                   parent='results_window'):
        # Add headers
        dpg.add_table_column(label="",
                             tag='RES_win_CH1_table_col1',
                             width_stretch=True,
                             init_width_or_weight=mode_init.RES_win_CH1_table_col1['width'],
                             # width = mode_init.FCS_win_table_col1['width']
                             )
        dpg.add_table_column(label="",
                             tag='RES_win_CH1_table_col2',
                             width_stretch=True,
                             init_width_or_weight=mode_init.RES_win_CH1_table_col1['width'],
                             # width = mode_init.RES_win_table_col2['width']
                             )

        # Add rows and columns
        with dpg.table_row(tag='RES_win_CH1_table_row1'):
            dpg.add_drag_float(label='',
                               tag='sinle_phot_output_ch_1',
                               width=mode_init.sinle_phot_output_ch_1['width'],
                               default_value=0,
                               format='Photons per pixel = %.1f',
                               enabled=False
                               )
            with dpg.tooltip('sinle_phot_output_ch_1', tag='sinle_phot_output_ch_1_tooltip'):
                dpg.add_text("Mean number of photons per pixel.", tag='sinle_phot_output_ch_1_tooltip_text')
            dpg.add_drag_float(label='',
                               tag='sinle_phot_err_output_ch_1',
                               width=mode_init.sinle_phot_err_output_ch_1['width'],
                               default_value=0,
                               format='\u00B1 %.3f',
                               enabled=False
                               )
            with dpg.tooltip('sinle_phot_err_output_ch_1', tag='sinle_phot_err_output_ch_1_tooltip'):
                dpg.add_text("SD of number of photons per pixel.", tag='sinle_phot_err_output_ch_1_tooltip_text')

        with dpg.table_row(tag='RES_win_CH1_table_row2'):
            dpg.add_drag_float(label='',
                               tag='sinle_mols_output_ch_1',
                               width=mode_init.sinle_mols_output_ch_1['width'],
                               default_value=0,
                               format='<N_p> per pixel = %.3f',
                               enabled=False
                               )
            with dpg.tooltip('sinle_mols_output_ch_1', tag='sinle_mols_output_ch_1_tooltip'):
                dpg.add_text("Mean number of molecules per pixel.", tag='sinle_mols_output_ch_1_tooltip_text')
            dpg.add_drag_float(label='',
                               tag='sinle_mols_err_output_ch_1',
                               width=mode_init.sinle_mols_err_output_ch_1['width'],
                               default_value=0,
                               format='\u00B1 %.3f',
                               enabled=False
                               )
            with dpg.tooltip('sinle_mols_err_output_ch_1', tag='sinle_mols_err_output_ch_1_tooltip'):
                dpg.add_text("SD of number of molecules per pixel.", tag='sinle_mols_err_output_ch_1_tooltip_text')

        with dpg.table_row(tag='RES_win_CH1_table_row3'):
            dpg.add_drag_float(label='',
                               tag='single_conc_output_ch_1',
                               width=mode_init.single_conc_output_ch_1['width'],
                               default_value=0,
                               format='<C> = %.3f',
                               enabled=False
                               )
            with dpg.tooltip('single_conc_output_ch_1', tag='single_conc_output_ch_1_tooltip'):
                dpg.add_text("Mean concentration. Average over entire image/ROI.",
                             tag='single_conc_output_ch_1_tooltip_text')
            dpg.add_drag_float(label='',
                               tag='single_conc_err_output_ch_1',
                               width=mode_init.single_conc_err_output_ch_1['width'],
                               default_value=0,
                               format='\u00B1 %.3f [nM]',
                               enabled=False
                               )
            with dpg.tooltip('single_conc_err_output_ch_1', tag='single_conc_err_output_ch_1_tooltip'):
                dpg.add_text("SD of concentration. Average over entire image/ROI.",
                             tag='single_conc_err_output_ch_1_tooltip_text')

    dpg.add_separator(tag='RESULTS_mid_sep_1', show=True)

    dpg.add_text(default_value='Channel 2', show=True, tag='Bright_pm_ch_2')

    with dpg.table(header_row=False,
                   width=-1,
                   borders_innerH=False,
                   borders_outerH=False,
                   borders_innerV=False,
                   borders_outerV=False,
                   no_pad_innerX=False,
                   no_pad_outerX=True,
                   no_host_extendX=True,
                   no_clip=True,
                   policy=dpg.mvTable_SizingFixedFit,
                   tag='RES_win_CH2_table',
                   parent='results_window'):
        # Add headers
        dpg.add_table_column(label="",
                             tag='RES_win_CH2_table_col1',
                             width_stretch=True,
                             init_width_or_weight=mode_init.RES_win_CH2_table_col1['width'],
                             # width = mode_init.FCS_win_table_col1['width']
                             )
        dpg.add_table_column(label="",
                             tag='RES_win_CH2_table_col2',
                             width_stretch=True,
                             init_width_or_weight=mode_init.RES_win_CH2_table_col2['width'],
                             # width = mode_init.RES_win_table_col2['width']
                             )

        # Add rows and columns
        with dpg.table_row(tag='RES_win_CH2_table_row1'):
            dpg.add_drag_float(label='',
                               tag='sinle_phot_output_ch_2',
                               width=mode_init.sinle_phot_output_ch_2['width'],
                               default_value=0,
                               format='Photons per pixel = %.1f',
                               enabled=False
                               )
            with dpg.tooltip('sinle_phot_output_ch_2', tag='sinle_phot_output_ch_2_tooltip'):
                dpg.add_text("Mean number of photons per pixel.", tag='sinle_phot_output_ch_2_tooltip_text')
            dpg.add_drag_float(label='',
                               tag='sinle_phot_err_output_ch_2',
                               width=mode_init.sinle_phot_err_output_ch_2['width'],
                               default_value=0,
                               format='\u00B1 %.3f',
                               enabled=False
                               )
            with dpg.tooltip('sinle_phot_err_output_ch_2', tag='sinle_phot_err_output_ch_2_tooltip'):
                dpg.add_text("SD of number of photons per pixel.", tag='sinle_phot_err_output_ch_2_tooltip_text')

        with dpg.table_row(tag='RES_win_CH2_table_row2'):
            dpg.add_drag_float(label='',
                               tag='sinle_mols_output_ch_2',
                               width=mode_init.sinle_mols_output_ch_2['width'],
                               default_value=0,
                               format='<N_p> per pixel = %.3f',
                               enabled=False
                               )
            with dpg.tooltip('sinle_mols_output_ch_2', tag='sinle_mols_output_ch_2_tooltip'):
                dpg.add_text("Mean number of molecules per pixel.", tag='sinle_mols_output_ch_2_tooltip_text')
            dpg.add_drag_float(label='',
                               tag='sinle_mols_err_output_ch_2',
                               width=mode_init.sinle_mols_err_output_ch_2['width'],
                               default_value=0,
                               format='\u00B1 %.3f',
                               enabled=False
                               )
            with dpg.tooltip('sinle_mols_err_output_ch_2', tag='sinle_mols_err_output_ch_2_tooltip'):
                dpg.add_text("SD of number of molecules per pixel.", tag='sinle_mols_err_output_ch_2_tooltip_text')

        with dpg.table_row(tag='RES_win_CH2_table_row3'):
            dpg.add_drag_float(label='',
                               tag='single_conc_output_ch_2',
                               width=mode_init.single_conc_output_ch_2['width'],
                               default_value=0,
                               format='<C> = %.3f',
                               enabled=False
                               )
            with dpg.tooltip('single_conc_output_ch_2', tag='single_conc_output_ch_2_tooltip'):
                dpg.add_text("Mean concentration. Average over entire image/ROI.",
                             tag='single_conc_output_ch_2_tooltip_text')
            dpg.add_drag_float(label='',
                               tag='single_conc_err_output_ch_2',
                               width=mode_init.single_conc_err_output_ch_2['width'],
                               default_value=0,
                               format='\u00B1 %.3f [nM]',
                               enabled=False
                               )
            with dpg.tooltip('single_conc_err_output_ch_2', tag='single_conc_err_output_ch_2_tooltip'):
                dpg.add_text("SD of concentration. Average over entire image/ROI.",
                             tag='single_conc_err_output_ch_2_tooltip_text')
    dpg.add_separator(tag='RESULTS_bott2_sep', show=True)
    dpg.add_checkbox(label='Errors as SD',
                     tag='Error_type_checkbox',
                     default_value=False,
                     callback=mode_cmn.callback_calculate
                     )

globalITEMS.windows.extend(['results_window',
                            'RES_pm',
                            'RESULTS_top_sep',
                            'RES_pm_ch_1',
                            'RES_win_CH1_table',
                            'RES_win_CH1_table_col1',
                            'RES_win_CH1_table_col2',
                            'RES_win_CH1_table_row1',
                            'sinle_phot_output_ch_1',
                            'sinle_phot_output_ch_1_tooltip',
                            'sinle_phot_output_ch_1_tooltip_text',
                            'sinle_phot_err_output_ch_1',
                            'sinle_phot_err_output_ch_1_tooltip',
                            'sinle_phot_err_output_ch_1_tooltip_text',
                            'sinle_mols_output_ch_1',
                            'sinle_mols_output_ch_1_tooltip',
                            'sinle_mols_output_ch_1_tooltip_text',
                            'sinle_mols_err_output_ch_1',
                            'sinle_mols_err_output_ch_1_tooltip',
                            'sinle_mols_err_output_ch_1_tooltip_text',
                            'single_conc_output_ch_1',
                            'single_conc_output_ch_1_tooltip',
                            'single_conc_output_ch_1_tooltip_text',
                            'single_conc_err_output_ch_1',
                            'single_conc_err_output_ch_1_tooltip',
                            'single_conc_err_output_ch_1_tooltip_text',

                            'RESULTS_mid_sep_1',
                            'Bright_pm_ch_2',

                            'RES_win_CH2_table',
                            'RES_win_CH2_table_col1',
                            'RES_win_CH2_table_col2',
                            'RES_win_CH2_table_row1',
                            'sinle_phot_output_ch_2',
                            'sinle_phot_output_ch_2_tooltip',
                            'sinle_phot_output_ch_2_tooltip_text',
                            'sinle_phot_err_output_ch_2',
                            'sinle_phot_err_output_ch_2_tooltip',
                            'sinle_phot_err_output_ch_2_tooltip_text',
                            'sinle_mols_output_ch_2',
                            'sinle_mols_output_ch_2_tooltip',
                            'sinle_mols_output_ch_2_tooltip_text',
                            'sinle_mols_err_output_ch_2',
                            'sinle_mols_err_output_ch_2_tooltip',
                            'sinle_mols_err_output_ch_2_tooltip_text',
                            'single_conc_output_ch_2',
                            'single_conc_output_ch_2_tooltip',
                            'single_conc_output_ch_2_tooltip_text',
                            'single_conc_err_output_ch_2',
                            'single_conc_err_output_ch_2_tooltip',
                            'single_conc_err_output_ch_2_tooltip_text',
                            'RESULTS_bott2_sep',
                            'Error_type_checkbox'

                            ]
                           )

'''Dialog window items'''

dpg.add_file_dialog(directory_selector=True,
                    label='Select ROI',
                    width=mode_init.ROI_folder_dialog_id['width'],
                    height=mode_init.ROI_folder_dialog_id['height'],
                    show=False,
                    file_count=5,
                    default_path=mode_cmn.last_directory,
                    callback=mode_cmn.callback_ROI_directory_select,
                    cancel_callback=mode_cmn.callback_empty,
                    tag="ROI_folder_dialog_id",
                    modal=False
                    )

dpg.add_file_dialog(directory_selector=True,
                    label='Select working directory',
                    width=mode_init.file_dialog_id['width'],
                    height=mode_init.file_dialog_id['height'],
                    show=False,
                    file_count=5,
                    default_path=mode_cmn.last_directory,
                    callback=mode_cmn.callback_directory_select,
                    cancel_callback=mode_cmn.callback_empty,
                    tag="file_dialog_id",
                    modal=False
                    )

dpg.add_file_dialog(directory_selector=True,
                    label='Select PTU folder to extract',
                    width=mode_init.PTU_file_dialog_id['width'],
                    height=mode_init.PTU_file_dialog_id['height'],
                    show=False,
                    file_count=5,
                    default_path=mode_cmn.last_directory,
                    callback=mode_cmn.callback_PTU_directory_select,
                    cancel_callback=mode_cmn.callback_empty,
                    tag="PTU_file_dialog_id",
                    modal=False
                    )

with dpg.file_dialog(directory_selector=False,
                     label='Select ROI',
                     default_filename='*.dat',
                     width=mode_init.Select_ROI_dialog['width'],
                     height=mode_init.Select_ROI_dialog['height'],
                     show=False,
                     file_count=10,
                     default_path=mode_cmn.last_directory,
                     callback=mode_cmn.import_ROI,
                     cancel_callback=mode_cmn.callback_empty,
                     tag="Select_ROI_dialog",
                     modal=False
                     ):
    dpg.add_file_extension("{.dat}")

with dpg.file_dialog(directory_selector=False,
                     show=False,
                     file_count=15,
                     default_path=mode_cmn.last_directory,
                     width=mode_init.file_dialog_export['width'],
                     height=mode_init.file_dialog_export['height'],
                     callback=mode_cmn.Export_result_dataframe_to_file,
                     cancel_callback=mode_cmn.callback_empty,
                     tag="file_dialog_export",
                     modal=False):
    '''Dialog window for exporting the results of the fitting.'''
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    dpg.add_file_extension("{.xlsx,.csv,.dat}")
    dpg.add_file_extension(".xlsx", color=(255, 0, 255, 255), custom_text="[Excel]")
    dpg.add_file_extension(".dat", color=(255, 255, 0, 255), custom_text="[DAT]")
    dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[CSV]")
    dpg.add_file_extension(".pickle", color=(0, 255, 255, 255), custom_text="[Pandas]")

with dpg.file_dialog(directory_selector=False,
                     label='Select callibration file',
                     default_filename='.',
                     width=mode_init.Calib_file_dialog_id['width'],
                     height=mode_init.Calib_file_dialog_id['height'],
                     show=False,
                     file_count=10,
                     default_path=mode_cmn.last_directory,
                     callback=mode_cmn.Load_Save_Calib_file,
                     cancel_callback=mode_cmn.callback_empty,
                     tag="Calib_file_dialog_id",
                     modal=False
                     ):
    dpg.add_file_extension(".json", color=(0, 255, 0, 255), custom_text="[JSON]")

globalITEMS.windows.extend(['ROI_folder_dialog_id',
                            'file_dialog_id',
                            'PTU_file_dialog_id',
                            'Select_ROI_dialog',
                            'file_dialog_export',
                            'Calib_file_dialog_id'])