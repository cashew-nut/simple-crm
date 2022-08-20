from dis import Instruction
from sre_parse import State
from tkinter import *
import tkinter
from functions.database_ops import *
from functions.treeview import *
import config


def clearFrame(frame: tkinter):
    frame.pack_forget()


def positionRecordBoxes(bxs: list):
    for n, b in enumerate(bxs):
        b.delete(0, END)
        b.grid(row=n, column=2, padx=10, pady=10)


def positionRecordLabels(lbls: list):
    for n, l in enumerate(lbls):
        l.grid(row=n, column=1, padx=10, pady=10)


def selectRecord(tree: tkinter) -> list:

    selected = tree.focus()

    values = tree.item(selected, "values")

    return list(values)


def insertValuesToBox(
    tree: tkinter,
    labels: list,
    boxes: list,
    frame: tkinter,
):
    frame.pack(fill="x", expand="yes", padx=20)
    
    values = selectRecord(tree)

    positionRecordBoxes(boxes)
    positionRecordLabels(labels)

    for n, box in enumerate(boxes):
        box.insert(0, values[n])

    

    config.btn_st = "Update"


def createNewRecordFrame(
    frame: tkinter,
    boxes: list,
    labels: list,
):

    positionRecordBoxes(boxes)
    positionRecordLabels(labels)

    frame.pack(fill="x", expand="yes", padx=20)

    config.btn_st = "New"
