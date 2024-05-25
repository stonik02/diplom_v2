from scipy.signal import hilbert

from function.utils.modulate_utils import *
from function.utils.signal import *
from function.utils.spectrum_utils import *

c = 1500  # Скорость звука
pi = math.pi
v_dna = 1900  # Скорость звука в дне
count_bit = 10  # Кол-во битов в сигнале


# 40 фаз на один




def main_func(h_k, l_moda, receiver, inception, f1):
    Tb = (1/f1) * 10  # продолжительность бита в фазах
    Fs = (f1 * 10)
    t = 1 / Fs  # Один отрезок времени (продолжительность бита в фазах)
    # code = np.random.randint(0, 2, count_bit)  # Генерация случайной последовательности бит
    # code[0] = 1 if code[0] != 1 else 1
    # code = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]
    n_for_bit = int((Tb / t))  # Кол-во отсчетов на бит
    code = generate_ones_and_neg_ones(count_bit)
    duration_signal = Tb * len(code)

    signal_time_array = np.arange(0, duration_signal, t)  # Массив длительности сигнала
    receiver_distance = distance_between_points(inception[0], inception[1], receiver[0],
                                                receiver[1])  # Примерное расстояние до приемника
    t_path = receiver_distance / c + 2  # Время сигнала в пути + 1c
    step_path = int(t_path / t)  # Колличество отсчетов пути
    t_path = step_path * t  # Пересчитываем время пути из-за округления int()
    array_path = np.zeros((1, step_path))  # Массив нулей = пути
    t_arr = np.arange(0, t_path + duration_signal, t)  # Единый временной массив

    steps = t_arr.size  # Общее колличество временных отсчетов
    steps_signal = signal_time_array.size  # Колличество отсчетов сигнала
    print(f"steps_signal = {steps_signal} steps_time = {steps}")
    print(f'n_for_bit = {n_for_bit}')

    fk_arr = f_k(steps, t, steps_signal)  # Массив частот сигнала
    wk_arr = w_k(steps, pi, fk_arr)  # Массив фазовых набегов

    signal_arr_start = signal_sin(f1, signal_time_array)
    signal_arr_start = np.asarray(signal_arr_start)  # Список к массиву numpy для удобства

    # Модуляция ---------------------------------------------------------------------------
    modulated_signal = modulate_bpsk(code, n_for_bit, signal_arr_start)

    while t_arr.size > (len(modulated_signal) + array_path.size):
        array_path = np.append(array_path, 0)
    try:
        modulated_signal = np.concatenate((modulated_signal, array_path[0]))  # Добавляем к массиву сигнала массив нулей в конец
    except:
        modulated_signal = np.concatenate((modulated_signal, array_path))  # Добавляем к массиву сигнала массив нулей в конец

    # -----------------------------------------------------------------------------

    # while t_arr.size > (signal_arr.size + array_path.size):
    #     array_path = np.append(array_path, 0)
    # try:
    #     signal_arr = np.concatenate((signal_arr, array_path[0]))  # Добавляем к массиву сигнала массив нулей в конец
    # except:
    #     signal_arr = np.concatenate((signal_arr, array_path))  # Добавляем к массиву сигнала массив нулей в конец


    # Фурье сигнала ---------------------------------------------------------------
    signal_fft = np.fft.fft(modulated_signal)
    # Считаем fi_wk = ql(wk) * delta_l -----------------------------------------------
    fi_wk_res, lines, l_arr = fi_wk(wk_arr, h_k, c, pi, l_moda, receiver, inception, v_dna, t)
    # Считаем принятый сигнал fft -----------------------
    signal_fft_receiver_result = signal_receiver_fft(signal_fft, fi_wk_res, steps, 0)

    # signal_on_receiver_ymnoj_na_fi_ewe_raz = signal_receiver_fft(signal_fft_receiver_result, fi_wk_res, steps, 1)
    # Обратный фурье ---------------------------------------------------------------------
    signal_on_receiver = np.fft.ifft(signal_fft_receiver_result)
    signal_on_receiver = add_noise(signal_on_receiver, 0.07)
    signal_on_receiver_not_null = cut_null_points(signal_on_receiver)
    # signal_on_receiver_not_null = add_noise(signal_on_receiver_not_null, 0.01)
    # Демодуляция ---------------------------------------------
    y, signal_receiver_filter, dem = demodulate_bpsk(signal_arr_start, signal_on_receiver_not_null, n_for_bit)
    result_bits = take_bits_from_demodulated_signal(dem, n_for_bit)
    beer = bit_comparison(code, result_bits, count_bit)

    signal_filter = filter_signal(signal_arr_start, n_for_bit)
    # ---------------------------------------------
    print(f'Расстояние от источника до приемника = {max(l_arr)}')
    return modulated_signal, signal_on_receiver, t_arr, y, beer, signal_receiver_filter, signal_filter