def rewrtie_roi(file,input_folder,output_roi_path,shape):
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
    
    
def rewrtie_roi_txt(file,input_folder,output_roi_path,shape):
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


def callback_open_source_folder(sender,app_data):

    global source_type
    source_type = None
    path = app_data['file_path_name']
    dpg.set_value('tag_source_path',path)
    
    files = os.listdir(path)
    csv_files = [f for f in files if f.endswith('.csv')]
    dat_files = [f for f in files if f.endswith('.txt')]
    global data_files
    
    if len(csv_files)!=0:
        data_files = csv_files
        dpg.configure_item('file_box',items=data_files)
        source_type = 'csv'


            

    elif len(dat_files)!=0:
        data_files = dat_files
        dpg.configure_item('file_box',items=data_files)
        source_type = 'txt'



    else:
        pass
    

    
def callback_open_target_folder(sender,app_data):
    dpg.set_value('tag_target_path',app_data['file_path_name'])

    
def callback_empty(sender,app_data):
    '''Empty function. Do nothing.'''
    pass

def callback_no_files_dialog_close_only(sender,app_data):
    dpg.configure_item('No_data_files',show=False)
    dpg.delete_item('no_files_error_text')
    dpg.delete_item('no_files_error_butt')
    dpg.delete_item('No_data_files')

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


def show_done(error_text):
    try:
        with dpg.window(pos=(400,150),
                       label='',
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



def callback_proceed(sender,app_data):
    global data_files
    global source_type
    
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
        if len(data_files) == 0:
            show_error_no_files('No files selected')
        else:
            input_folder = dpg.get_value('tag_source_path')
            ROI_folder = dpg.get_value('tag_target_path')
            if input_folder != '':
                if ROI_folder != '':
                    error = False
                    for file in data_files:

                        dpg.configure_item('file_box',default_value=file)
    
    
                        if source_type == 'csv':
                            rewrtie_roi(file,input_folder,ROI_folder,resolution)

                        elif source_type == 'txt':
                            rewrtie_roi_txt(file,input_folder,ROI_folder,resolution)
                        else:
                            
                            error = True
                    if error == True:
                        show_error_no_files('Something gone wrong!')
                    else:
                        show_done('DONE')
                else:
                    show_error_no_files('Select target folder!')
            else:
                show_error_no_files('Select source folder!')
                
        
        
    else:
        show_error_no_files('Wrong resolution')
