import psycopg2
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')


def get_description_data(exam_id):
    file = np.round(get_exam_data(exam_id), 3)

    ideal_file = ideal_data()

    # Рассчитаем длину идеальной "эталонной" линии
    # Найдем разности между соседними членами массивов координат X и Y
    IdealX = np.diff(ideal_file.x)
    IdealY = np.diff(ideal_file.y)
    # Возведем разности в квадрат
    IdealX = np.power(IdealX, 2)
    IdealY = np.power(IdealY, 2)
    # Посчитаем сумму двух массивов, получим формулу:
    # (x2 - x1)^2 + (y2 - y1)
    IdealSum = IdealX + IdealY
    # Вычислим квадратный корень и посчитаем сумму, получим длину всей линии
    IdealSum = np.sqrt(IdealSum)
    lengthIdeal = np.sum(IdealSum)

    # Рассчитаем длину линии пациента
    # Найдем разности между соседними членами массивов координат X и Y
    PacientX = np.diff(file.x)
    PacientY = np.diff(file.y)
    # Возведем разности в квадрат
    PacientX = np.power(PacientX, 2)
    PacientY = np.power(PacientY, 2)
    # Посчитаем сумму двух массивов, получим формулу:
    # (x2 - x1)^2 + (y2 - y1)
    PacientSum = PacientX + PacientY
    # Вычислим квадратный корень и посчитаем сумму, получим длину всей линии
    PacientSum = np.sqrt(PacientSum)
    lengthPacient = np.sum(PacientSum)

    # Рассчитаем среднюю скорость рисования данного пациента
    # 1) Посчитаем время, потраченное на рисование всей спирали
    PacientTime = file.t[file.t.shape[0] - 1] - file.t[0]
    # 2) Разделим длину линии на затраченное время
    PacientSpeed = lengthPacient / PacientTime

    # Рассчитаем расстояние между витками спирали пациента
    data_nearest = nearest_dots(file, ideal_file)
    nearestY = data_nearest['nearestY']
    nearestX = data_nearest['nearestX']

    # Находим расстояние между спиралями
    # Отсортируем точки по координате
    nearestX = nearestX.sort_values(by='y')
    nearestY = nearestY.sort_values(by='x')
    # Рассчитаем расстояние между отдельными витками
    # Найдем разности между соседними членами массивов по координате X
    distanceBetweenLoopX = np.diff(nearestX.x)
    distanceBetweenLoopY = np.diff(nearestX.y)
    # Возведем разности в квадрат
    distanceBetweenLoopX = np.power(distanceBetweenLoopX, 2)
    distanceBetweenLoopY = np.power(distanceBetweenLoopY, 2)
    # Посчитаем сумму двух массивов, получим формулу:
    # (x2 - x1)^2 + (y2 - y1)
    distanceBetweenLoopSum = distanceBetweenLoopX + distanceBetweenLoopY
    # Вычислим квадратный корень и посчитаем сумму, получим длину всей линии
    distanceBetweenLoop = np.sqrt(distanceBetweenLoopSum)
    meanDistanceBetweenLoopX = np.mean(distanceBetweenLoop)
    stdDistanceBetweenLoopX = np.std(distanceBetweenLoop)

    # Тоже самое по координате Y
    # Найдем разности между соседними членами массивов по координате X
    distanceBetweenLoopX = np.diff(nearestY.x)
    distanceBetweenLoopY = np.diff(nearestY.y)
    # Возведем разности в квадрат
    distanceBetweenLoopX = np.power(distanceBetweenLoopX, 2)
    distanceBetweenLoopY = np.power(distanceBetweenLoopY, 2)
    # Посчитаем сумму двух массивов, получим формулу:
    # (x2 - x1)^2 + (y2 - y1)
    distanceBetweenLoopSum = distanceBetweenLoopX + distanceBetweenLoopY
    # Вычислим квадратный корень и посчитаем сумму, получим длину всей линии
    distanceBetweenLoop = np.sqrt(distanceBetweenLoopSum)
    meanDistanceBetweenLoopY = np.mean(distanceBetweenLoop)
    stdDistanceBetweenLoopY = np.std(distanceBetweenLoop)

    results = [lengthIdeal,
               lengthPacient,
               PacientSpeed,
               meanDistanceBetweenLoopX,
               stdDistanceBetweenLoopX,
               meanDistanceBetweenLoopY,
               stdDistanceBetweenLoopY]

    index = ['Длина "эталонной" линии',
             'Длина линии пациента',
             'Средняя скорость рисования пациента',
             'Среднее расстояние между витками (X=const)',
             'Стандартное отклонение расстояния между витками (X=const)',
             'Среднее расстояние между витками (Y=const)',
             'Стандартное отклонение расстояния между витками (Y=const)']

    total = pd.DataFrame({'Результаты': results}, index=index)

    return total


