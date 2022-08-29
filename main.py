from tkinter import *
from tkinter import ttk
from functions.treeview import *
from functions.database_ops import *
from functions.record_selection import *
from config_files.tables import active_table_name, r_tbl_name
from functions.scroll_frame import ScrollbarFrame
import pandas as pd


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


# main frames

top_frame = Frame(root)
top_frame.pack(side=TOP, fill=Y, pady=10)



# Create a treeview Frame
tree_frame = Frame(top_frame)
tree_frame.pack(fill=Y, pady=10)

query_frame = LabelFrame(top_frame, text="Filter")
query_frame.pack(fill=X)

select_entry = Entry(query_frame, width=50)
select_entry.insert(END, '*')
select_entry.grid(row=1, column=2, padx=10, pady=5)
select_label = Label(query_frame, text='SELECT')
select_label.grid(row=1, column=1, padx=10, pady=5)

where_entry = Entry(query_frame, width=50)
where_entry.grid(row=2, column=2, padx=10, pady=5)
where_label = Label(query_frame, text='WHERE')
where_label.grid(row=2, column=1, padx=10, pady=5)


button_frame = LabelFrame(top_frame, text="Commands")
button_frame.pack(fill=X, expand="yes", padx=0.5)


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

# this frame holds all the fields for individaul records and related records


data_frame = LabelFrame(root, text="Record")

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = Canvas(data_frame, borderwidth=0)
inner_df = Frame(data_frame)
tab_control = ttk.Notebook(inner_df)
record_details = Frame(tab_control)
related_objects = Frame(tab_control)


vsb = Scrollbar(data_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0,0), window=inner_df, anchor="nw")

data_frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))


tab_control.add(record_details, text = 'Record Details')
tab_control.add(related_objects, text = 'Related Objects')
tab_control.pack(expand=True, fill=BOTH)

r_parent_frame = Frame(related_objects)
r_parent_frame.pack()

r_button_frame = LabelFrame(r_parent_frame)
r_button_frame.pack()

# this frame holds the related records
r_tree_frame = Frame(r_parent_frame)
r_tree_frame.pack(side=LEFT, fill=BOTH)

r_fields_frame = LabelFrame(r_parent_frame)
r_fields_frame.pack(side=RIGHT, fill=BOTH)



# this frame holds the fields
fields_frame = LabelFrame(record_details)
fields_frame.pack()




# create a treeview scrollbar
related_scroll = Scrollbar(r_tree_frame)


# Create the treeview
related_tree = ttk.Treeview(
    r_tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended"
)

related_scroll.pack(side=RIGHT)
# configure scrollbar
related_scroll.config(command=related_tree.yview)





#pull the tables

active_table: pd.DataFrame = pullTable(active_table_name)
r_tbl: pd.DataFrame = pullTable(r_tbl_name)
r_tbl_ls: list = relatedTableNames(active_table_name, config.schema)


# adding buttons

configureTree(my_tree, active_table)


bxs = []

for n, b in enumerate(my_tree["columns"]):
    b = Entry(fields_frame)
    bxs.append(b)


lbls = []
for n, l in enumerate(my_tree["columns"]):
    l = Label(fields_frame, text=l)
    lbls.append(l)


r_bxs = []
for n, b in enumerate(r_tbl.columns): #using columns won't work since this needs to be dynamic
    b = Entry(r_fields_frame)
    r_bxs.append(b)


r_lbls = []
for n, l in enumerate(r_tbl.columns):
    l = Label(r_fields_frame, text=l)
    r_lbls.append(l)

positionRecordLabels(r_lbls)
positionRecordBoxes(r_bxs)

r_buttons = []
for n, b in enumerate(r_tbl_ls):
    b = Button(r_button_frame, text=b,
    command=lambda: configureRelatedTree(related_tree, r_tbl, "study_id", my_tree))
    r_buttons.append(b)
    

positionRelatedButtons(r_buttons)



# double click to select.
def onDouble(selected):
    insertValuesToBox(my_tree, lbls, bxs, data_frame, fields_frame)

def onDoubleRelated(selected):
    insertValuesToBox(related_tree, r_lbls, r_bxs, r_parent_frame, r_fields_frame)

def onReturn(selected):
    save(my_tree, bxs, active_table_name, data_frame, fields_frame)

def onReturnFilter(selected):
    filterTable(data_frame, my_tree, bxs, select_entry, where_entry)


my_tree.bind("<Double-1>", onDouble)
related_tree.bind("<Double-1>", onDoubleRelated)
fields_frame.bind("<Return>", onReturn)
where_entry.bind("<Return>", onReturnFilter)
select_entry.bind("<Return>", onReturnFilter)

clear_filter_button  = Button(
    button_frame,
    text='Clear Filter',
    command=lambda: refreshAfterUpdate(data_frame, my_tree, bxs, ct.query)
)


select_record_button = Button(
    button_frame,
    text="Select Record",
    command=lambda: insertValuesToBox(my_tree, lbls, bxs, data_frame, fields_frame),
)


create_new_record_button = Button(
    button_frame,
    text="Create New Record",
    command=lambda: createNewRecordFrame(data_frame, fields_frame, bxs, lbls),
)


delete_record_button = Button(
    button_frame,
    text="Delete Record",
    command=lambda: deleteRecord(my_tree, active_table_name, bxs, data_frame),
)


clear_frame_button = Button(
    button_frame,
    text="Clear Frame",
    command=lambda: clearFrame(data_frame),
)


save_button = Button(
    fields_frame,
    text="Save to Database",
    command=lambda: save(my_tree, bxs, active_table_name, fields_frame),
)


select_record_button.grid(row=0, column=1, padx=10, pady=10)

create_new_record_button.grid(row=0, column=2, padx=10, pady=10)

delete_record_button.grid(row=0, column=3, padx=10, pady=10)

clear_frame_button.grid(row=0, column=4, padx=10, pady=10)

save_button.grid(row=len(bxs) + 1, column=2, padx=10, pady=10)

clear_filter_button.grid(row=0, column = 5, padx=10, pady=10)

root.mainloop()
