import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import cv2
from PySide2.QtQml import *
from PySide2.QtQuickWidgets import QQuickWidget

import PySide2
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWebEngineWidgets import QWebEnginePage

from plotly.offline import plot

import pyqtgraph as pg
import numpy as np
# from . animated_toggle import AnimatedToggle

from resources import *
from modules import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# todo dodanie okna z wykresem po kliknięciu w okno


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class grid_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName(u"grid_page")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.Frame_grid = QFrame(self)
        # self.Frame_grid.setStyleSheet("background-color: rgba(90,90,250,90)")
        self.grid_layout = QGridLayout(self.Frame_grid)
        self.Frame_grid.setLayout(self.grid_layout)

        # Slider na x
        self.Frame_x_slider = QFrame(self.Frame_grid)
        self.Layout_x_slider = QVBoxLayout(self.Frame_x_slider)
        self.Frame_x_slider.setLayout(self.Layout_x_slider)
        self.x_text = QLabel(self.Frame_x_slider)
        self.x_slider = QSlider(Qt.Horizontal)
        self.x_slider.setMinimum(1)
        self.x_slider.setMaximum(99)
        self.x_slider.setValue(50)
        self.Layout_x_slider.addWidget(self.x_text)
        self.Layout_x_slider.addWidget(self.x_slider)

        self.grid_layout.addWidget(self.Frame_x_slider, 0, 1)

        # axis with slices
        self.Frame_axis_slices = QFrame(self.Frame_grid)
        self.Layout_axis_slices = QVBoxLayout(self.Frame_axis_slices)
        self.Frame_axis_slices.setMinimumSize(400, 400)
        self.Frame_axis_slices.setMaximumSize(400, 400)
        self.Frame_axis_slices.setLayout(self.Layout_axis_slices)

        # sc_slices = MplCanvas(self, width=5, height=4, dpi=100)
        # image = cv2.imread('recon_html/figure.png')

        pixmap = QPixmap('recon_html/figure.png')
        label = QLabel()
        label.setPixmap(pixmap)
        label.show()
        # label.show()

        # sc_slices = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888).rgbSwapped()

        self.axis_slices = label
        self.Layout_axis_slices.addWidget(self.axis_slices)

        self.grid_layout.addWidget(self.Frame_axis_slices, 1, 0)

        # axis with slice x
        self.Frame_axis_slice_x = QFrame(self.Frame_grid)
        self.Layout_axis_slice_x = QVBoxLayout(self.Frame_axis_slice_x)
        self.Frame_axis_slice_x.setLayout(self.Layout_axis_slice_x)


        self.axis_slice_x = QLabel()
        self.Frame_axis_slice_x.setMinimumSize(400, 400)
        self.Frame_axis_slice_x.setMaximumSize(400, 400)

        self.Layout_axis_slice_x.addWidget(self.axis_slice_x)

        self.grid_layout.addWidget(self.Frame_axis_slice_x, 1, 1)

        # slider y
        self.Frame_y_slider = QFrame(self.Frame_grid)
        self.Layout_y_slider = QVBoxLayout(self.Frame_y_slider)
        self.Frame_y_slider.setLayout(self.Layout_y_slider)
        self.y_text = QLabel(self.Frame_y_slider)
        self.y_slider = QSlider(Qt.Horizontal)
        self.y_slider.setMinimum(1)
        self.y_slider.setMaximum(99)
        self.y_slider.setValue(50)
        self.Layout_y_slider.addWidget(self.y_text)
        self.Layout_y_slider.addWidget(self.y_slider)

        self.grid_layout.addWidget(self.Frame_y_slider, 0, 2)

        # slider z
        self.Frame_z_slider = QFrame(self.Frame_grid)
        self.Layout_z_slider = QVBoxLayout(self.Frame_y_slider)
        self.Frame_z_slider.setLayout(self.Layout_z_slider)
        self.z_text = QLabel(self.Frame_z_slider)
        self.z_slider = QSlider(Qt.Horizontal)
        self.z_slider.setMinimum(1)
        self.z_slider.setMaximum(99)
        self.z_slider.setValue(50)
        self.Layout_z_slider.addWidget(self.z_text)
        self.Layout_z_slider.addWidget(self.z_slider)

        self.grid_layout.addWidget(self.Frame_z_slider, 0, 3)

        # axis with slice y
        self.Frame_axis_slice_y = QFrame(self.Frame_grid)
        self.Layout_axis_slice_y = QVBoxLayout(self.Frame_axis_slice_y)
        self.Frame_axis_slice_y.setMinimumSize(400, 400)
        self.Frame_axis_slice_y.setMaximumSize(400, 400)
        self.Frame_axis_slice_y.setLayout(self.Layout_axis_slice_y)

        # sc_slice_y = MplCanvas(self, width=5, height=4, dpi=100)

        self.axis_slice_y = QLabel()
        self.Layout_axis_slice_y.addWidget(self.axis_slice_y)

        self.grid_layout.addWidget(self.Frame_axis_slice_y, 1, 2)

        # axis with slice z
        self.Frame_axis_slice_z = QFrame(self.Frame_grid)
        self.Layout_axis_slice_z = QVBoxLayout(self.Frame_axis_slice_z)
        self.Frame_axis_slice_z.setMinimumSize(400, 400)
        self.Frame_axis_slice_z.setMaximumSize(400, 400)
        self.Frame_axis_slice_z.setLayout(self.Layout_axis_slice_z)

        # sc_slice_z = MplCanvas(self, width=5, height=4, dpi=100)

        self.axis_slice_z = QLabel()
        self.Layout_axis_slice_z.addWidget(self.axis_slice_z)

        self.grid_layout.addWidget(self.Frame_axis_slice_z, 1, 3)

