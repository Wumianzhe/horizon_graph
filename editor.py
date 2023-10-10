from typing import Optional
import yaml
from converter.line import line  as prodLine
from converter.cluster import cluster
from itertools import zip_longest
import dearpygui.dearpygui as dpg
import editor.utils as utils
from editor.fileIO import loadfromfile,saveAsCallback,saveCallback

dpg.create_context()
curr_line = prodLine({})
fname:str = ""

yaml.emitter.Emitter.prepare_tag = lambda self, tag: ''

def loadWrap(sender,a):
    global fname; fname = a["file_path_name"]
    global curr_line; curr_line = loadfromfile(fname)
    init_widgets(curr_line)

def init_widgets(line:prodLine):
    dpg.delete_item("lineRoot",children_only=True) # clear children
    utils.createTable("lineRoot")
    utils.populateTable(line,"lineRoot")


with dpg.theme() as borderless_child_theme:
    with dpg.theme_component(dpg.mvChildWindow):
        dpg.add_theme_color(dpg.mvThemeCol_Border, [0, 0, 0, 0])

dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Example",tag="Primary window"):
    with dpg.menu_bar():
        with dpg.menu(label="Menu"):
            with dpg.file_dialog(label="Open file", width=600, height=400, show=False, callback=loadWrap, tag="fd_open"):
                dpg.add_file_extension(".yaml", color=(0, 255, 255, 255))

            dpg.add_menu_item(label="Open",callback=lambda: dpg.show_item("fd_open"))
            dpg.add_menu_item(label="Save",callback=lambda: saveCallback(fname,curr_line))
            dpg.add_menu_item(label="Save As",callback=saveAsCallback)
    with dpg.group(horizontal=True):
        dpg.add_collapsing_header(label="Production line",tag="lineRoot",default_open=True)
    utils.createTable("lineRoot")

dpg.show_viewport()
dpg.set_primary_window("Primary window",True)
dpg.start_dearpygui()
dpg.destroy_context()
