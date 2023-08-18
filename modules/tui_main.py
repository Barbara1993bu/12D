# -*- coding: utf-8 -*-
from datetime import datetime
import os
import time
import json

# from PySide2.QtCore import *
import PySide2
from PySide2.QtWebEngineWidgets import QWebEngineView
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

# import modules and widgets



from modules import *
# from . usefull_function import build_axes
import copy

# os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


# -----------------------------------------
# define custom widgets with text input,
# they are required for use of virtual keyboard
# -----------------------------------------


class nxQLineEdit(QLineEdit):

    focused = Signal()
    noneFocused = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()


class nxQDateEdit(QDateEdit):

    focused = Signal()
    noneFocused = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()


class nxQDateTimeEdit(QDateTimeEdit):

    focused = Signal()
    noneFocused = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()


class nxQDoubleSpinBox(QDoubleSpinBox):

    focused = Signal()
    noneFocused = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()


class nxQDoubleSpinBox(QDoubleSpinBox):

    focused = Signal()
    noneFocused = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()


class nxQTimeEdit(QTimeEdit):

    focused = Signal()
    noneFocused = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()

# ------------------------------------------
# ------------- Worker ---------------------
# ------------------------------------------


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

# -----------------------------------------
# definition of main window
# -----------------------------------------


class tui_MainWindow(object):

    def setup_tui(self, MainWindow):

        # initizalize custom widgets

        self.nxQLineEdit = nxQLineEdit()
        self.nxQDateEdit = nxQDateEdit()
        self.nxQDateTimeEdit = nxQDateTimeEdit()
        self.nxQDoubleSpinBox = nxQDoubleSpinBox()
        self.nxQTimeEdit = nxQTimeEdit()

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        MainWindow.resize(1920, 1080)
        MainWindow.setMinimumSize(QSize(1920, 1080))
        self.threadpool = QThreadPool()

        # -----------------------------------------
        # styles and background
        # -----------------------------------------

        # general style sheet
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"")

        # application margins
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(0, 0, 0, 0)

        # application background
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)

        #  left menu background
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(100, 0))
        self.leftMenuBg.setMaximumSize(QSize(100, 10000))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)

        # keyboard background
        self.keyboardBg = QFrame(self.bgApp)
        self.keyboardBg.setObjectName(u"keyboardBg")
        self.keyboardBg.setFrameShape(QFrame.NoFrame)
        self.keyboardBg.setFrameShadow(QFrame.Raised)

        # -----------------------------------------
        # application main frames
        # -----------------------------------------

        # application top frame
        self.topFrameApp = QFrame(self.bgApp)
        self.topFrameApp.setObjectName(u"topFrameApp")
        self.topFrameApp.setStyleSheet(u"")
        self.topFrameApp.setFrameShape(QFrame.NoFrame)
        self.topFrameApp.setFrameShadow(QFrame.Raised)

        # application bottom frame
        self.bottomFrameApp = QFrame(self.bgApp)
        self.bottomFrameApp.setObjectName(u"bottomFrameApp")
        self.bottomFrameApp.setStyleSheet(u"")
        self.bottomFrameApp.setFrameShape(QFrame.NoFrame)
        self.bottomFrameApp.setFrameShadow(QFrame.Raised)

        # application keyboard frame
        self.keyboardFrameApp = QFrame(self.keyboardBg)
        self.keyboardFrameApp.setObjectName(u"keyboardFrameApp")
        self.keyboardFrameApp.setStyleSheet(u"")
        self.keyboardFrameApp.setFrameShape(QFrame.NoFrame)
        self.keyboardFrameApp.setFrameShadow(QFrame.Raised)

        # -----------------------------------------
        # application layout
        # -----------------------------------------

        # application layout
        self.appLayout = QVBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)

        # application top layout
        self.appTopLayout = QVBoxLayout(self.topFrameApp)
        self.appTopLayout.setSpacing(0)
        self.appTopLayout.setObjectName(u"appTopLayout")
        self.appTopLayout.setContentsMargins(0, 0, 0, 0)

        # application bottom layout
        self.appBottomLayout = QHBoxLayout(self.bottomFrameApp)
        self.appBottomLayout.setSpacing(0)
        self.appBottomLayout.setObjectName(u"appBottomLayout")
        self.appBottomLayout.setContentsMargins(0, 0, 0, 0)

        # application keyboard layout
        self.keyboardLayout = QHBoxLayout(self.keyboardFrameApp)
        self.keyboardLayout.setSpacing(0)
        self.keyboardLayout.setObjectName(u"keyboardLayout")
        self.keyboardLayout.setContentsMargins(0, 0, 0, 0)



        # -----------------------------------------
        # application header
        # -----------------------------------------

        # header frame
        self.headerTopBg = QFrame(self.topFrameApp)
        self.headerTopBg.setObjectName(u"headerTopBg")
        self.headerTopBg.setMinimumSize(QSize(0, 75))
        self.headerTopBg.setMaximumSize(QSize(10000, 75))
        self.headerTopBg.setFrameShape(QFrame.NoFrame)
        self.headerTopBg.setFrameShadow(QFrame.Raised)

        # header layout
        self.headerHorizLayout = QHBoxLayout(self.headerTopBg)
        self.headerHorizLayout.setSpacing(0)
        self.headerHorizLayout.setObjectName(u"headerHorizLayout")
        self.headerHorizLayout.setContentsMargins(0, 0, 0, 0)

        # application logo page
        self.headerLogoPage = QFrame(self.leftMenuBg)
        self.headerLogoPage.setObjectName(u"headerLogoPage")
        self.headerLogoPage.setMinimumSize(QSize(0, 75))
        self.headerLogoPage.setMaximumSize(QSize(10000, 75))
        self.headerLogoPage.setFrameShape(QFrame.NoFrame)
        self.headerLogoPage.setFrameShadow(QFrame.Raised)

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
        # font2 = QFont()
        # font2.setFamily(u"Segoe UI")
        # font2.setPointSize(12)
        # font2.setBold(False)
        # font2.setItalic(True)
        # self.appTitleDescription.setFont(font2)
        self.appTitleDescription.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        # attach logo page frame
        self.headerHorizLayout.addWidget(self.headerLogoPage)


        # header right buttons
        self.headerRightButtons  = QFrame(self.headerTopBg)
        self.headerRightButtons.setObjectName(u"headerRightButtons")
        self.headerRightButtons.setMinimumSize(QSize(0, 75))
        self.headerRightButtons.setFrameShape(QFrame.NoFrame)
        self.headerRightButtons.setFrameShadow(QFrame.Raised)

        # add layout
        self.headerHorizLayoutBtns = QHBoxLayout(self.headerRightButtons)
        self.headerHorizLayoutBtns.setSpacing(5)
        self.headerHorizLayoutBtns.setObjectName(u"headerHorizLayoutBtns")
        self.headerHorizLayoutBtns.setContentsMargins(0, 0, 0, 0)

        # add more options button
        self.moreSettingsBtn = QPushButton(self.headerRightButtons)
        self.moreSettingsBtn.setObjectName(u"moreAppBtn")
        self.moreSettingsBtn.setMinimumSize(QSize(150, 50))
        self.moreSettingsBtn.setMaximumSize(QSize(150, 55))
        self.moreSettingsBtn.setCursor(QCursor(Qt.PointingHandCursor))
        moreSettingsBtnIcon = QIcon()
        moreSettingsBtnIcon.addFile(u":/icons/images/icons/tool.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.moreSettingsBtn.setIcon(moreSettingsBtnIcon)
        self.moreSettingsBtn.setIconSize(QSize(50, 50))
        # attach more settings button to the butons layout
        self.headerHorizLayoutBtns.addWidget(self.moreSettingsBtn)

        # attach right buttons frame
        self.headerHorizLayout.addWidget(self.headerRightButtons, 0, Qt.AlignRight)

        # attach header frame
        self.appTopLayout.addWidget(self.headerTopBg, 0, Qt.AlignTop)


        # end of the header definition
        # -----------------------------------------


        # -----------------------------------------
        # application main content
        # -----------------------------------------


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

        # top menu frame
        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)

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

        # self.btn_widgets.mouseMoveEvent = self.btn_widgetsMouseMoveEvent

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

        # self.btn_new.mouseMoveEvent = self.btn_newMouseMoveEvent

        # attach new page button
        self.vertLayoutTopMenu.addWidget(self.btn_new)



        # attach new page button
        # self.vertLayoutTopMenu.addWidget(self.btn_grid)



        # attach new page button
        # self.vertLayoutTopMenu.addWidget(self.btn_meas)

        #
        # # top menu save button
        # self.btn_save = QPushButton(self.topMenu)
        # self.btn_save.setObjectName(u"btn_save")
        # sizePolicy.setHeightForWidth(self.btn_save.sizePolicy().hasHeightForWidth())
        # self.btn_save.setSizePolicy(sizePolicy)
        # self.btn_save.setMinimumSize(QSize(0, 125))
        # self.btn_save.setFont(font)
        # self.btn_save.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btn_save.setLayoutDirection(Qt.LeftToRight)
        # self.btn_save.setStyleSheet(u"background-image: url(:/icons/images/icons/save.svg)")
        #
        # # attach save button
        # self.vertLayoutTopMenu.addWidget(self.btn_save)
        #
        # # top menu exit button
        # self.btn_exit = QPushButton(self.topMenu)
        # self.btn_exit.setObjectName(u"btn_exit")
        # sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        # self.btn_exit.setSizePolicy(sizePolicy)
        # self.btn_exit.setMinimumSize(QSize(0, 125))
        # self.btn_exit.setFont(font)
        # self.btn_exit.setCursor(QCursor(Qt.PointingHandCursor))
        # self.btn_exit.setLayoutDirection(Qt.LeftToRight)
        # self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/file.svg);")
        #
        # # attach exit button
        # self.vertLayoutTopMenu.addWidget(self.btn_exit)

        # attach menu layout
        self.vertMenuLayout.addWidget(self.topMenu, 0, Qt.AlignTop)


        # bottom menu frame
        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)

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

        # attach left toggle menu
        self.appBottomLayout.addWidget(self.leftMenuBg)

        # end of left menu frame
        # -----------------------------------------


        # -----------------------------------------
        # application content frames
        # -----------------------------------------

        # main content frame
        self.mainContentFrame = QFrame(self.bgApp)
        self.mainContentFrame.setObjectName(u"mainContentFrame")
        self.mainContentFrame.setFrameShape(QFrame.NoFrame)
        self.mainContentFrame.setFrameShadow(QFrame.Raised)

        # vertical layout content frame
        self.vertLayoutContentFrame = QVBoxLayout(self.mainContentFrame)
        self.vertLayoutContentFrame.setSpacing(0)
        self.vertLayoutContentFrame.setObjectName(u"vertLayoutContentFrame")
        self.vertLayoutContentFrame.setContentsMargins(0, 0, 0, 0)

        # content bottom frame
        self.contentCentralFrame = QFrame(self.mainContentFrame)
        self.contentCentralFrame.setObjectName(u"contentCentralFrame")
        self.contentCentralFrame.setFrameShape(QFrame.NoFrame)
        self.contentCentralFrame.setFrameShadow(QFrame.Raised)

        # vertical layout
        self.vertLayoutCentralFrame = QVBoxLayout(self.contentCentralFrame)
        self.vertLayoutCentralFrame.setSpacing(0)
        self.vertLayoutCentralFrame.setObjectName(u"vertLayoutCentralFrame")
        self.vertLayoutCentralFrame.setContentsMargins(0, 0, 0, 0)

        # content frame
        self.content = QFrame(self.contentCentralFrame)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)

        # content frame layout
        self.horizLayoutContent = QHBoxLayout(self.content)
        self.horizLayoutContent.setSpacing(0)
        self.horizLayoutContent.setObjectName(u"horizLayoutContent")
        self.horizLayoutContent.setContentsMargins(0, 0, 0, 0)

        # pages container
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)

        # pages container layout
        self.vertLayoutContainer = QVBoxLayout(self.pagesContainer)
        self.vertLayoutContainer.setSpacing(0)
        self.vertLayoutContainer.setObjectName(u"vertLayoutContainer")
        self.vertLayoutContainer.setContentsMargins(0, 0, 0, 0)

        # stacked widgets
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")


        # -----------------------------------------
        # definition of widget pages
        # -----------------------------------------

        # -----------------------------------------
        # Home Frame
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"background-image: url(:/images/images/images/NX_logo.png);"
                                "background-position: center;"
                                "background-repeat: no-repeat;")
        self.stackedWidget.addWidget(self.home)


        # -----------------------------------------
        # Widgets Frame
        self.widgets = param_page()

        self.stackedWidget.addWidget(self.widgets)
        # self.stackedWidget.addWidget(self.widgets)


        # -----------------------------------------
        # New Page Frame
        self.new_page = new_page()

        # attach new page to stacked widgets
        self.stackedWidget.addWidget(self.new_page)

        # # ------------------------------------------
        # self.grid_page = grid_page()
        # self.stackedWidget.addWidget(self.grid_page)
        #
        # # ------------------------------------------
        # self.meas_page = meas_page()
        # self.stackedWidget.addWidget(self.meas_page)



        # -----------------------------------------
        # Setting Frame
        self.setting_page = setting_page()

        # attach new page to stacked widgets
        self.stackedWidget.addWidget(self.setting_page)

        # -----------------------------------------
        # add stacked widgets do pages container
        self.vertLayoutContainer.addWidget(self.stackedWidget)

        # -----------------------------------------
        # add pages container to content layout
        self.horizLayoutContent.addWidget(self.pagesContainer)

        # end of stacked widget frames definition
        # -----------------------------------------


        # -----------------------------------------
        # definition of right extra box
        # -----------------------------------------
        # right box
        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 10000))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)

        # right box layout
        self.vertLayoutRightBox = QVBoxLayout(self.extraRightBox)
        self.vertLayoutRightBox.setSpacing(0)
        self.vertLayoutRightBox.setObjectName(u"vertLayoutRightBox")
        self.vertLayoutRightBox.setContentsMargins(0, 0, 0, 0)

        # more settings frame
        self.contentMoreSettings = QFrame(self.extraRightBox)
        self.contentMoreSettings.setObjectName(u"contentMoreSettings")
        self.contentMoreSettings.setFrameShape(QFrame.NoFrame)
        self.contentMoreSettings.setFrameShadow(QFrame.Raised)

        # vertical layout content more settings
        self.vertLayoutMoreSettings = QVBoxLayout(self.contentMoreSettings)
        self.vertLayoutMoreSettings.setSpacing(0)
        self.vertLayoutMoreSettings.setObjectName(u"vertLayoutMoreSettings")
        self.vertLayoutMoreSettings.setContentsMargins(0, 0, 0, 0)

        # top menu frame
        self.topMenuMoreSettings = QFrame(self.contentMoreSettings)
        self.topMenuMoreSettings.setObjectName(u"topMenu")
        self.topMenuMoreSettings.setFrameShape(QFrame.NoFrame)
        self.topMenuMoreSettings.setFrameShadow(QFrame.Raised)

        # top menu vertical layout
        self.vertLayoutTopMenu = QVBoxLayout(self.topMenuMoreSettings)
        self.vertLayoutTopMenu.setSpacing(0)
        self.vertLayoutTopMenu.setObjectName(u"vertLayoutTopMenu")
        self.vertLayoutTopMenu.setContentsMargins(0, 0, 0, 0)

        # button close app
        self.btn_closeApp = QPushButton(self.topMenuMoreSettings)
        self.btn_closeApp.setObjectName(u"btn_closeApp")
        sizePolicy.setHeightForWidth(self.btn_closeApp.sizePolicy().hasHeightForWidth())
        self.btn_closeApp.setSizePolicy(sizePolicy)
        self.btn_closeApp.setMinimumSize(QSize(0, 125))
        self.btn_closeApp.setFont(font)
        self.btn_closeApp.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_closeApp.setLayoutDirection(Qt.LeftToRight)
        self.btn_closeApp.setStyleSheet(u"background-image: url(:/icons/images/icons/x-circle.svg);")
        # attach button close app
        self.vertLayoutTopMenu.addWidget(self.btn_closeApp)

        # button restart app
        self.btn_restartApp = QPushButton(self.topMenuMoreSettings)
        self.btn_restartApp.setObjectName(u"btn_restartApp")
        sizePolicy.setHeightForWidth(self.btn_restartApp.sizePolicy().hasHeightForWidth())
        self.btn_restartApp.setSizePolicy(sizePolicy)
        self.btn_restartApp.setMinimumSize(QSize(0, 125))
        self.btn_restartApp.setFont(font)
        self.btn_restartApp.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_restartApp.setLayoutDirection(Qt.LeftToRight)
        self.btn_restartApp.setStyleSheet(u"background-image: url(:/icons/images/icons/rotate-ccw.svg);")
        # attach button restart app
        self.vertLayoutTopMenu.addWidget(self.btn_restartApp)

        # button reboot device
        self.btn_rebootDevice = QPushButton(self.topMenuMoreSettings)
        self.btn_rebootDevice.setObjectName(u"btn_rebootDevice")
        sizePolicy.setHeightForWidth(self.btn_rebootDevice.sizePolicy().hasHeightForWidth())
        self.btn_rebootDevice.setSizePolicy(sizePolicy)
        self.btn_rebootDevice.setMinimumSize(QSize(0, 125))
        self.btn_rebootDevice.setFont(font)
        self.btn_rebootDevice.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_rebootDevice.setLayoutDirection(Qt.LeftToRight)
        self.btn_rebootDevice.setStyleSheet(u"background-image: url(:/icons/images/icons/refresh-cw.svg);")
        # attach button reboot device
        self.vertLayoutTopMenu.addWidget(self.btn_rebootDevice)

        # button shutdown device
        self.btn_shutDownDevice = QPushButton(self.topMenuMoreSettings)
        self.btn_shutDownDevice.setObjectName(u"btn_shutDownDevice")
        sizePolicy.setHeightForWidth(self.btn_shutDownDevice.sizePolicy().hasHeightForWidth())
        self.btn_shutDownDevice.setSizePolicy(sizePolicy)
        self.btn_shutDownDevice.setMinimumSize(QSize(0, 125))
        self.btn_shutDownDevice.setFont(font)
        self.btn_shutDownDevice.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_shutDownDevice.setLayoutDirection(Qt.LeftToRight)
        self.btn_shutDownDevice.setStyleSheet(u"background-image: url(:/icons/images/icons/power.svg);")
        # self.btn_shutDownDevice.setIcon(QIcon(u":/icons/images/icons/power.svg"))
        # self.btn_shutDownDevice.setIconSize(QSize(50,50))
        # self.btn_shutDownDevice.setStyleSheet("text-align: left;")

        # self.btn_shutDownDevice.setStyleSheet("QPushButton { padding-left: 20px; text-align: left; }")
        # self.btn_shutDownDevice.setStyleSheet("align: left; icon-size: 32px;")

        # attach button shutdown device
        self.vertLayoutTopMenu.addWidget(self.btn_shutDownDevice)

        # attach top menu to more settings frame
        self.vertLayoutMoreSettings.addWidget(self.topMenuMoreSettings, 0, Qt.AlignTop)

        # attach content more settings to right box layout
        self.vertLayoutRightBox.addWidget(self.contentMoreSettings)

        # attach extra right box to content layout
        self.horizLayoutContent.addWidget(self.extraRightBox)

        # attach content frame to central frame layout
        self.vertLayoutCentralFrame.addWidget(self.content)

        # end of the right frame definition
        # -----------------------------------------

        # -----------------------------------------
        # definition of info bar bottom bar
        # -----------------------------------------
        # bottom bar
        self.infoBar = QFrame(self.contentCentralFrame)
        self.infoBar.setObjectName(u"infoBar")
        self.infoBar.setMinimumSize(QSize(0, 50))
        self.infoBar.setMaximumSize(QSize(100000, 50))
        self.infoBar.setFrameShape(QFrame.NoFrame)
        self.infoBar.setFrameShadow(QFrame.Raised)

        # horizontal layout
        self.horizLayoutInfoBar = QHBoxLayout(self.infoBar)
        self.horizLayoutInfoBar.setSpacing(0)
        self.horizLayoutInfoBar.setObjectName(u"horizLayoutInfoBar")
        self.horizLayoutInfoBar.setContentsMargins(0, 0, 0, 0)

        # create message box
        self.message_box = QTextEdit(self.infoBar)
        self.message_box.setObjectName(u"message_box")
        self.message_box.setStyleSheet(u"color: white;"
                                       u" border: 0px solid rgb(90,90,250);"
                                       u" background-color: transparent;")
        self.message_box.setMinimumSize(QSize(0, 50))
        self.message_box.setMaximumSize(QSize(100000, 50))
        message_box_font = QFont()
        message_box_font.setFamily(u"Segoe UI Light")
        message_box_font.setPointSize(18)
        message_box_font.setBold(False)
        message_box_font.setItalic(False)
        self.message_box.setFont(message_box_font)
        # add init empty space
        self.message_box.insertPlainText("  ")
        self.message_box.setTextCursor(QTextCursor(self.message_box.document()))
        self.message_box.moveCursor(QTextCursor.Start)
        # forbid text input
        self.message_box.setDisabled(True)

        # attach message box to the frame
        self.horizLayoutInfoBar.addWidget(self.message_box)

        # add info bar to application frame
        self.vertLayoutContainer.addWidget(self.infoBar)

        # end of the info bar
        # -----------------------------------------


        # -----------------------------------------
        # definition of bottom bar
        # -----------------------------------------
        # bottom bar
        # self.bottomBar = QFrame(self.contentCentralFrame)
        # self.bottomBar.setObjectName(u"bottomBar")
        # self.bottomBar.setMinimumSize(QSize(0, 22))
        # self.bottomBar.setMaximumSize(QSize(100000, 22))
        # self.bottomBar.setFrameShape(QFrame.NoFrame)
        # self.bottomBar.setFrameShadow(QFrame.Raised)
        # self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        # self.horizontalLayout_5.setSpacing(0)
        # self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        # self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        # self.creditsLabel = QLabel(self.bottomBar)
        # self.creditsLabel.setObjectName(u"creditsLabel")
        # self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        # font5 = QFont()
        # font5.setFamily(u"Segoe UI")
        # font5.setBold(False)
        # font5.setItalic(False)
        # self.creditsLabel.setFont(font5)
        # self.creditsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        #
        # self.horizontalLayout_5.addWidget(self.creditsLabel)
        #
        # self.version = QLabel(self.bottomBar)
        # self.version.setObjectName(u"version")
        # self.version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        #
        # self.horizontalLayout_5.addWidget(self.version)
        #
        # self.frame_size_grip = QFrame(self.bottomBar)
        # self.frame_size_grip.setObjectName(u"frame_size_grip")
        # self.frame_size_grip.setMinimumSize(QSize(20, 0))
        # self.frame_size_grip.setMaximumSize(QSize(20, 100000))
        # self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        # self.frame_size_grip.setFrameShadow(QFrame.Raised)
        #
        # self.horizontalLayout_5.addWidget(self.frame_size_grip)
        #
        # self.vertLayoutCentralFrame.addWidget(self.bottomBar)


        # -----------------------------------------
        # embedding a virtual keyboard in the application
        # -----------------------------------------

        # virtual keyboard frame
        self.keyboardBox = QFrame(self.keyboardBg)
        self.keyboardBox.setStyleSheet(u"background-color: rgb (230, 230, 230);")
        self.keyboardBox.setObjectName(u"keyboardBox")
        self.keyboardBox.setMinimumSize(QSize(0, 0))
        self.keyboardBox.setMaximumSize(QSize(10000, 0))
        self.keyboardBox.setFrameShape(QFrame.NoFrame)
        self.keyboardBox.setFrameShadow(QFrame.Raised)
        #
        self.keyboardBoxLayout = QVBoxLayout(self.keyboardBox)

        self.keyboardwidget = QQuickWidget(self.keyboardBox)
        self.keyboardwidget.setMinimumSize(QSize(845, 320))
        self.keyboardwidget.setMaximumSize(QSize(845, 320))
        self.keyboardwidget.setSource(QUrl.fromLocalFile("src/keyboard.qml"))

        self.keyboardwidget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.keyboardwidget.setAttribute(Qt.WA_AcceptTouchEvents)
        self.keyboardwidget.setFocusPolicy(Qt.NoFocus)


        self.keyboardBoxLayout.addWidget(self.keyboardwidget, 0, Qt.AlignCenter)

        #
        # r=self.keyboardwidget.rootObject().findChild(QObject,"inputPanel_object")
        #
        # print(r)
        # print("{}".format(QQmlProperty(r, "isKeyboardActive").read()))

        # attach header frame
        self.keyboardLayout.addWidget(self.keyboardBox, 0, Qt.AlignTop)


        # end of the virtual keyboard definition
        # -----------------------------------------

        #
        # self.foo = Foo()
        # self.foo.var = "{}".format(QQmlProperty(self.keyboardwidget.rootObject().findChild(QObject,"inputPanel_object"), "isKeyboardActive").read())
        #
        #

        # self.foo.valueChanged.connect(openCloseKeyboardTab)

        # self.stackedWidget.addWidget(self.testinput)

        # -----------------------------------------
        # ATTACH MAIN LAYOUTS AND WIDGETS

        # -----------------------------------------
        # attach content central frame to the content layout
        self.vertLayoutContentFrame.addWidget(self.contentCentralFrame)
        # -----------------------------------------
        # attach main content frame to the app bottom layout
        self.appBottomLayout.addWidget(self.mainContentFrame)
        # -----------------------------------------
        # attach top frame do the app layout
        self.appLayout.addWidget(self.topFrameApp)
        # -----------------------------------------
        # attach bottom frame do the app layout
        self.appLayout.addWidget(self.bottomFrameApp)
        # -----------------------------------------
        # attach keyboard frame do the app layout
        self.appLayout.addWidget(self.keyboardFrameApp)
        # -----------------------------------------
        # attach bgApp widget to app margins
        self.appMargins.addWidget(self.bgApp)


        # -----------------------------------------
        # set central widget
        MainWindow.setCentralWidget(self.styleSheet)
        # -----------------------------------------
        # re-translate TUI
        self.retranslate_tui(MainWindow)
        # -----------------------------------------
        # set index of current widget
        self.stackedWidget.setCurrentIndex(2)

        # -----------------------------------------
        QMetaObject.connectSlotsByName(MainWindow)



    # -----------------------------------------



    def retranslate_tui(self, MainWindow):

        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))

        self.appTitle.setText(QCoreApplication.translate("MainWindow", u"EIT 3.0", None))

        self.appTitleDescription.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Electrical Impedance Tomography Device'][Dictionaries._AppVars['Language']], None))

        self.toggleButton.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Hide'][Dictionaries._AppVars['Language']], None))

        self.btn_home.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Home'][Dictionaries._AppVars['Language']], None))

        self.btn_widgets.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Widgets'][Dictionaries._AppVars['Language']], None))

        self.setting_page.Label_language.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Language'][Dictionaries._AppVars['Language']], None))

        self.widgets.Label_tryb.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Tryb'][Dictionaries._AppVars['Language']], None))
        self.widgets.Label_stim_pattern.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Stim'][Dictionaries._AppVars['Language']], None))
        self.widgets.Label_frequency.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Freq'][Dictionaries._AppVars['Language']], None))
        self.widgets.Label_interval_frame.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Interval frame'][Dictionaries._AppVars['Language']], None))
        self.widgets.Label_amp.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Amp'][Dictionaries._AppVars['Language']], None))
        self.widgets.Label_int_frame.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Int frame'][Dictionaries._AppVars['Language']], None))
        self.widgets.Text_Live.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Live'][Dictionaries._AppVars['Language']], None))
        self.widgets.btn_send_params.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Send param'][Dictionaries._AppVars['Language']], None))


        self.btn_new.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['EIT 3D'][Dictionaries._AppVars['Language']], None))
        self.new_page.btn_grid.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Visualisation'][Dictionaries._AppVars['Language']], None))
        self.new_page.btn_meas.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Measurment'][Dictionaries._AppVars['Language']], None))
        # self.leftMenuBg.btn_new2.setText(QCoreApplication.translate("MainWindow",
        #                                                 Dictionaries._AppLang['New Example Tab'][
        #                                                     Dictionaries._AppVars['Language']], None))


        # self.btn_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        # self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Settings'][Dictionaries._AppVars['Language']], None))

        self.moreSettingsBtn.setToolTip(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['More Options'][Dictionaries._AppVars['Language']], None))


        self.moreSettingsBtn.setText("")

        self.btn_closeApp.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Close Application'][Dictionaries._AppVars['Language']], None))

        self.btn_restartApp.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Restart Application'][Dictionaries._AppVars['Language']], None))

        self.btn_rebootDevice.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Reboot Device'][Dictionaries._AppVars['Language']], None))

        self.btn_shutDownDevice.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Shut Down'][Dictionaries._AppVars['Language']], None))


        self.new_page.meas_page.Label_colorMap.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Color map'][Dictionaries._AppVars['Language']], None))
        self.new_page.meas_page.Set_of_colorMap.addItems(['default', 'Greys', 'viridis', 'hsv', 'cool', 'hot'])

        self.new_page.reconstruction_page.btn_Model.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Model EIT'][Dictionaries._AppVars['Language']], None))
        self.new_page.reconstruction_page.btn_voltages_EIT.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Voltages EIT'][Dictionaries._AppVars['Language']], None))

        self.new_page.reconstruction_page.label_txt_method_reconstruction.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Method of reconstruction'][Dictionaries._AppVars['Language']], None))

        self.new_page.reconstruction_page.Method_of_reconstruction.addItems(['Tikhonov', 'Gausse-Newton', 'Kotre',
                                                'Marquardt-Levenberg', 'Total Variation', 'Elasticnet'])
        self.new_page.reconstruction_page.btn_reconstruction.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Reconstruction EIT'][Dictionaries._AppVars['Language']], None))
        self.new_page.reconstruction_page.btn_reconstruction_device.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Reconstruction EIT from device'][Dictionaries._AppVars['Language']], None))
        self.new_page.reconstruction_page.label_txt_number_of_iteration.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Number of iteration'][Dictionaries._AppVars['Language']], None))
        self.new_page.reconstruction_page.qdial_number_of_iteration.setMinimum(1)
        self.new_page.reconstruction_page.qdial_number_of_iteration.setMaximum(10)
        # self.qdial_number_of_iteration.setTickInterval(1)
        self.new_page.reconstruction_page.label_txt_regularyzation_parameter.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Regularyzation Parameter'][Dictionaries._AppVars['Language']], None))
        self.new_page.reconstruction_page.QcomboBox_regularyzation_parameter.addItems(['1e-1', '1e-2', '1e-3', '1e-4', '1e-5','1e-6','1e-7'])
        self.new_page.reconstruction_page.Label_load_Voltages.setText(r'D:\Aplikacje_pyQt\raw25072021190113389.csv')
        self.new_page.reconstruction_page.Label_load_model.setText(r'D:\Aplikacje_pyQt\wall_3D_G_2021_v1.mat')
        self.new_page.btn_meas.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Measurment'][Dictionaries._AppVars['Language']], None))
        self.new_page.btn_recontruction_frame.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Reconstruction'][Dictionaries._AppVars['Language']], None))
        AA = read_csv(r'D:\Aplikacje_pyQt\raw25072021190113389.csv', sep=';', header=None).to_numpy()
        self.new_page.meas_page.model._data = AA[:, 3:-1].tolist()
        # Ustawienie delegata do kolorowania komórek
        color_palette = build_color_palette(AA[:, 3:-1])
        delegate = ColorDelegate(color_palette)
        self.new_page.meas_page.table.setItemDelegate(delegate)

        self.new_page.grid_page.x_text.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Slice plane x = '][Dictionaries._AppVars['Language']], None))
        self.new_page.grid_page.y_text.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Slice plane y = '][Dictionaries._AppVars['Language']], None))
        self.new_page.grid_page.z_text.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Slice plane z = '][Dictionaries._AppVars['Language']], None))
        self.new_page.grid_page.vis_text.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Visualization voltages'][Dictionaries._AppVars['Language']], None))
        self.new_page.grid_page.btn_saveVis.setText(QCoreApplication.translate("MainWindow",
            Dictionaries._AppLang['Save Visualization'][Dictionaries._AppVars['Language']], None))

        # I = pg.ImageItem()
        # Maska = pg.ImageItem()
        # stimulation = {
        #     'n_electrodes': 8,
        #     'd_stim': 4,
        #     'd_meas': 1,
        #     'amp': 0.003,
        #     'z_contact': 0.01 * np.ones(8),
        #     'part_of_matrix': np.r_[1:8]
        #
        # }
        # Model = ImageEIT(50, np.array([0, 2*np.pi, 8]), 'point', stimulation=stimulation)
        # Model.setup()
        #
        # n_value = np.ones(Model.elems.shape[0])
        # n_value[10:100] = 2
        # Model.up_grade_value_elems(n_value)
        #
        # I.setImage(Model.field_of_view)
        # Maska.setImage(~Model.field_of_view.mask)
        # I.setRect(0, 0, 500, 500)
        # Maska.setRect(0, 0, 500, 500)
        # # self.inputGraph.adjustSize()
        #
        # cm = pg.colormap.get('CET-L17')
        # I.setColorMap(cm)
        # # Maskowanie
        # ver_b = Model.vertices_boundary
        # Points = [QPoint(ver_b[0][x], ver_b[1][x]) for x in range(len(ver_b[0]))]
        # Polygon = QPolygon(Points)
        # Region = QRegion(Polygon)
        #
        # self.inputGraph.addItem(Maska)
        # Maska.setZValue(10)
        # Maska.setOpacity(0.5)
        # self.inputGraph.addItem(I)
        # self.inputGraph.setBackground('w')
        # self.inputGraph.scaleToImage(I)


        # self.msgRestartBox.setText("Czy chcesz zrestartować aplikację AAAAAAA ")


    def disable_enable_all_buttons_for_multithreading(self, make_active = True):

        # self.btn_refresh_eit_reconstruction.setEnabled(make_active)

        pass


    def disable_enable_language_buttons_for_multithreading(self, make_active):

        self.setting_page.btnLangEnglish.setEnabled(make_active)
        self.setting_page.btnLangPolish.setEnabled(make_active)

    # update info box
    def update_message_box(self, new_message):

        self.disable_enable_language_buttons_for_multithreading(make_active=False)

        self.message_box.clear()
        self.infoBar.setStyleSheet("background:rgb(230,100,7)")
        self.message_box.moveCursor(QTextCursor.Start)
        self.message_box.insertPlainText(str(datetime.now().strftime('%H:%M:%S'))
                                             + " - Info: "
                                             + new_message)

        # run worker - it restores the info box to the previous state and look
        worker = Worker(self.waiting_process)
        worker.signals.finished.connect(self.clear_infoBar)


        # execute worker
        self.threadpool.start(worker)


    def waiting_process(self, progress_callback):
        time.sleep(1.25)


    def clear_infoBar(self):
        self.message_box.clear()
        self.infoBar.setStyleSheet("background:rgb(90,90,250)")
        self.disable_enable_language_buttons_for_multithreading(make_active=True)
    # def btn_widgetsMouseMoveEvent(self, event):
    #     print('jestem na zakladce widgets')
    #     self.keyboardwidget.setSource(QUrl.fromLocalFile("src/keyboard.qml"))
    #
    #
    # def btn_newMouseMoveEvent(self, event):
    #     print('jestem na zakladce new_page')
    #     self.keyboardwidget.setSource(QUrl.fromLocalFile("src/empty.qml"))

    def up_grade_info_box(self, s):
        self.new_page.reconstruction_page.Info_box.moveCursor(QTextCursor.Start)
        self.new_page.reconstruction_page.Info_box.insertPlainText(str(s) + '\n')
        self.new_page.reconstruction_page.Info_box.moveCursor(QTextCursor.Start)


    def solve_inverse_problem_device(self, progress_callback=None):
        if progress_callback is None:
            self.up_grade_info_box('Loading Model')
        else:
            progress_callback.emit('Loading Model')
        eit_3D = Dictionaries._AppModel['Model']
        max_iterations = int(self.new_page.reconstruction_page.qdial_number_of_iteration.value())
        alpha = float(self.new_page.reconstruction_page.QcomboBox_regularyzation_parameter.currentText())
        method = self.new_page.reconstruction_page.Method_of_reconstruction.currentText()
        raw_data = np.array(Dictionaries._AppModel['raw_data'])
        HT_data = get_data_from_array(raw_data)
        data_frame_full = {'stimulation': HT_data['stimulation'], 'voltages': HT_data['voltages']}

        DFs = separate_EIT_data_frame(data_frame_full)

        if ('message' in DFs):
            data_frame = data_frame_full

        else:
            data_frame = {'stimulation': DFs['stimulation'], 'voltages': DFs['voltages_P']}
        self.up_grade_info_box('Defined preliminary variables')

        eit_3D.up_grade_value_elems(np.ones_like(eit_3D.value_elems))

        U_ref = eit_3D.simulation()

        voltage_factor = np.linalg.norm(data_frame['voltages']) / np.linalg.norm(U_ref)

        U = (1.0 / voltage_factor) * data_frame['voltages'].reshape(-1)
        Dictionaries._AppModel['U1'] = U
        if (type(alpha).__name__ != 'float'): raise TypeError("Parameter 'alpha' is not valid.")

        if (alpha <= 0): raise ValueError("Parameter 'alpha' is not valid.")


        eit_3D.profiler['reconstruction_gn'] = True

        max_iterations = int(max_iterations)

        if (max_iterations < 1): raise ValueError("Parameter 'max_iterations' is not valid.")

        self.up_grade_info_box('Calculate reconstruction')

        # ['Tikhonov', 'Damp_Newton', 'Kotre',
        #  'Marquardt-Levenberg', 'Total Variation', 'Elasticnet']
        if method == 'Gausse-Newton' or method == 'Total Variation':

            R = matrix_laplacea(eit_3D.elems, eit_3D.nodes, 'tetra')

            RtR = (R.T @ R).toarray()

            RtR = RtR.astype(np.float_)

            eit_3D.change_ms_inv(lamb=alpha, RtR=RtR)
            if progress_callback is None:
                eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True)
            else:
                eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True, progress_callback=progress_callback)
            U2 = eit_3D.fs
        if method == 'Tikhonov':
            eit_3D.change_ms_inv(lamb=alpha, method='dgn')
            if progress_callback is None:
                eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True)
            else:
                eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True, progress_callback=progress_callback)
            U2 = eit_3D.fs
        if method == 'Marquardt-Levenberg':
            eit_3D.change_ms_inv(lamb=alpha, method='lm')
            if progress_callback is None:
                eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True)
            else:
                eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True, progress_callback=progress_callback)
            U2 = eit_3D.fs

        if method == 'Kotre':
            eit_3D.change_ms_inv(lamb=alpha, method='kotre')
            if progress_callback is None:
                eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True)
            else:
                eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True, progress_callback=progress_callback)
            U2 = eit_3D.fs

        if method == 'Elasticnet':
            parametry = json.load(open(r'modules\EIT_3D_kolo_parametry_elast.json'))
            parametry.keys()
            par = parametry['wspolczynniki']
            par = np.array(par)
            rec = par @ np.vstack((np.array([1]), U.reshape(-1, 1)))
            eit_3D.up_grade_value_elems(rec.reshape(-1))
            U2 = eit_3D.simulation()

        sigma = copy.deepcopy(eit_3D.value_elems)

        sigma[sigma < 1.0E-5] = 1.0E-5

        eit_3D.up_grade_value_elems(sigma)

        V = vars(copy.deepcopy(eit_3D))

        V['HT_data'] = HT_data
        V['method'] = method

        # V = vars(copy.deepcopy(V))
        for k in V.keys():
            try:
                V[k] = getattr(eit_3D, k)
            except:
                zero = 0

        if not os.path.exists('data'):
            os.makedirs('data')

        TimeLabel = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")

        np.savez('data\\reconstruction_' + TimeLabel, np.array(V))

        Dictionaries._AppModel['U2'] = U2
        self.printVoltages()


        return eit_3D


    def solve_inverse_problem(self, progress_callback):
        """
        Funkcja rozwiązuje problem odwrotny w elektrycznej tomografii impedancyjnej.
        W przypadku przekazania nowej ramki danych wyniki są zapisywane do pliku 'reconstruction.npz' w katalogu z bieżącym skryptem.

        Parametry wejściowe:
        finite_element_mesh: ścieżka do pliku MAT z siatką zbudowaną z czworościanów, siatka musi posiadać elektrody powierzchniowe
        data_frame: ścieżka do pliku CSV z ramką danych EIT
        alpha: parametr regularyzacyjny - dodatnia liczba rzeczywista
        max_iterations: maksymalna liczna iteracji w metodzie Gaussa-Newtona

        Parametr wyjściowy:
        eit_3D - obiekt klasy Image_EIT_3D_tetra - zawiera model oraz rozwiązanie zagadnienia odwrotnego """
        # time.sleep(2)
        finite_element_mesh = self.new_page.reconstruction_page.Label_load_model.text()
        data_frame = self.new_page.reconstruction_page.Label_load_Voltages.text()
        max_iterations = int(self.new_page.reconstruction_page.qdial_number_of_iteration.value())
        alpha = float(self.new_page.reconstruction_page.QcomboBox_regularyzation_parameter.currentText())
        method = self.new_page.reconstruction_page.Method_of_reconstruction.currentText()
        progress_callback.emit('Loading Model')

        mesh = load_mesh_from_mat_file_v2(finite_element_mesh)

        progress_callback.emit('Loading data frame')

        HT_data = load_data_from_HT2(data_frame)

        data_frame_full = {'stimulation': HT_data['stimulation'], 'voltages': HT_data['voltages']}

        DFs = separate_EIT_data_frame(data_frame_full)

        if ('message' in DFs):
            data_frame = data_frame_full

        else:
            data_frame = {'stimulation': DFs['stimulation'], 'voltages': DFs['voltages_P']}

        stimulation = data_frame['stimulation']

        stimulation['z_contact'] = mesh['z_contact']

        eit_3D = Image_EIT_3D_tetra(mesh, stimulation=stimulation, shape_ele='surface')
        progress_callback.emit('Defined preliminary variables')
        eit_3D.set_up()

        eit_3D.up_grade_value_elems(np.ones_like(eit_3D.value_elems))

        U_ref = eit_3D.simulation()

        voltage_factor = np.linalg.norm(data_frame['voltages']) / np.linalg.norm(U_ref)

        U = (1.0 / voltage_factor) * data_frame['voltages']
        Dictionaries._AppModel['U1'] = U


        if (type(alpha).__name__ != 'float'): raise TypeError("Parameter 'alpha' is not valid.")

        if (alpha <= 0): raise ValueError("Parameter 'alpha' is not valid.")


        eit_3D.profiler['reconstruction_gn'] = True

        max_iterations = int(max_iterations)

        if (max_iterations < 1): raise ValueError("Parameter 'max_iterations' is not valid.")

        progress_callback.emit('Calculate reconstruction')

        # ['Tikhonov', 'Damp_Newton', 'Kotre',
        #  'Marquardt-Levenberg', 'Total Variation']
        if method == 'Gausse-Newton' or method == 'Total Variation':

            R = matrix_laplacea(eit_3D.elems, eit_3D.nodes, 'tetra')

            RtR = (R.T @ R).toarray()

            RtR = RtR.astype(np.float_)

            eit_3D.change_ms_inv(lamb=alpha, RtR=RtR)
            eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True, progress_callback=progress_callback)
            U2 = eit_3D.fs
        if method == 'Tikhonov':
            eit_3D.change_ms_inv(lamb=alpha, method='dgn')
            eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True, progress_callback=progress_callback)
            U2 = eit_3D.fs
        if method == 'Marquardt-Levenberg':
            eit_3D.change_ms_inv(lamb=alpha, method='lm')
            eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True, progress_callback=progress_callback)
            U2 = eit_3D.fs

        if method == 'Kotre':
            eit_3D.change_ms_inv(lamb=alpha, method='kotre')
            eit_3D.reconstruction_gn(U, maxiter=max_iterations, obj_fun_val=True, progress_callback=progress_callback)
            U2 = eit_3D.fs

        if method == 'Elasticnet':
            parametry = json.load(open(r'modules\EIT_3D_kolo_parametry_elast.json'))
            parametry.keys()
            par = parametry['wspolczynniki']
            par = np.array(par)
            rec = par @ np.vstack((np.array([1]), U.reshape(-1, 1)))
            eit_3D.up_grade_value_elems(rec.reshape(-1))
            U2 = eit_3D.simulation()

        sigma = copy.deepcopy(eit_3D.value_elems)

        sigma[sigma < 1.0E-5] = 1.0E-5

        eit_3D.up_grade_value_elems(sigma)

        V = vars(copy.deepcopy(eit_3D))

        V['HT_data'] = HT_data
        V['method'] = method

        # V = vars(copy.deepcopy(V))
        for k in V.keys():
            try:
                V[k] = getattr(eit_3D, k)
            except:
                zero = 0

        if not os.path.exists('data'):
            os.makedirs('data')

        TimeLabel = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")

        np.savez('data\\reconstruction_' + TimeLabel, np.array(V))
        self.EIT_reconstruction = eit_3D

        Dictionaries._AppModel['U2'] = U2
        self.printVoltages()


        return eit_3D

    def rotation_zy(self):
        # print(self.keyboardBox.isVisible())
        # if self.keyboardBox.isVisible():
        #     self.keyboardBox.hide()
        # print(self.keyboardBox.isVisible())
        alpha = self.new_page.reconstruction_page.sliderHorizontal.value()
        beta = self.new_page.reconstruction_page.sliderVertical.value()
        Rzy = rotation_ZY(alpha, beta)
        old_up = np.array([[-1, 0, 1]]).reshape(3, 1)

        new_up = np.matmul(Rzy, old_up).reshape(-1)

        colormap = np.load('cm/cm_seismic_plotly.npy')
        sm = [[float(colormap[x][0]), colormap[x][1]] for x in range(256)]
        Model = Dictionaries._AppModel['Model']
        Fig = Model.display(middle_value=Model.value_elems.mean(), colormap=sm)
        # camera = dict(eye=dict(x=1.25, y=1.25, z=1.25),
        #               up=dict(x=0,y=0,z=0),
        #               # up=dict(x=np.round(old_up[0],2), y=np.round(old_up[1],2), z=np.round(old_up[2],2)),
        #               center=dict(x=0, y=0, z=0)),  # the default values are 1.25, 1.25, 1.25
        #
        #
        #
        # Fig.update_layout(scene_camera=camera)
        # Default parameters which are used when `layout.scene.camera` is not provided
        scene = dict(camera=dict(up=dict(x=new_up[0], y=new_up[1], z=new_up[2])),  # the default values are 1.25, 1.25, 1.25
                     xaxis=dict(),
                     yaxis=dict(),
                     zaxis=dict(),
                     aspectmode='data',  # this string can be 'data', 'cube', 'auto', 'manual'
                     # a custom aspectratio is defined as follows:
                     aspectratio=dict(x=1, y=1, z=0.95)
                     )
        Fig.update_layout(scene=scene)
        Fig.write_html("recon_html/figure.html")
        # self.new_page.inputGraph.clear_Graph()
        # self.new_page.inputGraph.load_html(Fig.to_html(include_plotlyjs='cdn'))
        self.new_page.reconstruction_page.inputGraph.webview.setHtml(Fig.to_html(include_plotlyjs='cdn'))
        # self.new_page.inputGraph.setSource(QUrl.fromLocalFile("recon_html/figure.html"))

    def get_value_to_slice(self, axis, s=None):
        if s is None:
            s = Dictionaries._AppModel['Model']
        if axis == 0:
            value = self.new_page.grid_page.x_slider.value() * 0.01
            x_min = s.nodes[:, 0].min()
            x_max = s.nodes[:, 0].max()
            value = value * (x_max - x_min) + x_min

        if axis == 1:
            value = self.new_page.grid_page.y_slider.value() * 0.01
            y_min = s.nodes[:, 1].min()
            y_max = s.nodes[:, 1].max()
            value = value * (y_max - y_min) + y_min
        if axis == 2:
            value = self.new_page.grid_page.z_slider.value() * 0.01
            z_min = s.nodes[:, 2].min()
            z_max = s.nodes[:, 2].max()
            value = value * (z_max - z_min) + z_min
        return value


    def get_value_to_slices(self, s):
        value_x = self.new_page.grid_page.x_slider.value() * 0.01
        value_y = self.new_page.grid_page.y_slider.value() * 0.01
        value_z = self.new_page.grid_page.z_slider.value() * 0.01
        x_min = s.nodes[:, 0].min()
        y_min = s.nodes[:, 1].min()
        z_min = s.nodes[:, 2].min()
        x_max = s.nodes[:, 0].max()
        y_max = s.nodes[:, 1].max()
        z_max = s.nodes[:, 2].max()
        value = np.array([value_x*(x_max-x_min) + x_min,
                          value_y*(y_max-y_min) + y_min,
                          value_z*(z_max-z_min) + z_min])
        return value

    def build_slice(self, W_i, axis, reference_level=None):
        if axis == 0:
            W = list(W_i)
            pom = np.row_stack([W[0][:, 1], W[0][:, 2]]).T
            W[0] = pom
            sc = build_tri(W, reference_level=reference_level)
            Dictionaries._AppModel['Wx'] = W

        if axis == 1:
            W = list(W_i)
            pom = np.row_stack([W[0][:, 0], W[0][:, 2]]).T
            W[0] = pom
            Dictionaries._AppModel['Wy'] = W
            sc = build_tri(W, reference_level=reference_level)
        if axis == 2:
            W = list(W_i)
            pom = np.row_stack([W[0][:, 0], W[0][:, 1]]).T
            W[0] = pom
            Dictionaries._AppModel['Wz'] = W

            sc = build_tri(W, reference_level=reference_level)
        return sc



    def build_slices(self, W):

        W_x = list(W[0])
        pom_x = np.row_stack([W_x[0][:, 1], W_x[0][:, 2]]).T
        W_x[0] = pom_x
        W_y = list(W[1])
        pom_y = np.row_stack([W_y[0][:, 0], W_y[0][:, 2]]).T
        W_y[0] = pom_y
        W_z = list(W[2])
        pom_z = np.row_stack([W_z[0][:, 0], W_z[0][:, 1]]).T
        W_z[0] = pom_z
        Dictionaries._AppModel['Wx'] = W_x
        Dictionaries._AppModel['Wy'] = W_y
        Dictionaries._AppModel['Wz'] = W_z
        sc_x = build_tri(W_x)
        sc_y = build_tri(W_y)
        sc_z = build_tri(W_z)

        # im_x = QImage(sc_x.buffer_rgba(), sc_x.size().height(), sc_x.width(), QImage.Format_ARGB32)
        # im_y = QImage(sc_y.buffer_rgba(), sc_y.size().height(), sc_y.width(), QImage.Format_ARGB32)
        # im_z = QImage(sc_z.buffer_rgba(), sc_z.size().height(), sc_z.width(), QImage.Format_ARGB32)

        return [sc_x, sc_y, sc_z]


    def change_axis_slices(self):
        scene = dict(camera=dict(eye=dict(x=2, y=2, z=2)),
                     xaxis=dict(),
                     yaxis=dict(),
                     zaxis=dict(),
                     aspectmode='data',
                     aspectratio=dict(x=1, y=1, z=1.95)
                     )
        s = Dictionaries._AppModel['Model']
        value = self.get_value_to_slices(s)
        Dictionaries._AppModel['value_x'] = value[0]
        Dictionaries._AppModel['value_y'] = value[1]
        Dictionaries._AppModel['value_z'] = value[2]

        colormap = np.load('cm/cm_seismic_plotly.npy')
        sm = [[float(colormap[x][0]), colormap[x][1]] for x in range(256)]
        [fig_slices, W] = s.display_slice(axis=np.array([0, 1, 2]), value=value, middle_value=s.value_elems.mean(), colormap=sm)

        fig_slices.update_layout(scene=scene)
        fig_slices.update_traces(showscale=False)
        fig_slices.write_image("recon_html/figure.png", width=400, height=400)
        pixmap = QPixmap('recon_html/figure.png')

        self.new_page.grid_page.axis_slices.setPixmap(pixmap)
        self.new_page.grid_page.axis_slices.show()


    def change_slicer_x(self, axis3D = True):
        if axis3D:
            self.change_axis_slices()
        s = Dictionaries._AppModel['Model']
        value = self.get_value_to_slice(0, s)
        reference_level = s.value_elems.mean()

        W = s.build_slice(0, value)

        slice = self.build_slice(W, 0, reference_level=reference_level)

        self.new_page.grid_page.axis_slice_x.setPixmap(slice)
        self.new_page.grid_page.axis_slice_x.show()
        x_text = QCoreApplication.translate("MainWindow", Dictionaries._AppLang['Slice plane x = ']
        [Dictionaries._AppVars['Language']], None)
        self.new_page.grid_page.x_text.setText(x_text + str(value))


    def change_slicer_y(self, axis3D=True):
        if axis3D:
            self.change_axis_slices()
        s = Dictionaries._AppModel['Model']
        value = self.get_value_to_slice(1, s)
        reference_level = s.value_elems.mean()

        W = s.build_slice(1, value)

        slice = self.build_slice(W, 1, reference_level=reference_level)

        self.new_page.grid_page.axis_slice_y.setPixmap(slice)
        self.new_page.grid_page.axis_slice_y.show()
        y_text = QCoreApplication.translate("MainWindow", Dictionaries._AppLang['Slice plane y = ']
        [Dictionaries._AppVars['Language']], None)
        self.new_page.grid_page.y_text.setText(y_text + str(value))


    def change_slicer_z(self, axis3D=True):
        if axis3D:
            self.change_axis_slices()
        s = Dictionaries._AppModel['Model']
        value = self.get_value_to_slice(2, s)
        reference_level = s.value_elems.mean()

        W = s.build_slice(2, value)

        slice = self.build_slice(W, 2, reference_level=reference_level)

        self.new_page.grid_page.axis_slice_z.setPixmap(slice)
        self.new_page.grid_page.axis_slice_z.show()
        z_text = QCoreApplication.translate("MainWindow", Dictionaries._AppLang['Slice plane z = ']
                [Dictionaries._AppVars['Language']], None)
        self.new_page.grid_page.z_text.setText(z_text + str(value))

    def printVoltages(self):
        # pixmap = print_voltages(U1, U2)
        U1 = Dictionaries._AppModel['U1']
        U2 = Dictionaries._AppModel['U2']

        pen1 = pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.SolidLine)
        pen2 = pg.mkPen(color=(0, 0, 255), width=2, style=QtCore.Qt.SolidLine)


        # self.new_page.grid_page.axis_voltages = pg.plot()
        try:
            self.new_page.grid_page.axis_voltages.clear()
        except:
            zero = 0
        self.new_page.grid_page.axis_voltages.addLegend()

        # Dodawanie danych do wykresu
        self.new_page.grid_page.axis_voltages.plot(U1, pen=pen1, name='Voltages real')
        self.new_page.grid_page.axis_voltages.plot(U2, pen=pen2, name='Voltages calculated')

        self.new_page.grid_page.axis_voltages.setBackground('white')
        self.new_page.grid_page.axis_voltages.plot()



    def do_nothing(self):
        pass









