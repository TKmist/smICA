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
