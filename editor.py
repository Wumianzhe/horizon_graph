import yaml
import converter.utils
import converter.line
import dearpygui.dearpygui as dpg
from editor.loadFile import loadfromfile

dpg.create_context()

def saveCallback():
    print("Saved")

def openCallback(sender,app_data):
    print("Sender: ",sender)
    print("Appdata: ",app_data["file_path_name"])

with dpg.theme() as borderless_child_theme:
    with dpg.theme_component(dpg.mvChildWindow):
        dpg.add_theme_color(dpg.mvThemeCol_Border, [0, 0, 0, 0])

dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Example",tag="Primary window"):
    with dpg.menu_bar():
        with dpg.menu(label="Menu"):
            with dpg.file_dialog(label="Open file", width=300, height=400, show=False, callback=loadfromfile, tag="fd_open"):
                dpg.add_file_extension(".yaml", color=(255, 255, 255, 255))

            dpg.add_menu_item(label="Open",callback=lambda: dpg.show_item("fd_open"))
            dpg.add_menu_item(label="Save",callback=saveCallback)
    with dpg.group(horizontal=True):
        with dpg.child_window(width=200) as treeWindow:
            dpg.bind_item_theme(treeWindow,borderless_child_theme)
            with dpg.collapsing_header(label="Production line",tag="lineRoot"):
                with dpg.tree_node(label="Fakeroot"):
                    pass
        with dpg.group():
            dpg.add_text("Hello world")
            dpg.add_input_text(label="string")
            dpg.add_slider_float(label="float")

dpg.show_viewport()
dpg.set_primary_window("Primary window",True)
dpg.start_dearpygui()
dpg.destroy_context()
