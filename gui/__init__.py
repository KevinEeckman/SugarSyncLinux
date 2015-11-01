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
        #super().__init__() # Creates self.master
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        #self.columnconfigure(0, weight=1)

        up_btn = ttk.Button(self, text="up", command=self.up)
        up_btn.grid(column=0, row=0,)

        self.tree = ttk.Treeview(self, columns='Type')
        self.tree.bind('<Double-1>', self.tree_item_clicked)
        self.tree.grid(column=0, row=1, sticky=(N, S, E, W))

        save_as_btn = ttk.Button(self, text="save as", command=self.save_as)
        save_as_btn.grid(column=0, row=2,)

        Window.root.columnconfigure(0, weight=1)
        Window.root.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)
        self.root_node=None

    def up(self):
        if self.root_node and self.root_node.parent:
            self.display_tree(self.root_node.parent)

    def save_as(self):
        pass

    def tree_item_clicked(self, event):
        uri = self.tree.focus()
        node = sugarsync.Resource.resources[uri]

        self.display_tree(node.contents)

    def display_tree(self, root_node):
        '''
        :param root_node: sugarsync.CollectionResource
        :return: None
        '''
        self.tree.delete(*self.tree.get_children())
        self.root_node=root_node
        for i in self.root_node:
            self.tree.insert('', 'end', i.uri, text=i.name, values=(i.__class__.__name__))