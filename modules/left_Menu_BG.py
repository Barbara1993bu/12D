import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtQml import *
from PySide2.QtQuickWidgets import QQuickWidget

import PySide2

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtQml import *
from PySide2.QtQuickWidgets import QQuickWidget
import pyqtgraph as pg
import numpy as np
# from . animated_toggle import AnimatedToggle

from resources import *
from modules import *


class Left_Menu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        font = QFont()
        self.setObjectName(u"leftMenuBg")
        # self.leftMenuBg = QFrame(self)
        # ------------------------------------------
        # region left menue
        # ------------------------------------------
        #  left menu background
        self.leftMenuBg = QFrame(self)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(100, 0))
        self.leftMenuBg.setMaximumSize(QSize(100, 10000))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)

        # application logo page
        self.headerLogoPage = QFrame(self.leftMenuBg)
        self.headerLogoPage.setObjectName(u"headerLogoPage")
        self.headerLogoPage.setMinimumSize(QSize(0, 75))
        self.headerLogoPage.setMaximumSize(QSize(10000, 75))
        self.headerLogoPage.setFrameShape(QFrame.NoFrame)
        self.headerLogoPage.setFrameShadow(QFrame.Raised)

        # -----------------------------------------
        # first application column
        # keeping toggle menu and app icons
        # -----------------------------------------
        # vertical layout
        self.vertLayoutToggleMenu = QVBoxLayout(self.leftMenuBg)
        self.vertLayoutToggleMenu.setSpacing(0)
        self.vertLayoutToggleMenu.setObjectName(u"vertLayoutToggleMenu")
        self.vertLayoutToggleMenu.setContentsMargins(0, 0, 0, 0)

        # -----------------------------------------
        # first application column buttons

        # left manu frame
        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)

        # application logo
        self.headerLogo = QFrame(self.headerLogoPage)
        self.headerLogo.setObjectName(u"headerLogo")
        self.headerLogo.setGeometry(QRect(10, 10, 100, 100))
        self.headerLogo.setMinimumSize(QSize(100, 100))
        self.headerLogo.setMaximumSize(QSize(100, 100))
        self.headerLogo.setFrameShape(QFrame.NoFrame)
        self.headerLogo.setFrameShadow(QFrame.Raised)

        # application title
        self.appTitle = QLabel(self.headerLogoPage)
        self.appTitle.setObjectName(u"appTitle")
        self.appTitle.setGeometry(QRect(125, 5, 600, 35))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(18)
        font1.setBold(True)
        font1.setItalic(False)
        self.appTitle.setFont(font1)
        self.appTitle.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        # title description
        self.appTitleDescription = QLabel(self.headerLogoPage)
        self.appTitleDescription.setObjectName(u"appTitleDescription")
        self.appTitleDescription.setGeometry(QRect(125, 40, 600, 35))
        self.appTitleDescription.setMaximumSize(QSize(10000, 35))

        self.appTitleDescription.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        # left menu layout
        self.vertMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.vertMenuLayout.setSpacing(0)
        self.vertMenuLayout.setObjectName(u"vertMenuLayout")
        self.vertMenuLayout.setContentsMargins(0, 0, 0, 0)

        # toggle box
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(10000, 100))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)

        # bottom menu frame
        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)

        # top menu frame
        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)

        # toggle box vertical layout
        self.vertLayoutToggleBox = QVBoxLayout(self.toggleBox)
        self.vertLayoutToggleBox.setSpacing(0)
        self.vertLayoutToggleBox.setObjectName(u"vertLayoutToggleBox")
        self.vertLayoutToggleBox.setContentsMargins(0, 0, 0, 0)

        # toggle button
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 125))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/menu.svg);")

        # attach toggle button
        self.vertLayoutToggleBox.addWidget(self.toggleButton)

        # attach toggle box
        self.vertMenuLayout.addWidget(self.toggleBox)

        self.vertMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)

        # top menu layout
        self.vertLayoutTopMenu = QVBoxLayout(self.topMenu)
        self.vertLayoutTopMenu.setSpacing(0)
        self.vertLayoutTopMenu.setObjectName(u"vertLayoutTopMenu")
        self.vertLayoutTopMenu.setContentsMargins(0, 0, 0, 0)

        # top menu home button
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 125))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/home.svg);")

        # attach home button
        self.vertLayoutTopMenu.addWidget(self.btn_home)



        # top menu widgets button
        self.btn_widgets = QPushButton(self.topMenu)
        self.btn_widgets.setObjectName(u"btn_widgets")
        sizePolicy.setHeightForWidth(self.btn_widgets.sizePolicy().hasHeightForWidth())
        self.btn_widgets.setSizePolicy(sizePolicy)
        self.btn_widgets.setMinimumSize(QSize(0, 125))
        self.btn_widgets.setFont(font)
        self.btn_widgets.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_widgets.setLayoutDirection(Qt.LeftToRight)
        self.btn_widgets.setStyleSheet(u"background-image: url(:/icons/images/icons/play.svg);")

        # attach widgets button
        self.vertLayoutTopMenu.addWidget(self.btn_widgets)

        # top menu new page button
        self.btn_new = QPushButton(self.topMenu)
        self.btn_new.setObjectName(u"btn_new")
        sizePolicy.setHeightForWidth(self.btn_new.sizePolicy().hasHeightForWidth())
        self.btn_new.setSizePolicy(sizePolicy)
        self.btn_new.setMinimumSize(QSize(0, 125))
        self.btn_new.setFont(font)
        self.btn_new.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_new.setLayoutDirection(Qt.LeftToRight)
        self.btn_new.setStyleSheet(u"background-image: url(:/icons/images/icons/archive.svg);")

        # attach new page button
        self.vertLayoutTopMenu.addWidget(self.btn_new)

        # bottom menu layout
        self.vertLayoutBottomMenu = QVBoxLayout(self.bottomMenu)
        self.vertLayoutBottomMenu.setSpacing(0)
        self.vertLayoutBottomMenu.setObjectName(u"vertLayoutBottomMenu")
        self.vertLayoutBottomMenu.setContentsMargins(0, 0, 0, 0)

        # top menu settings button
        self.btn_settings = QPushButton(self.bottomMenu)
        self.btn_settings.setObjectName(u"btn_settings")
        sizePolicy.setHeightForWidth(self.btn_settings.sizePolicy().hasHeightForWidth())
        self.btn_settings.setSizePolicy(sizePolicy)
        self.btn_settings.setMinimumSize(QSize(0, 125))
        self.btn_settings.setFont(font)
        self.btn_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_settings.setLayoutDirection(Qt.LeftToRight)
        self.btn_settings.setStyleSheet(u"background-image: url(:/icons/images/icons/settings.svg);")

        # attach btn_settings button
        self.vertLayoutBottomMenu.addWidget(self.btn_settings)

        # attach bottom menu
        self.vertMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignBottom)

        # attach buttons menu frame
        self.vertLayoutToggleMenu.addWidget(self.leftMenuFrame)

        # -----------------------------------------------
        # end region
        # -----------------------------------------------