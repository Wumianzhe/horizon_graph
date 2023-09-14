import yaml
import converter.utils
import converter.line
import dearpygui.dearpygui as dpg

def saveCallback():
    print("Saved")

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Example",tag="Primary window"):
    dpg.add_text("Hello world")
    dpg.add_button(label="Save",callback=saveCallback)
    dpg.add_input_text(label="string")
    dpg.add_slider_float(label="float")

dpg.show_viewport()
dpg.set_primary_window("Primary window",True)
dpg.start_dearpygui()
dpg.destroy_context()
