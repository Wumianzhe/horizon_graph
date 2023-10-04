from string import Template
from numbers import Number
from typing import Optional
import converter.utils as utils
import shortuuid

class base:
    def __init__(self,proc:dict):
        self.machine:str = proc["machine"]
        self.tier:str = proc["tier"]
        self.tag:str = proc.get("tag",shortuuid.uuid())
        self.duration:Number = proc["duration"]
        self.inputs:dict[str,Number] = proc["inputs"]
        self.outputs:dict[str,Number] = proc["outputs"]

    def __hash__(self):
        return self.tag
    def getInputs(self) -> list[tuple[str,str]]:
        """Returns pairs of material name and corresponding graph node"""
        return [(mat,"p_{}:\"{}\"".format(self.tag,mat)) for mat in self.inputs.keys()]
    def getOutputs(self)-> list[tuple[str,str]]:
        """Returns pairs of material name and corresponding graph node"""
        return [(mat,"p_{}:\"{}\"".format(self.tag,mat)) for mat in self.outputs.keys()]

    def __str__(self) -> str:
        """Graph element corresponding to recipe"""
        lines: list[str] = []
        # header
        lines.extend(self.header())

        # io
        lines.extend(self.inputBlock())
        lines.extend(self.outputBlock())

        # middle rows
        lines.extend(self.children())
        # linkage
        lines.extend(self.linking())
        # footer
        lines.extend(self.footer())
        return "\n".join(lines)
    def header(self) -> list[str]:
        lines: list[str] = []
        # header
        lines.append("p_{} [shape=plain,label = <".format(self.tag))
        lines.append("<TABLE>")
        headRow = Template("<TR><TD>$first</TD><TD>$second</TD></TR>")
        lines.append(headRow.substitute(first=self.machine,second=self.tier))
        lines.append(headRow.substitute(first="Duration:",second=str(self.duration) + " sec"))
        return lines

    def children(self) -> list[str]:
        lines: list[str] = []
        return lines
    def inputBlock(self) -> list[str]:
        lines: list[str] = []
        recRow = Template("<TR><TD PORT=\"$name\">$name</TD><TD>$amount</TD></TR>")
        lines.append("<TR><TD COLSPAN=\"2\">Inputs</TD></TR>")
        lines.extend([recRow.substitute(name=mat,amount=count) for (mat,count) in self.inputs.items()])
        return lines
    def outputBlock(self) -> list[str]:
        lines: list[str] = []
        recRow = Template("<TR><TD>$name</TD><TD PORT=\"$name\">$amount</TD></TR>")
        lines.append("<TR><TD COLSPAN=\"2\">Outputs</TD></TR>")
        lines.extend([recRow.substitute(name=mat,amount=count) for (mat,count) in self.outputs.items()])
        return lines

    def footer(self) -> list[str]:
        return ["</TABLE>>]"]

    def linking(self) -> list[str]:
        return []
