from typing import Optional
import yaml
import converter.utils
from converter.line import line  as prodLine
from converter.cluster import cluster
from itertools import zip_longest
import dearpygui.dearpygui as dpg
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
    create_table("lineRoot")
    populate_table(line,"lineRoot")

def create_table(item: int|str):
    with dpg.table(header_row=True,parent=item,user_data=0) as ioTable:
        dpg.add_table_column(label="Inputs")
        dpg.add_table_column(label="Outputs")
    dpg.add_button(parent=item,label="Add input",callback=lambda: print(dpg.get_item_user_data(ioTable)))
    dpg.add_button(parent=item,label="Add output",callback=lambda: print(dpg.get_item_user_data(ioTable)))
    with dpg.table(header_row=True,parent=item):
        dpg.add_table_column(label="Machine")
        dpg.add_table_column(label="Tier",width_fixed=True)
        dpg.add_table_column(label="Recipe tier",width_fixed=True)
        dpg.add_table_column(label="Duration")
        dpg.add_table_column(label="Inputs")
        dpg.add_table_column(label="Outputs")
        dpg.add_table_column(label="Count")
    with dpg.tree_node(parent=item,label="Subfactories",indent=5):
        pass

def populate_table(cl:cluster,item: int|str):
    items = dpg.get_item_children(item)
    assert(isinstance(items, dict))
    items = items[1]
    ioTable = items[0]

    diff = len(cl.buffers["input"]) - len(cl.buffers["output"])
    dpg.set_item_user_data(ioTable,diff)
    for (i,o) in zip_longest(cl.buffers["input"],cl.buffers["output"]):
        with dpg.table_row(parent=ioTable):
            if i:
                dpg.add_text(i)
            if o:
                dpg.add_text(o)

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
    create_table("lineRoot")

dpg.show_viewport()
dpg.set_primary_window("Primary window",True)
dpg.start_dearpygui()
dpg.destroy_context()
