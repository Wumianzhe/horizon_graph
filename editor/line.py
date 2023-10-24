import yaml
from editor.fileIO import loadfromfile
from converter.line import line  as prodLine
from typing import Optional
import dearpygui.dearpygui as dpg
import editor.utils as utils

class line:
    def __init__(self,fname:Optional[str]):
        self.fname = fname
        if fname:
            with open(fname) as file:
                obj = yaml.safe_load(file)
        else:
            obj = {}
        self.line = prodLine(obj)
    def load(self,a):
        self.fname = a["file_path_name"]
        self.line = loadfromfile(self.fname)
        self.init_widgets()
    def save(self):
        if self.fname:
            with open(self.fname,"w") as file:
                yaml.dump(line,file)
        else:
            self.saveAs()
    def saveAs(self):
        print("Not done yet")
    def init_widgets(self):
        dpg.delete_item("lineRoot",children_only=True) # clear children
        utils.createTable("lineRoot")
        utils.populateTable(self.line,"lineRoot")
