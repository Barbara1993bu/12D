import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
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

# todo dodanie wyboru między metodami rekonstrukcji
# rekonstrukcja liniowa i rekonstrukcja różnicowa


class PlotlyWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        # super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.webview = QWebEngineView(self)
        self.webview.setObjectName(u"webVieW")
        # self.webview.setContent(QByteArray(100,100))

        # self.webview.load(QtCore.QUrl(r'D:\Aplikacje_pyQt\Od_Bartka_app\app\recon_html\figure.html'))
        # self.webview.show()
        # self.webview.url()

        self.layout.addWidget(self.webview)


class reconstruction_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout reconstruction EIT
        self.Frame_page2 = QFrame(self)
        # self.Frame_page2.setStyleSheet("background-color: rgba(90,90,250,90)")
        self.girdLayoutNewPage2 = QGridLayout(self.Frame_page2)
        self.Frame_page2.setLayout(self.girdLayoutNewPage2)
        self.girdLayoutNewPage2.setObjectName(u"girdLayoutNewPage")

        self.Frame_mesh = QFrame(self.Frame_page2)
        self.Layout_mesh = QVBoxLayout(self.Frame_mesh)
        self.Frame_mesh.setLayout(self.Layout_mesh)
        self.Frame_mesh.setMinimumSize(10, 10)
        self.Frame_mesh.setMinimumSize(700, 700)

        self.inputGraph = PlotlyWidget()
        # self.inputGraph = PlotlyWidget(self.Frame_mesh)
        self.inputGraph.setLayout(self.Layout_mesh)
        self.inputGraph.setMinimumSize(100, 100)
        self.inputGraph.setMaximumSize(1000, 1000)



        # self.inputGraph.setSource

        self.Layout_mesh.addWidget(self.inputGraph)

        self.girdLayoutNewPage2.addWidget(self.Frame_mesh, 1, 0)

        # Slidery to rotate mesh
        self.Frame_sliderVertical = QFrame(self.Frame_page2)
        self.Layout_sliderVertical = QVBoxLayout(self.Frame_sliderVertical)
        self.Frame_sliderVertical.setLayout(self.Layout_sliderVertical)
        self.Label_sliderVertical = QLabel()
        self.Label_sliderVertical.setText('z')
        self.Label_sliderVertical.setStyleSheet("color: black;"
                                                "font: bold;"
                                                "font-size: 15px")
        self.Label_sliderVertical.setMinimumSize(10, 10)
        self.Label_sliderVertical.setMaximumSize(800, 20)
        self.Layout_sliderVertical.addWidget(self.Label_sliderVertical)
        self.sliderVertical = QSlider(Qt.Vertical)
        self.sliderVertical.setMinimum(-180)
        self.sliderVertical.setMaximum(180)
        self.sliderVertical.setValue(0)
        self.sliderVertical.setMinimumSize(10, 10)
        self.sliderVertical.setMaximumSize(10, 800)
        self.Layout_sliderVertical.addWidget(self.sliderVertical)
        self.girdLayoutNewPage2.addWidget(self.Frame_sliderVertical, 1, 1)

        self.Frame_sliderHorizontal = QFrame(self.Frame_page2)
        self.Layout_sliderHorizontal = QHBoxLayout(self.Frame_sliderHorizontal)

        self.Frame_sliderHorizontal.setLayout(self.Layout_sliderHorizontal)

        self.Label_sliderHorizontal = QLabel()
        self.Label_sliderHorizontal.setText('x')
        self.Label_sliderHorizontal.setStyleSheet("color: black;"
                                                  "font: bold;"
                                                  "font-size: 15px")
        self.Label_sliderHorizontal.setMinimumSize(10, 10)
        self.Label_sliderHorizontal.setMaximumSize(20, 20)
        self.Layout_sliderHorizontal.addWidget(self.Label_sliderHorizontal)

        self.sliderHorizontal = QSlider(Qt.Horizontal)
        self.sliderHorizontal.setMinimumSize(10, 10)
        self.sliderHorizontal.setMaximumSize(700, 50)
        self.sliderHorizontal.setMinimum(-180)
        self.sliderHorizontal.setMaximum(180)
        self.sliderHorizontal.setValue(0)
        self.Layout_sliderHorizontal.addWidget(self.sliderHorizontal)

        self.girdLayoutNewPage2.addWidget(self.Frame_sliderHorizontal, 2, 0)

        # PushButtons defined mesh model
        self.Frame_parameters_of_reconstruction = QFrame(self.Frame_page2)
        self.Layout_parameters_of_reconstruction = QVBoxLayout(self.Frame_parameters_of_reconstruction)
        self.Frame_parameters_of_reconstruction.setLayout(self.Layout_parameters_of_reconstruction)

        self.girdLayoutNewPage2.addWidget(self.Frame_parameters_of_reconstruction, 1, 2, 2, 1)

        self.btn_Model = QPushButton(self.Frame_parameters_of_reconstruction)
        self.btn_Model.setObjectName(u"btn_Model")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.btn_Model.sizePolicy().hasHeightForWidth())
        self.btn_Model.setSizePolicy(sizePolicy)
        self.btn_Model.setMinimumSize(QSize(0, 50))
        self.btn_Model.setMaximumSize(QSize(200, 50))
        self.btn_Model.setStyleSheet(u"QPushButton {\n"
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
        self.btn_Model.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_Model.setLayoutDirection(Qt.LeftToRight)

        self.Frame_load_model = QFrame(self.Frame_parameters_of_reconstruction)
        self.Frame_load_model.setFixedSize(500, 100)
        self.Layout_load_model = QHBoxLayout(self.Frame_load_model)
        self.Frame_load_model.setLayout(self.Layout_load_model)

        self.Label_load_model = QLabel(self.Frame_load_model)
        self.Label_load_model.setFixedSize(300, 100)
        self.Layout_load_model.addWidget(self.Label_load_model)
        self.Layout_load_model.addWidget(self.btn_Model)

        self.Layout_parameters_of_reconstruction.addWidget(self.Frame_load_model)

        # PushButton load voltages
        self.btn_voltages_EIT = QPushButton(self.Frame_parameters_of_reconstruction)
        self.btn_voltages_EIT.setObjectName(u"btn_voltages_EIT")
        sizePolicy.setHeightForWidth(self.btn_voltages_EIT.sizePolicy().hasHeightForWidth())
        self.btn_voltages_EIT.setSizePolicy(sizePolicy)
        self.btn_voltages_EIT.setMinimumSize(QSize(0, 50))
        self.btn_voltages_EIT.setMaximumSize(QSize(200, 50))
        self.btn_voltages_EIT.setStyleSheet(u"QPushButton {\n"
                                            "	background-color: rgb(147, 186, 249);\n"
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

        self.btn_voltages_EIT.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_voltages_EIT.setLayoutDirection(Qt.LeftToRight)

        self.Frame_load_Voltages = QFrame(self.Frame_parameters_of_reconstruction)
        self.Frame_load_Voltages.setFixedSize(500, 100)
        self.Layout_load_Voltages = QHBoxLayout(self.Frame_load_Voltages)
        self.Frame_load_Voltages.setLayout(self.Layout_load_Voltages)

        self.Label_load_Voltages = QLabel(self.Frame_load_Voltages)
        self.Label_load_Voltages.setFixedSize(300, 100)
        self.Layout_load_Voltages.addWidget(self.Label_load_Voltages)
        self.Layout_load_Voltages.addWidget(self.btn_voltages_EIT)

        self.Layout_parameters_of_reconstruction.addWidget(self.Frame_load_Voltages)

        # Parameters of reconstruction
        self.label_txt_method_reconstruction = QLabel(self.Frame_parameters_of_reconstruction)
        self.label_txt_method_reconstruction.setSizePolicy(sizePolicy)
        self.label_txt_method_reconstruction.setFixedSize(500, 50)

        self.label_txt_method_reconstruction.setStyleSheet("color: black;"
                                                           "font: bold;"
                                                           "font-size: 15px")

        self.Method_of_reconstruction = QComboBox(self.Frame_parameters_of_reconstruction)
        self.Method_of_reconstruction.setStyleSheet("color: white;"
                                                    "background-color: rgb(147, 186, 249);"
                                                    "selection-color: red;"
                                                    "selection-background-color: rgb(40,40,250);")
        self.Method_of_reconstruction.setFixedSize(500, 50)

        self.Layout_parameters_of_reconstruction.addWidget(self.label_txt_method_reconstruction)
        self.Layout_parameters_of_reconstruction.addWidget(self.Method_of_reconstruction)

        # Parameters of reconstruction
        # self.Frame_parameters_of_reconstruction = QFrame(self.Frame_Data_Recon)
        # self.Frame_parameters_of_reconstruction.setMinimumSize(100, 100)
        # self.Frame_parameters_of_reconstruction.setMaximumSize(600, 600)
        # self.Frame_Data_Recon_Layout.addWidget(self.Frame_parameters_of_reconstruction)
        # self.Layout_parameters_of_reconstruction = QGridLayout(self.Frame_parameters_of_reconstruction)
        # self.Frame_parameters_of_reconstruction.setLayout(self.Layout_parameters_of_reconstruction)

        self.label_txt_number_of_iteration = QLabel(self.Frame_parameters_of_reconstruction)
        self.label_txt_number_of_iteration.setSizePolicy(sizePolicy)
        self.label_txt_number_of_iteration.setFixedSize(500, 50)
        self.label_txt_number_of_iteration.setStyleSheet("color: black;"
                                                         "font: bold;"
                                                         "font-size: 15px")
        self.Layout_parameters_of_reconstruction.addWidget(self.label_txt_number_of_iteration)

        self.qdial_number_of_iteration = ValueDial(self.Frame_parameters_of_reconstruction)

        self.qdial_number_of_iteration.setMinimumSize(100, 100)
        self.qdial_number_of_iteration.setMaximumSize(150, 150)
        self.qdial_number_of_iteration.setStyleSheet("QDial { background-color: blue; color: green}")
        self.qdial_number_of_iteration.setStyleSheet(
            "QDial { background-color: rgb(0, 0, 200); selection-background-color: rgb(230, 100, 7)}")
        # self.qdial_number_of_iteration.setStyle("color: red")

        self.Layout_parameters_of_reconstruction.addWidget(self.qdial_number_of_iteration)

        self.label_txt_regularyzation_parameter = QLabel(self.Frame_parameters_of_reconstruction)
        self.label_txt_regularyzation_parameter.setSizePolicy(sizePolicy)
        self.label_txt_regularyzation_parameter.setFixedSize(500, 50)
        self.label_txt_regularyzation_parameter.setStyleSheet("color: black;"
                                                              "font: bold;"
                                                              "font-size: 15px")
        self.Layout_parameters_of_reconstruction.addWidget(self.label_txt_regularyzation_parameter)

        self.QcomboBox_regularyzation_parameter = QComboBox(self.Frame_parameters_of_reconstruction)
        self.QcomboBox_regularyzation_parameter.setStyleSheet("color: white;"
                                                              "background-color: rgb(147, 186, 249);"
                                                              "selection-color: red;"
                                                              "selection-background-color: rgb(40,40,250);")

        self.Layout_parameters_of_reconstruction.addWidget(self.QcomboBox_regularyzation_parameter)

        self.btn_reconstruction = QPushButton(self.Frame_parameters_of_reconstruction)
        self.btn_reconstruction.setObjectName(u"btn_reconstruction")
        sizePolicy.setHeightForWidth(self.btn_reconstruction.sizePolicy().hasHeightForWidth())
        self.btn_reconstruction.setSizePolicy(sizePolicy)
        self.btn_reconstruction.setFixedSize(200, 50)
        # self.btn_reconstruction.setFixedSize(200,50)
        # self.btn_reconstruction.setStyleSheet("border-radius: 10px;")
        # self.btn_reconstruction.setStyleSheet(u"border-radius: 10px;")
        self.btn_reconstruction.setStyleSheet(u"QPushButton {\n"
                                              "	background-color: rgb(147, 186, 249);\n"
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


        self.Layout_parameters_of_reconstruction.addWidget(self.btn_reconstruction)

        self.Info_box = QTextEdit()
        self.Info_box.setObjectName(u"info_box")
        self.Info_box.setStyleSheet(u"color: rgb(0,0,0);"
                                    "border: 1px solid rgb(255,255,255);"
                                    "backgraund-color: rgb(255,255,255);")
        self.Info_box.setMinimumSize(QSize(1000, 40))
        self.Info_box.setMaximumSize(QSize(1000, 40))

        self.Info_box.insertPlainText(" ")
        self.Info_box.setTextCursor(QTextCursor(self.Info_box.document()))
        self.Info_box.moveCursor(QTextCursor.Start)
        self.Info_box.insertPlainText('Information ' + '\n')
        # self.Info_box.setTextInteractionFlags()

        self.girdLayoutNewPage2.addWidget(self.Info_box, 3, 0, 1, 2)
