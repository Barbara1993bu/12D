# -*- coding: utf-8 -*-

import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtQuickWidgets import QQuickWidget
# from . animated_toggle import AnimatedToggle

from resources import *

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


# -----------------------------------------
# define custom widgets with text input,
# they are required for use of virtual keyboard
# -----------------------------------------

class nxQLineEdit(QLineEdit):

    focused = pyqtSignal()
    noneFocused = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()

class nxQDateEdit(QDateEdit):

    focused = pyqtSignal()
    noneFocused = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()

class nxQDateTimeEdit(QDateTimeEdit):

    focused = pyqtSignal()
    noneFocused = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()

class nxQDoubleSpinBox(QDoubleSpinBox):

    focused = pyqtSignal()
    noneFocused = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()

class nxQDoubleSpinBox(QDoubleSpinBox):

    focused = pyqtSignal()
    noneFocused = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()

class nxQTimeEdit(QTimeEdit):

    focused = pyqtSignal()
    noneFocused = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused.emit()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.noneFocused.emit()

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
        self.appMargins.setContentsMargins(10, 10, 10, 10)

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
        self.headerHorizLayout.setContentsMargins(0, 0, 10, 0)

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
        self.headerHorizLayoutBtns.setContentsMargins(0, 0, 25, 0)

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
        self.vertLayoutContainer.setContentsMargins(10, 10, 10, 10)

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
        self.widgets = QWidget()
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"b")

        self.vertLayoutWidgets = QVBoxLayout(self.widgets)
        self.vertLayoutWidgets.setObjectName(u"vertLayoutWidgets")


        # # self.testinput = self.nxQLineEdit
        # self.vertLayoutWidgets.addWidget(self.nxQLineEdit)

        # test = QCheckBox()
        # test.setStyleSheet("QCheckBox::indicator { width: 50px; height: 50px;}")
        # self.vertLayoutWidgets.addWidget(test)



        self.vertLayoutWidgets.addWidget(self.nxQLineEdit)

        self.vertLayoutWidgets.addWidget(self.nxQDateEdit)

        self.vertLayoutWidgets.addWidget(self.nxQDateTimeEdit)

        self.vertLayoutWidgets.addWidget(self.nxQDoubleSpinBox)
        self.vertLayoutWidgets.addWidget(self.nxQTimeEdit)
        # self.vertLayoutWidgets.addWidget(self.nxQTimeEdit)


        self.stackedWidget.addWidget(self.widgets)


        # -----------------------------------------
        # New Page Frame
        self.new_page = QWidget()
        self.new_page.setObjectName(u"new_page")

        self.vertLayoutNewPage = QVBoxLayout(self.new_page)
        self.vertLayoutNewPage.setObjectName(u"vertLayoutNewPage")

        self.label = QLabel(self.new_page)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        # attach label widget to new page layout
        self.vertLayoutNewPage.addWidget(self.label)

        self.inputText = QLineEdit()
        self.vertLayoutNewPage.addWidget(self.inputText)

        # attach new page to stacked widgets
        self.stackedWidget.addWidget(self.new_page)


        # -----------------------------------------
        # Setting Frame
        self.setting_page = QWidget()
        self.setting_page.setObjectName(u"setting_page")

        self.vertLayoutNewPage = QVBoxLayout(self.setting_page)
        self.vertLayoutNewPage.setObjectName(u"vertLayoutNewPage")

        # self.label = QLabel(self.setting_page)
        # self.label.setObjectName(u"label")
        # self.label.setAlignment(Qt.AlignCenter)
        # self.label.setText("Settings")

        # attach label widget to new page layout
        self.vertLayoutNewPage.addWidget(QLabel("Settings"))

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
        # self.keyboardBox.setStyleSheet(u"background-color: rgb (230, 230, 230);")
        self.keyboardBox.setObjectName(u"keyboardBox")
        self.keyboardBox.setMinimumSize(QSize(0, 0))
        self.keyboardBox.setMaximumSize(QSize(10000, 0))
        self.keyboardBox.setFrameShape(QFrame.NoFrame)
        self.keyboardBox.setFrameShadow(QFrame.Raised)

        self.keyboardBoxLayout = QVBoxLayout(self.keyboardBox)

        self.keyboardwidget = QQuickWidget(self.keyboardBox)
        self.keyboardwidget.setMinimumSize(QSize(845,320))
        self.keyboardwidget.setMaximumSize(QSize(845,320))
        self.keyboardwidget.setSource(QUrl.fromLocalFile("src/keyboard.qml"))
        self.keyboardwidget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.keyboardwidget.setAttribute(Qt.WA_AcceptTouchEvents)
        self.keyboardwidget.setFocusPolicy(Qt.NoFocus)
        self.keyboardwidget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.keyboardwidget.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)

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

        self.appTitle.setText(QCoreApplication.translate("MainWindow", u"UST 4.0", None))
        self.appTitleDescription.setText(QCoreApplication.translate("MainWindow", u"Ultrasound Tomography Device", None))

        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))

        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_widgets.setText(QCoreApplication.translate("MainWindow", u"Widgets", None))
        self.btn_new.setText(QCoreApplication.translate("MainWindow", u"New", None))
        # self.btn_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        # self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))


        self.moreSettingsBtn.setToolTip(QCoreApplication.translate("MainWindow", u"More Options", None))
        self.moreSettingsBtn.setText("")


        self.btn_closeApp.setText(QCoreApplication.translate("MainWindow", u"Close Application", None))
        self.btn_restartApp.setText(QCoreApplication.translate("MainWindow", u"Restart Application", None))
        self.btn_rebootDevice.setText(QCoreApplication.translate("MainWindow", u"Reboot Device", None))
        self.btn_shutDownDevice.setText(QCoreApplication.translate("MainWindow", u"Shut Down", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"NEW PAGE TEST", None))
