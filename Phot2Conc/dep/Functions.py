'''Sorted functions'''
resizable_items = ['mvAppItemType::mvWindowAppItem',
                   'mvAppItemType::mvFileDialog',
                   'mvAppItemType::mvListbox',
                   'mvAppItemType::mvDragFloat',
                   'mvAppItemType::mvDragInt',
                   'mvAppItemType::mvButton',
                   'mvAppItemType::mvSliderFloat',
                   'mvAppItemType::mvGroup',
                   'mvAppItemType::mvSubPlots',
                   'mvAppItemType::mvDrawImage',
                   'mvAppItemType::mvInputFloat',
                   'mvAppItemType::mvDrawlist',
                   'mvAppItemType::mvInputText',
                   'mvAppItemType::mvDynamicTexture',
                   
                  ]
resizable_width = ['mvAppItemType::mvListbox',
                   'mvAppItemType::mvDragFloat',
                   'mvAppItemType::mvDragInt',
                   'mvAppItemType::mvButton',
                   'mvAppItemType::mvSliderFloat',
                   'mvAppItemType::mvGroup',
                   'mvAppItemType::mvInputFloat',
                   'mvAppItemType::mvDrawlist',
                   'mvAppItemType::mvInputText',
                   'mvAppItemType::mvDynamicTexture'
                  ]

file_panel_items = [
                    'file_box',
    'Browse_directory_button',
    'Brightness_input_ch_1',
    'Brightness_err_input_ch_1',
    'Brightness_input_ch_2',
    'Brightness_err_input_ch_2',
    'Load_calib_button',
    'Save_calib_button',
    'omega_input_ch_1',
    'omega_err_input_ch_1',
    'kappa_input_ch_1',
    'kappa_err_input_ch_1',
    'focal_vol_input_ch_1',
    'focal_vol_err_input_ch_1',
    'omega_input_ch_2',
    'omega_err_input_ch_2',
    'kappa_input_ch_2',
    'kappa_err_input_ch_2',
    'focal_vol_input_ch_2',
    'focal_vol_err_input_ch_2',
    'Add_ROI_1_button',
    'Add_ROI_2_button',
    'Browse_ROI_directory_button',
    'Pixel_dwell_output',
    'Nframes_output',
    'Resolution_output',
    'Pixel_size_output',
    'Calculate_button',
    'Calculate_all_button',
    'sinle_phot_output_ch_1',
    'sinle_phot_err_output_ch_1',
    'sinle_mols_output_ch_1',
    'sinle_mols_err_output_ch_1',
    'single_conc_output_ch_1',
    'single_conc_err_output_ch_1',
    'empty_output_ch_1',
    'empty_err_output_ch_1',
    'sinle_phot_output_ch_2',
    'sinle_phot_err_output_ch_2',
    'sinle_mols_output_ch_2',
    'sinle_mols_err_output_ch_2',
    'single_conc_output_ch_2',
    'single_conc_err_output_ch_2',
    'empty_output_ch_2',
    'empty_err_output_ch_2',
    'add_to_res_single_button',
    'Export_all_button']
image_panel_items = []
dialogs = ['file_dialog_id','PTU_file_dialog_id']
global ratio_w,ratio_h
ratio_w = ratio_h = 1


log_it('Functions.py -loaded on '+str(datetime.datetime.now()),'a')


def CNTR_FIT(x,SLOPE):
    
    CNTS_SUM = SLOPE*x
    return CNTS_SUM



def CNTR_itercept_FIT(x,SLOPE,itercept):
    
    CNTS_SUM = SLOPE*x+itercept
    return CNTS_SUM



def CONC(N,V,N_err,V_err):
    
    Na = 6.022e23
    C = N/(Na*V)
    C_err = sqrt(((N**2)*(V_err**2))/((Na**2)*(V**4))+(N_err**2)/((Na**2)*(V**2)))
    return C, C_err




def CPMPS(direct,file,DF):
    
    TT_file_path = os.path.join(direct,file)
    tt_data = pd.read_csv(TT_file_path,skiprows=2,sep='\t',header=None)
    tt_data.columns = ['Time','Cnts','W1','W2']
    tt_data.drop(['W1','W2'],axis=1,inplace=True)

    test = pd.read_csv(TT_file_path,skiprows=1,sep='\t',header=None,low_memory=False)
    if '[kCnts]' in ''.join(str(test.head(1)[1].values)):
        tt_data['Cnts'] = (tt_data.Cnts*1000).astype(int)
    ss_limit = int(0.15*len(tt_data.Cnts))
    
    start = tt_data.Cnts[:ss_limit].mean()
    stop = tt_data.Cnts[-ss_limit:].mean()
    st_ratio = start/stop
    
    if st_ratio <1.15:
        my_model = Model(CNTR_FIT)
        xdata = tt_data.Time
        ydata = tt_data.Cnts.cumsum()
        
        slope = 1
        fit_results = my_model.fit(ydata, SLOPE=slope, x=xdata)
        cntr=fit_results.best_values['SLOPE']
        
        
    else:
        my_model = Model(CNTR_itercept_FIT)
        xdata = tt_data.Time[-2*ss_limit:]
        ydata = tt_data.Cnts[-2*ss_limit:].cumsum()
        
        slope = 1
        itercept = 0
        fit_results = my_model.fit(ydata, SLOPE=slope,itercept = itercept, x=xdata)
        cntr=fit_results.best_values['SLOPE']
        itercept=fit_results.best_values['itercept']
        
        
    fcs_file = file.replace('_TT_','_curve_')
    
    dataq=DF.query("file =='"+fcs_file+"'")
    
    
    
    NP = float(dataq.N_p.values)
    
    Brightness = np.round(cntr/NP)
    
    return Brightness


def Exception(tried):
    function_name = sys._getframe(0).f_code.co_name
    log_it('\tException in function '+str(function_name)+ ' while trying: '+tried,'a')
    
    

def Export_result_dataframe_to_file(sender,app_data):
    global directory, new_directory,last_directory
    # print(app_data)
    directory = app_data['current_path']
    new_directory=directory
    last_directory=directory
    update_dialogs_default_directory(last_directory)
    
    global Sing_Results_DF
    
    filtr = app_data['current_filter']
    
    if filtr == '':
        fnam = app_data['file_name']
        filtr = '.'+fnam.split('.')[1]
    
    if filtr == '.xlsx' :
        path = app_data['file_path_name']
        
        
        
        Sing_Results_DF.to_excel(path,index=False)
    elif filtr == '.dat' :
        path = app_data['file_path_name']
        
        
        
        Sing_Results_DF.to_csv(path,sep='\t',index=False)
    elif filtr == '.csv' :
        path = app_data['file_path_name']
        
        
        
        Sing_Results_DF.to_csv(path,index=False)
    else:
        path = app_data['file_path_name']
        
        
        
        Sing_Results_DF.to_pickle(path)
        
        
        


def Load_Save_Calib_file(sender,app_data,user_data):
    global directory, new_directory,last_directory,calib_directory
    # print(app_data)
    directory = app_data['current_path']
    new_directory=directory
    last_directory=directory
    update_dialogs_default_directory(last_directory)
    
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
                Exception("len_kappa = len(data[k0]['kappa'])")

            try:
                len_omega = len(data[k0]['omega'])
            except:
                Exception("len_omega = len(data[k0]['omega'])")

            try:
                len_V0= len(data[k0]['V0'])
            except:
                Exception("len_V0= len(data[k0]['V0'])")

            try:
                len_Bright= len(data[k0]['Mol.Brightness'])
            except:
                Exception("len_Bright= len(data[k0]['Mol.Brightness'])")


            if (len_kappa==2) and (len_omega==2) and (len_V0 == 2) and (len_Bright ==2):

                if k0 == 'Channel_1':
                    dpg.set_value('omega_input_ch_1',data[k0]['omega'][0])
                    dpg.set_value('omega_err_input_ch_1',data[k0]['omega'][1])

                    dpg.set_value('kappa_input_ch_1',data[k0]['kappa'][0])
                    dpg.set_value('kappa_err_input_ch_1',data[k0]['kappa'][1])

                    dpg.set_value('focal_vol_input_ch_1',data[k0]['V0'][0])
                    dpg.set_value('focal_vol_err_input_ch_1',data[k0]['V0'][1])

                    dpg.set_value('Brightness_input_ch_1',data[k0]['Mol.Brightness'][0])
                    dpg.set_value('Brightness_err_input_ch_1',data[k0]['Mol.Brightness'][1])

                elif k0 == 'Channel_2':

                    dpg.set_value('omega_input_ch_2',data[k0]['omega'][0])
                    dpg.set_value('omega_err_input_ch_2',data[k0]['omega'][1])

                    dpg.set_value('kappa_input_ch_2',data[k0]['kappa'][0])
                    dpg.set_value('kappa_err_input_ch_2',data[k0]['kappa'][1])

                    dpg.set_value('focal_vol_input_ch_2',data[k0]['V0'][0])
                    dpg.set_value('focal_vol_err_input_ch_2',data[k0]['V0'][1])

                    dpg.set_value('Brightness_input_ch_2',data[k0]['Mol.Brightness'][0])
                    dpg.set_value('Brightness_err_input_ch_2',data[k0]['Mol.Brightness'][1])

                else:
                    pass
            elif (len_kappa==0) and (len_omega==0) and (len_V0 == 0) and (len_Bright ==0):
                pass

            else:
                pass
        
    elif user_data == 'Save_calib_button':  
        path_to_json_file = app_data['file_path_name']
        calib_directory = path_to_json_file
        omega_1 = [dpg.get_value('omega_input_ch_1'),dpg.get_value('omega_err_input_ch_1')]
        kappa_1 = [dpg.get_value('kappa_input_ch_1'),dpg.get_value('kappa_err_input_ch_1')]
        V0_1 = [dpg.get_value('focal_vol_input_ch_1'),dpg.get_value('focal_vol_err_input_ch_1')]
        bright_1 = [dpg.get_value('Brightness_input_ch_1'),dpg.get_value('Brightness_err_input_ch_1')]
        
        omega_2 = [dpg.get_value('omega_input_ch_2'),dpg.get_value('omega_err_input_ch_2')]
        kappa_2 = [dpg.get_value('kappa_input_ch_2'),dpg.get_value('kappa_err_input_ch_2')]
        V0_2 = [dpg.get_value('focal_vol_input_ch_2'),dpg.get_value('focal_vol_err_input_ch_2')]
        bright_2 = [dpg.get_value('Brightness_input_ch_2'),dpg.get_value('Brightness_err_input_ch_2')]
        
        
        output_dict = {'Channel_1':{'omega':omega_1,
                                    'kappa':kappa_1,
                                    'V0':V0_1,
                                    'Mol.Brightness':bright_1
                                   },
                       'Channel_2':{'omega':omega_2,
                                    'kappa':kappa_2,
                                    'V0':V0_2,
                                    'Mol.Brightness':bright_2
                                   }
                      }
        
        with open(path_to_json_file, 'w') as f:
            json.dump(output_dict, f, indent=4, sort_keys=False)
        
            
            
            
            






def VEFF(w,k,w_err,k_err):
    
    
    V = (pi**(3/2))*(w**3)*k
    V_err = sqrt(9*(k**2)*(pi**3)*(w**4)*(w_err**2)+(k_err**2)*(pi**3)*(w**6))
    return V, V_err



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





