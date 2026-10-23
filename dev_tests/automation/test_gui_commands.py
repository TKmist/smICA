# This file is part of the smICA repository that is distributed under the MIT license; see below.
#
#
# ############################################################################
#
# MIT License
#
# Copyright (c) 2026 Tomasz Kalwarczyk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from __future__ import annotations

from types import SimpleNamespace

import pytest

from smICA.Required.automation_gui_commands import (
    _EXTRACT_MODE,
    _PHOT2CONC_MODE,
    SmicaGuiCommands,
)
from smICA.Required.automation_protocol import AutomationProtocolError
from smICA.Required.automation_registry import AutomationCommandRegistry


class FakeDpg:
    def __init__(self):
        self.values = {}
        self.events = []

    def does_item_exist(self, tag):
        return tag in self.values

    def set_value(self, tag, value):
        self.values[tag] = value
        self.events.append(("set", tag, value))

    def get_value(self, tag):
        return self.values.get(tag)

    def get_aliases(self):
        return list(self.values)


class FakeMode:
    def __init__(self):
        self.events = []
        self.files = ["sample.ptu"]
        self.anal_file = "sample.ptu"
        self.last_directory = "/data"
        self.MODE = "PIE"
        self.display_option = "Foreground intensity"
        self.PTU_directory = "/data"
        self.ROI_directory = None

    def __getattr__(self, name):
        if name.startswith("callback_") or name in {
            "calllback_use_stat_filters_chbx",
            "add_single_result_to_DF",
            "copy_roi_from_channel",
            "show_br_fltr_wndw",
            "_update_textures_both_roi",
            "_roi_mode",
            "Export_result_dataframe_to_file",
            "Load_Save_Calib_file",
        }:
            def callback(*args):
                self.events.append((name, *args))
            return callback
        raise AttributeError(name)


def make_commands(mounted=_EXTRACT_MODE):
    registry = AutomationCommandRegistry()
    dpg = FakeDpg()
    mode = FakeMode()
    in_v = SimpleNamespace(mounted_method=mounted)

    class Menu:
        def __init__(self, target):
            self.target = target
            self.calls = 0

        def callback_PHOTEXTR_menu(self):
            self.calls += 1
            in_v.mounted_method = _EXTRACT_MODE

        def callback_PHOT2CONC_menu(self):
            self.calls += 1
            in_v.mounted_method = _PHOT2CONC_MODE

    extract_menu = Menu(_EXTRACT_MODE)
    phot_menu = Menu(_PHOT2CONC_MODE)

    class BasicFunctions:
        def __init__(self):
            self.calls = []

        def callback_init_buttons(self, sender, app_data):
            self.calls.append((sender, app_data))
            if sender == "EXTRACT_FROM_PTU_INIT_BUTTON":
                extract_menu.callback_PHOTEXTR_menu()
            else:
                phot_menu.callback_PHOT2CONC_menu()
            dpg.values.pop("initial_window", None)

    basic_functions = BasicFunctions()
    context = {
        "inV": in_v,
        "mode_cmn": mode,
        "PE_manu_F": extract_menu,
        "P2C_manu_F": phot_menu,
        "basf": basic_functions,
    }
    commands = SmicaGuiCommands(registry, dpg, lambda: context)
    return commands, registry, dpg, mode, context, extract_menu, phot_menu


def invoke(registry, name, parameters):
    command = registry.resolve(name)
    return command.handler(registry.validate(command, parameters))


def test_public_commands_do_not_expose_widget_tags() -> None:
    _, registry, *_ = make_commands()
    assert "gui.set_widget" not in registry.names()
    assert "gui.call_callback" not in registry.names()
    assert "extract.set_gate" in registry.names()
    assert "extract.set_background_range" in registry.names()
    assert "extract.open_decay_library" in registry.names()
    assert "extract.select_library_decay" in registry.names()
    assert "extract.import_library_decays" in registry.names()
    assert "extract.select_filter" in registry.names()
    assert "phot2conc.calculate" in registry.names()


def test_select_mode_uses_existing_menu_callback() -> None:
    _, registry, _, _, context, _, phot_menu = make_commands()
    result = invoke(registry, "gui.select_mode", {"mode": "phot2conc"})
    assert phot_menu.calls == 1
    assert context["inV"].mounted_method == _PHOT2CONC_MODE
    assert result["mode"] == "phot2conc"


