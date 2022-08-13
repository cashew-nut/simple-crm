from tkinter import *



def configureTree(tree, data: Frame):

    tree['columns'] = list(data.columns)

    # format columns
    tree.column("#0", width=0, stretch=NO)

    for column in tree['columns']:
        tree.column(column, anchor=CENTER, width=140)

    # name headers
    tree.heading("#0", text="", anchor=W)
    for column in tree['columns']:
        tree.heading(column, text=column, anchor=CENTER)

    # create striped row tags
    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("evenrow", background="lightblue")

    # add our data to the screen

    column_count = data.shape[1]

    for n, record in enumerate(data.values):
        if n % 2 == 0:
            tree.insert(
                parent="",
                index="end",
                iid=n,
                text="",
                values=(list(record[0:column_count])),
                tags=("evenrow",),
            )
        else:
            tree.insert(
                parent="",
                index="end",
                iid=n,
                text="",
                values=(list(record[0:column_count])),
                tags=("oddrow",),
            )