import numpy as np
import pyvista as pv
from io import StringIO
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

if __name__ == "__main__":
    origin_data = convert_xyz_to_array("data3.xyz", 15)[2][:]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(convert_xyz_to_array("data3.xyz", 15)[2][:])
    pcd.normals = o3d.utility.Vector3dVector(convert_xyz_to_array("data3.xyz", 15)[1][:])

    poisson_mesh = \
    o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]
    bbox = pcd.get_axis_aligned_bounding_box()
    p_mesh_crop = poisson_mesh.crop(bbox)

    o3d.io.write_triangle_mesh("mesh_triangle.obj", p_mesh_crop)
    mesh = pv.read("teapot.ply")
    pl = pv.Plotter()
    pl.add_mesh(mesh)
    pl.show()