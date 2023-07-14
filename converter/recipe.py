from string import Template
import utils

class base:
    def __init__(self,proc:dict):
        self.machine:str = proc["machine"]
        self.tier:str = proc["tier"]
        self.duration:str = proc["duration"]
        self.inputs:tuple = proc["inputs"]
        self.outputs:tuple = proc["outputs"]

    def __key(self):
        return (self.machine,self.inputs,self.outputs)
    def __hash__(self):
        return hash(self.__key())
    def getInputs(self) -> list[tuple[str,str]]:
        """Returns pairs of material name and corresponding graph node"""
        return [(req[0],"p_{}:{}".format(utils.hexHash(self),req[0])) for req in self.inputs]
    def getOutputs(self)-> list[tuple[str,str]]:
        """Returns pairs of material name and corresponding graph node"""
        return [(req[0],"p_{}:{}".format(utils.hexHash(self),req[0])) for req in self.outputs]

    def __str__(self) -> str:
        """Graph element corresponding to recipe"""
        lines: list[str] = []
        # header
        lines.extend(self.header())

        # middle rows
        lines.extend(self.intermediary())
        # io
        lines.extend(self.ioBlock())

        # linkage
        lines.extend(self.linking())
        # footer
        lines.extend(self.footer())
        return "\n".join(lines)
    def header(self) -> list[str]:
        lines: list[str] = []
        # header
        lines.append("p_{} [shape=plain,label = <".format(utils.hexHash(self)))
        lines.append("<TABLE>")
        return lines

    def intermediary(self) -> list[str]:
        lines: list[str] = []
        headRow = Template("<TR><TD>$first</TD><TD>$second</TD></TR>")
        lines.append(headRow.substitute(first=self.machine,second=self.tier))
        lines.append(headRow.substitute(first="Duration:",second=self.duration + " sec"))
        return lines

    def ioBlock(self) -> list[str]:
        lines: list[str] = []
        recRow = Template("<TR><TD>$name</TD><TD PORT=\"$name\">$amount</TD></TR>")
        lines.append("<TR><TD COLSPAN=\"2\">Inputs</TD></TR>")
        lines.extend([recRow.substitute(name=req[0],amount=req[1]) for req in self.inputs])
        lines.append("<TR><TD COLSPAN=\"2\">Outputs</TD></TR>")
        lines.extend([recRow.substitute(name=req[0],amount=req[1]) for req in self.outputs])
        return lines

    def footer(self) -> list[str]:
        return ["</TABLE>>]"]

    def linking(self) -> list[str]:
        return []
