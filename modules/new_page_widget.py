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
# from plotly.graph_objs import Scatter

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtQml import *
from PySide2.QtQuickWidgets import QQuickWidget
import pyqtgraph as pg
import numpy as np
# from . animated_toggle import AnimatedToggle

from resources import *
from modules import *

# os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"







class new_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName(u"new_page2")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        font = QFont()

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setObjectName(u"LayoutNewPage")
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Layout reconstruction EIT
        self.Frame_page2 = QFrame(self)
        self.Frame_page2.setStyleSheet("background-color: rgb(90,90,250)")
        self.girdLayoutNewPage2 = QHBoxLayout(self.Frame_page2)
        self.Frame_page2.setLayout(self.girdLayoutNewPage2)
        self.girdLayoutNewPage2.setSpacing(0)
        self.girdLayoutNewPage2.setContentsMargins(0, 0, 0, 0)
        self.girdLayoutNewPage2.setObjectName(u"girdLayoutNewPage")
        self.girdLayoutNewPage2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignCenter)

        self.menuBarMinSize = QSize(300, 50)
        self.menuBarMaxSize = QSize(400, 50)
        self.menuBarIconSize = QSize(40, 40)

        self.MeasFrame = QFrame(self.Frame_page2)
        self.MeasFrame.setMinimumSize(self.menuBarMinSize)
        self.MeasFrame.setMaximumSize(self.menuBarMinSize)

        self.btn_meas = QPushButton(self.MeasFrame)
        self.btn_meas.setObjectName(u"btn_meas")
        self.btn_meas.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.btn_meas.setMinimumSize(self.menuBarMinSize)
        self.btn_meas.setMaximumSize(self.menuBarMinSize)
        self.btn_meas.setFont(font)

        self.btn_meas.setStyleSheet(u"QPushButton {\n"
                                    "	border: none;\n"
                                    "	background-color: transparent;\n"
                                    "background-repeat: no-repeat;\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "	background-color: rgb(90,90,150);\n"
                                    "}\n"
                                    "QPushButton:pressed {	\n"
                                    "	background-color: rgb(90,90,250);\n"
                                    "}")
        self.btn_meas.setFlat(True)

        # self.btn_meas.setStyleSheet(u"background-image: url(:/icons/images/icons/activity.svg);")
        self.girdLayoutNewPage2.addWidget(self.MeasFrame)


        self.ReconFrame = QFrame(self.Frame_page2)
        self.ReconFrame.setMinimumSize(self.menuBarMinSize)
        self.ReconFrame.setMaximumSize(self.menuBarMinSize)

        self.btn_recontruction_frame = QPushButton(self.ReconFrame)
        self.btn_recontruction_frame.setObjectName(u"btn_recontruction_frame")
        # sizePolicy.setHeightForWidth(self.btn_recontruction_frame.sizePolicy().hasHeightForWidth())
        self.btn_recontruction_frame.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        # self.btn_grid.styleSheet(u"QPushButton {",
	    #                          "background-position: left center;",
    	#                          "background-repeat: no-repeat;",
	    #                          "border: none;",
	    #                          "border-left: 35px solid transparent;",
	    #                          "background-color: transparent;",
	    #                          "text-align: left;",
	    #                          "padding-left: 80px;",
    	#                          "color: #f8f8f2;}")
        self.btn_recontruction_frame.setMinimumSize(self.menuBarMinSize)
        self.btn_recontruction_frame.setMaximumSize(self.menuBarMaxSize)
        self.btn_recontruction_frame.setFont(font)
        self.btn_recontruction_frame.setStyleSheet(u"QPushButton {\n"
                                                   "	border: none;\n"
                                                   "	background-color: transparent;\n"
                                                   "}\n"
                                                   "QPushButton:hover {\n"
                                                   "	background-color: rgb(90,90,150);\n"
                                                   "}\n"
                                                   "QPushButton:pressed {	\n"
                                                   "	background-color: rgb(90,90,250);\n"
                                                   "}")
        self.btn_recontruction_frame.setFlat(True)
        # self.btn_recontruction_frame.setStyleSheet(u"background-image: url(:/icons/images/icons/image.svg);")
        self.girdLayoutNewPage2.addWidget(self.ReconFrame)

        self.GridFrame = QFrame(self.Frame_page2)
        self.GridFrame.setMinimumSize(self.menuBarMinSize)
        self.GridFrame.setMaximumSize(self.menuBarMinSize)

        self.btn_grid = QPushButton(self.GridFrame)
        self.btn_grid.setObjectName(u"btn_grid")
        # sizePolicy.setHeightForWidth(self.btn_grid.sizePolicy().hasHeightForWidth())
        self.btn_grid.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        self.btn_grid.setMinimumSize(self.menuBarMinSize)
        self.btn_grid.setMaximumSize(self.menuBarMaxSize)
        self.btn_grid.setFont(font)
        self.btn_grid.setStyleSheet(u"QPushButton {\n"
                                    "	border: none;\n"
                                    "	background-color: transparent;\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "	background-color: rgb(90,90,150);\n"
                                    "}\n"
                                    "QPushButton:pressed {	\n"
                                    "	background-color: rgb(90,90,250);\n"
                                    "}")

        self.btn_grid.setFlat(True)
        # self.btn_grid.setStyleSheet(u"background: rgb(10,10,10);")
        self.girdLayoutNewPage2.addWidget(self.GridFrame)


        self.layout.addWidget(self.Frame_page2)

        # -----------------------------------------
        # define stacked widgets
        self.newPage_StackedWidget = QStackedWidget(self)
        self.newPage_StackedWidget.setObjectName(
            u"newPage_StackedWidget")
        # self.newPage_StackedWidget.setStyleSheet(
        #     u"background:rgba(90,90,150,90);")

        # Defined widgets to btns

        self.meas_page = meas_page()

        self.newPage_StackedWidget.addWidget(self.meas_page)


        self.reconstruction_page = reconstruction_page()

        self.newPage_StackedWidget.addWidget(self.reconstruction_page)

        self.grid_page = grid_page()

        self.newPage_StackedWidget.addWidget(self.grid_page)

        self.layout.addWidget(self.newPage_StackedWidget)

        # self.newPage_StackedWidget.setCurrentIndex(2)



