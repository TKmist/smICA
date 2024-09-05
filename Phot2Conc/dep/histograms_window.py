log_it('histograms_window.py - loaded on '+str(datetime.datetime.now()),'a')

# width_1=init_widths['image_window_ch1']
# height_1 =init_heights['image_window_ch1']
# position_1 = init_position['image_window_ch1']
# width_2=init_widths['image_window_ch2']
# height_2 =init_heights['image_window_ch2']
# position_2 = init_position['image_window_ch2']

with dpg.window(label = 'Results channel 1',
                tag='hist_window_ch1',
                width = dpg.get_item_width(tex_1_name)+int(1.5*init_internal_indent),
                height = dpg.get_item_height(tex_1_name)*hist_scaller,
                pos = init_position['hist_window_ch1'],
                autosize=False,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_bring_to_front_on_focus=True,
                no_move=True,
                show=True
               ):
    ###############################################
    dpg.add_separator(tag ='HIST_CH1_top_sep',show=True)
    ###############################################
    with dpg.tab_bar():
        with dpg.tab(label="Concentration/pixel"):
            with dpg.plot(label="",
                          height=-1,
                          width=-1,
                          no_menus=True,
                          no_box_select=True,no_mouse_pos=True,
                         tag = 'hist_conc_plot_ch1',
                         show=False):
                dpg.add_plot_legend(outside=True,location =dpg.mvPlot_Location_South)
                dpg.add_plot_axis(dpg.mvXAxis, label="Concentration per pixel [nM]", no_gridlines=True, tag="hist_xc_axis_ch1")
                # dpg.set_axis_limits(dpg.last_item(), 0, 100)
                # dpg.set_axis_ticks(dpg.last_item(), (("S1", 11), ("S2", 21), ("S3", 31)))
                # values=np.random.normal(0, 1, 1000)
                # hist,bins =np.histogram(values,density=True,bins='auto')
                # bins=bins[:-1]
                # print(values)
                # print(bins,hist)
                # create y axis
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_yc_axis_ch1")
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xc_axis_ch1',label='Cocnentration per pixel distribution',tag='c_dist_ser_ch_1')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xc_axis_ch1',label='Mean = ',tag='c_mean_ser_ch_1')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xc_axis_ch1',label='Median = ',tag='c_med_ser_ch_1')
        with dpg.tab(label="N_p/pixel"):
            with dpg.plot(label="",
                          height=-1,
                          width=-1,
                          no_menus=True,
                          no_box_select=True,no_mouse_pos=True,
                         tag = 'hist_np_plot_ch1',
                         show=False):
                dpg.add_plot_legend(outside=True,location =dpg.mvPlot_Location_South)
                dpg.add_plot_axis(dpg.mvXAxis, label="Number of molecules per pixel", no_gridlines=True, tag="hist_xnp_axis_ch1")
                # dpg.set_axis_limits(dpg.last_item(), 0, 100)
                # dpg.set_axis_ticks(dpg.last_item(), (("S1", 11), ("S2", 21), ("S3", 31)))
                # values=np.random.normal(0, 1, 1000)
                # hist,bins =np.histogram(values,density=True,bins='auto')
                # bins=bins[:-1]
                # print(values)
                # print(bins,hist)
                # create y axis
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_ynp_axis_ch1")
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xnp_axis_ch1',label='N_p per pixel distribution',tag='np_dist_ser_ch_1')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xnp_axis_ch1',label='Mean = ',tag='np_mean_ser_ch_1')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xnp_axis_ch1',label='Median = ',tag='np_med_ser_ch_1')
        with dpg.tab(label="Photons/pixel"):
            with dpg.plot(label="",
                          height=-1,
                          width=-1,
                          no_menus=True,
                          no_box_select=True,no_mouse_pos=True,
                         tag = 'hist_phot_plot_ch1',
                         show=False):
                dpg.add_plot_legend(outside=True,location =dpg.mvPlot_Location_South)
                dpg.add_plot_axis(dpg.mvXAxis, label="Photons per pixel", no_gridlines=True, tag="hist_xphot_axis_ch1")
                # dpg.set_axis_limits(dpg.last_item(), 0, 100)
                # dpg.set_axis_ticks(dpg.last_item(), (("S1", 11), ("S2", 21), ("S3", 31)))
                # values=np.random.normal(0, 1, 1000)
                # hist,bins =np.histogram(values,density=True,bins='auto')
                # bins=bins[:-1]
                # print(values)
                # print(bins,hist)
                # create y axis
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_yphot_axis_ch1")
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xphot_axis_ch1',label='Photons per pixel distribution',tag='phot_dist_ser_ch_1')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xphot_axis_ch1',label='Mean = ',tag='phot_mean_ser_ch_1')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xphot_axis_ch1',label='Median = ',tag='phot_med_ser_ch_1')
        # dpg.add_drag_line(label="dline1", color=[255, 0, 0, 255], default_value=np.mean(values))
        
    # pass
#     dpg.add_image(tex_1_name,
#                   uv_min=(0,0),
#                   uv_max=(1,1),
#                   tag = 'texture_CH_1')
    
