#!/usr/bin/env python3
import json
import hashlib
import sys
import subprocess

fluidColor = "darkorchid"
solidColor = "firebrick"
inputColor = "blue"
outputColor = "orange"
globalOutputColor = "gold"
globalInputColor = "teal"

def objhash(o):
    return hashlib.md5(json.dumps(o).encode('utf8')).hexdigest()

def procNode(p):
    print("p_{} [label = <".format(objhash(p)))
    print("<TABLE>")
    print("<TR><TD>{}</TD><TD>{}</TD></TR>".format(p["machine"],p["tier"]))
    print("<TR><TD>{}</TD><TD>{} sec</TD></TR>".format("Duration: ",p["duration"]))

    print("<TR><TD COLSPAN=\"2\"> Inputs</TD></TR>")
    for mat in p["inputs"]:
        print("<TR><TD PORT=\"{}\">{}</TD><TD>{}</TD></TR>".format(mat[0],mat[0],mat[1]))

    print("<TR><TD COLSPAN=\"2\"> Outputs</TD></TR>")
    for o in p["outputs"]:
        print("<TR><TD>{}</TD><TD PORT=\"{}\">{}</TD></TR>".format(o[0],o[0],o[1]))

    print("</TABLE>>]")

def matNode(prefix, mat, materials):
    if mat in materials[0]:
        print("b_{} [label={},shape = box]".format(objhash(prefix + mat),mat))
    if mat in materials[1]:
        print("b_{} [label={},shape = ellipse]".format(objhash(prefix + mat),mat))

def bufferCluster(prefix, buffers, materials, iColor = inputColor, oColor = outputColor)
    print("subgraph cluster_{}i".format(prefix) + "{")
    print("label=\"input\"")
    print("bgcolor=\"{}\"".format(iColor))
    for mat in buffers["input"]:
        matNode(prefix,mat,stored)
    print("}")

    print("subgraph cluster_{}o".format(prefix) + "{")
    print("label=\"output\"")
    print("bgcolor=\"{}\"".format(oColor))
    for mat in buffers["output"]:
        matNode(prefix,mat,stored)
    print("}")

    for mat in buffers["other"]:
        matNode(prefix,mat,stored)

    return buffers["input"] + buffers["output"] + buffers["other"]

def recipeCluster(prefix,cluster,materials)
    print("subgraph \"cluster_{}\"".format(prefix + cluster["name"]) + "{")
    print("label = \"{}\"".format(cluster["name"]))
    buf = bufferCluster(prefix + cluster["name"],cluster["buffers"],materials)
    for rec in cluster["recipes"]:
        procNode(rec)
    # linking inside
    
def convert(obj):
    # graph beginning
    print("digraph " + "GREG" + "{")
    print("rankdir = \"LR\"")

    # materials
    stored = [set(obj["materials"]["solids"]), set(obj["materials"]["fluids"])]
    # global buffers
    glob_buf = bufferCluster("gl",obj["buffers"],stored,globalInputColor,globalOutputColor)

    recipeList = []
    # process nodes
    print("node [shape = plain]")
    for proc in obj["processes"]:
        if "cluster" in proc:
            print("subgraph \"cluster_{}\"".format(proc["cluster"]) + "{")
            print("label = \"{}\"".format(proc["cluster"]))
            recipeList+=proc["processes"]
            for recipe in proc["processes"]:
                procNode(recipe)
            print("}")
        else:
            recipeList.append(proc)
            procNode(proc)
    # linking
    for proc in recipeList:
        h = objhash(proc)
        for req in proc["inputs"]:
            mat = req[0]
            base = "s_{} -> p_{}:\"{}\"".format(objhash(mat),h,mat)
            if mat in stored[0]:
                print(base,"[color={}]".format(solidColor))
            elif mat in stored[1]:
                print(base,"[color={}]".format(fluidColor))
            else:
                for source in recipeList:
                    if mat in [req[0] for req in source["outputs"]]:
                        print("p_{}:\"{}\" -> p_{}:\"{}\"".format(objhash(source),mat,h,mat))
        for req in proc["outputs"]:
            mat = req[0]
            base = "p_{}:\"{}\" -> s_{}".format(h,mat,objhash(mat))
            if mat in stored[0]:
                print(base,"[color={}]".format(solidColor))
            elif mat in stored[1]:
                print(base,"[color={}]".format(fluidColor))

    print("}")

def main():
    name = sys.argv[1]
    old_stdout = sys.stdout
    with open(name + ".json") as file:
        obj = json.load(file)
        with open(name + ".dot",'w') as out:
            sys.stdout = out
            convert(obj)
            sys.stdout.flush()
            sys.stdout = old_stdout

    subprocess.run(["dot",name + ".dot","-Tpng","-o",name+".png"])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Missing argument")
    else:
        main()
