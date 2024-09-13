import sys
import json
from pprint import pprint
import os
import numpy as np
import pandas as pd
from scipy.stats import median_abs_deviation
from numpy import log10, sqrt, exp, log, pi

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
from PIL import Image
import pyautogui
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import datetime




class CLI:
    def __init__(self, workspace_path,output_path,output_format):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y%m%d_%H%M")
        
        

        if os.path.isfile(workspace_path):
            self.workspace_path = workspace_path
        else:
            print('Provide a correct path to the workspace file. Try again!')
            sys.exit(1)

        if os.path.isdir(output_path):
            self.output_path = output_path
            self.output_format =output_format
        else:
            print('Provide a correct path to the output folder. Try again!')
            sys.exit(1)
            
        
        if self.is_json_file(self.workspace_path):
            if self.output_format == 'excel' :
                ext = '.xlsx'
                self.output_results_path = os.path.join(self.output_path,str(formatted_time)+'_results'+ext)
                self.logfile_path = os.path.join(self.output_path,str(formatted_time)+'_log.txt')
                

            elif self.output_format == 'dat' :
                ext = '.dat'
                self.output_results_path = os.path.join(self.output_path,str(formatted_time)+'_results'+ext)
                self.logfile_path = os.path.join(self.output_path,str(formatted_time)+'_log.txt')
                
            elif self.output_format == 'csv' :
                ext = '.csv'
                self.output_results_path = os.path.join(self.output_path,str(formatted_time)+'_results'+ext)
                self.logfile_path = os.path.join(self.output_path,str(formatted_time)+'_log.txt')
            elif self.output_format == 'pickle' :
                ext = '.pickle'
                self.output_results_path = os.path.join(self.output_path,str(formatted_time)+'_results'+ext)
                self.logfile_path = os.path.join(self.output_path,str(formatted_time)+'_log.txt')
            else:
                print('Wrong output format. Allowed formats are: excel, dat, csv, or pickle. Try again!')
                sys.exit(1)
            
            
            
            self.setts = self.read_json(self.workspace_path)
            self.PTU_directory_path = self.setts['PTU_files_dir']
            self.ptu_files = self.load_ptu_file_names(self.PTU_directory_path)
            self.DF = self.DF2 = []
            self.ROI_directory_path = self.setts['ROI_file_dir']
            self.Sing_Results_DF = pd.DataFrame(columns=['File',
                                                        'Channel',
                                                        '<Counts>',
                                                        'Counts_std',
                                                        '<N_p>',
                                                        'N_p_err',
                                                        '<C>',
                                                        'C_err',
                                                        'C_median',
                                                        'C_median_abs_err'])
        else:
            print('This is not a right workspace file!')
            print('TERMINATING')
            sys.exit(1)
    def log_it(self,text_to_log,mode):
    
        logf = open(self.logfile_path, mode)
        
        logf.write(text_to_log+'\n')
        
        logf.close()
    def print_init(self):
        print('Executing script\n\n')
        print('================\n\n')
        print("Path to PTU folder:\t",self.PTU_directory_path)
        self.log_it("Path to PTU folder:\t"+str(self.PTU_directory_path),'w')

        print("Path to ROI folder:\t",self.ROI_directory_path)
        self.log_it("Path to ROI folder:\t"+str(self.ROI_directory_path),'a')

        print("Path to output folder:\t",self.output_path)
        self.log_it("Path to output folder:\t"+str(self.output_path),'a')

        print("output file format:\t",self.output_format)
        self.log_it("output file format:\t"+str(self.output_format),'a')

        print("\nCalibration data:")
        self.log_it("\nCalibration data:",'a')
        
        print('\tPath to calibration file:')
        self.log_it('\tPath to calibration file:','a')
        
        print('\t\t',self.setts['Calib_data']['Calib_file_path'])
        self.log_it('\t\t'+str(self.setts['Calib_data']['Calib_file_path']),'a')

        print('\tChannel 1')
        self.log_it('\tChannel 1','a')
        
        print('\t\tMolecular brightness (cnts/molecule/sec):\t',self.setts['Calib_data']['Ch_1_B'],'+/-',self.setts['Calib_data']['Ch_1_B_err'])
        self.log_it('\t\tMolecular brightness (cnts/molecule/sec):\t'+str(self.setts['Calib_data']['Ch_1_B'])+'+/-'+str(self.setts['Calib_data']['Ch_1_B_err']),'a')
        
        print('\t\tFocal volume (fL):\t\t\t\t',self.setts['Calib_data']['Ch_1_V0'],'+/-',self.setts['Calib_data']['Ch_1_V0_err'])
        self.log_it('\t\tFocal volume (fL):\t\t\t\t'+str(self.setts['Calib_data']['Ch_1_V0'])+'+/-'+str(self.setts['Calib_data']['Ch_1_V0_err']),'a')
        
        print('\t\tStructutre parameter, \u03BA:\t\t\t',self.setts['Calib_data']['Ch_1_kappa'],'+/-',self.setts['Calib_data']['Ch_1_kappa_err'])
        self.log_it('\t\tStructutre parameter, \u03BA:\t\t\t'+str(self.setts['Calib_data']['Ch_1_kappa'])+'+/-'+str(self.setts['Calib_data']['Ch_1_kappa_err']),'a')
        
        print('\t\tWidth of focal volume, \u03C9 (\u03BCm):\t\t\t',self.setts['Calib_data']['Ch_1_omega'],'+/-',self.setts['Calib_data']['Ch_1_omega_err'])
        self.log_it('\t\tWidth of focal volume, \u03C9 (\u03BCm):\t\t\t'+str(self.setts['Calib_data']['Ch_1_omega'])+'+/-'+str(self.setts['Calib_data']['Ch_1_omega_err']),'a')

        print('\tChannel 2')
        self.log_it('\tChannel 2','a')
        
        print('\t\tMolecular brightness (cnts/molecule/sec):\t',self.setts['Calib_data']['Ch_2_B'],'+/-',self.setts['Calib_data']['Ch_2_B_err'])
        self.log_it('\t\tMolecular brightness (cnts/molecule/sec):\t'+str(self.setts['Calib_data']['Ch_2_B'])+'+/-'+str(self.setts['Calib_data']['Ch_2_B_err']),'a')
        
        print('\t\tFocal volume (fL):\t\t\t\t',self.setts['Calib_data']['Ch_2_V0'],'+/-',self.setts['Calib_data']['Ch_2_V0_err'])
        self.log_it('\t\tFocal volume (fL):\t\t\t\t'+str(self.setts['Calib_data']['Ch_2_V0'])+'+/-'+str(self.setts['Calib_data']['Ch_2_V0_err']),'a')
        
        print('\t\tStructutre parameter, \u03BA:\t\t\t',self.setts['Calib_data']['Ch_2_kappa'],'+/-',self.setts['Calib_data']['Ch_2_kappa_err'])
        self.log_it('\t\tStructutre parameter, \u03BA:\t\t\t'+str(self.setts['Calib_data']['Ch_2_kappa'])+'+/-'+str(self.setts['Calib_data']['Ch_2_kappa_err']),'a')
        
        print('\t\tWidth of focal volume , \u03C9 (\u03BCm):\t\t\t',self.setts['Calib_data']['Ch_2_omega'],'+/-',self.setts['Calib_data']['Ch_2_omega_err'])
        self.log_it('\t\tWidth of focal volume , \u03C9 (\u03BCm):\t\t\t'+str(self.setts['Calib_data']['Ch_2_omega'])+'+/-'+str(self.setts['Calib_data']['Ch_2_omega_err']),'a')

        print('\n\tErrors as SD:\t',self.setts['Error_notation'])
        self.log_it('\n\tErrors as SD:\t'+str(self.setts['Error_notation']),'a')

        print('\n\tExport options:\t')
        self.log_it('\n\tExport options:\t','a')
        
        print('\t\t Photons to array:\t\t\t',self.setts['Export_opts']['Photons to array'])
        self.log_it('\t\t Photons to array:\t\t\t'+str(self.setts['Export_opts']['Photons to array']),'a')
        
        print('\t\t Photons to heatmap:\t\t\t',self.setts['Export_opts']['Photons to heatmap'])
        self.log_it('\t\t Photons to heatmap:\t\t\t'+str(self.setts['Export_opts']['Photons to heatmap']),'a')
        

        print('\t\t Number of molecules to array:\t\t',self.setts['Export_opts']['N_p to array'])
        self.log_it('\t\t Number of molecules to array:\t\t'+str(self.setts['Export_opts']['N_p to array']),'a')
        
        print('\t\t Number of molecules to heatmap:\t',self.setts['Export_opts']['N_p to heatmap'])
        self.log_it('\t\t Number of molecules to heatmap:\t'+str(self.setts['Export_opts']['N_p to heatmap']),'a')

        
        print('\t\t Concentration to array:\t\t',self.setts['Export_opts']['Conc. to array'])
        self.log_it('\t\t Concentration to array:\t\t'+str(self.setts['Export_opts']['Conc. to array']),'a')
        
        print('\t\t Concentration to heatmap:\t\t',self.setts['Export_opts']['Conc. to heatmap'])
        self.log_it('\t\t Concentration to heatmap:\t\t'+str(self.setts['Export_opts']['Conc. to heatmap']),'a')

        
    def is_json_file(self,file_path):
        try:
            with open(file_path, 'r') as file:
                json.load(file)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
            
    def read_json(self,file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def print_pretty_dict(self,dictionary):
        pprint(dictionary, indent=4)

    def load_ptu_file_names(self,path):
        ptu_files = os.listdir(path)
        ptu_files = list(np.sort([f for f in ptu_files if f.endswith('ptu')]))
        return ptu_files

    def calc_molecules(self,DF,PTU_Px_dwell,PTU_N_frames,brightness,brightness_err):
    
        PTU_Px_dwell = PTU_Px_dwell*1e-6
        MOL = ( DF*(1/(PTU_Px_dwell*PTU_N_frames)))/brightness
        part_BR = -DF/(PTU_N_frames*PTU_Px_dwell*(brightness**2))
        MOL_err = sqrt((part_BR**2)*(brightness_err**2))
        return MOL,MOL_err

    def CONC(self,N,V,N_err,V_err):
    
        Na = 6.022e23
        C = N/(Na*V)
        C_err = sqrt(((N**2)*(V_err**2))/((Na**2)*(V**4))+(N_err**2)/((Na**2)*(V**2)))
        return C, C_err

    
    def load_ROI(self,path):
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
    
    
    
    
    
    def load_ptu_file(self,file_name,path):
        PTU_directory = path
        self.an_file = file_name.replace('.ptu','')
        info_file = os.path.join(path,file_name.replace('.ptu','.info'))
        f = open(info_file)
        self.ptu_meta = json.load(f)

        
        
        self.PTU_Resolution = str(self.ptu_meta['Pixels per line'])+'x'+str(self.ptu_meta['Number of lines'])
        self.PTU_Px_size = self.ptu_meta['Pixels size']
        self.PTU_N_frames = self.ptu_meta['Number of frames']
        self.PTU_Px_dwell = self.ptu_meta['Pixel dwell']
        self.tau_resolution = self.ptu_meta['Lifetime resolution']

        if self.PTU_N_frames>1:
            self.PTU_N_frames = self.PTU_N_frames-1
        else:
            pass

        npy_files = list(np.sort([f for f in os.listdir(path) if f.startswith(self.an_file+'_')]))
        npy_files = [f for f in npy_files if f.endswith('.npy')]
    
        self.Channels = [f[-8:-4].split('_')[1] for f in npy_files if '_INT_ch_'in f]
        # print(npy_files)
        # print(self.Channels)
        ROI_directory = self.ROI_directory_path
        if self.ROI_directory_path != None:
            # print('something')

            if len(self.Channels)==1:
                if '1' in self.Channels[0]:
                    Intensity_1 = np.load(os.path.join(PTU_directory,
                                                       self.an_file+'_INT_ch_'+self.Channels[0]+'.npy'))
                    Lifetime_1 = np.load(os.path.join(PTU_directory,
                                                      self.an_file+'_LT_ch_'+self.Channels[0]+'.npy'))
                    lt_mask = Lifetime_1/Lifetime_1
                    Intensity_1 = Intensity_1*lt_mask
                    roi_1_path = os.path.join(ROI_directory,
                                              self.an_file + '_roi_ch_1.dat')
                    roi_1 = self.load_ROI(roi_1_path).to_numpy()
                    Intensity_1 = Intensity_1*roi_1
                    Lifetime_1 = Lifetime_1*roi_1
                    self.Current_image_1 = (Intensity_1,Lifetime_1)
                    self.Current_image_2 = (np.empty(Intensity_1.shape),
                                            np.empty(Lifetime_1.shape))
                elif '2' in self.Channels[0]:
                    Intensity_2 = np.load(os.path.join(PTU_directory,
                                                       self.an_file+'_INT_ch_'+self.Channels[0]+'.npy'))
                    Lifetime_2 = np.load(os.path.join(PTU_directory,
                                                      self.an_file+'_LT_ch_'+self.Channels[0]+'.npy'))
                    lt_mask = Lifetime_2/Lifetime_2
                    Intensity_2 = Intensity_2*lt_mask
                    roi_2_path = os.path.join(ROI_directory,
                                              self.an_file + '_roi_ch_2.dat')
                    roi_2 = self.load_ROI(roi_2_path).to_numpy()
                    Intensity_2 = Intensity_2*roi_2
                    Lifetime_2 = Lifetime_2*roi_2
                    
                    self.Current_image_2 = (Intensity_2,Lifetime_2)
                    self.Current_image_1 = (np.empty(Intensity_2.shape),
                                            np.empty(Lifetime_2.shape))
                else:
                    pass
            
            
            elif len(self.Channels)==2:
                    
                Intensity_1 = np.load(os.path.join(PTU_directory,
                                                   self.an_file+'_INT_ch_'+self.Channels[0]+'.npy'))                    
                Lifetime_1 = np.load(os.path.join(PTU_directory,
                                                  self.an_file+'_LT_ch_'+self.Channels[0]+'.npy'))
                Intensity_2 = np.load(os.path.join(PTU_directory,
                                                   self.an_file+'_INT_ch_'+self.Channels[1]+'.npy'))
                Lifetime_2 = np.load(os.path.join(PTU_directory,
                                                  self.an_file+'_LT_ch_'+self.Channels[1]+'.npy'))
                lt_mask = Lifetime_1/Lifetime_1
                Intensity_1 = Intensity_1
                lt_mask = Lifetime_2/Lifetime_2
                Intensity_2 = Intensity_2
                roi_1_path = os.path.join(ROI_directory,
                                          self.an_file + '_roi_ch_1.dat')
                roi_1 = self.load_ROI(roi_1_path).to_numpy()
                Intensity_1 = Intensity_1*roi_1
                Lifetime_1 = Lifetime_1*roi_1
                roi_2_path = os.path.join(ROI_directory,
                                          self.an_file + '_roi_ch_2.dat')
                roi_2 = self.load_ROI(roi_2_path).to_numpy()
                Intensity_2 = Intensity_2*roi_2
                Lifetime_2 = Lifetime_2*roi_2


                

                self.Current_image_1 = (Intensity_1,Lifetime_1)
                self.Current_image_2 = (Intensity_2,Lifetime_2)
                
                
        
        else:
            if len(self.Channels)==1:
                if '1' in self.Channels[0]:
                    Intensity_1 = np.load(os.path.join(PTU_directory,
                                                       self.an_file+'_INT_ch_'+self.Channels[0]+'.npy'))                    
                    Lifetime_1 = np.load(os.path.join(PTU_directory,
                                                      self.an_file+'_LT_ch_'+self.Channels[0]+'.npy'))
                    lt_mask = Lifetime_1/Lifetime_1
                    Intensity_1 = Intensity_1


                    self.Current_image_1 = (Intensity_1,Lifetime_1)
                    self.Current_image_2 = (np.empty(Intensity_1.shape),
                                            np.empty(Lifetime_1.shape))
                    


                elif '2' in self.Channels[0]:
                    Intensity_2 = np.load(os.path.join(PTU_directory,
                                                       self.an_file+'_INT_ch_'+self.Channels[0]+'.npy'))                    
                    Lifetime_2 = np.load(os.path.join(PTU_directory,
                                                      self.an_file+'_LT_ch_'+self.Channels[0]+'.npy'))
                    lt_mask = Lifetime_2/Lifetime_2
                    Intensity_2 = Intensity_2
    


    

    
                    self.Current_image_2 = (Intensity_2,Lifetime_2)
                    self.Current_image_1 = (np.empty(Intensity_2.shape),
                                            np.empty(Lifetime_2.shape))

    


    
                else:
                    pass
            elif len(self.Channels)==2:
                Intensity_1 = np.load(os.path.join(PTU_directory,
                                                   self.an_file+'_INT_ch_'+self.Channels[0]+'.npy'))                    
                Lifetime_1 = np.load(os.path.join(PTU_directory,
                                                  self.an_file+'_LT_ch_'+self.Channels[0]+'.npy'))
                self.Current_image_1 = (Intensity_1,Lifetime_1)
                Intensity_2 = np.load(os.path.join(PTU_directory,
                                                   self.an_file+'_INT_ch_'+self.Channels[1]+'.npy'))                    
                Lifetime_2 = np.load(os.path.join(PTU_directory,
                                                  self.an_file+'_LT_ch_'+self.Channels[1]+'.npy'))
                lt_mask = Lifetime_1/Lifetime_1
                Intensity_1 = Intensity_1
                lt_mask = Lifetime_2/Lifetime_2
                Intensity_2 = Intensity_2
                self.Current_image_2 = (Intensity_2,Lifetime_2)

    def calculate(self,anal_file):
        self.mean_Molecules_ch_1=None
        self.std_Molecules_ch_1=None
        self.mean_Concentration_ch_1=None
        self.std_Concentration_ch_1=None
        self.std_err_Concentration_ch_1=None
        self.median_C_ch_1=None
        self.median_err_C_ch_1=None
        self.mean_Photons_ch_1=None
        self.mean_Photons_err_ch_1=None
        self.mean_Molecules_ch_2=None
        self.std_Molecules_ch_2=None
        self.mean_Concentration_ch_2=None
        self.std_Concentration_ch_2=None
        self.std_err_Concentration_ch_2=None
        self.median_C_ch_2=None
        self.median_err_C_ch_2=None
        self.mean_Photons_ch_2=None
        self.mean_Photons_err_ch_2=None
        PTU_directory = self.setts['PTU_files_dir']
        
        if len(self.Channels) == 1:
        
            if '1' in self.Channels[0]:
                brightness_ch_1 = self.setts['Calib_data']['Ch_1_B']
                brightness_err_ch_1 = self.setts['Calib_data']['Ch_1_B_err']
                Veff_ch_1 = 1e-15*self.setts['Calib_data']['Ch_1_V0']
                Veff_err_ch_1 = 1e-15*self.setts['Calib_data']['Ch_1_V0_err']
                self.DF = self.Current_image_1[0]
                Photons_1 = pd.DataFrame(self.DF)
                n_pixels_1 =  Photons_1.stack().reset_index(drop=True).dropna().count()

                Molecules_ch_1 = self.calc_molecules(self.DF,
                                                self.PTU_Px_dwell,self.PTU_N_frames,
                                                brightness_ch_1,
                                                brightness_err_ch_1)[0]
                Molecules_err_ch_1 = self.calc_molecules(self.DF,
                                                    self.PTU_Px_dwell,
                                                    self.PTU_N_frames,
                                                    brightness_ch_1,
                                                    brightness_err_ch_1)[1]
                Concentration_ch_1 = 1e9*self.CONC(Molecules_ch_1,
                                                   Veff_ch_1,
                                                   Molecules_err_ch_1,
                                                   Veff_err_ch_1)[0]
                Concentration_err_ch_1 = 1e9*self.CONC(Molecules_ch_1,
                                                       Veff_ch_1,
                                                       Molecules_err_ch_1,
                                                       Veff_err_ch_1)[1]
                self.mean_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().mean()
            
                self.mean_Photons_err_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
                self.mean_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().mean()
                self.mean_Concentration_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().mean()

                if not self.setts['Error_notation']:
                    self.mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1).stack().reset_index(drop=True).dropna().mean()
                    self.mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1).stack().reset_index(drop=True).dropna().mean()
                else:
                    self.mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
                    self.mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)


                self.median_C_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().median()
                self.median_err_C_ch_1 = median_abs_deviation(pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna())

                Molecules_ch_1 = pd.DataFrame(Molecules_ch_1)
                Concentration_ch_1 = pd.DataFrame(Concentration_ch_1)
                
                Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1)
                Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1)

                
                if self.setts['Export_opts']['Photons to array']:
                    phot_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Phot_ch_1.csv')
                    
                    Photons_1.to_csv(phot_array_path_ch_1,index=False,sep=',', header=None)
                else:
                    pass
                
                if self.setts['Export_opts']['N_p to array']:
                    Np_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_ch_1.csv')
                    
                    
                    Molecules_ch_1.to_csv(Np_array_path_ch_1,index=False,sep=',', header=None)
                    
                    Np_err_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_err_ch_1.csv')
                    Molecules_err_ch_1.to_csv(Np_err_array_path_ch_1,index=False,sep=',', header=None)
                    
                else:
                    pass
                if self.setts['Export_opts']['Conc. to array']:
                    Conc_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_ch_1.csv')
                    
                    Concentration_ch_1.to_csv(Conc_array_path_ch_1,index=False,sep=',', header=None)
                    
                    Conc_err_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_err_ch_1.csv')
                    Concentration_err_ch_1.to_csv(Conc_err_array_path_ch_1,index=False,sep=',', header=None)
                    
                else:
                    pass
                
                if self.setts['Export_opts']['Photons to heatmap']:
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
                
                if self.setts['Export_opts']['N_p to heatmap']:
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
    
                if self.setts['Export_opts']['Conc. to heatmap']:
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

                Sing_Results_DF_tmp = pd.DataFrame([[anal_file,
                                                     1,
                                                     self.mean_Photons_ch_1,
                                                     self.mean_Photons_err_ch_1,
                                                     self.mean_Molecules_ch_1,
                                                     self.mean_Molecules_err_ch_1,
                                                     self.mean_Concentration_ch_1,
                                                     self.mean_Concentration_err_ch_1,
                                                     
                                                     self.median_C_ch_1,
                                                     self.median_err_C_ch_1]],columns=self.Sing_Results_DF.columns)
                
        
            elif '2' in self.Channels[0]:  
                brightness_ch_2 = self.setts['Calib_data']['Ch_2_B']
                brightness_err_ch_2 = self.setts['Calib_data']['Ch_2_B_err']
                Veff_ch_2 = 1e-15*self.setts['Calib_data']['Ch_2_V0']
                Veff_err_ch_2 = 1e-15*self.setts['Calib_data']['Ch_2_V0_err']
                self.DF2 = self.Current_image_2[0]
                Photons_2 = pd.DataFrame(self.DF2)
                n_pixels_2 =  Photons_2.stack().reset_index(drop=True).dropna().count()
                # print(self.DF2)
                Molecules_ch_2 = self.calc_molecules(self.DF2,
                                                self.PTU_Px_dwell,self.PTU_N_frames,
                                                brightness_ch_2,
                                                brightness_err_ch_2)[0]
                Molecules_err_ch_2 = self.calc_molecules(self.DF2,
                                                    self.PTU_Px_dwell,
                                                    self.PTU_N_frames,
                                                    brightness_ch_2,
                                                    brightness_err_ch_2)[1]
                Concentration_ch_2 = 1e9*self.CONC(Molecules_ch_2,
                                                   Veff_ch_2,
                                                   Molecules_err_ch_2,
                                                   Veff_err_ch_2)[0]
                Concentration_err_ch_2 = 1e9*self.CONC(Molecules_ch_2,
                                                       Veff_ch_2,
                                                       Molecules_err_ch_2,
                                                       Veff_err_ch_2)[1]
                self.mean_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().mean()
            
                self.mean_Photons_err_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
                self.mean_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().mean()
                self.mean_Concentration_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().mean()

                if not self.setts['Error_notation']:
                    self.mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2).stack().reset_index(drop=True).dropna().mean()
                    self.mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2).stack().reset_index(drop=True).dropna().mean()
                else:
                    self.mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
                    self.mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)


                self.median_C_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().median()
                self.median_err_C_ch_2 = median_abs_deviation(pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna())

                Molecules_ch_2 = pd.DataFrame(Molecules_ch_2)
                Concentration_ch_2 = pd.DataFrame(Concentration_ch_2)
                
                Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2)
                Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2)

                
                if self.setts['Export_opts']['Photons to array']:
                    phot_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Phot_ch_2.csv')
                    
                    Photons_2.to_csv(phot_array_path_ch_2,index=False,sep=',', header=None)
                else:
                    pass
                
                if self.setts['Export_opts']['N_p to array']:
                    Np_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_ch_2.csv')
                    
                    
                    Molecules_ch_2.to_csv(Np_array_path_ch_2,index=False,sep=',', header=None)
                    
                    Np_err_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_err_ch_2.csv')
                    Molecules_err_ch_2.to_csv(Np_err_array_path_ch_2,index=False,sep=',', header=None)
                    
                else:
                    pass
                if self.setts['Export_opts']['Conc. to array']:
                    Conc_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_ch_2.csv')
                    
                    Concentration_ch_2.to_csv(Conc_array_path_ch_2,index=False,sep=',', header=None)
                    
                    Conc_err_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_err_ch_2.csv')
                    Concentration_err_ch_2.to_csv(Conc_err_array_path_ch_2,index=False,sep=',', header=None)
                    
                else:
                    pass
                
                if self.setts['Export_opts']['Photons to heatmap']:
                    phot_hmap_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Phot_HM_ch_2.png')
    
                    fig = Figure(facecolor='white')
    
                    ax = fig.add_axes(rect)
                    norm = mpl.colors.Normalize(vmin=Photons_1.min().min(), vmax=Photons_2.max().max())
                    ax.imshow(Photons_2,cmap =cmap)
    
                    ax.axis('off')
                    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
                    FigureCanvas(fig).print_png(phot_hmap_path_ch_2)
                    
                else:
                    pass
                
                if self.setts['Export_opts']['N_p to heatmap']:
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
    
                if self.setts['Export_opts']['Conc. to heatmap']:
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
                Sing_Results_DF_tmp = pd.DataFrame([
                                                   [anal_file,
                                                 2,
                                                 self.mean_Photons_ch_2,
                                                 self.mean_Photons_err_ch_2,
                                                 self.mean_Molecules_ch_2,
                                                 self.mean_Molecules_err_ch_2,
                                                 self.mean_Concentration_ch_2,
                                                 self.mean_Concentration_err_ch_2,
                                                 
                                                 self.median_C_ch_2,
                                                 self.median_err_C_ch_2]],columns=self.Sing_Results_DF.columns)
        if len(self.Channels) == 2:        
            
            brightness_ch_1 = self.setts['Calib_data']['Ch_1_B']
            brightness_err_ch_1 = self.setts['Calib_data']['Ch_1_B_err']
            Veff_ch_1 = 1e-15*self.setts['Calib_data']['Ch_1_V0']
            Veff_err_ch_1 = 1e-15*self.setts['Calib_data']['Ch_1_V0_err']
            self.DF = self.Current_image_1[0]
            Photons_1 = pd.DataFrame(self.DF)
            n_pixels_1 =  Photons_1.stack().reset_index(drop=True).dropna().count()

            Molecules_ch_1 = self.calc_molecules(self.DF,
                                            self.PTU_Px_dwell,self.PTU_N_frames,
                                            brightness_ch_1,
                                            brightness_err_ch_1)[0]
            Molecules_err_ch_1 = self.calc_molecules(self.DF,
                                                self.PTU_Px_dwell,
                                                self.PTU_N_frames,
                                                brightness_ch_1,
                                                brightness_err_ch_1)[1]
            Concentration_ch_1 = 1e9*self.CONC(Molecules_ch_1,
                                               Veff_ch_1,
                                               Molecules_err_ch_1,
                                               Veff_err_ch_1)[0]
            Concentration_err_ch_1 = 1e9*self.CONC(Molecules_ch_1,
                                                   Veff_ch_1,
                                                   Molecules_err_ch_1,
                                                   Veff_err_ch_1)[1]
            self.mean_Photons_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().mean()
        
            self.mean_Photons_err_ch_1 = pd.DataFrame(Photons_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
            self.mean_Molecules_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().mean()
            self.mean_Concentration_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().mean()

            if not self.setts['Error_notation']:
                self.mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1).stack().reset_index(drop=True).dropna().mean()
                self.mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1).stack().reset_index(drop=True).dropna().mean()
            else:
                self.mean_Molecules_err_ch_1 = pd.DataFrame(Molecules_ch_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)
                self.mean_Concentration_err_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_1)


            self.median_C_ch_1 = pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna().median()
            self.median_err_C_ch_1 = median_abs_deviation(pd.DataFrame(Concentration_ch_1).stack().reset_index(drop=True).dropna())

            Molecules_ch_1 = pd.DataFrame(Molecules_ch_1)
            Concentration_ch_1 = pd.DataFrame(Concentration_ch_1)
            
            Molecules_err_ch_1 = pd.DataFrame(Molecules_err_ch_1)
            Concentration_err_ch_1 = pd.DataFrame(Concentration_err_ch_1)

            
            if self.setts['Export_opts']['Photons to array']:
                phot_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Phot_ch_1.csv')
                
                Photons_1.to_csv(phot_array_path_ch_1,index=False,sep=',', header=None)
            else:
                pass
            
            if self.setts['Export_opts']['N_p to array']:
                Np_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_ch_1.csv')
                
                
                Molecules_ch_1.to_csv(Np_array_path_ch_1,index=False,sep=',', header=None)
                
                Np_err_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_Np_err_ch_1.csv')
                Molecules_err_ch_1.to_csv(Np_err_array_path_ch_1,index=False,sep=',', header=None)
                
            else:
                pass
            if self.setts['Export_opts']['Conc. to array']:
                Conc_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_ch_1.csv')
                
                Concentration_ch_1.to_csv(Conc_array_path_ch_1,index=False,sep=',', header=None)
                
                Conc_err_array_path_ch_1 = os.path.join(PTU_directory,anal_file+'_conc_err_ch_1.csv')
                Concentration_err_ch_1.to_csv(Conc_err_array_path_ch_1,index=False,sep=',', header=None)
                
            else:
                pass
            
            if self.setts['Export_opts']['Photons to heatmap']:
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
            
            if self.setts['Export_opts']['N_p to heatmap']:
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

            if self.setts['Export_opts']['Conc. to heatmap']:
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
    
        
            brightness_ch_2 = self.setts['Calib_data']['Ch_2_B']
            brightness_err_ch_2 = self.setts['Calib_data']['Ch_2_B_err']
            Veff_ch_2 = 1e-15*self.setts['Calib_data']['Ch_2_V0']
            Veff_err_ch_2 = 1e-15*self.setts['Calib_data']['Ch_2_V0_err']
            self.DF = self.Current_image_2[0]
            Photons_2 = pd.DataFrame(self.DF2)
            n_pixels_2 =  Photons_2.stack().reset_index(drop=True).dropna().count()

            Molecules_ch_2 = self.calc_molecules(self.DF2,
                                            self.PTU_Px_dwell,self.PTU_N_frames,
                                            brightness_ch_2,
                                            brightness_err_ch_2)[0]
            Molecules_err_ch_2 = self.calc_molecules(self.DF2,
                                                self.PTU_Px_dwell,
                                                self.PTU_N_frames,
                                                brightness_ch_2,
                                                brightness_err_ch_2)[1]
            Concentration_ch_2 = 1e9*self.CONC(Molecules_ch_2,
                                               Veff_ch_2,
                                               Molecules_err_ch_2,
                                               Veff_err_ch_2)[0]
            Concentration_err_ch_2 = 1e9*self.CONC(Molecules_ch_2,
                                                   Veff_ch_2,
                                                   Molecules_err_ch_2,
                                                   Veff_err_ch_2)[1]
            self.mean_Photons_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().mean()
        
            self.mean_Photons_err_ch_2 = pd.DataFrame(Photons_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
            self.mean_Molecules_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().mean()
            self.mean_Concentration_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().mean()

            if not self.setts['Error_notation']:
                self.mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2).stack().reset_index(drop=True).dropna().mean()
                self.mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2).stack().reset_index(drop=True).dropna().mean()
            else:
                self.mean_Molecules_err_ch_2 = pd.DataFrame(Molecules_ch_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)
                self.mean_Concentration_err_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().std()/sqrt(n_pixels_2)


            self.median_C_ch_2 = pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna().median()
            self.median_err_C_ch_2 = median_abs_deviation(pd.DataFrame(Concentration_ch_2).stack().reset_index(drop=True).dropna())

            Molecules_ch_2 = pd.DataFrame(Molecules_ch_2)
            Concentration_ch_2 = pd.DataFrame(Concentration_ch_2)
            
            Molecules_err_ch_2 = pd.DataFrame(Molecules_err_ch_2)
            Concentration_err_ch_2 = pd.DataFrame(Concentration_err_ch_2)

            
            if self.setts['Export_opts']['Photons to array']:
                phot_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Phot_ch_2.csv')
                
                Photons_2.to_csv(phot_array_path_ch_2,index=False,sep=',', header=None)
            else:
                pass
            
            if self.setts['Export_opts']['N_p to array']:
                Np_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_ch_2.csv')
                
                
                Molecules_ch_2.to_csv(Np_array_path_ch_2,index=False,sep=',', header=None)
                
                Np_err_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Np_err_ch_2.csv')
                Molecules_err_ch_2.to_csv(Np_err_array_path_ch_2,index=False,sep=',', header=None)
                
            else:
                pass
            if self.setts['Export_opts']['Conc. to array']:
                Conc_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_ch_2.csv')
                
                Concentration_ch_2.to_csv(Conc_array_path_ch_2,index=False,sep=',', header=None)
                
                Conc_err_array_path_ch_2 = os.path.join(PTU_directory,anal_file+'_conc_err_ch_2.csv')
                Concentration_err_ch_2.to_csv(Conc_err_array_path_ch_2,index=False,sep=',', header=None)
                
            else:
                pass
            
            if self.setts['Export_opts']['Photons to heatmap']:
                phot_hmap_path_ch_2 = os.path.join(PTU_directory,anal_file+'_Phot_HM_ch_2.png')

                fig = Figure(facecolor='white')

                ax = fig.add_axes(rect)
                norm = mpl.colors.Normalize(vmin=Photons_1.min().min(), vmax=Photons_2.max().max())
                ax.imshow(Photons_2,cmap =cmap)

                ax.axis('off')
                fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
                FigureCanvas(fig).print_png(phot_hmap_path_ch_2)
                
            else:
                pass
            
            if self.setts['Export_opts']['N_p to heatmap']:
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

            if self.setts['Export_opts']['Conc. to heatmap']:
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

            Sing_Results_DF_tmp = pd.DataFrame([[anal_file,
                                                 1,
                                                 self.mean_Photons_ch_1,
                                                 self.mean_Photons_err_ch_1,
                                                 self.mean_Molecules_ch_1,
                                                 self.mean_Molecules_err_ch_1,
                                                 self.mean_Concentration_ch_1,
                                                 self.mean_Concentration_err_ch_1,
                                                 
                                                 self.median_C_ch_1,
                                                 self.median_err_C_ch_1],
                                                   [anal_file,
                                                 2,
                                                 self.mean_Photons_ch_2,
                                                 self.mean_Photons_err_ch_2,
                                                 self.mean_Molecules_ch_2,
                                                 self.mean_Molecules_err_ch_2,
                                                 self.mean_Concentration_ch_2,
                                                 self.mean_Concentration_err_ch_2,
                                                 
                                                 self.median_C_ch_2,
                                                 self.median_err_C_ch_2]],columns=self.Sing_Results_DF.columns)
        
        self.Sing_Results_DF=pd.concat([self.Sing_Results_DF,Sing_Results_DF_tmp]).reset_index(drop=True)
        
    def export_results(self):
        if self.output_format == 'excel' :
            self.Sing_Results_DF.to_excel(self.output_results_path,index=False)
    
        elif self.output_format == 'dat' :
            
            self.Sing_Results_DF.to_csv(self.output_results_path,sep='\t',index=False)
        elif self.output_format == 'csv' :
            
            self.Sing_Results_DF.to_csv(self.output_results_path,index=False)
        elif self.output_format == 'pickle' :
            
            self.Sing_Results_DF.to_pickle(self.output_results_path)
        else:
            pass