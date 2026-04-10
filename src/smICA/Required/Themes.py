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




DARK = {
    # baza okien
    "viewport_bg":        (0, 0, 0, 255),
    "window_bg":        (37, 37, 38, 255),
    "child_bg":         (30, 30, 30, 255),
    "popup_bg":         (50, 50, 52, 255),

    # tekst
    "text":             (235, 235, 235, 255),
    "text_disabled":    (150, 150, 150, 255),

    # pola / inputy
    "frame_bg":         (51, 51, 55, 255),
    "frame_bg_hovered": (66, 66, 72, 255),
    "frame_bg_active":  (78, 78, 84, 255),

    # buttony ogólne
    # "button":           (66, 66, 70, 255),
    # "button_hovered":   (86, 86, 92, 255),
    # "button_active":    (98, 98, 106, 255),

    # sekcje rozwijane / select / table header-like
    "header":           (70, 70, 74, 255),
    "header_hovered":   (90, 90, 96, 255),
    "header_active":    (102, 102, 110, 255),

    # title / menu
    "title_bg":         (45, 45, 48, 255),
    "title_bg_active":  (60, 60, 65, 255),
    "menu_bar_bg":      (45, 45, 48, 255),

    # detale
    "check_mark":       (0, 119, 200, 180),
    "separator":        (95, 95, 100, 255),
    "modal_dim":        (5, 5, 5, 215),

    # statusy menu
    "menu_text":        (255, 255, 255, 255),
    "menu_warn":        (246, 115, 10, 255),
    "menu_ok":          (62, 190, 15, 255),

    # error window
    "error_window_bg":  (139, 16, 16, 255),
    "error_title_bg":   (83, 23, 23, 255),
    "error_button":     (116, 7, 29, 255),

    # checkboxy
    "checkbox_active":  (0, 119, 200, 153),
    "checkbox_disabled":(194, 194, 194, 45),

    # zwykłe buttony
    # zwykłe buttony
    "button":           (66, 66, 70, 255),
    "button_hovered":   (86, 86, 92, 255),
    "button_active":    (98, 98, 106, 255),
    "button_disabled":  (55, 55, 58, 255),

    # action buttony
    "action_button":           (100, 153, 61, 255),
    "action_button_hovered":   (117, 178, 71, 255),
    "action_button_active":    (134, 204, 81, 255),
    "action_button_disabled":  (77, 92, 61, 255),
    "action_button_inactive":  (122, 153, 92, 255),

    # ploty
    "plot_line":        (31, 255, 0, 255),
    "plot_fill":        (62, 122, 56, 64),
    "plot_fill_line":   (62, 122, 56, 90),
    "plot_filter":      (12, 172, 182, 255),

        # border / outlines
    "border":              (110, 110, 115, 255),
    "border_shadow":       (0, 0, 0, 0),

    # scrollbars
    "scrollbar_bg":        (43, 43, 46, 255),
    "scrollbar_grab":      (95, 120, 100, 255),
    "scrollbar_grab_hovered": (110, 140, 115, 255),
    "scrollbar_grab_active":  (125, 155, 130, 255),

    # tabs
    "tab":                 (58, 62, 60, 255),
    "tab_hovered":         (78, 96, 82, 255),
    "tab_active":          (95, 120, 100, 255),
    "tab_unfocused":       (50, 52, 54, 255),
    "tab_unfocused_active":(72, 88, 76, 255),
}

