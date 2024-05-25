from tkinter import Entry


class MyEntry:
    def __init__(self, master, width):
        self.root = Entry(
            master,
            width=width,
            font=("Arial Bold", 12)
        )

    def grid(self, row, column, padx, pady, sticky):
        self.root.grid(
            row=row,
            column=column,
            padx=padx,
            pady=pady,
            sticky=sticky
        )

    def insert(self, index, text):
        self.root.insert(
            index=index,
            string=text
        )

    def destroy(self):
        self.root.destroy()