def add_single_result_to_DF(sender,app_data):
    
    
    global Sing_Results_DF,anal_file,pck_list
    global Current_image_1,Current_image_2,Channels
    global mean_Molecules_ch_1,std_Molecules_ch_1,mean_Concentration_ch_1,std_Concentration_ch_1,std_err_Concentration_ch_1,median_C_ch_1,median_err_C_ch_1,mean_Molecules_err_ch_1,mean_Concentration_err_ch_1,mean_Photons_ch_1,mean_Photons_err_ch_1
    global mean_Molecules_ch_2,std_Molecules_ch_2,mean_Concentration_ch_2,std_Concentration_ch_2,std_err_Concentration_ch_2,median_C_ch_2,median_err_C_ch_2,mean_Molecules_err_ch_2,mean_Concentration_err_ch_2,mean_Photons_ch_2,mean_Photons_err_ch_2
    stored_results = Sing_Results_DF.File.values
    if anal_file in stored_results:
        Sing_Results_DF.File=Sing_Results_DF.File.where(Sing_Results_DF.File!=anal_file)
        Sing_Results_DF.dropna(inplace=True)
    else:
        pass
    if len(Channels) == 1:
    
        
        if '1' in Channels[0]:
            Sing_Results_DF_tmp = pd.DataFrame([[anal_file,
                                                 1,
                                                 mean_Photons_ch_1,
                                                 mean_Photons_err_ch_1,
                                                 mean_Molecules_ch_1,
                                                 mean_Molecules_err_ch_1,
                                                 mean_Concentration_ch_1,
                                                 mean_Concentration_err_ch_1,
                                                 
                                                     median_C_ch_1,
                                                     median_err_C_ch_1]],columns=Sing_Results_DF.columns)
        elif '2' in Channels[0]:
            Sing_Results_DF_tmp = pd.DataFrame([
                                               [anal_file,
                                             2,
                                             mean_Photons_ch_2,
                                             mean_Photons_err_ch_2,
                                             mean_Molecules_ch_2,
                                             mean_Molecules_err_ch_2,
                                             mean_Concentration_ch_2,
                                             mean_Concentration_err_ch_2,
                                                
                                                     median_C_ch_2,
                                                     median_err_C_ch_2]],columns=Sing_Results_DF.columns)
        else:
            pass
    if len(Channels) == 2:
        Sing_Results_DF_tmp = pd.DataFrame([[anal_file,
                                             1,
                                             mean_Photons_ch_1,
                                             mean_Photons_err_ch_1,
                                             mean_Molecules_ch_1,
                                             mean_Molecules_err_ch_1,
                                             mean_Concentration_ch_1,
                                             mean_Concentration_err_ch_1,
                                                 
                                                     median_C_ch_1,
                                                     median_err_C_ch_1],
                                               [anal_file,
                                             2,
                                             mean_Photons_ch_2,
                                             mean_Photons_err_ch_2,
                                             mean_Molecules_ch_2,
                                             mean_Molecules_err_ch_2,
                                             mean_Concentration_ch_2,
                                             mean_Concentration_err_ch_2,
                                                 
                                                     median_C_ch_2,
                                                     median_err_C_ch_2]],columns=Sing_Results_DF.columns)
    
    
    
    Sing_Results_DF=pd.concat([Sing_Results_DF,Sing_Results_DF_tmp]).reset_index(drop=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


def calc_molecules(DF,PTU_Px_dwell,PTU_N_frames,brightness,brightness_err):
    
    PTU_Px_dwell = PTU_Px_dwell*1e-6
    MOL = ( DF*(1/(PTU_Px_dwell*PTU_N_frames)))/brightness
    part_BR = -DF/(PTU_N_frames*PTU_Px_dwell*(brightness**2))
    MOL_err = sqrt((part_BR**2)*(brightness_err**2))
    return MOL,MOL_err




def callback_Brightness_err_input(sender,app_data):
    
    
    global FCS_results_ch_1,FCS_results_ch_2
    global mean_brightness_ch_1, mean_brightness_err_ch_1
    if sender == 'Brightness_err_input_ch_1':
        mean_brightness_err_ch_1  = app_data
        FCS_results_ch_1 = pd.DataFrame()
        



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
    else:
        mean_brightness_err_ch_1  = app_data
        FCS_results_ch_1 = pd.DataFrame()
        



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
    
    
    
    


def callback_Brightness_input(sender,app_data):
    
    
    global FCS_results_ch_1,FCS_results_ch_2
    global mean_brightness_ch_1, mean_brightness_err_ch_1,mean_brightness_ch_2, mean_brightness_err_ch_2
    if sender == 'Brightness_input_ch_1':
        mean_brightness_ch_1  = app_data
        FCS_results_ch_1 = pd.DataFrame()
        





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
    else:
        mean_brightness_ch_1  = app_data
        FCS_results_ch_1 = pd.DataFrame()
        





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
    


def callback_Keyword_key(sender,app_data):
    files = dpg.get_item_configuration('file_box')['items']
    up_key = dpg.mvKey_Up
    down_key = dpg.mvKey_Down
    
    if len(files)!=0:
        def_val = dpg.get_value('file_box')
        index = files.index(def_val)
    
        if app_data == up_key:
            if index!=0:
                index=index-1
                dpg.set_value('file_box',files[index])
                callback_listbox('file_box',files[index])
            else:
                pass
        if app_data == down_key:
            if index!=len(files)-1:
                index=index+1
                dpg.set_value('file_box',files[index])
                callback_listbox('file_box',files[index])
            else:
                pass
            



def callback_PTU_directory_select(sender,app_data):
    
    
    
    
    
    
    
    
    
    
    global directory, files,new_directory,last_directory,anal_file,pck_files,PTU_directory
    global sync_rate,pixel_dwell, number_of_frames
    global Sing_Results_DF,ratio_w
    Sing_Results_DF = pd.DataFrame(columns=['File', 'Channel','<Counts>','Counts_std','<N_p>','N_p_err','<C>', 'C_err','C_median', 'C_median_abs_err'])

    files=()
    dpg.set_value('AUTO_ROI_checkbox',False)
    
    directory = app_data['file_path_name']
    new_directory=directory
    PTU_directory = directory
    last_directory=directory
    update_dialogs_default_directory(last_directory)
    files = tuple(np.sort([f for f in os.listdir(PTU_directory) if f.endswith('.ptu')]))
    pck_files = list(np.sort([f for f in os.listdir(PTU_directory) if f.endswith('.pck')]))
    
    
    try:
        hide_histograms()
    except:
        pass
    filenames = [f.replace('.ptu','') for f in files]
    if len(files)==0:
        show_error_no_files('No PTU files found.')
    else:
        
        stop=False
        
        
        
        
        

















        
        
        
        
        
        
        for file in filenames:
            
            
            
            
            
            ptufile = file+'.ptu'
            for f in pck_files:
                if file in f:
                    stop = True
                    ffile = file
                    break
                else:
                    stop = False
                    
                    
            
            if stop:
                pass
            else:
                show_error_no_files('No .pck files found. Run the PTU2pck.py script and try again. Mising file: '+ffile)
                
                try:
                    pass
                    
                except:
                    pass
                
                














































                    

                    
                    
        
        
        
        
        
        
        
            
                
    
    if len(pck_files)!=0:
        update_flist(filenames)


        anal_file=filenames[0]
        dpg.configure_item('file_box', default_value=anal_file)

        load_PTU_images(anal_file)
        
    else:
        
        show_error_no_files('No .pck files found. Run the PTU2pck.py script and try again.')
    
    
    
    
    
    



    




        








    




    






def callback_ROI_directory_select(sender,app_data):
    global ROI_directory,last_directory
    
    
    ROI_directory = app_data['file_path_name']
    last_directory =ROI_directory
    update_dialogs_default_directory(last_directory)
    dpg.set_value('AUTO_ROI_checkbox',True)
    callback_select_roi('AUTO_ROI_checkbox',True)
    
    
    
        

    
    


def callback_TT_directory_select(sender,app_data):
    global directory, files,new_directory,last_directory,anal_file
    global TT_directory,FCS_results_ch_1,FCS_results_ch_2
    
    directory = app_data['file_path_name']
    TT_directory = directory
    new_directory=directory
    last_directory=new_directory
    update_dialogs_default_directory(last_directory)
    if sender == 'TT_file_dialog_id_ch_1':
        
        
        
        
        
        
        pickle_files = tuple(np.sort([f for f in os.listdir(directory) if f.endswith('.pickle')]))
        
        TT_files = list(tuple(np.sort([f for f in os.listdir(directory) if ('TT'in f) and (f.endswith('.dat'))])))
        
        
        if len(pickle_files)==0:
            show_error_no_files('No "pickle" files found.')
        else:
            pass
        if len(TT_files)==0:
            show_error_no_files('No timetrace files found.')
        else:
            pass
        FCS_results_ch_1 = pd.DataFrame()
        for pickle in pickle_files:
            FCS_results_ch_1 = pd.concat([FCS_results_ch_1,pd.read_pickle(os.path.join(TT_directory,pickle))[['file','N_p']]])
        FCS_results_ch_1.reset_index(drop=True,inplace=True)        

        FCS_files=list(FCS_results_ch_1.file.values)
        compare_lists=[]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        FCS_files = [f.replace('_curve_','_TT_') for f in FCS_files]
        
        compare_lists  = list(set([x for x in TT_files + FCS_files if x in TT_files and x  in FCS_files]))
        
        
        compare_lists.sort()
        
        
        
        FCS_results_ch_1['Brightness']=np.nan
        for file in compare_lists:
            
            fcs_file = file.replace('_TT_','_curve_')
            

            Brightness = CPMPS(TT_directory,file,FCS_results_ch_1)
            
            ind = int(FCS_results_ch_1.query("file =='"+fcs_file+"'").index.values)
            
            FCS_results_ch_1.at[ind,'Brightness'] = Brightness
        FCS_results_ch_1.dropna(inplace=True)
        FCS_results_ch_1.reset_index(drop=True,inplace=True)
        

        mean_bright_input_ch_1()


        dpg.configure_item('Show_brightness_results_button_ch_1',enabled=True)
        try:
            mount_bright_table(sender)




































        except:
            unmount_bright_table(sender)
            mount_bright_table(sender)
    else:
        
        
        
        pickle_files = tuple(np.sort([f for f in os.listdir(directory) if f.endswith('.pickle')]))
        TT_files = list(tuple(np.sort([f for f in os.listdir(directory) if ('TT'in f) and (f.endswith('.dat'))])))
        
        
        if len(pickle_files)==0:
            show_error_no_files('No "pickle" files found.')
        else:
            pass
        if len(TT_files)==0:
            show_error_no_files('No timetrace files found.')
        else:
            pass
        FCS_results_ch_2 = pd.DataFrame()
        for pickle in pickle_files:
            FCS_results_ch_2 = pd.concat([FCS_results_ch_2,pd.read_pickle(os.path.join(TT_directory,pickle))[['file','N_p']]])
        FCS_results_ch_2.reset_index(drop=True,inplace=True)        
        
        FCS_files=list(FCS_results_ch_2.file.values)
        FCS_files = [f.replace('_curve_','_TT_') for f in FCS_files]
        
        compare_lists  = list(set([x for x in TT_files + FCS_files if x in TT_files and x  in FCS_files]))
        compare_lists.sort()
        
        FCS_results_ch_2['Brightness']=np.nan
        for file in compare_lists:
            
            fcs_file = file.replace('_TT_','_curve_')
            

            Brightness = CPMPS(TT_directory,file,FCS_results_ch_2)
            
            ind = int(FCS_results_ch_2.query("file =='"+fcs_file+"'").index.values)
            
            FCS_results_ch_2.at[ind,'Brightness'] = Brightness
        FCS_results_ch_2.dropna(inplace=True)
        FCS_results_ch_2.reset_index(drop=True,inplace=True)
        

        mean_bright_input_ch_2()


        dpg.configure_item('Show_brightness_results_button_ch_2',enabled=True)
        try:
            mount_bright_table(sender)




































        except:
            unmount_bright_table(sender)
            mount_bright_table(sender)
    
    



    


def callback_add_ROI(sender,app_data):
    
    
    dpg.configure_item("Select_ROI_dialog",user_data = sender)
    dpg.show_item("Select_ROI_dialog")

    


def callback_auto_adjust(sender,app_data):

    # global mouse_down
    
    # if not mouse_down:
        callback_windows_size(sender,app_data)
        callback_font_size(sender,app_data)
    # else:
    #     pass









def callback_calculate(sender,app_data):
    cmap = 'afmhot'
    rect = 0.1, 0.1, 0.85, 0.9

    norm = None
    global DF,DF2,anal_file,PTU_directory,pck_list
    global mean_Molecules_ch_1,std_Molecules_ch_1,mean_Concentration_ch_1,std_Concentration_ch_1,std_err_Concentration_ch_1,median_C_ch_1,median_err_C_ch_1,mean_Molecules_err_ch_1,mean_Concentration_err_ch_1,mean_Photons_ch_1,mean_Photons_err_ch_1
    global mean_Molecules_ch_2,std_Molecules_ch_2,mean_Concentration_ch_2,std_Concentration_ch_2,std_err_Concentration_ch_2,median_C_ch_2,median_err_C_ch_2,mean_Molecules_err_ch_2,mean_Concentration_err_ch_2,mean_Photons_ch_2,mean_Photons_err_ch_2
    global Current_image_1,Current_image_2,Channels
    
    
    mean_Molecules_ch_1=std_Molecules_ch_1=mean_Concentration_ch_1=std_Concentration_ch_1=std_err_Concentration_ch_1=median_C_ch_1=median_err_C_ch_1=mean_Photons_ch_1=mean_Photons_err_ch_1=None
    mean_Molecules_ch_2=std_Molecules_ch_2=mean_Concentration_ch_2=std_Concentration_ch_2=std_err_Concentration_ch_2=median_C_ch_2=median_err_C_ch_2=mean_Photons_ch_2=mean_Photons_err_ch_2=None
    
    global PTU_N_frames,PTU_Px_dwell
    
    
    
    
    
    
    if len(Channels) == 1:
        
        if '1' in Channels[0]:
            brightness_ch_1 = dpg.get_value('Brightness_input_ch_1')
            brightness_err_ch_1 = dpg.get_value('Brightness_err_input_ch_1') 
            Veff_ch_1 = 1e-15*dpg.get_value('focal_vol_input_ch_1')
            Veff_err_ch_1 = 1e-15*dpg.get_value('focal_vol_err_input_ch_1')
            DF = Current_image_1[0]
            Photons_1 = pd.DataFrame(DF)
            n_pixels_1 =  Photons_1.stack().reset_index(drop=True).dropna().count()
            
            Molecules_ch_1 = calc_molecules(DF,PTU_Px_dwell,PTU_N_frames,brightness_ch_1,brightness_err_ch_1)[0]
            Molecules_err_ch_1 = calc_molecules(DF,PTU_Px_dwell,PTU_N_frames,brightness_ch_1,brightness_err_ch_1)[1]
            Concentration_ch_1 = 1e9*CONC(Molecules_ch_1,Veff_ch_1,Molecules_err_ch_1,Veff_err_ch_1)[0]
            Concentration_err_ch_1 = 1e9*CONC(Molecules_ch_1,Veff_ch_1,Molecules_err_ch_1,Veff_err_ch_1)[1]
            
            
            
            mean_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().mean()
            
            mean_Photons_err_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
            mean_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().mean()
            
            if not dpg.get_value('Error_type_checkbox'):
                mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1).stack().reset_index(drop=True).dropna().mean()
            else:
                mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
            
            
            mean_Concentration_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().mean()
            if not dpg.get_value('Error_type_checkbox'):
                mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1).stack().reset_index(drop=True).dropna().mean()
            else:
                mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
            
            
            median_C_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().median()
            median_err_C_ch_1 = median_abs_deviation(pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna())
            
            dpg.set_value('sinle_phot_output_ch_1',mean_Photons_ch_1)
        
            dpg.set_value('sinle_phot_err_output_ch_1',mean_Photons_err_ch_1)
            dpg.set_value('sinle_mols_output_ch_1',mean_Molecules_ch_1)
            
            dpg.set_value('sinle_mols_err_output_ch_1',mean_Molecules_err_ch_1)
            dpg.set_value('single_conc_output_ch_1',mean_Concentration_ch_1)
            
            dpg.set_value('single_conc_err_output_ch_1',mean_Concentration_err_ch_1)
            Molecules_ch_1 = pd.DataFrame(Molecules_ch_1)
            Concentration_ch_1 = pd.DataFrame(Concentration_ch_1)
            
            Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1)
            Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1)
            
            
            
            Phot_hist_ch_1,Phot_bins_ch_1 =np.histogram(Photons_1.stack().reset_index(drop=True).dropna().values,
                                                        density=True,bins='auto')
            Phot_bins_ch_1=Phot_bins_ch_1[:-1]
            median_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().median()
            
            Mols_hist_ch_1,Mols_bins_ch_1 =np.histogram(pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().values
                                                        ,density=True,bins='auto')
            Mols_bins_ch_1=Mols_bins_ch_1[:-1]
            median_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().median()
            
            Conc_hist_ch_1,Conc_bins_ch_1 =np.histogram(pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().values
                                                        ,density=True,bins='auto')
            Conc_bins_ch_1=Conc_bins_ch_1[:-1]
            
            ind=np.where(Conc_hist_ch_1!=0)[0]
            
            Conc_hist_ch_1=Conc_hist_ch_1[ind]
            Conc_bins_ch_1=Conc_bins_ch_1[ind]
            
            ind=np.where(Mols_hist_ch_1!=0)[0]
            
            Mols_hist_ch_1=Mols_hist_ch_1[ind]
            Mols_bins_ch_1=Mols_bins_ch_1[ind]
            
            ind=np.where(Phot_hist_ch_1!=0)[0]
            
            Phot_hist_ch_1=Phot_hist_ch_1[ind]
            Phot_bins_ch_1=Phot_bins_ch_1[ind]
            
            dpg.set_value('c_dist_ser_ch_1',(Conc_bins_ch_1,Conc_hist_ch_1))
            dpg.set_value('c_mean_ser_ch_1',(np.array([mean_Concentration_ch_1]),np.array([max(Conc_hist_ch_1)])))
            dpg.set_value('c_med_ser_ch_1',(np.array([median_C_ch_1]),np.array([max(Conc_hist_ch_1)])))
            dpg.set_axis_limits('hist_xc_axis_ch1', min(Conc_bins_ch_1), max(Conc_bins_ch_1))
            dpg.set_axis_limits('hist_yc_axis_ch1', 0, max(Conc_hist_ch_1))
            
            dpg.set_value('np_dist_ser_ch_1',(Mols_bins_ch_1,Mols_hist_ch_1))
            dpg.set_value('np_mean_ser_ch_1',(np.array([mean_Molecules_ch_1]),np.array([max(Mols_hist_ch_1)])))
            dpg.set_value('np_med_ser_ch_1',(np.array([median_Molecules_ch_1]),np.array([max(Mols_hist_ch_1)])))
            dpg.set_axis_limits('hist_xnp_axis_ch1', min(Mols_bins_ch_1), max(Mols_bins_ch_1))
            dpg.set_axis_limits('hist_ynp_axis_ch1', 0, max(Mols_hist_ch_1))
            
            dpg.set_value('phot_dist_ser_ch_1',(Phot_bins_ch_1,Phot_hist_ch_1))
            dpg.set_value('phot_mean_ser_ch_1',(np.array([mean_Photons_ch_1]),np.array([max(Phot_hist_ch_1)])))
            dpg.set_value('phot_med_ser_ch_1',(np.array([median_Photons_ch_1]),np.array([max(Phot_hist_ch_1)])))
            dpg.set_axis_limits('hist_xphot_axis_ch1', min(Phot_bins_ch_1), max(Phot_bins_ch_1))
            dpg.set_axis_limits('hist_yphot_axis_ch1', 0, max(Phot_hist_ch_1))
            
            dpg.configure_item('c_mean_ser_ch_1',label='Mean = '+str(np.round(mean_Concentration_ch_1,4)))
            dpg.configure_item('c_med_ser_ch_1',label='Median = '+str(np.round(median_C_ch_1,4)))
            
            dpg.configure_item('np_mean_ser_ch_1',label='Mean = '+str(np.round(mean_Molecules_ch_1,2)))
            dpg.configure_item('np_med_ser_ch_1',label='Median = '+str(np.round(median_Molecules_ch_1,2)))
            
            dpg.configure_item('phot_mean_ser_ch_1',label='Mean = '+str(np.round(mean_Photons_ch_1,1)))
            dpg.configure_item('phot_med_ser_ch_1',label='Median = '+str(np.round(median_Photons_ch_1,1)))
            
            
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
                phot_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Phot_ch_1.csv')
                
                Photons_1.to_csv(phot_array_path_ch_1,index=False,sep=',', header=None)
            else:
                pass
            
            if dpg.get_value('Np_array_checkbox'):
                Np_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_ch_1.csv')
                
                
                Molecules_ch_1.to_csv(Np_array_path_ch_1,index=False,sep=',', header=None)
                
                Np_err_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_err_ch_1.csv')
                Molecules_err_ch_1.to_csv(Np_err_array_path_ch_1,index=False,sep=',', header=None)
                
            else:
                pass
            if dpg.get_value('C_array_checkbox'):
                Conc_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_ch_1.csv')
                
                Concentration_ch_1.to_csv(Conc_array_path_ch_1,index=False,sep=',', header=None)
                
                Conc_err_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_err_ch_1.csv')
                Concentration_err_ch_1.to_csv(Conc_err_array_path_ch_1,index=False,sep=',', header=None)
                
            else:
                pass
            
            if dpg.get_value('Photons_Hmaps_checkbox'):
                phot_hmap_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Phot_HM_ch_1.png')

                fig = Figure(facecolor='white')

                ax = fig.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Photons_1.min().min(), vmax=Photons_1.max().max())
                ax.imshow(Photons_1,cmap =cmap)

                ax.axis('off')
                fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
                FigureCanvas(fig).print_png(phot_hmap_path_ch_1)
                
            else:
                pass
            
            if dpg.get_value('Np_Hmaps_checkbox'):
                Np_hmap_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_HM_ch_1.png')

                fig = Figure(facecolor='white')

                ax = fig.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Molecules_ch_1.min().min(), vmax=Molecules_ch_1.max().max())
                ax.imshow(Molecules_ch_1,cmap =cmap)

                ax.axis('off')
                fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
                FigureCanvas(fig).print_png(Np_hmap_path_ch_1)
                
            else:
                pass

            if dpg.get_value('C_Hmaps_checkbox'):
                C_hmap_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_HM_ch_1.png')
                fig = Figure(facecolor='white')
                ax = fig.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Concentration_ch_1.min().min(), vmax=Concentration_ch_1.max().max())
                ax.imshow(Concentration_ch_1,cmap =cmap)

                ax.axis('off')
                fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
                FigureCanvas(fig).print_png(C_hmap_path_ch_1)
                
            else:
                pass
        
        elif '2' in Channels[0]:
            brightness_ch_2 = dpg.get_value('Brightness_input_ch_2')
            brightness_err_ch_2 = dpg.get_value('Brightness_err_input_ch_2') 
            Veff_ch_2 = 1e-15*dpg.get_value('focal_vol_input_ch_2')
            Veff_err_ch_2 = 1e-15*dpg.get_value('focal_vol_err_input_ch_2')
            DF2 = Current_image_2[0]
            Photons_2 = pd.DataFrame(DF2)
            n_pixels_2 =  Photons_2.stack().reset_index(drop=True).dropna().count()
            
            mean_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().mean()
            mean_Photons_err_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
            Molecules_ch_2 = calc_molecules(DF2,PTU_Px_dwell,PTU_N_frames,brightness_ch_2,brightness_err_ch_2)[0]
            Molecules_err_ch_2 = calc_molecules(DF2,PTU_Px_dwell,PTU_N_frames,brightness_ch_2,brightness_err_ch_2)[1]
            
            
            
            
            Concentration_ch_2 = 1e9*CONC(Molecules_ch_2,Veff_ch_2,Molecules_err_ch_2,Veff_err_ch_2)[0]
            Concentration_err_ch_2 = 1e9*CONC(Molecules_ch_2,Veff_ch_2,Molecules_err_ch_2,Veff_err_ch_2)[1]
            
            mean_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().mean()
            if not dpg.get_value('Error_type_checkbox'):
                mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2).stack().reset_index(drop=True).dropna().mean()
            else:
                mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
            
            
            
            mean_Concentration_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().mean()
            if not dpg.get_value('Error_type_checkbox'):
                mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2).stack().reset_index(drop=True).dropna().mean()
            else:
                mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
            
            median_C_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().median()
            median_err_C_ch_2 = median_abs_deviation(pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna())
            dpg.set_value('sinle_phot_output_ch_2',mean_Photons_ch_2)
        
            dpg.set_value('sinle_phot_err_output_ch_2',mean_Photons_err_ch_2)
            dpg.set_value('sinle_mols_output_ch_2',mean_Molecules_ch_2)
            
            dpg.set_value('sinle_mols_err_output_ch_2',mean_Molecules_err_ch_2)
            dpg.set_value('single_conc_output_ch_2',mean_Concentration_ch_2)
            
            dpg.set_value('single_conc_err_output_ch_2',mean_Concentration_err_ch_2)
            Molecules_ch_2 = pd.DataFrame(Molecules_ch_2)
            Concentration_ch_2 = pd.DataFrame(Concentration_ch_2)
            
            Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2)
            Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2)
            
            
            
            
            Phot_hist_ch_2,Phot_bins_ch_2 =np.histogram(Photons_2.stack().reset_index(drop=True).dropna().values,
                                                        density=True,bins='auto')
            Phot_bins_ch_2=Phot_bins_ch_2[:-1]
            median_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().median()
            
            Mols_hist_ch_2,Mols_bins_ch_2 =np.histogram(pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().values
                                                        ,density=True,bins='auto')
            Mols_bins_ch_2=Mols_bins_ch_2[:-1]
            median_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().median()
            
            Conc_hist_ch_2,Conc_bins_ch_2 =np.histogram(pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().values
                                                        ,density=True,bins='auto')
            Conc_bins_ch_2=Conc_bins_ch_2[:-1]
            
            ind=np.where(Conc_hist_ch_2!=0)[0]
            
            Conc_hist_ch_2=Conc_hist_ch_2[ind]
            Conc_bins_ch_2=Conc_bins_ch_2[ind]
            
            ind=np.where(Mols_hist_ch_2!=0)[0]
            
            Mols_hist_ch_2=Mols_hist_ch_2[ind]
            Mols_bins_ch_2=Mols_bins_ch_2[ind]
            
            ind=np.where(Phot_hist_ch_2!=0)[0]
            
            Phot_hist_ch_2=Phot_hist_ch_2[ind]
            Phot_bins_ch_2=Phot_bins_ch_2[ind]
            
            dpg.set_value('c_dist_ser_ch_2',(Conc_bins_ch_2,Conc_hist_ch_2))
            dpg.set_value('c_mean_ser_ch_2',(np.array([mean_Concentration_ch_2]),np.array([max(Conc_hist_ch_2)])))
            dpg.set_value('c_med_ser_ch_2',(np.array([median_C_ch_2]),np.array([max(Conc_hist_ch_2)])))
            dpg.set_axis_limits('hist_xc_axis_ch2', min(Conc_bins_ch_2), max(Conc_bins_ch_2))
            dpg.set_axis_limits('hist_yc_axis_ch2', 0, max(Conc_hist_ch_2))
            
            dpg.set_value('np_dist_ser_ch_2',(Mols_bins_ch_2,Mols_hist_ch_2))
            dpg.set_value('np_mean_ser_ch_2',(np.array([mean_Molecules_ch_2]),np.array([max(Mols_hist_ch_2)])))
            dpg.set_value('np_med_ser_ch_2',(np.array([median_Molecules_ch_2]),np.array([max(Mols_hist_ch_2)])))
            dpg.set_axis_limits('hist_xnp_axis_ch2', min(Mols_bins_ch_2), max(Mols_bins_ch_2))
            dpg.set_axis_limits('hist_ynp_axis_ch2', 0, max(Mols_hist_ch_2))
            
            dpg.set_value('phot_dist_ser_ch_2',(Phot_bins_ch_2,Phot_hist_ch_2))
            dpg.set_value('phot_mean_ser_ch_2',(np.array([mean_Photons_ch_2]),np.array([max(Phot_hist_ch_2)])))
            dpg.set_value('phot_med_ser_ch_2',(np.array([median_Photons_ch_2]),np.array([max(Phot_hist_ch_2)])))
            dpg.set_axis_limits('hist_xphot_axis_ch2', min(Phot_bins_ch_2), max(Phot_bins_ch_2))
            dpg.set_axis_limits('hist_yphot_axis_ch2', 0, max(Phot_hist_ch_2))
            
            dpg.configure_item('c_mean_ser_ch_2',label='Mean = '+str(np.round(mean_Concentration_ch_2,4)))
            dpg.configure_item('c_med_ser_ch_2',label='Median = '+str(np.round(median_C_ch_2,4)))
            
            dpg.configure_item('np_mean_ser_ch_2',label='Mean = '+str(np.round(mean_Molecules_ch_2,2)))
            dpg.configure_item('np_med_ser_ch_2',label='Median = '+str(np.round(median_Molecules_ch_2,2)))
            
            dpg.configure_item('phot_mean_ser_ch_2',label='Mean = '+str(np.round(mean_Photons_ch_2,1)))
            dpg.configure_item('phot_med_ser_ch_2',label='Median = '+str(np.round(median_Photons_ch_2,1)))
            
            
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
                phot_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Phot_ch_2.csv')
                
                Photons_2.to_csv(phot_array_path_ch_2,index=False,sep=',', header=None)
            else:
                pass
            
            
            if dpg.get_value('Np_array_checkbox'):
                Np_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_ch_2.csv')
                
                Molecules_ch_2.to_csv(Np_array_path_ch_2,index=False,sep=',', header=None)
                
                Np_err_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_err_ch_2.csv')
                Molecules_err_ch_2.to_csv(Np_err_array_path_ch_2,index=False,sep=',', header=None)
            else:
                pass
            if dpg.get_value('C_array_checkbox'):
                Conc_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_ch_2.csv')
                
                Concentration_ch_2.to_csv(Conc_array_path_ch_2,index=False,sep=',', header=None)
                
                Conc_err_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_err_ch_2.csv')
                Concentration_err_ch_2.to_csv(Conc_err_array_path_ch_2,index=False,sep=',', header=None)
                
                
            else:
                pass
            
            if dpg.get_value('Photons_Hmaps_checkbox'):
                phot_hmap_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Phot_HM_ch_2.png')

                fig = Figure(facecolor='white')

                ax = fig.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Photons_2.min().min(), vmax=Photons_2.max().max())
                ax.imshow(Photons_2,cmap =cmap)

                ax.axis('off')
                fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
                FigureCanvas(fig).print_png(phot_hmap_path_ch_2)
                
            else:
                pass
            
            if dpg.get_value('Np_Hmaps_checkbox'):
                Np_hmap_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_HM_ch_2.png')

                fig = Figure(facecolor='white')

                ax = fig.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Molecules_ch_2.min().min(), vmax=Molecules_ch_2.max().max())
                ax.imshow(Molecules_ch_2,cmap =cmap)

                ax.axis('off')
                fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
                FigureCanvas(fig).print_png(Np_hmap_path_ch_2)
                
            else:
                pass

            if dpg.get_value('C_Hmaps_checkbox'):
                C_hmap_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_HM_ch_2.png')
                fig = Figure(facecolor='white')
                ax = fig.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Concentration_ch_2.min().min(), vmax=Concentration_ch_2.max().max())
                ax.imshow(Concentration_ch_2,cmap =cmap)

                ax.axis('off')
                fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
                FigureCanvas(fig).print_png(C_hmap_path_ch_2)
                
            else:
                pass
        else:
            pass
    
    
    if len(Channels) == 2:
        brightness_ch_1 = dpg.get_value('Brightness_input_ch_1')
        brightness_err_ch_1 = dpg.get_value('Brightness_err_input_ch_1') 
        Veff_ch_1 = 1e-15*dpg.get_value('focal_vol_input_ch_1')
        Veff_err_ch_1 = 1e-15*dpg.get_value('focal_vol_err_input_ch_1')
        DF = Current_image_1[0]
        Photons_1 = pd.DataFrame(DF)
        n_pixels_1 =  Photons_1.stack().reset_index(drop=True).dropna().count()
        
        Molecules_ch_1 = calc_molecules(DF,PTU_Px_dwell,PTU_N_frames,brightness_ch_1,brightness_err_ch_1)[0]
        Molecules_err_ch_1 = calc_molecules(DF,PTU_Px_dwell,PTU_N_frames,brightness_ch_1,brightness_err_ch_1)[1]
        Concentration_ch_1 = 1e9*CONC(Molecules_ch_1,Veff_ch_1,Molecules_err_ch_1,Veff_err_ch_1)[0]
        Concentration_err_ch_1 = 1e9*CONC(Molecules_ch_1,Veff_ch_1,Molecules_err_ch_1,Veff_err_ch_1)[1]

        
        
        mean_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().mean()
        mean_Photons_err_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
        mean_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().mean()
        if not dpg.get_value('Error_type_checkbox'):
            mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1).stack().reset_index(drop=True).dropna().mean()
        else:
            mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
        
        
        mean_Concentration_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().mean()
        if not dpg.get_value('Error_type_checkbox'):
            mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1).stack().reset_index(drop=True).dropna().mean()
        else:
            mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
        
        
        median_C_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().median()
        median_err_C_ch_1 = median_abs_deviation(pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna())
        dpg.set_value('sinle_phot_output_ch_1',mean_Photons_ch_1)
        
        dpg.set_value('sinle_phot_err_output_ch_1',mean_Photons_err_ch_1)
        dpg.set_value('sinle_mols_output_ch_1',mean_Molecules_ch_1)
        
        dpg.set_value('sinle_mols_err_output_ch_1',mean_Molecules_err_ch_1)
        dpg.set_value('single_conc_output_ch_1',mean_Concentration_ch_1)
        
        dpg.set_value('single_conc_err_output_ch_1',mean_Concentration_err_ch_1)
        Molecules_ch_1 = pd.DataFrame(Molecules_ch_1)
        Concentration_ch_1 = pd.DataFrame(Concentration_ch_1)
        
        Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1)
        Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1)
        
        
        

        Phot_hist_ch_1,Phot_bins_ch_1 =np.histogram(Photons_1.stack().reset_index(drop=True).dropna().values,
                                                    density=True,bins='auto')
        Phot_bins_ch_1=Phot_bins_ch_1[:-1]
        median_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().median()

        Mols_hist_ch_1,Mols_bins_ch_1 =np.histogram(pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().values
                                                    ,density=True,bins='auto')
        Mols_bins_ch_1=Mols_bins_ch_1[:-1]
        median_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().median()

        Conc_hist_ch_1,Conc_bins_ch_1 =np.histogram(pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().values
                                                    ,density=True,bins='auto')
        Conc_bins_ch_1=Conc_bins_ch_1[:-1]

        ind=np.where(Conc_hist_ch_1!=0)[0]

        Conc_hist_ch_1=Conc_hist_ch_1[ind]
        Conc_bins_ch_1=Conc_bins_ch_1[ind]

        ind=np.where(Mols_hist_ch_1!=0)[0]

        Mols_hist_ch_1=Mols_hist_ch_1[ind]
        Mols_bins_ch_1=Mols_bins_ch_1[ind]

        ind=np.where(Phot_hist_ch_1!=0)[0]

        Phot_hist_ch_1=Phot_hist_ch_1[ind]
        Phot_bins_ch_1=Phot_bins_ch_1[ind]

        dpg.set_value('c_dist_ser_ch_1',(Conc_bins_ch_1,Conc_hist_ch_1))
        dpg.set_value('c_mean_ser_ch_1',(np.array([mean_Concentration_ch_1]),np.array([max(Conc_hist_ch_1)])))
        dpg.set_value('c_med_ser_ch_1',(np.array([median_C_ch_1]),np.array([max(Conc_hist_ch_1)])))
        dpg.set_axis_limits('hist_xc_axis_ch1', min(Conc_bins_ch_1), max(Conc_bins_ch_1))
        dpg.set_axis_limits('hist_yc_axis_ch1', 0, max(Conc_hist_ch_1))

        dpg.set_value('np_dist_ser_ch_1',(Mols_bins_ch_1,Mols_hist_ch_1))
        dpg.set_value('np_mean_ser_ch_1',(np.array([mean_Molecules_ch_1]),np.array([max(Mols_hist_ch_1)])))
        dpg.set_value('np_med_ser_ch_1',(np.array([median_Molecules_ch_1]),np.array([max(Mols_hist_ch_1)])))
        dpg.set_axis_limits('hist_xnp_axis_ch1', min(Mols_bins_ch_1), max(Mols_bins_ch_1))
        dpg.set_axis_limits('hist_ynp_axis_ch1', 0, max(Mols_hist_ch_1))

        dpg.set_value('phot_dist_ser_ch_1',(Phot_bins_ch_1,Phot_hist_ch_1))
        dpg.set_value('phot_mean_ser_ch_1',(np.array([mean_Photons_ch_1]),np.array([max(Phot_hist_ch_1)])))
        dpg.set_value('phot_med_ser_ch_1',(np.array([median_Photons_ch_1]),np.array([max(Phot_hist_ch_1)])))
        dpg.set_axis_limits('hist_xphot_axis_ch1', min(Phot_bins_ch_1), max(Phot_bins_ch_1))
        dpg.set_axis_limits('hist_yphot_axis_ch1', 0, max(Phot_hist_ch_1))

        dpg.configure_item('c_mean_ser_ch_1',label='Mean = '+str(np.round(mean_Concentration_ch_1,4)))
        dpg.configure_item('c_med_ser_ch_1',label='Median = '+str(np.round(median_C_ch_1,4)))

        dpg.configure_item('np_mean_ser_ch_1',label='Mean = '+str(np.round(mean_Molecules_ch_1,2)))
        dpg.configure_item('np_med_ser_ch_1',label='Median = '+str(np.round(median_Molecules_ch_1,2)))

        dpg.configure_item('phot_mean_ser_ch_1',label='Mean = '+str(np.round(mean_Photons_ch_1,1)))
        dpg.configure_item('phot_med_ser_ch_1',label='Median = '+str(np.round(median_Photons_ch_1,1)))


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
            phot_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Phot_ch_1.csv')
            
            Photons_1.to_csv(phot_array_path_ch_1,index=False,sep=',', header=None)
        else:
            pass
        
        if dpg.get_value('Np_array_checkbox'):
            Np_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_ch_1.csv')
            
            Molecules_ch_1.to_csv(Np_array_path_ch_1,index=False,sep=',', header=None)
            
            Np_err_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_err_ch_1.csv')
            Molecules_err_ch_1.to_csv(Np_err_array_path_ch_1,index=False,sep=',', header=None)
            
        else:
            pass
        if dpg.get_value('C_array_checkbox'):
            Conc_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_ch_1.csv')
            
            Concentration_ch_1.to_csv(Conc_array_path_ch_1,index=False,sep=',', header=None)
            
            Conc_err_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_err_ch_1.csv')
            Concentration_err_ch_1.to_csv(Conc_err_array_path_ch_1,index=False,sep=',', header=None)
            
        else:
            pass

        
        if dpg.get_value('Photons_Hmaps_checkbox'):
            phot_hmap_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Phot_HM_ch_1.png')

            fig = Figure(facecolor='white')

            ax = fig.add_axes(rect)
            norm = mpl.colors.Normalize(vmin=Photons_1.min().min(), vmax=Photons_1.max().max())
            ax.imshow(Photons_1,cmap =cmap)

            ax.axis('off')
            fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
            FigureCanvas(fig).print_png(phot_hmap_path_ch_1)
            
        else:
            pass        

        if dpg.get_value('Np_Hmaps_checkbox'):
            Np_hmap_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_HM_ch_1.png')

            fig1 = Figure(facecolor='white')

            ax = fig1.add_axes(rect)
            norm = mpl.colors.Normalize(vmin=Molecules_ch_1.min().min(), vmax=Molecules_ch_1.max().max())
            ax.imshow(Molecules_ch_1,cmap =cmap)

            ax.axis('off')
            fig1.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
            FigureCanvas(fig1).print_png(Np_hmap_path_ch_1)
            
        else:
            pass

        if dpg.get_value('C_Hmaps_checkbox'):
            C_hmap_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_HM_ch_1.png')
            fig1 = Figure(facecolor='white')
            ax = fig1.add_axes(rect)
            norm = mpl.colors.Normalize(vmin=Concentration_ch_1.min().min(), vmax=Concentration_ch_1.max().max())
            ax.imshow(Concentration_ch_1,cmap =cmap)

            ax.axis('off')
            fig1.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
            FigureCanvas(fig1).print_png(C_hmap_path_ch_1)
            
        else:
            pass
        
        brightness_ch_2 = dpg.get_value('Brightness_input_ch_2')
        brightness_err_ch_2 = dpg.get_value('Brightness_err_input_ch_2') 
        Veff_ch_2 = 1e-15*dpg.get_value('focal_vol_input_ch_2')
        Veff_err_ch_2 = 1e-15*dpg.get_value('focal_vol_err_input_ch_2')
        DF2 = Current_image_2[0]
        Photons_2 = pd.DataFrame(DF2)
        n_pixels_2 =  Photons_2.stack().reset_index(drop=True).dropna().count()
        
        mean_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().mean()
        mean_Photons_err_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
        Molecules_ch_2 = calc_molecules(DF2,PTU_Px_dwell,PTU_N_frames,brightness_ch_2,brightness_err_ch_2)[0]
        Molecules_err_ch_2 = calc_molecules(DF2,PTU_Px_dwell,PTU_N_frames,brightness_ch_2,brightness_err_ch_2)[1]
        
        
        
        
        Concentration_ch_2 = 1e9*CONC(Molecules_ch_2,Veff_ch_2,Molecules_err_ch_2,Veff_err_ch_2)[0]
        Concentration_err_ch_2 = 1e9*CONC(Molecules_ch_2,Veff_ch_2,Molecules_err_ch_2,Veff_err_ch_2)[1]
        
        mean_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().mean()
        if not dpg.get_value('Error_type_checkbox'):
            mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2).stack().reset_index(drop=True).dropna().mean()
        else:
            mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
        
        
        
        mean_Concentration_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().mean()
        if not dpg.get_value('Error_type_checkbox'):
            mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2).stack().reset_index(drop=True).dropna().mean()
        else:
            mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
        
        median_C_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().median()
        median_err_C_ch_2 = median_abs_deviation(pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna())
        dpg.set_value('sinle_phot_output_ch_2',mean_Photons_ch_2)
        
        dpg.set_value('sinle_phot_err_output_ch_2',mean_Photons_err_ch_2)
        dpg.set_value('sinle_mols_output_ch_2',mean_Molecules_ch_2)
        
        dpg.set_value('sinle_mols_err_output_ch_2',mean_Molecules_err_ch_2)
        dpg.set_value('single_conc_output_ch_2',mean_Concentration_ch_2)
        
        dpg.set_value('single_conc_err_output_ch_2',mean_Concentration_err_ch_2)
        Molecules_ch_2 = pd.DataFrame(Molecules_ch_2)
        Concentration_ch_2 = pd.DataFrame(Concentration_ch_2)
        
        Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2)
        Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2)
        
        
        
            
        Phot_hist_ch_2,Phot_bins_ch_2 =np.histogram(Photons_2.stack().reset_index(drop=True).dropna().values,
                                                    density=True,bins='auto')
        Phot_bins_ch_2=Phot_bins_ch_2[:-1]
        median_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().median()

        Mols_hist_ch_2,Mols_bins_ch_2 =np.histogram(pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().values
                                                    ,density=True,bins='auto')
        Mols_bins_ch_2=Mols_bins_ch_2[:-1]
        median_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().median()

        Conc_hist_ch_2,Conc_bins_ch_2 =np.histogram(pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().values
                                                    ,density=True,bins='auto')
        Conc_bins_ch_2=Conc_bins_ch_2[:-1]

        ind=np.where(Conc_hist_ch_2!=0)[0]

        Conc_hist_ch_2=Conc_hist_ch_2[ind]
        Conc_bins_ch_2=Conc_bins_ch_2[ind]

        ind=np.where(Mols_hist_ch_2!=0)[0]

        Mols_hist_ch_2=Mols_hist_ch_2[ind]
        Mols_bins_ch_2=Mols_bins_ch_2[ind]

        ind=np.where(Phot_hist_ch_2!=0)[0]

        Phot_hist_ch_2=Phot_hist_ch_2[ind]
        Phot_bins_ch_2=Phot_bins_ch_2[ind]

        dpg.set_value('c_dist_ser_ch_2',(Conc_bins_ch_2,Conc_hist_ch_2))
        dpg.set_value('c_mean_ser_ch_2',(np.array([mean_Concentration_ch_2]),np.array([max(Conc_hist_ch_2)])))
        dpg.set_value('c_med_ser_ch_2',(np.array([median_C_ch_2]),np.array([max(Conc_hist_ch_2)])))
        dpg.set_axis_limits('hist_xc_axis_ch2', min(Conc_bins_ch_2), max(Conc_bins_ch_2))
        dpg.set_axis_limits('hist_yc_axis_ch2', 0, max(Conc_hist_ch_2))

        dpg.set_value('np_dist_ser_ch_2',(Mols_bins_ch_2,Mols_hist_ch_2))
        dpg.set_value('np_mean_ser_ch_2',(np.array([mean_Molecules_ch_2]),np.array([max(Mols_hist_ch_2)])))
        dpg.set_value('np_med_ser_ch_2',(np.array([median_Molecules_ch_2]),np.array([max(Mols_hist_ch_2)])))
        dpg.set_axis_limits('hist_xnp_axis_ch2', min(Mols_bins_ch_2), max(Mols_bins_ch_2))
        dpg.set_axis_limits('hist_ynp_axis_ch2', 0, max(Mols_hist_ch_2))

        dpg.set_value('phot_dist_ser_ch_2',(Phot_bins_ch_2,Phot_hist_ch_2))
        dpg.set_value('phot_mean_ser_ch_2',(np.array([mean_Photons_ch_2]),np.array([max(Phot_hist_ch_2)])))
        dpg.set_value('phot_med_ser_ch_2',(np.array([median_Photons_ch_2]),np.array([max(Phot_hist_ch_2)])))
        dpg.set_axis_limits('hist_xphot_axis_ch2', min(Phot_bins_ch_2), max(Phot_bins_ch_2))
        dpg.set_axis_limits('hist_yphot_axis_ch2', 0, max(Phot_hist_ch_2))

        dpg.configure_item('c_mean_ser_ch_2',label='Mean = '+str(np.round(mean_Concentration_ch_2,4)))
        dpg.configure_item('c_med_ser_ch_2',label='Median = '+str(np.round(median_C_ch_2,4)))

        dpg.configure_item('np_mean_ser_ch_2',label='Mean = '+str(np.round(mean_Molecules_ch_2,2)))
        dpg.configure_item('np_med_ser_ch_2',label='Median = '+str(np.round(median_Molecules_ch_2,2)))

        dpg.configure_item('phot_mean_ser_ch_2',label='Mean = '+str(np.round(mean_Photons_ch_2,1)))
        dpg.configure_item('phot_med_ser_ch_2',label='Median = '+str(np.round(median_Photons_ch_2,1)))


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
            phot_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Phot_ch_2.csv')
            
            Photons_2.to_csv(phot_array_path_ch_2,index=False,sep=',', header=None)
        else:
            pass        

        if dpg.get_value('Np_array_checkbox'):
            Np_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_ch_2.csv')
            
            Molecules_ch_2.to_csv(Np_array_path_ch_2,index=False,sep=',', header=None)
            
            Np_err_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_err_ch_2.csv')
            Molecules_err_ch_2.to_csv(Np_err_array_path_ch_2,index=False,sep=',', header=None)
        else:
            pass
        if dpg.get_value('C_array_checkbox'):
            Conc_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_ch_2.csv')
            
            Concentration_ch_2.to_csv(Conc_array_path_ch_2,index=False,sep=',', header=None)
            
            
            Conc_err_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_err_ch_2.csv')
            Concentration_err_ch_2.to_csv(Conc_err_array_path_ch_2,index=False,sep=',', header=None)
        else:
            pass

        if dpg.get_value('Photons_Hmaps_checkbox'):
            phot_hmap_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Phot_HM_ch_2.png')

            fig = Figure(facecolor='white')

            ax = fig.add_axes(rect)
            norm = mpl.colors.Normalize(vmin=Photons_2.min().min(), vmax=Photons_2.max().max())
            ax.imshow(Photons_2,cmap =cmap)

            ax.axis('off')
            fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
            FigureCanvas(fig).print_png(phot_hmap_path_ch_2)
            
        else:
            pass       

        if dpg.get_value('Np_Hmaps_checkbox'):
            Np_hmap_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_HM_ch_2.png')

            fig2 = Figure(facecolor='white')

            ax = fig2.add_axes(rect)
            norm = mpl.colors.Normalize(vmin=Molecules_ch_2.min().min(), vmax=Molecules_ch_2.max().max())
            ax.imshow(Molecules_ch_2,cmap =cmap)

            ax.axis('off')
            fig2.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
            FigureCanvas(fig2).print_png(Np_hmap_path_ch_2)
            
        else:
            pass

        if dpg.get_value('C_Hmaps_checkbox'):
            C_hmap_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_HM_ch_2.png')
            fig2 = Figure(facecolor='white')
            ax = fig2.add_axes(rect)
            norm = mpl.colors.Normalize(vmin=Concentration_ch_2.min().min(), vmax=Concentration_ch_2.max().max())
            ax.imshow(Concentration_ch_2,cmap =cmap)

            ax.axis('off')
            fig2.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
            FigureCanvas(fig2).print_png(C_hmap_path_ch_2)
            
        else:
            pass
    
    
    
    
   

