#!/usr/bin/python3

import json
import sys
import tkinter as tk


from lib.listview import ListView
from lib.textbook import TextBook

class Root(tk.Tk):
    
    def __init__(self):
        super().__init__(className="Opcode Viewer - {}".format(sys.argv[-1]))
        self.bind("<Escape>", lambda k: self.quit())

        self.note = TextBook(self)
        self.note.pack(side="left")

        self.tree = ListView(self, (("pc", 80), ("opcode", 200)), height=30)
        self.tree.pack(side="right")

        compiled = json.load(open("build/contracts/"+sys.argv[-1]+".json"))
        for contract in sorted(set(
            i['contract'] for i in compiled['pcMap'] if i['contract']
        )):
            code = open(contract, 'r').read()
            self.note.add(code, contract.rsplit('/')[-1])

        first = compiled['pcMap'][0].copy()
        self.note.set_active(first['contract'].rsplit('/')[-1])
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
            self.tree.insert([str(op['pc']), op['op']], [tag, op['op']])

        self.pcMap = dict((str(i.pop('pc')), i) for i in compiled['pcMap'])
        
