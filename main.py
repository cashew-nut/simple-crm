from tkinter import *
from tkinter import ttk
import pandas as pd
import config




root = Tk()
root.title("Cash CRM")
root.iconbitmap()
root.geometry("1000x800")
root.configure(bg='#4068a8')

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


#create listview frame, top of page
top_frame = Frame(root)
top_frame.pack(side = TOP, fill=Y, pady=10)
top_frame.configure(bg='#4068a8')


#add command buttons

button_frame = LabelFrame(top_frame, text="Commands")
button_frame.pack(side=BOTTOM, fill=X, expand="yes", padx=0.5)

# Create a treeview Frame
tree_frame = Frame(top_frame)
tree_frame.pack(side = TOP, fill=Y, pady=10)
tree_frame.configure(bg='#4068a8')

# create a treeview scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create the treeview
my_tree = ttk.Treeview(
    tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended"
)
my_tree.pack(side=LEFT)

# configure scrollbar
tree_scroll.config(command=my_tree.yview)

#this frame holds all the fields for individaul records and related records
data_frame = LabelFrame(root, text="Record")


#this frame holds the fields
fields_frame = LabelFrame(data_frame)
fields_frame.pack(side=LEFT)


# this frame holds the related records
related_frame = Frame(data_frame)
related_frame.pack(side=RIGHT)

# related_frame.pack(side=RIGHT)

# create a treeview scrollbar
related_scroll = Scrollbar(related_frame)
related_scroll.pack(side=RIGHT, fill=Y)

# Create the treeview
related_tree = ttk.Treeview(
    related_frame, yscrollcommand=tree_scroll.set, selectmode="extended"
)

related_tree.pack(side=RIGHT)

# configure scrollbar
related_scroll.config(command=my_tree.yview)

# get db tables
from functions.database_ops import *

active_table_name: str = "studies"

r_tbl_name: str = "study_organisations"

active_table: pd.DataFrame = pullTable(active_table_name)

r_tbl: pd.DataFrame = pullTable(r_tbl_name)

# configure the treeview
from functions.treeview import *

configureTree(my_tree, active_table)
configureTree(related_tree, r_tbl)



# building boxes dynamically

from functions.record_selection import *

bxs = []
for n, b in enumerate(my_tree["columns"]):
    b = Entry(fields_frame)
    bxs.append(b)


lbls = []
for n, l in enumerate(my_tree["columns"]):
    l = Label(fields_frame, text=l)
    lbls.append(l)


tbl_columns = list(active_table.columns)


# double click to select. 
def onDouble(selected):
    insertValuesToBox(my_tree, lbls, bxs, data_frame, fields_frame)


def onReturn(selected):
    save(my_tree, bxs, active_table_name, data_frame, fields_frame)


my_tree.bind("<Double-1>", onDouble)
root.bind("<Return>", onReturn)


# adding buttons

select_record_button = Button(
    button_frame,
    text="Select Record",
    command=lambda: insertValuesToBox(my_tree, lbls, bxs, data_frame, fields_frame),
)
select_record_button.grid(row=0, column=1, padx=10, pady=10)

create_new_record_button = Button(
    button_frame,
    text="Create New Record",
    command=lambda: createNewRecordFrame(data_frame, fields_frame, bxs, lbls),
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
    fields_frame,
    text="Save to Database",
    command=lambda: save(my_tree, bxs, active_table_name, fields_frame),
)
save_button.grid(row=len(bxs) + 1, column=2, padx=10, pady=10)

root.mainloop()
