from recipe import base
from theme import defaultTheme
import utils

class cluster(base):
    def __init__(self,obj:dict,materials,theme=defaultTheme,prefix=""):
        self.buffers:dict[str,tuple[str,...]] = obj["buffers"]
        self.name:str = obj["name"]
        self.prefix:str = prefix + self.name
        self.theme:dict[str,str] = theme
        self.materials:dict = materials
        self.recipes:tuple[base,...] = tuple((base(rec) for rec in obj.get("recipes",[])))
        self.subclusters:tuple[cluster,...] = tuple((cluster(cl,materials,theme) for cl in obj.get("clusters",[])))

    def __key(self):
        return (self.buffers,self.recipes,self.subclusters)
    def __hash__(self):
        return hash(self.__key())
    def getInputs(self) -> list[tuple[str, str]]:
        return [(mat,"b_{}".format(utils.hexHash(self.prefix + mat))) for mat in self.buffers["input"]]
    def getOutputs(self) -> list[tuple[str, str]]:
        return [(mat,"b_{}".format(utils.hexHash(self.prefix + mat))) for mat in self.buffers["output"]]
    def __str__(self) -> str:
        return super().__str__()

    def ioBlock(self) -> list[str]:
        return self.inputBlock() + self.outputBlock()

    def inputBlock(self) -> list[str]:
        lines: list[str] = []
        lines.append("node [style=\"filled\",fillcolor=\"{}\"]".format(
            self.theme.get("inputColor",defaultTheme["inputColor"])))
        lines.extend([utils.matNode(self.prefix,mat,self.materials,self.theme) for mat in self.buffers["input"]])
        return lines

    def outputBlock(self) -> list[str]:
        lines: list[str] = []
        lines.append("node [style=\"filled\",fillcolor=\"{}\"]".format(
            self.theme.get("outputColor",defaultTheme["outputColor"])))
        lines.extend([utils.matNode(self.prefix,mat,self.materials,self.theme) for mat in self.buffers["output"]])
        return lines

    def intermediary(self) -> list[str]:
        lines: list[str] = []
        lines.append("node [style=\"\"]")
        lines.extend([utils.matNode(self.prefix,mat,self.materials,self.theme) for mat in self.buffers["other"]])

        lines.extend([str(rec) for rec in self.recipes])
        lines.extend([str(cl) for cl in self.subclusters])
        return lines

    def header(self) -> list[str]:
        lines: list[str] = []
        lines.append("subgraph \"cluster_{}\"{{".format(self.prefix))
        lines.append("label = \"{}\"".format(self.name))
        return lines

    def linking(self) -> list[str]:
        lines: list[str] = []
        recList:tuple[base,...] = self.recipes + self.subclusters
        buf: tuple[str,...] = self.buffers["input"] + self.buffers["output"] + self.buffers["other"]
        inputs = [inList for rec in recList for inList in rec.getInputs()]
        outputs = [outList for rec in recList for outList in rec.getOutputs()]
        for (mat,slot) in inputs:
            color = self.theme.get(self.materials.get(mat,"")+"Color","black")
            if mat in buf:
                lines.append("b_{} -> {}".format(utils.hexHash(self.prefix + mat),slot))
            else:
                sources = [p for p in outputs if p[0] == mat]
                lines.extend(["{} -> {}".format(source[1],slot) for source in sources])
        for (mat,slot) in outputs:
            color = self.theme.get(self.materials.get(mat,"")+"Color","black")
            if mat in buf:
                lines.append("{1} -> b_{0}".format(utils.hexHash(self.prefix + mat),slot))
        return lines

    def footer(self) -> list[str]:
        return ["}"]
