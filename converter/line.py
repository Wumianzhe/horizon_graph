from converter.cluster import cluster
from converter.recipe import base
from converter.theme import defaultTheme
import converter.utils as utils

class line(cluster):
    def __init__(self,obj:dict,theme=defaultTheme):
        self.buffers:dict[str,tuple[str,...]] = obj.get("buffers",{"input":(),"output":()})
        self.prefix = "gl"
        self.tag = "top"
        self.theme = theme
        self.materials = obj.get("materials",{})
        self.recipes:list[base] = [base(rec) for rec in obj.get("recipes",[])]
        self.clusters:list[cluster] = [cluster(cl,self.materials,theme) for cl in obj.get("clusters",[])]

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
