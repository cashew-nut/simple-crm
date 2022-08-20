from tkinter import *
from tkinter import ttk


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

# get db tables
from functions.database_ops import *

active_table_name = "animals"

active_table = pullTable(active_table_name)

# configure the treeview
from functions.treeview import *

configureTree(my_tree, active_table)


# add buttons and record entry boxes
button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

data_frame = LabelFrame(root, text="Record")


# building boxes dynamically

from functions.record_selection import *

bxs = []
for n, b in enumerate(my_tree["columns"]):
    b = Entry(data_frame)
    bxs.append(b)


lbls = []
for n, l in enumerate(my_tree["columns"]):
    l = Label(data_frame, text=l)
    lbls.append(l)


tbl_columns = list(active_table.columns)


# double click to select. This is bad as it's using global variables in a functions scope
def onDouble(selected):
    insertValuesToBox(my_tree, lbls, bxs, data_frame)


def onReturn(selected):
    save(my_tree, bxs, active_table_name, data_frame)


my_tree.bind("<Double-1>", onDouble)
root.bind("<Return>", onReturn)


# adding buttons

select_record_button = Button(
    button_frame,
    text="Select Record",
    command=lambda: insertValuesToBox(my_tree, lbls, bxs, data_frame),
)
select_record_button.grid(row=0, column=1, padx=10, pady=10)

create_new_record_button = Button(
    button_frame,
    text="Create New Record",
    command=lambda: createNewRecordFrame(data_frame, bxs, lbls),
)
create_new_record_button.grid(row=0, column=2, padx=10, pady=10)

delete_record_button = Button(
    button_frame,
    text="Delete Record",
    command=lambda: deleteRecord(my_tree, active_table_name, bxs, data_frame),
)
delete_record_button.grid(row=0, column=3, padx=10, pady=10)

clear_frame_button = Button(
    button_frame,
    text="Clear Frame",
    command=lambda: clearFrame(data_frame),
)
clear_frame_button.grid(row=0, column=4, padx=10, pady=10)


save_button = Button(
    data_frame,
    text="Save to Database",
    command=lambda: save(my_tree, bxs, active_table_name, data_frame),
)
save_button.grid(row=len(bxs) + 1, column=2, padx=10, pady=10)

root.mainloop()
