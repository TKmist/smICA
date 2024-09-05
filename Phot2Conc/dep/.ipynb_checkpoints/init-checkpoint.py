
'''1. Layout Init'''

log_it('init - loaded on '+str(datetime.datetime.now()),'a')
init_top_indent = top_indent = 24+11
init_bottom_indent = bottom_indent = 11
init_left_indent = left_indent = 11
init_right_indent = right_indent = 11
init_internal_indent = internal_indent = 11
init_font_size = font_size = 18
init_group_spacer = group_spacer = 2
current_font_size = init_font_size
init_image_width1 = image_width1 = 1224
init_image_height1 = image_height1 = 200
init_var_def_group_1_spacer = var_def_group_1_spacer =20
global ratio_w,ratio_h

ratio_w =1
ratio_h = 1
hist_scaller =1.1

global dif_vp0_width
dif_vp0_width =  380

init_widths = {
    'VIEWPORT':1205+dif_vp0_width,
    'results_window':380,
    'file_window':380,
    'FCS_window':380,
    
    'PTU_DATA_window':380,
    'image_window':1110,
    'image_window_ch1':366,
    'image_window_ch2':366,
    'hist_window_ch1':366,
    'hist_window_ch2':366,
    
    
    'file_box':370,
    'directory_input_text':300,
    'Brightness_directory_input_text':300,
    'Browse_brightness_directory_button_ch_1':365,
    'Show_brightness_results_button_ch_1':365,
    'Browse_brightness_directory_button_ch_2':365,
    'Show_brightness_results_button_ch_2':365,
    
    'Load_calib_button':365,
    'Save_calib_button':365,
    'Brightness_input_ch_1':242,
    'Brightness_err_input_ch_1':121,
    'Brightness_input_ch_2':242,
    'Brightness_err_input_ch_2':121,
    'omega_input_ch_1':242,
    'omega_err_input_ch_1':121,
    'kappa_input_ch_1':242,
    'kappa_err_input_ch_1':121,
    'focal_vol_input_ch_1':242,
    'focal_vol_err_input_ch_1':121,
    'omega_input_ch_2':242,
    'omega_err_input_ch_2':121,
    'kappa_input_ch_2':242,
    'kappa_err_input_ch_2':121,
    'focal_vol_input_ch_2':242,
    'focal_vol_err_input_ch_2':121,
    'Add_ROI_1_button':181,
    'Add_ROI_2_button':181,
    'Browse_ROI_directory_button':365,
    'Nframes_output':181,
    'Pixel_dwell_output':181,
    'Resolution_output':181,
    'Pixel_size_output':181,
    'Calculate_button':365,
    'Calculate_all_button':365,
    
    'Export_all_button':365,
    
    'sinle_phot_output_ch_1':242,
    'sinle_phot_err_output_ch_1':121,
    'sinle_mols_output_ch_1':242,
    'sinle_mols_err_output_ch_1':121,
    
    'single_conc_output_ch_1':242,
    'single_conc_err_output_ch_1':121,
    'empty_output_ch_1':242,
    'empty_err_output_ch_1':121,
    'sinle_phot_output_ch_2':242,
    'sinle_phot_err_output_ch_2':121,
    'sinle_mols_output_ch_2':242,
    'sinle_mols_err_output_ch_2':121,
    'single_conc_output_ch_2':242,
    'single_conc_err_output_ch_2':121,
    'empty_output_ch_2':242,
    'empty_err_output_ch_2':121,
    
    'add_to_res_single_button':365,
    
    'show_TT_res_win_ch_1':1100,
    'show_TT_res_win_ch_2':1100,
    
    'Browse_directory_button':365,
    'file_dialog_id':913-10*init_left_indent,
    'Calib_file_dialog_id':913-10*init_left_indent,
    'file_dialog_export':913-10*init_left_indent,
    'TT_file_dialog_id_ch_1':913-10*init_left_indent,
    'TT_file_dialog_id_ch_2':913-10*init_left_indent,
    'ROI_folder_dialog_id':913-10*init_left_indent,
    
    'close_button_results_ch_1':100,
    'remove_button_results_ch_1':100,
    'close_button_results_ch_2':100,
    'remove_button_results_ch_2':100,
    
    'PTU_file_dialog_id':1513-10*init_left_indent}

