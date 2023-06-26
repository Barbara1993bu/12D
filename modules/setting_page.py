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


class setting_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName(u"setting_page")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setting_page = QFrame(self)
        self.setting_page.setMinimumSize(700,700)
        self.setting_page.setMaximumSize(1000, 1000)
        self.setting_page.setObjectName(u"setting_page")

        self.vertLayoutNewPage = QHBoxLayout(self.setting_page)
        self.vertLayoutNewPage.setObjectName(u"vertLayoutNewPage")

        # attach label widget to new page layout
        self.Label_language = QLabel(self.setting_page)
        self.Label_language.setFixedSize(200, 50)
        self.Label_language.setStyleSheet("color: black;"
                                          "font: bold;"
                                          "font-size: 15px")
        self.vertLayoutNewPage.addWidget(self.Label_language)

        # button for english
        self.btnLangEnglish = QPushButton(self.setting_page)  # QIcon(u":/images/images/polishflag.svg"),"")
        self.btnLangEnglish.setObjectName(u"btnLangEnglish")
        self.btnLangEnglish.setSizePolicy(sizePolicy)
        self.btnLangEnglish.setMinimumSize(QSize(100, 100))
        self.btnLangEnglish.setMaximumSize(QSize(200, 200))
        # self.btnLangEnglish.setFont(font)
        self.btnLangEnglish.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnLangEnglish.setLayoutDirection(Qt.LeftToRight)
        self.btnLangEnglish.setStyleSheet(u"border-image: url(:/images/images/images/englishflag.svg);")

        self.vertLayoutNewPage.addWidget(self.btnLangEnglish)

        self.btnLangPolish = QPushButton(self.setting_page)
        self.btnLangPolish.setObjectName(u"btnLangPolish")
        self.btnLangPolish.setSizePolicy(sizePolicy)
        self.btnLangPolish.setMinimumSize(QSize(100, 100))
        self.btnLangPolish.setMaximumSize(QSize(200, 200))
        # self.btnLangPolish.setFont(font)
        self.btnLangPolish.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnLangPolish.setLayoutDirection(Qt.LeftToRight)
        self.btnLangPolish.setStyleSheet(u"border-image: url(:/images/images/images/polishflag.svg);")

        self.vertLayoutNewPage.addWidget(self.btnLangPolish)

