from function.utils.signal import *
from function.utils.spectrum_utils import *
from scipy.fft import fft, ifft
import cmath

# t = 1e-3  # Один отрезок времени
t = 2e-3  # Один отрезок времени
# steps = 100 # Число шагов в цикле
c = 1500  # Скорость звука
inception = np.array([0, 3000])   # Источник
pi = 3.14
v_dna = 1900   # Скорость звука в дне
duration_signal = 3

f_diskr = 1/t

signal_time_array = np.arange(0, duration_signal, t)
if len(signal_time_array) % 2 == 1:
    signal_time_array = np.append(signal_time_array, t * len(signal_time_array))
steps = len(signal_time_array)


def signal_receiver_fft(signal_fft, fi_wk_res):
    c1 = []
    c2 = []
    flag = 0
    if steps % 2 == 0:
        # Считаем первую половину
        for i in range(len(fi_wk_res)):
            if i == 0 or i == (len(fi_wk_res)-1):
                c1.append(signal_fft[i])
                continue
            c_res = signal_fft[i] * cmath.exp((-1j) * fi_wk_res[i])
            c1.append(c_res)
        # Считаем вторую половину
        for i in reversed(c1):
            if i.imag == 0:
                flag += 1
                continue
            c2.append(i.conjugate())
    return c1 + c2, c1, c2


def main_func(h_k, l_moda, receiver):
    # lines, result_ray, y_min, distance_min, steps_res = ray_path_calculation(h_k, l_moda, f, receiver, num_rays)
    receiver_distance = distance_between_points(inception[0], inception[1], receiver[0], receiver[1])

    t_path = receiver_distance/c
    step_path = int(t_path/t)
    array_path = np.zeros((1, step_path))
    t_arr = np.arange(0, t_path + duration_signal + 3, t)
    if len(t_arr) % 2 == 1:
        t_arr = np.append(t_arr, t * len(t_arr))
    steps = t_arr.size
    steps2 = signal_time_array.size
    fk_arr = f_k(steps, t, steps2)
    wk_arr = w_k(steps, pi, fk_arr)   # Массив фазовых набегов
    f = f_diskr / 10

    print("f_diskr = {}".format(f_diskr))
    print("f = {}".format(f))
    print("wk_arr = {}".format(len(wk_arr)))
    j = 0
    for i in wk_arr:
        if i == 0:
            j+=1


    f_diskr_f = f / len(signal_time_array)
    f_arr = np.arange(50, len(signal_time_array), f_diskr_f)
    signal_arr = signal_sin(f, signal_time_array)
    # signal_arr = signal_chirp(f_arr, signal_time_array)



    signal_arr = np.asarray(signal_arr)
    while t_arr.size > (signal_arr.size + array_path.size):
        array_path = np.append(array_path, 0)
    try:
        signal_arr = np.concatenate((signal_arr, array_path[0]))
    except:
        signal_arr = np.concatenate((signal_arr, array_path))
    for i in range(len(signal_arr)):
        if i < 50:
            print(signal_arr[i])
    signal_fft = fft(signal_arr)  # Фурье сигнала

    fi_wk_res, lines, l_arr = fi_wk(wk_arr, h_k, c, pi, l_moda, receiver, inception, v_dna, t)   # Считаем fi_wk = ql(wk) * delta_l
    j = 0
    for i in fi_wk_res:
        if i == 0:
            j+=1

    print("0 in fi = {}".format(j))
    print("FI_WS_SIZE = {}".format(len(fi_wk_res)))


    # print("wk_arr")
    # print(wk_arr)
    # print("fi_wk_res")
    # print(fi_wk_res)
    signal_fft_receiver_result, c1, c2 = signal_receiver_fft(signal_fft, fi_wk_res)
    signal_on_receiver = ifft(signal_fft_receiver_result)   # Обратный фурье
    print("LEN: signal_arr = {}  signal_fft = {} t_arr = {}\n fi_wk_res = {} wk_arr = {} c1 = {} c2 = {} "
          .format(len(signal_arr),  len(signal_fft), len(t_arr), len(fi_wk_res), len(wk_arr), len(c1), len(c2)))
    c_null = []
    # for i in range(len(signal_arr) - len(signal_on_receiver)):
    #     c_null.append(0)
    # c_null.extend(signal_on_receiver)
    # print("Сигнал на источнике")
    # print(str(signal_arr))
    # print("Сигнал на приемнике")
    # print(str(signal_on_receiver))
    # print("signal_arr = {}".format(signal_arr.size))
    # print("signal_on_receiver = {}".format(signal_on_receiver.size))
    # print("array_path = {}".format(signal_on_receiver.size))
    # print("t_arr = {}".format(t_arr.size))
    # try:
    #     signal_arr = np.concatenate((signal_arr, array_path[0]))
    #     signal_on_receiver = np.concatenate((array_path[0], signal_on_receiver))
    # except:
    #     signal_arr = np.concatenate((signal_arr, array_path))
    #     signal_on_receiver = np.concatenate((array_path, signal_on_receiver))
    # print("signal_arr = {}".format(signal_arr.size))
    # print("signal_on_receiver = {}".format(signal_on_receiver.size))
    # print("array_path = {}".format(signal_on_receiver.size))
    # print("t_arr = {}".format(t_arr.size))
    return signal_arr, signal_on_receiver, t_arr, lines, l_arr, fi_wk_res, wk_arr, t
