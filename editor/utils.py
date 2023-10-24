from typing import Any
from converter.cluster import cluster
from itertools import zip_longest
import dearpygui.dearpygui as dpg

from converter.recipe import base
from editor.recipe import recipe

def unwrap(val: Any|None,default):
    return val if val is not None else default

def _select(sender):
    for item in ioitems:
        if item != sender:
            dpg.set_value(item,False)

def _edit(sender,a,ioTable):
    rows = dpg.get_item_children(ioTable,slot=1)
    cells = [cell for row in unwrap(rows,[]) for cell in unwrap(dpg.get_item_children(row,slot=1),[])]
    selections = [sel for cell in cells for sel in unwrap(dpg.get_item_children(cell,slot=1),[])]
    for sel in selections:
        if dpg.get_value(sel) is True:
            cell = dpg.get_item_parent(sel)
            name = dpg.get_item_label(sel)
            assert(cell is not None)
            assert(name is not None)
            ioitems.remove(sel)
            dpg.delete_item(cell,children_only=True)

            dpg.add_input_text(parent=cell,default_value=name,on_enter=True,callback=_sreplace)

ioitems = []
def _sreplace(item: int|str,text: str):
    cell = dpg.get_item_parent(item)
    assert(cell is not None)
    dpg.delete_item(cell,children_only=True)

    ioitems.append(dpg.add_selectable(parent=cell,label=text,callback=_select))

def addIO(Itype: int, udata: int|str):
    ioTable = udata
    diff:int = unwrap(dpg.get_item_user_data(ioTable),0)
    if diff*Itype>=0: # diff and Itype have same sign or diff is 0
        with dpg.table_row(parent=ioTable):
            cells = [dpg.add_table_cell() for i in range(2)]
    else:
        rows = unwrap(dpg.get_item_children(ioTable,slot=1),[])
        cells = unwrap(dpg.get_item_children(rows[diff*Itype],slot=1),[])
    dpg.add_input_text(on_enter=True,callback=_sreplace,parent=cells[0] if Itype == 1 else cells[1])
    diff+=Itype
    dpg.set_item_user_data(ioTable,diff)

def createTable(parent: int|str):
    with dpg.collapsing_header(label="IO",parent=parent,indent=5):
        with dpg.table(header_row=True,user_data=0) as ioTable:
            dpg.add_table_column(label="Inputs")
            dpg.add_table_column(label="Outputs")
        with dpg.group(horizontal=True, horizontal_spacing=20):
            dpg.add_button(label="Add input",callback=lambda s,a,u: addIO(1,u),user_data=ioTable)
            dpg.add_button(label="Add output",callback=lambda s,a,u: addIO(-1,u),user_data=ioTable)
            dpg.add_button(label="Edit",callback=_edit,user_data=ioTable)
            dpg.add_button(label="Remove selected",callback=lambda: print("WIP"))

    with dpg.collapsing_header(label="Recipes",parent=parent,indent=5):
        with dpg.table(header_row=True):
            dpg.add_table_column(label="Machine")
            dpg.add_table_column(label="Tier",width_fixed=True)
            dpg.add_table_column(label="Recipe tier",width_fixed=True)
            dpg.add_table_column(label="Duration")
            dpg.add_table_column(label="Outputs")
            dpg.add_table_column(label="Count")
            dpg.add_table_column()
    with dpg.collapsing_header(parent=parent,label="Subfactories",indent=5):
        pass

def populateTable(cl:cluster,parent: int|str):
    items = dpg.get_item_children(parent,slot=1)
    assert(isinstance(items, list))
    ioHeader = dpg.get_item_children(items[0],slot=1)
    assert(isinstance(ioHeader,list))
    ioTable = ioHeader[0]

    diff = len(cl.buffers["input"]) - len(cl.buffers["output"])
    dpg.set_item_user_data(ioTable,diff)
    for (i,o) in zip_longest(cl.buffers["input"],cl.buffers["output"]):
        with dpg.table_row(parent=ioTable):
            cells = [dpg.add_table_cell() for i in range(2)]
            if i:
                ioitems.append(dpg.add_selectable(label=i,parent=cells[0],callback=_select))
            if o:
                ioitems.append(dpg.add_selectable(label=o,parent=cells[1],callback=_select))

    recHeader = dpg.get_item_children(items[1],slot=1)
    assert(isinstance(recHeader,list))
    recTable = recHeader[0]
    for rec in cl.recipes:
        r = recipe(rec)
        with dpg.table_row(parent=recTable) as row:
            r.recRow(row)

    subHeader = items[2]
    for c in cl.clusters:
        clHeader = dpg.add_collapsing_header(label=c.name,parent=subHeader)
        createTable(clHeader)
        populateTable(c,clHeader)
