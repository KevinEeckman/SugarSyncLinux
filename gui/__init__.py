from tkinter import *
from tkinter import ttk
import sugarsync


__author__ = 'kevin'


class Window(ttk.Frame):

    root = None

    def __init__(self):
        if not Window.root:
            Window.root = Tk()
        super().__init__(Window.root) # Creates self.master
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(self)
        self.tree.grid(column=1, row=2)
        # hellolabel = ttk.Label(self, text="Hello Tkinter!")
        # hellolabel.grid(column=1, row=1, sticky=EW)
        up_btn = ttk.Button(self, text="up", command=self.up)
        up_btn.grid(column=1, row=1)
        # hellolabel.bind('<Enter>', lambda e: hellolabel.configure(text='Moved mouse inside'))
        # hellolabel.bind('<Leave>', lambda e: hellolabel.configure(text='Moved mouse outside'))
        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.root_node=None

    def up(self):
        pass

    def init_tree(self, root_node):
        self.root_node=root_node
        for i in self.root_node:
            self.tree.insert('', 'end', '', text=i.name)