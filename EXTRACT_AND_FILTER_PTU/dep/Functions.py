'''Sorted functions'''



def _hsv_to_rgb(h,s,v):
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








def adjust_curves(imported_data,original_time_data):
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
    
    
    

@trace
def calculate_filters_from_routine(routine):
    global anal_file
    global fl_bg_curves_dict
    global tchanx1,tchany1,tchanx2,tchany2
    global Filters
    global bg_channel_marker
    global tau_resolution
    channel = None
    if bg_channel_marker == None:
        pass
    elif bg_channel_marker == 1:
        channel = 1
        rawx = tchanx1
        rawdatax_t = tchanx1*tau_resolution-(tchanx1*tau_resolution)[0]
        rawy = tchany1
        Btch_limit= fl_bg_curves_dict['Channel '+str(channel)][anal_file]['Btch_limit_ch_1']*tau_resolution-(tchanx1*tau_resolution)[0]
        Utch_limit= fl_bg_curves_dict['Channel '+str(channel)][anal_file]['Utch_limit_ch_1']*tau_resolution-(tchanx1*tau_resolution)[0]
        
        
        cname = 'Current decay; CH 1'
        
    elif bg_channel_marker == 2:
        channel = 2
        rawx = tchanx2
        rawdatax_t = tchanx2*tau_resolution-(tchanx2*tau_resolution)[0]
        rawy = tchany2
        Btch_limit= fl_bg_curves_dict['Channel '+str(channel)][anal_file]['Btch_limit_ch_2']*tau_resolution-(tchanx2*tau_resolution)[0]
        Utch_limit= fl_bg_curves_dict['Channel '+str(channel)][anal_file]['Utch_limit_ch_2']*tau_resolution-(tchanx2*tau_resolution)[0]
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

            adjusted = adjust_curves(df, pd.Series(rawdatax_t).to_frame())

            
            curve=adjusted.ydata.values


            CURVES[curv]=curve
            
        if if_afterpulse:

            afterpulse = 1/np.unique(rawx).size
            afterpulse = np.array([afterpulse for i in CURVES[curve_names[0]]])
            CURVES['Afterpulsing and background']=afterpulse
            
        else:
            pass
        
    
        
    elif if_BG and len(curve_names)==0:
        xs = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]
        ys = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]
        norma = np.sum(ys)
        CURVES[cname] = ys/norma
        
        if if_afterpulse:

            afterpulse = 1/np.unique(xs).size
            afterpulse = np.array([afterpulse for i in CURVES[cname]])
            CURVES['Afterpulsing and background']=afterpulse
        else:
            pass
    else:
        xs = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]
        ys = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]
        norma = np.sum(ys)

        CURVES[cname] = ys/norma
        
        
        for curv in curve_names:
            curve = np.load(routine['Channel '+str(channel)][curv])

            df = pd.DataFrame(curve.T,columns=['time','ydata'])
            df.ydata = df.ydata/df.ydata.sum()

            adjusted = adjust_curves(df, pd.Series(rawdatax_t).to_frame())

            
            curve=adjusted.ydata.values
            


            
            CURVES[curv]=curve
        if if_afterpulse:
            afterpulse = 1/np.unique(rawx).size
            afterpulse = np.array([afterpulse for i in CURVES[cname]])
            CURVES['Afterpulsing and background']=afterpulse
        else:
            pass

    



    
    Filters = calculate_stat_filter(CURVES,rawy)

    
    minlist=[]
    remove_existing_filter_plots()
    for F_name in Filters.keys():
        F = Filters[F_name]
        F = F/np.max(F)


        dpg.add_scatter_series(rawdatax_t, F, parent='yaxis_tltr_fltr',tag="tag_series_F_"+F_name,label=F_name)
        minlist.append(min(abs(F[np.where(F!=0)[0]]))/2)
    minimum = min(minlist)
    maximum =2
    dpg.set_axis_limits("xaxis_tltr_fltr", Btch_limit ,Utch_limit)
    dpg.set_axis_limits("yaxis_tltr_fltr", minimum ,maximum)
    dpg.show_item('fltr_filters_plot')
    dpg.show_item('fl_accpet_filters_group')
    
    dpg.show_item('Decline_filters')
    dpg.show_item('Accept_filters')
    
    
    
    
@trace    
def calculate_stat_filter(Pure_components_dict,raw_signal):

    pure_components = []
    for c in Pure_components_dict.keys():
        

        pure_components.append(Pure_components_dict[c])
    
    
    
    
    M = np.concatenate(pure_components).reshape((len(pure_components),len(pure_components[-1]))).T


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




def callback_Accept_filters():
    global Filters
    global filtering_routine
    global bg_channel_marker
    channel = None
    if bg_channel_marker == None:
        pass
    elif bg_channel_marker == 1:
        channel = 1
        
    elif bg_channel_marker == 2:
        channel = 2
    else:
        pass
    dpg.hide_item('fltr_filters_plot')
    dpg.hide_item('Decline_filters')
    dpg.hide_item('fl_accpet_filters_group')
    dpg.hide_item('Accept_filters')
    unmount_decay_table()
    unmount_LIB_decay_table()
    remove_imported_curves_from_plot()
    dpg.hide_item('BG_removal_window')
    
    
    dpg.set_value('use_as_statistical_filters_chkbx_ch_'+str(channel),True)
    dpg.show_item('filters_ch_'+str(channel)+'_tab_list_tag')
    
    log_it('Set of filters accepted','a')
    log_it('Filters:','a')
    mount_filter_list_table(channel)

    
    









                    
                    




                    




















def callback_Calculate_filters(sender,app_data):
    
    global bg_channel_marker
    global anal_file
    global fl_bg_curves_dict
    global tchanx1,tchany1,tchanx2,tchany2
    global filtering_routine
    global tau_resolution
    

    jsn_file = 'TCSPC_decay_library.json'
    jsn_path = os.path.join('res','Lib','json',jsn_file)
    with open(jsn_path) as json_library:
        jsn_dict = json.load(json_library)
    
    channel = None
    if bg_channel_marker == None:
        pass
    elif bg_channel_marker == 1:
        channel = 1
        rawx = tchanx1*tau_resolution-(tchanx1*tau_resolution)[0]
        rawy = tchany1
        xs = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]
        ys = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]
        Btch_limit= fl_bg_curves_dict['Channel '+str(channel)][anal_file]['Btch_limit_ch_1']*tau_resolution-(tchanx1*tau_resolution)[0]
        Utch_limit= fl_bg_curves_dict['Channel '+str(channel)][anal_file]['Utch_limit_ch_1']*tau_resolution-(tchanx1*tau_resolution)[0]
        
    elif bg_channel_marker == 2:
        channel = 2
        rawx = tchanx2*tau_resolution-(tchanx2*tau_resolution)[0]
        rawy = tchany2
        xs = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]
        ys = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]
        Btch_limit= fl_bg_curves_dict['Channel '+str(channel)][anal_file]['Btch_limit_ch_2']*tau_resolution-(tchanx2*tau_resolution)[0]
        Utch_limit= fl_bg_curves_dict['Channel '+str(channel)][anal_file]['Utch_limit_ch_2']*tau_resolution-(tchanx2*tau_resolution)[0]
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
        
        
        
        filtering_routine['Channel '+str(channel)][c_name]=cnpy
        
    
    
    
    calculate_filters_from_routine(filtering_routine)
    
    
        
        
        
        
        
        
    







    

    
    



    
    
    




















    





def callback_Cancel_library_import(sender,app_data):
    dpg.hide_item('Cancel_library_import')
    dpg.hide_item('decays_tab_lib_list_tag')
    dpg.hide_item('Proceed_library_import')
    dpg.hide_item('empty_library_notiffication')
    
    unmount_LIB_decay_table()

    
    tmp_series = dpg.get_aliases()
        
    tmp_series = [r for r in tmp_series if 'tag_series_fltr_temp_import' in r]
    
    for r in tmp_series:
        dpg.delete_item(r)
        
    to_import_list = dpg.get_aliases()
    to_import_list = [s for s in to_import_list if s.startswith('decays_lib_tab_row_')]
    to_import_list = [s for s in to_import_list if s.endswith('_cell e_chk')]
    for marked_decay in to_import_list:
        dpg.set_value(marked_decay,False)

        


def callback_Decline_filters():
    global Filters
    remove_existing_filter_plots()
    dpg.hide_item('fltr_filters_plot')
    dpg.hide_item('Decline_filters')
    dpg.hide_item('fl_accpet_filters_group')
    dpg.hide_item('Accept_filters')
    Filters = None
    


    





def callback_ERROR_dialog_close(sender,app_data):
    dpg.configure_item('ERROR',show=False)
    dpg.delete_item('ERROR_text')
    dpg.delete_item('ERROR_butt')
    dpg.delete_item('ERROR')


    
    
    


def callback_Proceed_library_import(sender,app_data):

    global curve_list

    global bg_channel_marker
    channel = None
    if bg_channel_marker == None:
            pass
    elif bg_channel_marker == 1:
        channel = 'Channel 1'


    elif bg_channel_marker == 2:
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

        if not name in curve_list:
            curve_list.append(name)
        else:
            pass
    unmount_decay_table()
    mount_decay_table(curve_list)
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

            callback_chkbox_decay_table_mark(d)
        else:
            pass
    callback_Cancel_library_import('Cancel_library_import',None)
    
    
            
        
    


def callback_Set_background_level(sender,app_data):
    global fl_bg_curves_dict
    global filtering_routine
    global bg_channel_marker
    global anal_file
    global tchanx1,tchany1,tchanx2,tchany2
    channel = None
    
    if bg_channel_marker == None:
        pass
    elif bg_channel_marker == 1:
        
        channel = 1
        xs = tchanx1
        ys = tchany1

        
    elif bg_channel_marker == 2:
        channel = 2
        xs = tchanx2
        ys = tchany2

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
        
        
        make_smooth(subtr,substracted_tchany)
        
        
        dpg.set_value('tag_series_fltr_subtr', [xs, substracted_tchany])
        dpg.configure_item("tag_series_fltr_subtr", label = 'Subtracted')
        minimum = min(abs(substracted_tchany[np.where(substracted_tchany!=0)[0]]))/2
        if bg_df_val<= minimum:
            bg_df_val = 1.1*minimum
        dpg.configure_item('Background_level_line',default_value=bg_df_val)
        dpg.set_axis_limits("yaxis_tltr", minimum ,max(substracted_tchany)*2)
        
        
        
        
        
        
        
        
        
        fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]=xs
        fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]=substracted_tchany*np.sum(ys)        
        
        
        
        
        dpg.configure_item('Add_decay_to_lib',enabled=True)
        dpg.set_value('decays_tab_row_'+str(0)+'_cell b_chk',True)
        
        filtering_routine['Channel '+str(channel)]['BG']=True

        
        
    else:
        dpg.hide_item('Background_level_line')
        dpg.configure_item('Background_level_line',default_value=0)
        dpg.set_value('tag_series_fltr_subtr', [[], []])
        dpg.configure_item("tag_series_fltr_subtr", label = '')
        fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]=[]
        fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]=[]
        ys=ys/np.sum(ys)
        minimum = min(abs(ys[np.where(ys!=0)[0]]))/2
        dpg.set_axis_limits("yaxis_tltr", minimum ,max(ys)*2)
        dpg.set_value('decays_tab_row_'+str(0)+'_cell b_chk',False)
        filtering_routine['Channel '+str(channel)]['BG']=False

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        dpg.configure_item('Add_decay_to_lib',enabled=False)
        
        
        


