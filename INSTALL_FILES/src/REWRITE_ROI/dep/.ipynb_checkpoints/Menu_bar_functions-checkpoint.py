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
            dpg.add_button(tag='Licence_title',width=dpg.get_viewport_width()/2,label='LICENCE')

            dpg.bind_item_theme('Licence_title', 'transparent_theme')
            with open('Licence.txt', 'r') as file:
                Licence = file.read()
            dpg.add_text(label='Licence',
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
            dpg.add_button(tag='Licence_title',width=dpg.get_viewport_width()/2,label='LICENCE')

            dpg.bind_item_theme('Licence_title', 'transparent_theme')
            with open('Licence.txt', 'r') as file:
                Licence = file.read()
            dpg.add_text(label='Licence',
                         tag='licence_text',
                         default_value = Licence,
                         wrap = int(0.95*(dpg.get_viewport_width()/2)))
            



        
