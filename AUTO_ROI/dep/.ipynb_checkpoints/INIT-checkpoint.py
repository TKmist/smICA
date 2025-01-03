import inspect
import dearpygui.dearpygui as dpg
import numpy as np
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
import pickle
from PIL import Image
from io import BytesIO
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import time
import cv2
from matplotlib.transforms import Bbox
from dep.automated_roi_TK import ImageROIProcessor



class _init_varaibles:
    def __init__(self):
        
        self.init_size_ratio = {'width':1,
                          'height':1}
        self.init_top_indent = 24+11
        self.init_bottom_indent = 11
        self.init_left_indent = 11
        self.init_right_indent = 11
        self.init_internal_indent = 11
        self.init_group_spacer = 2
        self.init_font_size  = 20
        self.VIEWPORT_prop = {'width':1523,
                              'height':940+2*11,
                              'pos':(0,0)
                                }
        self.last_directory = 'samples'
        self.tex_1_name = 'texture_tag_chan_1'
        self.tex_2_name = 'texture_tag_chan_2'
        self.loadmode = None
        
    
class inits:
    def __init__(self,
                 size_ratio,
                 left_indent,
                 internal_indent,
                 right_indent,
                 bottom_indent,
                 top_indent,
                 group_spacer,
                 font_size,
                 callbacks,
                 tex_1_name,
                 tex_2_name
                 
                ):
        self.size_ratio=size_ratio
        self.top_indent = int(top_indent*self.size_ratio['width'])
        self.bottom_indent  = int(bottom_indent*self.size_ratio['width'])
        self.left_indent  = int(left_indent*self.size_ratio['width'])
        self.right_indent  = int(right_indent*self.size_ratio['width'])
        self.internal_indent  = int(internal_indent*self.size_ratio['width'])
        self.fnt_ratio = (self.size_ratio['width']+self.size_ratio['height'])/2
        self.font_size  = int(np.round(font_size*self.fnt_ratio,0))
        self.group_spacer  = int(group_spacer*self.size_ratio['width'])

        self.callback=callbacks
        self.tex_1_name = tex_1_name
        self.tex_2_name = tex_2_name


        
        


        self.file_window = {'name':'file_window',
                            'width':int(340*self.size_ratio['width']),
                            'height':dpg.get_viewport_height()-4*self.bottom_indent,
                            'pos':(self.left_indent,self.top_indent)
                            }

        self.file_window = {'name':'file_window',
                            'width':int(340*self.size_ratio['width']),
                            'height':dpg.get_viewport_height()-4*self.bottom_indent,
                            'pos':(self.left_indent,self.top_indent)
                            }
        self.file_dialog_id = {'name':'file_dialog_id',
                               'width':int(dpg.get_viewport_width())-11*self.left_indent,
                               'height':int(dpg.get_viewport_height()*3/4)
                              }
        
        
        self.image_window_1 = {'name':'image_window_1',
                            'width':int(np.round((dpg.get_viewport_width()-self.file_window['width']-self.file_window['pos'][0]-2*self.internal_indent-self.right_indent)/2,0)),
                            'height':int(np.round((dpg.get_viewport_width()-self.file_window['width']-self.file_window['pos'][0]-2*self.internal_indent-self.right_indent)/2,0))+75,
                            'pos':(self.left_indent+self.file_window['width']+self.internal_indent,
                                   self.top_indent)
                            }

        self.image_window_2 = {'name':'image_window_2',
                            'width':self.image_window_1['width'],
                            'height':self.image_window_1['height'],
                            'pos':(self.image_window_1['pos'][0]+self.image_window_1['width']+self.internal_indent,
                                   self.top_indent)
                            }

        self.file_box = {'name':'file_box',
                         'width':-1,
                         'num_items':30
                        }
        
