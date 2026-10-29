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


"""Public automation commands backed by the existing Dear PyGui callbacks."""

from __future__ import annotations

import math
import os
from typing import Any, Callable

from .automation_protocol import AutomationProtocolError


_EXTRACT_MODE = "Modes/Extract_from_PTU"
_PHOT2CONC_MODE = "Modes/Phot2conc"


def _invalid(message: str, **details: Any) -> None:
    raise AutomationProtocolError(
        "INVALID_PARAMETERS",
        message,
        details=details or None,
    )


def _operation_error(message: str, **details: Any) -> None:
    raise AutomationProtocolError(
        "OPERATION_UNAVAILABLE",
        message,
        details=details or None,
    )


def _fields(
    parameters: dict[str, Any],
    *,
    required: set[str] = frozenset(),
    optional: set[str] = frozenset(),
) -> dict[str, Any]:
    missing = sorted(required - set(parameters))
    unknown = sorted(set(parameters) - required - optional)
    if missing:
        _invalid("Required parameters are missing.", fields=missing)
    if unknown:
        _invalid("Unknown parameters were supplied.", fields=unknown)
    return parameters


def _text(value: Any, field: str, *, choices: set[str] | None = None) -> str:
    if not isinstance(value, str) or not value.strip():
        _invalid(f"{field} must be a non-empty string.", field=field)
    normalized = value.strip()
    if choices is not None and normalized not in choices:
        _invalid(
            f"{field} has an unsupported value.",
            field=field,
            allowed=sorted(choices),
        )
    return normalized


