#!/usr/bin/env python3
import sys
import json
import subprocess
import utils
import cluster

def convert(obj):
    print(cluster.cluster(obj["clusters"][0],{}))

def main():
    name = '../test'
    old_stdout = sys.stdout
    with open(name + ".json") as file:
        obj = json.load(file)
        # with open(name + ".dot",'w') as out:
        #     sys.stdout = out
        immObj = utils.tuplify(obj)
        convert(immObj)
            # sys.stdout.flush()
            # sys.stdout = old_stdout

    # subprocess.run(["dot",name + ".dot","-Tpdf","-o",name+".pdf"])

if __name__ == '__main__':
    main()
