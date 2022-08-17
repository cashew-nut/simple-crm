from tkinter import *
import tkinter
from functions.database_ops import *
from functions.treeview import *


def positionRecordBoxes(bxs: list):  
    for n, b in enumerate(bxs):
        b.delete(0,END)
        b.grid(row=n, column=2, padx=10, pady=10)

    
def positionRecordLabels(lbls: list):
    for n, l in enumerate(lbls):
        l.grid(row=n, column=1, padx=10, pady=10)

def refreshAfterUpdate(frame: tkinter, tree: tkinter, boxes: list, active_table_name: str):
    data = pullTable(active_table_name)
    
    try:
        frame.pack_forget()
    except:
        print('no frame packed')

    #clear old tree
    for i in tree.get_children():
        tree.delete(i)
    
    # clear boxes
    for box in boxes:
        box.delete(0, END)
    
    #refresh tree
    configureTree(tree, data)

def selectRecord(tree: tkinter) -> list:

    selected = tree.focus()

    values = tree.item(selected, "values")

    return list(values)


def insertValuesToBox(tree: tkinter, labels: list, boxes: list, frame: tkinter, tbl_name: str):

    try:
        frame.pack_forget()
    except:
        print('no frame packed')


    values = selectRecord(tree)

    positionRecordBoxes(boxes)
    positionRecordLabels(labels)

    frame.pack(fill="x", expand="yes", padx=20)

    for n, box in enumerate(boxes):
        # box.delete(0, END)
        box.insert(0, values[n])
    
    save_to_database_button = Button(
    frame,
    text="Update Database",
    command=lambda: updateRecord(tree, boxes, tbl_name, frame),
    )
    save_to_database_button.grid(row= len(boxes) + 1, column=2, padx=10, pady=10)

def updateRecord(tree: tkinter, boxes: list, tbl_name: str, frame: tkinter):

    columns = list(tree['columns'])

    values = selectRecord(tree)

    updates = {}

    changes = []

    connection = myConnection()

    #format update dictionary
    for n, item in enumerate(boxes):
        v = item.get()
        update = {values[n]: v}
        updates[columns[n]] = update

    #extract just the changed values that need updating / inserting
    for n, item in enumerate(updates):
        old = list(list(updates.values())[n].keys())
        new = list(list(updates.values())[n].values())
        if old != new and new != ['']:
            changes.append(item)

    #change action depending on update or insert
    if len(changes) > 0:
        for item in changes:
            nv = str(list(updates[item].values())[0])
            ov = list(updates[item].keys())[0]
            id = list(updates['id'].keys())[0]
            try:
                connection.execute(f"UPDATE {tbl_name} SET `{item}` = '{nv}' WHERE `id` = '{id}'", con=connection)
                print(f"updated: record id {id}, field {item}, from {ov} to {nv}")
            except:
                print(f"Could not update record id {id}, field {item}, from {ov} to {nv}")
        
        refreshAfterUpdate(frame, tree, boxes, tbl_name)
    

def createNewRecordFrame(tree: tkinter, active_table_name: str, frame: tkinter, boxes: list, labels: list):

    try:
        frame.pack_forget()
    except:
        print('no frame packed')

    positionRecordBoxes(boxes)
    positionRecordLabels(labels)

    frame.pack(fill="x", expand="yes", padx=20)

    save_to_database_button = Button(
    frame,
    text="Save New Record to Database",
    command=lambda: saveNew(tree, boxes, active_table_name, frame),
    )
    save_to_database_button.grid(row= len(boxes) + 1, column=2, padx=10, pady=10)


def saveNew(tree: tkinter, boxes: list, active_table_name: str, frame: tkinter):

    updates = []

    columns = tree['columns']

    connection = myConnection()

    for n, item in enumerate(boxes):
        if n > 0: #first is always id
            v = item.get()
            update = {columns[n]: v}
            updates.append(update)

    iv = [list(n.values()) for n in updates]
    iv = [item for sublist in iv for item in sublist]
    iv_string = ', '.join(f"'{item}'" for item in iv)
    column_string = ', '.join(f"`{item}`" for item in columns) #note mysql column reference syntax
    try:
        connection.execute(f"INSERT INTO {active_table_name} ({column_string}) VALUES (DEFAULT, {iv_string})")
        print(f"new record: ({column_string}) VALUES (DEFAULT, {iv_string})")
    except:
        print(f("insertion faild"))

    refreshAfterUpdate(frame, tree, boxes, active_table_name)



def deleteRecord(tree: tkinter, active_tbl_name: str, boxes: list, frame: tkinter):
    values = selectRecord(tree)
    id = values[0]
    connection = myConnection()
    try:
        connection.execute(f'DELETE FROM {active_tbl_name} WHERE `id` = {id}')
        print(f"the following record has been deleted: {values}")
    except:
        print(f"could not delete record: {values}")

    refreshAfterUpdate(frame, tree, boxes, active_tbl_name)
