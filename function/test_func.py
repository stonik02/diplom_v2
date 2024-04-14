from function.utils.signal import *
from function.utils.spectrum_utils import *
from scipy.fft import fft, ifft
import cmath


c = 1500  # Скорость звука
# inception = np.array([0, 5000])   # Источник
pi = math.pi
v_dna = 1900   # Скорость звука в дне

# t = 6e-4  # Один отрезок времени
# duration_signal = 1
#
# signal_time_array = np.arange(0, duration_signal, t)



def rass4et_ql0(wk, c, pi, l_moda, h_k, inception, v_dna):
    h_start = depth(inception[1], h_k)
    ql0 = []
    k = 0
    for w in wk:
        try:
            ql_point = ql(w, c, pi, h_start, l_moda)
            c_point = w / ql_point
            if c_point > v_dna:
                k += 1
                ql0.append(0)
            else:
                ql0.append(ql0)
        except:
            k += 1
            ql0.append(0)
    print(f"ql0 complex = {k}")
    return ql0


def signal_receiver_fft(signal_fft, fi_wk_res, steps, ql0_arr):
    c1 = []
    c2 = []
    count1 = 0
    count2 = 0

    flag = 0
    if steps % 2 == 0:  # Если колличество отсчетов сигнала четное
        # Считаем первую половину
        for i in range(len(fi_wk_res)):  # Проходим по массиву fi(wk) - половина массива сигнала
            if i == 0 or i == (len(fi_wk_res)-1):  # Первый и средний элемент в конечном массиве - действительные
                c1.append(signal_fft[i])
                continue
            if fi_wk_res == 0:  # Если при определенной частоте сигнал ушел в дно - зануляем его
                c1.append(0)
                continue
            c_res = signal_fft[i] * cmath.exp((-1j) * fi_wk_res[i])  # Рассчитываем полученный сигнал
            c1.append(c_res)
        # Считаем вторую половину
        for i in reversed(c1):
            if flag == 0 or flag == len(c1) - 1:
                flag += 1
                continue
            flag += 1
            c2.append(i.conjugate())
    else:
        print("Мы в елсе")
        for i in range(len(fi_wk_res)):
            if i == 0:
                c1.append(signal_fft[i])
                continue
            if ql0_arr[i] == 0:
                c1.append(0)
                continue
            c_res = signal_fft[i] * cmath.exp((-1j) * fi_wk_res[i])
            c1.append(c_res)
        # Считаем вторую половину
        for i in reversed(c1):
            if flag == len(c1) - 1:
                flag += 1
                continue
            flag += 1
            c2.append(i.conjugate())

    for i in c2:
        if i == 0:
            count2 += 1

    count3 = 0
    for i in (c1 + c2):
        if i == 0:
            count3 += 1

    print(f"count1 = {count1} count2 = {count2} count3 = {count3}")
    return c1 + c2


def main_func(h_k, l_moda, signal_type, receiver, inception, f1, f2, duration_signal):
    t = 0
    if signal_type == 'sin':
        t = 1/f1 / (10 + l_moda)  # Один отрезок времени
    if signal_type == 'chirp':
        t = 1/f2 / 10  # Один отрезок времени
    signal_time_array = np.arange(0, duration_signal, t)  # Массив длительности сигнала
    receiver_distance = distance_between_points(inception[0], inception[1], receiver[0], receiver[1])  # Примерное расстояние до приемника
    t_path = receiver_distance/c + 5  # Время сигнала в пути + 3c
    step_path = int(t_path/t)  # Колличество отсчетов пути
    t_path = step_path * t  # Пересчитываем время пути из-за округления int()
    array_path = np.zeros((1, step_path))  # Массив нулей = пути
    t_arr = np.arange(0, t_path + duration_signal, t)  # Единый временной массив

    steps = t_arr.size  # Колличество временных отсчетов
    steps_signal = signal_time_array.size  # Колличество отсчетов сигнала
    print(f"steps_signal = {steps_signal} steps_time = {steps}")

    fk_arr = f_k(steps, t, steps_signal)  # Массив частот сигнала
    wk_arr = w_k(steps, pi, fk_arr)   # Массив фазовых набегов


    signal_arr = [] # Массив сигнала
    if signal_type == 'sin':
        signal_arr = signal_sin(f1, signal_time_array)
    if signal_type == 'chirp':
        f_arr = np.linspace(f1, f2, len(signal_time_array))  # Массив частот сигнала для chirp
        print(f_arr)
        signal_arr = signal_chirp(f_arr, signal_time_array)

    signal_arr = np.asarray(signal_arr)  # Список к массиву numpy для удобства
    print(f"t_arr = {len(t_arr)} signal = {len(signal_arr)}")
    while t_arr.size > (signal_arr.size + array_path.size):
        array_path = np.append(array_path, 0)
    try:
        signal_arr = np.concatenate((signal_arr, array_path[0]))   # Добавляем к массиву сигнала массив нулей в конец
    except:
        signal_arr = np.concatenate((signal_arr, array_path))  # Добавляем к массиву сигнала массив нулей в конец
    print(f"t_arr = {len(t_arr)} signal = {len(signal_arr)}")

    signal_fft = np.fft.fft(signal_arr)  # Фурье сигнала

    fi_wk_res, lines, l_arr = fi_wk(wk_arr, h_k, c, pi, l_moda, receiver, inception, v_dna, t)   # Считаем fi_wk = ql(wk) * delta_l




    ql0_arr = rass4et_ql0(wk_arr, c, pi, l_moda, h_k, inception, v_dna)
    signal_fft_receiver_result = signal_receiver_fft(signal_fft, fi_wk_res, steps, ql0_arr)  # Считаем принятый сигнал fft

    signal_on_receiver = np.fft.ifft(signal_fft_receiver_result)   # Обратный фурье

    print("LEN: signal_arr = {}  signal_fft = {} t_arr = {}\n fi_wk_res = {} wk_arr = {} "
          .format(len(signal_arr),  len(signal_fft), len(t_arr), len(fi_wk_res), len(wk_arr)))

    return signal_arr, signal_on_receiver, t_arr, lines, l_arr, fi_wk_res, wk_arr, t
