from converter.recipe import base
from converter.line import line as prodLine
from converter.cluster import cluster as prodCluster
from converter.utils import tuplify
import dearpygui.dearpygui as dpg
import yaml

def loadfromfile(filename) -> prodLine:
    with open(filename) as file:
        obj = yaml.safe_load(file)
        line = prodLine(obj)
        gen_widgets(line)
        return line

def gen_widgets(line:prodLine):
    dpg.delete_item("lineRoot",children_only=True) # clear children
    for c in line.clusters:
        if c.clusters:
            dpg.add_collapsing_header(parent="lineRoot",label=c.name)
        else:
            dpg.add_tree_node(parent="lineRoot",label=c.name)
    pass
