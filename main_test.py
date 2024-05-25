import numpy
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from scipy.special import erfc
import sys
import logging
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from function.modulate_signal import *

if __name__ == "__main__":

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# code = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]
    # code = np.random.randint(0, 2, 30)  # Генерация случайной последовательности бит
    #
    # Tb = 1/f1 * 10  # продолжительность бита в фазах
    # t = 1 / (f1 * 20)  # Один отрезок времени (продолжительность бита в фазах)
    # duration_signal = Tb * len(code)
    # n_for_bit = int(Tb / t)  # Кол-во отсчетов на бит
    # signal_time_array = np.arange(0, duration_signal, t)  # Массив длительности сигнала
    # signal_arr_start = signal_sin(f1, signal_time_array)
    #
    # modulated_signal = modulate_qpsk(code, n_for_bit, signal_arr_start)
    #
    # y, signal_receiver_filter, dem = demodulate_qpsk(modulated_signal, n_for_bit)
    # result_bits = take_bits_from_demodulated_signal(dem, n_for_bit)
    # beer = bit_comparison(code, result_bits, count_bit)
    #
    # signal_fft = fft(signal_arr_start)
    #
    # signal_filter = filter_signal(signal_fft, n_for_bit)
    #
    # signal_filter = ifft(signal_filter)
    #
    # plt.figure(figsize=(20, 5))
    # plt.plot(signal_time_array, signal_filter)
    # plt.title("Изначальный сигнал с фильтром низких частот")
    # plt.xlabel("t")
    # plt.ylabel("s")
    # # plt.xticks(np.arange(0, max(t_arr), 0.2))
    # plt.grid(True)
    #
    # plt.figure(figsize=(20, 5))
    # plt.plot(signal_time_array, signal_receiver_filter)
    # plt.title("Принятый сигнал сигнал с фильтром низких частот")
    # plt.xlabel("t")
    # plt.ylabel("s")
    # # plt.xticks(np.arange(0, max(t_arr), 0.2))
    # plt.grid(True)
    #
    # plt.show()
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  MAIN
    h_k = 0.1
    l_moda = 2
    signal_type = 'sin'
    inception = [100, 5000]
    receiver = [1000, 10000]
    f1 = 150
    f2 = 0
    duration_signal = 1

    signal_arr, signal_on_receiver, t_arr, y, beer, signal_receiver_filter, signal_filter = main_func(h_k, l_moda, receiver, inception, f1)

    Tb = 1 / f1 * 10  # продолжительность бита в фазах
    t = 1 / (f1 * 20)  # Один отрезок времени (продолжительность бита в фазах)
    n_for_bit = int(Tb / t)  # Кол-во отсчетов на бит

    print(f'Кол-во ошибок = {beer}')

    plt.figure(figsize=(20, 5))
    plt.plot(t_arr[0:5*n_for_bit], signal_arr[0:5*n_for_bit])
    plt.title("Исходный сигнал")
    plt.xlabel("t")
    plt.ylabel("s")
    # plt.xticks(np.arange(0, max(t_arr), 0.2))
    plt.grid(True)

    plt.figure(figsize=(20, 5))
    plt.plot(t_arr[0:5*n_for_bit], signal_on_receiver[0:5*n_for_bit])
    plt.title("Принятый сигнал")
    plt.xlabel("t")
    plt.ylabel("s")
    plt.xticks(np.arange(0, max(t_arr), 0.2))
    plt.grid(True)

    plt.figure(figsize=(20, 5))
    plt.plot(t_arr, signal_arr)
    plt.title("Исходный сигнал")
    plt.xlabel("t")
    plt.ylabel("s")
    # plt.xticks(np.arange(0, max(t_arr), 0.2))
    plt.grid(True)

    plt.figure(figsize=(20, 5))
    plt.plot(t_arr, signal_on_receiver)
    plt.title("Принятый сигнал")
    plt.xlabel("t")
    plt.ylabel("s")
    plt.xticks(np.arange(0, max(t_arr), 0.2))
    plt.grid(True)


    plt.show()





# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # signal_arr, signal_on_receiver, t_arr, lines, l_arr, fi_wk_res, wk_arr = main_func(h_k, l_moda, signal_type, receiver, inception, f1, f2, duration_signal)
    #
    # medium_l = 0
    # for i in l_arr:
    #     medium_l+=i
    # medium_l = medium_l / len(l_arr)
    # print("Среднее пройденное лучем расстояние = {}".format(max(l_arr)))
    # print("Время, которое шел сигнал = {}".format(max(l_arr)/c))
    #
    #
    # plt.figure(figsize=(20, 5))
    # plt.plot(t_arr, signal_arr)
    # plt.title("Исходный сигнал")
    # plt.xlabel("t")
    # plt.ylabel("s")
    # plt.xticks(np.arange(0, max(t_arr), 0.2))
    # plt.grid(True)
    #
    # plt.figure(figsize=(20, 5))
    # plt.plot(t_arr, signal_on_receiver)
    # plt.title("Принятый сигнал")
    # plt.xlabel("t")
    # plt.ylabel("s")
    # plt.xticks(np.arange(0, max(t_arr), 0.2))
    # plt.legend(title="Среднее пройденное лучем расстояние = {}".format(int(max(l_arr))))
    # plt.grid(True)
    #
    # plt.show()