def callback_Set_background_range(sender,app_data):
    global fl_bg_curves_dict
    global anal_file
    global bg_channel_marker
    global tchanx1,tchany1,tchanx2,tchany2
    global tau_resolution
    channel = None
    if bg_channel_marker == None:
        pass
    elif bg_channel_marker == 1:
        channel = 1
        xs = tchanx1*tau_resolution-(tchanx1*tau_resolution)[0]
        ys = tchany1
        
        
    elif bg_channel_marker == 2:
        channel = 2
        xs = tchanx2*tau_resolution-(tchanx2*tau_resolution)[0]
        ys = tchany2
        
        
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
        subtr = make_smooth(xs,substracted_tchany)
    
        dpg.set_value('tag_series_fltr_subtr', [subtr['xs'].values, subtr.smth.values])
        
        
        dpg.configure_item("tag_series_fltr_subtr", label = 'Subtracted')
        minimum = min(abs(substracted_tchany[np.where(substracted_tchany!=0)[0]]))
        dpg.set_axis_limits("yaxis_tltr", minimum/2 ,max(substracted_tchany)*2)
        
        fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]=xs
        fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]=subtr.smth.values*np.sum(ys)        
        
        
        
        
        dpg.configure_item('Add_decay_to_lib',enabled=True)
        dpg.set_value('decays_tab_row_'+str(0)+'_cell b_chk',True)
        filtering_routine['Channel '+str(channel)]['BG']=True
        filtering_routine['Channel '+str(channel)]['BG_rng']=(bgrl_df_val,bgru_df_val)

        
    else:
        dpg.configure_item('Background_RLL_line',default_value=0)
        dpg.configure_item('Background_RUL_line',default_value=0)
        dpg.hide_item('Background_RLL_line')
        dpg.hide_item('Background_RUL_line')
        dpg.set_value('tag_series_fltr_subtr', [[], []])
        dpg.configure_item("tag_series_fltr_subtr", label = '')
        fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]=[]
        fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]=[]
        ys=ys/np.sum(ys)
        minimum = min(abs(ys[np.where(ys!=0)[0]]))/2
        dpg.set_axis_limits("yaxis_tltr", minimum ,max(ys)*2)
        dpg.set_value('decays_tab_row_'+str(0)+'_cell b_chk',False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        dpg.configure_item('Add_decay_to_lib',enabled=False)
        filtering_routine['Channel '+str(channel)]['BG']=False

        


def callback_add_decay_to_lib(sender,app_data):

    
    
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
    
    


@trace
def callback_apply_to_all_ptus():
    global files,last_directory
    global B_limit_ch_1,U_limit_ch_1,B_limit_ch_2,U_limit_ch_2


    
   
    







                            

                    













    mount_status_modal()
    for i,an_file in enumerate(files):
        perc = int(np.round(i/len(files)*100))
        
        
        
        
        
        dpg.configure_item('loading_butt',label=an_file)
        dpg.configure_item('loading_cnt_butt',label=str(perc)+'%')
        
        
        
        extract_from_ptu(last_directory,an_file,B_limit_ch_1,U_limit_ch_1,B_limit_ch_2,U_limit_ch_2)
        
        
        
    
    dpg.configure_item('loading_cnt_butt',label=str(100)+'%')    
    time.sleep(0.1)
    unmount_status_modal()






        
        


    
    




def callback_apply_to_files():
    
    dpg.configure_item('PTU_dir_dialog',show=True)
    
    pass


@trace
def callback_apply_to_single_ptus():
    global files,last_directory,anal_file
    global B_limit_ch_1,U_limit_ch_1,B_limit_ch_2,U_limit_ch_2
    global Filters
    global fl_bg_curves_dict
    global filtering_routine

    an_file = anal_file.split('/')[-1]

   
    mount_status_modal()







                            

                    

















    
    
    

    
    
    
    
        
    dpg.configure_item('loading_butt',label=an_file)    
    
        

    try:
        extract_from_ptu(last_directory,an_file,B_limit_ch_1,U_limit_ch_1,B_limit_ch_2,U_limit_ch_2)
    except:
        log_it('\n\tSomething wrong with your input file, try again.','a')
        log_it('\tIncorrect file: '+an_file+'\n','a')
        
        
    
    dpg.configure_item('loading_cnt_butt',label=str(100)+'%')    
    
    unmount_status_modal()





        



        
        


    
    




def callback_cancel_submission(sender,app_data):

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
    


def callback_check_lib_decay(sender,app_data):
    global anal_file,bg_channel_marker
    global fl_bg_curves_dict
    global tchanx1,tchany1,tchanx2,tchany2
    channel = None
    if bg_channel_marker == None:
            pass
    elif bg_channel_marker == 1:
        channel = 'Channel 1'
        rawx = tchanx1
        rawy = tchany1


    elif bg_channel_marker == 2:
        channel = 'Channel 2'
        rawx = tchanx2
        rawy = tchany2

    else:
        pass
    

    
    jsn_file = 'TCSPC_decay_library.json'
    jsn_path = os.path.join('res','Lib','json',jsn_file)
    with open(jsn_path) as json_library:
        jsn_dict = json.load(json_library)
    i = int(sender.split('_')[4])

    name = dpg.get_value('decays_lib_tab_row_'+str(i)+'_cell a_text')
    anal_file_tscpc_res = str(fl_bg_curves_dict[channel][anal_file]['TCSPC_resolution'])
    anal_file_tscpc_chan = str(fl_bg_curves_dict[channel][anal_file]['TCSPC_channels'])
                                                                        


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

            tmp_xs = decay_npy_data[0]*tau_resolution-(decay_npy_data[0]*tau_resolution)[0]
            tmp_ys = decay_npy_data[1]/np.sum(decay_npy_data[1])
            dpg.add_scatter_series(tmp_xs, tmp_ys,
                                    parent='yaxis_tltr',
                                tag="tag_series_fltr_temp_import"+str(i),
                                label='To be imported (#'+str(i+1)+')')
            
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
    
    

    



def callback_chkbox_decay_table_mark(sender):
    global fl_bg_curves_dict,anal_file
    global bg_channel_marker
    global filtering_routine

    global tau_resolution
    channel = None
    if bg_channel_marker == None:
            pass
    elif bg_channel_marker == 1:
        channel = 'Channel 1'
        tchanx1 = fl_bg_curves_dict[channel][anal_file]['tchanx1']
        rawdatax_t = tchanx1*tau_resolution-(tchanx1*tau_resolution)[0]
        rawdatay = fl_bg_curves_dict[channel][anal_file]['tchany1']
        subtry = fl_bg_curves_dict[channel][anal_file]['subtract_bg']['tchany1']


    elif bg_channel_marker == 2:
        channel = 'Channel 2'
        tchanx2 = fl_bg_curves_dict[channel][anal_file]['tchanx2']
        rawdatax_t = tchanx2*tau_resolution-(tchanx2*tau_resolution)[0]
        rawdatay = fl_bg_curves_dict[channel][anal_file]['tchany2']
        subtry = fl_bg_curves_dict[channel][anal_file]['subtract_bg']['tchany2']

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


            del filtering_routine[channel][decay_name]

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


            
            adjusted = adjust_curves(df, pd.Series(rawdatax_t).to_frame())
            
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

            dpg.set_axis_limits("yaxis_tltr", minimum ,maximum)




def callback_drag_Background_Range_line(sender,app_data):
    global bg_channel_marker
    global anal_file
    global fl_bg_curves_dict
    global tchanx1,tchany1,tchanx2,tchany2
    channel = None
    if bg_channel_marker == None:
        pass
    elif bg_channel_marker == 1:
        channel = 1
        xs = tchanx1*tau_resolution-(tchanx1*tau_resolution)[0]
        ys = tchany1
        
    elif bg_channel_marker == 2:
        channel = 2
        xs = tchanx2*tau_resolution-(tchanx2*tau_resolution)[0]
        ys = tchany2 
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
    
    subtr = make_smooth(xs,substracted_tchany)
    
    
    



    



    
    
    dpg.set_value('tag_series_fltr_subtr', [subtr['xs'].values, subtr.smth.values])
    dpg.configure_item("tag_series_fltr_subtr", label = 'Subtracted')
    
    
    
    fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]=subtr['xs'].values
    fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]=subtr.smth.values*np.sum(ys)
    
    minimum = min(subtr.smth.where(subtr.smth!=0).dropna())/2
    dpg.set_axis_limits("yaxis_tltr", minimum ,subtr.smth.max()*2)
    
    



    
    
    
    


def callback_drag_Background_level_line(sender,app_data):
    global bg_channel_marker
    global anal_file
    global fl_bg_curves_dict
    global tchanx1,tchany1,tchanx2,tchany2
    channel = None
    if bg_channel_marker == None:
        pass
    elif bg_channel_marker == 1:
        channel = 1
        xs = tchanx1*tau_resolution-(tchanx1*tau_resolution)[0]
        ys = tchany1
        
    elif bg_channel_marker == 2:
        channel = 2
        xs = tchanx2*tau_resolution-(tchanx2*tau_resolution)[0]
        ys = tchany2 
    else:
        pass
    
    noise_LVL = dpg.get_value(sender)
    
    substracted_tchany = (ys/np.sum(ys))-noise_LVL
    
    subtr = make_smooth(xs,substracted_tchany)
    
    dpg.set_value('tag_series_fltr_subtr', [subtr['xs'].values, subtr.smth.values])
    
    
    fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]=xs
    fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]=subtr.smth.values*np.sum(ys)

    


