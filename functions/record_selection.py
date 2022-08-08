from tkinter import *


def selectRecord(tree, labels,boxes):

    selected = tree.focus()

    values = tree.item(selected, 'values')

    n = 0

    for label in labels:
        label.grid(row=n, column=1, padx=10, pady=10)
        n += 1
        
    n = 0

    for box in boxes:
        box.grid(row=n, column=2, padx=10, pady=10)
        box.delete(0,END)
        box.insert(0,values[n])
        n += 1

def getRecord(boxes, updates):
    for item in boxes:
        v = item.get()
        updates.append(v)
        print(v)