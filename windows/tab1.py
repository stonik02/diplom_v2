from tkinter import SOLID, Label, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from function.function import main_function


class Tab1:
    def __init__(self, window, tabs_controller):
        self.window = window
        self.frame = self.window.create_tab_frame(tabs_controller.root)
        self.frame_canvas = None
        self.frame_description = None
        self.description = None
        self.canvas = None
        self.entry_num_rays = None
        self.entry_l_moda = None
        self.entry_inception = None
        self.entry_f = None
        self.entry_hk = None

    def pack(self):
        self.frame.pack()

        # # Создание canvas и графика

    def generate_scatter_chart(self, h_k, l_moda, f, inception, num_rays):
        lines, result_lych, y_min, distance_min = main_function(h_k, l_moda, f, inception, num_rays)
        if self.canvas:
            self.canvas.destroy()
        if self.description:
            self.description.destroy()
        fig = Figure(dpi=100)
        grafik = fig.add_subplot(111)
        for x, y in zip(lines[0], lines[1]):
            grafik.plot(x, y, color='black')
        if len(result_lych) == 3:
            x_coords = [coord for sublist in result_lych[0] for coord in sublist]
            y_coords = [coord for sublist in result_lych[1] for coord in sublist]
            grafik.plot(x_coords, y_coords, color='red', label='')
            grafik.scatter(inception[0], inception[1], color='green', label='Приемник')
        grafik.legend()

        self.canvas = self.window.create_figure_canvas(self.frame_canvas.root, fig)
        self.canvas.draw()
        self.canvas.pack(expand=True, fill="both")
        self.description = self.window.create_label(
            self.frame_description.root,
            text="1. Луч, выпущенный под {} градусов попадает в приемник. На графике он отображен {} цветом. \n\n"
                 "2. Лучи подходят к берегу на расстояние = {} метров. \n\n".format(
                int(result_lych[2] * 180 / 3.14), "Красным", int(distance_min), int(y_min)),
            font=("Arial Bold", 12)
        )

        self.description.pack()
        self.window.root.after(200, None)

    def draw_graph(self):
        try:
            l_moda = int(self.entry_l_moda.root.get())
        except ValueError:
            messagebox.showinfo('Неверное значение моды', 'Необходимо ввести число')
            return

        try:
            h_k = float(self.entry_hk.root.get())
        except ValueError:
            messagebox.showinfo('Неверное значение коэффициента глубины', 'Необходимо ввести дробное число')
            return

        try:
            num_rays = int(self.entry_num_rays.root.get())
            num_rays = num_rays * 2
        except ValueError:
            messagebox.showinfo('Неверное значение кол-ва лучей', 'Необходимо ввести число')
            return

        try:
            f = int(self.entry_f.root.get())
        except ValueError:
            messagebox.showinfo('Неверное значение частоты', 'Необходимо ввести число')
            return

        try:
            inception = self.entry_inception.root.get()
            inception_arr = [float(x) for x in inception.split(",")]

        except ValueError:
            messagebox.showinfo('Неверное значение координат приемника', 'Необходимо ввести числа в формате 1234, 4321')
            return

        if inception_arr[0] < 0 or inception_arr[1] < 0 or inception_arr[0] > 30000 or inception_arr[1] > 30000:
            messagebox.showinfo('Неверное значение координат приемника',
                                'Необходимо ввести неотрицательные числа в диапазоне 5000-30000')
            return

        if f > 10000 or f < 10:
            messagebox.showinfo('Неверное значение частоты', 'Необходимо ввести число в интервале 10-1000')
            return

        if l_moda > 6 or l_moda < 1:
            messagebox.showinfo('Неверное значение моды', 'Необходимо ввести число в интервале 1-6')
            return

        # Для отрисовки в половине графиков всех лучей мы их * 2
        if num_rays > 200 or num_rays < 60:
            messagebox.showinfo('Неверное значение кол-ва лучей', 'Необходимо ввести число в интервале 30-100')
            return

        if h_k > 1000 or h_k < 0.004:
            messagebox.showinfo('Неверное значение коэффициента глубины',
                                'Необходимо ввести число в интервале 0.002 - 1000')
            return

        self.generate_scatter_chart(h_k, l_moda, f, inception_arr, num_rays)

    #

    def clear_canvas(self):

        if self.canvas:
            self.canvas.destroy()
            self.canvas = self.window.create_figure_canvas(self.frame_canvas.root, None)

        if self.description:
            self.description.destroy()
            self.description = Label()

    def run(self):

        self.canvas = None
        self.description = None

        self.frame_main = self.window.create_label_frame(self.frame.root, height=800, width=1200, text='Траектория сигнала на определенной частоте')
        self.frame_main.place(relx=0.1, rely=0.06)

        # Создание фрейма для графика
        frame_canvas_description = self.window.create_frame(self.frame_main.root, height=0, width=0, relief=0, borderwidth=0)
        frame_canvas_description.pack(
            side='right',
            padx=20,
            pady=20
        )
        # frame_canvas_description.place(relx=0.40, rely=0.1)

        self.frame_canvas = self.window.create_label_frame(frame_canvas_description.root, width=600, height=500,
                                                           text='График')
        self.frame_canvas.pack(side='top', padx=20, pady=20)
        self.frame_canvas.pack_propagate(True)

        self.frame_description = self.window.create_label_frame(frame_canvas_description.root, width=700, height=150,
                                                                text='Описание')
        self.frame_description.pack(side='bottom', padx=20, pady=20)
        self.frame_description.pack_propagate(True)

        frame_buttons_entrys = self.window.create_frame(self.frame_main.root, height=0, width=0, relief=SOLID, borderwidth=1)
        frame_buttons_entrys.pack(
            side='left',
            padx=50,
            pady=20
        )
        # frame_buttons_entrys.place(relx=0.15, rely=0.3)
        # frame_buttons_text.pack_propagate(True)

        frame_entrys = self.window.create_frame(frame_buttons_entrys.root, height=450, width=40, relief=0,
                                                borderwidth=0)
        frame_entrys.grid(row=1, column=1, pady=0, padx=0)

        frame_buttons = self.window.create_frame(frame_buttons_entrys.root, height=450, width=40, relief=0,
                                                 borderwidth=0)
        frame_buttons.grid(row=2, column=1, pady=0, padx=0)



        btn_paint = self.window.create_button(master=frame_buttons.root, text='Отрисовать график',
                                              command=self.draw_graph, width=17, height=2)
        btn_paint.grid(row=0, column=0, padx=5, pady=0, sticky='nsew')

        btn_clear_canvas = self.window.create_button(master=frame_buttons.root, text='Очистить график',
                                                     command=self.clear_canvas, width=17, height=2)
        btn_clear_canvas.grid(row=0, column=1, padx=5, pady=0, sticky='nsew')

        label_f = self.window.create_label(frame_entrys.root, text="Укажите частоту, Гц", font=("Arial Bold", 12))
        label_f.grid(row=0, column=0, padx=5, pady=0, sticky="nsew")
        self.entry_f = self.window.create_entry(frame_entrys.root, width=10)
        self.entry_f.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        self.entry_f.insert(index=0, text='300')

        label_inception = self.window.create_label(frame_entrys.root, text="Укажите координаты приемника, м",
                                                   font=("Arial Bold", 12))
        label_inception.grid(row=1, column=0, padx=5, pady=0, sticky="nsew")
        self.entry_inception = self.window.create_entry(frame_entrys.root, width=15)
        self.entry_inception.grid(row=1, column=1, padx=5, pady=15, sticky="nsew")
        self.entry_inception.insert(index=0, text='2121, 7788')

        label_l_moda = self.window.create_label(frame_entrys.root, text="Укажите номер моды",
                                                font=("Arial Bold", 12))
        label_l_moda.grid(row=2, column=0, padx=5, pady=0, sticky="nsew")
        self.entry_l_moda = self.window.create_entry(frame_entrys.root, width=10)
        self.entry_l_moda.grid(row=2, column=1, padx=5, pady=15, sticky="nsew")
        self.entry_l_moda.insert(index=0, text='3')

        label_num_rays = self.window.create_label(frame_entrys.root, text="Укажите колличество лучей",
                                                  font=("Arial Bold", 12))
        label_num_rays.grid(row=3, column=0, padx=5, pady=0, sticky="nsew")
        self.entry_num_rays = self.window.create_entry(frame_entrys.root, width=12)
        self.entry_num_rays.grid(row=3, column=1, padx=5, pady=15, sticky="nsew")
        self.entry_num_rays.insert(index=0, text='50')

        label_hk = self.window.create_label(frame_entrys.root, text="Укажите коэффициент уклона дна",
                                            font=("Arial Bold", 12))
        label_hk.grid(row=4, column=0, padx=5, pady=0, sticky="nsew")
        self.entry_hk = self.window.create_entry(frame_entrys.root, width=10)
        self.entry_hk.grid(row=4, column=1, padx=5, pady=15, sticky="nsew")
        self.entry_hk.insert(index=0, text='0.03')
