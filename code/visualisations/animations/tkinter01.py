import tkinter as tk
from tkinter import *
from tkinter import ttk
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
#root.mainloop()
# window = tk.Tk()
# greeting = tk.Label(text="Hello, Tkinter")
# #greeting.pack()
# window.mainloop()

import sys
import os
from tkinter import *

window=Tk()

window.title("Running Python Script")
window.geometry('200x200+900+500')

def run():
    os.system('./anim_showcase2.py')

btn = Button(window, text="Click Me", bg="black", fg="blue",command=run)

btn.pack()
#btn.grid(column=0, row=0)

window.mainloop()