def get_graph(exam_id):
    file = np.round(get_exam_data(exam_id), 3)
    ideal_file = ideal_data()

    data = nearest_dots(file, ideal_file)
    nearestY = data['nearestY']
    nearestX = data['nearestX']

    fig, ax = plt.subplots()
    # ключ цвета из {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}:
    ax.plot(file.x, file.y, c='r')
    # hex RGB:
    ax.scatter(nearestX.x, nearestX.y, c='b')
    # hex RGB:
    ax.scatter(nearestY.x, nearestY.y, c='g')
    ax.set_facecolor('white')
    ax.set_title('')
    fig.set_figwidth(8)  # ширина и
    fig.set_figheight(8)  # высота "Figure"
    return plt


def nearest_dots(file, ideal_file):
    # Возьмем центр спирали, как начальная точка "эталонной" спирали
    spiralCenter = (ideal_file.x[0], ideal_file.y[0])
    # Найдем отклонения X от центра спирали и отсортируем по модулю
    deviationX = file.x - spiralCenter[0]
    deviationX = abs(deviationX)
    # Отберем 20 измерений, наиболее близких к заданному Y
    nearestX = deviationX.sort_values(ascending=True)[:20].index
    nearestX = file.iloc[nearestX]
    nearestX['diff'] = np.insert(abs(np.diff(nearestX['y'])), 0, 0)  # Измерим расстояние между данными точками
    nearestX = nearestX.query("diff > 20 | diff == 0")  # Расстояние между точками должно быть > 20
    nearestX.index = pd.to_numeric(nearestX.index)
    ind = nearestX.index.values
    # Удалим те точки, которые по индексу близки друг к другу, то есть различаются меньше, чем на 10
    delete = dict()
    for i in range(len(ind)):
        for j in range(len(ind)):
            if (i != j) and (abs(float(ind[i]) - float(ind[j])) < 10) and (ind[j] not in delete.keys()) and (
                    ind[j] not in delete.values()):
                delete[ind[j]] = ind[i]
    nearestX = nearestX.drop(delete.keys(), axis=0)[:6]

    # Повторим тоже самое для Y
    deviationY = file.y - spiralCenter[1]
    deviationY = abs(deviationY)
    # Отберем 20 измерений, наиболее близких к заданному Y
    nearestY = deviationY.sort_values(ascending=True)[:20].index
    nearestY = file.iloc[nearestY]
    nearestY['diff'] = np.insert(abs(np.diff(nearestY['x'])), 0, 0)  # Измерим расстояние между данными точками
    nearestY = nearestY.query("diff > 20 | diff == 0")  # Расстояние между точками должно быть > 20
    nearestY.index = pd.to_numeric(nearestY.index)
    ind = nearestY.index.values
    # Удалим те точки, которые по инексу близки друг к другу, то есть различаются меньше, чем на 10
    delete = dict()
    for i in range(len(ind)):
        for j in range(len(ind)):
            if (i != j) and (abs(ind[i] - ind[j]) < 10) and (ind[j] not in delete.keys()) and (
                    ind[j] not in delete.values()):
                delete[ind[j]] = ind[i]
    nearestY = nearestY.drop(delete.keys(), axis=0)

    return {'nearestX': nearestX, 'nearestY': nearestY}


def get_exam_data(exam_id):
    conn = psycopg2.connect(
        dbname='spiral',
        user='dron',
        host='127.0.0.1',
        port='5432')
    cursor = conn.cursor()
    cursor.execute('SELECT data FROM examinations WHERE id = {}'.format(exam_id))
    records = cursor.fetchall()
    df = pd.DataFrame.from_dict(records[0][0])

    return df


def ideal_data():
    ideal = './1200_1794.csv'
    names_ideal = ['x', 'y']
    ideal_file = pd.read_csv(ideal, header=None, names=names_ideal)
    ideal_file = ideal_file.iloc[:1025]
    ideal_file = np.round(ideal_file, 3)

    return ideal_file
