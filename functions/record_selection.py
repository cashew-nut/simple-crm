from tkinter import *
from functions.database_ops import *
from functions.treeview import *

def selectRecord(tree):

    selected = tree.focus()

    values = tree.item(selected, "values")

    return values


def insertValuesToBox(tree, labels, boxes):

    values = selectRecord(tree)

    for n, label in enumerate(labels):
        label.grid(row=n, column=1, padx=10, pady=10)

    for n, box in enumerate(boxes):
        box.grid(row=n, column=2, padx=10, pady=10)
        box.delete(0, END)
        box.insert(0, values[n])


# split to two functions, 1 to get values and 1 to put the values in the button. And run the function within bottom


def updateRecord(tree, boxes: list, columns: list, tbl_name: str):

    values = list(selectRecord(tree))

    updates = {}

    changes = []

    connection = myConnection()

    for n, item in enumerate(boxes):
        v = item.get()
        update = {values[n]: v}
        updates[columns[n]] = update

    for n, item in enumerate(updates):
        old = list(list(updates.values())[n].keys())
        new = list(list(updates.values())[n].values())
        if old != new:
            changes.append(item)

    for item in changes:
        nv = str(list(updates[item].values())[0])
        ov = list(updates[item].keys())[0]
        id = list(updates['id'].keys())[0]
        try:
            connection.execute(f"UPDATE {tbl_name} SET `{item}` = '{nv}' WHERE `id` = '{id}'", con=connection)
            print(f"updated: record id {id}, field {item}, from {ov} to {nv}")
        except:
            print(f"Could not update record id {id}, field {item}, from {ov} to {nv}")

    df = pullTable(tbl_name)

    for i in tree.get_children():
        tree.delete(i)
        
    configureTree(tree, df)

    return df
    
    
    

    