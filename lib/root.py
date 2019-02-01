#!/usr/bin/python3

import json

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

        self.combo = SelectContract(self, frame)
        self.combo.pack(side="top", expand="true", fill="x")

        self._show_coverage = False
        self.bind("c", self._toggle_coverage)


    def _toggle_coverage(self, event):
        active = self.combo.get()
        if not active:
            return
        try:
            coverage = json.load(open("build/coverage.json"))[active]
        except FileNotFoundError:
            return
        if self._show_coverage:
            self.note.unmark_all('green', 'red', 'yellow', 'orange')
            self._show_coverage = False
            return
        self._show_coverage = True
        for i in coverage:
            label = i['contract'].split('/')[-1]
            if not i['count']:
                tag = "red"
            elif not i['jump'] or 0 not in i['jump']:
                tag = "green"
            elif i['jump'][0]:
                tag = "yellow"
            else:
                tag = "orange"
            self.note.mark(label, tag, i['start'], i['stop'])
