from tkinter import ttk, Radiobutton


class MyRadioButton:
    def __init__(self, master, text, value, width, variable, command):
        self.root = Radiobutton(
            master=master,
            text=text,
            value=value,
            width=width,
            variable=variable,
            command=command,
            font=("Arial Bold", 11)
        )

    def grid(self, row, column, padx, pady, sticky):
        self.root.grid(
            row=row,
            column=column,
            padx=padx,
            pady=pady,
            sticky=sticky
        )