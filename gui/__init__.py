from tkinter import *
from tkinter import ttk
import sugarsync


__author__ = 'kevin'

root = None

class LoginWindow(ttk.Frame):

    def __init__(self):
        global root
        if not root:
            root = Tk()
        super().__init__(root) # Creates self.master
        self.grid(column=0, row=0, sticky=(N, S, E, W))

        label_login = ttk.Label(self, text='Login:')
        label_password = ttk.Label(self, text='Login:')

        login = StringVar()
        entry_login = ttk.Entry(self, textvariable=login)

        password = StringVar()
        entry_password = ttk.Entry(self, textvariable=password, show='*')

        rem_credentials = StringVar()
        rem_credentials.set("0")
        chk_remember = ttk.Checkbutton(self, text='Remember credentials', variable=rem_credentials)

        btn_ok = ttk.Button(self, text="Login", command=self.login)

        label_login.grid(column=0, row=0, sticky=(N, S, E, W))
        label_password.grid(column=0, row=1, sticky=(N, S, E, W))
        entry_login.grid(column=1, row=0, sticky=(N, S, E, W))
        entry_password.grid(column=1, row=1, sticky=(N, S, E, W))
        chk_remember.grid(column=1, row=3, columnspan=2, sticky=(N, S, E, W))
        btn_ok.grid(column=2, row=4, sticky=(S, E))

    def login(self):
        pass


class MainWindow(ttk.Frame):

    def __init__(self):
        global root
        if not root:
            root = Tk()
        super().__init__(root) # Creates self.master
        #super().__init__() # Creates self.master
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        # self.columnconfigure(0, weight=1)

        up_btn = ttk.Button(self, text="up", command=self.up)
        up_btn.grid(column=0, row=0,)

        self.tree = ttk.Treeview(self, columns='Type')
        self.tree.bind('<Double-1>', self.tree_item_clicked)
        self.tree.grid(column=0, row=1, sticky=(N, S, E, W))

        save_as_btn = ttk.Button(self, text="save as", command=self.save_as)
        save_as_btn.grid(column=0, row=2,)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
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