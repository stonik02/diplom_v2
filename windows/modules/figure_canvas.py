
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MyFigureCanvas:
    def __init__(self, master, figure):
        self.root = FigureCanvasTkAgg(
            figure,
            master
        )


    def draw(self):
        self.root.draw()

    def pack(self, expand, fill):
        self.root.get_tk_widget().pack(
            expand=expand,
            fill=fill
        )
    def destroy(self):
        self.root.get_tk_widget().destroy()