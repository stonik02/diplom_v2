from tkinter import SOLID, messagebox, StringVar

import numpy as np
from matplotlib.figure import Figure

from function.test_func import main_func


class Tab2:
    def __init__(self, window, tabs_controller):
        self.window = window
        self.frame = self.window.create_tab_frame(tabs_controller.root)
        self.selected_signals = None
        self.entry_f1 = None
        self.entry_f2 = None

    def pack(self):
        self.frame.pack()



    def take_values(self):
        try:
            l_moda = int(self.entry_l_moda.root.get())
        except ValueError:
            messagebox.showinfo('Неверное значение моды', 'Необходимо ввести число')
            return
        try:
            h_k = float(self.entry_hk.root.get())
        except:
            messagebox.showinfo('Неверное значение коэффициента глубины', 'Необходимо ввести число')
            return
        try:
            duration = float(self.entry_duration.root.get())
        except:
            messagebox.showinfo('Неверное значение длительности сигнала', 'Необходимо ввести число')
            return
        try:
            recevier = self.entry_receiver.root.get()
            receiver_arr = [float(x) for x in recevier.split(",")]
        except ValueError:
            messagebox.showinfo('Неверное значение координат приемника',
                                'Необходимо ввести числа в формате 1234, 4321')
            return
        try:
            inceprion = self.entry_inception.root.get()
            inceprion_arr = [float(x) for x in inceprion.split(",")]
        except ValueError:
            messagebox.showinfo('Неверное значение координат источника',
                                'Необходимо ввести числа в формате 1234, 4321')
            return
        try:
            signal_type = self.selected_signals.get()
            if signal_type == '':
                messagebox.showinfo('Неверный тип сигнала', 'Необходимо выбрать тип сигнала')
                return
        except:
            messagebox.showinfo('Неверный тип сигнала', 'Необходимо выбрать тип сигнала')
            return
        try:
            f1 = 0
            f2 = 0
            print(signal_type)
            if signal_type == 'sin':
                f1 = int(self.entry_f1.root.get())
                print(f1)
                f2 = 0
            if signal_type == 'chirp':
                f1 = int(self.entry_f1.root.get())
                f2 = int(self.entry_f2.root.get())
        except:
            messagebox.showinfo('Неверная частота', 'Необходимо ввести целое число')
            return

        return l_moda, h_k, duration, receiver_arr, signal_type, inceprion_arr, f1, f2


    def validate_values(self, l_moda, h_k, duration, receiver, signal_type, inception, f1, f2):
        if l_moda > 6 or l_moda < 1:
            messagebox.showinfo('Неверное значение моды', 'Необходимо ввести число в интервале 1-7')
            return 1

        if h_k > 1000 or h_k < 0.004:
            messagebox.showinfo('Неверное значение коэффициента глубины',
                                'Необходимо ввести число в интервале 0.004 - 1000')
            return 1

        if duration > 5 or duration < 0.1:
            messagebox.showinfo('Неверное значение длительности сигнала',
                                'Необходимо ввести число в интервале 0.1 - 5')
            return 1

        if receiver[0] < 0 or receiver[1] < 0 or receiver[0] > 30000 or receiver[1] > 30000:
            messagebox.showinfo('Неверное значение координат приемника',
                                'Необходимо ввести неотрицательные числа в диапазоне 0-30000')
            return 1

        if inception[0] < 0 or inception[1] < 0 or inception[0] > 30000 or inception[1] > 30000:
            messagebox.showinfo('Неверное значение координат приемника',
                                'Необходимо ввести неотрицательные числа в диапазоне 0-30000')
            return 1

        if signal_type != 'sin' and signal_type != 'chirp':
            messagebox.showinfo('Непредвиденная ошибка',
                                'Ошибка выбора типа сигнала')
            return 1

        if signal_type == 'sin':
            if f1 > 5000 or f1 < 10:
                messagebox.showinfo('Неверное значение частоты',
                                    'Необходимо ввести число в диапазоне 10-5000')
                return 1
        if signal_type == 'chirp':
            if f1 > 5000 or f1 < 1:
                messagebox.showinfo('Неверное значение начальной частоты',
                                    'Необходимо ввести число в диапазоне 1-5000')
                return 1
            if f2 > 5000 or f2 < 10:
                messagebox.showinfo('Неверное значение конечной частоты',
                                    'Необходимо ввести число в диапазоне 10-5000')
                return 1

        return 0




    def generate_scatter_chart(self):
        try:
            l_moda, h_k, duration, receiver, signal_type, inception, f1, f2 = self.take_values()
        except:
            return

        validate = self.validate_values(l_moda, h_k, duration, receiver, signal_type, inception, f1, f2)
        if validate == 1:
            return

        signal_arr, signal_on_receiver, t_arr, lines, l_arr, fi_wk_res, wk_arr, t = main_func(h_k, l_moda, signal_type, receiver, inception, f1, f2, duration)

        if self.canvas_receiver:
            self.canvas_receiver.destroy()
        if self.canvas_inception:
            self.canvas_inception.destroy()
        fig_inception = Figure(dpi=100)
        fig_receiver = Figure(dpi=100)
        grafik_inception = fig_inception.add_subplot(111)
        grafik_receiver = fig_receiver.add_subplot(111)


        grafik_inception.plot(t_arr, signal_arr)
        grafik_inception.set_xlabel("t")
        grafik_inception.set_ylabel("s")
        grafik_inception.set_xticks(np.arange(0, max(t_arr), 0.2))
        grafik_inception.grid(True)

        grafik_receiver.plot(t_arr, signal_on_receiver)
        grafik_receiver.set_xlabel("t")
        grafik_receiver.set_ylabel("s")
        grafik_receiver.set_xticks(np.arange(0, max(t_arr), 0.2))
        grafik_receiver.grid(True)

        self.canvas_inception = self.window.create_figure_canvas(self.frame_canvas_inception.root, fig_inception)
        self.canvas_receiver = self.window.create_figure_canvas(self.frame_canvas_receiver.root, fig_receiver)

        self.canvas_inception.draw()
        self.canvas_inception.pack(expand=True, fill="both")


        self.canvas_receiver.draw()
        self.canvas_receiver.pack(expand=True, fill="both")

        self.window.root.after(200, None)


    def clear_canvas(self):

        if self.canvas_receiver:
            self.canvas_receiver.destroy()
            self.canvas_receiver = self.window.create_figure_canvas(self.frame_canvas_receiver.root, None)
        if self.canvas_inception:
            self.canvas_inception.destroy()
            self.canvas_inception = self.window.create_figure_canvas(self.frame_canvas_inception.root, None)

    def view_entry_f1(self):
        if self.label_f1:
            self.label_f1.destroy()
        self.label_f1 = self.window.create_label(self.frame_buttons_entrys.root, "Введите частоту", font=("Arial Bold", 10))
        self.label_f1.grid(row=0, column=8, padx=10, pady=0, sticky='nsew')

        if self.entry_f1:
            self.entry_f1.destroy()
        self.entry_f1 = self.window.create_entry(self.frame_buttons_entrys.root, width=10)
        self.entry_f1.grid(row=0, column=9, padx=10, pady=15, sticky='nsew')
        self.entry_f1.insert(index=0, text='1')

        if self.label_f2:
            self.label_f2.destroy()

        if self.entry_f2:
            self.entry_f2.destroy()

    def view_entry_f1_f2(self):
        if self.label_f1:
            self.label_f1.destroy()
        self.label_f1 = self.window.create_label(self.frame_buttons_entrys.root, "Введите начальную частоту", font=("Arial Bold", 10))
        self.label_f1.grid(row=0, column=8, padx=10, pady=0, sticky='nsew')

        if self.entry_f1:
            self.entry_f1.destroy()
        self.entry_f1 = self.window.create_entry(self.frame_buttons_entrys.root, width=10)
        self.entry_f1.grid(row=0, column=9, padx=10, pady=15, sticky='nsew')
        self.entry_f1.insert(index=0, text='100')

        if self.label_f2:
            self.label_f2.destroy()
        self.label_f2 = self.window.create_label(self.frame_buttons_entrys.root, "Введите конечную частоту", font=("Arial Bold", 10))
        self.label_f2.grid(row=1, column=8, padx=10, pady=0, sticky='nsew')

        if self.entry_f2:
            self.entry_f2.destroy()
        self.entry_f2 = self.window.create_entry(self.frame_buttons_entrys.root, width=10)
        self.entry_f2.grid(row=1, column=9, padx=10, pady=15, sticky='nsew')
        self.entry_f2.insert(index=0, text='100')





    def run(self):

        self.canvas_inception = None
        self.canvas_receiver = None

        self.entry_f1 = None
        self.entry_f2 = None

        self.label_f1 = None
        self.label_f2 = None

        self.frame_buttons_entrys = self.window.create_label_frame(self.frame.root, width=1650, height=180, text='Входные параметры')
        self.frame_buttons_entrys.place(relx=0.005, rely=0.01)
        self.frame_buttons_entrys.grid_propagate(False)

        frame_canvas = self.window.create_frame(self.frame.root, width=1600, height=800, relief=SOLID, borderwidth=1)
        frame_canvas.place(relx=0.005, rely=0.22)

        self.frame_canvas_inception = self.window.create_label_frame(frame_canvas.root, width=1600, height=350, text='Сигнал на источнике')
        self.frame_canvas_inception.pack(side='top', padx=20, pady=5)
        self.frame_canvas_inception.pack_propagate(False)

        self.frame_canvas_receiver = self.window.create_label_frame(frame_canvas.root, width=1600, height=350, text='Сигнал на приемнике')
        self.frame_canvas_receiver.pack(side='top', padx=20, pady=5)
        self.frame_canvas_receiver.pack_propagate(False)



        label_hk = self.window.create_label(self.frame_buttons_entrys.root, text='Укажите коэффициент глубины 0.004-1000', font=("Arial Bold", 10))
        label_hk.grid(row=0, column=0, padx=5, pady=0, sticky='nsew')
        self.entry_hk = self.window.create_entry(self.frame_buttons_entrys.root, width=10)
        self.entry_hk.grid(row=0, column=1, padx=5, pady=15, sticky='nsew')
        self.entry_hk.insert(index=0, text='0.03')

        label_l_moda = self.window.create_label(self.frame_buttons_entrys.root, text='Укажите номер моды 1-6', font=("Arial Bold", 10))
        label_l_moda.grid(row=1, column=0, padx=5, pady=0, sticky='nsew')
        self.entry_l_moda = self.window.create_entry(self.frame_buttons_entrys.root, width=10)
        self.entry_l_moda.grid(row=1, column=1, padx=5, pady=15, sticky='nsew')
        self.entry_l_moda.insert(index=0, text='2')

        label_inception = self.window.create_label(self.frame_buttons_entrys.root, text='Укажите координаты источника в формате x,y', font=("Arial Bold", 10))
        label_inception.grid(row=0, column=2, padx=10, pady=0, sticky='nsew')
        self.entry_inception = self.window.create_entry(self.frame_buttons_entrys.root, width=15)
        self.entry_inception.grid(row=0, column=3, padx=10, pady=15, sticky='nsew')
        self.entry_inception.insert(index=0, text='0, 5000')

        label_receiver = self.window.create_label(self.frame_buttons_entrys.root, text='Укажите координаты приемника в формате x,y', font=("Arial Bold", 10))
        label_receiver.grid(row=1, column=2, padx=10, pady=0, sticky='nsew')
        self.entry_receiver = self.window.create_entry(self.frame_buttons_entrys.root, width=15)
        self.entry_receiver.grid(row=1, column=3, padx=10, pady=15, sticky='nsew')
        self.entry_receiver.insert(index=0, text='2121, 7788')


        label_duration = self.window.create_label(self.frame_buttons_entrys.root, text='Укажите длительность сигнала', font=("Arial Bold", 10))
        label_duration.grid(row=0, column=4, padx=10, pady=0, sticky='nsew')
        self.entry_duration = self.window.create_entry(self.frame_buttons_entrys.root, width=10)
        self.entry_duration.grid(row=0, column=5, padx=10, pady=15, sticky='nsew')
        self.entry_duration.insert(index=0, text='1')

        singals_type = ['sin', 'chirp']
        self.selected_signals = StringVar()

        label_signals_type = self.window.create_label(self.frame_buttons_entrys.root, text='Выберите тип сигнала',
                                               font=("Arial Bold", 10))
        label_signals_type.grid(row=0, column=6, padx=10, pady=0, sticky='nsew')
        radiobutton_sin = self.window.create_radiobutton(self.frame_buttons_entrys.root, state='NORMAL', text=singals_type[0],
                                                         value=singals_type[0], width = 10, variable = self.selected_signals, command = self.view_entry_f1)
        radiobutton_sin.grid(row=0, column=7, padx=10, pady=0, sticky='nsew')
        radiobutton_chirp = self.window.create_radiobutton(self.frame_buttons_entrys.root, state='NORMAL', text=singals_type[1],
                                                         value=singals_type[1], width = 10, variable = self.selected_signals, command = self.view_entry_f1_f2)
        radiobutton_chirp.grid(row=1, column=7, padx=10, pady=0, sticky='nsew')


        btn_paint = self.window.create_button(master=self.frame_buttons_entrys.root, text='Отрисовать график',
                                              command=self.generate_scatter_chart, width=17, height=2)
        btn_paint.grid(row=2, column=2, padx=5, pady=0, sticky='nsew')

        btn_clear = self.window.create_button(master=self.frame_buttons_entrys.root, text='Очистить график',
                                                     command=self.clear_canvas, width=17, height=2)
        btn_clear.grid(row=2, column=3, padx=5, pady=5, sticky='nsew')


