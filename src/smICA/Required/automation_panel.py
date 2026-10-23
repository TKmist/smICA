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


"""Dear PyGui controls for the optional smICA automation server."""

from __future__ import annotations

import dearpygui.dearpygui as dpg


class AutomationServerPanel:
    """Mount persistent server controls under the About menu."""

    TAGS = [
        "automation_server_menu_item",
        "automation_server_window",
        "automation_server_title",
        "automation_server_status_text",
        "automation_server_address_text",
        "automation_server_port_input",
        "automation_server_buttons_group",
        "automation_server_start_button",
        "automation_server_stop_button",
        "automation_server_close_button",
    ]

    def __init__(self, service, global_items, *, default_port: int) -> None:
        self.service = service
        self.global_items = global_items
        self.default_port = default_port
        self._mount()
        self.global_items.items.extend(self.TAGS)
        self.refresh()

    def _mount(self) -> None:
        dpg.add_menu_item(
            label="Automation server",
            tag="automation_server_menu_item",
            parent="menu_about_dropout",
            before="menu_Version_dropout_item",
            callback=self.show,
        )
        with dpg.window(
            label="Automation server",
            tag="automation_server_window",
            width=430,
            height=210,
            show=False,
            no_collapse=True,
            on_close=self.hide,
        ):
            dpg.add_text("Local automation server", tag="automation_server_title")
            dpg.add_text("Stopped", tag="automation_server_status_text")
            dpg.add_text("Address: 127.0.0.1", tag="automation_server_address_text")
            dpg.add_input_int(
                label="Port",
                tag="automation_server_port_input",
                default_value=self.default_port,
                min_value=0,
                max_value=65535,
                min_clamped=True,
                max_clamped=True,
            )
            with dpg.group(tag="automation_server_buttons_group", horizontal=True):
                dpg.add_button(
                    label="Start",
                    tag="automation_server_start_button",
                    callback=self.start,
                )
                dpg.add_button(
                    label="Stop",
                    tag="automation_server_stop_button",
                    callback=self.stop,
                )
                dpg.add_button(
                    label="Close",
                    tag="automation_server_close_button",
                    callback=self.hide,
                )

    def show(self, sender=None, app_data=None) -> None:
        dpg.show_item("automation_server_window")
        self.refresh()

    def hide(self, sender=None, app_data=None) -> None:
        dpg.hide_item("automation_server_window")

    def start(self, sender=None, app_data=None) -> None:
        try:
            port = int(dpg.get_value("automation_server_port_input"))
            self.service.start(port=port)
        except (OSError, ValueError) as exc:
            dpg.set_value(
                "automation_server_status_text",
                f"Start failed: {exc}",
            )
        else:
            self.refresh()

    def stop(self, sender=None, app_data=None) -> None:
        self.service.stop()
        self.refresh()

    def refresh(self) -> None:
        status = self.service.status()
        running = status["running"]
        dpg.set_value(
            "automation_server_status_text",
            "Running" if running else "Stopped",
        )
        address = f"Address: {status['host']}"
        if status["port"] is not None:
            address += f":{status['port']}"
        dpg.set_value("automation_server_address_text", address)
        dpg.configure_item("automation_server_port_input", enabled=not running)
        dpg.configure_item("automation_server_start_button", enabled=not running)
        dpg.configure_item("automation_server_stop_button", enabled=running)
