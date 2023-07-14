#!/usr/bin/env python3
import sys
import json
import subprocess
import converter.utils
import converter.line

def convert(obj):
    print(converter.line.line(obj))

def main():
    name = sys.argv[1]
    old_stdout = sys.stdout
    with open(name + ".json") as file:
        obj = json.load(file)
        with open(name + ".dot",'w') as out:
            sys.stdout = out
            immObj = converter.utils.tuplify(obj)
            convert(immObj)
            sys.stdout.flush()
            sys.stdout = old_stdout

    subprocess.run(["dot",name + ".dot","-Tpdf","-o",name+".pdf"])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Missing argument")
    else:
        main()
