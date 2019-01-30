#!/usr/bin/python3

from tkinter import ttk


TEXT_STYLE = {
    'font':("Courier", 14),
    'background':"#383838",
    'foreground':"#ECECEC",
    'selectforeground':"white",
    'selectbackground':"#4a6984",
    'inactiveselectbackground':"#4a6984",
    'borderwidth': 1,
    'highlightthickness': 0,
}


def set_style():

    style = ttk.Style()
    style.configure(
        "Treeview",
        background="#383838",
        fieldbackground="#383838",
        foreground="#ECECEC",
        font=(None, 16),
        rowheight=21,
        borderwidth=1
    )
    style.configure(
        "Treeview.Heading",
        background="#161616",
        foreground="#ECECEC",
        borderwidth=0,
        font=(None, 16)
    )
    style.map(
        "Treeview.Heading",
        background=[("active","#383838"), ("selected","#383838")],
        foreground=[("active","#ECECEC"), ("selected","#ECECEC")]
    )
    style.configure("TNotebook", background="#161616")
    style.configure("TNotebook.Tab", background="#272727", foreground="#a9a9a9")
    style.map(
        "TNotebook.Tab",
        background=[("active","#383838"), ("selected","#383838")],
        foreground=[("active","#ECECEC"), ("selected","#ECECEC")]
    )
    style.configure(
        "TFrame",
        background="#161616",
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
        background=[('active', "#272727")]
    )
    style.layout(
        'Vertical.TScrollbar', 
        [(
            'Vertical.Scrollbar.trough',
            {
                'children':[(
                    'Vertical.Scrollbar.thumb',
                    {'expand': '1', 'sticky': 'nswe'}
                )],
                'sticky': 'ns'
            }
        )]
    )