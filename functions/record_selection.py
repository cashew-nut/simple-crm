from tkinter import *


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


def updateRecord(tree, boxes, columns: list):

    values = list(selectRecord(tree))

    updates = {}

    # for n, item in enumerate(boxes):
    #     v = item.get()
    #     update = {columns[n]: v}
    #     updates.append(update)


    for n, item in enumerate(boxes):
        v = item.get()
        update = {values[n]: v}
        updates[columns[n]] = update

    print(f"New values: {updates}")
    

    