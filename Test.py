# import math
#
# import numpy as np
# import matplotlib.pyplot as plt
#
#
#
#
# def signal_point(f, t):
#     return 1 * math.sin(2*math.pi*f*t)
#     # chirp
#
#
# def signal_sin(f, ts):
#     signal_arr = []
#     for i in range(len(ts)):
#         signal_arr.append(signal_point(f, ts[i]))
#     return signal_arr
#
#
#
#
# fs = 10000
# t = 1/fs
# ts = np.arange(-0.1, 0.1-t, t)
# N = len(ts)
# f=500
#
# signal = signal_sin(f, ts)
# n_for_bit = 200
# code = [1, 0.1, 0.1, 1, 1, 0.1, 1, 0.1, 1, 1]
#
# fm = np.zeros((1, N))
# for i in range(len(code)):
#
#
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

def take_code_by_signal(signal, step=200):
    code = []
    for i in range(1, len(signal), step):
        code.append(signal[i])
    return code

def create_code_signal():
    return

# Параметры сигнала
t = 4e-4

fs = 10000
ts = np.arange(-0.1, 0.1, 1/fs)
N = len(ts)

# Несущая частота
fc = np.cos(2 * np.pi * 500 * ts)
print(len(fc))

# Модулирующий сигнал
n_for_bit = 200
code = [1, 0.1, 0.1, 1, 1, 0.1, 1, 0.1, 1, 1]
fm = np.zeros(N)
for i in range(len(code)):
    for j in range(n_for_bit*(i), n_for_bit*(i+1)):
        fm[j] = code[i]

# Амплитудная модуляция
x = fc * fm



# Визуализация
plt.plot(ts, x, linewidth=0.5)
plt.plot(ts, fm, linewidth=2)
plt.title('ASK модуляция')
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.legend(['Модулированный сигнал', 'Модулирующий сигнал'])
plt.grid(True)
plt.show()

# Амплитудная демодуляция
# Преобразование Гильберта
# h = np.imag(np.hilbert(x))
h = hilbert(x)

# Компаратор
dem = np.zeros(len(h))
for i in range(len(h)):
    if np.abs(h[i]) >= 0.5:
        dem[i] = 1
    else:
        dem[i] = 0

code_on_priemnik = take_code_by_signal(dem, n_for_bit)
print(f"Изначальный код = {code}\nКод на приемнике = {code_on_priemnik}")

# Визуализация ASK демодуляции
plt.subplot(2, 1, 1)
plt.plot(ts, x, linewidth=0.5)
plt.plot(ts, np.abs(h), linewidth=2)
plt.title('ASK демодуляция')
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.legend(['Модулированный сигнал', 'Демодулированный сигнал'])
plt.grid(True)

# Визуализация кода демодулированного сигнала
plt.subplot(2, 1, 2)
plt.plot(ts, dem, linewidth=2)
plt.title('Код демодулированного сигнала')
plt.xlabel('Время')
plt.ylabel('Амплитуда')
plt.grid(True)

plt.tight_layout()
plt.show()


# Изначальный код = [1, 0.1, 0.1, 1, 1, 0.1, 1, 0.1, 1, 1]
# Код на приемнике= [1, 0.0, 0.0, 1, 1, 0.0, 1, 0.0, 1, 1]