def test_select_mode_uses_initial_button_callback_and_removes_start_screen() -> None:
    _, registry, dpg, _, context, extract_menu, _ = make_commands(None)
    dpg.values["initial_window"] = True
    result = invoke(registry, "gui.select_mode", {"mode": "extract"})
    assert context["basf"].calls == [("EXTRACT_FROM_PTU_INIT_BUTTON", None)]
    assert extract_menu.calls == 1
    assert dpg.does_item_exist("initial_window") is False
    assert result["mounted_method"] == _EXTRACT_MODE


def test_extract_gate_sets_widgets_then_invokes_their_callbacks() -> None:
    _, registry, dpg, mode, *_ = make_commands()
    result = invoke(registry, "extract.set_gate", {
        "channel": 1,
        "lower_ns": 2.5,
        "upper_ns": 19.5,
    })
    assert dpg.events == [
        ("set", "bottom_limit_ch1", 2.5),
        ("set", "upper_limit_ch1", 19.5),
    ]
    assert mode.events == [
        ("callback_query", "bottom_limit_ch1", 2.5),
        ("callback_query", "upper_limit_ch1", 19.5),
    ]
    assert result == {"channel": 1, "lower_ns": 2.5, "upper_ns": 19.5}


def test_extract_load_directory_uses_the_native_file_dialog_callback(tmp_path) -> None:
    _, registry, _, mode, *_ = make_commands()

    invoke(registry, "extract.load_directory", {"directory": str(tmp_path)})

    assert mode.events == [
        (
            "callback_open_folder",
            "PTU_dir_dialog",
            {"current_path": str(tmp_path)},
        ),
    ]


def test_filter_setup_uses_existing_setup_callback() -> None:
    _, registry, _, mode, *_ = make_commands()
    result = invoke(registry, "extract.open_filter_setup", {"channel": 2})
    assert mode.events == [("show_br_fltr_wndw", "Remove_bgd_butt_ch_2")]
    assert result == {"channel": 2, "setup_open": True}


def test_background_range_uses_existing_checkbox_callback() -> None:
    _, registry, dpg, mode, *_ = make_commands()
    mode.bg_channel_marker = 2

    result = invoke(registry, "extract.set_background_range", {
        "channel": 2,
        "enabled": True,
    })

    assert dpg.events == [("set", "add_bg_range", True)]
    assert mode.events == [
        ("callback_Set_background_range", "add_bg_range", True),
    ]
    assert result == {"channel": 2, "enabled": True}


def test_decay_library_commands_follow_gui_callbacks() -> None:
    _, registry, dpg, mode, *_ = make_commands()
    mode.bg_channel_marker = 1
    name = "(Ch1) Dex_100nM_40_uW_PD_15.12us_PXS_100.3nm1.ptu"
    name_tag = "decays_lib_tab_row_3_cell a_text"
    checkbox = "decays_lib_tab_row_3_cell e_chk"
    dpg.values.update({name_tag: name, checkbox: False})

    opened = invoke(registry, "extract.open_decay_library", {"channel": 1})
    selected = invoke(registry, "extract.select_library_decay", {
        "channel": 1,
        "name": name,
    })
    imported = invoke(registry, "extract.import_library_decays", {"channel": 1})

    assert opened["available_decays"] == [name]
    assert selected == {"channel": 1, "name": name, "selected": True}
    assert imported == {"channel": 1, "imported_decays": [name]}
    assert dpg.values[checkbox] is True
    assert mode.events == [
        ("callback_import_from_library", "Add_decay_from_lib", None),
        ("callback_check_lib_decay", checkbox, True),
        ("callback_Proceed_library_import", "Proceed_library_import", None),
    ]


def test_select_library_decay_reports_available_records() -> None:
    _, registry, dpg, mode, *_ = make_commands()
    mode.bg_channel_marker = 1
    dpg.values.update({
        "decays_lib_tab_row_0_cell a_text": "available decay",
        "decays_lib_tab_row_0_cell e_chk": False,
    })

    with pytest.raises(AutomationProtocolError) as raised:
        invoke(registry, "extract.select_library_decay", {
            "channel": 1,
            "name": "missing decay",
        })

    assert raised.value.code == "OPERATION_UNAVAILABLE"
    assert raised.value.details["available_decays"] == ["available decay"]


