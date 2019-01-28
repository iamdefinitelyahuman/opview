#!/usr/bin/python3

from tkinter import ttk


def set_style():

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