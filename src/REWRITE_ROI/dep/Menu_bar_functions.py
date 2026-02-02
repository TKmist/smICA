'''
This file is part of the smICA repository that is distributed under the MIT license; see below.


############################################################################

MIT License

Copyright (c) 2026 Tomasz Kalwarczyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
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
            dpg.add_button(tag='Licence_title',width=dpg.get_viewport_width()/2,label='LICENSE')

            dpg.bind_item_theme('Licence_title', 'transparent_theme')
            with open('../LICENSE', 'r') as file:
                Licence = file.read()
            dpg.add_text(label='License',
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
            dpg.add_button(tag='Licence_title',width=dpg.get_viewport_width()/2,label='LICENSE')

            dpg.bind_item_theme('Licence_title', 'transparent_theme')
            with open('../LICENSE', 'r') as file:
                Licence = file.read()
            dpg.add_text(label='License',
                         tag='licence_text',
                         default_value = Licence,
                         wrap = int(0.95*(dpg.get_viewport_width()/2)))
            



        
