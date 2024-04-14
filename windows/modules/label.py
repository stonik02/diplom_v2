from tkinter import Entry, Label


class MyLabel:
    def __init__(self, master, text, font):
        self.root = Label(
            master,
            text=text,
            font=font
        )


    def grid(self, row, column, padx, pady, sticky):
        self.root.grid(
            row=row,
            column=column,
            padx=padx,
            pady=pady,
            sticky=sticky
        )

    def pack(self):
        self.root.pack()

    def destroy(self):
        self.root.destroy()