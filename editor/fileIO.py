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
        return line

def saveCallback(fname,line):
    if fname:
        with open(fname,"w") as file:
            yaml.dump(line,file)
    else:
        saveAsCallback()

def saveAsCallback():
    print("Not done yet")