def _boolean(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        _invalid(f"{field} must be a boolean.", field=field)
    return value


def _number(
    value: Any,
    field: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _invalid(f"{field} must be a finite number.", field=field)
    result = float(value)
    if not math.isfinite(result):
        _invalid(f"{field} must be a finite number.", field=field)
    if minimum is not None and result < minimum:
        _invalid(f"{field} is below its minimum.", field=field, minimum=minimum)
    if maximum is not None and result > maximum:
        _invalid(f"{field} is above its maximum.", field=field, maximum=maximum)
    return result


def _channel(value: Any) -> str:
    if value in (1, "1"):
        return "1"
    if value in (2, "2"):
        return "2"
    _invalid("channel must be 1 or 2.", field="channel")


def _existing_directory(value: Any, field: str = "directory") -> str:
    path = os.path.abspath(os.path.expanduser(_text(value, field)))
    if not os.path.isdir(path):
        _invalid(f"{field} must identify an existing directory.", field=field)
    return path


def _existing_json_file(value: Any, field: str = "path") -> str:
    path = os.path.abspath(os.path.expanduser(_text(value, field)))
    if not os.path.isfile(path):
        _invalid(f"{field} must identify an existing file.", field=field)
    if os.path.splitext(path)[1].lower() != ".json":
        _invalid(f"{field} must identify a JSON file.", field=field)
    return path


def _output_file(value: Any) -> str:
    path = os.path.abspath(os.path.expanduser(_text(value, "path")))
    if not os.path.isdir(os.path.dirname(path)):
        _invalid("The output parent directory does not exist.", field="path")
    if os.path.splitext(path)[1].lower() not in {".csv", ".dat", ".pkl"}:
        _invalid("The output suffix must be .csv, .dat, or .pkl.", field="path")
    return path


def _json_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if hasattr(value, "item"):
        return _json_value(value.item())
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return str(value)


class SmicaGuiCommands:
    """Map stable public commands onto the current smICA GUI interaction path."""

    def __init__(self, registry: Any, dpg: Any, context_provider: Callable[[], dict[str, Any]]):
        self.registry = registry
        self.dpg = dpg
        self.context_provider = context_provider
        self._register_commands()

    def _context(self) -> dict[str, Any]:
        return self.context_provider()

    def _mode(self, expected: str) -> Any:
        context = self._context()
        mounted = context["inV"].mounted_method
        if mounted != expected or "mode_cmn" not in context:
            _operation_error(
                "The command requires another smICA mode.",
                required_mode=expected,
                mounted_mode=mounted,
            )
        return context["mode_cmn"]

    def _value(self, tag: str) -> Any:
        try:
            return _json_value(self.dpg.get_value(tag))
        except Exception:
            return None

    def _register(self, name: str, handler: Callable, validator: Callable, description: str) -> None:
        self.registry.register(
            name,
            handler,
            validator=validator,
            description=description,
            result_description="The resulting GUI-backed smICA state.",
        )

    def _register_commands(self) -> None:
        self._register("gui.select_mode", self.select_mode, self.validate_select_mode,
                       "Select an analysis mode through its existing menu callback.")
        self._register("extract.load_directory", self.extract_load_directory,
                       lambda p: {"directory": _existing_directory(_fields(p, required={"directory"})["directory"])},
                       "Load a PTU directory in Extract from PTU.")
        self._register("extract.select_file", self.extract_select_file, self.validate_filename,
                       "Select a loaded PTU file in Extract from PTU.")
        self._register("extract.set_gate", self.extract_set_gate, self.validate_gate,
                       "Set a channel microtime gate through the existing gate callbacks.")
        self._register("extract.set_rows_to_skip", self.extract_set_rows_to_skip,
                       self.validate_rows_to_skip, "Configure line correction through its GUI callback.")
        self._register("extract.set_statistical_filter", self.extract_set_statistical_filter,
                       self.validate_channel_enabled, "Enable or disable statistical filtering for a channel.")
        self._register("extract.open_filter_setup", self.extract_open_filter_setup,
                       self.validate_channel_only, "Open and initialize the existing statistical-filter setup.")
        self._register("extract.set_background_range", self.extract_set_background_range,
                       self.validate_channel_enabled,
                       "Enable or disable the automatic background data range.")
        self._register("extract.open_decay_library", self.extract_open_decay_library,
                       self.validate_channel_only, "Open the decay library through its GUI button.")
        self._register("extract.select_library_decay", self.extract_select_library_decay,
                       self.validate_library_decay, "Select one decay record in the open library.")
        self._register("extract.import_library_decays", self.extract_import_library_decays,
                       self.validate_channel_only, "Import the selected decay records through the GUI button.")
        self._register("extract.calculate_filters", self.extract_calculate_filters,
                       self.validate_channel_only, "Run the configured statistical-filter calculation.")
        self._register("extract.accept_filters", self.extract_accept_filters,
                       self.validate_channel_only, "Accept the calculated statistical filters.")
        self._register("extract.select_filter", self.extract_select_filter,
                       self.validate_filter_name,
                       "Select the foreground filter used for batch extraction.")
        self._register("extract.decline_filters", self.extract_decline_filters,
                       self.validate_channel_only, "Decline the calculated statistical filters.")
        self._register("extract.apply_current", self.extract_apply_current, self.validate_empty,
                       "Extract and filter the selected PTU file.")
        self._register("extract.apply_all", self.extract_apply_all, self.validate_empty,
                       "Extract and filter all loaded PTU files in deterministic GUI order.")
        self._register("extract.get_state", self.extract_get_state, self.validate_empty,
                       "Return the current Extract from PTU settings.")

        self._register("phot2conc.load_directory", self.phot_load_directory,
                       lambda p: {"directory": _existing_directory(_fields(p, required={"directory"})["directory"])},
                       "Load a PTU/PKL directory in Phot2conc.")
        self._register("phot2conc.load_roi_directory", self.phot_load_roi_directory,
                       lambda p: {"directory": _existing_directory(_fields(p, required={"directory"})["directory"])},
                       "Load an ROI directory in Phot2conc.")
        self._register("phot2conc.select_file", self.phot_select_file, self.validate_filename,
                       "Select a loaded measurement in Phot2conc.")
        self._register("phot2conc.set_display", self.phot_set_display, self.validate_display,
                       "Select the image product shown and calculated by Phot2conc.")
        self._register("phot2conc.set_decay_range", self.phot_set_decay_range,
                       self.validate_decay_range, "Set the visible decay-time interval for a channel.")
        self._register("phot2conc.set_calibration", self.phot_set_calibration,
                       self.validate_calibration, "Set FCS calibration values through their GUI callbacks.")
        self._register("phot2conc.load_calibration", self.phot_load_calibration,
                       self.validate_calibration_path,
                       "Load an FCS calibration JSON file through the existing GUI callback.")
        self._register("phot2conc.set_error_mode", self.phot_set_error_mode,
                       self.validate_error_mode, "Select propagated errors or SEM and recalculate.")
        self._register("phot2conc.set_export_options", self.phot_set_export_options,
                       self.validate_export_options, "Set array and heatmap export checkboxes.")
        self._register("phot2conc.set_roi_source", self.phot_set_roi_source,
                       self.validate_roi_source, "Select no ROI, file ROI, or automatic ROI.")
        self._register("phot2conc.set_auto_roi", self.phot_set_auto_roi,
                       self.validate_auto_roi, "Configure automatic ROI controls and refresh detection.")
        self._register("phot2conc.select_roi", self.phot_select_roi, self.validate_roi_name,
                       "Select a named ROI loaded from files.")
        self._register("phot2conc.calculate", self.phot_calculate, self.validate_empty,
                       "Run the existing single-file calculation callback.")
        self._register("phot2conc.add_result", self.phot_add_result, self.validate_empty,
                       "Add the current calculation to the results table.")
        self._register("phot2conc.calculate_all", self.phot_calculate_all, self.validate_empty,
                       "Run the existing batch calculation callback.")
        self._register("phot2conc.export_results", self.phot_export_results,
                       self.validate_export_path, "Export the results table through its existing callback.")
        self._register("phot2conc.get_state", self.phot_get_state, self.validate_empty,
                       "Return the current Phot2conc settings and results.")

    @staticmethod
    def validate_empty(parameters: dict[str, Any]) -> dict[str, Any]:
        return _fields(parameters)

    @staticmethod
    def validate_select_mode(parameters: dict[str, Any]) -> dict[str, Any]:
        value = _fields(parameters, required={"mode"})["mode"]
        return {"mode": _text(value, "mode", choices={"extract", "phot2conc"})}

    @staticmethod
    def validate_filename(parameters: dict[str, Any]) -> dict[str, Any]:
        value = _fields(parameters, required={"filename"})["filename"]
        return {"filename": _text(value, "filename")}

    @staticmethod
    def validate_channel_only(parameters: dict[str, Any]) -> dict[str, Any]:
        return {"channel": _channel(_fields(parameters, required={"channel"})["channel"])}

    @staticmethod
    def validate_channel_enabled(parameters: dict[str, Any]) -> dict[str, Any]:
        values = _fields(parameters, required={"channel", "enabled"})
        return {"channel": _channel(values["channel"]), "enabled": _boolean(values["enabled"], "enabled")}

    @staticmethod
    def validate_library_decay(parameters: dict[str, Any]) -> dict[str, Any]:
        values = _fields(parameters, required={"channel", "name"})
        return {
            "channel": _channel(values["channel"]),
            "name": _text(values["name"], "name"),
        }

    @staticmethod
    def validate_filter_name(parameters: dict[str, Any]) -> dict[str, Any]:
        values = _fields(parameters, required={"channel", "name"})
        return {
            "channel": _channel(values["channel"]),
            "name": _text(values["name"], "name"),
        }

    @staticmethod
    def validate_gate(parameters: dict[str, Any]) -> dict[str, Any]:
        values = _fields(parameters, required={"channel", "lower_ns", "upper_ns"})
        lower = _number(values["lower_ns"], "lower_ns", minimum=0)
        upper = _number(values["upper_ns"], "upper_ns", minimum=0)
        if lower >= upper:
            _invalid("lower_ns must be less than upper_ns.")
        return {"channel": _channel(values["channel"]), "lower_ns": lower, "upper_ns": upper}

    @staticmethod
    def validate_rows_to_skip(parameters: dict[str, Any]) -> dict[str, Any]:
        values = _fields(parameters, required={"enabled"}, optional={"rows"})
        enabled = _boolean(values["enabled"], "enabled")
        rows = values.get("rows", 0)
        if isinstance(rows, bool) or not isinstance(rows, int) or rows < 0:
            _invalid("rows must be a non-negative integer.", field="rows")
        return {"enabled": enabled, "rows": rows}

    @staticmethod
    def validate_display(parameters: dict[str, Any]) -> dict[str, Any]:
        value = _fields(parameters, required={"display"})["display"]
        return {"display": _text(value, "display", choices={
            "Foreground intensity", "Background intensity", "Foreground decay times",
        })}

    @staticmethod
    def validate_decay_range(parameters: dict[str, Any]) -> dict[str, Any]:
        values = _fields(parameters, required={"channel", "minimum_ns", "maximum_ns"})
        lower = _number(values["minimum_ns"], "minimum_ns", minimum=0)
        upper = _number(values["maximum_ns"], "maximum_ns", minimum=0)
        if lower >= upper:
            _invalid("minimum_ns must be less than maximum_ns.")
        return {"channel": _channel(values["channel"]), "minimum_ns": lower, "maximum_ns": upper}

    @staticmethod
    def validate_calibration(parameters: dict[str, Any]) -> dict[str, Any]:
        required = {"channel", "omega", "omega_error", "kappa", "kappa_error", "brightness", "brightness_error"}
        values = _fields(parameters, required=required)
        result = {"channel": _channel(values["channel"])}
        for field in required - {"channel"}:
            result[field] = _number(values[field], field, minimum=0)
        if result["omega"] == 0 or result["kappa"] == 0 or result["brightness"] == 0:
            _invalid("omega, kappa, and brightness must be greater than zero.")
        return result

    @staticmethod
    def validate_calibration_path(parameters: dict[str, Any]) -> dict[str, Any]:
        value = _fields(parameters, required={"path"})["path"]
        return {"path": _existing_json_file(value)}

    @staticmethod
    def validate_error_mode(parameters: dict[str, Any]) -> dict[str, Any]:
        return {"sem": _boolean(_fields(parameters, required={"sem"})["sem"], "sem")}

    @staticmethod
    def validate_export_options(parameters: dict[str, Any]) -> dict[str, Any]:
        allowed = {"photons_array", "photons_heatmap", "molecules_array", "molecules_heatmap", "concentration_array", "concentration_heatmap"}
        values = _fields(parameters, optional=allowed)
        return {field: _boolean(value, field) for field, value in values.items()}

    @staticmethod
    def validate_roi_source(parameters: dict[str, Any]) -> dict[str, Any]:
        value = _fields(parameters, required={"source"})["source"]
        return {"source": _text(value, "source", choices={"none", "file", "auto"})}

    @staticmethod
    def validate_auto_roi(parameters: dict[str, Any]) -> dict[str, Any]:
        allowed = {"channel", "cell_threshold", "many_cells", "roi_mode", "object_threshold", "copy_from_other"}
        values = _fields(parameters, required={"channel"}, optional=allowed - {"channel"})
        result: dict[str, Any] = {"channel": _channel(values["channel"])}
        if "cell_threshold" in values:
            result["cell_threshold"] = _number(values["cell_threshold"], "cell_threshold", minimum=0)
        if "object_threshold" in values:
            result["object_threshold"] = _number(values["object_threshold"], "object_threshold", minimum=0)
        for field in ("many_cells", "copy_from_other"):
            if field in values:
                result[field] = _boolean(values[field], field)
        if "roi_mode" in values:
            result["roi_mode"] = _text(values["roi_mode"], "roi_mode")
        return result

    @staticmethod
    def validate_roi_name(parameters: dict[str, Any]) -> dict[str, Any]:
        return {"name": _text(_fields(parameters, required={"name"})["name"], "name")}

    @staticmethod
    def validate_export_path(parameters: dict[str, Any]) -> dict[str, Any]:
        return {"path": _output_file(_fields(parameters, required={"path"})["path"])}

    def select_mode(self, parameters: dict[str, Any]) -> dict[str, Any]:
        context = self._context()
        expected = _EXTRACT_MODE if parameters["mode"] == "extract" else _PHOT2CONC_MODE
        initial_window_exists = self.dpg.does_item_exist("initial_window")
        if initial_window_exists:
            sender = (
                "EXTRACT_FROM_PTU_INIT_BUTTON"
                if expected == _EXTRACT_MODE
                else "Phot_2_Conc_INIT_BUTTON"
            )
            context["basf"].callback_init_buttons(sender, None)
        elif context["inV"].mounted_method != expected:
            menu = context["PE_manu_F"] if expected == _EXTRACT_MODE else context["P2C_manu_F"]
            callback = menu.callback_PHOTEXTR_menu if expected == _EXTRACT_MODE else menu.callback_PHOT2CONC_menu
            callback()
        return {"mode": parameters["mode"], "mounted_method": context["inV"].mounted_method}

    def extract_load_directory(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        mode.callback_open_folder("PTU_dir_dialog", {"current_path": parameters["directory"]})
        return self.extract_get_state({})

    def _ensure_loaded_file(self, mode: Any, filename: str) -> None:
        items = list(getattr(mode, "files", []))
        if filename not in items:
            _invalid("filename is not present in the loaded directory.", field="filename")

    def extract_select_file(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        filename = parameters["filename"]
        self._ensure_loaded_file(mode, filename)
        self.dpg.set_value("file_box", filename)
        mode.callback_listbox("file_box", filename)
        return self.extract_get_state({})

    def extract_set_gate(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        channel = parameters["channel"]
        for boundary, value in (("bottom", parameters["lower_ns"]), ("upper", parameters["upper_ns"])):
            tag = f"{boundary}_limit_ch{channel}"
            self.dpg.set_value(tag, value)
            mode.callback_query(tag, value)
        return {"channel": int(channel), "lower_ns": self._value(f"bottom_limit_ch{channel}"), "upper_ns": self._value(f"upper_limit_ch{channel}")}

    def extract_set_rows_to_skip(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        self.dpg.set_value("skip_lines_drag", parameters["rows"])
        self.dpg.set_value("skip_lines_check", parameters["enabled"])
        mode.callback_skip_lines_check("skip_lines_check", parameters["enabled"])
        return dict(parameters)

    def extract_set_statistical_filter(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        tag = f"use_as_statistical_filters_chkbx_ch_{parameters['channel']}"
        self.dpg.set_value(tag, parameters["enabled"])
        mode.calllback_use_stat_filters_chbx(tag, parameters["enabled"])
        return dict(parameters)

    def extract_open_filter_setup(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        channel = parameters["channel"]
        mode.show_br_fltr_wndw(f"Remove_bgd_butt_ch_{channel}")
        return {"channel": int(channel), "setup_open": True}

    def extract_set_background_range(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        channel = parameters["channel"]
        self._require_filter_channel(mode, channel)
        enabled = parameters["enabled"]
        self.dpg.set_value("add_bg_range", enabled)
        mode.callback_Set_background_range("add_bg_range", enabled)
        return {"channel": int(channel), "enabled": enabled}

    def _library_decay_rows(self) -> list[tuple[str, str]]:
        rows = []
        for tag in self.dpg.get_aliases():
            if tag.startswith("decays_lib_tab_row_") and tag.endswith("_cell a_text"):
                checkbox = tag.removesuffix("_cell a_text") + "_cell e_chk"
                rows.append((str(self.dpg.get_value(tag)), checkbox))
        return rows

    def extract_open_decay_library(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        channel = parameters["channel"]
        self._require_filter_channel(mode, channel)
        mode.callback_import_from_library("Add_decay_from_lib", None)
        return {
            "channel": int(channel),
            "library_open": True,
            "available_decays": [name for name, _ in self._library_decay_rows()],
        }

    def extract_select_library_decay(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        channel = parameters["channel"]
        self._require_filter_channel(mode, channel)
        rows = self._library_decay_rows()
        matches = [(name, checkbox) for name, checkbox in rows if name == parameters["name"]]
        if not matches:
            _operation_error(
                "The requested decay is not available in the open channel library.",
                channel=int(channel),
                name=parameters["name"],
                available_decays=[name for name, _ in rows],
            )
        name, checkbox = matches[0]
        self.dpg.set_value(checkbox, True)
        mode.callback_check_lib_decay(checkbox, True)
        return {"channel": int(channel), "name": name, "selected": True}

    def extract_import_library_decays(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        channel = parameters["channel"]
        self._require_filter_channel(mode, channel)
        selected = [
            name for name, checkbox in self._library_decay_rows()
            if self.dpg.get_value(checkbox)
        ]
        if not selected:
            _operation_error(
                "Select at least one decay before importing from the library.",
                channel=int(channel),
            )
        mode.callback_Proceed_library_import("Proceed_library_import", None)
        return {"channel": int(channel), "imported_decays": selected}

    @staticmethod
    def _require_filter_channel(mode: Any, channel: str) -> None:
        if getattr(mode, "bg_channel_marker", None) != int(channel):
            _operation_error(
                "Open the statistical-filter setup for this channel first.",
                channel=int(channel),
            )

    def extract_calculate_filters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        channel = parameters["channel"]
        self._require_filter_channel(mode, channel)
        selected_decays = []
        prefix = "decays_tab_row_"
        for tag in self.dpg.get_aliases():
            if not tag.startswith(prefix) or not tag.endswith("_cell b_chk"):
                continue
            if tag == "decays_tab_row_0_cell b_chk" or not self.dpg.get_value(tag):
                continue
            name_tag = tag.removesuffix("_cell b_chk") + "_cell a_text"
            selected_decays.append(str(self.dpg.get_value(name_tag)))
        routine = getattr(mode, "filtering_routine", {}).get(f"Channel {channel}", {})
        if not selected_decays and not routine.get("BG", False):
            _operation_error(
                "No decay component is selected for filter calculation.",
                channel=int(channel),
                available_decays=[
                    str(self.dpg.get_value(tag))
                    for tag in self.dpg.get_aliases()
                    if tag.startswith(prefix) and tag.endswith("_cell a_text")
                ],
            )
        mode.callback_Calculate_filters("Calculate_filters", None)
        return {"channel": int(channel), "calculated": True}

    def extract_accept_filters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        self._require_filter_channel(mode, parameters["channel"])
        mode.callback_Accept_filters("Accept_filters", None, None)
        return {"channel": int(parameters["channel"]), "accepted": True}

    def _filter_rows(self, channel: str) -> list[tuple[str, str]]:
        prefix = f"filters_ch_{channel}_tab_list_row_"
        rows = []
        for tag in self.dpg.get_aliases():
            if tag.startswith(prefix) and tag.endswith("_cell a_text"):
                checkbox = tag.removesuffix("_cell a_text") + "_cell b_chk"
                rows.append((str(self.dpg.get_value(tag)), checkbox))
        return rows

    def extract_select_filter(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        channel = parameters["channel"]
        rows = self._filter_rows(channel)
        matches = [(name, checkbox) for name, checkbox in rows if name == parameters["name"]]
        if not matches:
            _operation_error(
                "The requested filter is not available in the accepted filter table.",
                channel=int(channel),
                name=parameters["name"],
                available_filters=[name for name, _ in rows],
            )
        name, checkbox = matches[0]
        self.dpg.set_value(checkbox, True)
        mode.callback_select_filter_for_batch(checkbox, True)
        return {"channel": int(channel), "name": name, "selected": True}

    def extract_decline_filters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        self._require_filter_channel(mode, parameters["channel"])
        mode.callback_Decline_filters("Decline_filters", None, None)
        return {"channel": int(parameters["channel"]), "declined": True}

    def extract_apply_current(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        mode.callback_apply_to_single_ptus(
            "apply_to_file",
            None,
            self.dpg.get_item_user_data("apply_to_file"),
            refresh_progress=True,
        )
        return {"filename": os.path.basename(mode.anal_file), "completed": True}

    def extract_apply_all(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        for channel in ("1", "2"):
            filter_checkbox = f"use_as_statistical_filters_chkbx_ch_{channel}"
            is_item_shown = getattr(self.dpg, "is_item_shown", None)
            # The native GUI ignores a filter checkbox when its detector
            # channel is absent and the control is hidden. Mirror that behavior
            # instead of rejecting Apply all because of stale invisible state.
            if is_item_shown is not None and not is_item_shown(filter_checkbox):
                continue
            if not self.dpg.get_value(filter_checkbox):
                continue
            rows = self._filter_rows(channel)
            selected = [name for name, checkbox in rows if self.dpg.get_value(checkbox)]
            if not selected:
                _operation_error(
                    "Select a foreground filter before applying extraction to all PTU files.",
                    channel=int(channel),
                    available_filters=[name for name, _ in rows],
                )
        files = list(mode.files)
        mode.callback_apply_to_all_ptus(
            "apply_to_all", None, None, refresh_progress=True
        )
        return {
            "files": files,
            "count": len(files),
            "completed": True,
            "file_timings": list(getattr(mode, "last_batch_file_timings", [])),
        }

    def extract_get_state(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_EXTRACT_MODE)
        return {
            "directory": getattr(mode, "last_directory", None),
            "filename": os.path.basename(getattr(mode, "anal_file", "")),
            "files": list(getattr(mode, "files", [])),
            "mode": getattr(mode, "MODE", None),
            "gates_ns": {
                "1": [self._value("bottom_limit_ch1"), self._value("upper_limit_ch1")],
                "2": [self._value("bottom_limit_ch2"), self._value("upper_limit_ch2")],
            },
            "rows_to_skip": {"enabled": self._value("skip_lines_check"), "rows": self._value("skip_lines_drag")},
            "statistical_filter": {
                "1": self._value("use_as_statistical_filters_chkbx_ch_1"),
                "2": self._value("use_as_statistical_filters_chkbx_ch_2"),
            },
        }

    def phot_load_directory(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        directory = parameters["directory"]
        mode.callback_PTU_directory_select("PTU_file_dialog_id", {
            "file_path_name": directory, "current_path": directory,
        })
        return self.phot_get_state({})

    def phot_load_roi_directory(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        directory = parameters["directory"]
        mode.callback_ROI_directory_select("ROI_folder_dialog_id", {
            "file_path_name": directory, "current_path": directory,
        })
        return self.phot_get_state({})

    def phot_select_file(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        filename = parameters["filename"].removesuffix(".ptu")
        available = [str(item).removesuffix(".ptu") for item in getattr(mode, "files", [])]
        if filename not in available:
            _invalid("filename is not present in the loaded directory.", field="filename")
        self.dpg.set_value("file_box", filename)
        mode.callback_listbox("file_box", filename)
        return self.phot_get_state({})

    def phot_set_display(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        value = parameters["display"]
        self.dpg.set_value("DISP_OPT_combo", value)
        mode.callback_DISP_OPT_combo("DISP_OPT_combo", value)
        return {"display": getattr(mode, "display_option", value)}

    def phot_set_decay_range(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        channel = parameters["channel"]
        current_upper = self.dpg.get_value(f"decay_range_max_ch_{channel}")
        if current_upper is not None and parameters["minimum_ns"] >= float(current_upper):
            boundaries = (("max", "maximum_ns"), ("min", "minimum_ns"))
        else:
            boundaries = (("min", "minimum_ns"), ("max", "maximum_ns"))
        for boundary, key in boundaries:
            tag = f"decay_range_{boundary}_ch_{channel}"
            self.dpg.set_value(tag, parameters[key])
            mode.callback_decay_time_range(tag, parameters[key], channel)
        return {"channel": int(channel), "minimum_ns": self._value(f"decay_range_min_ch_{channel}"), "maximum_ns": self._value(f"decay_range_max_ch_{channel}")}

    def phot_set_calibration(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        channel = parameters["channel"]
        callbacks = {
            "omega": mode.callback_omega_input,
            "omega_error": mode.callback_omega_err_input,
            "kappa": mode.callback_kappa_input,
            "kappa_error": mode.callback_kappa_err_input,
            "brightness": mode.callback_Brightness_input,
            "brightness_error": mode.callback_Brightness_err_input,
        }
        tag_names = {
            "omega": "omega_input", "omega_error": "omega_err_input",
            "kappa": "kappa_input", "kappa_error": "kappa_err_input",
            "brightness": "Brightness_input", "brightness_error": "Brightness_err_input",
        }
        for field in ("omega", "omega_error", "kappa", "kappa_error", "brightness", "brightness_error"):
            tag = f"{tag_names[field]}_ch_{channel}"
            self.dpg.set_value(tag, parameters[field])
            callbacks[field](tag, parameters[field])
        return self._calibration_state(channel)

    def phot_load_calibration(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        path = parameters["path"]
        mode.Load_Save_Calib_file(
            "Calib_file_dialog_id",
            {
                "current_path": os.path.dirname(path),
                "file_path_name": path,
            },
            "Load_calib_button",
        )
        return {
            "path": path,
            "calibration": {
                channel: self._calibration_state(channel)
                for channel in ("1", "2")
            },
        }

    def _calibration_state(self, channel: str) -> dict[str, Any]:
        return {
            "channel": int(channel),
            "omega": self._value(f"omega_input_ch_{channel}"),
            "omega_error": self._value(f"omega_err_input_ch_{channel}"),
            "kappa": self._value(f"kappa_input_ch_{channel}"),
            "kappa_error": self._value(f"kappa_err_input_ch_{channel}"),
            "focal_volume": self._value(f"focal_vol_input_ch_{channel}"),
            "focal_volume_error": self._value(f"focal_vol_err_input_ch_{channel}"),
            "brightness": self._value(f"Brightness_input_ch_{channel}"),
            "brightness_error": self._value(f"Brightness_err_input_ch_{channel}"),
        }

    def phot_set_error_mode(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        self.dpg.set_value("Error_type_checkbox", parameters["sem"])
        mode.callback_calculate("Error_type_checkbox", parameters["sem"])
        return dict(parameters)

    def phot_set_export_options(self, parameters: dict[str, Any]) -> dict[str, Any]:
        self._mode(_PHOT2CONC_MODE)
        tags = {
            "photons_array": "Photons_array_checkbox", "photons_heatmap": "Photons_Hmaps_checkbox",
            "molecules_array": "Np_array_checkbox", "molecules_heatmap": "Np_Hmaps_checkbox",
            "concentration_array": "C_array_checkbox", "concentration_heatmap": "C_Hmaps_checkbox",
        }
        for field, value in parameters.items():
            self.dpg.set_value(tags[field], value)
        return {field: self._value(tag) for field, tag in tags.items()}

    def phot_set_roi_source(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        source = parameters["source"]
        if source == "file":
            self.dpg.set_value("FILE_ROI_checkbox", True)
            mode.callback_select_roi("FILE_ROI_checkbox", True)
        elif source == "auto":
            self.dpg.set_value("Auto_ROI_checkbox", True)
            mode.callback_select_autoroi("Auto_ROI_checkbox", True)
        elif self.dpg.get_value("FILE_ROI_checkbox"):
            self.dpg.set_value("FILE_ROI_checkbox", False)
            mode.callback_select_roi("FILE_ROI_checkbox", False)
        elif self.dpg.get_value("Auto_ROI_checkbox"):
            self.dpg.set_value("Auto_ROI_checkbox", False)
            mode.callback_select_autoroi("Auto_ROI_checkbox", False)
        return {"source": source}

    def phot_set_auto_roi(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        channel = parameters["channel"]
        actions = (
            ("cell_threshold", f"cell_thres_ratio_{channel}", mode._update_textures_both_roi, None),
            ("many_cells", f"multiple_cells_checkbox_{channel}", mode._update_textures_both_roi, None),
            ("roi_mode", f"ROI_mode_{channel}", mode._roi_mode, None),
            ("object_threshold", f"nucl_thres_ratio_{channel}", mode._roi_mode, None),
            ("copy_from_other", f"cp_roi_{channel}", mode.copy_roi_from_channel, None),
        )
        for field, tag, callback, user_data in actions:
            if field not in parameters:
                continue
            value = parameters[field]
            self.dpg.set_value(tag, value)
            if field == "copy_from_other":
                callback(tag)
            elif callback == mode._roi_mode:
                callback(tag, value, user_data)
            else:
                callback(tag, value)
        return self._auto_roi_state(channel)

    def _auto_roi_state(self, channel: str) -> dict[str, Any]:
        return {
            "channel": int(channel),
            "cell_threshold": self._value(f"cell_thres_ratio_{channel}"),
            "many_cells": self._value(f"multiple_cells_checkbox_{channel}"),
            "roi_mode": self._value(f"ROI_mode_{channel}"),
            "object_threshold": self._value(f"nucl_thres_ratio_{channel}"),
            "copy_from_other": self._value(f"cp_roi_{channel}"),
        }

    def phot_select_roi(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        name = parameters["name"]
        self.dpg.set_value("ROI_names_combo_tag", name)
        mode.callback_ROI_names_combo("ROI_names_combo_tag", name)
        return {"name": name}

    def phot_calculate(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        mode.callback_calculate("Calculate_button", None)
        return self._calculation_results(mode)

    def phot_add_result(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        mode.add_single_result_to_DF("add_to_res_single_button", None)
        return {"rows": len(mode.Sing_Results_DF), "results": self._results_records(mode)}

    def phot_calculate_all(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        mode.callback_calculate_all(
            "Calculate_all_button", None, None, refresh_progress=True
        )
        return {
            "rows": len(mode.Sing_Results_DF),
            "results": self._results_records(mode),
            "file_timings": list(getattr(mode, "last_batch_file_timings", [])),
        }

    def phot_export_results(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        path = parameters["path"]
        suffix = os.path.splitext(path)[1].lower()
        mode.Export_result_dataframe_to_file("file_dialog_export", {
            "current_path": os.path.dirname(path),
            "current_filter": suffix,
            "file_name": os.path.basename(path),
            "file_path_name": path,
        })
        return {"path": path, "exists": os.path.isfile(path), "rows": len(mode.Sing_Results_DF)}

    def _results_records(self, mode: Any) -> list[dict[str, Any]]:
        dataframe = getattr(mode, "Sing_Results_DF", None)
        if dataframe is None:
            return []
        return _json_value(dataframe.to_dict(orient="records"))

    def _calculation_results(self, mode: Any) -> dict[str, Any]:
        output = {"filename": getattr(mode, "anal_file", None), "display": getattr(mode, "display_option", None), "channels": {}}
        for channel in ("1", "2"):
            output["channels"][channel] = {
                "photons_per_pixel": self._value(f"sinle_phot_output_ch_{channel}"),
                "photons_error": self._value(f"sinle_phot_err_output_ch_{channel}"),
                "molecules_per_pixel": self._value(f"sinle_mols_output_ch_{channel}"),
                "molecules_error": self._value(f"sinle_mols_err_output_ch_{channel}"),
                "concentration_nm": self._value(f"single_conc_output_ch_{channel}"),
                "concentration_error": self._value(f"single_conc_err_output_ch_{channel}"),
            }
        return output

    def phot_get_state(self, parameters: dict[str, Any]) -> dict[str, Any]:
        mode = self._mode(_PHOT2CONC_MODE)
        return {
            "directory": getattr(mode, "PTU_directory", None),
            "roi_directory": getattr(mode, "ROI_directory", None),
            "filename": getattr(mode, "anal_file", None),
            "files": list(getattr(mode, "files", [])),
            "display": getattr(mode, "display_option", None),
            "roi_source": {
                "file": self._value("FILE_ROI_checkbox"),
                "auto": self._value("Auto_ROI_checkbox"),
            },
            "calibration": {channel: self._calibration_state(channel) for channel in ("1", "2")},
            "calculation": self._calculation_results(mode),
            "results": self._results_records(mode),
        }


def register_gui_commands(registry: Any, dpg: Any, context_provider: Callable[[], dict[str, Any]]) -> SmicaGuiCommands:
    """Register all callback-backed smICA commands and retain their adapter."""

    return SmicaGuiCommands(registry, dpg, context_provider)
