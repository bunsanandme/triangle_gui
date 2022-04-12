import open3d as o3d
from stl import mesh
import pyvista as pv

if __name__ == "__main__":
    your_mesh = mesh.Mesh.from_file('mesh2.stl')
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(your_mesh.points[:, :3])
    pcd.normals = o3d.utility.Vector3dVector(your_mesh.normals)

    poisson_mesh = \
        o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]
    bbox = pcd.get_axis_aligned_bounding_box()
    mesh = poisson_mesh.crop(bbox)
    o3d.io.write_triangle_mesh("triangle_mesh.obj", mesh)
    mesh = pv.read("triangle_mesh.obj")
    pl = pv.plotter()
    pl.add_mesh(mesh)
    pl.show()
