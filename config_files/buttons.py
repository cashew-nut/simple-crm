# from tkinter import *
# from functions.record_selection import *
# from config_files.frames import my_tree, fields_frame, data_frame, related_tree, button_frame
# import config_files.tables as tb
# from functions.treeview import configureRelatedTree

# bxs = []

# for n, b in enumerate(my_tree["columns"]):
#     b = Entry(fields_frame)
#     bxs.append(b)


# lbls = []
# for n, l in enumerate(my_tree["columns"]):
#     l = Label(fields_frame, text=l)
#     lbls.append(l)

# select_record_button = Button(
#     button_frame,
#     text="Select Record",
#     command=lambda: insertValuesToBox(my_tree, lbls, bxs, data_frame, fields_frame),
# )


# create_new_record_button = Button(
#     button_frame,
#     text="Create New Record",
#     command=lambda: createNewRecordFrame(data_frame, fields_frame, bxs, lbls),
# )


# delete_record_button = Button(
#     button_frame,
#     text="Delete Record",
#     command=lambda: deleteRecord(my_tree, tb.active_table_name, bxs, data_frame),
# )


# clear_frame_button = Button(
#     button_frame,
#     text="Clear Frame",
#     command=lambda: clearFrame(data_frame),
# )


# save_button = Button(
#     fields_frame,
#     text="Save to Database",
#     command=lambda: save(my_tree, bxs, tb.active_table_name, fields_frame),
# )


# get_related_records = Button(
#     fields_frame,
#     text="Get related Records",
#     command=lambda: configureRelatedTree(related_tree, tb.r_tbl, "study_id", my_tree),
# )
