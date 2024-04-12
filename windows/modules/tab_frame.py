from tkinter import LabelFrame, SOLID, BOTH, ttk


class TabFrame:
    def __init__(self, master):
        self.root = ttk.Frame(
            master=master,
        )

    def pack(self):
        self.root.pack(
            fill=BOTH,
            expand=True
        )

    def place(self, relx, rely):
        self.root.place(
            relx=relx,
            rely=rely
        )
