import random

import numpy as np


def modulate_bpsk(code, n_for_bit, signal_arr):
    pm = []
    for bit in code:
        for i in range(n_for_bit):
            if bit == 1:
                pm.append(1)
            else:
                pm.append(-1)

    x = []
    print(f'pm = {len(pm)}, signal_arr - {len(signal_arr)}')
    for i in range(len(pm)):
        x.append(signal_arr[i] * pm[i])
    return x


def demodulate_bpsk(signal_arr_start, signal_on_receiver_not_null, n_for_bit):
    y = []
    print(f'len(signal_on_receiver_not_null) = {len(signal_on_receiver_not_null)} len(signal_arr) = {len(signal_arr_start)}')
    for i in range(len(signal_arr_start)):
        # try:
        y.append(signal_arr_start[i] * signal_on_receiver_not_null[i])
        # except:
        #     y.append(0)

    # Фильтра нижних частот
    z = filter_signal(y, n_for_bit)
    dem = np.where(z > 0, 1, 0)

    return y, z, dem


def filter_signal(signal, n_for_bit):
    return np.convolve(signal, np.ones(n_for_bit) / n_for_bit, mode='same')


def take_bits_from_demodulated_signal(dem, n_for_bit):
    result_bits = []
    for i in range(0, len(dem), n_for_bit):
        bit_segment = dem[i:i + n_for_bit]
        # Определение значения бита по среднему значению сегмента
        recovered_bit = 1 if np.mean(bit_segment) > 0.5 else -1
        result_bits.append(recovered_bit)
    return result_bits




def bit_comparison(code, result_bits, count_bit):
    beer = 0
    for i in range(count_bit):
        if code[i] != result_bits[i]:
            beer += 1
    print(f'Start -  {code}\n End   - {result_bits}')
    return beer


def generate_ones_and_neg_ones(n):
    return [random.choice([-1, 1]) for _ in range(n)]


def cut_null_points(signal):
    result_signal = []
    flag = True
    for s in signal:
        if flag:
            if 0.3 > s > -0.3:
                continue
            flag = False
            result_signal.append(s)
            continue
        result_signal.append(s)
    return result_signal


def add_noise(signal, k):
    noise = np.random.normal(0, k, len(signal))
    channel = noise + signal
    return channel
