from converter.line import line as prodLine
import yaml

def loadfromfile(filename) -> prodLine:
    with open(filename) as file:
        obj = yaml.safe_load(file)
        line = prodLine(obj)
        return line
