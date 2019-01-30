#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

from lib.listview import ListView
from lib.textbook import TextBook
from lib.select import SelectContract

class Root(tk.Tk):
    
    def __init__(self):
        super().__init__(className="Opcode Viewer")
        self.bind("<Escape>", lambda k: self.quit())

        self.note = TextBook(self)
        self.note.pack(side="left")

        frame = ttk.Frame(self)
        frame.pack(side="right", expand="true", fill="y")
        
        self.tree = ListView(self, frame, (("pc", 80), ("opcode", 200)), height=30)
        self.tree.pack(side="bottom")

        s = SelectContract(self, frame)
        s.pack(side="top")