with dpg.window(label = 'Results channel 2',
                tag='hist_window_ch2',
                width = dpg.get_item_width(tex_2_name)+int(1.5*init_internal_indent),
                height = dpg.get_item_height(tex_2_name)*hist_scaller,
                pos = init_position['hist_window_ch2'],
                autosize=False,
                no_resize=True,
                no_close=True,
                no_collapse=True,
                no_bring_to_front_on_focus=True,
                no_move=True,
                show=True
               ):
    ###############################################
    dpg.add_separator(tag ='HIST_CH2_top_sep',show=True)
    ###############################################
    with dpg.tab_bar():
        with dpg.tab(label="Concentration/pixel"):
            with dpg.plot(label="",
                          height=-1,
                          width=-1,
                          no_menus=True,
                          no_box_select=True,no_mouse_pos=True,
                            tag = 'hist_conc_plot_ch2',
                         show=False):
                dpg.add_plot_legend(outside=True,location =dpg.mvPlot_Location_South)
                dpg.add_plot_axis(dpg.mvXAxis, label="Concentration per pixel [nM]", no_gridlines=True, tag="hist_xc_axis_ch2")
                # dpg.set_axis_limits(dpg.last_item(), 0, 100)
                # dpg.set_axis_ticks(dpg.last_item(), (("S1", 11), ("S2", 21), ("S3", 31)))
                # values=np.random.normal(1, 1, 1000)
                # hist,bins =np.histogram(values,density=True,bins='auto')
                # bins=bins[:-1]
                # print(values)
                # print(bins,hist)
                # create y axis
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_yc_axis_ch2")
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xc_axis_ch2',label='Cocnentration per pixel distribution',tag='c_dist_ser_ch_2')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xc_axis_ch2',label='Mean = ',tag='c_mean_ser_ch_2')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xc_axis_ch2',label='Median = ',tag='c_med_ser_ch_2')
        with dpg.tab(label="N_p/pixel"):
            with dpg.plot(label="",
                          height=-1,
                          width=-1,
                          no_menus=True,
                          no_box_select=True,no_mouse_pos=True,
                            tag = 'hist_np_plot_ch2',
                         show=False):
                dpg.add_plot_legend(outside=True,location =dpg.mvPlot_Location_South)
                dpg.add_plot_axis(dpg.mvXAxis, label="Number of molecules per pixel", no_gridlines=True, tag="hist_xnp_axis_ch2")
                # dpg.set_axis_limits(dpg.last_item(), 0, 100)
                # dpg.set_axis_limits(dpg.last_item(), 0, 100)
                # dpg.set_axis_ticks(dpg.last_item(), (("S1", 11), ("S2", 21), ("S3", 31)))
                # values=np.random.normal(1, 1, 1000)
                # hist,bins =np.histogram(values,density=True,bins='auto')
                # bins=bins[:-1]
                # print(values)
                # print(bins,hist)
                # create y axis
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_ynp_axis_ch2")
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xnp_axis_ch2',label='N_p per pixel distribution',tag='np_dist_ser_ch_2')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xnp_axis_ch2',label='Mean = ',tag='np_mean_ser_ch_2')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xnp_axis_ch2',label='Median = ',tag='np_med_ser_ch_2')
        with dpg.tab(label="Photons/pixel"):
            with dpg.plot(label="",
                          height=-1,
                          width=-1,
                          no_menus=True,
                          no_box_select=True,no_mouse_pos=True,
                            tag = 'hist_phot_plot_ch2',
                         show=False):
                dpg.add_plot_legend(outside=True,location =dpg.mvPlot_Location_South)
                dpg.add_plot_axis(dpg.mvXAxis, label="Photons per pixel", no_gridlines=True, tag="hist_xphot_axis_ch2")
                # dpg.set_axis_limits(dpg.last_item(), 0, 100)
                # dpg.set_axis_ticks(dpg.last_item(), (("S1", 11), ("S2", 21), ("S3", 31)))
                # values=np.random.normal(1, 1, 1000)
                # hist,bins =np.histogram(values,density=True,bins='auto')
                # bins=bins[:-1]
                # print(values)
                # print(bins,hist)
                # create y axis
                dpg.add_plot_axis(dpg.mvYAxis, label="PDF", tag="hist_yphot_axis_ch2")
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xphot_axis_ch2',label='Photons per pixel distribution',tag='phot_dist_ser_ch_2')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xphot_axis_ch2',label='Mean = ',tag='phot_mean_ser_ch_2')
                dpg.add_stem_series(np.empty(10),np.empty(10),parent = 'hist_xphot_axis_ch2',label='Median = ',tag='phot_med_ser_ch_2')
    # dpg.add_image(tex_2_name,
    #               uv_min=(0,0),
    #               uv_max=(1,1),
    #               tag = 'texture_CH_2')


# width = init_widths['FCS_window']
# height =init_widths['FCS_window']
# texture_data = []


# directory = 'samples/data'


# with dpg.window(label='',
#                 pos=init_position['image_window'],
#                 width=init_widths['image_window'],
#                 height=init_heights['image_window'],
#                 no_move=True,
#                 no_close=True,
#                 no_title_bar=True,
#                 no_resize=True,
#                 tag='image_window',
#                 show=True
#                ):
#     pass
#     '''Window containing file selection panel.'''
#     with dpg.group(tag='dir_sel_group',horizontal=True,horizontal_spacing=init_group_spacer):
#         dpg.add_input_text(default_value='',
#                            tag = 'directory_input_text',
#                            on_enter=True,
#                            hint='Enter relative path to directory or Browse',
#                           width =init_widths['directory_input_text'] )
#         dpg.add_button(label="Browse",
#                    callback=lambda: dpg.show_item("file_dialog_id"),
#                    width = init_widths['Browse_directory_button'],
#                    tag='Browse_directory_button',
#                    show=True,enabled=True
#                   )
#         dpg.bind_item_theme('Browse_directory_button', 'fit_button_theme')  
#     dpg.add_separator(tag ='sep_left_1')
#     list_box = dpg.add_listbox(items=files,
#                                width=init_widths['file_box'],
#                                num_items=10,
#                                tag='file_box',
# #                                callback=callback_listbox
#                               )
#     dpg.add_separator(tag ='sep_left_2',show=False)
#     with dpg.group(tag='PTU_metadata',show=False):
#         dpg.add_text(default_value='Number of chanels:',show=True,tag='N_channels')