class _basicF:      
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


    def plot_IMAGE(self,img,width,height):
        width = int(width)
        height = int(height)
        if img.shape != (height, width):  # Resize if necessary
            resized_img = cv2.resize(img, (width, height))  # Resize to (width, height)
        else:
            resized_img = img

        # Check if grayscale (2D) or already RGB (3D)
        if len(resized_img.shape) == 2:  # Grayscale image (H, W)
            rgb_img = np.stack([resized_img] * 3, axis=2)  # Convert (H, W) to (H, W, 3)
        else:
            rgb_img = resized_img  # Already RGB (H, W, 3)
        
        # Ensure pixel values are in range [0, 255]
        if rgb_img.max() <= 1.0:  # If the image is in range [0, 1]
            rgb_img = (rgb_img * 255).astype(np.uint8)  # Convert to [0, 255]
        else:
            rgb_img = rgb_img.astype(np.uint8)  # Ensure dtype is uint8

        return rgb_img
        # fg_color = 'white'
        # px = 1/plt.rcParams['figure.dpi']
        # # print(width,height)
        
        
        # fig,ax = plt.subplots(figsize=((width*px),(height*px)),facecolor='black')
        
        
        # fig.subplots_adjust(top=0.9, bottom=0.1, right=1, left=0, hspace=0, wspace=0)
        # ax.margins(0, 0,)
        # ax.axis('off')

        # pa = ax.imshow(img,cmap='gray')
        
        # plt.axis('tight')
        # b =BytesIO()
        # FigureCanvas(fig).print_png(b)
        # plt.close(fig)
        # b.seek(0)
        # image=Image.open(b)
        # return image
        
    def create_textures(self,curr_img_1,curr_img_2,w,h):
        image_1=self.plot_IMAGE(curr_img_1,w,h)
        image_2=self.plot_IMAGE(curr_img_2,w,h)
        # dpg_image_1 = []
        # for i in range(0, image_1._size[1]):
        #     for j in range(0, image_1._size[0]):
        #         pixel = image_1.getpixel((j, i))
                
        #         dpg_image_1.append(pixel[0]/255)
        #         dpg_image_1.append(pixel[1]/255)
        #         dpg_image_1.append(pixel[2]/255)
        #         dpg_image_1.append(255/255)
                
        # dpg_image_2 = []
        # for i in range(0, image_2._size[1]):
        #     for j in range(0, image_2._size[0]):
        #         pixel = image_2.getpixel((j, i))
                
        #         dpg_image_2.append(pixel[0]/255)
        #         dpg_image_2.append(pixel[1]/255)
        #         dpg_image_2.append(pixel[2]/255)
        #         dpg_image_2.append(255/255)
        dpg_image_1 = self.convert_to_texture(image_1)
        dpg_image_2 = self.convert_to_texture(image_2)
        
        return dpg_image_1, dpg_image_2
        # return dpg_image_1,dpg_image_2



    def convert_to_texture(self, img):
        height, width, channels = img.shape
        
        # Ensure the image is in range [0, 255]
        if img.max() <= 1.0:  # If the image is in range [0, 1]
            img = (img * 255).astype(np.uint8)
        
        # Add alpha channel (255) to every pixel
        alpha_channel = np.full((height, width, 1), 255, dtype=np.uint8)  # Full opacity
        img_rgba = np.concatenate((img, alpha_channel), axis=2)  # (H, W, 4)
        
        # Normalize pixel values from [0, 255] to [0, 1] (convert to float32)
        img_rgba_normalized = img_rgba.astype(np.float32) / 255.0
        
        # Flatten the array into a 1D list for DearPyGui
        return img_rgba_normalized.flatten().tolist()
    
    


class _init_Menu:
    
    
    def __init__(self,VERSION,inV):
        self.VERSION = VERSION
        self.inV=inV
        
        
    
    
    def callback_open_ptu_diaolog(self,sender,app_data):
        # print(self.inV.loadmode)
        dpg.show_item('file_dialog_id')
        self.inV.loadmode = 'PTU' 
        # print(self.inV.loadmode)



    def callback_open_npy_diaolog(self,sender,app_data):
        # print(self.inV.loadmode)
        dpg.show_item('file_dialog_id')
        self.inV.loadmode = 'NPY' 
        # print(self.inV.loadmode)

    def callback_open_png_diaolog(self,sender,app_data):
        # print(self.inV.loadmode)
        dpg.show_item('file_dialog_id')
        self.inV.loadmode = 'PNG' 
        # print(self.inV.loadmode)

    
    def mount_main_Menu_bar(self):
    
        with dpg.viewport_menu_bar(tag="vieport's_menubar"):
            with dpg.menu(label="Menu",tag='menu_file_dropout'):
                dpg.add_menu_item(label="Open PTU folder",callback=self.callback_open_ptu_diaolog ,tag='menu_item_open_ptu')
                dpg.add_menu_item(label="Open npy folder",callback=self.callback_open_npy_diaolog,tag='menu_item_open_npy')
                dpg.add_menu_item(label="Open png folder",callback=self.callback_open_png_diaolog,tag='menu_item_open_png')
                dpg.add_separator(tag ='menu_sep_left_1',parent = 'menu_file_dropout',
                  before = 'menu_item_open_output_folder',)
                dpg.add_menu_item(label="Open OUTPUT folder",callback=None,tag='menu_item_open_output_folder')
                dpg.add_separator(tag ='menu_sep_left_2',parent = 'menu_file_dropout',
                  before = 'menu_item_exit',)
                
                dpg.add_menu_item(label="Exit",callback=lambda: dpg.stop_dearpygui(),tag='menu_item_exit')