def callback_dragline(sender,app_data):
    global B_limit_ch_1,U_limit_ch_1,B_limit_ch_2,U_limit_ch_2
    global Btch_limit_ch_1,Utch_limit_ch_1,Btch_limit_ch_2,Utch_limit_ch_2
    global tau_resolution
    global tchanx1,tchany1,tchanx2,tchany2
    global Tchanx1,Tchany1,Tchanx2,Tchany2
    
    
    if str(sender).isdigit():
        
        sender = dpg.get_item_alias(sender)
    else:
        pass
    
    value = dpg.get_value(sender)
    
    if sender == 'L_dline_ch1':
        if value >= dpg.get_value('U_dline_ch1'):
            value = dpg.get_value('U_dline_ch1')
            dpg.set_value(sender,value)
        elif value < min(sindatax1):
            value = min(sindatax1)
            dpg.set_value(sender,value)
        else:
            pass
        
        dpg.set_axis_limits("xaxis_chan1_zoom", value, dpg.get_value('U_dline_ch1'))
        dpg.set_value('bottom_limit_ch1',value)
        dpg.set_value('upper_limit_ch1',dpg.get_value('U_dline_ch1'))
        B_limit_ch_1 = dpg.get_value('L_dline_ch1')
        Btch_limit_ch_1 = int(B_limit_ch_1/tau_resolution)
        Utch_limit_ch_1 = int(dpg.get_value('U_dline_ch1')/tau_resolution)
        tchanx1 = Tchanx1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]
        tchany1 = Tchany1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]

    elif sender == 'U_dline_ch1':
        if value <= dpg.get_value('L_dline_ch1'):
            value = dpg.get_value('L_dline_ch1')
            dpg.set_value(sender,value)
        elif value > max(sindatax1):
            value = max(sindatax1)
            dpg.set_value(sender,value)
        else:
            pass
        dpg.set_axis_limits("xaxis_chan1_zoom",dpg.get_value('L_dline_ch1') , value)
        dpg.set_value('bottom_limit_ch1',dpg.get_value('L_dline_ch1'))
        dpg.set_value('upper_limit_ch1',value)
        U_limit_ch_1 = dpg.get_value('U_dline_ch1')
        
        Btch_limit_ch_1 = int(dpg.get_value('L_dline_ch1')/tau_resolution)
        Utch_limit_ch_1 = int(U_limit_ch_1/tau_resolution)
        tchanx1 = Tchanx1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]
        tchany1 = Tchany1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]
    elif sender == 'L_dline_ch2':
        if value >= dpg.get_value('U_dline_ch2'):
            value = dpg.get_value('U_dline_ch2')
            dpg.set_value(sender,value)
        elif value < min(sindatax2):
            value = min(sindatax2)
            dpg.set_value(sender,value)
        else:
            pass
        dpg.set_axis_limits("xaxis_chan2_zoom", value, dpg.get_value('U_dline_ch2'))
        dpg.set_value('bottom_limit_ch2',value)
        dpg.set_value('upper_limit_ch2',dpg.get_value('U_dline_ch2'))
        B_limit_ch_2 = dpg.get_value('L_dline_ch2')
        
        Btch_limit_ch_2 = int(B_limit_ch_2/tau_resolution)
        Utch_limit_ch_2 = int(dpg.get_value('U_dline_ch2')/tau_resolution)
        tchanx2 = Tchanx2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
        tchany2 = Tchany2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
    elif sender == 'U_dline_ch2':
        if value <= dpg.get_value('L_dline_ch2'):
            value = dpg.get_value('L_dline_ch2')
            dpg.set_value(sender,value)
        elif value > max(sindatax2):
            value = max(sindatax2)
            dpg.set_value(sender,value)
        else:
            pass
        dpg.set_axis_limits("xaxis_chan2_zoom",dpg.get_value('L_dline_ch2') , value)
        dpg.set_value('bottom_limit_ch2',dpg.get_value('L_dline_ch2'))
        dpg.set_value('upper_limit_ch2',value)
        U_limit_ch_2 = dpg.get_value('U_dline_ch2')
        
        Btch_limit_ch_2 = int(dpg.get_value('L_dline_ch2')/tau_resolution)
        Utch_limit_ch_2 = int(U_limit_ch_2/tau_resolution)
        tchanx2 = Tchanx2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
        tchany2 = Tchany2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]

        
    




def callback_empty(sender,app_data):
    '''Empty function. Do nothing.'''
    pass






def callback_import_from_library(sender,app_data):
    global bg_channel_marker
    unmount_LIB_decay_table()
    dpg.show_item('fl_bg_win_group_3')
    
    jsn_file = 'TCSPC_decay_library.json'
    jsn_path = os.path.join('res','Lib','json',jsn_file)
    
    
    
    
    global bg_channel_marker
    channel = None
    if bg_channel_marker == None:
            pass
    elif bg_channel_marker == 1:
        channel = 'Channel 1'


    elif bg_channel_marker == 2:
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
            mount_LIB_decay_table(decay_list,jsn_dict[channel])
        except:
            dpg.show_item('empty_library_notiffication')
            dpg.show_item('Cancel_library_import')
            
        
    else:
        dpg.show_item('Cancel_library_import')
        dpg.show_item('empty_library_notiffication')
    



def callback_licence(sender,app_data):
    if not 'Licence_title' in dpg.get_aliases():
        with dpg.window(tag='Licence_win',width=dpg.get_viewport_width()/2,
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
            dpg.add_button(tag='Licence_title',width=dpg.get_viewport_width()/2,label='LICENSE')

            dpg.bind_item_theme('Licence_title', 'transparent_theme')
            
            dpg.add_text(label='License',
                         tag='licence_text',
                         default_value = Licence,
                         wrap = int(0.95*(dpg.get_viewport_width()/2)))
    else:
        dpg.delete_item('licence_text')
        dpg.delete_item('Licence_title')
        dpg.delete_item('Licence_win')
        with dpg.window(tag='Licence_win',width=dpg.get_viewport_width()/2,
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
            dpg.add_button(tag='Licence_title',width=dpg.get_viewport_width()/2,label='LICENSE')

            dpg.bind_item_theme('Licence_title', 'transparent_theme')
            with open('../LICENSE', 'r') as file:
                Licence = file.read()
            dpg.add_text(label='License',
                         tag='licence_text',
                         default_value = Licence,
                         wrap = int(0.95*(dpg.get_viewport_width()/2)))



def callback_listbox(sender,app_data):
    global files,last_directory,anal_file
    global fl_bg_curves_dict
    fl_bg_curves_dict ={}
    anal_file = os.path.join(last_directory,app_data)
    load_ptu(anal_file)
    
    
    




def callback_ok_button(sender):
    dpg.hide_item('fl_bg_win_group_4')
    dpg.hide_item('no_curves_notiffication')
    dpg.hide_item('OK_button')
    dpg.configure_item('Calculate_filters',enabled=True)
    
    


def callback_open_folder(sender,app_data):
    global files,last_directory,anal_file
    path = app_data['current_path']
    last_directory = path
    fls = os.listdir(path)
    files = [f for f in fls if f.endswith('.ptu')]
    files.sort()
    
    dpg.configure_item('Files_window',show=True)
    dpg.configure_item('file_box',items=files)
    anal_file = os.path.join(last_directory,files[0])
    load_ptu(anal_file)
    dpg.configure_item('apply_to_all',enabled=True)
    dpg.configure_item('apply_to_file',enabled=True)
    dpg.configure_item('Open_file_dialog',default_path=last_directory)
    dpg.configure_item('PTU_dir_dialog',default_path=last_directory)
    
    
    
    






def callback_proceed_submission(sender,app_data):

    global anal_file,bg_channel_marker
    global fl_bg_curves_dict
    global ntchannels
    global tchanx1,tchany1,tchanx2,tchany2
    wavelength = dpg.get_value('get_wavelength')
    if wavelength == '' or wavelength == 'ERROR!!!':
        
        dpg.set_value('get_wavelength','ERROR!!!')
    else:
        
        
        channel_name = dpg.get_value('get_channel')
        TCSPC_resolution = dpg.get_value('get_tcspc_resolution')
        
        
        
        
        
        
        
        channel = None
        if bg_channel_marker == None:
            pass
        elif bg_channel_marker == 1:
            channel = 1
            xs = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]
            ys = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]

        elif bg_channel_marker == 2:
            channel = 2
            xs = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchanx'+str(channel)]
            ys = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['subtract_bg']['tchany'+str(channel)]
        else:
            pass

        data_array = np.concatenate([xs,ys]).reshape((len([xs,ys]),len([xs,ys][-1])))
        if dpg.get_value('get_name') == '' or dpg.get_value('get_name') == 'Name (optional)':
            name = fl_bg_curves_dict['Channel '+str(channel)][anal_file]['name']
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
                    'TCSPC_channels':ntchannels,
                    'Description':describe,
                    'npy_path':npy_path
                    }
                    
                
        else:

            jsn_dict = {
                channel_name:{
                    name:{
                    'EXC-wavelength':wavelength,
                    'TCSPC_resolution':TCSPC_resolution,
                    'TCSPC_channels':ntchannels,
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
        
        


def callback_query(sender,app_data):
    global B_limit_ch_1,U_limit_ch_1,B_limit_ch_2,U_limit_ch_2
    global Btch_limit_ch_1,Utch_limit_ch_1,Btch_limit_ch_2,Utch_limit_ch_2
    global tau_resolution
    global tchanx1,tchany1,tchanx2,tchany2
    global Tchanx1,Tchany1,Tchanx2,Tchany2
    if sender == 'bottom_limit_ch1':
        dpg.set_axis_limits("xaxis_chan1_zoom", app_data, dpg.get_value('upper_limit_ch1'))
        dpg.set_value('L_dline_ch1',app_data)
        dpg.set_value('U_dline_ch1',dpg.get_value('upper_limit_ch1'))
        B_limit_ch_1 = app_data
        
        Btch_limit_ch_1 = int(B_limit_ch_1/tau_resolution)
        Utch_limit_ch_1 = int(dpg.get_value('upper_limit_ch1')/tau_resolution)
        tchanx1 = Tchanx1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]
        tchany1 = Tchany1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]

    elif sender == 'upper_limit_ch1':
        dpg.set_axis_limits("xaxis_chan1_zoom", dpg.get_value('bottom_limit_ch1'),app_data)
        dpg.set_value('L_dline_ch1',dpg.get_value('bottom_limit_ch1'))
        dpg.set_value('U_dline_ch1',app_data)
        U_limit_ch_1 = app_data
        
        Btch_limit_ch_1 = int(dpg.get_value('bottom_limit_ch1')/tau_resolution)
        Utch_limit_ch_1 = int(U_limit_ch_1/tau_resolution)
        tchanx1 = Tchanx1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]
        tchany1 = Tchany1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]
        
    elif sender == 'bottom_limit_ch2':
        dpg.set_axis_limits("xaxis_chan2_zoom", app_data, dpg.get_value('upper_limit_ch2'))
        dpg.set_value('L_dline_ch2',app_data)
        dpg.set_value('U_dline_ch2',dpg.get_value('upper_limit_ch2'))
        B_limit_ch_2 = app_data
        
        Btch_limit_ch_2 = int(B_limit_ch_2/tau_resolution)
        Utch_limit_ch_2 = int(dpg.get_value('upper_limit_ch2')/tau_resolution)
        tchanx2 = Tchanx2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
        tchany2 = Tchany2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
        
    elif sender == 'upper_limit_ch2':
        dpg.set_axis_limits("xaxis_chan2_zoom", dpg.get_value('bottom_limit_ch2'),app_data)
        dpg.set_value('L_dline_ch2',dpg.get_value('bottom_limit_ch2'))
        dpg.set_value('U_dline_ch2',app_data)
        U_limit_ch_2 = app_data
        
        Btch_limit_ch_2 = int(dpg.get_value('bottom_limit_ch2')/tau_resolution)
        Utch_limit_ch_2 = int(U_limit_ch_2/tau_resolution)
        tchanx2 = Tchanx2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
        tchany2 = Tchany2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
    else:
        pass


    




