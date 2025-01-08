
log_it('menu_bar - loaded on '+str(datetime.datetime.now()),'a')
with dpg.viewport_menu_bar(tag="vieport's_menubar"):
    with dpg.menu(label="Menu"):
        dpg.add_menu_item(label="Open PTU directory",callback=lambda: dpg.show_item("PTU_file_dialog_id"))
        dpg.add_menu_item(label="Open ROI directory",callback=lambda: dpg.show_item("ROI_folder_dialog_id"))
        dpg.add_separator(tag ='File_menu_sep_1',show=True)
        dpg.add_menu_item(label="Reset results",callback=callback_reset_results_DF())
        dpg.add_menu_item(label="Export settings",callback=callback_exportsettings)
        dpg.add_menu_item(label="Exit",callback=lambda:dpg.stop_dearpygui())
    with dpg.menu(label="About"):
        dpg.add_menu_item(label='License',callback = callback_licence)
        dpg.add_menu_item(label='Version: '+VERSION)
