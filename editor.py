import os
import sys
from typing import Optional
import yaml
import dearpygui.dearpygui as dpg
import editor.utils as utils
from editor.line import line

def main(filename:Optional[str]):
    lineObj = line(filename)
    with dpg.window(label="Example",tag="Primary window"):
        with dpg.menu_bar():
            with dpg.menu(label="Menu"):
                with dpg.file_dialog(label="Open file", width=600, height=400, show=False, callback=
                                     lambda s,a: lineObj.load(a), tag="fd_open"):
                    dpg.add_file_extension(".yaml", color=(0, 255, 255, 255))

                dpg.add_menu_item(label="Open",callback=lambda: dpg.show_item("fd_open"))
                dpg.add_menu_item(label="Save",callback=lambda: lineObj.save())
                dpg.add_menu_item(label="Save As",callback=lambda: lineObj.saveAs())
        with dpg.group(horizontal=True):
            dpg.add_collapsing_header(label="Production line",tag="lineRoot",default_open=True,user_data=lineObj)
        utils.createTable("lineRoot")
    lineObj.init_widgets()

def debugBegin():
    # I have no idea what the correct order of dpg commands is anymore
    dpg.configure_app(manual_callback_management=True)
    dpg.create_viewport()
    dpg.setup_dearpygui()
def debug():
    while dpg.is_dearpygui_running():
        jobs = dpg.get_callback_queue()
        if jobs:
            dpg.run_callbacks(jobs)
        dpg.render_dearpygui_frame()
    pass

if __name__ == '__main__':
    yaml.emitter.Emitter.prepare_tag = lambda self, tag: ''
    dpg.create_context()

    if os.getenv("DEBUG"):
        debugBegin()
    else:
        dpg.create_viewport()
        dpg.setup_dearpygui()
    try:
        fname = sys.argv[1]
    except IndexError:
        fname = None
    main(fname)
    dpg.show_viewport()
    dpg.set_primary_window("Primary window",True)
    if os.getenv("DEBUG"):
        debug()
    else:
        dpg.start_dearpygui()
    dpg.destroy_context()