def test_select_filter_uses_existing_checkbox_callback() -> None:
    _, registry, dpg, mode, *_ = make_commands()
    name = "(Ch1) Dextran pattern"
    name_tag = "filters_ch_1_tab_list_row_0_cell a_text"
    checkbox = "filters_ch_1_tab_list_row_0_cell b_chk"
    dpg.values.update({name_tag: name, checkbox: False})

    result = invoke(registry, "extract.select_filter", {
        "channel": 1,
        "name": name,
    })

    assert result == {"channel": 1, "name": name, "selected": True}
    assert dpg.values[checkbox] is True
    assert mode.events == [
        ("callback_select_filter_for_batch", checkbox, True),
    ]


def test_apply_all_requires_a_selected_filter() -> None:
    _, registry, dpg, _, *_ = make_commands()
    dpg.values.update({
        "use_as_statistical_filters_chkbx_ch_1": True,
        "use_as_statistical_filters_chkbx_ch_2": False,
        "filters_ch_1_tab_list_row_0_cell a_text": "Signal filter",
        "filters_ch_1_tab_list_row_0_cell b_chk": False,
    })

    with pytest.raises(AutomationProtocolError) as raised:
        invoke(registry, "extract.apply_all", {})

    assert raised.value.code == "OPERATION_UNAVAILABLE"
    assert raised.value.details == {
        "channel": 1,
        "available_filters": ["Signal filter"],
    }


def test_apply_all_ignores_a_stale_filter_on_a_hidden_channel() -> None:
    _, registry, dpg, mode, *_ = make_commands()
    dpg.values.update({
        "use_as_statistical_filters_chkbx_ch_1": False,
        "use_as_statistical_filters_chkbx_ch_2": True,
    })
    dpg.is_item_shown = lambda tag: tag.endswith("ch_1")
    calls = []

    def apply_all(*args, **kwargs):
        calls.append((args, kwargs))

    mode.callback_apply_to_all_ptus = apply_all

    result = invoke(registry, "extract.apply_all", {})

    assert result["completed"] is True
    assert calls == [
        (
            ("apply_to_all", None, None),
            {"refresh_progress": True},
        ),
    ]


def test_apply_all_returns_per_file_timing_telemetry() -> None:
    _, registry, dpg, mode, *_ = make_commands()
    dpg.values.update({
        "use_as_statistical_filters_chkbx_ch_1": False,
        "use_as_statistical_filters_chkbx_ch_2": False,
    })
    expected = [{
        "filename": "sample.ptu",
        "size_bytes": 1024,
        "wall_time_seconds": 0.25,
    }]

    def apply_all(*args, **kwargs):
        mode.last_batch_file_timings = expected

    mode.callback_apply_to_all_ptus = apply_all
    result = invoke(registry, "extract.apply_all", {})

    assert result["count"] == 1
    assert result["file_timings"] == expected


def test_calculate_filters_rejects_an_empty_component_list() -> None:
    _, registry, dpg, mode, *_ = make_commands()
    mode.bg_channel_marker = 1
    mode.filtering_routine = {"Channel 1": {"BG": False}}
    dpg.values.update({
        "decays_tab_row_0_cell a_text": "Current decay",
        "decays_tab_row_0_cell b_chk": False,
    })

    with pytest.raises(AutomationProtocolError) as raised:
        invoke(registry, "extract.calculate_filters", {"channel": 1})

    assert raised.value.code == "OPERATION_UNAVAILABLE"
    assert raised.value.details == {
        "channel": 1,
        "available_decays": ["Current decay"],
    }


def test_phot2conc_calibration_uses_all_existing_input_callbacks() -> None:
    _, registry, dpg, mode, *_ = make_commands(_PHOT2CONC_MODE)
    values = {
        "channel": 2,
        "omega": 0.25,
        "omega_error": 0.01,
        "kappa": 5.0,
        "kappa_error": 0.2,
        "brightness": 4500,
        "brightness_error": 100,
    }
    invoke(registry, "phot2conc.set_calibration", values)
    assert [event[0] for event in mode.events] == [
        "callback_omega_input",
        "callback_omega_err_input",
        "callback_kappa_input",
        "callback_kappa_err_input",
        "callback_Brightness_input",
        "callback_Brightness_err_input",
    ]
    assert dpg.values["omega_input_ch_2"] == 0.25
    assert dpg.values["Brightness_input_ch_2"] == 4500.0


def test_phot2conc_load_calibration_uses_existing_file_callback(tmp_path) -> None:
    _, registry, _, mode, *_ = make_commands(_PHOT2CONC_MODE)
    calibration = tmp_path / "calib.json"
    calibration.write_text("{}", encoding="utf-8")

    result = invoke(registry, "phot2conc.load_calibration", {
        "path": str(calibration),
    })

    assert mode.events == [
        (
            "Load_Save_Calib_file",
            "Calib_file_dialog_id",
            {
                "current_path": str(tmp_path),
                "file_path_name": str(calibration),
            },
            "Load_calib_button",
        ),
    ]
    assert result["path"] == str(calibration)


