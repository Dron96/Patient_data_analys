import psycopg2
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('agg')


def get_description_data(exam_id):
    file = np.round(get_exam_data(exam_id), 3)

    ideal_file = ideal_data(exam_id)

    # Рассчитаем длину идеальной "эталонной" линии
    # Найдем разности между соседними членами массивов координат X и Y
    ideal_x = np.diff(ideal_file.x)
    ideal_y = np.diff(ideal_file.y)
    # Возведем разности в квадрат
    ideal_x = np.power(ideal_x, 2)
    ideal_y = np.power(ideal_y, 2)
    # Посчитаем сумму двух массивов, получим формулу:
    # (x2 - x1)^2 + (y2 - y1)^2
    ideal_sum = ideal_x + ideal_y
    # Вычислим квадратный корень и посчитаем сумму, получим длину всей линии
    ideal_sum = np.sqrt(ideal_sum)
    length_ideal = np.sum(ideal_sum)

    # Рассчитаем длину линии пациента
    # Найдем разности между соседними членами массивов координат X и Y
    patient_x = np.diff(file.x)
    patient_y = np.diff(file.y)
    # Возведем разности в квадрат
    patient_x = np.power(patient_x, 2)
    patient_y = np.power(patient_y, 2)
    # Посчитаем сумму двух массивов, получим формулу:
    # (x2 - x1)^2 + (y2 - y1)
    patient_sum = patient_x + patient_y
    # Вычислим квадратный корень и посчитаем сумму, получим длину всей линии
    patient_sum = np.sqrt(patient_sum)
    length_patient = np.sum(patient_sum)

    # Рассчитаем среднюю скорость рисования данного пациента
    # 1) Посчитаем время, потраченное на рисование всей спирали
    patient_time = file.t[file.t.shape[0] - 1] - file.t[0]
    # 2) Разделим длину линии на затраченное время
    patient_speed = length_patient / patient_time

    # Рассчитаем расстояние между витками спирали пациента
    data_nearest = nearest_dots(file, ideal_file, get_spiral_type(exam_id))
    nearest_y = data_nearest['nearest_y']
    nearest_x = data_nearest['nearest_x']

    # Находим расстояние между спиралями
    # Отсортируем точки по координате
    nearest_x = nearest_x.sort_values(by='y')
    nearest_y = nearest_y.sort_values(by='x')
    # Рассчитаем расстояние между отдельными витками
    # Найдем разности между соседними членами массивов по координате X
    distance_between_loop_x = np.diff(nearest_x.x)
    distance_between_loop_y = np.diff(nearest_x.y)
    # Возведем разности в квадрат
    distance_between_loop_x = np.power(distance_between_loop_x, 2)
    distance_between_loop_y = np.power(distance_between_loop_y, 2)
    # Посчитаем сумму двух массивов, получим формулу:
    # (x2 - x1)^2 + (y2 - y1)
    distance_between_loop_sum = distance_between_loop_x + distance_between_loop_y
    # Вычислим квадратный корень и посчитаем сумму, получим длину всей линии
    distance_between_loop = np.sqrt(distance_between_loop_sum)
    mean_distance_between_loop_x = np.mean(distance_between_loop)
    std_distance_between_loop_x = np.std(distance_between_loop)

    # Тоже самое по координате Y
    # Найдем разности между соседними членами массивов по координате X
    distance_between_loop_x = np.diff(nearest_y.x)
    distance_between_loop_y = np.diff(nearest_y.y)
    # Возведем разности в квадрат
    distance_between_loop_x = np.power(distance_between_loop_x, 2)
    distance_between_loop_y = np.power(distance_between_loop_y, 2)
    # Посчитаем сумму двух массивов, получим формулу:
    # (x2 - x1)^2 + (y2 - y1)
    distance_between_loop_sum = distance_between_loop_x + distance_between_loop_y
    # Вычислим квадратный корень и посчитаем сумму, получим длину всей линии
    distance_between_loop = np.sqrt(distance_between_loop_sum)
    mean_distance_between_loop_y = np.mean(distance_between_loop)
    std_distance_between_loop_y = np.std(distance_between_loop)

    results = [length_ideal,
               length_patient,
               patient_speed,
               mean_distance_between_loop_x,
               std_distance_between_loop_x,
               mean_distance_between_loop_y,
               std_distance_between_loop_y]

    index = ['Длина контрольной линии',
             'Длина линии пациента',
             'Средняя скорость рисования пациента',
             'Среднее расстояние между витками (X=const)',
             'Стандартное отклонение расстояния между витками (X=const)',
             'Среднее расстояние между витками (Y=const)',
             'Стандартное отклонение расстояния между витками (Y=const)']

    total = pd.DataFrame({'Результаты': results}, index=index)
    total = np.round(total, 1)

    return total


