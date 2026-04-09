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

    # przycisk "fit"
    "button":           (100, 153, 61, 255),
    "button_hovered":   (117, 178, 71, 255),
    "button_active":    (134, 204, 81, 255),
    "button_disabled":  (77, 92, 61, 255),

    "button_inactive":  (122, 153, 92, 255),

    # ploty
    "plot_line":        (31, 255, 0, 255),
    "plot_fill":        (62, 122, 56, 64),
    "plot_fill_line":   (62, 122, 56, 90),
    "plot_filter":      (12, 172, 182, 255),
}

LIGHT = {
    # baza okien
    "viewport_bg":      (242, 244, 243, 255),
    "window_bg":        (242, 244, 243, 255),
    "child_bg":         (249, 250, 249, 255),
    "popup_bg":         (255, 255, 255, 255),

    # tekst
    "text":             (28, 30, 28, 255),
    "text_disabled":    (135, 140, 135, 255),

    # pola / inputy
    "frame_bg":         (235, 238, 236, 255),
    "frame_bg_hovered": (222, 226, 223, 255),
    "frame_bg_active":  (210, 214, 210, 255),

    # 🔹 AKCENT (muted green)
    "button":           (80, 130, 100, 255),
    "button_hovered":   (95, 150, 115, 255),
    "button_active":    (65, 110, 85, 255),
    "button_disabled":  (180, 200, 190, 255),

    "button_inactive":  (150, 175, 160, 255),

    # sekcje
    "header":           (222, 226, 223, 255),
    "header_hovered":   (208, 214, 210, 255),
    "header_active":    (195, 200, 196, 255),

    # title / menu
    "title_bg":         (232, 235, 233, 255),
    "title_bg_active":  (215, 220, 217, 255),
    "menu_bar_bg":      (236, 239, 237, 255),

    # detale
    "check_mark":       (70, 120, 95, 220),
    "separator":        (180, 185, 182, 255),
    "modal_dim":        (0, 0, 0, 90),

    # statusy (spójne z akcentem)
    "menu_text":        (28, 30, 28, 255),
    "menu_warn":        (120, 140, 90, 255),   # lekko oliwkowy (lepszy niż czerwony/green clash)
    "menu_ok":          (80, 130, 100, 255),

    # error window (lekko złagodzone)
    "error_window_bg":  (255, 240, 240, 255),
    "error_title_bg":   (215, 100, 100, 255),
    "error_button":     (190, 85, 85, 255),

    # checkboxy
    "checkbox_active":  (70, 120, 95, 180),
    "checkbox_disabled":(170, 175, 170, 90),

    # ploty (spójne z akcentem)
    "plot_line":        (80, 130, 100, 255),
    "plot_fill":        (80, 130, 100, 48),
    "plot_fill_line":   (80, 130, 100, 90),

    # kontrastowy kolor pomocniczy (zostawiam teal — bardzo dobry kontrast)
    "plot_filter":      (0, 140, 150, 255),
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





def create_button_theme(p):
    with dpg.theme(tag="button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,         p["button"],          category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   p["button_active"],   category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  p["button_hovered"],  category=dpg.mvThemeCat_Core)

        with dpg.theme_component(dpg.mvButton, enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_Button,         p["button_disabled"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   p["button_disabled"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  p["button_disabled"], category=dpg.mvThemeCat_Core)


def create_button_theme_inactive(p):
    with dpg.theme(tag="button_theme_inactive"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button,         p["button_inactive"], category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  p["button_hovered"],  category=dpg.mvThemeCat_Core)


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

def build_themes(mode: str):
    p = DARK if mode == "dark" else LIGHT

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

build_themes('light')
# build_themes('dark')