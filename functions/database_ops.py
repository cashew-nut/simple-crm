from sqlalchemy import create_engine
import config
import pandas as pd
import tkinter
from functions.record_selection import *
from functions.treeview import *


def myConnection():
    connection = create_engine(
        config.mysql_url
        + config.user
        + ":"
        + config.password
        + "@"
        + config.host_name
        + "/"
        + config.schema
    )
    return connection


def pullTable(tbl: str):
    connection = myConnection()
    tbl = pd.read_sql(f"SELECT * FROM simple_crm.{tbl}", con=connection)
    connection.connect().close()
    return tbl


def saveNew(tree: tkinter, boxes: list, tbl_name: str, frame: tkinter):

    updates = []

    columns = tree["columns"]

    connection = myConnection()

    for n, item in enumerate(boxes):
        if n > 0:  # first is always id
            v = item.get()
            update = {columns[n]: v}
            updates.append(update)

    iv = [list(n.values()) for n in updates]
    iv = [item for sublist in iv for item in sublist]
    iv_string = ", ".join(f"'{item}'" for item in iv)
    column_string = ", ".join(
        f"`{item}`" for item in columns
    )  # note mysql column reference syntax
    try:
        connection.execute(
            f"INSERT INTO {tbl_name} ({column_string}) VALUES (DEFAULT, {iv_string})"
        )
        print(f"new record: ({column_string}) VALUES (DEFAULT, {iv_string})")
    except:
        print(f("insertion faild"))

    refreshAfterUpdate(frame, tree, boxes, tbl_name)


def deleteRecord(tree: tkinter, tbl_name: str, boxes: list, frame: tkinter):
    values = selectRecord(tree)
    id = values[0]
    connection = myConnection()
    try:
        connection.execute(f"DELETE FROM {tbl_name} WHERE `id` = {id}")
        print(f"the following record has been deleted: {values}")
    except:
        print(f"could not delete record: {values}")

    refreshAfterUpdate(frame, tree, boxes, tbl_name)


def updateRecord(tree: tkinter, boxes: list, tbl_name: str, frame: tkinter):

    columns = list(tree["columns"])

    values = selectRecord(tree)

    updates = {}

    changes = []

    connection = myConnection()

    # format update dictionary
    for n, item in enumerate(boxes):
        v = item.get()
        update = {values[n]: v}
        updates[columns[n]] = update

    # extract just the changed values that need updating / inserting
    for n, item in enumerate(updates):
        old = list(list(updates.values())[n].keys())
        new = list(list(updates.values())[n].values())
        if old != new and new != [""]:
            changes.append(item)

    # change action depending on update or insert
    if len(changes) > 0:
        for item in changes:
            nv = str(list(updates[item].values())[0])
            ov = list(updates[item].keys())[0]
            id = boxes[0].get()
            try:
                connection.execute(
                    f"UPDATE {tbl_name} SET `{item}` = '{nv}' WHERE `id` = '{id}'",
                    con=connection,
                )
                print(f"updated: record id {id}, field {item}, from {ov} to {nv}")
            except:
                print(
                    f"Could not update record id {id}, field {item}, from {ov} to {nv}"
                )

        refreshAfterUpdate(frame, tree, boxes, tbl_name)


def save(tree: tkinter, boxes: list, tbl_name: str, frame: tkinter):
    if config.btn_st == "New":
        saveNew(tree, boxes, tbl_name, frame)
    if config.btn_st == "Update":
        updateRecord(tree, boxes, tbl_name, frame)


def refreshAfterUpdate(
    frame: tkinter, tree: tkinter, boxes: list, active_table_name: str
):
    data = pullTable(active_table_name)

    # clear old tree
    for i in tree.get_children():
        tree.delete(i)

    # clear boxes
    for box in boxes:
        box.delete(0, END)

    # refresh tree
    configureTree(tree, data)
    clearFrame(frame)

def relatedTableNames(tbl_name: str, schema: str) -> list:
    
    connection = myConnection()
    
    r_tbls = pd.read_sql(f"""SELECT
                            table_name
                            FROM information_schema.KEY_COLUMN_USAGE
                            WHERE table_schema = '{schema}'
                            AND referenced_table_name = '{tbl_name}';""", con=connection
    )
    print(r_tbls["TABLE_NAME"].to_list())
    return r_tbls["TABLE_NAME"].to_list()