from collections import defaultdict
from typing import Any
from converter.cluster import cluster
from itertools import zip_longest
import dearpygui.dearpygui as dpg

from converter.enums import VoltageTier

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

def _saveRec(s,a,u):
    modal, cells = u
    print("Save")
    dpg.configure_item(modal,show=False)
    print(cells)

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
        with dpg.table_row(parent=recTable):
            cells = [dpg.add_table_cell() for i in range(7)]
            rec_static = []
            rec_static.append(dpg.add_text(parent =cells[0], default_value =rec.machine))
            rec_static.append(dpg.add_text(parent =cells[1], default_value =rec.mtier))
            rec_static.append(dpg.add_text(parent =cells[2], default_value =rec.tier))
            rec_static.append(dpg.add_text(parent =cells[3], default_value =str(rec.duration)))
            rec_static.append(dpg.add_text(parent =cells[4], default_value =str(next(iter(rec.outputs.items())))))
            dpg.add_text(parent =cells[5], default_value ="1")
            b_Edit = dpg.add_button(parent=cells[6],label = "Edit")

            with dpg.popup(b_Edit,dpg.mvMouseButton_Left,True) as modal:
                with dpg.table(header_row=False,width=250):
                    dpg.add_table_column(width=150)
                    dpg.add_table_column(width=100)
                    with dpg.table_row():
                        dpg.add_text(default_value="Machine")
                        dpg.add_input_text(default_value=dpg.get_value(rec_static[0]))
                    with dpg.table_row():
                        dpg.add_text(default_value="Machine voltage")
                        dpg.add_combo(VoltageTier._member_names_,default_value=dpg.get_value(rec_static[1]))
                    with dpg.table_row():
                        dpg.add_text(default_value="Recipe voltabe")
                        dpg.add_combo(VoltageTier._member_names_,default_value=dpg.get_value(rec_static[2]))
                    with dpg.table_row():
                        dpg.add_text(default_value="Duration")
                        dpg.add_input_text(default_value=dpg.get_value(rec_static[3]))
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Save",width=75,callback=_saveRec,user_data=(modal,rec_static))
                    dpg.add_button(label="Cancel",width=75,callback=lambda s,a,u: dpg.configure_item(u,show=False),user_data=modal)

    subHeader = items[2]
    for c in cl.clusters:
        clHeader = dpg.add_collapsing_header(label=c.name,parent=subHeader)
        createTable(clHeader)
        populateTable(c,clHeader)