def callback_calculate_all(sender,app_data):
    global files,anal_file,DF,DF2,pck_list
    
    
    
    
    global Sing_Results_DF
    global mean_Molecules_ch_1,std_Molecules_ch_1,mean_Concentration_ch_1,std_Concentration_ch_1,std_err_Concentration_ch_1,median_C_ch_1,median_err_C_ch_1,mean_Molecules_err_ch_1,mean_Concentration_err_ch_1,mean_Photons_ch_1,mean_Photons_err_ch_1
    global mean_Molecules_ch_2,std_Molecules_ch_2,mean_Concentration_ch_2,std_Concentration_ch_2,std_err_Concentration_ch_2,median_C_ch_2,median_err_C_ch_2,mean_Molecules_err_ch_2,mean_Concentration_err_ch_2,mean_Photons_ch_2,mean_Photons_err_ch_2
    global Current_image_1,Current_image_2,Channels
    filenames = [f.replace('.ptu','') for f in files]
    
    
    for cnt, an_file in enumerate(filenames):
        anal_file=an_file
        
        dpg.configure_item('file_box', default_value=an_file)
        load_PTU_images(an_file)
        callback_calculate(sender,app_data)
        
        
        
        
        
        
        
        if len(Channels) == 1:
            if '1' in Channels[0]:
        
        
                Sing_Results_DF_tmp = pd.DataFrame([[anal_file,
                                                     1,
                                                     mean_Photons_ch_1,
                                                     mean_Photons_err_ch_1,
                                                     mean_Molecules_ch_1,
                                                     mean_Molecules_err_ch_1,
                                                     mean_Concentration_ch_1,
                                                     mean_Concentration_err_ch_1,
                                                     
                                                     median_C_ch_1,
                                                     median_err_C_ch_1]],columns=Sing_Results_DF.columns)
            
            elif '2' in Channels[0]:
                Sing_Results_DF_tmp = pd.DataFrame([
                                                   [anal_file,
                                                 2,
                                                 mean_Photons_ch_2,
                                                 mean_Photons_err_ch_2,
                                                 mean_Molecules_ch_2,
                                                 mean_Molecules_err_ch_2,
                                                 mean_Concentration_ch_2,
                                                 mean_Concentration_err_ch_2,
                                                 
                                                 median_C_ch_2,
                                                 median_err_C_ch_2]],columns=Sing_Results_DF.columns)
            else:
                pass
        
        if len(Channels) == 2:
            Sing_Results_DF_tmp = pd.DataFrame([[anal_file,
                                                 1,
                                                 mean_Photons_ch_1,
                                                 mean_Photons_err_ch_1,
                                                 mean_Molecules_ch_1,
                                                 mean_Molecules_err_ch_1,
                                                 mean_Concentration_ch_1,
                                                 mean_Concentration_err_ch_1,
                                                 
                                                     median_C_ch_1,
                                                     median_err_C_ch_1],
                                                   [anal_file,
                                                 2,
                                                 mean_Photons_ch_2,
                                                 mean_Photons_err_ch_2,
                                                 mean_Molecules_ch_2,
                                                 mean_Molecules_err_ch_2,
                                                 mean_Concentration_ch_2,
                                                 mean_Concentration_err_ch_2,
                                                 
                                                     median_C_ch_2,
                                                     median_err_C_ch_2]],columns=Sing_Results_DF.columns)



        Sing_Results_DF=pd.concat([Sing_Results_DF,Sing_Results_DF_tmp]).reset_index(drop=True)
        

   
    
    

    


