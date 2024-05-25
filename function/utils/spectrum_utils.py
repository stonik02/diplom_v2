import numpy as np

from function.utils.utils import *



def f_k(steps, t, steps_signal):
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
    t=1e-3
    # try:
    ql0 = ql(w, c, pi, h_start, l_moda)
    if ql0 == 0:
        print(f'ql0 complex w = {w} h_start = {h_start}')
        return [0, 0], 0


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
        j = 0
        # print(alfa_grad)
        while True:
            j += 1
            h_point = depth(r[1], h_k)
            ql_point = ql(w, c, pi, h_point, l_moda)
            if ql_point == 0:
                return [0, 0], 0
            c_point = w / ql_point
            if c_point > v_dna:
                return [0, 0], 0

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
            if y_point != 0 and y_point < y_min:
                y_min = y_point

            if x_point - receiver[0] > 0:
                result_y = y_point
                y_lines.append(y_arr)
                x_lines.append(x_arr)
                break
            if j > 20000:
                break
        # if i > 500:
        #     # print("Невозможно подойти к приемнику ближе, чем на {} метров.  ({}:{})".format(np.abs(int(result_y - receiver[1])), x_min, y_min))
        #     if result_y == 0:
        #         print(r[1])
        #         print("Невозможно подойти к приемнику ближе, чем на {} метров. alfa = {} w = {}  ({}:{})".format(
        #             np.abs(int(result_y - receiver[1])), alfa_grad, w, x_min, y_min))
        #
        #         return [0, 0], 0, y_min

        try:

            if result_y - receiver[1] > 300:
                # print("receiver_y = {} result_y = {} alfa -0.1 alfa_grad = {}".format(receiver[1], result_y, alfa_grad))
                alfa_grad -= 0.3
                continue
            if result_y - receiver[1] > 100:
                # print("receiver_y = {} result_y = {} alfa -0.1 alfa_grad = {}".format(receiver[1], result_y, alfa_grad))
                alfa_grad -= 0.1
                continue

            if result_y - receiver[1] < -300:
                # print("receiver_y = {} result_y = {} alfa +0.1 alfa_grad = {}".format(receiver[1], result_y, alfa_grad))
                alfa_grad += 0.3
                continue
            if result_y - receiver[1] < -100:
                # print("receiver_y = {} result_y = {} alfa +0.1 alfa_grad = {}".format(receiver[1], result_y, alfa_grad))
                alfa_grad += 0.1
                continue
            break
        except ValueError:
            alfa_grad += 1
            continue

    return [x_arr, y_arr],  alfa_grad


def fi_wk(wk, h_k, c, pi, l_moda, receiver, inception, v_dna, t):
    fi_wk_arr = []
    x_array = []
    y_array = []
    l_arr = [0] * (len(wk))
    alfa_grad = 0
    count_0 = 0

    for i in range(int(len(wk)/2+1)):
        wi = wk[i]
        if wi == 0:
            fi_wk_arr.append(0)
            count_0 += 1
            continue
        fi_wk_res = 0
        delta_ll = []
        line, alfa_grad = ray_path_calculation_v1(h_k, l_moda, receiver, wi, inception, c, pi, v_dna, t, alfa_grad)
        x_arr = line[0]
        y_arr = line[1]
        x_array.append(x_arr)
        y_array.append(y_arr)
        if alfa_grad == 0:
            count_0 += 0
            fi_wk_arr.append(0)
            continue
        for point in range(len(x_arr)):  # По кол-ву точек
            x_point = x_arr[point]
            y_point = y_arr[point]
            delta_l = 0
            if point != 0:
                # Расстояние между нашей точкой и предыдущей
                delta_l = distance_between_points(x_point, y_point, x_arr[point - 1],
                                                  y_arr[point - 1])
                # print(f"({x_point}:{y_point}) - ({x_arr[point - 1]}:{y_arr[point - 1]})")
            h_point = depth(y_point, h_k)
            # try:
            #     ql_point = ql(wi, c, pi, h_point, l_moda)
            # except:
            #     ql_point = 0
            ql_point = ql(wi, c, pi, h_point, l_moda)
            l_arr[i] += delta_l
            fi_wk = ql_point * delta_l
            fi_wk_res += fi_wk
            delta_ll.append(delta_l)
        fi_wk_arr.append(fi_wk_res)
        print("Луч номер {}  len(ray) = {} ".format(i,  len(x_arr)))
    print(f"count_0 = {count_0} ")
    return fi_wk_arr, [x_array, y_array], l_arr
