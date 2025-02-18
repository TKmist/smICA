'''
This file is part of the smICA repository that is distributed under the MIT license; see below.


############################################################################

MIT License

Copyright (c) 2024 Tomasz Kalwarczyk

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

dpg.add_file_dialog(directory_selector=True,
                    label = 'Select source ROI folder',
                    width =400,
                    height=300,
                    
                    show=False,
                    file_count=5,

                    callback=callback_open_source_folder,
                    cancel_callback=callback_empty,
                    tag="Source_file_dialog",
                    modal=False
                   )


dpg.add_file_dialog(directory_selector=True,
                    label = 'Select target ROI folder',
                    show=False,
                    width =400,
                    height=300,

                    file_count=5,

                    callback=callback_open_target_folder,
                    cancel_callback=callback_empty,
                    tag="Target_file_dialog",
                    modal=False
                   )
