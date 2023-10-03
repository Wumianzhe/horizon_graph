from typing import Optional
import yaml
import converter.utils
import converter.line
import dearpygui.dearpygui as dpg
from editor.loadFile import loadfromfile

dpg.create_context()
curr_line:Optional[converter.line.line] = None
fname:str = ""

def loadWrap(s,a):
    global fname; fname = a["file_path_name"]
    global curr_line; curr_line = loadfromfile(fname)

def saveCallback():
    if fname:
        with open(fname,"w") as file:
            yaml.dump(curr_line,file)
    else:
        saveAsCallback()

def saveAsCallback():
    print("Not done yet")


with dpg.theme() as borderless_child_theme:
    with dpg.theme_component(dpg.mvChildWindow):
        dpg.add_theme_color(dpg.mvThemeCol_Border, [0, 0, 0, 0])

dpg.create_viewport()
dpg.setup_dearpygui()


with dpg.window(label="Example",tag="Primary window"):
    with dpg.menu_bar():
        with dpg.menu(label="Menu"):
            with dpg.file_dialog(label="Open file", width=300, height=400, show=False, callback=loadWrap, tag="fd_open"):
                dpg.add_file_extension(".yaml", color=(255, 255, 255, 255))

            dpg.add_menu_item(label="Open",callback=lambda: dpg.show_item("fd_open"))
            dpg.add_menu_item(label="Save",callback=saveCallback)
            dpg.add_menu_item(label="Save As",callback=saveAsCallback)
    with dpg.group(horizontal=True):
        with dpg.child_window(width=200) as treeWindow:
            dpg.bind_item_theme(treeWindow,borderless_child_theme)
            dpg.add_collapsing_header(label="Production line",tag="lineRoot")
        with dpg.group():
            with dpg.table(header_row=True,tag="IOTable"):
                dpg.add_table_column(label="Inputs")
                dpg.add_table_column(label="Outputs")
            dpg.add_collapsing_header(label="Subfactories",tag="subclusters")
            with dpg.table(header_row=True,tag="RecipeTable"):
                dpg.add_table_column(label="Machine")
                dpg.add_table_column(label="Tier",width_fixed=True)
                dpg.add_table_column(label="Recipe tier",width_fixed=True)
                dpg.add_table_column(label="Duration")
                dpg.add_table_column(label="Inputs")
                dpg.add_table_column(label="Outputs")
                dpg.add_table_column(label="Count")

dpg.show_viewport()
dpg.set_primary_window("Primary window",True)
dpg.start_dearpygui()
dpg.destroy_context()