def get_graph(exam_id):
    file = np.round(get_exam_data(exam_id), 3)
    ideal_file = ideal_data(exam_id)

    data = nearest_dots(file, ideal_file, get_spiral_type(exam_id))
    nearest_y = data['nearest_y']
    nearest_x = data['nearest_x']

    fig, ax = plt.subplots()
    # ключ цвета из {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}:
    ax.plot(file.x, file.y, c='r')
    # hex RGB:
    ax.scatter(nearest_x.x, nearest_x.y, c='b')
    # hex RGB:
    ax.scatter(nearest_y.x, nearest_y.y, c='g')
    ax.set_facecolor('white')
    ax.set_title('')
    fig.set_figwidth(8)  # ширина и
    fig.set_figheight(8)  # высота "Figure"
    return plt


def nearest_dots(file, ideal_file, spiral_type):
    # Определяем сколько точек нужно найти в зависимости от типа спирали
    if spiral_type == 'Sp':
        n = 6
    elif spiral_type == 'Cp':
        n = 5
    elif spiral_type == 'In':
        n = 6
    else:
        n = 6

    # Возьмем центр спирали, как начальная точка "эталонной" спирали
    spiral_center = (ideal_file.x[0], ideal_file.y[0])
    # Найдем отклонения X от центра спирали и отсортируем по модулю
    deviation_x = file.x - spiral_center[0]
    deviation_x = abs(deviation_x)
    # Отберем 20 измерений, наиболее близких к заданному Y
    nearest_x = deviation_x.sort_values(ascending=True)[:50].index
    nearest_x = file.iloc[nearest_x]
    nearest_x['diff'] = np.insert(abs(np.diff(nearest_x['y'])), 0, 0)  # Измерим расстояние между данными точками
    nearest_x = nearest_x.query("diff > 20 | diff == 0")  # Расстояние между точками должно быть > 20
    nearest_x.index = pd.to_numeric(nearest_x.index)
    ind = nearest_x.index.values
    # Удалим те точки, которые по индексу близки друг к другу, то есть различаются меньше, чем на 10
    delete = dict()
    for i in range(len(ind)):
        for j in range(len(ind)):
            if (i != j) and (abs(float(ind[i]) - float(ind[j])) < 10) and (ind[j] not in delete.keys()) and (
                    ind[j] not in delete.values()):
                delete[ind[j]] = ind[i]
    nearest_x = nearest_x.drop(delete.keys(), axis=0)[:n]

    # Повторим тоже самое для Y
    deviation_y = file.y - spiral_center[1]
    deviation_y = abs(deviation_y)
    # Отберем 20 измерений, наиболее близких к заданному Y
    nearest_y = deviation_y.sort_values(ascending=True)[:50].index
    nearest_y = file.iloc[nearest_y]
    nearest_y['diff'] = np.insert(abs(np.diff(nearest_y['x'])), 0, 0)  # Измерим расстояние между данными точками
    nearest_y = nearest_y.query("diff > 20 | diff == 0")  # Расстояние между точками должно быть > 20
    nearest_y.index = pd.to_numeric(nearest_y.index)
    ind = nearest_y.index.values
    # Удалим те точки, которые по инексу близки друг к другу, то есть различаются меньше, чем на 10
    delete = dict()
    for i in range(len(ind)):
        for j in range(len(ind)):
            if (i != j) and (abs(ind[i] - ind[j]) < 10) and (ind[j] not in delete.keys()) and (
                    ind[j] not in delete.values()):
                delete[ind[j]] = ind[i]
    nearest_y = nearest_y.drop(delete.keys(), axis=0)[:n]

    return {'nearest_x': nearest_x, 'nearest_y': nearest_y}


def get_exam_data(exam_id):
    conn = psycopg2.connect(
        dbname='spiral',
        user='dron',
        host='127.0.0.1',
        port='5432')
    cursor = conn.cursor()
    cursor.execute('SELECT x,y,t FROM examinations WHERE id = {}'.format(exam_id))
    records = cursor.fetchall()
    x = list(map(float, records[0][0].replace('[', '').replace(']', '').replace('"', '').split(', ')))
    y = list(map(float, records[0][1].replace('[', '').replace(']', '').replace('"', '').split(', ')))
    y = list(map(lambda i: -1 * i, y))
    t = list(map(float, records[0][2].replace('[', '').replace(']', '').replace('"', '').split(', ')))
    # print(x)
    # print(y)
    # print(t)
    df = pd.DataFrame.from_dict({'x': x, 'y': y, 't': t})
    df = np.round(df, 3)

    return df


def get_spiral_type(exam_id):
    conn = psycopg2.connect(
        dbname='spiral',
        user='dron',
        host='127.0.0.1',
        port='5432')
    cursor = conn.cursor()
    cursor.execute('SELECT spiral_type FROM examinations WHERE id = {}'.format(exam_id))
    records = cursor.fetchall()

    return records[0][0]


def ideal_data(exam_id):
    spiral_type = get_spiral_type(exam_id)
    if spiral_type == 'Sp':
        ideal = './spiral.txt'
    elif spiral_type == 'Cp':
        ideal = './copy_spiral.txt'
    elif spiral_type == 'In':
        ideal = './1200_1794.csv'
    else:
        ideal = './1200_1794.csv'
    names_ideal = ['x', 'y']
    ideal_file = pd.read_csv(ideal, header=None, names=names_ideal)
    ideal_file = np.round(ideal_file, 3)
    ideal_file.y = ideal_file.y * -1

    return ideal_file