def callback_directory_select(sender,app_data):
    
    global files, anal_file
    files=()
    global directory, new_directory,last_directory,PTU_directory
    directory = app_data['file_path_name']
    PTU_directory = directory
    new_directory=directory
    last_directory=directory
    update_dialogs_default_directory(last_directory)
    files = tuple(np.sort([f for f in os.listdir(directory) if f.endswith('.ptu')]))
    
    if len(files)==0:
        show_error_no_files('No PTU files found.')
    else:
        update_flist(files)
    
    anal_file=files[0]
    dpg.configure_item('file_box', default_value=anal_file)
    



def callback_empty(sender,app_data):
    '''Empty function. Do nothing.'''
    pass



def callback_font_size(sender,app_data):
    global current_font_size,ratio_w,ratio_h,dif_vp0_width
    global inf_w
    font = 'DejaVu'
    
    inf_w = dpg.get_viewport_width()-dif_vp0_width
    inf_h = dpg.get_viewport_height()
    ratio_w = inf_w/(init_widths['VIEWPORT']-dif_vp0_width)
    ratio_h = inf_h/init_heights['VIEWPORT']
    ratio = 1
    if ratio_w < ratio_h:
        ratio = ratio_w
    else:
        ratio = ratio_h

    new_font_size = int(init_font_size*ratio)
    current_font_size = new_font_size
    
    dpg.delete_item(font)
    dpg.delete_item('Font_registry')
    add_font_to_registry(current_font_size)
    



