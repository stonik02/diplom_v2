from tkinter import LabelFrame, SOLID


class FrLabel:
    def __init__(self, master, width, height, text):
        self.root = LabelFrame(
            master=master,
            width=width,
            height=height,
            borderwidth=1,
            relief=SOLID,
            padx=5,
            pady=5,
            text=text
        )

    def pack(self, side, padx, pady):
        self.root.pack(
            side=side,
            padx=padx,
            pady=pady
        )

    def place(self, relx, rely):
        self.root.place(
            relx=relx,
            rely=rely
        )

    def pack_propagate(self, boolean):
        self.root.pack_propagate(boolean)

    def grid_propagate(self, boolean):
        self.root.grid_propagate(boolean)