LIGHT = {
    # baza okien (bardziej jasna)
    "viewport_bg":      (246, 247, 246, 255),
    "window_bg":        (246, 247, 246, 255),
    "child_bg":         (252, 253, 252, 255),
    "popup_bg":         (255, 255, 255, 255),

    # tekst (lekko złagodzony)
    "text":             (40, 42, 40, 255),
    "text_disabled":    (150, 155, 150, 255),

    # pola / inputy (jaśniejsze!)
    "frame_bg":         (225, 227, 225, 255),
    "frame_bg_hovered": (232, 235, 232, 255),
    "frame_bg_active":  (224, 228, 224, 255),

    # zwykłe buttony
    "button":           (226, 230, 226, 255),
    "button_hovered":   (214, 220, 214, 255),
    "button_active":    (202, 210, 202, 255),
    "button_disabled":  (235, 238, 235, 255),

    # action buttony
    "action_button":           (150, 175, 140, 255),
    "action_button_hovered":   (165, 190, 155, 255),
    "action_button_active":    (135, 160, 125, 255),
    "action_button_disabled":  (210, 220, 205, 255),
    "action_button_inactive":  (190, 205, 185, 255),

    # sekcje (bardzo subtelne różnice)
    "header":           (206, 209, 206, 255),
    "header_hovered":   (200, 202, 200, 255),
    "header_active":    (200, 205, 200, 255),

    # title / menu
    "title_bg":         (240, 243, 240, 255),
    "title_bg_active":  (230, 235, 230, 255),
    "menu_bar_bg":      (242, 245, 242, 255),

    # detale
    "check_mark":       (110, 150, 120, 220),
    "separator":        (200, 205, 200, 255),
    "modal_dim":        (250, 250, 250, 220),

    # statusy
    "menu_text":        (40, 42, 40, 255),
    "menu_warn":        (170, 180, 120, 255),  # oliwkowy — spokojniejszy niż czerwony
    "menu_ok":          (150, 175, 140, 255),

    # error window (też złagodzony)
    "error_window_bg":  (255, 245, 245, 255),
    "error_title_bg":   (220, 120, 120, 255),
    "error_button":     (200, 100, 100, 255),

    # checkboxy
    "checkbox_active":  (110, 150, 120, 180),
    "checkbox_disabled":(190, 195, 190, 90),

    # ploty (pastelowe, nie agresywne)
    "plot_line":        (140, 170, 135, 255),
    "plot_fill":        (140, 170, 135, 48),
    "plot_fill_line":   (140, 170, 135, 90),

    # kontrast pomocniczy
    "plot_filter":      (120, 160, 170, 255),

        # border / outlines
    "border":              (185, 190, 185, 255),
    "border_shadow":       (0, 0, 0, 0),

    # scrollbars
    "scrollbar_bg":        (236, 239, 236, 255),
    "scrollbar_grab":      (170, 188, 165, 255),
    "scrollbar_grab_hovered": (150, 175, 140, 255),
    "scrollbar_grab_active":  (130, 160, 125, 255),

    # tabs
    "tab":                 (205, 212, 205, 255),
    "tab_hovered":         (180, 200, 175, 255),
    "tab_active":          (150, 175, 140, 255),
    "tab_unfocused":       (215, 220, 215, 255),
    "tab_unfocused_active":(185, 198, 182, 255),
}

