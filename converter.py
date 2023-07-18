#!/usr/bin/env python3
import sys
import json
import subprocess
import converter.utils
import converter.line

def convert(obj,out = sys.stdout):
    print(converter.line.line(obj),file=out)

def main():
    name = sys.argv[1]
    with open(name + ".json") as file:
        obj = json.load(file)
        with open(name + ".dot",'w') as out:
            immObj = converter.utils.tuplify(obj)
            convert(immObj,out)

    subprocess.run(["dot",name + ".dot","-Tpdf","-o",name+".pdf"])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Missing argument")
    else:
        main()
