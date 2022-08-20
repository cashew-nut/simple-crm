from tkinter import *
import tkinter


def openNewWindow(title: str, subtitle: str, root_w):

    # Toplevel object which will
    # be treated as a new window
    new_window = Toplevel(root_w)

    # sets the title of the
    # Toplevel widget
    new_window.title("New Window")

    # sets the geometry of toplevel
    new_window.geometry("600x400")

    # A Label widget to show in toplevel
    Label(new_window, text=title).pack()

    record_frame = LabelFrame(new_window, text=subtitle)
    record_frame.pack(fill="x", expand="yes", padx=20)

    return record_frame
