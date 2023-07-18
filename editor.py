from PyQt5.QtWidgets import *
from editor.model import modelLine
import json
import converter.utils
import converter.line

def readPlatline():
    with open("platline.json") as file:
        obj = json.load(file)
        immObj = converter.utils.tuplify(obj)
    return converter.line.line(immObj)

app = QApplication([])
window = QMainWindow()
fileMenu = window.menuBar().addMenu("File")
central = QWidget()
window.setCentralWidget(central)
layout = QHBoxLayout()
central.setLayout(layout)
line = readPlatline()
model = modelLine(line)
tree = QTreeView()
tree.setModel(model)
tree.header().hide()
layout.addWidget(tree)
window.show()
app.exec()
