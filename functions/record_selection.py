from tkinter import *
import tkinter
from tkinter.tix import COLUMN
from functions.scroll_frame import onFrameConfigure
import config

def packFilter(textbox: tkinter):
    textbox.pack(fill=X)

def clearFrame(frame: tkinter):
    frame.pack_forget()


def positionRecordBoxes(boxes: list):
    for n, b in enumerate(boxes):
        b.delete(0, END)
        b.grid(row=n + 1, column=2, padx=10, pady=10)


def positionRecordLabels(labels: list):
    for n, l in enumerate(labels):
        l.grid(row=n + 1, column=1, padx=10, pady=10)

def positionRelatedButtons(btns: list):
    for n, b in enumerate(btns):
        b.grid(row=n, column=1, padx=10, pady=10)


def selectRecord(tree: tkinter) -> list:

    selected = tree.focus()

    values = tree.item(selected, "values")

    return list(values)


def insertValuesToBox(
    tree: tkinter,
    labels: list,
    boxes: list,
    parent_frame: tkinter,
    frame: tkinter,
    canvas: tkinter
):
    
    parent_frame.pack(fill="x", expand="yes", padx=20)

    frame.pack(fill="x", expand="yes", padx=20)

    values = selectRecord(tree)

    boxes[0].configure(state="normal")

    positionRecordBoxes(boxes)
    positionRecordLabels(labels)

    for n, box in enumerate(boxes):
        box.insert(0, values[n])

    boxes[0].configure(state="readonly")

    onFrameConfigure(canvas)

    config.btn_st = "Update"


def createNewRecordFrame(
    parent_frame: tkinter,
    frame: tkinter,
    boxes: list,
    labels: list,
    canvas: tkinter
):
    boxes[0].configure(state="normal")

    positionRecordBoxes(boxes)
    positionRecordLabels(labels)

    boxes[0].configure(state="readonly")

    parent_frame.pack(fill="x", expand="yes", padx=20)
    frame.pack(fill="x", expand="yes", padx=20)

    onFrameConfigure(canvas)

    config.btn_st = "New"
