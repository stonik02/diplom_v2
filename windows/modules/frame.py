from tkinter import Frame


class MyFrame:
    def __init__(self, master, height, width, relief, borderwidth):
        if height != 0 and width != 0 and relief != 0 and borderwidth != 0:
            self.root = Frame(master=master,
                              padx=5,
                              pady=5,
                              height=height,
                              width=width,
                              relief=relief,
                              borderwidth=borderwidth
                              )
            print("1")
        else:
            if relief != 0 and borderwidth != 0:
                self.root = Frame(master=master,
                                  height=height,
                                  width=width,
                                  relief=relief,
                                  borderwidth=borderwidth
                                  )
                print("2")

            else:
                if height != 0 and width != 0:
                    self.root = Frame(master=master,
                                      padx=5,
                                      pady=5,
                                      height=height,
                                      width=width
                                      )
                    print("3")

                else:
                    self.root = Frame(master=master,
                                     padx=5,
                                     pady=5
                                     )
                    print("4")



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

    def grid(self, row, column, pady, padx):
        self.root.grid(
            row=row,
            column=column,
            pady=pady,
            padx=padx
        )

    def pack_propagate(self, boolean):
        self.root.pack_propagate(boolean)