def callback_kappa_err_input(sender,app_data):
    
    if sender == 'kappa_err_input_ch_1':
        omega = dpg.get_value('omega_input_ch_1')
        omega_err = dpg.get_value('omega_err_input_ch_1')
        kappa = dpg.get_value('kappa_input_ch_1')
        kappa_err =  app_data
        foc_vol = VEFF(omega,kappa,omega_err,kappa_err)
        dpg.configure_item('focal_vol_input_ch_1',default_value = foc_vol[0] )
        dpg.configure_item('focal_vol_err_input_ch_1',default_value = foc_vol[1] )
    else:
        omega = dpg.get_value('omega_input_ch_2')
        omega_err = dpg.get_value('omega_err_input_ch_2')
        kappa = dpg.get_value('kappa_input_ch_2')
        kappa_err =  app_data
        foc_vol = VEFF(omega,kappa,omega_err,kappa_err)
        dpg.configure_item('focal_vol_input_ch_2',default_value = foc_vol[0] )
        dpg.configure_item('focal_vol_err_input_ch_2',default_value = foc_vol[1] )

    


def callback_kappa_input(sender,app_data):
    
    if sender == 'kappa_input_ch_1':
        omega = dpg.get_value('omega_input_ch_1')
        omega_err = dpg.get_value('omega_err_input_ch_1')
        kappa = app_data
        kappa_err =  dpg.get_value('kappa_err_input_ch_1')
        foc_vol = VEFF(omega,kappa,omega_err,kappa_err)
        dpg.configure_item('focal_vol_input_ch_1',default_value = foc_vol[0] )
        dpg.configure_item('focal_vol_err_input_ch_1',default_value = foc_vol[1] )
    else:
        omega = dpg.get_value('omega_input_ch_2')
        omega_err = dpg.get_value('omega_err_input_ch_2')
        kappa = app_data
        kappa_err =  dpg.get_value('kappa_err_input_ch_2')
        foc_vol = VEFF(omega,kappa,omega_err,kappa_err)
        dpg.configure_item('focal_vol_input_ch_2',default_value = foc_vol[0] )
        dpg.configure_item('focal_vol_err_input_ch_2',default_value = foc_vol[1] )
    
    


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
            with open('../LICENSE', 'r') as file:
                Licence = file.read()
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
    global anal_file
    anal_file = app_data
    load_PTU_images(anal_file)
    hide_histograms()
    callback_calculate(sender,app_data)
    
    
    
    
    
    


def callback_no_files_dialog_close_only(sender,app_data):
    dpg.configure_item('No_data_files',show=False)
    dpg.delete_item('no_files_error_text')
    dpg.delete_item('no_files_error_butt')
    dpg.delete_item('No_data_files')



def callback_omega_err_input(sender,app_data):
    
    if sender == 'omega_err_input_ch_1':
        omega = dpg.get_value('omega_input_ch_1')
        omega_err = app_data
        kappa = dpg.get_value('kappa_input_ch_1')
        kappa_err =  dpg.get_value('kappa_err_input_ch_1')
        foc_vol = VEFF(omega,kappa,omega_err,kappa_err)
        dpg.configure_item('focal_vol_input_ch_1',default_value = foc_vol[0] )
        dpg.configure_item('focal_vol_err_input_ch_1',default_value = foc_vol[1] )
    else:
        omega = dpg.get_value('omega_input_ch_2')
        omega_err = app_data
        kappa = dpg.get_value('kappa_input_ch_2')
        kappa_err =  dpg.get_value('kappa_err_input_ch_2')
        foc_vol = VEFF(omega,kappa,omega_err,kappa_err)
        dpg.configure_item('focal_vol_input_ch_2',default_value = foc_vol[0] )
        dpg.configure_item('focal_vol_err_input_ch_2',default_value = foc_vol[1] )
    


def callback_omega_input(sender,app_data):
    
    if sender == 'omega_input_ch_1':
        omega = app_data
        omega_err = dpg.get_value('omega_err_input_ch_1')
        kappa = dpg.get_value('kappa_input_ch_1')
        kappa_err =  dpg.get_value('kappa_err_input_ch_1')
        foc_vol = VEFF(omega,kappa,omega_err,kappa_err)
        dpg.configure_item('focal_vol_input_ch_1',default_value = foc_vol[0] )
        dpg.configure_item('focal_vol_err_input_ch_1',default_value = foc_vol[1] )
    else:
        omega = app_data
        omega_err = dpg.get_value('omega_err_input_ch_2')
        kappa = dpg.get_value('kappa_input_ch_2')
        kappa_err =  dpg.get_value('kappa_err_input_ch_2')
        foc_vol = VEFF(omega,kappa,omega_err,kappa_err)
        dpg.configure_item('focal_vol_input_ch_2',default_value = foc_vol[0] )
        dpg.configure_item('focal_vol_err_input_ch_2',default_value = foc_vol[1] )
    


def callback_remove_result_button(sender,app_data):
    
    global FCS_results_ch_1,FCS_results_ch_2
    if sender == 'remove_button_results_ch_1':
        ind_result_to_remove =[]
        for i in FCS_results_ch_1.index:
            if dpg.get_value('ch_1_results_delete_'+str(i)+'_check_ch_1'):
                ind_result_to_remove.append(i)
        
        FCS_results_ch_1.drop(FCS_results_ch_1.index[ind_result_to_remove],inplace=True)
        FCS_results_ch_1.reset_index(drop=True,inplace=True)

        mean_bright_input_ch_1()

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
        for i in FCS_results_ch_1.index:

            with dpg.table_row(tag='ch_1_row_results_show_ch_1'+str(i),parent='table_results_show_ch_1'):

                dpg.add_text(FCS_results_ch_1.at[i,'file'],tag='ch_1_results_show_'+str(i)+'_name_ch_1')
                dpg.add_text(np.round(FCS_results_ch_1.at[i,'N_p'],2),tag='ch_1_results_show_'+str(i)+'_N_p_value_ch_1')
                dpg.add_text(FCS_results_ch_1.at[i,'Brightness'],tag='ch_1_results_show_'+str(i)+'_Brightness_value_ch_1')
                dpg.add_checkbox(label='',
                                 tag='ch_1_results_delete_'+str(i)+'_check_ch_1')
    else:
        ind_result_to_remove =[]
        for i in FCS_results_ch_2.index:
            if dpg.get_value('ch_2_results_delete_'+str(i)+'_check_ch_2'):
                ind_result_to_remove.append(i)
        FCS_results_ch_2.drop(FCS_results_ch_2.index[ind_result_to_remove],inplace=True)
        FCS_results_ch_2.reset_index(drop=True,inplace=True)

        mean_bright_input_ch_2()

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
        for i in FCS_results_ch_2.index:

            with dpg.table_row(tag='ch_2_row_results_show_ch_2'+str(i),parent='table_results_show_ch_2'):

                dpg.add_text(FCS_results_ch_2.at[i,'file'],tag='ch_2_results_show_'+str(i)+'_name_ch_2')
                dpg.add_text(np.round(FCS_results_ch_2.at[i,'N_p'],2),tag='ch_2_results_show_'+str(i)+'_N_p_value_ch_2')
                dpg.add_text(FCS_results_ch_2.at[i,'Brightness'],tag='ch_2_results_show_'+str(i)+'_Brightness_value_ch_2')
                dpg.add_checkbox(label='',
                                 tag='ch_2_results_delete_'+str(i)+'_check_ch_2')
    
    
    


