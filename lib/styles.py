#!/usr/bin/python3

from tkinter import ttk


TEXT_STYLE = {
    'font':("Courier", 14),
    'background':"#383838",
    'foreground':"#ECECEC",
    'selectforeground':"white",
    'selectbackground':"#4a6984",
    'inactiveselectbackground':"#4a6984",
}


def set_style():

    style = ttk.Style()
    style.configure(
        "Treeview",
        background="#383838",
        fieldbackground="#383838",
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
    style.configure(
        "TFrame",
        background="#272727",
        foreground="#ECECEC",
    )
    style.configure("TScrollbar",
        background="#272727",
        troughcolor="#383838",
        width=24,
        arrowsize=16,
        relief="flat",
        borderwidth=0,
        arrowcolor="#a9a9a9"
    )
    style.map(
        "TScrollbar",
        background=[('active', "#383838")]
    )