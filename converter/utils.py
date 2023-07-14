from string import Template

def hexHash(obj):
    return hex(abs(hash(obj)))

def matNode(prefix:str,mat:str,materials:dict[str,str],theme:dict[str,str]):
    shape = theme.get(materials.get(mat,"")+"Shape","octagon")
    s = Template("\"b_$ha\" [label=\"$name\",shape=$shape]")
    return s.substitute(ha=hexHash(prefix + mat),name=mat,shape=shape)

def tuplify(listything):
    if isinstance(listything, list): return tuple(map(tuplify, listything))
    if isinstance(listything, dict): return {k:tuplify(v) for k,v in listything.items()}
    return listything
