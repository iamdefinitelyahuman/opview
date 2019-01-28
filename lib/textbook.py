#!/usr/bin/python3

import os
import json
import sys
import time
import tkinter as tk
import tkinter.font as tkFont
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk


class TextBook(ttk.Notebook):

    def __init__(self, root):
        super().__init__(root)
        self._parent = root
        self.configure(padding=0)
        self._frames = {}
        root.bind("<Left>", self.key_left)
        root.bind("<Right>", self.key_right)

    def add(self, text, label):
        frame = TextBox(self, text, width=90, height=35)
        super().add(frame, text="   {}   ".format(label))
        frame._id = len(self._frames)
        frame._label = label
        self._frames[label] = frame

    def active_frame(self):
        id_ = self.index(self.select())
        return next(v for v in self._frames.values() if v._id == id_)

    def is_active(self, label):
        if self.index(self.select()) == self._frames[label]._id:
            return True
        return False
    
    def set_active(self, label):
        self.select(self._frames[label])

    def key_left(self, event):
        try:
            self.select(self.index(self.select())-1)
        except:
            self.select(len(self._frames)-1)

    def key_right(self, event):
        try: 
            self.select(self.index(self.select())+1)
        except:
            self.select(0)

    def _search(self, event):
        frame = self.active_frame()
        tree = self._parent.tree
        if not frame.tag_ranges('sel'):
            tree.clear_selection()
            return
        start, stop = [frame._coord_to_offset(i.string) for i in frame.tag_ranges('sel')]
        pc = [
            k for k,v in self._parent.pcMap.items() if 
            v['contract'] and frame._label in v['contract'] and
            start >= v['start'] and stop <= v['stop']
        ]
        if not pc:
            frame.clear_highlight()
            tree.clear_selection()
            return
        def key(k):
            return (
                (start - self._parent.pcMap[k]['start']) + 
                (self._parent.pcMap[k]['stop'] - stop)
            )
        id_ = sorted(pc, key=key)[0]
        tree.selection_set(id_)


class TextBox(ScrolledText):

    def __init__(self, root, text, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.insert(1.0, text)
        self['state'] = "disabled"
        self.config(
            font=("Courier", 14),
            background="#383838",
            foreground="#ECECEC",
            selectforeground="white",
            selectbackground="#4a6984",
            inactiveselectbackground="#4a6984",
            tabs=tkFont.Font(font=self['font']).measure('    '),
            wrap="none"
        )
        self.bind('<ButtonRelease-1>', root._search)

    def clear_highlight(self):
        self.tag_remove("sel", 1.0, "end")

    def highlight(self, start, end):
        self.clear_highlight()
        start = self._offset_to_coord(start)
        end = self._offset_to_coord(end)
        self.tag_add("sel", start, end)
        if start != end:
            self.see(end)
            self.see(start)

    def _offset_to_coord(self, value):
        text = self.get(1.0, "end")
        line = text[:value].count('\n') + 1
        offset = len(text[:value].split('\n')[-1])
        return "{}.{}".format(line, offset)

    def _coord_to_offset(self, value):
        row, col = [int(i) for i in value.split('.')]
        text = self.get(1.0, "end").split('\n')
        return sum(len(i)+1 for i in text[:row-1])+col