from tkinter import Tk

from windows.modules.Entry import MyEntry
from windows.modules.figure_canvas import MyFigureCanvas
from windows.modules.frame import MyFrame
from windows.modules.button import MyButton
from windows.modules.label import MyLabel
from windows.modules.radiobutton import MyRadioButton
from windows.modules.tabs_controller import TabsController
from windows.modules.tab_frame import TabFrame
from windows.modules.frame_label import FrLabel


class Window:
    def __init__(self, title):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry("1700x1000")
        # self.root.resizable(False, False)


    def run(self):
        self.root.mainloop()


    def create_label_frame(self, master, width, height, text):
        return FrLabel(master, width, height, text)

    def create_tab_frame(self, master):
        return TabFrame(master)

    def create_tabs_controller(self, master, width, height):
        return TabsController(master, width, height)



    def create_frame(self, master, height, width, relief, borderwidth):
        return MyFrame(master, height, width, relief, borderwidth)

    def create_button(self, master, text, command, width, height):
        return MyButton(master, text, command, width, height)

    def create_entry(self, master, width):
        return MyEntry(master, width)

    def create_label(self, master, text, font):
        return MyLabel(master, text, font)

    def create_figure_canvas(self, master, figure):
        return MyFigureCanvas(master, figure)

    def create_radiobutton(self, master, text, value, width, variable, command):
        return MyRadioButton(master,  text, value, width, variable, command)
