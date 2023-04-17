
# import main file
from app import *

# app functions with connection to MainWindow
class AppFunctions(MainWindow):

    def setThemeHack(self):

        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-top: 5px solid #1d65c2;
        background-color: #166cdb;
        """

        # # SET MANUAL STYLES
        # self.tui.lineEdit.setStyleSheet("background-color: #6272a4;")
        # self.tui.pushButton.setStyleSheet("background-color: #6272a4;")
        # self.tui.plainTextEdit.setStyleSheet("background-color: #6272a4;")
        # self.tui.tableWidget.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        # self.tui.scrollArea.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        # self.tui.comboBox.setStyleSheet("background-color: #6272a4;")
        # self.tui.horizontalScrollBar.setStyleSheet("background-color: #6272a4;")
        # self.tui.verticalScrollBar.setStyleSheet("background-color: #6272a4;")
        # self.tui.commandLinkButton.setStyleSheet("color: #ff79c6;")
