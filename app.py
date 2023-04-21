import time

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


# -----------------------------------------
# define custom QMessageWindow
# -----------------------------------------

class nxMessageWindow(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        # Set custom font and background color
        font = QFont("Segoe UI Semibold", 18)
        self.setFont(font)

        self.setStyleSheet("QMessageBox {"
                           "width:500 px;"
                           "background-color: #3c7bcf;"
                           "border-style: solid;"
                           "border-width: 5px;"
                           "border-radius: 0px;"
                           "border-color: #93e1f9;"
                           "}")

        # Create a custom label with a different font and style
        self.mbLabel = QLabel("?")
        self.mbLabel.setFont(QFont("Segoe UI Semibold", 20))
        self.mbLabel.setStyleSheet("QLabel{"
                                   "min-width:400 px;"
                                   "min-height:0 px;"
                                   "font-size: 18px;"
                                   "background-color: #3c7bcf;"
                                   "}")

        # Create custom button with icon
        customButtonYes = QPushButton(
            QIcon(u":/icons/images/icons/check-circle.svg"), "")
        customButtonYes.setStyleSheet("QPushButton {"
                                      "width:150px;"
                                      "height:50px;"
                                      "background-color: #3c7bcf;"
                                      "color: white;"
                                      "border-style: outset;"
                                      "border-width: 5px;"
                                      "border-radius: 15px;"
                                      "border-color: #93e1f9;"
                                      "font: bold 14px;"
                                      "min-width: 10em;"
                                      "padding: 6px;"
                                      "}")
        customButtonYes.setIconSize(QSize(50, 50))

        # Create custom button with icon
        customButtonNo = QPushButton(
            QIcon(u":/icons/images/icons/x-circle.svg"), "")
        customButtonNo.setStyleSheet("QPushButton {"
                                     "width:150px;"
                                     "height:50px;"
                                     "background-color: #3c7bcf;"
                                     "color: white;"
                                     "border-style: outset;"
                                     "border-width: 5px;"
                                     "border-radius: 15px;"
                                     "border-color: #93e1f9;"
                                     "font: bold 14px;"
                                     "min-width: 10em;"
                                     "padding: 6px;"
                                     "}")
        customButtonNo.setIconSize(QSize(50, 50))

        self.addButton(customButtonYes, QMessageBox.YesRole)
        self.addButton(customButtonNo, QMessageBox.NoRole)

        # Custom alignment
        grid_layout = self.layout()

        qt_msgboxex_icon_label = self.findChild(
            QLabel, "qt_msgboxex_icon_label")
        qt_msgboxex_icon_label.deleteLater()

        qt_msgbox_label = self.findChild(QLabel, "qt_msgbox_label")
        qt_msgbox_label.setAlignment(Qt.AlignCenter)
        grid_layout.removeWidget(qt_msgbox_label)

        qt_msgbox_buttonbox = self.findChild(
            QDialogButtonBox, "qt_msgbox_buttonbox")
        grid_layout.removeWidget(qt_msgbox_buttonbox)

        grid_layout.addWidget(qt_msgbox_label, 0, 0, alignment=Qt.AlignCenter)
        grid_layout.addWidget(qt_msgbox_buttonbox, 1, 0,
                              alignment=Qt.AlignCenter)

    def retranslateMessageBox(self):
        self.setText(QCoreApplication.translate("nxMessageWindow", u"?", None))


# -----------------------------------------
# main TUI Window
# -----------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # # make app full-screen
        # self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        # # self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
        # # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)

        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowFlag(Qt.WindowStaysOnBottomHint)
        self.setWindowState(Qt.WindowMaximized)

        # load main window frame and apply setup
        self.tui = tui_MainWindow()
        self.tui.setup_tui(self)

        # create pool for new threads
        self.threadpool = QThreadPool()
        print(
            "Multithreading with maximum %d threads" %
            self.threadpool.maxThreadCount())

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
        def openKeyboardTab():

            if self.check_virtual_keyboard_visibility() and self.tui.keyboardBox.height() != 0:
                pass

            if not self.check_virtual_keyboard_visibility(
            ) and self.tui.keyboardBox.height() != 0:
                QApplication.instance().inputMethod().show()

            elif not self.check_virtual_keyboard_visibility() and self.tui.keyboardBox.height() == 0:
                TUIFunctions.toggleKeyboardTab(self, True)
                QApplication.instance().inputMethod().show()

        def closeKeyboardTab():

            TUIFunctions.toggleKeyboardTab(self, True)
            self.tui.keyboardBox.setGeometry(QRect(0, 0, 1920, 0))

        # definition of virtual keyboard triggers
        widgets.nxQLineEdit.focused.connect(openKeyboardTab)
        widgets.nxQLineEdit.noneFocused.connect(closeKeyboardTab)
        # nxQDateEdit trigger
        widgets.nxQDateEdit.focused.connect(openKeyboardTab)
        widgets.nxQDateEdit.noneFocused.connect(closeKeyboardTab)
        # nxQDateTimeEdit trigger
        widgets.nxQDateTimeEdit.focused.connect(openKeyboardTab)
        widgets.nxQDateTimeEdit.noneFocused.connect(closeKeyboardTab)
        # nxQDoubleSpinBox trigger
        widgets.nxQDoubleSpinBox.focused.connect(openKeyboardTab)
        widgets.nxQDoubleSpinBox.noneFocused.connect(closeKeyboardTab)
        # nxQDateTimeEdit trigger
        widgets.nxQTimeEdit.focused.connect(openKeyboardTab)
        widgets.nxQTimeEdit.noneFocused.connect(closeKeyboardTab)

        # self.tui.btn_restartApp.clicked.connect(self.restart)

        # show application
        self.show()
        # self.showFullScreen()

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
        # print(f'Button "{btnName}" pressed!')

    # mouse click event

    def mousePressEvent(self, event):

        # drag position event
        self.dragPos = event.pos()

        # print mouse click event
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')

        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    def check_virtual_keyboard_visibility(self):

        # Get the virtual keyboard widget using its object name
        virtual_keyboard = QApplication.instance().inputMethod()

        # Check if the virtual keyboard widget is visible
        try:
            return virtual_keyboard.isVisible()
        except BaseException:
            raise Exception("Sorry, virtual keyboard can not be found!")

    def _close(self):

        self.msgCloseBox = nxMessageWindow()
        self.msgCloseBox.setText(
            Dictionaries._AppLang['Do you want to close the application?'][Dictionaries._AppVars['Language']])

        retval = self.msgCloseBox.exec_()

        if retval == 0:
            QCoreApplication.quit()

    def _restart(self):

        self.msgRestartBox = nxMessageWindow()
        self.msgRestartBox.setText(
            Dictionaries._AppLang['Do you want to restart the application?'][Dictionaries._AppVars['Language']])

        retval = self.msgRestartBox.exec_()

        if retval == 0:
            QCoreApplication.quit()
            status = QProcess.startDetached(sys.executable, sys.argv)
            print(status)

    def _reboot(self):

        self.msgRebootBox = nxMessageWindow()
        self.msgRebootBox.setText(
            Dictionaries._AppLang['Do you want to reboot the device?'][Dictionaries._AppVars['Language']])

        retval = self.msgRebootBox.exec_()

        if retval == 0:
            # os.system("shutdown -t 0 -r -f")
            print('ok')

    def _shut_down(self):

        self.msgShutDownBox = nxMessageWindow()
        self.msgShutDownBox.setText(
            Dictionaries._AppLang['Do you want to turn off the device?'][Dictionaries._AppVars['Language']])

        #test

        # Dictionaries._AppVars['Language'] = 1
        # self.tui.retranslate_tui(self)

        retval = self.msgShutDownBox.exec_()

        if retval == 0:
            # os.system('shutdown -s -t 0')
            print('ok')


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("nx_logo.ico"))
    window = MainWindow()
    sys.exit(app.exec())
