import numpy as np
import pyvista as pv
from io import StringIO
from math import trunc
import open3d as o3d


def convert_xyz_to_array(filename, scale=10):
    """
    Функция конвертации XYZ-файла в массив точек и векторов
    :param filename: название файла для обработки
    :param scale: коэффициент масштабирования
    :return: массив из оригинальных точек, данных для визуализации и векторов
    """

    file_text = open(filename, encoding="cp1251").read().replace(' ', ',')
    point_cloud = np.loadtxt(StringIO(file_text), skiprows=1, delimiter=',', usecols=(1, 2, 3))
    ijk = np.loadtxt(StringIO(file_text), skiprows=1, delimiter=',', usecols=(4, 5, 6))
    origin_data = point_cloud
    visualisation_data = origin_data / scale
    visualisation_data = np.floor(visualisation_data)
    return [origin_data, ijk, visualisation_data]


def plotter(mesh):
    '''
    Функция отрисовки модели
    :param mesh: Данные в формате PolyData
    :return:
    '''
    pl = pv.Plotter()
    pl.add_mesh(mesh)
    _ = pl.add_axes(line_width=5, labels_off=True)
    pl.show()


def create_x_plain(origin_data, x):
    """
    Функция построения плоскостей по x-координате.
    :param origin_data: данные с точками
    :param x: координата x, по которой будет строиться
    :return: возвращается массив с плоскостями-треугольниками
    """

    # Отбираем все точки с x
    polydata = []
    for i in origin_data:
        if i[:][0] == x:
            polydata.append(i)

    # Получаем крайние границы для x и z
    z_max = max(np.array(polydata)[:, 2])
    z_min = min(np.array(polydata)[:, 2])
    y_max = max(np.array(polydata)[:, 1]) - 1
    y_min = min(np.array(polydata)[:, 1]) + 3
    # доп точка для построения
    y_min_e = min(np.array(polydata)[:, 1])

    point1 = 0
    point2 = 0
    point3 = 0
    point4 = 0
    point5 = 0
    #
    # Теперь ищем крайние точки для построения. Код не совсем красивый, знаю))
    # Запускаем 5 циклом отдельно друг от друга и заполняем точки
    #
    for i in range(len(origin_data) - 1):
        if origin_data[i][2] == z_min and origin_data[i][1] == y_min_e and origin_data[i][0] == x:
            point1 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][2] == z_max and origin_data[i][1] == y_max and origin_data[i][0] == x:
            point2 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][2] == z_max and origin_data[i][1] == y_min and origin_data[i][0] == x:
            point3 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][2] == z_min and origin_data[i][1] == y_max and origin_data[i][0] == x:
            point4 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][2] == -59 and origin_data[i][1] == y_min_e and origin_data[i][0] == x:
            point5 = i
            break

    if point5 == 0 and x == 39:
        point5 = len(origin_data) - 1  # На всякий случай, если не заходит в цикл
    faces = [[3, point2, point3, point4],
             [3, point1, point3, point5],
             [3, point3, point1, point4]]
    return faces  # Вот это и есть плоскости


def create_z_plain(origin_data, z):
    """
    Аналогичная функция для построения плоскостей z, работает с применением только 4 точек

    :param origin_data:
    :param z:
    :return:
    """

    polydata = []
    for i in origin_data:
        if i[:][2] == z:
            polydata.append(i)

    x_max = max(np.array(polydata)[:, 0])
    x_min = min(np.array(polydata)[:, 0])
    y_max = max(np.array(polydata)[:, 1])
    y_min = min(np.array(polydata)[:, 1])

    if z <= -59:
        y_min += 1
    if z == -62:
        y_min -= 1
    point1 = 0
    point2 = 0
    point3 = 0
    point4 = 0

    for i in range(len(origin_data) - 1):
        if origin_data[i][0] == x_min and origin_data[i][1] == y_min and origin_data[i][2] == z:
            point1 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][0] == x_max and origin_data[i][1] == y_max and origin_data[i][2] == z:
            point2 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][0] == x_max and origin_data[i][1] == y_min and origin_data[i][2] == z:
            point3 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][0] == x_min and origin_data[i][1] == y_max and origin_data[i][2] == z:
            point4 = i
            break

    faces = [[3, point1, point2, point3],
             [3, point1, point2, point4],
             [3, point2, point1, point4]]
    return faces


def create_y_plain(origin_data, y):
    polydata = []
    for i in origin_data:
        if i[:][1] == y:
            polydata.append(i)

    point1 = 0
    point2 = 0
    point3 = 0
    point4 = 0

    x_max = max(np.array(polydata)[:, 0]) - 1
    x_min = min(np.array(polydata)[:, 0]) + 1
    z_max = max(np.array(polydata)[:, 2])
    z_min = min(np.array(polydata)[:, 2])

    for i in range(len(origin_data) - 1):
        if origin_data[i][0] == x_min and origin_data[i][1] == y and origin_data[i][2] == z_min:
            point1 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][0] == x_max and origin_data[i][1] == y and origin_data[i][2] == z_max:
            point2 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][0] == x_max and origin_data[i][1] == y and origin_data[i][2] == z_min:
            point3 = i
            break
    for i in range(len(origin_data) - 1):
        if origin_data[i][0] == x_min and origin_data[i][1] == y and origin_data[i][2] == z_max:
            point4 = i
            break

    faces = [[3, point1, point2, point3],
             [3, point1, point2, point4],
             [3, point2, point1, point4]]
    return faces


def main():
    filename = "data3.xyz"
    output_name = "output.obj"
    visualisation = "show"
    origin_data = convert_xyz_to_array(filename, 15)[2][:]

    polydata = []
    # Корректируем данные, удаляем и прибавляем точки
    for i in origin_data:
        polydata.append(i)
        if i[1] == 37 and i[2] != -62:
            i[1] -= 1
            i[2] -= 1
        if i[1] == 38 and i[0] == 37:
            i[1] -= 9
    polydata.append([38, 30, -59])
    polydata.append([39, 30, -59])
    polydata.append([39, 33.5, -59.5])
    polydata.append([33, 33.5, -59.5])
    polydata.append([33, 33.5, -58])
    polydata.append([33, 33.5, -61])

    origin_data = polydata
    faces = []
    pl = pv.Plotter()

    # Здесь начинается построение
    for x in range(34, 39):
        faces.append(create_x_plain(origin_data, x))
    faces.append(create_z_plain(origin_data, -56))
    faces.append(create_z_plain(origin_data, -62))
    faces.append(create_y_plain(origin_data, 36))

    pl = pv.Plotter()
    polydata = pv.PolyData(polydata)

    faces.append([[3, 1, 81, 620],
                  [3, 631, 1, 620],
                  [3, 1, 1, 1]])

    faces.append([[3, 110, 631, 1],
                  [3, 110, 101, 1],
                  [3, 1, 1, 1]])
    polydata.faces = faces
    c = pv.Tube(origin_data[632], origin_data[633], radius=1.5, n_sides=100)
    pl.add_mesh(c)
    if visualisation == "show":
        pl.add_mesh(polydata)
        _ = pl.add_axes(line_width=5, labels_off=False)
        pl.export_obj("final_mesh")
        pl.show()


if __name__ == "__main__":
    main()
