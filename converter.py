#!/usr/bin/env python3
import json
import hashlib
import sys
import subprocess

fluidColor = "darkorchid"
solidColor = "firebrick"
inputColor = "deepskyblue"
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
    # return pair of material and corresponding edge destination
    return {"inputs":[(req[0],"p_{}:{}".format(objhash(p),req[0])) for req in p["inputs"]],
            "outputs":[(req[0],"p_{}:{}".format(objhash(p),req[0])) for req in p["outputs"]]}

def matNode(prefix, mat, materials):
    if mat in materials[0]:
        print("b_{} [label=\"{}\",shape = box]".format(objhash(prefix + mat),mat))
    elif mat in materials[1]:
        print("b_{} [label=\"{}\",shape = ellipse]".format(objhash(prefix + mat),mat))
    else:
        print("b_{} [label=\"{}\",shape = octagon]".format(objhash(prefix + mat),mat))

def bufferCluster(prefix, buffers, materials, iColor = inputColor, oColor = outputColor, group = False):
    if group:
        print("subgraph \"cluster_{}i\"".format(prefix) + "{")
        print("label=\"input\"")
        print("bgcolor=\"{}\"".format(iColor))
    else:
        print("node [style=\"filled\",fillcolor=\"{}\"]".format(iColor))
    for mat in buffers["input"]:
        matNode(prefix,mat,materials)
    if group:
        print("}")

        print("subgraph \"cluster_{}o\"".format(prefix) + "{")
        print("label=\"output\"")
        print("bgcolor=\"{}\"".format(oColor))
    else:
        print("node [style=\"filled\",fillcolor=\"{}\"]".format(oColor))
    for mat in buffers["output"]:
        matNode(prefix,mat,materials)
    if group:
        print("}")

    print("node [style=\"\"]")
    for mat in buffers["other"]:
        matNode(prefix,mat,materials)

    return buffers["input"] + buffers["output"] + buffers["other"]

def recipeCluster(prefix,cluster,materials):
    print("subgraph \"cluster_{}\"".format(prefix + cluster["name"]) + "{")
    print("label = \"{}\"".format(cluster["name"]))
    buf = bufferCluster(prefix + cluster["name"],cluster["buffers"],materials)
    for rec in cluster["recipes"]:
        procNode(rec)
    # linking inside
    for proc in cluster["recipes"]:
        h = objhash(proc)
        for req in proc["inputs"]:
            mat = req[0]
            matColor = "black"
            if mat in materials[0]:
                matColor = solidColor
            elif mat in materials[1]:
                matColor = fluidColor

            base = "b_{} -> p_{}:\"{}\"".format(objhash(prefix + cluster["name"] + mat),h,mat)
            if mat in buf:
                print(base,"[color={}]".format(matColor))
            else:
                for source in cluster["recipes"]:
                    if mat in [req[0] for req in source["outputs"]]:
                        print("p_{}:\"{}\" -> p_{}:\"{}\" [color={}]".format(objhash(source),mat,h,mat,matColor))
        for req in proc["outputs"]:
            mat = req[0]
            matColor = "black"
            if mat in materials[0]:
                matColor = solidColor
            elif mat in materials[1]:
                matColor = fluidColor

            base = "p_{}:\"{}\" -> b_{}".format(h,mat,objhash(prefix+ cluster["name"] + mat))
            if mat in buf:
                print(base,"[color={}]".format(matColor))
    print("}")
    return {"inputs":[(mat,"b_{}".format(objhash(prefix + cluster["name"] + mat))) for mat in cluster["buffers"]["input"]],
            "outputs":[(mat,"b_{}".format(objhash(prefix + cluster["name"] + mat))) for mat in cluster["buffers"]["output"]]}
    
def convert(obj):
    # graph beginning
    print("digraph " + "GREG" + "{")
    print("rankdir = \"LR\"")

    # materials
    matList = [set(obj["materials"]["solids"]), set(obj["materials"]["fluids"])]
    # global buffers
    glob_buf = bufferCluster("gl",obj["buffers"],matList,globalInputColor,globalOutputColor,True)

    recipeList = []
    # process clusters
    print("node [shape = plain]")
    if "clusters" in obj:
        for cluster in obj["clusters"]:
            recipeList.append(recipeCluster("",cluster,matList))
    #process standalone recipes
    if "recipes" in obj:
        for req in obj["recipes"]:
            recipeList.append(procNode(req))
    # linking
    for proc in recipeList:
        h = objhash(proc)
        for (mat,slot) in proc["inputs"]:
            base = "b_{} -> {}".format(objhash("gl" +mat),slot)
            matColor = "black"
            if mat in matList[0]:
                matColor = solidColor
            elif mat in matList[1]:
                matColor = fluidColor
            if mat in glob_buf:
                print(base,"[color={}]".format(matColor))
            else:
                sources = [req for rec in recipeList for req in rec["outputs"] if req[0] == mat]
                #sources = [rec for rec in recipeList if mat in [req[0] for req in rec["outputs"]]]
                for source in sources:
                    print("{} -> {}".format(source[1],slot))
        for (mat,slot) in proc["outputs"]:
            base = "{} -> b_{}".format(slot, objhash("gl" +mat))
            matColor = "black"
            if mat in matList[0]:
                matColor = solidColor
            elif mat in matList[1]:
                matColor = fluidColor
            if mat in glob_buf:
                print(base,"[color={}]".format(matColor))

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

    subprocess.run(["dot",name + ".dot","-Tpdf","-o",name+".pdf"])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Missing argument")
    else:
        main()
