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
            font=(None, 14),
            background="#383838",
            foreground="#ECECEC",
            selectforeground="white",
            selectbackground="#4a6984",
            inactiveselectbackground="#4a6984"
        )
    
    def set_text(self, text):
        self['state'] = "normal"
        self.delete(1.0, "end")
        self.insert(1.0, text)
        self['state'] = "disabled"

    def clear_highlight(self):
        self.tag_remove("sel", 1.0, "end")
    
    def highlight(self, start, end):
        self.clear_highlight()
        start = self._offset(start)
        end = self._offset(end)
        self.tag_add("sel", start, end)
        self.see(start)
        self.see(end)
        

    def _offset(self, value):
        text = self.get(1.0, "end")
        line = text[:value].count('\n') + 1
        offset = len(text[:value].split('\n')[-1])
        return "{}.{}".format(line, offset)


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
        scroll.pack(side="right",fill="y")
        self.configure(yscrollcommand=scroll.set)
        scroll.configure(command=self.yview)
        self.bind("<<TreeviewSelect>>",self._select_bind)

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

    def _select_bind(self, event):
        pc = self.selection()[0]
        tag = self.item(pc,'tags')[0]
        self.tag_configure(self._last, background='')
        self.tag_configure(tag, background='#2a4864')
        self._last = tag
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

tree = ListView(root, (("pc",80), ("opcode", 200)), height=30)
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
    code = open(contract,'r').read()
    note.add(code, contract.rsplit('/')[-1])

for op in compiled['pcMap']:
    tree.insert([op['pc'], op['op']], ["{0[start]}:{0[stop]}:{0[contract]}".format(op)])

pcMap = dict((str(i.pop('pc')), i) for i in compiled['pcMap'])

root.mainloop()

