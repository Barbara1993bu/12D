
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import sys
import os
import platform

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtQml import *

# import modules and widgets
from modules import *

# high DPI scalling
os.environ["QT_FONT_DPI"] = "96"

# set global widgets
widgets = None

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


# main TUI Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # make app full-screen
        # self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        # load main window frame and apply setup
        self.tui = tui_MainWindow()
        self.tui.setup_tui(self)

        # declare all app widgets
        global widgets
        widgets = self.tui

        # application name
        title = "Touch User Interface UST 4.0"

        # apply text
        self.setWindowTitle(title)

        # toggle menu
        widgets.toggleButton.clicked.connect(
            lambda: TUIFunctions.toggleMenu(self, True))

        # setup tui definitions
        TUIFunctions.tuiDefinitions(self)

        # left menu buttons
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_settings.clicked.connect(self.buttonClick)

        # open and close More Settings Tab
        def openCloseMoreSettingsTab():
            TUIFunctions.toggleRightTab(self, True)

        widgets.moreSettingsBtn.clicked.connect(openCloseMoreSettingsTab)

        # open and close Keyboard Tab
        def openCloseKeyboardTab():

            if not self.check_virtual_keyboard_visibility():
                TUIFunctions.toggleKeyboardTab(self, True)
                QApplication.instance().inputMethod().show()
            else:
                TUIFunctions.toggleKeyboardTab(self, False)
                QApplication.instance().inputMethod().hide()

        # definition of virtual keyboard triggers
        widgets.nxQLineEdit.focused.connect(openCloseKeyboardTab)
        widgets.nxQLineEdit.noneFocused.connect(openCloseKeyboardTab)

        # show application
        self.show()

        # use custom theme
        useCustomTheme = True
        themeFile = "themes\\p_theme_test.qss"

        # set theme and hacks
        if useCustomTheme:
            # load and apply style
            TUIFunctions.theme(self, themeFile, True)

            # set hacks
            AppFunctions.setThemeHack(self)

        # set home page and select menu
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(
            TUIFunctions.selectMenu(
                widgets.btn_home.styleSheet()))

    # button clicks
    def buttonClick(self):

        btn = self.sender()  # get button
        btnName = btn.objectName()  # pass button name

        # show home page
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)   # set page
            # reset another buttons
            TUIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(
                TUIFunctions.selectMenu(
                    btn.styleSheet()))    # select menu

        # show widgets page
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            TUIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))

        # show new page
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)
            TUIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))

        # show settings
        if btnName == "btn_settings":
            widgets.stackedWidget.setCurrentWidget(widgets.setting_page)
            TUIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))

        # print btn name
        print(f'Button "{btnName}" pressed!')

    # mouse click event
    def mousePressEvent(self, event):

        # drag position event
        self.dragPos = event.pos()

        # print mouse click event
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')

        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
            print(self.check_virtual_keyboard_visibility())

    def check_virtual_keyboard_visibility(self):
        # Get the virtual keyboard widget using its object name
        virtual_keyboard = QApplication.instance().inputMethod()

        # Check if the virtual keyboard widget is visible
        try:
            return virtual_keyboard.isVisible()
        except:
            raise Exception("Sorry, virtual keyboard can not be found!")


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("nx_logo.ico"))
    window = MainWindow()
    sys.exit(app.exec())
