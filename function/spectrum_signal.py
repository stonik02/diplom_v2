import binascii

from scipy.signal import hilbert

from function.utils.signal import *
from function.utils.spectrum_utils import *
import cmath

c = 1500  # Скорость звука
pi = math.pi
v_dna = 1900  # Скорость звука в дне


def main_func(h_k, l_moda, signal_type, receiver, inception, f1, f2, duration_signal):
    t = 1 / (f1 * 10) if signal_type == 'sin' else 1 / (f2 * 10)  # Один отрезок времени

    signal_time_array = np.arange(0, duration_signal, t)  # Массив длительности сигнала
    receiver_distance = distance_between_points(inception[0], inception[1], receiver[0],
                                                receiver[1])  # Примерное расстояние до приемника
    t_path = receiver_distance / c + 1  # Время сигнала в пути + 3c
    step_path = int(t_path / t)  # Колличество отсчетов пути
    t_path = step_path * t  # Пересчитываем время пути из-за округления int()
    array_path = np.zeros((1, step_path))  # Массив нулей = пути
    t_arr = np.arange(0, t_path + duration_signal, t)  # Единый временной массив

    steps = t_arr.size  # Колличество временных отсчетов
    steps_signal = signal_time_array.size  # Колличество отсчетов сигнала
    print(f"steps_signal = {steps_signal} steps_time = {steps}")

    fk_arr = f_k(steps, t, steps_signal)  # Массив частот сигнала
    wk_arr = w_k(steps, pi, fk_arr)  # Массив фазовых набегов

    signal_arr = []  # Массив сигнала
    if signal_type == 'sin':
        signal_arr = signal_sin(f1, signal_time_array)
    if signal_type == 'chirp':
        f_arr = np.linspace(f1, f2, len(signal_time_array))  # Массив частот сигнала для chirp
        signal_arr = signal_chirp(f_arr, signal_time_array)
    signal_arr = np.asarray(signal_arr)  # Список к массиву numpy для удобства


    while t_arr.size > (signal_arr.size + array_path.size):
        array_path = np.append(array_path, 0)
    try:
        signal_arr = np.concatenate((signal_arr, array_path[0]))  # Добавляем к массиву сигнала массив нулей в конец
    except:
        signal_arr = np.concatenate((signal_arr, array_path))  # Добавляем к массиву сигнала массив нулей в конец

    signal_fft = np.fft.fft(signal_arr)  # Фурье сигнала

    fi_wk_res, lines, l_arr = fi_wk(wk_arr, h_k, c, pi, l_moda, receiver, inception, v_dna, t)  # Считаем fi_wk = ql(wk) * delta_l

    signal_fft_receiver_result = signal_receiver_fft(signal_fft, fi_wk_res, steps, 0)  # Считаем принятый сигнал fft

    # signal_on_receiver_ymnoj_na_fi_ewe_raz = signal_receiver_fft(signal_fft_receiver_result, fi_wk_res, steps, 1)
    signal_on_receiver = np.fft.ifft(signal_fft_receiver_result)  # Обратный фурье

    return signal_arr, signal_on_receiver, t_arr, lines, l_arr, fi_wk_res, wk_arr
