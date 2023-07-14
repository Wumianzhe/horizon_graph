from cluster import cluster
from recipe import base
from theme import defaultTheme
import utils

class line(cluster):
    def __init__(self,obj:dict,theme=defaultTheme):
        self.buffers:dict[str,tuple[str,...]] = obj["buffers"]
        self.prefix = "gl"
        self.theme = theme
        self.materials = self.convertMaterials(obj["materials"])
        self.recipes:tuple[base,...] = tuple((base(rec) for rec in obj.get("recipes",[])))
        self.subclusters:tuple[cluster,...] = tuple((cluster(cl,self.materials,theme) for cl in obj.get("clusters",[])))

    def convertMaterials(self,matDict):
        convDict = {mat:"solid" for mat in matDict["solids"]}
        convDict.update({mat:"fluid" for mat in matDict["fluids"]})
        return convDict
    def __key(self):
        return (self.buffers,self.recipes,self.subclusters)
    def __hash__(self):
        return hash(self.__key())
    def inputBlock(self) -> list[str]:
        lines: list[str] = []
        lines.append("subgraph cluster_glIn {")
        lines.append("label=\"input\"")
        lines.append("bgcolor=\"{}\"".format(self.theme.get("globalIColor",defaultTheme["globalIColor"])))
        lines.append("node [style=\"\"]")
        lines.extend([utils.matNode(self.prefix,mat,self.materials,self.theme) for mat in self.buffers["input"]])
        lines.append('}')
        return lines
    def outputBlock(self) -> list[str]:
        lines: list[str] = []
        lines.append("subgraph cluster_glOut {")
        lines.append("label=\"output\"")
        lines.append("bgcolor=\"{}\"".format(self.theme.get("globalOColor",defaultTheme["globalOColor"])))
        lines.append("node [style=\"\"]")
        lines.extend([utils.matNode(self.prefix,mat,self.materials,self.theme) for mat in self.buffers["output"]])
        lines.append('}')
        return lines
    def header(self) -> list[str]:
        lines: list[str] = []
        lines.append("digraph " + "GREG" + "{")
        lines.append("rankdir = \"LR\"")
        return lines
