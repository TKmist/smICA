
'''1. Layout Init'''
init_top_indent = top_indent = 24+11
bg_channel_marker =None
init_internal_indent = 11
init_font_size = font_size = 18
init_group_spacer = group_spacer = 2
drag_line_thickness = 3
filtering_routine={'Channel 1':
                   {'BG':False
                   },
                   'Channel 2':
                   {'BG':False
                   }
                  }
ww=450

sindatax1 = [0,1]
sindatay1 = [0,1]
sindatax2 = [0,1]
sindatay2 = [0,1]
last_directory = ''
sindatax1 = []
sindatay1 = []
sindatax2 = []
sindatay2 = []
tau_mid = 0
files=[]
base_window_width = 482
init_widths = {
    'VIEWPORT':1400,
    'Files_window':360,
    'Options':360,
    'plot_window':base_window_width+18,
    'plot':base_window_width,
    'bottom_limit_ch1':base_window_width//3-(2*init_group_spacer)//3,
    'bottom_limit_ch2':base_window_width//3-(2*init_group_spacer)//3,
    'upper_limit_ch1':base_window_width//3-(2*init_group_spacer)//3,
    'upper_limit_ch2':base_window_width//3-(2*init_group_spacer)//3,
    'reset_button':base_window_width//3-(2*init_group_spacer)//3,
    'file_box':350,
    'apply_button':350,
    'Calculate_filters':350,
    'List_of_filters_ch1': base_window_width,
    'List_of_filters_ch2': base_window_width,
    'Add_decay_to_lib':174,
    'Add_decay_from_lib':174,
    'Decline_filters':174,
    'Accept_filters':174,
    'get_name':350,
    'get_decay_description':base_window_width,
    'Proceed_decay_submission':116,
    'Cancel_decay_submission':116,
    'Cancel_library_import':116,
    'Proceed_library_import':116,
    
    'Remove_bgd_butt_ch_1':base_window_width,
    'Remove_bgd_butt_ch_2':base_window_width,
    'BG_removal_window':1350,
    'MODE_window': (base_window_width+18)*3 + 360,
    
    'decays_tab_lib_list_tag':350+group_spacer*5+base_window_width
    
}



default_height =870

init_heights = {
     'VIEWPORT':950,
    'plot_window':default_height,
    'Files_window':default_height-120-init_internal_indent,
    'Options': 120,
    'BG_removal_window':800,
    'MODE_window': 50,
    'decays_tab_lib_list_tag':150,
    'List_of_filters_ch1': 120,
    'List_of_filters_ch2': 120,
}

init_position = {
    'MODE_window': (0,0),
    'plot_window_ch_1':(0,init_top_indent),
    'plot_window_ch_2':(init_widths['plot_window']+20,init_top_indent),
    'Files_window':(2*init_widths['plot_window']+2*20,init_top_indent+init_heights['Options']+init_internal_indent),
    'Options':(2*init_widths['plot_window']+2*20,init_top_indent)
}












    




    












