def callback_reset_results_DF():
    global Sing_Results_DF
    Sing_Results_DF = pd.DataFrame(columns=['File', 'Channel','<Counts>','Counts_std','<N_p>','N_p_err','<C>', 'C_err','C_median', 'C_median_abs_err'])
        

        



def callback_select_lt_to_roi(sender,app_data):
    global anal_file
    load_PTU_images(anal_file)
    
    


def callback_select_roi(sender,app_data):
    global anal_file
    load_PTU_images(anal_file)
    
    
    


def callback_show_int(sender,app_data):
    global anal_file
    load_PTU_images(anal_file)
    


def callback_show_lt(sender,app_data):
    global anal_file
    load_PTU_images(anal_file)
    
    


def callback_test(sender,app_data):
    items = dpg.get_aliases()
    if 'texture_tag_chan_1' in items:
        dpg.delete_item('texture_tag_chan_1')
        
    
    
    else:
        pass
    
    


def callback_windows_size(sender,app_data):
    global image_width1,image_height1,dpg_image1
    global ratio_w ,ratio_h ,top_indent,bottom_indent,left_indent,right_indent,internal_indent
    global group_spacer,var_def_group_1_spacer
    global init_widths, init_heights,init_position
    global DF,DF2
    global Current_image_1,Current_image_2
    global tex_1_name,tex_2_name,dif_vp0_width
    global inf_w
    # print('RUNNING: callback_windows_size')
    inf_w = dpg.get_viewport_width()-dif_vp0_width
    
    inf_h = dpg.get_viewport_height()
    
    items = dpg.get_aliases()
    
    # print('reseize',inf_w,inf_h)

    item_types = []
    for item in items:
        item_types.append(dpg.get_item_type(item))
    item_types=set(item_types)
    item_types_dict = {}
    for item_type in item_types:
        its = []
        for item in items:
            if dpg.get_item_type(item) == item_type:
                its.append(item)
        item_types_dict[item_type]=its
    
    items = [item for item in items if dpg.get_item_type(item) in resizable_items ]
    ratio_w = inf_w/(init_widths['VIEWPORT']-dif_vp0_width)
    ratio_h = inf_h/init_heights['VIEWPORT']
    # print('line 2577',ratio_w,ratio_h)

    
    top_indent = int(init_top_indent*ratio_h)
    bottom_indent = int(init_bottom_indent*ratio_h)
    left_indent = int(init_left_indent*ratio_w)
    right_indent = int(init_right_indent*ratio_w)
    internal_indent = int(init_internal_indent*ratio_w)
    group_spacer = int(np.round(init_group_spacer*ratio_w))
    image_width1 = int(init_image_width1*ratio_w)
    image_height1 = int(init_image_height1*ratio_h)
    var_def_group_1_spacer = int(init_var_def_group_1_spacer*ratio_w)
    
    item = 'PTU_DATA_window'
    # print('line 2591',item)
    new_width = int(init_widths[item]*ratio_w)
    new_height = int(init_heights[item]*ratio_h)
    new_pos = (left_indent,top_indent)
    
    wdt_hgt_pos(item,new_width,new_height,new_pos)
    
    item = 'file_window'
    # print('line 2599',item)
    new_width = dpg.get_item_width('PTU_DATA_window')
    
    new_height = int(init_heights[item]*ratio_h)
    
    new_pos = (dpg.get_item_pos('PTU_DATA_window')[0],
               top_indent+dpg.get_item_height('PTU_DATA_window')+internal_indent)
    wdt_hgt_pos(item,new_width,new_height,new_pos)
    
    
    item1 = 'image_window_ch1'
    # print('line 2610',item1)
    item2 = 'image_window_ch2'
    # print('line 2612',item2)
    mult = ((init_widths['VIEWPORT']-dif_vp0_width)*ratio_w -left_indent-2*internal_indent-init_widths['PTU_DATA_window']-internal_indent- right_indent-5)/2/init_widths[item1]
    # print('line 2614',mult)
    
    
    
    
    new_width = (dpg.get_viewport_width()-left_indent-dpg.get_item_width('PTU_DATA_window')-5*internal_indent-init_widths['FCS_window']*ratio_w)//2
    new_height = new_width

    image_position_1 = (left_indent+dpg.get_item_width('PTU_DATA_window')+internal_indent,
                  top_indent)
    
    
    # print('line 2626',image_position_1)
    # print(Current_image_1)
    dpg_image_1 = update_texture(Current_image_1)
    dpg.set_item_pos('image_window_ch1',image_position_1)
    # print('line 2630',tex_1_name)
    # ites = dpg.get_aliases()
    # ites = [it for it in ites if it.startswith('texture')]
    # print(ites)
    
    if tex_1_name in dpg.get_aliases():
        dpg.delete_item(tex_1_name)
        
        dpg.remove_alias(tex_1_name)
        # print('line 2639','img1_passed0')
        dpg.delete_item('texture_CH_1')
        # print('line 2641','img1_passed')
        if 'new' in tex_1_name:
            new = 'texture_tag_chan_1-new_'+str(int(tex_1_name.split('-')[1].split('_')[1])+1)
            tex_1_name =new
            
            
            
        else:
            
            tex_1_name = 'texture_tag_chan_1-new_1'
        
        dpg.add_dynamic_texture(width=new_width,
                        height=new_height,
                        default_value=dpg_image_1,
                        tag=tex_1_name,
                        parent = 'texture_reg')
        
        dpg.add_image(tex_1_name,parent = 'image_window_ch1'
                              ,uv_min=(0,0),uv_max=(1,1),tag = 'texture_CH_1')

    
    
    

    image_position_2 = (left_indent+dpg.get_item_width('PTU_DATA_window')+internal_indent+dpg.get_item_width(tex_1_name)+2*internal_indent,
                  top_indent)
    
    # print('line 2668',image_position_2)
    dpg_image_2 = update_texture(Current_image_2)
    dpg.set_item_pos('image_window_ch2',image_position_2)
    if tex_2_name in dpg.get_aliases():
        dpg.delete_item(tex_2_name)
        # print('line 2673','img2_passed00')
        dpg.remove_alias(tex_2_name)
        # print('line 2675','img2_passed0')
        dpg.delete_item('texture_CH_2')
        # print('line 2677','img2_passed')
        if 'new' in tex_2_name:
            new = 'texture_tag_chan_2-new_'+str(int(tex_2_name.split('-')[1].split('_')[1])+1)
            tex_2_name =new
            
            
            
        else:
            
            tex_2_name = 'texture_tag_chan_2-new_1'
        dpg.add_dynamic_texture(width=new_width,
                        height=new_height,
                        default_value=dpg_image_2,
                        tag=tex_2_name,
                        parent = 'texture_reg')
        
        dpg.add_image(tex_2_name,parent = 'image_window_ch2'
                              ,uv_min=(0,0),uv_max=(1,1),tag = 'texture_CH_2')
    
    item = 'FCS_window'
    # print('line 2697',item)
    new_weight = int(init_widths[item]*ratio_w)
    new_height = int(init_heights[item]*ratio_h)
    new_pos = (left_indent+dpg.get_item_width('PTU_DATA_window')+internal_indent+dpg.get_item_width(tex_1_name)+2*internal_indent+dpg.get_item_width(tex_2_name)+2*internal_indent
               
               ,top_indent)
    wdt_hgt_pos(item,new_weight,new_height,new_pos)
    
    item = 'results_window'
    # print('line 2706',item)
    new_weight = int(init_widths[item]*ratio_w)
    new_height = int(init_heights[item]*ratio_h)
    new_pos = (dpg.get_item_pos('FCS_window')[0],dpg.get_item_pos('FCS_window')[1]+dpg.get_item_height('FCS_window')+internal_indent)
    wdt_hgt_pos(item,new_weight,new_height,new_pos)
    
    
    

    
    
    
    item = 'hist_window_ch1'
    # print('line 2719',item)
    new_width = dpg.get_item_width(tex_1_name)+int(1.5*init_internal_indent)
    new_height = dpg.get_item_height(tex_1_name)*hist_scaller+int(1.5*init_internal_indent)
    new_pos = (left_indent+dpg.get_item_width('PTU_DATA_window')+internal_indent,
               top_indent+dpg.get_item_height(tex_1_name)+int(4.5*init_internal_indent))
    
    wdt_hgt_pos(item,new_width,new_height,new_pos)
    
    
    item = 'hist_window_ch2'
    # print('line 2729',item)
    new_width = dpg.get_item_width(tex_2_name)+int(1.5*init_internal_indent)
    new_height = dpg.get_item_height(tex_2_name)*hist_scaller+int(1.5*init_internal_indent)
    new_pos = (left_indent+dpg.get_item_width('PTU_DATA_window')+internal_indent+dpg.get_item_width(tex_1_name)+2*internal_indent,
               top_indent+dpg.get_item_height(tex_2_name)+int(4.5*init_internal_indent))
    
    wdt_hgt_pos(item,new_width,new_height,new_pos)
    
    
    
    
    

    

    
    
    for item in file_panel_items:
        # print(item)
        new_weight = int(init_widths[item]*ratio_w)
        wdt_hgt_pos(item,new_weight,None,None)
        




    
    for item in dialogs:
        # print(item)
        new_weight = int(init_widths[item]*ratio_w)
        new_height = int(init_heights[item]*ratio_h)

        wdt_hgt_pos(item,new_weight,new_height,None)
    
    

    
    
    
    '''Group spacer resizing'''
    for item in item_types_dict['mvAppItemType::mvGroup']:
        # print(item)
        if dpg.get_item_configuration(item)['horizontal']:
            
            dpg.configure_item(item,horizontal_spacing = group_spacer)
        else:
            pass
        
    if platform.system().upper() == "LINUX":
        
        dpg.set_viewport_resizable(False)

    


def display_images(dframes,channel):

    global tex_1_name,tex_2_name



    if channel == 'both':
        df = dframes[0]
        df2 = dframes[1]
        
    elif channel == 1:
        df = dframes[0]
        
    elif channel == 2:
        df2 = dframes[0]
        
    else:
        pass


        











    

    
    

    

    
    


        

        

           







        









        








        



        


            

        











        







        

 

        
    if channel == 1:
        dpg_image_1 = update_texture(Current_image_1)
        
        















        
        








        dpg.set_value(tex_1_name, dpg_image_1)
    elif channel == 2:
        dpg_image_2 = update_texture(Current_image_2)















        








        dpg.set_value(tex_2_name, dpg_image_2)
    elif channel =='both':
        dpg_image_1 = update_texture(Current_image_1)
        dpg_image_2 = update_texture(Current_image_2)















        













        


















    
        dpg.set_value(tex_1_name, dpg_image_1)
        dpg.set_value(tex_2_name, dpg_image_2)
    



            

            





























    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
            
            
            
            
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        


def extract_PTU(Directory,ptu_file,):
    jsn={}
    ptu_path = os.path.join(directory,ptu_file)
    ptu_image  = PTUreader(ptu_path, print_header_data = False)
    flim_data_stack, intensity_image_all_channels = ptu_image.get_flim_data_stack()
    if flim_data_stack.ndim == 4:
        number_of_channels = flim_data_stack.shape[2]
        
        Resolution = str(flim_data_stack.shape[0])+'x'+str(flim_data_stack.shape[1])

        
    if flim_data_stack.ndim == 3:
        number_of_channels = flim_data_stack.shape[2]
        
        Resolution = str(flim_data_stack.shape[0])+'x'+str(flim_data_stack.shape[1])
    ccnt =0
    for channel in range(number_of_channels):
        channel_data = np.sum(flim_data_stack[:,:,channel,:],axis=2)
        data_sum = channel_data.sum()
        if data_sum!=0:
            ccnt +=1
            
    number_of_channels = ccnt
    dpg.configure_item("N_channels", default_value='Number of chanels: '+str(number_of_channels))
    dpg.configure_item("resolution", default_value='Resolution: '+Resolution)
    

        
    for channel in range(number_of_channels):
        pickle_name = ptu_file.replace('.ptu', '_in_ch_'+str(channel+1)+'.pck')
        jsn['channel_'+str(channel+1)]=pickle_name


        channel_data = np.sum(flim_data_stack[:,:,channel,:],axis=2)
        
        


    return jsn
            