class oth:
    def __init__(self,basf,inV):
        self.basf = basf
        self.inV=inV

    def update_texture(self,np_imgage_input):
    # global ratio_w,dif_vp0_width
        ratio = {'width': np.round(dpg.get_viewport_width()/self.inV.VIEWPORT_prop['width'],4),
             'height': np.round(dpg.get_viewport_height()/self.inV.VIEWPORT_prop['height'],4)} 
        ratio_w = ratio['width']
        width = np_imgage_input.shape[0]
        height = np_imgage_input.shape[1]
        
        w = int(np.round(dpg.get_item_width('image_window_1')))-int(np.round(15*ratio_w))
        h = w
        t0 = time.time()
        image=self.basf.plot_IMAGE(np_imgage_input,w,h)
        t1 = time.time()

        dpg_image = self.basf.convert_to_texture(image)
        # image_array = np.array(image, dtype=np.float32) / 255
        # t2 = time.time()
        
    
    
        # dpg_image = image_array[:, :, [0, 1, 2, 3]].reshape(-1).tolist()
        # t3 = time.time()
        # print(t1-t0,t2-t1,t3-t2)
        return dpg_image

    

class callbacks:
    def __init__(self,last_directory,basf,inV):
        self.items=[]
        self.last_directory = last_directory
        self.directory = ''
        self.files = ()
        self.anal_file = ''
        self.basf=basf
        self.inV=inV
        self.npy_channels = []
        self.png_channels = []
        
    

    
        
    
    def callback_listbox(self,sender,app_data):
        self.anal_file = app_data
        file = os.path.join(self.last_directory,self.anal_file)
        

        if self.inV.loadmode == 'PTU':
            self.load_PTU_images(file)
        elif self.inV.loadmode == 'NPY':
            self.npy_channels = self.filenames_dict[self.anal_file]
            channels = self.npy_channels
            self.load_NPY_images(file,channels)
        elif self.inV.loadmode == 'PNG':
            self.npy_channels = self.filenames_dict[self.anal_file]
            channels = self.npy_channels
            self.load_PNG_images(file,channels)
        
    

    def display_images(self,channel):
        ot = oth(self.basf,self.inV)
                  
        if channel == 1:
            dpg_image_1 = ot.update_texture(self.Current_image_1)
            # print('ch1')   
            dpg.set_value(self.inV.tex_1_name, dpg_image_1)
        elif channel == 2:
            dpg_image_2 = ot.update_texture(self.Current_image_2)
            # print('ch2')
            print(self.inV.tex_2_name)
            dpg.set_value(self.inV.tex_2_name, dpg_image_2)
        elif channel =='both':

            # print(np.max(self.Current_image_1))
            dpg_image_1 = ot.update_texture(self.Current_image_1)
            # print(np.max(self.Current_image_2))
            dpg_image_2 = ot.update_texture(self.Current_image_2)
            # print('ch12')   
            dpg.set_value(self.inV.tex_1_name, dpg_image_1)
            dpg.set_value(self.inV.tex_2_name, dpg_image_2)
            

    def callback_empty(self,sender,app_data):
        '''Empty function. Do nothing.'''
        pass

    def update_dialogs_default_directory(self,last_directory):
    # print(last_directory)
        pass
        # dpg.configure_item('TT_file_dialog_id_ch_2',default_path=last_directory)
        # dpg.configure_item('TT_file_dialog_id_ch_1',default_path=last_directory)
        
        # dpg.configure_item('ROI_folder_dialog_id',default_path=last_directory)
        # dpg.configure_item('file_dialog_id',default_path=last_directory)
        # dpg.configure_item('PTU_file_dialog_id',default_path=last_directory)
        # dpg.configure_item('Select_ROI_dialog',default_path=last_directory)
        # dpg.configure_item('file_dialog_export',default_path=last_directory)
        # dpg.configure_item('Calib_file_dialog_id',default_path=last_directory)

    def update_flist(self,fs):
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
    
    def callback_directory_select(self,sender,app_data):
        print('clab',self.inV.loadmode)
        self.directory = app_data['file_path_name']
        # new_directory=directory
        
        self.PTU_directory = self.directory
        self.last_directory=self.directory
        self.update_dialogs_default_directory(self.last_directory)

        if self.inV.loadmode == 'PTU':
        
            self.files = tuple(np.sort([f for f in os.listdir(self.PTU_directory) if f.endswith('.ptu')]))
            self.pck_files = list(np.sort([f for f in os.listdir(self.PTU_directory) if f.endswith('.pkl')]))
    
            filenames = [f.replace('.ptu','') for f in self.files]
    
            if len(self.pck_files)!=0:
                self.update_flist(filenames)
        
        
                self.anal_file=filenames[0]
                dpg.configure_item('file_box', default_value=self.anal_file)
    
                self.load_PTU_images(self.anal_file)
                print(self.anal_file)
        elif self.inV.loadmode == 'NPY':
        
            self.files = tuple(np.sort([f for f in os.listdir(self.PTU_directory) if f.endswith('.npy')]))
            # self.pck_files = list(np.sort([f for f in os.listdir(self.PTU_directory) if f.endswith('.pkl')]))
    
            filenames = [f.replace('.npy','') for f in self.files]

            self.filenames_dict = {}

            for name in filenames:
                base_name, channel_part = name.split('_ch_')
                channel = channel_part.split('.')[0]  # Extract the channel number
                if base_name not in self.filenames_dict:
                    self.filenames_dict[base_name] = []
                self.filenames_dict[base_name].append(channel)
            
            
            for base_name in self.filenames_dict:
                self.filenames_dict[base_name].sort()
            print(self.filenames_dict)
            if self.filenames_dict.keys()!=0:
                self.update_flist(list(self.filenames_dict.keys()))
        
        
                self.anal_file=list(self.filenames_dict.keys())[0]
                self.npy_channels=self.filenames_dict[self.anal_file]

                print(self.anal_file)
                print(self.npy_channels)
                self.load_NPY_images(self.anal_file,self.npy_channels)
        elif self.inV.loadmode == 'PNG':
            self.files = tuple(np.sort([f for f in os.listdir(self.PTU_directory) if f.endswith('.png')]))
            # self.pck_files = list(np.sort([f for f in os.listdir(self.PTU_directory) if f.endswith('.pkl')]))
    
            filenames = [f.replace('.png','') for f in self.files]
            self.filenames_dict = {}

            for name in filenames:
                base_name, channel_part = name.split('_ch_')
                channel = channel_part.split('.')[0]  # Extract the channel number
                if base_name not in self.filenames_dict:
                    self.filenames_dict[base_name] = []
                self.filenames_dict[base_name].append(channel)
            
            
            for base_name in self.filenames_dict:
                self.filenames_dict[base_name].sort()
            print(self.filenames_dict)
            if self.filenames_dict.keys()!=0:
                self.update_flist(list(self.filenames_dict.keys()))
        
        
                self.anal_file=list(self.filenames_dict.keys())[0]
                self.npy_channels=self.filenames_dict[self.anal_file]

                print(self.anal_file)
                print(self.npy_channels)
                self.load_PNG_images(self.anal_file,self.npy_channels)
            # dpg.configure_item('file_box', default_value=self.anal_file)
    
                
                
        
            
    
            # filenames_dict = {}

            # for name in filenames_dict.keys():
            #     base_name, channel_part = name.split('_ch_')
            #     channel = channel_part.split('.')[0]  # Extract the channel number
            #     if base_name not in filenames_dict:
            #         filenames_dict[base_name] = []
            #     filenames_dict[base_name].append(channel)
            
            
            # for base_name in filenames_dict:
            #     filenames_dict[base_name].sort()
            
            # if filenames!=0:
            #     self.update_flist(filenames)
        
        
            #     self.anal_file=filenames[0]
            #     dpg.configure_item('file_box', default_value=self.anal_file)
    
                
            #     self.load_PNG_images(filenames_dict[self.anal_file],channels)
    def load_NPY_images(self,an_file,Channels):
        print(an_file,Channels)
        
        if len(Channels)==1:
            if '1' in Channels[0]:
                npy_file = os.path.join(self.PTU_directory,an_file+'_ch_'+Channels[0]+'.npy')
                Intensity_1 = np.load(npy_file)
                self.processor_1 = ImageROIProcessor(npy_file, npy_file, False)
                self.processor_1.image=Intensity_1
                channel = 'both'
                self.Current_image_1 = Intensity_1/np.max(Intensity_1)
                self.Current_image_2 = self.NO_IMAGE_TEXTURE
                self.display_images(channel)
                self._update_textures_roi('cell_tresh_ratio_1', 1.0)
            elif '2' in Channels[0]:
                npy_file = os.path.join(self.PTU_directory,an_file+'_ch_'+Channels[0]+'.npy')
                Intensity_2 = np.load(npy_file)
                self.processor_2 = ImageROIProcessor(npy_file, npy_file, False)
                self.processor_2.image=Intensity_2
                channel = 'both'
                self.Current_image_1 = self.NO_IMAGE_TEXTURE
                self.Current_image_2 = Intensity_2/np.max(Intensity_2)
                self.display_images(channel)
                self._update_textures_roi('cell_tresh_ratio_2', 1.0)
        elif len(Channels)==2:
            npy_file_1 = os.path.join(self.PTU_directory,an_file+'_ch_1.npy')
            npy_file_2 = os.path.join(self.PTU_directory,an_file+'_ch_2.npy')
            
            Intensity_1 = np.load(npy_file_1)
            Intensity_2 = np.load(npy_file_2)
            self.processor_1 = ImageROIProcessor(npy_file_1, npy_file_1, False)
            self.processor_1.image=Intensity_1
            self.processor_2 = ImageROIProcessor(npy_file_2, npy_file_2, False)
            self.processor_2.image=Intensity_2
            channel = 'both'

            self.Current_image_1 = Intensity_1/np.max(Intensity_1)
            self.Current_image_2 = Intensity_2/np.max(Intensity_2)
            self.display_images(channel)
            self._update_textures_roi('cell_tresh_ratio_1', 1.0)
            self._update_textures_roi('cell_tresh_ratio_2', 1.0)
        

    def load_PNG_images(self,an_file,Channels):
        if len(Channels)==1:
            if '1' in Channels[0]:
                pass
                png_file = os.path.join(self.PTU_directory,an_file+'_ch_'+Channels[0]+'.png')
                
                Intensity_1 = cv2.imread(png_file,cv2.IMREAD_GRAYSCALE)
                self.processor_1 = ImageROIProcessor(png_file, png_file, False)
                self.processor_1.image=Intensity_1
                channel = 'both'
                self.Current_image_1 = Intensity_1/np.max(Intensity_1)
                self.Current_image_2 = self.NO_IMAGE_TEXTURE
                self.display_images(channel)
                self._update_textures_roi('cell_tresh_ratio_1', 1.0)
            
            elif '2' in Channels[0]:
                pass
                png_file = os.path.join(self.PTU_directory,an_file+'_ch_'+Channels[0]+'.png')
                Intensity_2 = cv2.imread(png_file,cv2.IMREAD_GRAYSCALE)
                self.processor_2 = ImageROIProcessor(png_file, png_file, False)
                self.processor_2.image=Intensity_2
                channel = 'both'
                self.Current_image_1 = self.NO_IMAGE_TEXTURE
                self.Current_image_2 = Intensity_2/np.max(Intensity_2)
                self.display_images(channel)
                
                self._update_textures_roi('cell_tresh_ratio_2', 1.0)
        elif len(Channels)==2:
            # pass
            png_file_1 = os.path.join(self.PTU_directory,an_file+'_ch_1.png')
            png_file_2 = os.path.join(self.PTU_directory,an_file+'_ch_2.png')
            Intensity_1 = cv2.imread(png_file_1,cv2.IMREAD_GRAYSCALE)
            Intensity_2 = cv2.imread(png_file_2,cv2.IMREAD_GRAYSCALE)

            self.processor_1 = ImageROIProcessor(png_file_1, png_file_1, False)
            self.processor_1.image=Intensity_1
            self.processor_2 = ImageROIProcessor(png_file_2, png_file_2, False)
            self.processor_2.image=Intensity_2
            channel = 'both'

            self.Current_image_1 = Intensity_1/np.max(Intensity_1)
            self.Current_image_2 = Intensity_2/np.max(Intensity_2)
            self.display_images(channel)
            self._update_textures_roi('cell_tresh_ratio_1', 1.0)
            self._update_textures_roi('cell_tresh_ratio_2', 1.0)

    
    def load_PTU_images(self,an_file):
        pickle_file = os.path.join(self.PTU_directory,an_file+'.pkl')
        
        with open(pickle_file, 'rb') as pcklf:
            pkl = pickle.load(pcklf)

        Channels = list(pkl.keys())
        Channels = [f for f in Channels if f.startswith('export_df')]
        # print(Channels)
        Channels = [ch[-1] for ch in Channels]
        # print(Channels)
        if len(Channels)==1:
            if '1' in Channels[0]:
                Intensity_1 = pkl['intensity_1']
                self.processor_1 = ImageROIProcessor(pcklf, pcklf, False)
                self.processor_1.image=Intensity_1
                
                channel = 'both'
                self.Current_image_1 = Intensity_1/np.max(Intensity_1)

                
                self.Current_image_2 = self.NO_IMAGE_TEXTURE
                
                self.display_images(channel)
                self._update_textures_roi('cell_tresh_ratio_1', 1.0)
            elif '2' in Channels[0]:
                Intensity_2 = pkl['intensity_2']

                self.processor_2 = ImageROIProcessor(pcklf, pcklf, False)
                self.processor_2.image=Intensity_2
                
                channel = 'both'
                self.Current_image_1 = self.NO_IMAGE_TEXTURE
                self.Current_image_2 = Intensity_2/np.max(Intensity_2)
                self.display_images(channel)
                self._update_textures_roi('cell_tresh_ratio_2', 1.0)
        elif len(Channels)==2:
            Intensity_1 = pkl['intensity_1']
            Intensity_2 = pkl['intensity_2']
            self.processor_1 = ImageROIProcessor(pcklf, pcklf, False)
            self.processor_1.image=Intensity_1
            self.processor_2 = ImageROIProcessor(pcklf, pcklf, False)
            self.processor_2.image=Intensity_2
            
            channel = 'both'

            self.Current_image_1 = Intensity_1/np.max(Intensity_1)
            self.Current_image_2 = Intensity_2/np.max(Intensity_2)
            self.display_images(channel)
            self._update_textures_roi('cell_tresh_ratio_1', 1.0)
            self._update_textures_roi('cell_tresh_ratio_2', 1.0)
    
    
    
    # def cell_roi_detect(self,img):

    def create_rgba_texture(self,image_data):
        # Ensure the image data is 2D (grayscale)
        if image_data.ndim != 2:
            raise ValueError("Image data should be a 2D array.")
        
        # Convert to a 3D RGB array (3 channels)
        rgba_data = np.stack([image_data] * 3, axis=-1)  # Duplicate grayscale data for RGB channels
        rgba_data = np.concatenate([rgba_data, np.ones((image_data.shape[0], image_data.shape[1], 1), dtype=np.uint8) * 255], axis=-1)  # Add alpha channel (fully opaque)
        
        # Flatten the RGBA array into a 1D list for the dynamic texture
        return rgba_data.flatten().tolist()    
        
    def _update_textures_roi(self,sender, app_data):
        ratio = {'width': np.round(dpg.get_viewport_width()/self.inV.VIEWPORT_prop['width'],4),
             'height': np.round(dpg.get_viewport_height()/self.inV.VIEWPORT_prop['height'],4)} 
        ratio_w = ratio['width']
        
        
        w = int(np.round(dpg.get_item_width('image_window_1')))-int(np.round(15*ratio_w))
        h = w
        ovrl = 15
        
        
        # print(sender)
        if sender[-1]=='1':
            find_nucleus = dpg.get_value('nucleus_search_1')
            cell_rat = dpg.get_value('cell_tresh_ratio_1')
            nucl_rat = dpg.get_value('nucl_tresh_ratio_1')
            img = self.processor_1.image.astype(np.uint8)
            
            image_data =(img* (255 / img.max())).astype(np.uint8)
            cell_roi_image = self.processor_1.detect_cell_roi(img,cell_rat)
            if not find_nucleus:    
                full_mask = cell_roi_image
                # image_data =(img* (255 / img.max())).astype(np.uint8)
                # image_data = np.multiply(image_data, cell_roi_image)
            else:
                nucleus_roi = self.processor_1.detect_nucleus_roi(img, cell_roi_image, nucl_rat)
                full_mask = self.processor_1.make_full_roi(cell_roi_image, nucleus_roi)
                
                # image_data =(img* (255 / img.max())).astype(np.uint8)
                # nucleus_roi = self.processor_1.detect_nucleus_roi(img,cell_roi,nucl_rat)
                # full_mask = self.processor_1.make_full_roi(cell_roi,nucleus_roi)
                # image_data = np.multiply(image_data, full_mask)
            # image_data = cv2.resize(image_data, (w, h), interpolation=cv2.INTER_CUBIC)
            # new_texture_data = self.create_rgba_texture(image_data/255)
            rgba_image = np.zeros((img.shape[1], img.shape[0], 4), dtype=np.uint8)
            rgba_image[..., 0] = img  # Red channel
            rgba_image[..., 1] = img  # Green channel
            rgba_image[..., 2] = img  # Blue channel
            rgba_image[..., 3] = 255

            overlay_alpha = ovrl  # Transparency level (0-255, where 255 is fully opaque)
            rgba_image[full_mask > 0, 0] = 255  # Red channel set to max for mask
            rgba_image[full_mask > 0, 1] = img[full_mask > 0]  # Blend green
            rgba_image[full_mask > 0, 2] = img[full_mask > 0]  # Blend blue
            rgba_image[full_mask > 0, 3] = overlay_alpha

            rgba_image  =cv2.resize(rgba_image, (w, h), interpolation=cv2.INTER_CUBIC)
            rgba_image=rgba_image.astype(np.float32) /255
            
            new_texture_data = rgba_image.flatten().tolist()
            dpg.set_value(self.inV.tex_1_name, new_texture_data)
            
                
        elif sender[-1]=='2':
            find_nucleus = dpg.get_value('nucleus_search_2')
            cell_rat = dpg.get_value('cell_tresh_ratio_2')
            nucl_rat = dpg.get_value('nucl_tresh_ratio_2')
            img = self.processor_2.image.astype(np.uint8)
            print(type(img))
            cell_roi_image = self.processor_2.detect_cell_roi(img,cell_rat)
            if not find_nucleus:    
                full_mask = cell_roi_image
                # image_data =(img* (255 / img.max())).astype(np.uint8)
                # image_data = np.multiply(image_data, cell_roi_image)
            else:
                nucleus_roi = self.processor_2.detect_nucleus_roi(img, cell_roi_image, nucl_rat)
                full_mask = self.processor_2.make_full_roi(cell_roi_image, nucleus_roi)
                
                # image_data =(img* (255 / img.max())).astype(np.uint8)
                # nucleus_roi = self.processor_1.detect_nucleus_roi(img,cell_roi,nucl_rat)
                # full_mask = self.processor_1.make_full_roi(cell_roi,nucleus_roi)
                # image_data = np.multiply(image_data, full_mask)
            # image_data = cv2.resize(image_data, (w, h), interpolation=cv2.INTER_CUBIC)
            # new_texture_data = self.create_rgba_texture(image_data/255)
            rgba_image = np.zeros((img.shape[1], img.shape[0], 4), dtype=np.uint8)
            rgba_image[..., 0] = img  # Red channel
            rgba_image[..., 1] = img  # Green channel
            rgba_image[..., 2] = img  # Blue channel
            rgba_image[..., 3] = 255

            overlay_alpha = ovrl  # Transparency level (0-255, where 255 is fully opaque)
            rgba_image[full_mask > 0, 0] = 255  # Red channel set to max for mask
            rgba_image[full_mask > 0, 1] = img[full_mask > 0]  # Blend green
            rgba_image[full_mask > 0, 2] = img[full_mask > 0]  # Blend blue
            rgba_image[full_mask > 0, 3] = overlay_alpha

            rgba_image  =cv2.resize(rgba_image, (w, h), interpolation=cv2.INTER_CUBIC)
            rgba_image=rgba_image.astype(np.float32) /np.max(img)
            new_texture_data = rgba_image.flatten().tolist()
            
            dpg.set_value(self.inV.tex_2_name, new_texture_data)
            
        else:
            pass
        
        # image_data = processor.image

        
        # image_data =(image_data* (255 / image_data.max())).astype(np.uint8)
        
        
        # cell_roi = processor.roi_image
       

        

        
        
