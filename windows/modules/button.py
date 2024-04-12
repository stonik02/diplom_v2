from tkinter import Button


class MyButton():
    def __init__(self, master, text, command, width, height):
        self.root = Button(
            master=master,
            text=text,
            command=command,
            width=width,
            height=height
        )

    def grid(self, row, column, padx, pady, sticky):
        self.root.grid(
            row=row,
            column=column,
            padx=padx,
            pady=pady,
            sticky=sticky
        )