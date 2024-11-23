import matplotlib.pyplot as plt
import numpy as np


def liang_barsky(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    p = [-1 * (x2 - x1), x2 - x1, -1 * (y2 - y1), y2 - y1]
    q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]
    u1, u2 = 0.0, 1.0

    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return None
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                u1 = max(u1, t)
            else:
                u2 = min(u2, t)

    if u1 > u2:
        return None

    clipped_x1 = x1 + u1 * (x2 - x1)
    clipped_y1 = y1 + u1 * (y2 - y1)
    clipped_x2 = x1 + u2 * (x2 - x1)
    clipped_y2 = y1 + u2 * (y2 - y1)

    return [(clipped_x1, clipped_y1), (clipped_x2, clipped_y2)]


def sutherland_hodgman(polygon, clip_rect):
    def inside(p, edge):
        x, y = p
        x1, y1, x2, y2 = edge
        return (x2 - x1) * (y - y1) > (y2 - y1) * (x - x1)

    def intersection(s, p, edge):
        x1, y1, x2, y2 = edge
        dx, dy = p[0] - s[0], p[1] - s[1]
        edge_dx, edge_dy = x2 - x1, y2 - y1
        t = ((x1 - s[0]) * edge_dy - (y1 - s[1]) * edge_dx) / (dx * edge_dy - dy * edge_dx)
        return s[0] + t * dx, s[1] + t * dy

    output_list = polygon
    for edge in clip_rect:
        input_list = output_list
        output_list = []
        s = input_list[-1]

        for p in input_list:
            if inside(p, edge):
                if not inside(s, edge):
                    output_list.append(intersection(s, p, edge))
                output_list.append(p)
            elif inside(s, edge):
                output_list.append(intersection(s, p, edge))
            s = p

    return output_list


def plot_lines(segments, xmin, ymin, xmax, ymax):
    plt.figure()
    plt.title("Отсечение отрезков (Лианг-Барски)")
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot([xmin, xmax, xmax, xmin, xmin], [ymin, ymin, ymax, ymax, ymin], 'r-', label='Окно отсечения')

    for x1, y1, x2, y2 in segments:
        plt.plot([x1, x2], [y1, y2], 'g--', label='Исходный отрезок' if (x1 == 1 and y1 == 2) else "")
        clipped_segment = liang_barsky(x1, y1, x2, y2, xmin, ymin, xmax, ymax)
        if clipped_segment:
            (cx1, cy1), (cx2, cy2) = clipped_segment
            plt.plot([cx1, cx2], [cy1, cy2], 'b-', label='Отсеченный отрезок' if (x1 == 1 and y1 == 2) else "")

    plt.legend()
    plt.show()


def plot_polygon(polygon, clip_rect):
    plt.figure()
    plt.title("Отсечение многоугольников (Сазерленд-Ходжман)")
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot([clip_rect[0][0], clip_rect[1][0], clip_rect[2][0], clip_rect[3][0], clip_rect[0][0]],
             [clip_rect[0][1], clip_rect[1][1], clip_rect[2][1], clip_rect[3][1], clip_rect[0][1]], 'r-',
             label='Окно отсечения')

    poly_x, poly_y = zip(*polygon)
    plt.plot(poly_x + (poly_x[0],), poly_y + (poly_y[0],), 'g--', label='Исходный многоугольник')

    clipped_polygon = sutherland_hodgman(polygon, clip_rect)
    if clipped_polygon:
        clip_x, clip_y = zip(*clipped_polygon)
        plt.plot(clip_x + (clip_x[0],), clip_y + (clip_y[0],), 'b-', label='Отсеченный многоугольник')

    plt.legend()
    plt.show()


def main():
    segments = [
        (1, 2, 8, 4),
        (2, 3, 5, 7),
        (3, 1, 6, 9),
    ]
    xmin, ymin, xmax, ymax = 2, 2, 7, 6
    clip_rect = [(xmin, ymin, xmax, ymin), (xmax, ymin, xmax, ymax),
                 (xmax, ymax, xmin, ymax), (xmin, ymax, xmin, ymin)]
    polygon = [(3, 3), (5, 8), (8, 5), (6, 2)]

    try:
        while True:
            choice = input("Выберите алгоритм: 1 для Лианга-Барски, 2 для Сазерленда-Ходжмана, q для выхода: ")

            if choice == '1':
                plot_lines(segments, xmin, ymin, xmax, ymax)
            elif choice == '2':
                plot_polygon(polygon, clip_rect)
            elif choice.lower() == 'q':
                break
            else:
                print("Неверный выбор. Пожалуйста, введите 1, 2 или q.")
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")


if __name__ == "__main__":
    main()