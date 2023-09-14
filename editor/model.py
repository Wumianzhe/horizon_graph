from converter.recipe import base
from converter.line import line as prodLine
from converter.cluster import cluster as prodCluster
from typing import Optional
from PyQt5.Qt import QStandardItemModel,QStandardItem

class RecipeItem(QStandardItem):
    def __init__(self,recipe:base):
        if isinstance(recipe,prodCluster):
            super().__init__(recipe.name)
        else:
            super().__init__(recipe.machine)
        self.data:base = recipe

def modelLine(line: Optional[prodLine]):
    model:QStandardItemModel = QStandardItemModel()
    if line is None:
        return model
    def addChildren(cl:prodCluster, parent):
        clItem = RecipeItem(cl)
        parent.appendRow(clItem)
        for c in cl.subclusters:
            addChildren(c,clItem)

    top = model.invisibleRootItem()
    for cl in line.subclusters:
        addChildren(cl,top)
    return model
