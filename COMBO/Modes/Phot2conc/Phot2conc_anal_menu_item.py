
import dearpygui.dearpygui as dpg
    
class _PHOT2CONC_mounting_functions:
    
    def unmount_me(self,fcs_items):
        
        for item in reversed(fcs_items):
            dpg.delete_item(item)
        dpg.delete_item('texture_reg')
        # dpg.delete_item('keyword_handler_Phot2conc')
        dpg.set_viewport_resize_callback(callback_none)
        self.is_mounted = False
        inV.mounted_method = None        
    def mount_me(self):
        dpg.add_menu_item(label="Open PTU directory",
                  tag='Open_PTU_menu_item',
                  parent = 'menu_file_dropout',
                  before = 'menu_item_exit',
                         )
        dpg.add_menu_item(label="Open ROI directory",
                  tag='Open_ROI_menu_item',
                  parent = 'menu_file_dropout',
                  before = 'menu_item_exit',
                         )
        dpg.add_separator(tag ='File_menu_sep_1',show=True,
                  parent = 'menu_file_dropout',
                  before = 'menu_item_exit')
        dpg.add_menu_item(label="Reset results",
                  tag='Reset_results_menu_item',
                  parent = 'menu_file_dropout',
                  before = 'menu_item_exit',
                         )

        dpg.add_menu_item(label="Export settings",
                  tag='Export_settings_menu_item',
                  parent = 'menu_file_dropout',
                  before = 'menu_item_exit',
                         )
    


            
        globalITEMS.windows.extend(['Open_PTU_menu_item',
                                    'Open_ROI_menu_item',
                                    'File_menu_sep_1',
                                    'Reset_results_menu_item',
                                    'Export_settings_menu_item'])
        
        
class _PHOT2CONC_menu_functions:
    
    def __init__(self):
        self.is_mounted = False
        self.mnt = _PHOT2CONC_mounting_functions()
        
    
    def unmnt_evthn(self,items,MTHD_conf):
        for item in reversed(items):
            # print(item)
            dpg.delete_item(item)
        
        # dpg.delete_item(MTHD_conf['keyword_handler_tag'])
        exec(MTHD_conf['menu_class_func']+'.is_mounted = False')
        dpg.set_viewport_resize_callback(callback_none)
        self.is_mounted = False
        inV.mounted_method = None
        globalITEMS.windows=[]
        
    def callback_PHOT2CONC_menu(self):

        if self.is_mounted:
            self.mnt.unmount_me(globalITEMS.windows)
            globalITEMS.windows=[]
            print(dpg.get_aliases())
        else:
            if inV.mounted_method != None:
                
                othm_conf = basf.method_config_dict(inV.mounted_method)
                self.unmnt_evthn(globalITEMS.windows,othm_conf)
            else:
                pass
                
        self.mnt.mount_me()
        
        self.is_mounted = True
        inV.mounted_method = 'Modes/Phot2conc'
        # print('SIZE_RATIO:',method_init.size_ratio)
    
        
        path_to_layout = os.path.join('Modes/Phot2conc',basf.path_to_method_anal_layout('Modes/Phot2conc'))
        execfile(path_to_layout)
        # mode_cmn.load_json()
        mode_cmn.define_file_menu_callbacks()
        
    
            
        
        
        
        
        
        
        
P2C_manu_F = _PHOT2CONC_menu_functions()

dpg.add_menu_item(label="Phot2Conc",
                          parent ='menu_analysis_method_dropout' ,
                          tag='Analysis_submenu_item_Phot2conc',
                          callback=P2C_manu_F.callback_PHOT2CONC_menu)




P2C_manu_F.callback_PHOT2CONC_menu()