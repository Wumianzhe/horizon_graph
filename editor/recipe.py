from converter.recipe import base
import dearpygui.dearpygui as dpg
from converter.enums import VoltageTier
from typing import Any

def unwrap(val: Any|None,default):
    return val if val is not None else default

class recipe:
    def __init__(self,rec:base):
        self.rec = rec
        self.labels = []
        self.edit = []
        self.inItems = []
        self.outItems = []
    def recRow(self,row):
        self.row = row
        dpg.set_item_user_data(row,self)
        cells = [dpg.add_table_cell(parent=row) for i in range(7)]
        self.labels.append(dpg.add_text(parent=cells[0]))
        self.labels.append(dpg.add_text(parent=cells[1]))
        self.labels.append(dpg.add_text(parent=cells[2]))
        self.labels.append(dpg.add_text(parent=cells[3]))
        self.labels.append(dpg.add_text(parent=cells[4]))
        self.setLabels()
        dpg.add_text(parent =cells[5], default_value ="1")
        b_Edit = dpg.add_button(parent=cells[6],label = "Edit")
        self.recModal(b_Edit)
    def setLabels(self):
        dpg.set_value(self.labels[0],self.rec.machine)
        dpg.set_value(self.labels[1],self.rec.mtier)
        dpg.set_value(self.labels[2],self.rec.tier)
        dpg.set_value(self.labels[3],str(self.rec.duration))
        dpg.set_value(self.labels[4],str(next(iter(self.rec.outputs.items()))))
    def recModal(self,button):
        with dpg.popup(button,dpg.mvMouseButton_Left,True) as modal:
            with dpg.group(horizontal=True,horizontal_spacing=10):
                with dpg.table(header_row=False,width=250):
                    dpg.add_table_column(width=150)
                    dpg.add_table_column(width=100)
                    with dpg.table_row():
                        dpg.add_text(default_value="Machine")
                        self.edit.append(dpg.add_input_text(default_value=dpg.get_value(self.labels[0])))
                    with dpg.table_row():
                        dpg.add_text(default_value="Machine voltage")
                        self.edit.append(dpg.add_combo(VoltageTier._member_names_,default_value=dpg.get_value(self.labels[1])))
                    with dpg.table_row():
                        dpg.add_text(default_value="Recipe voltabe")
                        self.edit.append(dpg.add_combo(VoltageTier._member_names_,default_value=dpg.get_value(self.labels[2])))
                    with dpg.table_row():
                        dpg.add_text(default_value="Duration")
                        self.edit.append(dpg.add_input_text(default_value=dpg.get_value(self.labels[3])))
                with dpg.group():
                    dpg.add_text(default_value="Input")
                    with dpg.table(header_row=True,width=250) as ITable:
                        dpg.add_table_column(width=150,label="Material")
                        dpg.add_table_column(width=100,label="Amount")
                        for mat,amount in self.rec.inputs.items():
                            self.addIO(ITable,mat,amount,l=self.inItems)
                    with dpg.group(horizontal=True,horizontal_spacing=10):
                        dpg.add_button(label="Add",callback = lambda:self.addIO(ITable,edit=True))
                        dpg.add_button(label="Edit")
                with dpg.group():
                    dpg.add_text(default_value="Output")
                    with dpg.table(header_row=True,width=250) as OTable:
                        dpg.add_table_column(width=150,label="Material")
                        dpg.add_table_column(width=100,label="Amount")
                        for mat,amount in self.rec.outputs.items():
                            self.addIO(OTable,mat,amount,l=self.outItems)
                    with dpg.group(horizontal=True,horizontal_spacing=10):
                        dpg.add_button(label="Add",callback = lambda:self.addIO(OTable,edit=True))
                        dpg.add_button(label="Edit",callback = lambda:print(self.outItems))
            with dpg.group(horizontal=True):
                dpg.add_button(label="Save",width=75,callback=lambda s,a,u: self.saveRec(u),user_data=modal)
                dpg.add_button(label="Cancel",width=75,callback=lambda s,a,u: dpg.configure_item(u,show=False),user_data=modal)

    def saveRec(self,u):
        modal = u
        dpg.configure_item(modal,show=False)
        self.rec.machine = dpg.get_value(self.edit[0])
        self.rec.mtier = dpg.get_value(self.edit[1])
        self.rec.tier = dpg.get_value(self.edit[2])
        self.rec.duration = float(dpg.get_value(self.edit[3]))
        self.setLabels()
    def addIO(self,table,mat:str = '',amount: int|float = 0,edit = False,l = []):
        with dpg.table_row(parent=table) as row:
            if not edit:
                iMat = dpg.add_selectable(label=mat)
                iVal = dpg.add_selectable(label=str(amount))
                l.append((iMat,iVal))
            else:
                iMat = dpg.add_input_text(default_value=mat,callback=lambda: self.fixRow(row,l),on_enter=True)
                iVal = dpg.add_input_text(default_value=str(amount),callback=lambda: self.fixRow(row,l),on_enter=True)
    def fixRow(self, row,l):
        children = unwrap(dpg.get_item_children(row,slot=1),[])
        vals = [dpg.get_value(i) for i in children]
        dpg.delete_item(row,children_only=True)
        iMat = dpg.add_selectable(label=vals[0])
        iVal = dpg.add_selectable(label=vals[1])
        l.append((iMat,iVal))
    def editOutput(self):
        pass
