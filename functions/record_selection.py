from tkinter import *
import tkinter
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
    parent_frame: tkinter,
    frame: tkinter,
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

    config.btn_st = "Update"


def createNewRecordFrame(
    parent_frame: tkinter,
    frame: tkinter,
    boxes: list,
    labels: list,
):
    boxes[0].configure(state="normal")

    positionRecordBoxes(boxes)
    positionRecordLabels(labels)

    boxes[0].configure(state="readonly")

    parent_frame.pack(fill="x", expand="yes", padx=20)
    frame.pack(fill="x", expand="yes", padx=20)

    config.btn_st = "New"