def callback_reset_range(sender,app_data):
    global sindatax1,sindatax2,sindatax01,sindatax02,tau_mid,MODE
    global B_limit_ch_1,U_limit_ch_1,B_limit_ch_2,U_limit_ch_2
    global Btch_limit_ch_1,Utch_limit_ch_1,Btch_limit_ch_2,Utch_limit_ch_2
    global tau_resolution
    global tchanx1,tchany1,tchanx2,tchany2
    global Tchanx1,Tchany1,Tchanx2,Tchany2

    if MODE == 'PIE':
    
        if sender == 'reset_button_ch1':
            
            dpg.set_axis_limits("xaxis_chan1_zoom", tau_mid ,max(sindatax1))
            dpg.set_value('L_dline_ch1',tau_mid)
            dpg.set_value('U_dline_ch1',max(sindatax1))
            dpg.set_value('bottom_limit_ch1',tau_mid)
            dpg.set_value('upper_limit_ch1',max(sindatax1))
            B_limit_ch_1 = tau_mid
            U_limit_ch_1 = max(sindatax1)
            Btch_limit_ch_1 = int(B_limit_ch_1/tau_resolution)
            Utch_limit_ch_1 = int(U_limit_ch_1/tau_resolution)
            tchanx1 = Tchanx1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]

            tchany1 = Tchany1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]

        elif sender == 'reset_button_ch2':
            dpg.set_axis_limits("xaxis_chan2_zoom", min(sindatax2), tau_mid)
            dpg.set_value('L_dline_ch2',min(sindatax2))
            dpg.set_value('U_dline_ch2',tau_mid)
            dpg.set_value('bottom_limit_ch2',min(sindatax2))
            dpg.set_value('upper_limit_ch2',tau_mid)
            B_limit_ch_2 = min(sindatax2)
            U_limit_ch_2 = tau_mid
            Btch_limit_ch_2 = int(B_limit_ch_2/tau_resolution)
            Utch_limit_ch_2 = int(U_limit_ch_2/tau_resolution)
            tchanx2 = Tchanx2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
            tchany2 = Tchany2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
        else:
            pass
        
    else:
        if sender == 'reset_button_ch1':
            dpg.set_axis_limits("xaxis_chan1_zoom", min(sindatax1), max(sindatax1))
            
            dpg.set_value('L_dline_ch1',min(sindatax1))
            dpg.set_value('U_dline_ch1',max(sindatax1))
            dpg.set_value('bottom_limit_ch1',min(sindatax1))
            dpg.set_value('upper_limit_ch1',max(sindatax1))
            B_limit_ch_1 = min(sindatax1)
            U_limit_ch_1 = max(sindatax1)
            Btch_limit_ch_1 = int(B_limit_ch_1/tau_resolution)
            Utch_limit_ch_1 = int(U_limit_ch_1/tau_resolution)
            tchanx1 = Tchanx1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]
            tchany1 = Tchany1[np.where((Tchanx1>Btch_limit_ch_1) & (Tchanx1<=Utch_limit_ch_1))[0]]
        elif sender == 'reset_button_ch2':
            dpg.set_axis_limits("xaxis_chan2_zoom", min(sindatax2), max(sindatax2))
            dpg.set_value('L_dline_ch2',min(sindatax2))
            dpg.set_value('U_dline_ch2',max(sindatax2))
            dpg.set_value('bottom_limit_ch2',min(sindatax2))
            dpg.set_value('upper_limit_ch2',max(sindatax2))
            B_limit_ch_2 = min(sindatax2)
            U_limit_ch_2 = max(sindatax2)
            Btch_limit_ch_2 = int(B_limit_ch_2/tau_resolution)
            Utch_limit_ch_2 = int(U_limit_ch_2/tau_resolution)
            tchanx2 = Tchanx2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
            tchany2 = Tchany2[np.where((Tchanx2>Btch_limit_ch_2) & (Tchanx2<=Utch_limit_ch_2))[0]]
        else:
            pass






def callback_select_filter_for_batch(sender,app_data):

    value=app_data
    channel = int(sender.split('_')[2])
    
    checkboxes = dpg.get_aliases()
    checkboxes = [ch for ch in checkboxes if ch.startswith('filters_ch_'+str(channel)+'_tab_list_row_')]
    checkboxes = [ch for ch in checkboxes if ch.endswith('_cell b_chk')]
    checkboxes = [ch for ch in checkboxes if ch != sender]

    if value:
        for ch in checkboxes:
            dpg.set_value(ch,False)
            
            
            



def callback_skip_lines_check(sender,app_data):
    
    if app_data:
        dpg.configure_item('skip_lines_drag',enabled=True)
    else:
        dpg.configure_item('skip_lines_drag',enabled=False)
    
    




def calllback_use_stat_filters_chbx(sender,app_data):
    
    log_it('Using statistical filters','a')
    if_value=app_data 
    if if_value:
        if sender == 'use_as_statistical_filters_chkbx_ch_1':
            dpg.show_item('Remove_bgd_butt_ch_1')
            callback_reset_range('reset_button_ch1',None)
            dpg.hide_item('L_dline_ch1')
            dpg.hide_item('U_dline_ch1')
            
            
        if sender == 'use_as_statistical_filters_chkbx_ch_2':
            dpg.show_item('Remove_bgd_butt_ch_2')
            callback_reset_range('reset_button_ch2',None)
            dpg.hide_item('L_dline_ch2')
            dpg.hide_item('U_dline_ch2')
    else:
        if sender == 'use_as_statistical_filters_chkbx_ch_1':
            dpg.hide_item('Remove_bgd_butt_ch_1')
            callback_reset_range('reset_button_ch1',None)
            dpg.show_item('L_dline_ch1')
            dpg.show_item('U_dline_ch1')
            
            
        if sender == 'use_as_statistical_filters_chkbx_ch_2':
            dpg.hide_item('Remove_bgd_butt_ch_2')
            callback_reset_range('reset_button_ch2',None)
            dpg.show_item('L_dline_ch2')
            dpg.show_item('U_dline_ch2')
            
        
@trace
def extract_from_ptu(folder,ptu_file,LLim_ch_1,ULim_ch_1,LLim_ch_2,ULim_ch_2):



    
    
    dpg.configure_item('loading_status',label='Loading')
    
    np.seterr(divide='ignore')
    file=ptu_file.replace('.ptu','')
    path_to_file = os.path.join(folder,ptu_file)
    ptu_image  = PTUreader(path_to_file, print_header_data = False)
    
    mode = ptu_image.head['UsrPulseCfg']
    tau_resolution = ptu_image.head["MeasDesc_Resolution"]*1e9
    tcspc_reolution = int(np.round(tau_resolution*1e-9*1e12))
    sync_rate = ptu_image.head['TTResult_SyncRate']


    if not LLim_ch_1 == None:
        LLim_ch_1 = int(np.floor(LLim_ch_1/tau_resolution))
    else:
        pass
    if not ULim_ch_1 == None:
        ULim_ch_1 = int(np.ceil(ULim_ch_1/tau_resolution))
    else:
        pass
    if not LLim_ch_2 == None:
        LLim_ch_2 = int(np.floor(LLim_ch_2/tau_resolution))
    else:
        pass
    if not ULim_ch_2 == None:
        ULim_ch_2 = int(np.ceil(ULim_ch_2/tau_resolution))
    else:
        pass
    
    
    
    if not dpg.get_value('skip_lines_check'):

        flim_data_stack, intensity_image_all_channels,special,sync = ptu_image.get_flim_data_stack()
    else:

        flim_data_stack, intensity_image_all_channels,special,sync = ptu_image.get_flim_data_stack_omit(dpg.get_value('skip_lines_drag'))

    number_of_frames = int(pd.Series(special).where(pd.Series(special)==4).dropna().count())


    line_width = ptu_image.head['ImgHdr_PixX']
    number_of_lines = ptu_image.head['ImgHdr_PixY']
    pixel_size = 1e3*ptu_image.head['ImgHdr_PixResol']
    special_markers = pd.DataFrame(special,columns=['marker'])
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
                'Lifetime resolution':float(tau_resolution)}
    infoname = file+'.info'

    ntchannels = flim_data_stack.shape[3]


    with open(os.path.join(folder,infoname), "w") as outL_file:
        json.dump(info_dict, outL_file, indent=4, sort_keys=False)

    
    

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


            
            tau = np.linspace(0,ntchannels,ntchannels, dtype = int)*tau_resolution
            XS = np.linspace(0,ntchannels,ntchannels, dtype = int)

            midle_sep = ntchannels//2

            if channels[channel] == 0:

                lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_1+1:ULim_ch_1]
                xs = XS[np.where(XS>midle_sep)[0]]
                ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
                
                ys = np.sum(ys, axis = 0).astype(float)
                fYS = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0) 
                fYS = np.sum(fYS, axis = 0).astype(float)
                ys = ys[np.where(XS>midle_sep)[0]]

                if dpg.get_value('use_as_statistical_filters_chkbx_ch_1'):
                    dpg.configure_item('loading_status',label='Calculating filters channel 1')
                    filtering_decays_ch_1 = prepare_input_to_calculate_filters_from_routine(xs,ys,ntchannels,tcspc_reolution,filtering_routine,1)

                    

                    
            
                    FILTRY_ch_1 = calculate_stat_filter(filtering_decays_ch_1,ys)

                    dpg.configure_item('loading_status',label='Calculating weights channel 1')
                    filter_weight_ch_1 = make_weight_from_filters(FILTRY_ch_1,1)
                    dpg.configure_item('loading_status',label='Filtering channel 1')
                    filtered_image_data=np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))


                    
                    for j in range(lifetime_data.shape[2]):
                        filtered_image_data[:,:,j] = lifetime_data[:,:,j]*filter_weight_ch_1[j]
                    
                    lifetime_data = filtered_image_data


                else: 
                    pass



            else:
                lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_2:ULim_ch_2]
                xs = XS[np.where(XS<=midle_sep)[0]]
                ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)

                ys = np.sum(ys, axis = 0).astype(float)
                fYS = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0) 
                fYS = np.sum(fYS, axis = 0).astype(float)
                ys = ys[np.where(XS<=midle_sep)[0]]
                if dpg.get_value('use_as_statistical_filters_chkbx_ch_2'):
                    dpg.configure_item('loading_status',label='Calculating filters channel 2')
                    filtering_decays_ch_2 = prepare_input_to_calculate_filters_from_routine(xs,ys,ntchannels,tcspc_reolution,filtering_routine,2)

                    FILTRY_ch_2 = calculate_stat_filter(filtering_decays_ch_2,ys)

                    dpg.configure_item('loading_status',label='Calculating weights channel 1')
                    filter_weight_ch_2 = make_weight_from_filters(FILTRY_ch_2,2)
                    dpg.configure_item('loading_status',label='Filtering channel 2')
                    filtered_image_data=np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
                    


                    for j in range(lifetime_data.shape[2]):
                        filtered_image_data[:,:,j] = lifetime_data[:,:,j]*filter_weight_ch_2[j]
                    lifetime_data = filtered_image_data
                    
                else:
                    pass
        else:
            NT_channels = flim_data_stack.shape[3]

            tau = np.linspace(0,ntchannels,ntchannels, dtype = int)*tau_resolution
            XS = np.linspace(0,ntchannels,ntchannels, dtype = int)


            if channels[channel] == 0:

                lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_1:ULim_ch_1]
                xs=XS
                ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)

                ys = np.sum(ys, axis = 0).astype(float)
                
                if dpg.get_value('use_as_statistical_filters_chkbx_ch_1'):
                    dpg.configure_item('loading_status',label='Calculating filters channel 1')
                    filtering_decays_ch_1 = prepare_input_to_calculate_filters_from_routine(xs,ys,ntchannels,tcspc_reolution,filtering_routine,1)
                    FILTRY_ch_1 = calculate_stat_filter(filtering_decays_ch_1,ys)

                    dpg.configure_item('loading_status',label='Calculating weights channel 1')
                    filter_weight_ch_1 = make_weight_from_filters(FILTRY_ch_1,1)
                    dpg.configure_item('loading_status',label='Filtering channel 1')
                    filtered_image_data=np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
                    for j in range(lifetime_data.shape[2]):
                        filtered_image_data[:,:,j] = lifetime_data[:,:,j]*filter_weight_ch_1[j]
                    lifetime_data = filtered_image_data

                else:
                    pass

            else:
                lifetime_data = flim_data_stack[:,:,channels[channel],LLim_ch_2:ULim_ch_2]
                xs=XS
                ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)

                ys = np.sum(ys, axis = 0).astype(float)
                if dpg.get_value('use_as_statistical_filters_chkbx_ch_2'):
                    dpg.configure_item('loading_status',label='Calculating filters channel 2')
                    filtering_decays_ch_2 = prepare_input_to_calculate_filters_from_routine(xs,ys,ntchannels,tcspc_reolution,filtering_routine,2)
                    FILTRY_ch_2 = calculate_stat_filter(filtering_decays_ch_2,ys)

                    dpg.configure_item('loading_status',label='Calculating weights channel 2')
                    filter_weight_ch_2 = make_weight_from_filters(FILTRY_ch_2,2)
                    dpg.configure_item('loading_status',label='Filtering channel 2')
                    filtered_image_data=np.zeros((lifetime_data.shape[0],lifetime_data.shape[1],lifetime_data.shape[2]))
                    for j in range(lifetime_data.shape[2]):
                        filtered_image_data[:,:,j] = lifetime_data[:,:,j]*filter_weight_ch_2[j]
                    
                    lifetime_data = filtered_image_data
                        
                else:
                    pass

        taus = pd.DataFrame(xs,columns = ['Tau'])
        fulltaus = pd.DataFrame(XS,columns = ['Tau'])
        

        taus['Intensity'] = ys
        fulltaus['Intensity'] = fYS

        
        
        

        intensity = np.sum(lifetime_data, axis = 2)    
        lifetime = np.zeros(lifetime_data.shape)




            











        if channels[channel] == 0:
            lt_chan_range = range(LLim_ch_1,ULim_ch_1,1)

            if lifetime_data.shape[2]<len(lt_chan_range):
                lt_chan_range = range(0,lifetime_data.shape[2],1)

            else:

                pass

            for k,t_chan in enumerate(lt_chan_range):




                lifetime[:,:,k]=lifetime_data[:,:,k]*t_chan*tau_resolution

        else:
            lt_chan_range = range(LLim_ch_2,ULim_ch_2,1)


            if lifetime_data.shape[2]<len(lt_chan_range):
                lt_chan_range = range(0,lifetime_data.shape[2],1)
            else:
                pass

            for k,t_chan in enumerate(lt_chan_range):



                lifetime[:,:,k]=lifetime_data[:,:,k]*t_chan*tau_resolution



        inv_intensity = np.where(intensity.astype(int)!=0,1/intensity.astype(int),np.nan)
        lifetimes = np.sum(lifetime, axis = 2)*inv_intensity






        channel_data = np.sum(flim_data_stack[:,:,channels[channel],:],axis=2)

        dpg.configure_item('loading_status',label='Exporting data to png - Channel '+str(channel+1))
        to_png = channel_data*1/(np.max(channel_data)/255)

        px = 1/plt.rcParams['figure.dpi']
        width = channel_data.shape[0]
        height = channel_data.shape[1]


        fig = Figure(figsize=(width*px,height*px),facecolor='black')
        ax = fig.add_subplot()
        fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        ax.margins(0, 0,)
        ax.axis('off')
        ax.imshow(to_png,cmap='nipy_spectral')
        b =BytesIO()
        FigureCanvas(fig).print_png(b)
        plt.close()

        b.seek(0)
        image=Image.open(b)
        image.save(os.path.join(folder,png_FC_name))
        del(b)

        im = Image.fromarray(np.uint8(to_png))
        im.save(os.path.join(folder,png_name))

        export_df = pd.DataFrame(channel_data)
        dpg.configure_item('loading_status',label='Exporting data to csv - Channel '+str(channel+1))
        export_df.to_csv(os.path.join(folder,csv_name), sep=',',index=False,header=False)
        dpg.configure_item('loading_status',label='Exporting data to pickle - Channel '+str(channel+1))
        export_df.to_pickle(os.path.join(folder,pickle_name))
        taus.to_pickle(os.path.join(folder,tau_pickle_name))
        fulltaus.to_pickle(os.path.join(folder,full_tau_pickle_name))
        dpg.configure_item('loading_status',label='Exporting data to numpy array - Channel '+str(channel+1))
        np.save(os.path.join(folder,np_LT_name), lifetimes) 
        np.save(os.path.join(folder,np_int_name), intensity)
    
    
    


