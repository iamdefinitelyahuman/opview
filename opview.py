#!/usr/bin/python3

import os
import json
import sys
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk


class TextBox(ScrolledText):

    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['state'] = "disabled"
        self.config(
            font=("Courier", 14),
            background="#383838",
            foreground="#ECECEC",
            selectforeground="white",
            selectbackground="#4a6984",
            inactiveselectbackground="#4a6984"
        )
        self.bind('<ButtonRelease-1>', self._search)

    def set_text(self, text):
        self['state'] = "normal"
        self.delete(1.0, "end")
        self.insert(1.0, text)
        self['state'] = "disabled"

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
    
    def _search(self, event):
        if not self.tag_ranges('sel'):
            tree.clear_selection()
            return
        start, stop = [self._coord_to_offset(i.string) for i in self.tag_ranges('sel')]
        pc = [k for k,v in pcMap.items() if 
            v['contract'] and self._label in v['contract'] and
            start >= v['start'] and stop <= v['stop']
        ]
        if not pc:
            self.clear_highlight()
            tree.clear_selection()
            return
        id_ = sorted(
            pc,
            key=lambda k: (start-pcMap[k]['start'])+(pcMap[k]['stop']-stop)
        )[0]
        tree.see(id_)
        tree.selection_set(id_)




class ListView(ttk.Treeview):

    def __init__(self, root, columns, **kwargs):
        self._last = ''
        self._frame = tk.Frame(root)
        super().__init__(
            self._frame,
            columns=[i[0] for i in columns[1:]],
            selectmode="browse",
            **kwargs
        )
        super().pack(side="left")
        self.heading("#0", text=columns[0][0])
        self.column("#0", width=columns[0][1])
        for tag, width in columns[1:]:
            self.heading(tag, text=tag)
            self.column(tag, width=width)

        scroll=tk.Scrollbar(self._frame)
        scroll.pack(side="right", fill="y")
        self.configure(yscrollcommand=scroll.set)
        scroll.configure(command=self.yview)
        self.bind("<<TreeviewSelect>>", self._select_bind)
        self.tag_configure("NoSource", background='#272727')

    def pack(self, *args, **kwargs):
        self._frame.pack(*args, **kwargs)

    def insert(self, values, tags=[]):
        super().insert(
            '',
            'end',
            iid=values[0],
            text=values[0],
            values=values[1:],
            tags=tags
        )

    def clear_selection(self):
        self.selection_remove(self.selection())
    
    def _select_bind(self, event):
        self.tag_configure(self._last, background='')
        if not self.selection():
            return
        pc = self.selection()[0]
        tag = self.item(pc, 'tags')[0]
        if tag == "NoSource":
            note.active_frame().clear_highlight()
            return
        self.tag_configure(tag, background='#2a4864')
        self._last = tag
        if pc == "I001":
            pc = "0"
        if not pcMap[pc]['contract']:
            note.active_frame().clear_highlight()
            return
        note.set_active(pcMap[pc]['contract'].split('/')[-1])
        note.active_frame().highlight(pcMap[pc]['start'],pcMap[pc]['stop'])


class Notebook(ttk.Notebook):
    
    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent
        self.configure(padding=0)
        self._frames = {}
        parent.bind("<Left>", self.key_left)
        parent.bind("<Right>", self.key_right)
    
    def add(self, text, label):
        frame = TextBox(self, width=90, height=35)
        frame.set_text(text)
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


root = tk.Tk(className="Opcode Viewer - {}".format(sys.argv[-1]))
root.bind("<Escape>", lambda k: root.quit())

note = Notebook(root)
note.pack(side="left")

tree = ListView(root, (("pc", 80), ("opcode", 200)), height=30)
tree.pack(side="right")

style = ttk.Style()
style.configure(
    "Treeview",
    background="#383838",
    foreground="#ECECEC",
    font=(None, 16),
    rowheight=22
)
style.configure(
    "Treeview.Heading",
    background="#272727",
    foreground="#ECECEC",
    font=(None, 16)
)
style.configure("TNotebook", background="#272727")
style.configure("TNotebook.Tab", background="#272727", foreground="#a9a9a9")
style.map(
    "TNotebook.Tab",
    background=[("active","#383838"), ("selected","#383838")],
    foreground=[("active","#ECECEC"), ("selected","#ECECEC")]
)

compiled = json.load(open("build/contracts/"+sys.argv[-1]+".json"))

for contract in sorted(set(i['contract'] for i in compiled['pcMap'] if i['contract'])):
    code = open(contract, 'r').read()
    note.add(code, contract.rsplit('/')[-1])

first = compiled['pcMap'][0].copy()
for op in compiled['pcMap']:
    if (
        op['contract'] == first['contract'] and
        op['start'] == first['start'] and
        op['stop'] == first['stop']
    ):
        op['contract'] = None
    if op['contract']:
        tag = "{0[start]}:{0[stop]}:{0[contract]}".format(op)
    else:
        tag = "NoSource"
    tree.insert([op['pc'], op['op']], [tag])


pcMap = dict((str(i.pop('pc')), i) for i in compiled['pcMap'])

root.mainloop()