#         Wizualizacja pomiarów
        self.Frame_visVoltages = QFrame(self.Frame_grid)
        self.Frame_visVoltages.setMinimumSize(1500, 300)
        self.Frame_visVoltages.setMaximumSize(1500, 300)
        self.Layout_visVoltages = QVBoxLayout(self.Frame_visVoltages)
        self.Frame_grid.setLayout(self.Layout_visVoltages)
        self.vis_text = QLabel()
        self.Layout_visVoltages.addWidget(self.vis_text)
        self.axis_voltages = pg.PlotWidget()
        self.axis_voltages.setBackground('white')
        self.Layout_visVoltages.addWidget(self.axis_voltages)

        self.grid_layout.addWidget(self.Frame_visVoltages, 2, 0, 1, 4)

        font = QFont(u'color: black')

        self.Frame_saveVis = QFrame(self.Frame_grid)
        self.btn_saveVis = QPushButton(self.Frame_saveVis)

        self.btn_saveVis.setMinimumSize(200, 50)
        self.btn_saveVis.setMaximumSize(200, 50)

        self.btn_saveVis.setFont(font)

        self.btn_saveVis.setStyleSheet(u"QPushButton {\n"
                                      " background-color: rgb(147, 186, 249);\n"
                                      "background-repeat: no-repeat;\n"
                                     "border-radius: 10px;\n"
                                     "font-size: 15px;\n"
                                     "}\n"
                                     "QPushButton:hover {\n"
                                     "	background-color: rgb(147, 186, 249);\n"
                                     "}\n"
                                     "QPushButton:pressed {	\n"
                                     "	background-color: rgb(40,40,250);\n"
                                     "}")
        self.btn_saveVis.setFixedSize(150, 50)
                                      # "background-image: url(:/icons/images/icons/download.svg);")
        SaveIcon = QIcon()
        SaveIcon.addFile(u":/icons/images/icons/download.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_saveVis.setIcon(SaveIcon)
        self.btn_saveVis.setIconSize(QSize(40, 40))
        self.btn_saveVis.setEnabled(False)

        # self.btn_saveVis.setFlat(True)
        self.grid_layout.addWidget(self.Frame_saveVis, 0, 0)







