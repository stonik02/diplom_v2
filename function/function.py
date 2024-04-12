from function.utils.utils import *

t = 9e-4  # Один отрезок времени Время все сильно меняет 0.002-0.005
c = 1500  # Скорость звука
inception = [0, 5000]
pi = 3.14

steps = 15000  # Число шагов в цикле

v_dna = 1800


def main_function(h_k, l_moda, f, receiver, num_rays):
    result_lych_x = []
    result_lych_y = []
    result_alfa = 0

    y_min = float('inf')

    h_start = depth(inception[1], h_k)
    wk = 2 * pi * f
    ql0 = ql(wk, c, pi, h_start, l_moda)

    distance_min = float('inf')
    lines_x = []
    lines_y = []
    flag = False
    for i in range(num_rays):
        alfa = i * pi / (num_rays / 2)
        k = [ql0 * math.cos(alfa), ql0 * math.sin(alfa)]
        r = inception
        x_arr = []  # Список для координат x текущей линии
        y_arr = []  # Список для координат y текущей линии
        for j in range(steps):
            h_point = depth(r[1], h_k)
            try:
                ql_point = ql(wk, c, pi, h_point, l_moda)
            except:
                break

            c_point = wk / ql_point
            # Проверяем, если звук уходит в дно, то заканчиваем его рассчет
            if c_point > v_dna:
                break
            n = refractive_index_v2(r[1], wk, c, l_moda, ql0, pi, h_k)
            try:
                gradient_n = gradient_v2(r, ql0, wk, c, l_moda, pi, h_k)
            except:
                break
            k = dk(wk, n, gradient_n, t, k)
            r = dr(c, wk, k, t, r)

            x_point = r[0]
            y_point = r[1]

            if y_point < y_min:
                y_min = y_point

            # Берем только правую половину графика
            if x_point < 0:
                break
            x_arr.append(x_point)
            y_arr.append(y_point)

            distance_points = distance_between_points(x_point, y_point, receiver[0], receiver[1])
            if distance_points < distance_min and distance_points < 500:
                distance_min = distance_points
                result_alfa = alfa
                result_lych_x.clear()
                result_lych_y.clear()
                result_lych_x.append(x_arr)
                result_lych_y.append(y_arr)

        lines_x.append(x_arr)
        lines_y.append(y_arr)
    return [lines_x, lines_y], [result_lych_x, result_lych_y, result_alfa], y_min, distance_min