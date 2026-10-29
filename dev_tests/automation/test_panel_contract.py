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

import ast
import os
from types import SimpleNamespace

import dearpygui.dearpygui as dpg

from smICA.Required.automation_panel import AutomationServerPanel


def test_every_created_dpg_item_has_an_explicit_registered_tag() -> None:
    repository_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    source_path = os.path.join(repository_root, "src", "smICA", "Required", "automation_panel.py")
    with open(source_path, encoding="utf-8") as source_stream:
        tree = ast.parse(source_stream.read())
    created_tags = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if not (
            node.func.attr.startswith("add_")
            or node.func.attr in {"window", "group"}
        ):
            continue
        tag_keywords = [keyword for keyword in node.keywords if keyword.arg == "tag"]
        assert len(tag_keywords) == 1, f"Missing explicit tag in {node.func.attr}"
        tag_value = tag_keywords[0].value
        assert isinstance(tag_value, ast.Constant) and isinstance(tag_value.value, str)
        created_tags.append(tag_value.value)
    assert sorted(created_tags) == sorted(AutomationServerPanel.TAGS)


def test_panel_registers_all_tags_in_global_items() -> None:
    repository_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    source_path = os.path.join(repository_root, "src", "smICA", "Required", "automation_panel.py")
    with open(source_path, encoding="utf-8") as source_stream:
        source = source_stream.read()
    assert "self.global_items.items.extend(self.TAGS)" in source


def test_panel_mounts_with_real_dearpygui_context() -> None:
    class Service:
        def __init__(self):
            self.running = False
            self.port = None

        def status(self):
            return {
                "running": self.running,
                "host": "127.0.0.1",
                "port": self.port,
            }

        def start(self, *, port):
            self.running = True
            self.port = 49152 if port == 0 else port
            return self.port

        def stop(self):
            self.running = False
            self.port = None

    dpg.create_context()
    try:
        with dpg.viewport_menu_bar(tag="test_menu_bar"):
            with dpg.menu(label="About", tag="menu_about_dropout"):
                dpg.add_menu_item(
                    label="Version",
                    tag="menu_Version_dropout_item",
                )
        global_items = SimpleNamespace(items=[])
        service = Service()
        panel = AutomationServerPanel(service, global_items, default_port=8765)
        assert global_items.items == AutomationServerPanel.TAGS
        assert all(dpg.does_item_exist(tag) for tag in AutomationServerPanel.TAGS)
        dpg.set_value("automation_server_port_input", 0)
        panel.start()
        assert service.running
        assert dpg.get_value("automation_server_status_text") == "Running"
        assert dpg.get_value("automation_server_address_text").endswith(":49152")
        panel.stop()
        assert not service.running
        assert dpg.get_value("automation_server_status_text") == "Stopped"
    finally:
        dpg.destroy_context()
