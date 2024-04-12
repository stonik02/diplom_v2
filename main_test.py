from matplotlib import pyplot as plt

from function.test_func import *

h_k = 0.09
l_moda = 6
f = 1200
receiver = [100, 4000]
# f = 4995.0
num_rays = 400
wk = 2*pi*f

# t = 1e-3  # Один отрезок времени
t = 6e-4  # Один отрезок времени
# steps = 100 # Число шагов в цикле
c = 1500  # Скорость звука
inception = np.array([0, 3000])   # Источник
pi = 3.14
v_dna = 1900   # Скорость звука в дне
duration_signal = 1

f_diskr = 1/t

signal_time_array = np.arange(0, duration_signal, t)

if __name__ == '__main__':

    # result_ray, lines, alfa = ray_path_calculation_v1(h_k, l_moda, receiver, wk, inception, c, pi, v_dna, t)
    #
    # if alfa != 0:
    #     plt.figure(figsize=(7, 5))
    #     # for x, y in zip(lines[0], lines[1]):
    #     #     plt.plot(x, y, color='black')
    #     # plt.title("График x y")
    #
    #     plt.grid()
    #     plt.xlabel("x")
    #     plt.ylabel("y")
    #
    #     x_coords = result_ray[0]
    #     y_coords = result_ray[1]
    #     plt.plot(x_coords, y_coords, color='red', label='')
    #     plt.scatter(receiver[0], receiver[1], color='green', label='Приемник')
    #     plt.show()



    # print(distance_between_points(inception[0], inception[1], receiver[0], receiver[1]))


#500
# 1400

    signal_arr, signal_on_receiver, t_arr, lines, l_arr, fi_wk_res, wk_arr, t = main_func(h_k, l_moda, receiver)

    medium_l = 0
    for i in l_arr:
        medium_l+=i
    medium_l = medium_l / len(l_arr)
    print("Среднее пройденное лучем расстояние = {}".format(max(l_arr)))
    print("Время, которое шел сигнал = {}".format(max(l_arr)/c))


    plt.figure(figsize=(20, 5))
    plt.plot(t_arr, signal_arr)
    plt.title("Исходный сигнал")
    plt.xlabel("t")
    plt.ylabel("s")
    plt.xticks(np.arange(0, max(t_arr), 0.2))
    plt.grid(True)


    plt.figure(figsize=(20, 5))
    plt.plot(t_arr, np.real(signal_on_receiver))
    plt.title("Принятый сигнал")
    plt.xlabel("t")
    plt.ylabel("s")
    plt.xticks(np.arange(0, max(t_arr), 0.2))
    plt.legend(title="Среднее пройденное лучем расстояние = {}".format(int(max(l_arr))))
    plt.grid(True)


    plt.figure(figsize=(7, 5))
    for x, y in zip(lines[0], lines[1]):
        plt.plot(x, y, color='black')
    plt.title("Лучи всех частот")
    plt.xlabel("x")
    plt.ylabel("y")

    # plt.figure(figsize=(7, 5))
    # plt.plot(wk_arr[:int(len(wk_arr)/2)+1], fi_wk_res)
    # plt.title("fi/wk")
    # plt.xlabel("wk")
    # plt.ylabel("fi")

    plt.show()







    #
    # signal_arr = chirp(signal_time_array, 1, 150, duration_signal, method='linear')
    # T = 1.0  # Длительность сигнала в секундах
    # f0 = 20  # Начальная частота в Гц
    # f1 = 200  # Конечная частота в Гц
    # t = np.linspace(0, T, int(T * 1000))  # Временная ось от 0 до T с шагом 1 миллисекунда
    #
    # # Генерация линейного chirp сигнала
    # signal = chirp(t, f0=f0, f1=f1, t1=T, method='linear')
    # plt.figure(figsize=(7, 5))
    # plt.plot(t, signal)
    # plt.title("fi/wk")
    # plt.xlabel("t")
    # plt.ylabel("s")
    #
    # plt.show()