from converter.recipe import base
from converter.line import line as prodLine
from converter.cluster import cluster as prodCluster
from converter.utils import tuplify
import dearpygui.dearpygui as dpg
import yaml

def loadfromfile(_,app_data):
    name = app_data["file_path_name"]
    with open(name) as file:
        obj = yaml.safe_load(file)
        immobj = tuplify(obj)
        assert(isinstance(immobj,dict))
        line = prodLine(immobj)
        gen_widgets(line)

def gen_widgets(line:prodLine):
    dpg.delete_item("lineRoot",children_only=True) # clear children
    for c in line.subclusters:
        print(c.name)
        if c.subclusters:
            dpg.add_collapsing_header(parent="lineRoot",label=c.name)
        else:
            dpg.add_tree_node(parent="lineRoot",label=c.name)
    pass
