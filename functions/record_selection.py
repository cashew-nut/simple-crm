from tkinter import *
import tkinter
from functions.database_ops import *
from functions.treeview import *

def selectRecord(tree: tkinter) -> list:

    selected = tree.focus()

    values = tree.item(selected, "values")

    return list(values)


def insertValuesToBox(tree, labels, boxes):

    values = selectRecord(tree)

    for n, label in enumerate(labels):
        label.grid(row=n, column=1, padx=10, pady=10)

    for n, box in enumerate(boxes):
        box.grid(row=n, column=2, padx=10, pady=10)
        box.delete(0, END)
        box.insert(0, values[n])

def updateRecord(tree: tkinter, boxes: list, columns: list, tbl_name: str):

    values = selectRecord(tree)

    updates = {}

    changes = []

    connection = myConnection()

    #check to see if this is a new record or update of old
    if len(values) > 0:
        insert = FALSE
    else:
        insert = TRUE

    #format update dictionary
    for n, item in enumerate(boxes):
        v = item.get()
        if insert == FALSE:
            update = {values[n]: v}
        else:
            update = {'': v}
        updates[columns[n]] = update

    #extract just the changed values that need updating / inserting
    for n, item in enumerate(updates):
        old = list(list(updates.values())[n].keys())
        new = list(list(updates.values())[n].values())
        if old != new and new != ['']:
            changes.append(item)

    #change action depending on update or insert
    if len(changes) > 0 and insert == FALSE:
        for item in changes:
            nv = str(list(updates[item].values())[0])
            ov = list(updates[item].keys())[0]
            id = list(updates['id'].keys())[0]
            try:
                connection.execute(f"UPDATE {tbl_name} SET `{item}` = '{nv}' WHERE `id` = '{id}'", con=connection)
                print(f"updated: record id {id}, field {item}, from {ov} to {nv}")
            except:
                print(f"Could not update record id {id}, field {item}, from {ov} to {nv}")
        
    elif len(changes) > 0 and insert == TRUE: 
        iv = [str(list(updates[item].values())[0]) for item in changes]
        iv_string = ', '.join(f"'{item}'" for item in iv)
        column_string = ', '.join(f"`{item}`" for item in columns) #note mysql column reference syntax
        try:
            connection.execute(f"INSERT INTO {tbl_name} ({column_string}) VALUES (DEFAULT, {iv_string})")
            print(f"new record: ({column_string}) VALUES (DEFAULT, {iv_string})")
        except:
            print(f("insertion faild"))

    df = pullTable(tbl_name)

    #clear old tree
    for i in tree.get_children():
        tree.delete(i)
    
    # clear boxes
    for box in boxes:
        box.delete(0, END)
    
    #refresh tree
    configureTree(tree, df)
    

def createNew(labels: list, boxes: list, tree: tkinter): 
    for n, label in enumerate(labels):
        label.grid(row=n, column=1, padx=10, pady=10)

    for n, box in enumerate(boxes):
        box.grid(row=n, column=2, padx=10, pady=10)
        box.delete(0, END)
    
    tree.selection_clear()


def deleteRecord(tree: tkinter, tbl_name: str, boxes: list):
    values = selectRecord(tree)
    id = values[0]
    connection = myConnection()
    try:
        connection.execute(f'DELETE FROM {tbl_name} WHERE `id` = {id}')
        print(f"the following record has been deleted: {values}")
    except:
        print(f"could not delete record: {values}")

    df = pullTable(tbl_name)

    #clear old tree
    for i in tree.get_children():
        tree.delete(i)
    
    # clear boxes
    for box in boxes:
        box.delete(0, END)
    
    #refresh tree
    configureTree(tree, df)