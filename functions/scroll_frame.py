from tkinter import *

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

def onMousewheel(event, canvas):
    canvas.yview_scroll(-1*(event.delta), "units")