with dpg.viewport_menu_bar(tag="vieport's_menubar"):
    with dpg.menu(label="Menu"):
        
        dpg.add_menu_item(label="Exit",callback=lambda:dpg.stop_dearpygui())
    with dpg.menu(label="About"):
        dpg.add_menu_item(label='License',callback = callback_licence)
        dpg.add_menu_item(label='Version: '+VERSION,enabled=False)
