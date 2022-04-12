import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from stl import mesh as m
import open3d as o3d

import design


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.filepath = ""
        self.setupUi(self)
        self.openfile_btn.clicked.connect(self.browse_folder)
        self.eval_btn.clicked.connect(self.get_info)
        self.savecad_btn.clicked.connect(self.save_model)
        self.demonstate_btn.clicked.connect(self.visualise)

    def browse_folder(self):
        self.filepath = ""
        self.evalresult_text.setPlainText("")
        filename = QFileDialog.getOpenFileName(self)[0]
        if filename.split(".")[-1] == "stl":
            self.filepath = filename
            self.filepath_text.setPlainText(self.filepath)
            self.name = self.filepath.split("/")[-1]
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Этот файл не поддерживается")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

    def get_info(self):
        if self.filepath == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Файл не был загружен")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            self.raw_mesh = m.Mesh.from_file(self.filepath)
            point_number = self.raw_mesh.points.__len__()
            self.evalresult_text.setPlainText("Название: {}\nКоличество точек: {}".format(self.name, point_number))

    def save_model(self):
        if self.filepath == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Файл не был загружен")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            self.raw_mesh = m.Mesh.from_file(self.filepath)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(self.raw_mesh.points[:, :3])
            pcd.normals = o3d.utility.Vector3dVector(self.raw_mesh.normals)

            poisson_mesh = \
                o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1,
                                                                          linear_fit=False)[0]
            bbox = pcd.get_axis_aligned_bounding_box()
            mesh = poisson_mesh.crop(bbox)
            o3d.io.write_triangle_mesh(self.name[:-4] + ".obj", mesh)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Загрузка завершена!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

    def visualise(self):
        if self.filepath == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Файл не был загружен")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            self.raw_mesh = m.Mesh.from_file(self.filepath)
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(self.raw_mesh.points[:, :3])
            pcd.normals = o3d.utility.Vector3dVector(self.raw_mesh.normals)

            poisson_mesh = \
                o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1,
                                                                          linear_fit=False)[0]
            bbox = pcd.get_axis_aligned_bounding_box()
            mesh = poisson_mesh.crop(bbox)

            o3d.visualization.draw_geometries([mesh])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()
