import numpy as np

from function.utils.utils import *


def f_k(steps, t, steps_signal):
    print("steps_signal = {}".format(steps_signal))
    fd = 1/t
    delfa_f = fd/steps
    fk = []  # Объявляем массив fk и потом заполняем fk = i * delfa_f

    for i in range(steps):
        if i < steps_signal:
            fk.append(i * delfa_f)
        else:
            fk.append(0)
    return fk


def w_k(steps, pi, fk):
    wk_result = []  # Объявляем массив фазовых набегов и заполняем его

    for i in range(steps):
        wk_result.append(2 * pi * fk[i])
    return wk_result



def ray_path_calculation_v1(h_k, l_moda, receiver, w, inception, c, pi, v_dna, t, alfa_grad):

    x_lines = []
    y_lines = []
    h_start = depth(inception[1], h_k)
    try:
        ql0 = ql(w, c, pi, h_start, l_moda)
    except:
        return [0,0], 0, 10000.0
    y_min = float('inf')
    i = 0
    while True:
        i += 1
        alfa = alfa_grad * pi / 180
        k = [ql0 * math.cos(alfa), ql0 * math.sin(alfa)]
        r = inception
        x_arr = []
        y_arr = []
        result_y = 0
        x_min = float('inf')
        j = 0
        # print(alfa_grad)
        while True:
            j += 1
            h_point = depth(r[1], h_k)
            try:
                ql_point = ql(w, c, pi, h_point, l_moda)
            except:
                break
            if ql_point == 0:
                break
            c_point = w / ql_point
            # Проверяем, если звук уходит в дно, то заканчиваем его рассчет
            if c_point > v_dna:
                # print("w - {} ql - {} r1 - {} alfa - {}".format(w, ql_point, r[1], alfa_grad))
                break
            n = refractive_index_v2(r[1], w, c, l_moda, ql0, pi, h_k)
            try:
                gradient_n = gradient_v2(r, ql0, w, c, l_moda, pi, h_k)
            except:
                break
            k = dk(w, n, gradient_n, t, k)
            r = dr(c, w, k, t, r)

            x_point = r[0]
            y_point = r[1]

            if x_point < 0:
                break

            x_arr.append(x_point)
            y_arr.append(y_point)
            if y_point !=0 and y_point < y_min:
                y_min = y_point
                x_min = x_point
            # print("({}:{} alfa = {})".format(x_point, y_point, alfa_grad))


            if x_point - receiver[0] > 0:
                # print("({}:{})".format(x_point,y_point))
                result_y = y_point
                y_lines.append(y_arr)
                x_lines.append(x_arr)
                # print("({}:{} alfa = {})".format(x_point,y_point, alfa_grad))
                break
            if j > 20000:
                break
        if i > 500:
            # print("Невозможно подойти к приемнику ближе, чем на {} метров.  ({}:{})".format(np.abs(int(result_y - receiver[1])), x_min, y_min))
            if result_y == 0:
                print(r[1])
                print("Невозможно подойти к приемнику ближе, чем на {} метров. alfa = {} w = {}  ({}:{})".format(
                    np.abs(int(result_y - receiver[1])), alfa_grad, w, x_min, y_min))

                return [0, 0], 0, y_min

        try:
            # zna4enie_x_v_to4ke_x_priemnika = min(x_arr, key=lambda x: abs(x - receiver[0]))
            # index_x_v_to4ke_x_priemnika = x_arr.index(zna4enie_x_v_to4ke_x_priemnika)
            # zna4enie_y_v_to4ke_x_priemnika = y_arr[index_x_v_to4ke_x_priemnika]
            # print("receiver_y = {} result_y = {} alfa = {}".format(receiver[1], result_y, alfa_grad))

            # if result_y - receiver[1] > 2000:
            #     # print("receiver_y = {} result_y = {} alfagrad = {} alfa -25".format(receiver[1], result_y, alfa_grad))
            #     alfa_grad -= 25
            #     continue
            # if result_y - receiver[1] > 1000:
            #     # print("receiver_y = {} result_y = {} alfagrad = {} alfa -15".format(receiver[1], result_y, alfa_grad))
            #     alfa_grad -= 15
            #     continue
            # if result_y - receiver[1] > 500:
            #     # print("receiver_y = {} result_y = {} alfagrad = {} alfa -5".format(receiver[1], result_y, alfa_grad))
            #     alfa_grad -= 5
            #     continue
            if result_y - receiver[1] > 300:
                # print("receiver_y = {} result_y = {} alfa -0.1 alfa_grad = {}".format(receiver[1], result_y, alfa_grad))
                alfa_grad -= 1
                continue
            if result_y - receiver[1] > 100:
                # print("receiver_y = {} result_y = {} alfa -0.1 alfa_grad = {}".format(receiver[1], result_y, alfa_grad))
                alfa_grad -= 0.1
                continue
            #
            # if result_y - receiver[1] < -2000:
            #     # print("receiver_y = {} result_y = {} alfagrad = {} alfa +25".format(receiver[1], result_y, alfa_grad))
            #     alfa_grad += 25
            #     continue
            # if result_y - receiver[1] < -1000:
            #     # print("receiver_y = {} result_y = {} alfagrad = {} alfa +15".format(receiver[1],  result_y, alfa_grad))
            #     alfa_grad += 15
            #     continue
            # if result_y - receiver[1] < -500:
            #     # print("receiver_y = {} result_y = {} alfagrad = {} alfa +5".format(receiver[1],  result_y, alfa_grad))
            #     alfa_grad += 5
            #     continue
            if result_y - receiver[1] < -300:
                # print("receiver_y = {} result_y = {} alfa +0.1 alfa_grad = {}".format(receiver[1], result_y, alfa_grad))
                alfa_grad += 1
                continue
            if result_y - receiver[1] < -100:
                # print("receiver_y = {} result_y = {} alfa +0.1 alfa_grad = {}".format(receiver[1], result_y, alfa_grad))
                alfa_grad += 0.1
                continue
            break
        except ValueError:
            alfa_grad += 1
            continue



    return [x_arr, y_arr],  alfa_grad, y_min


