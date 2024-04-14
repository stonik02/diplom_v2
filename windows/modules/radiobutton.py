from tkinter import ttk


class MyRadioButton:
    def __init__(self, master, state, text, value, width, variable, command):
        self.root = ttk.Radiobutton(
            master=master,
            state=state,
            text=text,
            value=value,
            width=width,
            variable=variable,
            command=command
        )

    def grid(self, row, column, padx, pady, sticky):
        self.root.grid(
            row=row,
            column=column,
            padx=padx,
            pady=pady,
            sticky=sticky
        )