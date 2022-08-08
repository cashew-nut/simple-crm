
select_record = '''
    
selected = my_tree.focus()

values = my_tree.item(selected, 'values')

n = 0

for item in my_tree['columns']:
    lbl = Label(data_frame, text=item)
    lbl.grid(row=n, column=1, padx=10, pady=10)
    lbls.append(lbl)
    box = Entry(data_frame)
    box.grid(row=n, column=2, padx=10, pady=10)
    box.delete(0,END)
    box.insert(0,values[n])
    boxes.append(box)
    n += 1
'''

# def sr_1(tree, frame, lbls, boxes):

#     selected = tree.focus()

#     values = tree.item(selected, 'values')

#     n = 0

#     lbls = []
#     boxes = []
#     columns = tree['columns']

#     for item in columns:
#         lbl = Label(frame, text=item)
#         lbl.grid(row=n, column=1, padx=10, pady=10)
#         lbls.append(lbl)
#         box = Entry(frame)
#         box.grid(row=n, column=2, padx=10, pady=10)
#         box.delete(0,END)
#         box.insert(0,values[n])
#         boxes.append(box)
#         n += 1