def test_decay_range_expands_upper_boundary_before_moving_minimum() -> None:
    _, registry, dpg, mode, *_ = make_commands(_PHOT2CONC_MODE)
    dpg.values["decay_range_max_ch_1"] = 25.0
    invoke(registry, "phot2conc.set_decay_range", {
        "channel": 1,
        "minimum_ns": 30.0,
        "maximum_ns": 40.0,
    })
    assert mode.events == [
        ("callback_decay_time_range", "decay_range_max_ch_1", 40.0, "1"),
        ("callback_decay_time_range", "decay_range_min_ch_1", 30.0, "1"),
    ]


def test_calculate_uses_the_same_callback_as_the_gui_button() -> None:
    _, registry, dpg, mode, *_ = make_commands(_PHOT2CONC_MODE)
    dpg.values.update({
        "sinle_phot_output_ch_1": 12.0,
        "sinle_phot_err_output_ch_1": 0.5,
        "sinle_mols_output_ch_1": 3.0,
        "sinle_mols_err_output_ch_1": 0.2,
        "single_conc_output_ch_1": 80.0,
        "single_conc_err_output_ch_1": 4.0,
    })
    result = invoke(registry, "phot2conc.calculate", {})
    assert mode.events == [("callback_calculate", "Calculate_button", None)]
    assert result["channels"]["1"]["photons_per_pixel"] == 12.0
    assert result["channels"]["1"]["concentration_nm"] == 80.0


def test_calculate_all_returns_per_file_timing_telemetry() -> None:
    _, registry, _, mode, *_ = make_commands(_PHOT2CONC_MODE)
    expected = [{
        "filename": "sample.ptu",
        "size_bytes": 2048,
        "wall_time_seconds": 0.5,
    }]

    class EmptyResults:
        def __len__(self):
            return 0

        def to_dict(self, orient):
            assert orient == "records"
            return []

    def calculate_all(*args, **kwargs):
        mode.last_batch_file_timings = expected

    mode.Sing_Results_DF = EmptyResults()
    mode.callback_calculate_all = calculate_all
    result = invoke(registry, "phot2conc.calculate_all", {})

    assert result["rows"] == 0
    assert result["file_timings"] == expected


def test_auto_roi_maps_public_fields_to_existing_controls() -> None:
    _, registry, dpg, mode, *_ = make_commands(_PHOT2CONC_MODE)
    invoke(registry, "phot2conc.set_auto_roi", {
        "channel": 1,
        "cell_threshold": 0.85,
        "many_cells": True,
    })
    assert dpg.values["cell_thres_ratio_1"] == 0.85
    assert dpg.values["multiple_cells_checkbox_1"] is True
    assert mode.events == [
        ("_update_textures_both_roi", "cell_thres_ratio_1", 0.85),
        ("_update_textures_both_roi", "multiple_cells_checkbox_1", True),
    ]


def test_auto_roi_rejects_removed_decay_time_source() -> None:
    _, registry, *_ = make_commands(_PHOT2CONC_MODE)
    with pytest.raises(AutomationProtocolError) as raised:
        invoke(registry, "phot2conc.set_auto_roi", {
            "channel": 1,
            "from_decay_time": True,
        })
    assert raised.value.code == "INVALID_PARAMETERS"


def test_mode_specific_command_reports_stable_error() -> None:
    _, registry, *_ = make_commands(_EXTRACT_MODE)
    with pytest.raises(AutomationProtocolError) as raised:
        invoke(registry, "phot2conc.calculate", {})
    assert raised.value.code == "OPERATION_UNAVAILABLE"


@pytest.mark.parametrize("parameters", [
    {"channel": 3, "lower_ns": 1, "upper_ns": 2},
    {"channel": 1, "lower_ns": 2, "upper_ns": 2},
    {"channel": 1, "lower_ns": -1, "upper_ns": 2},
    {"channel": 1, "lower_ns": 1, "upper_ns": 2, "widget": "x"},
])
def test_gate_rejects_invalid_or_internal_parameters(parameters) -> None:
    _, registry, *_ = make_commands()
    with pytest.raises(AutomationProtocolError) as raised:
        invoke(registry, "extract.set_gate", parameters)
    assert raised.value.code == "INVALID_PARAMETERS"