def hide_histograms():
    dpg.set_value('c_dist_ser_ch_1',(np.empty(2),np.empty(2)))
    dpg.set_value('c_mean_ser_ch_1',(np.empty(2),np.empty(2)))
    dpg.set_value('c_med_ser_ch_1',(np.empty(2),np.empty(2)))
    dpg.set_value('np_dist_ser_ch_1',(np.empty(2),np.empty(2)))
    dpg.set_value('np_mean_ser_ch_1',(np.empty(2),np.empty(2)))
    dpg.set_value('np_med_ser_ch_1',(np.empty(2),np.empty(2)))
    dpg.set_value('phot_dist_ser_ch_1',(np.empty(2),np.empty(2)))
    dpg.set_value('phot_mean_ser_ch_1',(np.empty(2),np.empty(2)))
    dpg.set_value('phot_med_ser_ch_1',(np.empty(2),np.empty(2)))
    dpg.configure_item('c_mean_ser_ch_1',label='Mean = ')
    dpg.configure_item('c_med_ser_ch_1',label='Median = ')
    dpg.configure_item('np_mean_ser_ch_1',label='Mean = ')
    dpg.configure_item('np_med_ser_ch_1',label='Median = ')
    dpg.configure_item('phot_mean_ser_ch_1',label='Mean = ')
    dpg.configure_item('phot_med_ser_ch_1',label='Median = ')
    dpg.hide_item('hist_conc_plot_ch1')
    dpg.hide_item('hist_np_plot_ch1')
    dpg.hide_item('hist_phot_plot_ch1')
    
    dpg.set_value('c_dist_ser_ch_2',(np.empty(2),np.empty(2)))
    dpg.set_value('c_mean_ser_ch_2',(np.empty(2),np.empty(2)))
    dpg.set_value('c_med_ser_ch_2',(np.empty(2),np.empty(2)))
    dpg.set_value('np_dist_ser_ch_2',(np.empty(2),np.empty(2)))
    dpg.set_value('np_mean_ser_ch_2',(np.empty(2),np.empty(2)))
    dpg.set_value('np_med_ser_ch_2',(np.empty(2),np.empty(2)))
    dpg.set_value('phot_dist_ser_ch_2',(np.empty(2),np.empty(2)))
    dpg.set_value('phot_mean_ser_ch_2',(np.empty(2),np.empty(2)))
    dpg.set_value('phot_med_ser_ch_2',(np.empty(2),np.empty(2)))
    dpg.configure_item('c_mean_ser_ch_2',label='Mean = ')
    dpg.configure_item('c_med_ser_ch_2',label='Median = ')
    dpg.configure_item('np_mean_ser_ch_2',label='Mean = ')
    dpg.configure_item('np_med_ser_ch_2',label='Median = ')
    dpg.configure_item('phot_mean_ser_ch_2',label='Mean = ')
    dpg.configure_item('phot_med_ser_ch_2',label='Median = ')
    dpg.hide_item('hist_conc_plot_ch2')
    dpg.hide_item('hist_np_plot_ch2')
    dpg.hide_item('hist_phot_plot_ch2')
    


def image_INT_LT(img,width,height):
    dct = locals()
    

    if isinstance(img[0],np.ndarray) and isinstance(img[1],np.ndarray):
        fg_color = 'white'
        px = 1/plt.rcParams['figure.dpi']


        
        
        fig,ax = plt.subplots(figsize=(np.round(width*px,3),np.round(height*px,3)),facecolor='black')
        
        
        fig.subplots_adjust(top=1, bottom=-0.15, right=1, left=0, hspace=0, wspace=0)
        ax.margins(0, 0,)
        ax.axis('off')

        pa = ax.imshow(img[0],cmap='gray')
        cba = plt.colorbar(pa,shrink=0.69,location = 'right',anchor=(-0.25,0.98))
        pb = ax.imshow(img[1],cmap='rainbow',alpha=0.5)
        cbb = plt.colorbar(pb,location = 'bottom',shrink=0.95,anchor=(0.5,2.15))
        cba.ax.yaxis.set_tick_params(color=fg_color)
        cba.set_label('Intensity', color=fg_color)

        cba.outline.set_edgecolor(fg_color)


        cbb.ax.xaxis.set_tick_params(color=fg_color, rotation=90)

        cbb.set_label('Lifetime', color=fg_color)

        cbb.outline.set_edgecolor(fg_color)
        plt.setp(plt.getp(cbb.ax.axes, 'xticklabels'), color=fg_color)
        plt.setp(plt.getp(cba.ax.axes, 'yticklabels'), color=fg_color)
        plt.axis('tight')
        b =BytesIO()
        FigureCanvas(fig).print_png(b)
        plt.close()
        b.seek(0)
        image=Image.open(b)

        return image
    elif isinstance(img[0],np.ndarray) and not isinstance(img[1],np.ndarray):
        fg_color = 'white'
        px = 1/plt.rcParams['figure.dpi']

        
        
        fig,ax = plt.subplots(figsize=((width*px),(height*px)),facecolor='black')
        
        
        fig.subplots_adjust(top=0.9, bottom=0.1, right=1, left=0, hspace=0, wspace=0)
        ax.margins(0, 0,)
        ax.axis('off')

        pa = ax.imshow(img[0],cmap='gray')
        cba = plt.colorbar(pa,shrink=1,location = 'right',anchor=(-0.3,1))
        
        
        cba.ax.yaxis.set_tick_params(color=fg_color)
        cba.set_label('Intensity', color=fg_color)

        cba.outline.set_edgecolor(fg_color)


    

    

    
        
        plt.setp(plt.getp(cba.ax.axes, 'yticklabels'), color=fg_color)
        plt.axis('tight')
        b =BytesIO()
        FigureCanvas(fig).print_png(b)
        plt.close()
        b.seek(0)
        image=Image.open(b)
        return image
    elif not isinstance(img[0],np.ndarray) and isinstance(img[1],np.ndarray):
        fg_color = 'white'
        px = 1/plt.rcParams['figure.dpi']

        
        
        fig,ax = plt.subplots(figsize=((width*px),(height*px)),facecolor='black')
        
        
        fig.subplots_adjust(top=1, bottom=-0.15, right=0.90, left=0.1, hspace=0, wspace=0)
        ax.margins(0, 0,)
        ax.axis('off')

        
        
        pb = ax.imshow(img[1],cmap='rainbow',alpha=1)
        for spine in pb.axes.spines.values():
            spine.set_edgecolor(fg_color) 
        cbb = plt.colorbar(pb,location = 'bottom',shrink=1,anchor=(0.5,2.2))
    
    

    


        cbb.ax.xaxis.set_tick_params(color=fg_color, rotation=90)

        cbb.set_label('Lifetime', color=fg_color)

        cbb.outline.set_edgecolor(fg_color)
        plt.setp(plt.getp(cbb.ax.axes, 'xticklabels'), color=fg_color)
        
        plt.axis('tight')
        b =BytesIO()
        FigureCanvas(fig).print_png(b)
        plt.close()
        b.seek(0)
        image=Image.open(b)
        
        return image
    else:
        pass



def import_ROI(sender,app_data,user_data):
    
    global DF, DF2,pck_list,roi_1,roi_2
    
    global directory, new_directory,last_directory
    directory = app_data['file_path_name']
    new_directory=directory
    last_directory=directory
    update_dialogs_default_directory(last_directory)
    

    roi = load_ROI(app_data['file_path_name'])

    
    if user_data == 'Add_ROI_1_button':
        try:
            roi_1 = roi.to_numpy()
            
            DF = DF*roi_1
            chan = 1
            
        except:
            show_error_no_files('PTU file loaded. Try again.')
    if user_data == 'Add_ROI_2_button':
        try:
            roi_2 = roi.to_numpy()
            DF2 = DF2*roi_2
            chan = 2
        except:
            show_error_no_files('PTU file loaded. Try again.')


    if len(pck_list)==2:
        chan = 'both'
        display_images([DF,DF2],chan)
    else:
        display_images([DF],chan)
    

    
    
    

    


def join_dicts(dict1,dict2):
    output = {**dict1, **dict2}
    return output





def load_PTU_images(an_file):
    
    global anal_file, pck_files,PTU_directory, DF, DF2,pck_list,ROI_directory,roi_1,roi_2,Channels,last_directory

    global PTU_Resolution,PTU_Px_size,PTU_N_frames,PTU_Px_dwell
    global Current_image_1,Current_image_2
    global NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME
    
    
    
    
    
    
    
    
    
    info_file = os.path.join(PTU_directory,an_file+'.info')
    f = open(info_file)
    ptu_meta = json.load(f)    
    try:
        DF=DF2=[]
    except:
        pass
    
    PTU_Resolution = str(ptu_meta['Pixels per line'])+'x'+str(ptu_meta['Number of lines'])
    PTU_Px_size = ptu_meta['Pixels size']
    PTU_N_frames = ptu_meta['Number of frames']
    PTU_Px_dwell = ptu_meta['Pixel dwell']
    tau_resolution = ptu_meta['Lifetime resolution']
    
    dpg.set_value('Resolution_output','Resolution: '+PTU_Resolution)
    dpg.set_value('Pixel_size_output',PTU_Px_size)
    dpg.set_value('Nframes_output',PTU_N_frames)
    dpg.set_value('Pixel_dwell_output',PTU_Px_dwell)
    
    dpg.set_value('sinle_phot_output_ch_1',0)
    dpg.set_value('sinle_phot_err_output_ch_1',0)
    dpg.set_value('sinle_mols_output_ch_1',0)
    dpg.set_value('sinle_mols_err_output_ch_1',0)
    dpg.set_value('single_conc_output_ch_1',0)
    dpg.set_value('single_conc_err_output_ch_1',0)
    dpg.set_value('sinle_phot_output_ch_2',0)
    dpg.set_value('sinle_phot_err_output_ch_2',0)
    dpg.set_value('sinle_mols_output_ch_2',0)
    dpg.set_value('sinle_mols_err_output_ch_2',0)
    dpg.set_value('single_conc_output_ch_2',0)
    dpg.set_value('single_conc_err_output_ch_2',0)
    if PTU_N_frames>1:
        PTU_N_frames = PTU_N_frames-1
    else:
        pass
    ptu_files = list(np.sort([f for f in os.listdir(PTU_directory) if f.endswith('.ptu')]))
    
    
    

    
    
    npy_files = list(np.sort([f for f in os.listdir(PTU_directory) if f.startswith(an_file+'_')]))
    npy_files = [f for f in npy_files if f.endswith('.npy')]

    Channels = [f[-8:-4].split('_')[1] for f in npy_files if '_INT_ch_'in f]

    
    
    if dpg.get_value('AUTO_ROI_checkbox'):
        if ROI_directory == None:
            show_error_no_files('No ROI folder defined. Try again.')
        else:
            if dpg.get_value('LT_TO_ROI_checkbox'):
                
                if len(Channels)==1:
                    if '1' in Channels[0]:
                        Intensity_1 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))

                        Lifetime_1 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                        lt_mask = Lifetime_1/Lifetime_1
                        Intensity_1 = Intensity_1*lt_mask

                        



    
    
                        roi_1_path = os.path.join(ROI_directory,an_file + '_roi_ch_1.dat')
                        roi_1 = load_ROI(roi_1_path).to_numpy()
    
                        Intensity_1 = Intensity_1*roi_1
                        Lifetime_1 = Lifetime_1*roi_1
                        channel = 'both'

                        Current_image_1 = (Intensity_1,Lifetime_1)
                        
                        Current_image_2 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
                        display_images([Current_image_1,Current_image_2],channel)
                    elif '2' in Channels[0]:
                        Intensity_2 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))

                        Lifetime_2 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                        lt_mask = Lifetime_2/Lifetime_2
                        Intensity_2 = Intensity_2*lt_mask
                        
                        

    
    
                        roi_2_path = os.path.join(ROI_directory,an_file + '_roi_ch_2.dat')
                        roi_2 = load_ROI(roi_2_path).to_numpy()
    
                        Intensity_2 = Intensity_2*roi_2
                        Lifetime_2 = Lifetime_2*roi_2
                        channel = 'both'
                        Current_image_1 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
                        Current_image_2 = (Intensity_2,Lifetime_2)
                        display_images([Current_image_1,Current_image_2],channel)
    
    
    
    
    
    
    
    
                    else:
                        pass
            else:
                if len(Channels)==1:
                    if '1' in Channels[0]:
                        Intensity_1 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))
                        Lifetime_1 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                        
                        Intensity_1 = Intensity_1


    
    
                        roi_1_path = os.path.join(ROI_directory,an_file + '_roi_ch_1.dat')
                        roi_1 = load_ROI(roi_1_path).to_numpy()
    
                        Intensity_1 = Intensity_1*roi_1
                        Lifetime_1 = Lifetime_1*roi_1
                        channel = 'both'

                        Current_image_1 = (Intensity_1,Lifetime_1)
                        
                        Current_image_2 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
                        display_images([Current_image_1,Current_image_2],channel)
                    elif '2' in Channels[0]:
                        Intensity_2 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))

                        Lifetime_2 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                        lt_mask = Lifetime_2/Lifetime_2
                        Intensity_2 = Intensity_2


    
    
                        roi_2_path = os.path.join(ROI_directory,an_file + '_roi_ch_2.dat')
                        roi_2 = load_ROI(roi_2_path).to_numpy()
    
                        Intensity_2 = Intensity_2*roi_2
                        Lifetime_2 = Lifetime_2*roi_2
                        channel = 'both'
                        Current_image_1 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
                        Current_image_2 = (Intensity_2,Lifetime_2)
                        display_images([Current_image_1,Current_image_2],channel)
    
    
    
    
    
    
    
    
                    else:
                        pass



             
                elif len(Channels)==2:
                    
                    Intensity_1 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))                    
                    Lifetime_1 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                    Intensity_2 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[1]+'.npy'))
                    Lifetime_2 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[1]+'.npy'))
                    lt_mask = Lifetime_1/Lifetime_1
                    Intensity_1 = Intensity_1
                    lt_mask = Lifetime_2/Lifetime_2
                    Intensity_2 = Intensity_2
                    roi_1_path = os.path.join(ROI_directory,an_file + '_roi_ch_1.dat')
                    roi_1 = load_ROI(roi_1_path).to_numpy()
                    Intensity_1 = Intensity_1*roi_1
                    Lifetime_1 = Lifetime_1*roi_1
                    roi_2_path = os.path.join(ROI_directory,an_file + '_roi_ch_2.dat')
                    roi_2 = load_ROI(roi_2_path).to_numpy()
                    Intensity_2 = Intensity_2*roi_2
                    Lifetime_2 = Lifetime_2*roi_2


                    channel = 'both'

                    Current_image_1 = (Intensity_1,Lifetime_1)
                    Current_image_2 = (Intensity_2,Lifetime_2)
                    display_images([Current_image_1,Current_image_2],channel)
                    
            
                
                
    else:
        if dpg.get_value('LT_TO_ROI_checkbox'):
            if len(Channels)==1:
                if '1' in Channels[0]:
                    Intensity_1 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))                    
                    Lifetime_1 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                    lt_mask = Lifetime_1/Lifetime_1
                    Intensity_1 = Intensity_1*lt_mask
                    channel = 'both'

                    Current_image_1 = (Intensity_1,Lifetime_1)
                    
                    Current_image_2 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
                    display_images([Current_image_1,Current_image_2],channel)
                elif '2' in Channels[0]:
                    Intensity_2 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))                    
                    Lifetime_2 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                    lt_mask = Lifetime_2/Lifetime_2
                    Intensity_2 = Intensity_2*lt_mask
    


    

                    lt_mask = Lifetime_2/Lifetime_2
                    Intensity_2 = Intensity_2*lt_mask
                    channel = 'both'
                    Current_image_1 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
                    Current_image_2 = (Intensity_2,Lifetime_2)
                    display_images([Current_image_1,Current_image_2],channel)
    


    
                else:
                    pass
            elif len(Channels)==2:
                Intensity_1 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))                    
                Lifetime_1 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                Current_image_1 = (Intensity_1,Lifetime_1)
                Intensity_2 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[1]+'.npy'))                    
                Lifetime_2 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[1]+'.npy'))
                lt_mask = Lifetime_1/Lifetime_1
                Intensity_1 = Intensity_1*lt_mask
                lt_mask = Lifetime_2/Lifetime_2
                Intensity_2 = Intensity_2*lt_mask

                channel = 'both'
                Current_image_2 = (Intensity_2,Lifetime_2)
                display_images([Current_image_1,Current_image_2],channel)
        else:
            if len(Channels)==1:
                if '1' in Channels[0]:
                    Intensity_1 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))                    
                    Lifetime_1 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                    lt_mask = Lifetime_1/Lifetime_1
                    Intensity_1 = Intensity_1
                    channel = 'both'

                    Current_image_1 = (Intensity_1,Lifetime_1)
                    
                    Current_image_2 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
                    display_images([Current_image_1,Current_image_2],channel)
                elif '2' in Channels[0]:
                    Intensity_2 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))                    
                    Lifetime_2 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                    lt_mask = Lifetime_2/Lifetime_2
                    Intensity_2 = Intensity_2
    


    

                    
                    
                    channel = 'both'
                    Current_image_1 = (NO_IMAGE_INTENSITY,NO_IMAGE_LIFETIME)
                    Current_image_2 = (Intensity_2,Lifetime_2)
                    display_images([Current_image_1,Current_image_2],channel)
    


    
                else:
                    pass
            elif len(Channels)==2:
                Intensity_1 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[0]+'.npy'))                    
                Lifetime_1 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[0]+'.npy'))
                Current_image_1 = (Intensity_1,Lifetime_1)
                Intensity_2 = np.load(os.path.join(PTU_directory,an_file+'_INT_ch_'+Channels[1]+'.npy'))                    
                Lifetime_2 = np.load(os.path.join(PTU_directory,an_file+'_LT_ch_'+Channels[1]+'.npy'))
                lt_mask = Lifetime_1/Lifetime_1
                Intensity_1 = Intensity_1
                lt_mask = Lifetime_2/Lifetime_2
                Intensity_2 = Intensity_2

                channel = 'both'
                Current_image_2 = (Intensity_2,Lifetime_2)
                display_images([Current_image_1,Current_image_2],channel)














        

    
    
    