def create_global_theme(p):
    with dpg.theme(tag="global_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,         p["window_bg"],        category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg,          p["child_bg"],         category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg,          p["popup_bg"],         category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_Text,             p["text"],             category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled,     p["text_disabled"],    category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_FrameBg,          p["frame_bg"],         category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,   p["frame_bg_hovered"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,    p["frame_bg_active"],  category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_Button,           p["button"],           category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,    p["button_hovered"],   category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,     p["button_active"],    category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_Header,           p["header"],           category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,    p["header_hovered"],   category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive,     p["header_active"],    category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_TitleBg,          p["title_bg"],         category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,    p["title_bg_active"],  category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg,        p["menu_bar_bg"],      category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_CheckMark,        p["check_mark"],       category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Separator,        p["separator"],        category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ModalWindowDimBg, p["modal_dim"],        category=dpg.mvThemeCat_Core)


            dpg.add_theme_color(dpg.mvThemeCol_Border,             p["border"],             category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow,       p["border_shadow"],      category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,        p["scrollbar_bg"],       category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,      p["scrollbar_grab"],     category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, p["scrollbar_grab_hovered"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive,  p["scrollbar_grab_active"],  category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_Tab,                p["tab"],                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered,         p["tab_hovered"],        category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive,          p["tab_active"],         category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused,       p["tab_unfocused"],      category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, p["tab_unfocused_active"], category=dpg.mvThemeCat_Core)





def create_button_theme(p):
    with dpg.theme(tag="button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,         p["action_button"],          category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   p["action_button_active"],   category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  p["action_button_hovered"],  category=dpg.mvThemeCat_Core)

        with dpg.theme_component(dpg.mvButton, enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_Button,         p["action_button_disabled"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   p["action_button_disabled"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  p["action_button_disabled"], category=dpg.mvThemeCat_Core)


def create_button_theme_inactive(p):
    with dpg.theme(tag="button_theme_inactive"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,         p["action_button_inactive"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  p["action_button_hovered"],  category=dpg.mvThemeCat_Core)


def create_error_window_theme(p):
    with dpg.theme(tag="Error_window_theme"):
        with dpg.theme_component(dpg.mvWindowAppItem):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,       p["error_window_bg"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,  p["error_title_bg"],  category=dpg.mvThemeCat_Core)

        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,         p["error_button"],    category=dpg.mvThemeCat_Core)


def create_checkbox_themes(p):
    with dpg.theme(tag="Inactive_checkbox"):
        with dpg.theme_component(dpg.mvCheckbox):
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, p["checkbox_active"], category=dpg.mvThemeCat_Core)
        with dpg.theme_component(dpg.mvCheckbox, enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, p["checkbox_disabled"], category=dpg.mvThemeCat_Core)

    with dpg.theme(tag="Active_checkbox"):
        with dpg.theme_component(dpg.mvCheckbox):
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, p["checkbox_active"], category=dpg.mvThemeCat_Core)


def create_menu_themes(p):
    with dpg.theme(tag="menu_normal"):
        with dpg.theme_component(dpg.mvMenu):
            dpg.add_theme_color(dpg.mvThemeCol_Text, p["menu_text"], category=dpg.mvThemeCat_Core)
        with dpg.theme_component(dpg.mvMenuItem):
            dpg.add_theme_color(dpg.mvThemeCol_Text, p["menu_text"], category=dpg.mvThemeCat_Core)

    with dpg.theme(tag="menu_update_available"):
        with dpg.theme_component(dpg.mvMenu):
            dpg.add_theme_color(dpg.mvThemeCol_Text, p["menu_warn"], category=dpg.mvThemeCat_Core)
        with dpg.theme_component(dpg.mvMenuItem, enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_Text, p["menu_warn"], category=dpg.mvThemeCat_Core)
        with dpg.theme_component(dpg.mvMenuItem):
            dpg.add_theme_color(dpg.mvThemeCol_Text, p["menu_warn"], category=dpg.mvThemeCat_Core)

    with dpg.theme(tag="menu_update_available_new"):
        with dpg.theme_component(dpg.mvMenu):
            dpg.add_theme_color(dpg.mvThemeCol_Text, p["menu_warn"], category=dpg.mvThemeCat_Core)
        with dpg.theme_component(dpg.mvMenuItem, enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_Text, p["menu_ok"], category=dpg.mvThemeCat_Core)
        with dpg.theme_component(dpg.mvMenuItem):
            dpg.add_theme_color(dpg.mvThemeCol_Text, p["menu_ok"], category=dpg.mvThemeCat_Core)


def create_transparent_theme():
    with dpg.theme(tag="transparent_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,        (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,  (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)


def create_plot_themes(p):
    with dpg.theme(tag="plot_theme"):
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, p["plot_line"], category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 5, category=dpg.mvThemeCat_Plots)

        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, p["plot_line"], category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 4, category=dpg.mvThemeCat_Plots)

        with dpg.theme_component(dpg.mvShadeSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, p["plot_fill"], category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_Line, p["plot_fill_line"], category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_LineWeight, 4, category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="plot_bg_filter_theme"):
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, p["plot_filter"], category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 5, category=dpg.mvThemeCat_Plots)

def apply_viewport_color(p):
    dpg.set_viewport_clear_color(p["viewport_bg"])

def delete_theme_if_exists(tag):
    print(tag,end='\t')
    if dpg.does_item_exist(tag):
        
        dpg.delete_item(tag)
        print('deleted', dpg.does_item_exist(tag))
    else:
        print('not deleted')

def delete_all_themes():
    THEME_TAGS = [
        "global_theme",
        "button_theme",
        "button_theme_inactive",
        "plot_theme",
        "plot_bg_filter_theme",
        "Error_window_theme",
        "Inactive_checkbox",
        "Active_checkbox",
        "transparent_theme",
        "menu_normal",
        "menu_update_available",
        "menu_update_available_new",
    ]
    for tag in THEME_TAGS:
        
        delete_theme_if_exists(tag)

def build_themes(mode: str):
    p = DARK if mode == "dark" else LIGHT

    
    # delete_all_themes()
    create_global_theme(p)
    create_button_theme(p)
    create_button_theme_inactive(p)
    create_plot_themes(p)
    create_error_window_theme(p)
    create_checkbox_themes(p)
    create_transparent_theme()
    create_menu_themes(p)

    dpg.bind_theme("global_theme")
    apply_viewport_color(p)



def callback_theme(sender,app_data):
    
    theme = dpg.get_item_label(sender)
    print(theme)
    if theme == 'Dark theme':
        THEME = 'dark'
        print(THEME)
        dpg.set_item_label(sender, 'Light theme')
        build_themes(THEME)
        
    elif theme == 'Light theme':
        THEME = 'light'
        dpg.set_item_label(sender, 'Dark theme')
        build_themes(THEME)
    else:
        pass



