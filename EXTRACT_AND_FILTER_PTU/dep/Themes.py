'''The themes definitions.'''
with dpg.theme(tag='global'):

    with dpg.theme_component(dpg.mvAll):


        dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, (5, 5, 5,215))


        
dpg.bind_theme('global')
with dpg.theme(tag="fit_button_theme"):
    '''Theme for active buttons'''
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            _hsv_to_rgb(2/7.0, 0.6, 0.6)
                           )
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,
                            _hsv_to_rgb(2/7.0, 0.8, 0.8)
                           )
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            _hsv_to_rgb(2/7.0, 0.7, 0.7)
                           )
    with dpg.theme_component(dpg.mvButton,enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            _hsv_to_rgb(2/7.0, 0.3, 0.3)
                           )
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,
                            _hsv_to_rgb(2/7.0, 0.3, 0.3)
                           )
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            _hsv_to_rgb(2/7.0, 0.3, 0.3)
                           )
                           
        
with dpg.theme(tag="fit_button_theme_inactive"):
    '''Theme for inactive buttons'''
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            _hsv_to_rgb(2/7.0, 0.4, 0.6)
                           )
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            _hsv_to_rgb(2/7.0, 0.7, 0.7)
                           )
                           
        
with dpg.theme(tag="plot_theme"):
    '''Themes for plot.'''
    with dpg.theme_component(dpg.mvScatterSeries):
        '''Theme for scattered points.'''
        dpg.add_theme_color(dpg.mvPlotCol_Line, (31, 255, 0), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 5, category=dpg.mvThemeCat_Plots)
        
    with dpg.theme_component(dpg.mvLineSeries):
        '''Theme for solid lines.'''        
        dpg.add_theme_color(dpg.mvPlotCol_Line, (229, 80, 48), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 4, category=dpg.mvThemeCat_Plots)
        
    with dpg.theme_component(dpg.mvShadeSeries):
        '''Theme for shade areas (errors).'''
        dpg.add_theme_color(dpg.mvPlotCol_Fill, (62, 122, 56, 64), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_Line, (62, 122, 56, 90), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 4, category=dpg.mvThemeCat_Plots)
        
        
with dpg.theme(tag="Error_window_theme"):
    '''Theme for Error windows'''
    with dpg.theme_component(dpg.mvWindowAppItem):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg,
                            (139,16,16,255)
                           )
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,
                            (83,23,23,255)
                           )
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (56,5,15,255)
                           )
        
with dpg.theme(tag="Inactive_checkbox"):
    '''Theme for inactive checkboxes'''
    with dpg.theme_component(dpg.mvCheckbox):
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark,
                            (0,119,200,153)
                           )
    with dpg.theme_component(dpg.mvCheckbox,enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark,
                            (194,194,194,45)
                           )

        
with dpg.theme(tag="Active_checkbox"):
    '''Theme for inactive checkboxes'''
    with dpg.theme_component(dpg.mvCheckbox):
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark,
                            (0,119,200,153)
                           )
BACKGROUND_COLOUR = (0,0,0,0)
with dpg.theme(tag='transparent_theme'):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            BACKGROUND_COLOUR
                           )
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,
                            BACKGROUND_COLOUR
                           )
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            BACKGROUND_COLOUR
                           )
