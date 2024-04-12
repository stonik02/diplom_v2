import math


def ql(Wk, c, pi, h, l_moda):
    return math.sqrt(math.pow(Wk, 2) / math.pow(c, 2) - math.pow(pi, 2) / math.pow(h, 2) * math.pow(l_moda - 1 / 2, 2))


def depth(y_point, k):
    # if y_point < 300:
    #     return y_point * 0.02
    return y_point * k


def refractive_index(x, y):
    # return 1 + 0.1 * (math.pow(x, 2) + math.pow(y, 2))
    return 0.1 * (x ** 2 + y ** 2)


def gradient(point):
    x_point = point[0]  # Координата x
    y_point = point[1]  # Координата y

    step = 1e-8

    delta_x = step
    delta_y = step

    grad_x = (refractive_index(x_point + delta_x, y_point) - refractive_index(x_point, y_point)) / delta_x
    grad_y = (refractive_index(x_point, y_point + delta_y) - refractive_index(x_point, y_point)) / delta_y
    return [grad_x, grad_y]


def refractive_index_v2(y, Wk, c, l, ql0, pi, k):
    h = depth(y, k)
    ql_point = ql(Wk, c, pi, h, l)
    n = ql_point / ql0
    # print("refractive_index_v2 n = ", n)
    return n


'''
 Из-за того, что изменение ql от y_point + delta_y очень незначительно отличается
 от ql от в данной точке, градиент очень мал и график получается непонятный
'''


def gradient_v2(point, ql0, Wk, c, l, pi, h_k):
    y_point = point[1]  # Координата y

    step = 50

    delta_x = step
    delta_y = step

    # print("y_point ", y_point)
    # print("y_point + delta_y = ", y_point + delta_y,)
    # print("H y_point ", depth(y_point))
    # print("H y_point + delta_y = ", depth(y_point + delta_y))

    grad_x = (refractive_index_v2(y_point, Wk, c, l, ql0, pi, h_k) - refractive_index_v2(y_point, Wk, c, l, ql0, pi, h_k)) / (
            2 * delta_x)
    grad_y = (refractive_index_v2(y_point + delta_y, Wk, c, l, ql0, pi, h_k) - refractive_index_v2(y_point - delta_y, Wk, c,
                                                                                              l, ql0, pi, h_k)) / (
                     2 * delta_y)
    # print([grad_x, grad_y])
    return [grad_x, grad_y]


def dr(c, Wk, k, t, r_old):
    r = [(math.pow(c, 2) / Wk) * k[0] * t, (math.pow(c, 2) / Wk) * k[1] * t]
    r = [r[0] + r_old[0], r[1] + r_old[1]]
    return r


def dk(Wk, n, gradient_n, t, k_old):
    k = [(Wk / n) * t * gradient_n[0], (Wk / n) * t * gradient_n[1]]
    k = [k[0] + k_old[0], k[1] + k_old[1]]
    return k


def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((float(x2) - x1) ** 2 + (float(y2) - y1) ** 2)