def fi_wk(wk, h_k, c, pi, l_moda, receiver, inception, v_dna, t):
    fi_wk_arr = []
    x_array = []
    y_array = []
    l_arr = [0] * (len(wk))
    alfa_grad = 0
    y_min = 100000.0
    for i in range(int(len(wk)/2+1)):
        wi = wk[i]
        if wi == 0:
            fi_wk_arr.append(0)
            continue
        fi_wk_res = 0
        delta_ll = []
        line, alfa_grad, y = ray_path_calculation_v1(h_k, l_moda, receiver, wi, inception, c, pi, v_dna, t, alfa_grad)
        if y_min > y:
            y_min = y
        # if alfa_grad == 0:
        #     alfa_grad = -90
        # print(line)
        x_arr = line[0]
        y_arr = line[1]
        x_array.append(x_arr)
        y_array.append(y_arr)
        if x_arr == 0:
            fi_wk_arr.append(0)
            continue
        for point in range(len(x_arr)):  # По кол-ву точек
            x_point = x_arr[point]
            y_point = y_arr[point]
            delta_l = 0
            if point != 0:
                # Расстояние между нашей точкой и предыдущей
                delta_l = distance_between_points(x_point, y_point, x_arr[point - 1],
                                                  y_arr[point - 1], )
            h_point = depth(y_point, h_k)
            try:
                ql_point = ql(wi, c, pi, h_point, l_moda)
            except:
                ql_point = 0
            l_arr[i] += delta_l
            fi_wk = ql_point * delta_l
            fi_wk_res += fi_wk
            delta_ll.append(delta_l)
        fi_wk_arr.append(fi_wk_res)
        print("Луч номер {}  len(ray) = {} ".format(i,  len(x_arr)))
        # print(delta_ll)
    print("Min y = {}".format(y_min))
    return fi_wk_arr, [x_array, y_array], l_arr

# def obrezaem_ly4(ray, receiver):
#     result_ray_x = []
#     result_ray_y = []
#
#     dist_min = float('inf')
#     for i in range(len(ray[0])):
#         dist = distance_between_points(ray[0][i], ray[1][i], receiver[0], receiver[1])
#         if dist < dist_min:
#             dist_min = dist
#             result_ray_x.append(ray[0][i])
#             result_ray_y.append(ray[1][i])
#     return [result_ray_x, result_ray_y]
#
# def take_points_result_ray(alfa, h_k, f, l_moda, steps):
#     h_start = depth(inception[1], h_k)
#     w = 2 * pi * f
#     ql0 = ql(w, c, pi, h_start, l_moda)
#     k = [ql0 * math.cos(alfa), ql0 * math.sin(alfa)]
#     r = inception
#     x_arr = []  # Список для координат x текущей линии
#     y_arr = []  # Список для координат y текущей линии
#     for j in range(steps):
#         h_point = depth(r[1], h_k)
#         try:
#             ql_point = ql(w, c, pi, h_point, l_moda)
#         except:
#             break
#
#         c_point = w / ql_point
#         # Проверяем, если звук уходит в дно, то заканчиваем его рассчет
#         if c_point > v_dna:
#             break
#         n = refractive_index_v2(r[1], w, c, l_moda, ql0, pi, h_k)
#         try:
#             gradient_n = gradient_v2(r, ql0, w, c, l_moda, pi, h_k)
#         except:
#             break
#         k = dk(w, n, gradient_n, t_signal, k)
#         r = dr(c, w, k, t_signal, r)
#
#         x_point = r[0]
#         y_point = r[1]
#
#
#         x_arr.append(x_point)
#         y_arr.append(y_point)
#
#     return [x_arr, y_arr]

# def t_full():
#     t_full = []
#     time = 0
#     for i in range(steps):
#         time += t
#         t_full.append(time)
#     return t_full