

# import main file
import time

from app import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os

# global variables
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True


def restart():

    QCoreApplication.quit()
    status = QProcess.startDetached(sys.executable, sys.argv)
    print(status)


def reboot():
    os.system("shutdown -t 0 -r -f")


def shut_down():
    os.system('shutdown -s -t 0')


class TUIFunctions(MainWindow):

    # # maximize/restore main window
    # def maximize_restore(self):
    #
    #     global GLOBAL_STATE
    #     status = GLOBAL_STATE
    #
    #     if status == False:
    #         self.showMaximized()
    #         GLOBAL_STATE = True
    #         self.tui.appMargins.setContentsMargins(0, 0, 0, 0)
    #         self.tui.maximizeRestoreAppBtn.setToolTip("Restore")
    #         self.tui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
    #         self.tui.frame_size_grip.hide()
    #         self.left_grip.hide()
    #         self.right_grip.hide()
    #         self.top_grip.hide()
    #         self.bottom_grip.hide()
    #
    #     else:
    #         GLOBAL_STATE = False
    #         self.showNormal()
    #         self.resize(self.width()+1, self.height()+1)
    #         self.tui.appMargins.setContentsMargins(10, 10, 10, 10)
    #         self.tui.maximizeRestoreAppBtn.setToolTip("Maximize")
    #         self.tui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))
    #         self.tui.frame_size_grip.show()
    #         self.left_grip.show()
    #         self.right_grip.show()
    #         self.top_grip.show()
    #         self.bottom_grip.show()

    # return status
    def returStatus(self):
        return GLOBAL_STATE

    # set status
    def setStatus(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # toggle menu animation
    def toggleMenu(self, enable):

        time.sleep(0.1)

        if enable:
            # get width
            width = self.tui.leftMenuBg.width()
            maxExtend = Settings.MENU_WIDTH
            standard = 100

            # set max width
            if width == 100:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # animation
            self.animation = QPropertyAnimation(
                self.tui.leftMenuBg, b"minimumWidth")
            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    # toggle right tab

    def toggleRightTab(self, enable):

        time.sleep(0.1)

        if enable:
            # get width
            width = self.tui.extraRightBox.width()
            widthLeftBox = 0  # self.tui.extraLeftBox.width()
            maxExtend = Settings.RIGHT_BOX_WIDTH
            color = Settings.BTN_RIGHT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.tui.moreSettingsBtn.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.tui.moreSettingsBtn.setStyleSheet(style + color)
                if widthLeftBox != 0:
                    style = self.tui.toggleLeftBox.styleSheet()
                    self.tui.toggleLeftBox.setStyleSheet(
                        style.replace(Settings.BTN_LEFT_BOX_COLOR, ''))
            else:
                widthExtended = standard
                # RESET BTN
                self.tui.moreSettingsBtn.setStyleSheet(
                    style.replace(color, ''))

            TUIFunctions.start_box_animation(
                self, widthLeftBox, width, "right")

    # toggle right tab
    def toggleKeyboardTab(self, enable):

        if enable:

            # get height
            height = self.tui.keyboardBox.height()
            heightContentBox = self.tui.mainContentFrame.height()
            maxExtend = Settings.KEYBOARD_BOX_HEIGHT

            standardExtend = 0

            # SET MAX HEIGHT
            if height == 0:
                heightExtend = maxExtend

            else:
                heightExtend = standardExtend

            TUIFunctions.start_keyboard_box_animation(self, heightContentBox, height, heightExtend)

        else:

            height = self.tui.keyboardBox.height()
            heightContentBox = self.tui.mainContentFrame.height()

            QApplication.instance().inputMethod().hide()
            TUIFunctions.start_keyboard_box_animation(self, heightContentBox, height, 0)

    def start_box_animation(self, left_box_width, right_box_width, direction):

        right_width = 0
        left_width = 0

        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = 250
        else:
            left_width = 0
        # Check values
        if right_box_width == 0 and direction == "right":
            right_width = 250
        else:
            right_width = 0

        # ANIMATION RIGHT BOX
        self.right_box = QPropertyAnimation(
            self.tui.extraRightBox, b"minimumWidth")
        self.right_box.setDuration(Settings.TIME_ANIMATION)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        # self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()


    def start_keyboard_box_animation(self, content_box_height, keyboard_box_height, heightExtend):

        # Check values
        if keyboard_box_height == 0:
            keyboard_height = heightExtend

            self.tui.keyboardBox.setStyleSheet(u"background-color: #000000;")
            self.tui.keyboardwidget.setStyleSheet(
                u"background-color: #000000;")

        else:
            keyboard_height = 0

        # ANIMATION KEYBOARD BOX
        self.keyboard_box = QPropertyAnimation(self.tui.keyboardBox, b"minimumHeight")
        self.keyboard_box.setDuration(Settings.KEYBOARD_TIME_ANIMATION)
        self.keyboard_box.setStartValue(keyboard_box_height)
        self.keyboard_box.setEndValue(keyboard_height)
        self.keyboard_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.keyboard_box)
        self.group.start()

        print(f'after anim {self.tui.keyboardBox.height()}')

    # select/deselect page
    # select

    def selectMenu(getStyle):
        select = getStyle + Settings.MENU_SELECTED_STYLESHEET
        return select

    # deselect
    def deselectMenu(getStyle):
        deselect = getStyle.replace(Settings.MENU_SELECTED_STYLESHEET, "")
        return deselect

    # start selection
    def selectStandardMenu(self, widget):
        for w in self.tui.topMenu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(TUIFunctions.selectMenu(w.styleSheet()))

    # reset page selection
    def resetStyle(self, widget):
        for w in self.tui.topMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(TUIFunctions.deselectMenu(w.styleSheet()))

        for w in self.tui.bottomMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(TUIFunctions.deselectMenu(w.styleSheet()))

    # import QSS theme
    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            str = open(file, 'r').read()
            self.tui.styleSheet.setStyleSheet(str)

    # TUI definitions
    def tuiDefinitions(self):

        self.tui.appMargins.setContentsMargins(0, 0, 0, 0)

        # self.tui.minimizeAppBtn.hide()
        # self.tui.maximizeRestoreAppBtn.hide()
        # self.tui.closeAppBtn.hide()
        # self.tui.frame_size_grip.hide()

        # # drop shadow
        # self.shadow = QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(17)
        # self.shadow.setXOffset(0)
        # self.shadow.setYOffset(0)
        # self.shadow.setColor(QColor(0, 0, 0, 150))
        # self.tui.bgApp.setGraphicsEffect(self.shadow)

        # # resize application window
        # self.sizegrip = QSizeGrip(self.tui.frame_size_grip)
        # self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # # minimize application
        # self.tui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # maximize/restore application
        # self.tui.maximizeRestoreAppBtn.clicked.connect(lambda: TUIFunctions.maximize_restore(self))

        # close application
        self.tui.btn_closeApp.clicked.connect(lambda: self.close())

        # restart application
        self.tui.btn_restartApp.clicked.connect(restart)

        # reboot device
        # self.tui.btn_rebootDevice.clicked.connect(reboot)

        # shut down device
        # self.tui.btn_shutDownDevice.clicked.connect(shut_down)