def load_ROI(path):
    df=pd.read_csv(path, sep='\t',header=None,skiprows=3,encoding ='latin1')
    df=df.replace('-',-1.)
    
    try:
        df=df.astype(float)
    except:
        for i in df.index:
            try:
                df.at[i,0]=float(df.at[i,0])
                
            except:
            
            
            
            
            
                ind =i
                break
        df = df[df.index<ind]
        df=df.astype(int)
    
    
    dfs=df[0].to_frame().applymap(np.isreal)

    if len(dfs.mask(dfs).dropna()) != 0:
        ind = int(dfs.mask(dfs).dropna().head(1).index.values) 
        
        df = df[df.index<ind]
        df = df.astype(float)
        df=df.mask(df!=-1,1)
        df = df.where(df!=-1,np.nan)
    else:
        df = df.astype(float)
        df=df.mask(df!=-1,1)
        df = df.where(df!=-1,np.nan)
    




    return df

    

    




    


    


def mean_bright_input_ch_1():
    global FCS_results_ch_1,mean_brightness, mean_brightness_err
    mean_brightness_ch_1  = FCS_results_ch_1.Brightness.mean()
    mean_brightness_err_ch_1 = FCS_results_ch_1.Brightness.std(ddof=1)
    dpg.configure_item('Brightness_input_ch_1',default_value = mean_brightness_ch_1 )
    dpg.configure_item('Brightness_err_input_ch_1',default_value = mean_brightness_err_ch_1 )



def mean_bright_input_ch_2():
    global FCS_results_ch_2,mean_brightness, mean_brightness_err
    
    
    mean_brightness_ch_2  = FCS_results_ch_2.Brightness.mean()
    mean_brightness_err_ch_2 = FCS_results_ch_2.Brightness.std(ddof=1)
    dpg.configure_item('Brightness_input_ch_2',default_value = mean_brightness_ch_2 )
    dpg.configure_item('Brightness_err_input_ch_2',default_value = mean_brightness_err_ch_2 )

    
    


def mount_bright_table(sender):
    if sender == 'TT_file_dialog_id_ch_1':
        with dpg.window(pos=curr_position['show_TT_res_win_ch_1'],
                            width=curr_widths['show_TT_res_win_ch_1'],
                            tag='show_TT_res_win_ch_1',
                            show=False,
                            autosize=True,
                            horizontal_scrollbar=True,
                            modal=True
                              ):
                row_number_count = 0
                with dpg.table(header_row=True,show=True,tag='table_results_show_ch_1',policy=dpg.mvTable_SizingFixedFit, resizable=True,):
                    dpg.add_table_column(label='File',tag='column_results_show_file_ch_1',init_width_or_weight =200)
                    dpg.add_table_column(label='N_p',tag='column_results_show_N_p_ch_1',init_width_or_weight =50)
                    dpg.add_table_column(label='Brightness',tag='column_results_show_Brightness_ch_1',init_width_or_weight =70)
                    dpg.add_table_column(label='Remove?',tag='column_results_show_del_ch_1',init_width_or_weight =70)
                    for i in FCS_results_ch_1.index:
                        with dpg.table_row(tag='ch_1_row_results_show_ch_1'+str(i)):

                            dpg.add_text(FCS_results_ch_1.at[i,'file'],tag='ch_1_results_show_'+str(i)+'_name_ch_1')
                            dpg.add_text(np.round(FCS_results_ch_1.at[i,'N_p'],2),tag='ch_1_results_show_'+str(i)+'_N_p_value_ch_1')
                            dpg.add_text(int(FCS_results_ch_1.at[i,'Brightness']),tag='ch_1_results_show_'+str(i)+'_Brightness_value_ch_1')
                            dpg.add_checkbox(label='',
                                             tag='ch_1_results_delete_'+str(i)+'_check_ch_1')
                with dpg.group(tag='group_close_results_table_ch_1',parent='show_TT_res_win_ch_1',horizontal=True,horizontal_spacing=init_group_spacer, show=True):
                    dpg.add_button(label='Close',
                                   tag='close_button_results_ch_1',
                                   parent='group_close_results_table_ch_1',
                                   width = curr_widths['close_button_results_ch_1'],
                                   callback=lambda:dpg.configure_item('show_TT_res_win_ch_1',show=False)
                                  )
                    dpg.add_button(label='Remove',
                                   parent='group_close_results_table_ch_1',
                                   tag='remove_button_results_ch_1',
                                   width = curr_widths['remove_button_results_ch_1'],
                                   callback=callback_remove_result_button,
                                   show=True
                                  )
    else:
        with dpg.window(pos=curr_position['show_TT_res_win_ch_2'],
                            width=curr_widths['show_TT_res_win_ch_2'],
                            tag='show_TT_res_win_ch_2',
                            show=False,
                            autosize=True,
                            horizontal_scrollbar=True,
                            modal=True
                              ):
                row_number_count = 0
                with dpg.table(header_row=True,show=True,tag='table_results_show_ch_2',policy=dpg.mvTable_SizingFixedFit, resizable=True,):
                    dpg.add_table_column(label='File',tag='column_results_show_file_ch_2',init_width_or_weight =200)
                    dpg.add_table_column(label='N_p',tag='column_results_show_N_p_ch_2',init_width_or_weight =50)
                    dpg.add_table_column(label='Brightness',tag='column_results_show_Brightness_ch_2',init_width_or_weight =70)
                    dpg.add_table_column(label='Remove?',tag='column_results_show_del_ch_2',init_width_or_weight =70)
                    for i in FCS_results_ch_2.index:
                        with dpg.table_row(tag='ch_2_row_results_show'+str(i)):

                            dpg.add_text(FCS_results_ch_2.at[i,'file'],tag='ch_2_results_show_'+str(i)+'_name_ch_2')
                            dpg.add_text(np.round(FCS_results_ch_2.at[i,'N_p'],2),tag='ch_2_results_show_'+str(i)+'_N_p_value_ch_2')
                            dpg.add_text(int(FCS_results_ch_2.at[i,'Brightness']),tag='ch_2_results_show_'+str(i)+'_Brightness_value_ch_2')
                            dpg.add_checkbox(label='',
                                             tag='ch_2_results_delete_'+str(i)+'_check_ch_2')
                with dpg.group(tag='group_close_results_table_ch_2',parent='show_TT_res_win_ch_2',horizontal=True,horizontal_spacing=init_group_spacer, show=True):
                    dpg.add_button(label='Close',
                                   tag='close_button_results_ch_2',
                                   parent='group_close_results_table_ch_2',
                                   width = curr_widths['close_button_results_ch_2'],
                                   callback=lambda:dpg.configure_item('show_TT_res_win_ch_2',show=False)
                                  )
                    dpg.add_button(label='Remove',
                                   parent='group_close_results_table_ch_2',
                                   tag='remove_button_results_ch_2',
                                   width = curr_widths['remove_button_results_ch_2'],
                                   callback=callback_remove_result_button,
                                   show=True
                                  )
    
    
    


def show_error_no_files(error_text):
    try:
        with dpg.window(pos=(400,150),
                       label='Error!',
                           tag='No_data_files',

                           no_move=True,
                            no_close=False,
                            no_title_bar=False,
                            no_resize=True,
                           show=True,
                           modal=True
                          ):
            dpg.add_text(error_text,tag='no_files_error_text')
            

            dpg.add_button(label='Close',
                           tag='no_files_error_butt',
                           show=True,
                           callback=callback_no_files_dialog_close_only
                          )
            
            dpg.bind_item_theme('No_data_files', 'Error_window_theme')
    except:
        dpg.show_item('No_data_files')

        


def unmount_bright_table(sender):
    if sender == 'TT_file_dialog_id_ch_1':
        items_to_remove = ['remove_button_results_ch_1','group_close_results_table_ch_1','group_close_results_table_ch_1']
        
        for i in FCS_results_ch_1.index:
            items_to_remove.append('ch_1_results_delete_'+str(i)+'_check_ch_1')
            items_to_remove.append('ch_1_results_show_'+str(i)+'_Brightness_value_ch_1')
            items_to_remove.append('ch_1_results_show_'+str(i)+'_N_p_value_ch_1')
            items_to_remove.append('ch_1_results_show_'+str(i)+'_name_ch_1')
            items_to_remove.append('ch_1_row_results_show_ch_1'+str(i))
        items_to_remove.append('column_results_show_del_ch_1')
        items_to_remove.append('column_results_show_Brightness_ch_1')
        items_to_remove.append('column_results_show_N_p_ch_1')
        items_to_remove.append('column_results_show_file_ch_1')
        items_to_remove.append('table_results_show_ch_1')
        items_to_remove.append('show_TT_res_win_ch_1')
        
        
        for item in items_to_remove:
            dpg.delete_item(item)
    else:
        items_to_remove = ['remove_button_results_ch_2','group_close_results_table_ch_2','group_close_results_table_ch_2']
        
        for i in FCS_results_ch_2.index:
            items_to_remove.append('ch_2_results_delete_'+str(i)+'_check_ch_2')
            items_to_remove.append('ch_2results_show_'+str(i)+'_Brightness_value_ch_2')
            items_to_remove.append('ch_2_results_show_'+str(i)+'_N_p_value_ch_2')
            items_to_remove.append('ch_2_results_show_'+str(i)+'_name_ch_2')
            items_to_remove.append('ch_2_row_results_show_ch_2'+str(i))
        items_to_remove.append('column_results_show_del_ch_2')
        items_to_remove.append('column_results_show_Brightness_ch_2')
        items_to_remove.append('column_results_show_N_p_ch_2')
        items_to_remove.append('column_results_show_file_ch_2')
        items_to_remove.append('table_results_show_ch_2')
        items_to_remove.append('show_TT_res_win_ch_2')
        
        for item in items_to_remove:
            dpg.delete_item(item)
                                   


def update_dialogs_default_directory(last_directory):
    # print(last_directory)
    dpg.configure_item('TT_file_dialog_id_ch_2',default_path=last_directory)
    dpg.configure_item('TT_file_dialog_id_ch_1',default_path=last_directory)
    
    dpg.configure_item('ROI_folder_dialog_id',default_path=last_directory)
    dpg.configure_item('file_dialog_id',default_path=last_directory)
    dpg.configure_item('PTU_file_dialog_id',default_path=last_directory)
    dpg.configure_item('Select_ROI_dialog',default_path=last_directory)
    dpg.configure_item('file_dialog_export',default_path=last_directory)
    dpg.configure_item('Calib_file_dialog_id',default_path=last_directory)
    
    
    
    


def update_flist(fs):
    '''Updates the filelist. '''
    
    
    if not len(fs)==0:
        try:
            dpg.configure_item("file_box", items=fs)

            dpg.configure_item("file_box", default_value=fs[0])
        except:
            pass
    else:
        dpg.configure_item("file_box", items=())
        dpg.configure_item("file_box", default_value='')        

        


def wdt_hgt_pos(item,wdth,hght,pos):
    dct = locals()
    
    lista = [dct[f] for f in dct.keys()]
    if not dct['wdth']== None:
        dpg.set_item_width(item,wdth)
    if not dct['hght']== None:
        dpg.set_item_height(item,hght)
        
    if not dct['pos']== None:
        dpg.set_item_pos(item,pos)
    
        
        
        
    

def callback_exportsettings(sender,app_data):
    global ROI_directory,PTU_directory,calib_directory
    setts = {
        'Calib_data':{
                        'Calib_file_path': calib_directory,
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
        'PTU_files_dir':PTU_directory,
        'ROI_file_dir': ROI_directory,
        'Export_opts':{
                        'Photons to array':dpg.get_value('Photons_array_checkbox'),
                        'Photons to heatmap':dpg.get_value('Photons_Hmaps_checkbox'),
                        'N_p to array':dpg.get_value('Np_array_checkbox'),
                        'N_p to heatmap':dpg.get_value('Np_Hmaps_checkbox'),
                        'Conc. to array':dpg.get_value('C_array_checkbox'),
                        'Conc. to heatmap':dpg.get_value('C_Hmaps_checkbox')
            
            
                        },
        'Error_notation':dpg.get_value('Error_type_checkbox')
        
        
            }
    
    
    
    print(setts)
    if PTU_directory !=None:
        path_to_json_file = os.path.join(PTU_directory,'workspace_info.json')
        with open(path_to_json_file, 'w') as f:
            json.dump(setts, f, indent=4, sort_keys=False)
    else:
        print('Select PTU directory, at least!')