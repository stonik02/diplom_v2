
import tkinter.ttk
from tkinter import BOTH


class TabsController:
    def __init__(self, master, width, height):
        self.root = tkinter.ttk.Notebook(
            master,
            height=width,
            width=height
        )

    def pack(self):
        self.root.pack(
            expand=True,
            fill=BOTH,
            padx=10,
            pady=5
        )

    def add(self, child, name):
        self.root.add(child, text=name)