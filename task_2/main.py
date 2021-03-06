import argparse
import time
import matplotlib.pyplot as plt

import launch
from distributions import SEPARATOR

HIST_COUNT = 25


def parse_args():
    # Костыль 1
    args = launch.handle_windows_style()
    # Костыль 2
    launch.handle_usage(args)

    parser = argparse.ArgumentParser()
    parser.add_argument('--d')
    parser.add_argument('--p1', type=float)
    parser.add_argument('--p2', type=float)
    parser.add_argument('--p3', type=float)
    parser.add_argument('--f')
    parser.add_argument('--fout')
    parser.add_argument('--gui', action='store_true')

    return parser.parse_args(args)


def transform(args, values_in):
    dist_name = launch.handle_dist(args)
    print('Инициализация распределения {}'.format(dist_name) + SEPARATOR)

    dist = launch.DISTS_DICT[dist_name](args)

    print('Старт преобразования')
    time_start = time.time()
    values_out, values_reference = dist.transform(values_in)
    time_elapsed = int((time.time() - time_start) * 1000)
    print('Преобразование заняло {} милисекунд'.format(time_elapsed) + SEPARATOR)

    return values_out, values_reference


def plot(args, values, values_reference):
    if args.gui:
        plt.subplot(1, 2, 1)
        plt.title('Преобразованные числа')
        plt.hist(values, HIST_COUNT)

        plt.subplot(1, 2, 2)
        plt.title('Эталон')
        plt.hist(values_reference, HIST_COUNT)

        plt.show()


def main():
    # Аргументы
    args = parse_args()
    # Считывание ПСП из файла
    values_in = launch.handle_file_in(args)
    # Старт преобразования к распределению
    values_out, values_reference = transform(args, values_in)
    print('Длина последовательности на выходе = {}'.format(len(values_out)))
    # Запись в файл
    launch.handle_file_out(args, values_out)
    # Построение графика полученного распределения
    plot(args, values_out, values_reference)


if __name__ == '__main__':
    main()