curr_widths = init_widths.copy()

init_heights = {
    'VIEWPORT':950+init_bottom_indent + 11,
'results_window':360,
    'file_window':600,
    'FCS_window':390,
    'PTU_DATA_window':300,
    'image_window':935,
    'image_window_ch1':366,
    'image_window_ch2':366,
    'hist_window_ch1':366,
    'hist_window_ch2':366,
    'file_box':327,
    'show_res_win':200, 
    'file_dialog_id':935+init_bottom_indent + 11 - 20*init_bottom_indent,
    'Calib_file_dialog_id':935+init_bottom_indent + 11 - 20*init_bottom_indent,
    'file_dialog_export':935+init_bottom_indent + 11 - 20*init_bottom_indent,
    
    'TT_file_dialog_id_ch_1':935+init_bottom_indent + 11 - 20*init_bottom_indent,
    'TT_file_dialog_id_ch_2':935+init_bottom_indent + 11 - 20*init_bottom_indent,
    'PTU_file_dialog_id':935+init_bottom_indent + 11 - 20*init_bottom_indent,
    'ROI_folder_dialog_id':935+init_bottom_indent + 11 - 20*init_bottom_indent
}
curr_heights=init_heights.copy()
init_position = {
    'PTU_DATA_window':(init_left_indent,init_top_indent),
    'file_window':(init_left_indent,init_top_indent+init_heights['PTU_DATA_window']+init_internal_indent),
    'FCS_window':(init_left_indent+init_widths['PTU_DATA_window']+init_internal_indent+init_widths['image_window_ch1']+int(2.5*init_internal_indent)+init_widths['image_window_ch2']+int(2.5*init_internal_indent)
                  ,init_top_indent),
    
    
    
    'results_window':(init_left_indent+init_widths['PTU_DATA_window']+init_internal_indent+init_widths['image_window_ch1']+int(2.5*init_internal_indent)+init_widths['image_window_ch2']+int(2.5*init_internal_indent),init_top_indent+init_heights['FCS_window']+init_internal_indent),
    
    'show_TT_res_win_ch_1':(8,150),
    'show_TT_res_win_ch_2':(8,150),
    
    
    'image_window_ch1':(left_indent+init_widths['PTU_DATA_window']+init_internal_indent,
                  top_indent),
    'image_window_ch2':(left_indent+init_widths['PTU_DATA_window']+init_internal_indent+init_widths['image_window_ch1']+int(2.5*init_internal_indent),
                  top_indent),
    
    'hist_window_ch1':(left_indent+init_widths['PTU_DATA_window']+init_internal_indent,
                  top_indent+init_internal_indent+init_heights['image_window_ch1']+int(3.5*init_internal_indent)),
    'hist_window_ch2':(left_indent+init_widths['PTU_DATA_window']+init_internal_indent+init_widths['image_window_ch1']+int(2.5*init_internal_indent),
                  top_indent+init_internal_indent+init_heights['image_window_ch2']+int(3.5*init_internal_indent)),
    
    
    
    
    

    




    
                }
curr_position = init_position.copy()
cmap='gray'
cmap_LT='rainbow'


'''2. SYSTEM  VARIABLES'''

'''2.a list of allowed amthematical functions'''

math_expr =['arccos','arccosh','arcsin','arcsinh','arctan','arctan2',
            'arctanh','cos','cosh','exp','exp2','expm1','log','log10','log1p',
            'log2','mod','sign','sin','sinh','sqrt','square','tan','tanh',
            'pi','isfinite']

'''2.b Paths to the JSON files conating the predefined models and user defined models'''




global directory,files,last_directory,TT_directory,ROI_directory,DF,DF2
last_directory=''
files=()
ROI_directory = None
DF=DF2=[]


