@trace
def load_ptu(file_path):
    global ww
    global tau_resolution
    global filtering_routine
    global ntchannels
    with dpg.window(tag='load_ind_win',width=ww,height=250,
                            menubar=False,
                            autosize=False,
                            no_title_bar=True,
                            no_move=True,
                            no_background=True,
                            modal=True,
                            
                       show=True):
                    
        dpg.add_button(tag='loading_title',width=ww,label='Please wait')

        dpg.bind_item_theme('loading_title', 'transparent_theme')
        dpg.add_button(tag='loading_butt',width=ww,label='LOADING...')
        dpg.bind_item_theme('loading_butt', 'transparent_theme')
    win_width = dpg.get_item_configuration('load_ind_win')['width']
    win_height = dpg.get_item_configuration('load_ind_win')['height']
    VP_w = dpg.get_viewport_width()
    VP_h = dpg.get_viewport_height()
    posit = (int(VP_w/2-win_width/2),int(VP_h/2-win_height/2))
    dpg.configure_item('load_ind_win',pos=posit)
    
    
    
    global sindatax1, sindatay1,sindatax2, sindatay2,tau_mid,MODE
    global B_limit_ch_1,U_limit_ch_1,B_limit_ch_2,U_limit_ch_2
    global tchanx1,tchany1,tchanx2,tchany2
    global Tchanx1,Tchany1,Tchanx2,Tchany2
    global Btch_limit_ch_1,Utch_limit_ch_1,Btch_limit_ch_2,Utch_limit_ch_2
    B_limit_ch_1 = U_limit_ch_1 = B_limit_ch_2 = U_limit_ch_2 = None
    Btch_limit_ch_1 = Utch_limit_ch_1 = Btch_limit_ch_2 = Utch_limit_ch_2 = None
    
    tchanx1=tchany1=tchanx2=tchany2=Tchanx1=Tchany1=Tchanx2=Tchany2=[]
    sindatax1 = sindatay1 = sindatax2 = sindatay2 = []
    dpg.set_value('tag_series_ch_1', [sindatax1, sindatay1])
    dpg.fit_axis_data("xaxis_chan1")
    dpg.fit_axis_data("yaxis_chan1")

    dpg.set_value('tag_series_ch_1_zoom', [sindatax1, sindatay1])
    dpg.fit_axis_data("xaxis_chan1_zoom")
    dpg.fit_axis_data("yaxis_chan1_zoom")
    dpg.set_value('tag_series_ch_2', [sindatax2, sindatay2])
    dpg.fit_axis_data("xaxis_chan2")
    dpg.fit_axis_data("yaxis_chan2")
    dpg.set_value('tag_series_ch_2_zoom', [sindatax2, sindatay2])
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
    log_it('\tFile','a')
    log_it('\t\t '+file_path,'a')
    log_it('\tloaded.','a')
    tau_resolution = ptu_image.head["MeasDesc_Resolution"]*1e9  
    sync_rate = ptu_image.head['TTResult_SyncRate']

    
    if not dpg.get_value('skip_lines_check'):

        flim_data_stack, intensity_image_all_channels,special,sync = ptu_image.get_flim_data_stack()
    else:
        flim_data_stack, intensity_image_all_channels,special,sync = ptu_image.get_flim_data_stack_omit(dpg.get_value('skip_lines_drag'))
    
    ntchannels = flim_data_stack.shape[3]
    MODE = ptu_image.head['UsrPulseCfg']
    dpg.set_value('mode_text','MODE: '+MODE)
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
            
            
            
            tau = np.linspace(0,ntchannels,ntchannels, dtype = int)*tau_resolution
            Tchanx1 = Tchanx2 = np.linspace(0,ntchannels,ntchannels, dtype = int)
            if MODE == 'PIE':
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

                    midle_sep = ntchannels//2
                    
                    
                    tau_mid = midle_sep*tau_resolution

                    if channels[channel] == 0:
                        
                        lifetime_data = flim_data_stack[:,:,channels[channel],midle_sep:]

                        ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
            
                        ys = np.sum(ys, axis = 0).astype(float)
                        tchanx1 = Tchanx1[np.where(Tchanx1>midle_sep)[0]]
                        Tchany1 = ys
                        tchany1 = Tchany1[np.where(Tchanx1>midle_sep)[0]]

                        sindatax1, sindatay1 = tau,ys
                        dpg.set_value('tag_series_ch_1', [sindatax1, sindatay1])
                        dpg.fit_axis_data("xaxis_chan1")
                        dpg.fit_axis_data("yaxis_chan1")
                        dpg.set_axis_limits("xaxis_chan1", min(sindatax1) ,max(sindatax1))
                        dpg.set_value('tag_series_ch_1_zoom', [sindatax1, sindatay1])
                        dpg.fit_axis_data("xaxis_chan1_zoom")
                        dpg.fit_axis_data("yaxis_chan1_zoom")
                        
                        dpg.set_axis_limits("xaxis_chan1_zoom", tau_mid ,max(sindatax1))
                        dpg.set_value('bottom_limit_ch1',tau_mid)
                        dpg.set_value('upper_limit_ch1',max(sindatax1))
                        dpg.set_value('L_dline_ch1',tau_mid)
                        dpg.set_value('U_dline_ch1',max(sindatax1))
                        dpg.configure_item('bottom_limit_ch1',min_value=min(sindatax1))
                        dpg.configure_item('bottom_limit_ch1',max_value=max(sindatax1))
                        dpg.configure_item('upper_limit_ch1',min_value=min(sindatax1))
                        dpg.configure_item('upper_limit_ch1',max_value=max(sindatax1))
                        
                        
                        
                        
                        

                        
                        

                        
                        B_limit_ch_1 = dpg.get_value('L_dline_ch1')
                        U_limit_ch_1 = dpg.get_value('U_dline_ch1')
                        
                        Btch_limit_ch_1 = B_limit_ch_1/tau_resolution
                        Utch_limit_ch_1 = U_limit_ch_1/tau_resolution


    
                        dpg.show_item('use_as_statistical_filters_chkbx_ch_1')
                        dpg.set_value('use_as_statistical_filters_chkbx_ch_1',False)
                        calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_1',False)
                        
                        
                    else:
                        tchanx2 = Tchanx2[np.where(Tchanx2<=midle_sep)[0]]
                        lifetime_data = flim_data_stack[:,:,channels[channel],:midle_sep]
                        ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
            
                        ys = np.sum(ys, axis = 0).astype(float)
                        Tchany2 = ys
                        tchany2 = Tchany2[np.where(Tchanx2<=midle_sep)[0]]
                        sindatax2, sindatay2 = tau,ys
                        dpg.set_value('tag_series_ch_2', [sindatax2, sindatay2])
                        dpg.fit_axis_data("xaxis_chan2")
                        dpg.fit_axis_data("yaxis_chan2")
                        dpg.set_axis_limits("xaxis_chan2", min(sindatax2) ,max(sindatax2))
                        dpg.set_value('tag_series_ch_2_zoom', [sindatax2, sindatay2])
                        dpg.fit_axis_data("xaxis_chan2_zoom")
                        dpg.fit_axis_data("yaxis_chan2_zoom")


                        
                        dpg.set_axis_limits("xaxis_chan2_zoom", min(sindatax2) ,tau_mid)
                        dpg.set_value('bottom_limit_ch2',min(sindatax2))
                        dpg.set_value('upper_limit_ch2',tau_mid)
                        dpg.set_value('L_dline_ch2',min(sindatax2))
                        dpg.set_value('U_dline_ch2',tau_mid)
                        dpg.configure_item('bottom_limit_ch2',min_value=min(sindatax2))
                        dpg.configure_item('bottom_limit_ch2',max_value=max(sindatax2))
                        dpg.configure_item('upper_limit_ch2',min_value=min(sindatax2))
                        dpg.configure_item('upper_limit_ch2',max_value=max(sindatax2))
                        
                        B_limit_ch_2 = dpg.get_value('L_dline_ch2')
                        U_limit_ch_2 = dpg.get_value('U_dline_ch2')
                        
                        Btch_limit_ch_2 = B_limit_ch_2/tau_resolution
                        Utch_limit_ch_2 = U_limit_ch_2/tau_resolution


                        
                        
                        
                        

                        dpg.show_item('use_as_statistical_filters_chkbx_ch_2')
                        dpg.set_value('use_as_statistical_filters_chkbx_ch_2',False)
                        calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_2',False)
                        
                else:
                    '''PIE MODE one channels'''
                    
                    midle_sep = ntchannels//2
                    
                    
                    tau_mid = midle_sep*tau_resolution
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
                        tchanx1 = Tchanx1[np.where(Tchanx1>midle_sep)[0]]
                        Tchany1 = ys
                        tchany1 = Tchany1[np.where(Tchanx1>midle_sep)[0]]
                        
                        sindatax1, sindatay1 = tau,ys
                        dpg.set_value('tag_series_ch_1', [sindatax1, sindatay1])
                        dpg.fit_axis_data("xaxis_chan1")
                        dpg.fit_axis_data("yaxis_chan1")
                        dpg.set_axis_limits("xaxis_chan1", min(sindatax1) ,max(sindatax1))
                        dpg.set_value('tag_series_ch_1_zoom', [sindatax1, sindatay1])
                        dpg.fit_axis_data("xaxis_chan1_zoom")
                        dpg.fit_axis_data("yaxis_chan1_zoom")
                        dpg.set_axis_limits("xaxis_chan1_zoom", tau_mid ,max(sindatax1))
                        dpg.set_value('bottom_limit_ch1',tau_mid)
                        dpg.set_value('upper_limit_ch1',max(sindatax1))
                        dpg.set_value('L_dline_ch1',tau_mid)
                        dpg.set_value('U_dline_ch1',max(sindatax1))
                        dpg.configure_item('bottom_limit_ch1',min_value=min(sindatax1))
                        dpg.configure_item('bottom_limit_ch1',max_value=max(sindatax1))
                        dpg.configure_item('upper_limit_ch1',min_value=min(sindatax1))
                        dpg.configure_item('upper_limit_ch1',max_value=max(sindatax1))




                        B_limit_ch_1 = dpg.get_value('L_dline_ch1')
                        U_limit_ch_1 = dpg.get_value('U_dline_ch1')
                        Btch_limit_ch_1 = B_limit_ch_1/tau_resolution
                        Utch_limit_ch_1 = U_limit_ch_1/tau_resolution
                        
                        
                        dpg.show_item('use_as_statistical_filters_chkbx_ch_1')
                        dpg.set_value('use_as_statistical_filters_chkbx_ch_1',False)
                        calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_1',False)


                        
                        
                        
                        
                        
                        
                        
                        
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
                        
                        tchanx2 = Tchanx2[np.where(Tchanx2<=midle_sep)[0]]
                        Tchany2 = ys
                        tchany2 = Tchany2[np.where(Tchanx2<=midle_sep)[0]]
                        sindatax2, sindatay2 = tau,ys
                        dpg.set_value('tag_series_ch_2', [sindatax2, sindatay2])
                        dpg.fit_axis_data("xaxis_chan2")
                        dpg.fit_axis_data("yaxis_chan2")
                        dpg.set_axis_limits("xaxis_chan2", min(sindatax2) ,max(sindatax2))
                        dpg.set_value('tag_series_ch_2_zoom', [sindatax2, sindatay2])
                        dpg.fit_axis_data("xaxis_chan2_zoom")
                        dpg.fit_axis_data("yaxis_chan2_zoom")
                        dpg.set_axis_limits("xaxis_chan2_zoom", min(sindatax2) ,tau_mid)
                        dpg.set_value('bottom_limit_ch2',min(sindatax2))
                        dpg.set_value('upper_limit_ch2',tau_mid)
                        dpg.set_value('L_dline_ch2',min(sindatax2))
                        dpg.set_value('U_dline_ch2',tau_mid)
                        dpg.configure_item('bottom_limit_ch2',min_value=min(sindatax2))
                        dpg.configure_item('bottom_limit_ch2',max_value=max(sindatax2))
                        dpg.configure_item('upper_limit_ch2',min_value=min(sindatax2))
                        dpg.configure_item('upper_limit_ch2',max_value=max(sindatax2))


                        B_limit_ch_2 = dpg.get_value('L_dline_ch2')
                        U_limit_ch_2 = dpg.get_value('U_dline_ch2')
                        Btch_limit_ch_2 = B_limit_ch_2/tau_resolution
                        Utch_limit_ch_2 = U_limit_ch_2/tau_resolution
                        
                        
                        dpg.show_item('use_as_statistical_filters_chkbx_ch_2')
                        dpg.set_value('use_as_statistical_filters_chkbx_ch_2',False)
                        calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_2',False)


                        
                        
                        
                        
                        
                        

                    
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
                        
                        tchanx1 = Tchanx1
                        Tchany1 = ys
                        tchany1 = Tchany1
                        sindatax1, sindatay1 = tau,ys
                        dpg.set_value('tag_series_ch_1', [sindatax1, sindatay1])
                        dpg.fit_axis_data("xaxis_chan1")
                        dpg.fit_axis_data("yaxis_chan1")
                        dpg.set_axis_limits("xaxis_chan1", min(sindatax1) ,max(sindatax1))
                        dpg.set_value('tag_series_ch_1_zoom', [sindatax1, sindatay1])
                        dpg.fit_axis_data("xaxis_chan1_zoom")
                        dpg.fit_axis_data("yaxis_chan1_zoom")
                        
                        dpg.set_axis_limits("xaxis_chan1_zoom", min(sindatax1) ,max(sindatax1))
                        dpg.set_value('bottom_limit_ch1',min(sindatax1))
                        dpg.set_value('upper_limit_ch1',max(sindatax1))
                        dpg.set_value('L_dline_ch1',min(sindatax1))
                        dpg.set_value('U_dline_ch1',max(sindatax1))
                        dpg.configure_item('bottom_limit_ch1',min_value=min(sindatax1))
                        dpg.configure_item('bottom_limit_ch1',max_value=max(sindatax1))
                        dpg.configure_item('upper_limit_ch1',min_value=min(sindatax1))
                        dpg.configure_item('upper_limit_ch1',max_value=max(sindatax1))
                        
                        


                        
                        B_limit_ch_1 = dpg.get_value('L_dline_ch1')
                        U_limit_ch_1 = dpg.get_value('U_dline_ch1')
                        
                        Btch_limit_ch_1 = B_limit_ch_1/tau_resolution
                        Utch_limit_ch_1 = U_limit_ch_1/tau_resolution
                        
                        dpg.show_item('use_as_statistical_filters_chkbx_ch_1')
                        dpg.set_value('use_as_statistical_filters_chkbx_ch_1',False)
                        calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_1',False)


    
                        
                    else:
                        lifetime_data = flim_data_stack[:,:,channels[channel],:]
                        ys = np.sum(flim_data_stack[:,:,channels[channel],:], axis=0)
            
                        ys = np.sum(ys, axis = 0).astype(float)
                        tchanx2 = Tchanx2
                        Tchany2 = ys
                        tchany2 = Tchany2
                        sindatax2, sindatay2 = tau,ys
                        dpg.set_value('tag_series_ch_2', [sindatax2, sindatay2])
                        dpg.fit_axis_data("xaxis_chan2")
                        dpg.fit_axis_data("yaxis_chan2")
                        dpg.set_axis_limits("xaxis_chan2", min(sindatax2) ,max(sindatax2))
                        dpg.set_value('tag_series_ch_2_zoom', [sindatax2, sindatay2])
                        dpg.fit_axis_data("xaxis_chan2_zoom")
                        dpg.fit_axis_data("yaxis_chan2_zoom")


                        
                        dpg.set_axis_limits("xaxis_chan2_zoom", min(sindatax2) ,max(sindatax2))
                        dpg.set_value('bottom_limit_ch2',min(sindatax2))
                        dpg.set_value('upper_limit_ch2',max(sindatax2))
                        dpg.set_value('L_dline_ch2',min(sindatax2))
                        dpg.set_value('U_dline_ch2',max(sindatax2))
                        dpg.configure_item('bottom_limit_ch2',min_value=min(sindatax2))
                        dpg.configure_item('bottom_limit_ch2',max_value=max(sindatax2))
                        dpg.configure_item('upper_limit_ch2',min_value=min(sindatax2))
                        dpg.configure_item('upper_limit_ch2',max_value=max(sindatax2))
                        
                        B_limit_ch_2 = dpg.get_value('L_dline_ch2')
                        U_limit_ch_2 = dpg.get_value('U_dline_ch2')
                        
                        Btch_limit_ch_2 = B_limit_ch_2/tau_resolution
                        Utch_limit_ch_2 = U_limit_ch_2/tau_resolution
                        
                        dpg.show_item('use_as_statistical_filters_chkbx_ch_2')
                        dpg.set_value('use_as_statistical_filters_chkbx_ch_2',False)
                        calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_2',False)


                
                
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
                
                        tchanx1 = Tchanx1
                        Tchany1 = ys
                        tchany1 = Tchany1

                        sindatax1, sindatay1 = tau,ys
                        dpg.set_value('tag_series_ch_1', [sindatax1, sindatay1])
                        dpg.fit_axis_data("xaxis_chan1")
                        dpg.fit_axis_data("yaxis_chan1")
                        dpg.set_axis_limits("xaxis_chan1", min(sindatax1) ,max(sindatax1))
                        dpg.set_axis_limits("xaxis_chan1_zoom", min(sindatax1) ,max(sindatax1))
                        dpg.set_value('tag_series_ch_1_zoom', [sindatax1, sindatay1])
                        dpg.fit_axis_data("xaxis_chan1_zoom")
                        dpg.fit_axis_data("yaxis_chan1_zoom")
                        dpg.set_value('bottom_limit_ch1',min(sindatax1))
                        dpg.set_value('upper_limit_ch1',max(sindatax1))
                        dpg.set_value('L_dline_ch1',min(sindatax1))
                        dpg.set_value('U_dline_ch1',max(sindatax1))
                        dpg.configure_item('bottom_limit_ch1',min_value=min(sindatax1))
                        dpg.configure_item('bottom_limit_ch1',max_value=max(sindatax1))
                        dpg.configure_item('upper_limit_ch1',min_value=min(sindatax1))
                        dpg.configure_item('upper_limit_ch1',max_value=max(sindatax1))





                        B_limit_ch_1 = dpg.get_value('L_dline_ch1')
                        U_limit_ch_1 = dpg.get_value('U_dline_ch1')
                        
                        Btch_limit_ch_1 = B_limit_ch_1/tau_resolution
                        Utch_limit_ch_1 = U_limit_ch_1/tau_resolution
                        
                        dpg.show_item('use_as_statistical_filters_chkbx_ch_1')
                        dpg.set_value('use_as_statistical_filters_chkbx_ch_1',False)
                        calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_1',False)


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
                        tchanx2 = Tchanx2
                        Tchany2 = ys
                        tchany2 = Tchany2
                        sindatax2, sindatay2 = tau,ys
                        dpg.set_value('tag_series_ch_2', [sindatax2, sindatay2])
                        dpg.fit_axis_data("xaxis_chan2")
                        dpg.fit_axis_data("yaxis_chan2")
                        dpg.set_axis_limits("xaxis_chan2", min(sindatax2) ,max(sindatax2))
                        dpg.set_axis_limits("xaxis_chan2_zoom", min(sindatax2) ,max(sindatax2))
                        dpg.set_value('tag_series_ch_2_zoom', [sindatax2, sindatay2])
                        dpg.fit_axis_data("xaxis_chan2_zoom")
                        dpg.fit_axis_data("yaxis_chan2_zoom")
                        dpg.set_value('bottom_limit_ch2',min(sindatax2))
                        dpg.set_value('upper_limit_ch2',max(sindatax2))
                        dpg.set_value('L_dline_ch2',min(sindatax2))
                        dpg.set_value('U_dline_ch2',max(sindatax2))
                        dpg.configure_item('bottom_limit_ch2',min_value=min(sindatax2))
                        dpg.configure_item('bottom_limit_ch2',max_value=max(sindatax2))
                        dpg.configure_item('upper_limit_ch2',min_value=min(sindatax2))
                        dpg.configure_item('upper_limit_ch2',max_value=max(sindatax2))


                        B_limit_ch_2 = dpg.get_value('L_dline_ch2')
                        U_limit_ch_2 = dpg.get_value('U_dline_ch2')
                        
                        Btch_limit_ch_2 = B_limit_ch_2/tau_resolution
                        Utch_limit_ch_2 = U_limit_ch_2/tau_resolution
                        
                        dpg.show_item('use_as_statistical_filters_chkbx_ch_2')
                        dpg.set_value('use_as_statistical_filters_chkbx_ch_2',False)
                        calllback_use_stat_filters_chbx('use_as_statistical_filters_chkbx_ch_2',False)


    
    


    
    if_Tchany1 = len(Tchany1)!=0
    if_Tchany2 = len(Tchany2)!=0
    



        

        





        



        
    
    if_routine_ch_1 = dpg.get_value('use_as_group_routine_chkbx_ch_1')
    if_routine_ch_2 = dpg.get_value('use_as_group_routine_chkbx_ch_2')
    
    if if_routine_ch_1 and if_routine_ch_2:
        pass
    elif if_routine_ch_1 and not if_routine_ch_2:
        
        filtering_routine['Channel 2']={ 'BG':False}
    elif not if_routine_ch_1 and  if_routine_ch_2:
        filtering_routine['Channel 1']={ 'BG':False}
    elif not if_routine_ch_1 and not if_routine_ch_2:
        filtering_routine={'Channel 1':
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
        
    
        unmount_filter_list_table(1)
        
    if if_routine_ch_2:

        dpg.show_item('filters_ch_2_tab_list_tag')
    else:
        dpg.hide_item('filters_ch_2_tab_list_tag')
        unmount_filter_list_table(2)
        
        
            
    
    dpg.configure_item('load_ind_win',show=False)
    try:
        dpg.delete_item('loading_butt')
        dpg.delete_item('loading_title')
        dpg.delete_item('load_ind_win')
        
        
    except:
        pass
     
            




def make_smooth(xs,substracted_tchany):
    subtr = pd.DataFrame(xs,columns=['xs'])
    subtr['ys']= substracted_tchany
    subtr['ys'] = subtr['ys'].where(subtr['ys']>=0,0)
    rol_win = len(substracted_tchany)//50
    
    subtr['smth'] = subtr.ys.rolling(rol_win,center=True).median().fillna(0)

    
    
    return subtr
    


@trace
def make_weight_from_filters(filters_dict,channel):

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
        log_it('No filters selected - ignoring','a')

    else:
        F = filters_dict[filter_name]

        weight = F/max(F)
        weight = np.where(weight>0,weight,0)

    return weight

    

    
    
    


def mount_LIB_decay_table(decay_list,_dict):
    
    for i,decay in enumerate(decay_list):
        EXC_wavelength = _dict[decay]['EXC-wavelength']
        TCSPC_resolution = _dict[decay]['TCSPC_resolution']
        TCSPC_channels = _dict[decay]['TCSPC_channels']
        Description = _dict[decay]['Description']
        with dpg.table_row(tag ='decays_lib_tab_row_'+str(i),parent='decays_tab_lib_list_tag'):
            with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell null'):
                dpg.add_text(i+1,tag = 'decays_lib_tab_row_'+str(i)+'_cell null_text')
            with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell a'):
                dpg.add_text(decay,tag = 'decays_lib_tab_row_'+str(i)+'_cell a_text')
            with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell b'):
                dpg.add_text(EXC_wavelength,tag = 'decays_lib_tab_row_'+str(i)+'_cell b_text')
            with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell c'):
                dpg.add_text(Description,tag = 'decays_lib_tab_row_'+str(i)+'_cell c_text')
            with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell d'):
                dpg.add_text(TCSPC_resolution,tag = 'decays_lib_tab_row_'+str(i)+'_cell d_text')
            with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell f'):
                dpg.add_text(TCSPC_channels,tag = 'decays_lib_tab_row_'+str(i)+'_cell f_text')
            with dpg.table_cell(tag = 'decays_lib_tab_row_'+str(i)+'_cell e'):
                dpg.add_checkbox(
                         default_value=False,
                    enabled=True,
                    tag = 'decays_lib_tab_row_'+str(i)+'_cell e_chk',
                   
                            )
                



def mount_decay_table(decay_list):
    global fl_bg_curves_dict
    global anal_file
    global bg_channel_marker
    channel = None
    if bg_channel_marker == None:
            pass
    elif bg_channel_marker == 1:
        channel = 'Channel 1'
        if_substracted = len(fl_bg_curves_dict[channel][anal_file]['subtract_bg']['tchanx1'])>0

    elif bg_channel_marker == 2:
        channel = 'Channel 2'
        if_substracted = len(fl_bg_curves_dict[channel][anal_file]['subtract_bg']['tchanx2'])>0

    else:
        pass
    
    
    
    for i,decay in enumerate(decay_list):
        with dpg.table_row(tag ='decays_tab_row_'+str(i),parent='decays_tab_list_tag'):
            with dpg.table_cell(tag = 'decays_tab_row_'+str(i)+'_cell #'):
                dpg.add_text(str(i+1),tag = 'decays_tab_row_'+str(i)+'_cell #_text')
            with dpg.table_cell(tag = 'decays_tab_row_'+str(i)+'_cell a'):
                dpg.add_text(decay,tag = 'decays_tab_row_'+str(i)+'_cell a_text')
            with dpg.table_cell(tag = 'decays_tab_row_'+str(i)+'_cell b'):
                
                if i!=0:
                    
                    
                         dpg.add_checkbox(
                             default_value=True,enabled=True,tag = 'decays_tab_row_'+str(i)+'_cell b_chk',
                             callback=callback_chkbox_decay_table_mark
                                )
                    
                else:

                    if if_substracted:
                        dpg.add_checkbox(
                             default_value=True,
                            enabled=False,
                            tag = 'decays_tab_row_'+str(i)+'_cell b_chk',
                            callback=callback_chkbox_decay_table_mark
                                )
                    else:
                        dpg.add_checkbox(
                             default_value=False,
                            enabled=False,
                            tag = 'decays_tab_row_'+str(i)+'_cell b_chk',
                            callback=callback_chkbox_decay_table_mark
                                )
            
                



def mount_filter_list_table(channel):
    global Filters
    for i,F in enumerate(Filters.keys()):
        
        log_it('\t- '+F,'a')
        
        with dpg.table_row(tag ='filters_ch_'+str(channel)+'_tab_list_row_'+str(i),
                           parent='filters_ch_'+str(channel)+'_tab_list_tag'):
            with dpg.table_cell(tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell #'):
                dpg.add_text(str(i+1),tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell #_text')
            with dpg.table_cell(tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell a'):
                dpg.add_text(F,tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell a_text')
            with dpg.table_cell(tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell b'):
                if F == 'Current decay; CH '+str(channel):
                    dpg.add_checkbox(
                                 default_value=True,
                        enabled=True,
                        tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell b_chk',
                        callback=callback_select_filter_for_batch
                                    )
                else:
                    dpg.add_checkbox(
                                 default_value=False,
                        enabled=True,
                        tag = 'filters_ch_'+str(channel)+'_tab_list_row_'+str(i)+'_cell b_chk',
                        callback=callback_select_filter_for_batch
                                    )
                


def mount_status_modal():
    with dpg.window(tag='load_ind_win',width=ww,height=250,
                            menubar=False,
                            autosize=False,
                            no_title_bar=True,
                            no_move=True,
                            no_background=True,
                            modal=True,
                            
                       show=True):
                    
        dpg.add_button(tag='loading_title',width=ww,label='Processing file:')

        dpg.bind_item_theme('loading_title', 'transparent_theme')
        dpg.add_button(tag='loading_butt',width=ww,label='')
        dpg.bind_item_theme('loading_butt', 'transparent_theme')
        dpg.add_button(tag='loading_status_text',width=ww,label='Status:')
        dpg.bind_item_theme('loading_status_text', 'transparent_theme')
        dpg.add_button(tag='loading_status',width=ww,label='Extracting')
        dpg.bind_item_theme('loading_status', 'transparent_theme')
        dpg.add_button(tag='loading_cnt_butt',width=ww,label='')
        dpg.bind_item_theme('loading_cnt_butt', 'transparent_theme')
    win_width = dpg.get_item_configuration('load_ind_win')['width']
    win_height = dpg.get_item_configuration('load_ind_win')['height']
    VP_w = dpg.get_viewport_width()
    VP_h = dpg.get_viewport_height()
    posit = (int(VP_w/2-win_width/2),int(VP_h/2-win_height/2))
    dpg.configure_item('load_ind_win',pos=posit)
    
    
    

@trace
def prepare_input_to_calculate_filters_from_routine(XS,YS,TCSPC_SIZE,TCSPC_RESOLUTION,routine,channel):
    global anal_file
    global fl_bg_curves_dict
    global tchanx1,tchany1,tchanx2,tchany2
    global tau_resolution
    XS = XS*tau_resolution-(XS*tau_resolution)[0]
    log_it('\tCalculating input for filtering for '+anal_file+'; channel '+str(channel),'a')

    











        









    
    
    
    
    
    
    
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
        log_it('\tFailure: no filters selected.','a')
        
        
        
        
        
        
    elif not if_BG and len(curve_names)>0:
        
        
        for curv in curve_names:

            

            curve = np.load(routine['Channel '+str(channel)][curv])

            df = pd.DataFrame(curve.T,columns=['time','ydata'])
            df.ydata = df.ydata/df.ydata.sum()

            adjusted = adjust_curves(df, pd.Series(XS).to_frame())

            
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

            adjusted = adjust_curves(df, pd.Series(XS).to_frame())

            
            curve=adjusted.ydata.values
            
            


            

            CURVES[curv]=curve










            

        if if_afterpulse:
            afterpulse = 1/np.unique(xs).size
            afterpulse = np.array([afterpulse for i in CURVES[cname]])
            CURVES['Afterpulsing and background']=afterpulse
        else:
            pass

    return CURVES





def print_val(sender):
    pass

    
    
    
    




def query_ch1(sender,app_data,user_data):
        global sindatax1, sindatay1
        
        
        
        
        
        if app_data[0]<min(sindatax1) and app_data[1]<max(sindatax1):
            
            dpg.set_axis_limits("xaxis_chan1_zoom", min(sindatax1), app_data[1])
            dpg.set_value('bottom_limit_ch1',min(sindatax1))
            dpg.set_value('upper_limit_ch1',app_data[1])
        elif app_data[0]<min(sindatax1) and app_data[1]>max(sindatax1):
            dpg.set_axis_limits("xaxis_chan1_zoom", min(sindatax1), max(sindatax1))
            dpg.set_value('bottom_limit_ch1',min(sindatax1))
            dpg.set_value('upper_limit_ch1',max(sindatax1))
        elif app_data[0]>=min(sindatax1) and app_data[1]>max(sindatax1):
            dpg.set_axis_limits("xaxis_chan1_zoom", app_data[0], max(sindatax1))
            dpg.set_value('bottom_limit_ch1',app_data[0])
            dpg.set_value('upper_limit_ch1',max(sindatax1))
        elif app_data[0]>=min(sindatax1) and app_data[1]<=max(sindatax1):
            dpg.set_axis_limits("xaxis_chan1_zoom", app_data[0], app_data[1])
            dpg.set_value('bottom_limit_ch1',app_data[0])
            dpg.set_value('upper_limit_ch1',app_data[1])
        else:
            pass
        
        






def query_ch2(sender,app_data,user_data):
        global sindatax2, sindatay2
        
        
        if app_data[0]<min(sindatax2) and app_data[1]<max(sindatax2):
            
            dpg.set_axis_limits("xaxis_chan2_zoom", min(sindatax2), app_data[1])
            dpg.set_value('bottom_limit_ch2',min(sindatax2))
            dpg.set_value('upper_limit_ch2',app_data[1])
        elif app_data[0]<min(sindatax2) and app_data[1]>max(sindatax2):
            dpg.set_axis_limits("xaxis_chan2_zoom", min(sindatax2), max(sindatax2))
            dpg.set_value('bottom_limit_ch2',min(sindatax2))
            dpg.set_value('upper_limit_ch2',max(sindatax2))
        elif app_data[0]>=min(sindatax2) and app_data[1]>max(sindatax2):
            dpg.set_axis_limits("xaxis_chan2_zoom", app_data[0], max(sindatax2))
            dpg.set_value('bottom_limit_ch2',app_data[0])
            dpg.set_value('upper_limit_ch2',max(sindatax2))
        elif app_data[0]>=min(sindatax2) and app_data[1]<=max(sindatax2):
            dpg.set_axis_limits("xaxis_chan2_zoom", app_data[0], app_data[1])
            dpg.set_value('bottom_limit_ch2',app_data[0])
            dpg.set_value('upper_limit_ch2',app_data[1])
        else:
            pass
        
        





def remove_existing_filter_plots():
    existing_filter_plots = dpg.get_aliases()
    existing_filter_plots = [p for p in existing_filter_plots if p.startswith('tag_series_F_')]
    for p in existing_filter_plots:
        dpg.delete_item(p)

        
        


def remove_imported_curves_from_plot():
    cur = dpg.get_aliases()
    cur = [c for c in cur if 'tag_series_fltr_imported_' in c]
    
    for c in cur:
        dpg.delete_item(c)
    
    


def show_br_fltr_wndw(sender):
    global tchanx1,tchany1,tchanx2,tchany2
    global Tchanx1,Tchany1,Tchanx2,Tchany2
    global anal_file
    global bg_channel_marker
    global Btch_limit_ch_1,Utch_limit_ch_1,Btch_limit_ch_2,Utch_limit_ch_2
    global fl_bg_curadd_line_serieses_dict
    global tau_resolution
    global filtering_routine
    global curve_list
    global ntchannels

    dpg.set_value('tag_series_fltr', [[], []])
    dpg.set_value('tag_series_fltr_subtr', [[], []])
    dpg.configure_item("tag_series_fltr", label = '')
    dpg.configure_item("tag_series_fltr_subtr", label = '')
    
    dpg.hide_item("Background_RLL_line")
    dpg.hide_item("Background_RUL_line")
    dpg.hide_item('fltr_filters_plot')
    
    unmount_decay_table()
    unmount_LIB_decay_table()
    callback_Cancel_library_import('Cancel_library_import',None)
    remove_imported_curves_from_plot()
    remove_existing_filter_plots()
    
    dpg.set_value('add_bg_range', False)
    dpg.set_axis_limits("xaxis_tltr", 0 ,1)
    if sender == 'Remove_bgd_butt_ch_1':
        bg_channel_marker = 1
        the_channel = 'Channel 1'
        fl_bg_curves_dict[the_channel] = {anal_file:{
                                             'name':'(Ch1) '+anal_file.split('/')[-1],
                                             'file_path':anal_file,
                                            'TCSPC_resolution':int(np.round(tau_resolution*1e-9*1e12)),
                                            'TCSPC_channels':ntchannels,
                                             'Tchanx1' : Tchanx1,
                                             'Tchany1' : Tchany1,
                                             'tchanx1' : tchanx1,
                                             'tchany1' : tchany1,
                                             'Btch_limit_ch_1': Btch_limit_ch_1,
                                             'Utch_limit_ch_1': Utch_limit_ch_1,
                                             'subtract_bg':{
                                                  'tchanx1' : [],
                                                  'tchany1' : []
                                                             }
                                                     }
                                          
                                         }
        

        dpg.set_value('get_channel',the_channel)
        dpg.set_value('get_tcspc_resolution',int(np.round(tau_resolution*1e-9*1e12)))


        
        ys = tchany1/np.sum(tchany1)


        minimum = min(abs(ys[np.where(ys!=0)[0]]))/2
        
        dpg.set_value('tag_series_fltr', [tchanx1*tau_resolution-(tchanx1*tau_resolution)[0], ys])
        dpg.set_axis_limits("xaxis_tltr", Btch_limit_ch_1*tau_resolution-(tchanx1*tau_resolution)[0] ,Utch_limit_ch_1*tau_resolution-(tchanx1*tau_resolution)[0])
        dpg.set_axis_limits("yaxis_tltr", minimum ,max(ys)*2)
        

        curve_list =[]
        for k in fl_bg_curves_dict['Channel 1'].keys():
            name = fl_bg_curves_dict['Channel 1'][k]['name']
            len_subtr_y = len(fl_bg_curves_dict['Channel 1'][k]['tchany1'])
            
            if name == 'Subtracted':
                if len_subtr_y == 0:
                    
                    
                    pass
            else:
                
                
                curve_list.append(name)
                
        
        mount_decay_table(curve_list)
        

        tau_resolution
        
    elif sender == 'Remove_bgd_butt_ch_2':
        bg_channel_marker = 2
        the_channel = 'Channel 2'
        fl_bg_curves_dict[the_channel] = {anal_file:{
                                         'name':'(Ch2) '+anal_file.split('/')[-1],
                                         'file_path':anal_file,
                                        'TCSPC_resolution':int(np.round(tau_resolution*1e-9*1e12)),
                                        'TCSPC_channels':ntchannels,
                                         'Tchanx2' : Tchanx2,
                                         'Tchany2' : Tchany2,
                                         'tchanx2' : tchanx2,
                                         'tchany2' : tchany2,
                                         'Btch_limit_ch_2': Btch_limit_ch_2,
                                         'Utch_limit_ch_2': Utch_limit_ch_2,
                                        'subtract_bg':{
                                              'tchanx2' : [],
                                              'tchany2' : []
                                                         }
                                                }
                                          
                                         }
        dpg.set_value('get_channel',the_channel)
        dpg.set_value('get_tcspc_resolution',int(np.round(tau_resolution*1e-9*1e12)))
        

        
        
        ys = tchany2/np.sum(tchany2)
        minimum = min(abs(ys[np.where(ys!=0)[0]]))/2
        dpg.set_value('tag_series_fltr', [tchanx2*tau_resolution-(tchanx2*tau_resolution)[0], ys])
        dpg.set_axis_limits("xaxis_tltr", Btch_limit_ch_2*tau_resolution-(tchanx2*tau_resolution)[0] ,Utch_limit_ch_2*tau_resolution-(tchanx2*tau_resolution)[0])
        dpg.set_axis_limits("yaxis_tltr", minimum ,max(ys)*2)
        
        
        curve_list =[]
        for k in fl_bg_curves_dict['Channel 2'].keys():
            name = fl_bg_curves_dict['Channel 2'][k]['name']
            len_subtr_y = len(fl_bg_curves_dict['Channel 2'][k]['tchany2'])
            
            if name == 'Subtracted':
                if len_subtr_y == 0:
                    
                    
                    pass
            else:
                
                
                curve_list.append(name)
        mount_decay_table(curve_list)
        
    unmount_filter_list_table(bg_channel_marker)
    dpg.configure_item("tag_series_fltr", label = 'Decay')
    dpg.show_item('BG_removal_window')
    
    
    
    
    
    
    
    
    
    
    
    

    


def show_error(TEXT):
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
                       callback=callback_ERROR_dialog_close
                      )
        dpg.bind_item_theme('No_data_files', 'Error_window_theme')
    except:
        dpg.show_item('ERROR')



def unmount_LIB_decay_table():
    rows = dpg.get_aliases()
    
    rows = [r for r in rows if r.startswith('decays_lib_tab_row_')]
    

    for r in rows:
        dpg.delete_item(r)
    dpg.hide_item('decays_tab_lib_list_tag')
                


def unmount_decay_table():
    
    rows = dpg.get_aliases()
    
    rows = [r for r in rows if r.startswith('decays_tab_row_')]
    
    for r in rows:
        dpg.delete_item(r)
        


def unmount_filter_list_table(channel):
    rows = dpg.get_aliases()
    rows = [r for r in rows if r.startswith('filters_ch_'+str(channel)+'_tab_list_row_')]
    for r in rows:
        dpg.delete_item(r)
        
        
        
        
        


def unmount_status_modal():
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
    
    
    

