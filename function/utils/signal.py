import math


# s = sin(2*pi*f*t)

pi = 3.14


def signal_point(f, t):
    # return 1 * math.sin(2*pi*f*t)
    return math.sin(2 * pi * f * t)
    # chirp


def signal_chirp(f, signal_time_array):
    signal_arr = []
    for i in range(len(signal_time_array)):
        signal_arr.append(signal_point(f[i], signal_time_array[i]))
    return signal_arr


def signal_sin(f, signal_time_array):
    signal_arr = []
    for i in range(len(signal_time_array)):
        signal_arr.append(signal_point(f, signal_time_array[i]))
    return signal_arr
