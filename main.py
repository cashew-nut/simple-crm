from tkinter import *
from tkinter import ttk
import pandas as pd
import config

root = Tk()
root.title("Cash CRM")
root.iconbitmap()
root.geometry("1000x800")

# add style
style = ttk.Style()

# pick a theme
style.theme_use("default")

# configure colours
style.configure(
    "Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3",
)

# Change selected colour
style.map("Treeview", background=[("selected", "#347083")])

# Create a treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# create a treeview scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create the treeview
my_tree = ttk.Treeview(
    tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended"
)
my_tree.pack()

# configure scrollbar
tree_scroll.config(command=my_tree.yview)

from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine(
    config.mysql_url
    + config.user
    + ":"
    + config.password
    + "@"
    + config.host_name
    + "/"
    + config.schema
)

animals = pd.read_sql("SELECT * FROM simple_crm.animals", con=engine)

engine.connect().close()

active_table = animals

my_tree["columns"] = list(active_table.columns)

# format columns
my_tree.column("#0", width=0, stretch=NO)
for column in my_tree["columns"]:
    my_tree.column(column, anchor=CENTER, width=140)

# name headers
my_tree.heading("#0", text="", anchor=W)
for column in my_tree["columns"]:
    my_tree.heading(column, text=column, anchor=CENTER)

# create striped row tags
my_tree.tag_configure("oddrow", background="white")
my_tree.tag_configure("evenrow", background="lightblue")

# add our data to the screen
global count
count = 0

column_count = active_table.shape[1]

for record in active_table.values:
    if count % 2 == 0:
        my_tree.insert(
            parent="",
            index="end",
            iid=count,
            text="",
            values=(list(record[0:column_count])),
            tags=("evenrow",),
        )
    else:
        my_tree.insert(
            parent="",
            index="end",
            iid=count,
            text="",
            values=(list(record[0:column_count])),
            tags=("oddrow",),
        )
    # increment counter
    count += 1

# add buttons and record entry boxes
button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

# building boxes dynamically

from functions.record_selection import selectRecord, updateRecord, insertValuesToBox

bxs = []
for b in my_tree["columns"]:
    b = Entry(data_frame)
    # i.pack()
    bxs.append(b)

lbls = []
for l in my_tree["columns"]:
    l = Label(data_frame, text=l)
    # i.pack()
    lbls.append(l)


tbl_columns = list(active_table.columns)


# double click to select. This is bad as it's using global variables in a functions scope
def onDouble(selected):
    insertValuesToBox(my_tree, lbls, bxs)


my_tree.bind("<Double-1>", onDouble)

# adding buttons

select_record_button = Button(
    button_frame,
    text="Select Record",
    command=lambda: insertValuesToBox(my_tree, lbls, bxs),
)
select_record_button.grid(row=0, column=1, padx=10, pady=10)

select_record_button = Button(
    button_frame,
    text="Update Record",
    command=lambda: updateRecord(my_tree, bxs, tbl_columns),
)
select_record_button.grid(row=0, column=2, padx=10, pady=10)

root.mainloop()
