import json
import time
from datetime import datetime

import numpy as np
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer
from PySide2.QtNetwork import *

import sys
import os
import platform
import cv2
# from matplotlib.pyplot import imread
# import matplotlib
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
#
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# matplotlib.use('QtAgg')
import socket
from threading import Thread
from contextlib import contextmanager
import sys
import PySide2
import multiprocessing
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtQml import *

# import modules and widgets
from modules import *
import time
from datetime import datetime
# high DPI scalling
# os.environ["QT_FONT_DPI"] = "96"

# set global widgets
widgets = None

os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"


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
    progress = Signal(str)


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


class ClientManager(QtCore.QObject):
    def __init__(self, parent=None):
        super(ClientManager, self).__init__(parent)
        self._socket = QTcpSocket(self)
        self._socket.stateChanged.connect(self.on_stateChanged)
        self._socket.readyRead.connect(self.on_readyRead)
        self._timer = QtCore.QTimer(self, interval=1000)
        # self._timer.timeout.connect(self.sendMessage)

    def launch(self, address=QHostAddress.Any, port=9999):
        return self._socket.connectToHost(QHostAddress(address), port)

    @QtCore.Slot(QAbstractSocket.SocketState)
    def on_stateChanged(self, state):
        if state == QAbstractSocket.ConnectedState:
            self._timer.start()
            print("connected")
        elif state == QAbstractSocket.UnconnectedState:
            print("disconnected")
            QtCore.QCoreApplication.quit()

    @QtCore.Slot()
    def sendMessage(self, msg=''):
        if self._socket.state() == QAbstractSocket.ConnectedState:
            # msg = QtCore.QDateTime.currentDateTime().toString()
            self._socket.write(msg)

    @QtCore.Slot()
    def on_readyRead(self):
        return self._socket.readAll()

# -----------------------------------------
# define custom QMessageWindow
# -----------------------------------------


class nxMessageWindow(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowFlag(Qt.WindowStaysOnBottomHint)
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
        self.customButtonYes = QPushButton(
            QIcon(u":/icons/images/icons/check-circle.svg"), "")
        self.customButtonYes.setStyleSheet("QPushButton {"
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
        self.customButtonYes.setIconSize(QSize(50, 50))

        # Create custom button with icon
        self.customButtonNo = QPushButton(
            QIcon(u":/icons/images/icons/x-circle.svg"), "")
        self.customButtonNo.setStyleSheet("QPushButton {"
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
        self.customButtonNo.setIconSize(QSize(50, 50))

        self.addButton(self.customButtonYes, QMessageBox.YesRole)
        self.addButton(self.customButtonNo, QMessageBox.NoRole)

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



class VoltagesDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visualization voltages")
        self.setMaximumSize(1500, 600)
        self.setMinimumSize(1500, 600)

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        U1 = Dictionaries._AppModel['U1']
        U2 = Dictionaries._AppModel['U2']
        pen1 = pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.SolidLine)
        pen2 = pg.mkPen(color=(0, 0, 255), width=2, style=QtCore.Qt.SolidLine)


        self.win = pg.PlotWidget()
        self.win.addLegend()

        # Dodawanie danych do wykresu
        self.win.plot(U1, pen=pen1, name='Voltages real')
        self.win.plot(U2, pen=pen2, name='Voltages calculated')

        self.win.setBackground('white')


        self.layout.addWidget(self.win)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class SliceDialog(QDialog):
    def __init__(self, W):
        super().__init__()

        reference_level = Dictionaries._AppModel['Model'].value_elems.mean()

        self.setWindowTitle("Visualization voltages")
        self.setMaximumSize(1000, 1000)
        self.setMinimumSize(1000, 1000)

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        pixmap = build_tri(W, reference_level=reference_level, width=10, hight=10)

        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setPixmap(pixmap)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class SlicesDialog(QDialog):
    def __init__(self):
        super().__init__()

        scene = dict(camera=dict(eye=dict(x=2, y=2, z=2)),
                     xaxis=dict(),
                     yaxis=dict(),
                     zaxis=dict(),
                     aspectmode='data',
                     aspectratio=dict(x=1, y=1, z=1.95)
                     )

        s = Dictionaries._AppModel['Model']
        value_x = Dictionaries._AppModel['value_x']
        value_y = Dictionaries._AppModel['value_y']
        value_z = Dictionaries._AppModel['value_z']
        value = [value_x, value_y, value_z]
        colormap = np.load('cm/cm_seismic_plotly.npy')
        sm = [[float(colormap[x][0]), colormap[x][1]] for x in range(256)]
        [fig_slices, W] = s.display_slice(axis=np.array([0, 1, 2]), value=value, middle_value=s.value_elems.mean(),
                                          colormap=sm)

        fig_slices.update_layout(scene=scene)
        Dictionaries._AppModel['fig_slices'] = fig_slices
        fig_slices.update(layout_coloraxis_showscale=False)


        self.layout = QVBoxLayout()

        self.webview = QWebEngineView(self)
        self.webview.setHtml(fig_slices.to_html(include_plotlyjs='cdn'))


        self.setWindowTitle("Slices visualization")
        self.setMaximumSize(1000, 1000)
        self.setMinimumSize(1000, 1000)

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)



        self.layout.addWidget(self.webview)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class ProgessDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.Layout = QVBoxLayout()
        self.ProgressBar = QProgressBar()
        self.Layout.addWidget(self.ProgressBar)

        self.ProgressBar.setMaximum(100)
        self.ProgressBar.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}"
                                       "QProgressBar::chunk {background:gray}")
        self.ProgressBar.setValue(1)

        def setProgressVal(val):
            self.ProgressBar.setValue(val)








# -----------------------------------------
# main TUI Window
# -----------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.clientname = "EITDevice"
        self.host = "10.10.2.84"
        self.port = 32048
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.s = QTcpSocket()

        # # make app full-screen
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
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
        title = "Touch User Interface EIT"

        # apply text
        self.setWindowTitle(title)

        # toggle menu
        widgets.toggleButton.clicked.connect(
            lambda: TUIFunctions.toggleMenu(self, True))

        # setup tui definitions
        # TUIFunctions.tuiDefinitions(self)
        self.TUIFunctions = TUIFunctions
        self.TUIFunctions.tuiDefinitions(self)

        # left menu buttons
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)

        widgets.btn_settings.clicked.connect(self.buttonClick)

        widgets.widgets.btn_send_params.clicked.connect(self.send_param_do_recon)
        widgets.widgets.btn_STOP.clicked.connect(self.STOP_device)

        widgets.new_page.meas_page.Set_of_colorMap.currentIndexChanged.connect(self.change_colorMap)

        widgets.new_page.reconstruction_page.btn_Model.clicked.connect(self.buttonModelClick)
        widgets.new_page.reconstruction_page.btn_voltages_EIT.clicked.connect(self.buttonVoltagesClick)
        widgets.new_page.reconstruction_page.btn_reconstruction.clicked.connect(self.buttonReconstructionClick)
        widgets.new_page.reconstruction_page.btn_reconstruction_device.clicked.connect(self.buttonReconstructionDeviceClick)
        widgets.new_page.reconstruction_page.sliderHorizontal.valueChanged.connect(self.tui.rotation_zy)
        widgets.new_page.reconstruction_page.sliderVertical.valueChanged.connect(self.tui.rotation_zy)
        # widgets.new_page.reconstruction_page.inputGraph.webview.selectionChanged.connect(self.mousePressEvent)
        widgets.new_page.grid_page.x_slider.valueChanged.connect(self.tui.change_slicer_x)
        widgets.new_page.grid_page.y_slider.valueChanged.connect(self.tui.change_slicer_y)
        widgets.new_page.grid_page.z_slider.valueChanged.connect(self.tui.change_slicer_z)

        widgets.new_page.grid_page.axis_voltages.mousePressEvent = self.axisV_mausePressEvent
        widgets.new_page.grid_page.axis_slice_x.mousePressEvent = self.axis_sliceX_mausePressEvent
        widgets.new_page.grid_page.axis_slice_y.mousePressEvent = self.axis_sliceY_mausePressEvent
        widgets.new_page.grid_page.axis_slice_z.mousePressEvent = self.axis_sliceZ_mausePressEvent
        widgets.new_page.grid_page.axis_slices.mousePressEvent = self.axis_slices_maousePressEvent


        widgets.new_page.grid_page.btn_saveVis.clicked.connect(self.saveVis)

        # language option buttons
        widgets.setting_page.btnLangEnglish.clicked.connect(self.languageButtonClick)
        widgets.setting_page.btnLangPolish.clicked.connect(self.languageButtonClick)


        # functions of stack buttons for sub-frames
        self.TUIFunctions.stackPage(self)

        # open and close More Settings Tab
        def openCloseMoreSettingsTab():
            TUIFunctions.toggleRightTab(self, True)

        widgets.moreSettingsBtn.clicked.connect(openCloseMoreSettingsTab)
        # self.tui.new_page.meas_page.mouseMoveEvent = TUIFunctions.MeasPage_mouseMove

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
        widgets.widgets.LineEdit_interval_frame.focused.connect(openKeyboardTab)
        widgets.widgets.LineEdit_int_frame.focused.connect(openKeyboardTab)
        widgets.widgets.LineEdit_interval_frame.noneFocused.connect(closeKeyboardTab)
        widgets.widgets.LineEdit_int_frame.noneFocused.connect(closeKeyboardTab)

        # # nxQDateEdit trigger
        # widgets.nxQDateEdit.focused.connect(openKeyboardTab)
        # widgets.nxQDateEdit.noneFocused.connect(closeKeyboardTab)
        # # nxQDateTimeEdit trigger
        # widgets.nxQDateTimeEdit.focused.connect(openKeyboardTab)
        # widgets.nxQDateTimeEdit.noneFocused.connect(closeKeyboardTab)
        # # nxQDoubleSpinBox trigger
        # widgets.nxQDoubleSpinBox.focused.connect(openKeyboardTab)
        # widgets.nxQDoubleSpinBox.noneFocused.connect(closeKeyboardTab)
        # # nxQDateTimeEdit trigger
        # widgets.nxQTimeEdit.focused.connect(openKeyboardTab)
        # widgets.nxQTimeEdit.noneFocused.connect(closeKeyboardTab)
        # # widgets.new_page.inputGraph.focused.connect(closeKeyboardTab)
        # # widgets.new_page.inputGraph.noneFocused.connect(closeKeyboardTab)
        # # widgets.keyboardwidget.
        #
        # # self.tui.btn_restartApp.clicked.connect(self.restart)

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


    def connection(self):
        # MY_SERVER = (self.host, self.port)
        # with tcp_connection_to(MY_SERVER) as conn:
        #     conn.send(Dictionaries._AppVars['message'].encode())
        try:
            # self.s.launch(self.host, self.port)
            self.s.connect((self.host, self.port))
            self.tui.widgets.btn_STOP.setEnabled(True)
            QMessageBox.warning(self, "Connection", "Connection made")
        except:
            print("Failed to connect with {}:{}" .format(self.host, self.port))
        Dictionaries._AppVars['Device active'] = 1


    def receivemessage_live(self, progress_callback):
        n_frame = self.tui.widgets.LineEdit_int_frame.value()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        while Dictionaries._AppVars['recon_dane'] == False:

            try:
                self.s.connect((self.host, self.port))
                self.tui.widgets.btn_STOP.setEnabled(True)
                # QMessageBox.warning(self, "Connection", "Connection made")
                Dictionaries._AppVars['Device active'] = 1
                total_frame = ''
                t = 2  # dla samej ramiki danych jest 1 dla początkowych wartości jest 0
                # message = Dictionaries._AppVars['message']
                # wyślij ustawienia urządzenia
                # print('Wysyłam')
                # print(message.encode())
                # self.s.sendall(message.encode())
                # urządznie odsyła że zostało poprawnie skonfigurowane
                # print('odbieram')
                # data = self.s.recv(1024)

                # data = data.data()
                # print(data.decode())
                # self.tui.update_message_box(new_message=data.decode())
                while Dictionaries._AppVars['recon_dane'] == False:
                # while Dictionaries._AppVars['recon_dane'] == False:
                #     if t <= 1:
                #         print('Wysyłam')
                #         message = Dictionaries._AppVars['message']
                #         if t == 0:
                #             # M = Dictionaries._AppNotifications['Send param device'][Dictionaries._AppVars['Language']]
                #             # progress_callback.emit(M)
                #             # self.tui.update_message_box(new_message=M)
                #             print('wysyłam ustawienia urządzenia')
                #             meas_Dicit = json.loads(message.encode())
                #             Keys = meas_Dicit['payload'].keys()
                #
                #             for k in Keys:
                #                 new_message = {
                #                     'sequence': {},
                #                     'payload': {
                #                         k: meas_Dicit['payload'][k]
                #                     }
                #                 }
                #                 jm = json.dumps(new_message) + '\r\n'
                #                 nr_prub = 0
                #                 while nr_prub <= 3:
                #                     self.s.sendall(jm.encode())
                #                     data_recev = self.s.recv(1024)
                #                     recev_Dicit = json.loads(data_recev.decode('utf-8'))
                #                     nr_prub = 0
                #                     if recev_Dicit['payload'][k] == meas_Dicit['payload'][k]:
                #                         print(k + ' zaktualizowano')
                #                         nr_prub = 10
                #                     else:
                #                         nr_prub += 1
                #                         if nr_prub > 3:
                #                             print('dla ' + k + ' wykonano 3 pruby ustawienia urzadenia')
                #             print('ustawiono parametry urządzenia')
                #             # self.tui.update_message_box(new_message='wysyłam ustawienia urządzenia')
                #         else:
                #             self.sendmessage_newFrame()
                #             # print('Pobieram ustawienia ramki')
                #             message = Dictionaries._AppVars['message']
                #             # print('wysyłam ustawienia ramki')
                #             # M = Dictionaries._AppNotifications['Send param frames'][Dictionaries._AppVars['Language']]
                #             # self.tui.update_message_box(new_message=M)
                #             # progress_callback.emit(M)
                #
                #             meas_Dicit = json.loads(message.encode())
                #             Keys = meas_Dicit['payload'].keys()
                #
                #             for k in Keys:
                #                 new_message = {
                #                     'sequence': {},
                #                     'payload': {
                #                         k: meas_Dicit['payload'][k]
                #                     }
                #                 }
                #                 jm = json.dumps(new_message) + '\r\n'
                #                 nr_prub = 0
                #                 while nr_prub <= 3:
                #                     self.s.sendall(jm.encode())
                #                     data_recev = self.s.recv(1024)
                #                     recev_Dicit = json.loads(data_recev.decode('utf-8'))
                #                     nr_prub = 0
                #                     if recev_Dicit['payload'][k] == meas_Dicit['payload'][k]:
                #                         print(k + ' zaktualizowano')
                #                         nr_prub = 10
                #                     else:
                #                         nr_prub += 1
                #                         if nr_prub > 3:
                #                             print('dla ' + k + ' wykonano 3 pruby ustawienia urzadenia')
                #             print('ustawiono parametry ramki')
                #
                #             # self.s.sendall(message.encode())
                #
                #     # time.sleep(2)
                #     # print('Odbieram')
                #
                #     # self.tui.update_message_box(new_message='pobieram ramkę danych')
                #     # time.sleep(2)
                #
                #     # if t == 0:
                #     #     data = self.s.recv(1024)
                #     #     print(data.decode())
                #     #     # self.tui.update_message_box(new_message=data.decode())
                #     #
                #     else:
                #         # print('Odbieram ramkę danych')
                #
                #         # while True:

                    # if t == 1:
                    #     message = {"sequence": {},
                    #                "payload":
                    #                    {"start": "1"}}
                    #     jm = json.dumps(message)
                    #     self.s.sendall(jm.encode())
                    # else:
                    data = self.s.recv(2067)

                    total_str = data

                    self.Voltages_from_json(total_str)
                    self.buttonReconstructionClick()

                    time.sleep(7)

                    # Dictionaries._AppVars['message'] = jm
                    if n_frame != 1 and t == n_frame:
                        Dictionaries._AppVars['recon_dane'] = False
                        self.STOP_device()
                        message = Dictionaries._AppVars['message']
                        self.s.sendall(message.encode())
                        self.s.close()
                        M = Dictionaries._AppNotifications['Recon n done'][Dictionaries._AppVars['Language']]
                        progress_callback.emit(M)
                        # self.tui.update_message_box(new_message=M)
                        break

                    t += 1


            except:
                print("Failed to connect with {}:{}".format(self.host, self.port))


    def receivemessage(self, progress_callback=None):
        n_frame = self.tui.widgets.LineEdit_int_frame.value()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        while Dictionaries._AppVars['recon_dane'] == False:

            try:
                self.s.connect((self.host, self.port))
                self.tui.widgets.btn_STOP.setEnabled(True)
                # QMessageBox.warning(self, "Connection", "Connection made")
                Dictionaries._AppVars['Device active'] = 1
                total_frame = ''
                t = 1  # dla samej ramiki danych jest 1 dla początkowych wartości jest 0


                while Dictionaries._AppVars['recon_dane'] == False:

                    # message = Dictionaries._AppVars['message']
                    # if t == 0:
                    #     # M = Dictionaries._AppNotifications['Send param device'][Dictionaries._AppVars['Language']]
                    #     # progress_callback.emit(M)
                    #     print('wysyłam ustawienia urządzenia')
                    #     # self.tui.update_message_box(new_message=M)
                    #     meas_Dicit = json.loads(message.encode())
                    #     Keys = meas_Dicit['payload'].keys()
                    #
                    #     for k in Keys:
                    #         new_message = {
                    #             'sequence': {},
                    #             'payload': {
                    #                 k: meas_Dicit['payload'][k]
                    #             }
                    #         }
                    #         jm = json.dumps(new_message) + '\r\n'
                    #         nr_prub = 0
                    #         while nr_prub <= 3:
                    #             self.s.sendall(jm.encode())
                    #             data_recev = self.s.recv(1024)
                    #             recev_Dicit = json.loads(data_recev.decode('utf-8'))
                    #             nr_prub = 0
                    #             if recev_Dicit['payload'][k] == meas_Dicit['payload'][k]:
                    #                 print(k +' zaktualizowano')
                    #                 nr_prub = 10
                    #             else:
                    #                 nr_prub += 1
                    #                 if nr_prub > 3:
                    #                     print('dla ' + k + ' wykonano 3 pruby ustawienia urzadenia')
                    #     print('ustawiono parametry urządzenia')
                    # elif t == 1:
                    #     self.sendmessage_newFrame()
                    #     # print('Pobieram ustawienia ramki')
                    #     message = Dictionaries._AppVars['message']
                    #     print('wysyłam ustawienia ramki')
                    #     # M = Dictionaries._AppNotifications['Send param frames'][Dictionaries._AppVars['Language']]
                    #     # progress_callback.emit(M)
                    #     # self.tui.update_message_box(new_message=M)
                    #
                    #     # self.s.sendall(message.encode())
                    #     meas_Dicit = json.loads(message.encode())
                    #     Keys = meas_Dicit['payload'].keys()
                    #
                    #     for k in Keys:
                    #         new_message = {
                    #             'sequence': {},
                    #             'payload': {
                    #                 k: meas_Dicit['payload'][k]
                    #             }
                    #         }
                    #         jm = json.dumps(new_message) + '\r\n'
                    #         nr_prub = 0
                    #         while nr_prub <= 3:
                    #             self.s.sendall(jm.encode())
                    #             data_recev = self.s.recv(1024)
                    #             recev_Dicit = json.loads(data_recev.decode('utf-8'))
                    #             nr_prub = 0
                    #             if recev_Dicit['payload'][k] == meas_Dicit['payload'][k]:
                    #                 print(k +' zaktualizowano')
                    #                 nr_prub = 10
                    #             else:
                    #                 nr_prub += 1
                    #                 if nr_prub > 3:
                    #                     print('dla ' + k + ' wykonano 3 pruby ustawienia urzadenia')
                    #     print('ustawiono parametry ramki')
                    #
                    # # time.sleep(2)
                    # # print('Odbieram')
                    #
                    # # self.tui.update_message_box(new_message='pobieram ramkę danych')
                    # # time.sleep(2)
                    # # total_str = ''
                    # # if t == 0:
                    # #     data = self.s.recv(1024)
                    # #     print(data.decode())
                    # #     # sparawdz czy pokrywają się jsony
                    # #     if np.all(message == data.decode()):
                    # #         print('poprawnie wysłano ustawienia')
                    # #     else:
                    # #         print('coś poszło nie tak')
                    # #
                    # #     # self.tui.update_message_box(new_message=data.decode())
                    # #
                    # # else:
                    # #     # print('Odbieram ramkę danych')
                    # #
                    # #     # while True:
                    # else:
                        # odbieramy komunikaty ile zostało już zapisanych ramek danych


                    data = self.s.recv(2067)
                    # endData = data.decode('utf-8')[-5:-1]
                    # if endData == 'FEFF':
                    #     total_str += data.decode('utf-8')
                    #     break
                    total_str = data
                    # print('cała ramka pobrana')
                    # M = Dictionaries._AppNotifications['Recive frame'][Dictionaries._AppVars['Language']]
                    # self.tui.update_message_box(new_message=M)
                    # progress_callback.emit(M)
                    # M = Dictionaries._AppNotifications['Recon'][Dictionaries._AppVars['Language']]
                    # self.tui.update_message_box(new_message=M)
                    # progress_callback.emit(M)
                    self.Voltages_from_json(total_str)
                    self.buttonReconstructionClick()

                    time.sleep(10)
                    # n_frame = t - 2
                    if t == n_frame:
                        Dictionaries._AppVars['recon_dane'] = False
                        self.STOP_device()
                        message = Dictionaries._AppVars['message']
                        self.s.sendall(message.encode())
                        self.s.close()
                        M = Dictionaries._AppNotifications['Recon n done'][Dictionaries._AppVars['Language']]
                        progress_callback.emit(M)
                        # self.tui.update_message_box(new_message=M)
                        break

                        # Dictionaries._AppVars['message'] = jm
                    t += 1


            except:
                M = Dictionaries._AppNotifications['Connection field'][Dictionaries._AppVars['Language']]
                progress_callback.emit(M)
                # self.tui.update_message_box(new_message=M)
                # print("Failed to connect with {}:{}".format(self.host, self.port))


    def sendmessage_newFrame(self):
        # self.tui.update_message_box(new_message='pobieranie ramki danych')
        serie = self.tui.widgets.LineEdit_int_frame.value()
        ch_live = self.tui.widgets.Live_check_box.isChecked()
        live = '1' if ch_live else '0'

        message = {
            "sequence": {},
            "payload": {
                "live": live,
                "count": str(serie),
                "start": "1",
            }
        }
        jm = json.dumps(message)
        Dictionaries._AppVars['message'] = jm + '\r\n'
        # with open
        # self.s.sendall(jm.encode())

        # with tcp_connection_to((self.host, self.port)) as conn:
        #     conn.sendall(jm.encode())



    def STOP_device(self):
        message = {
            "sequence": {},
            "payload": {
                "start": "0"
            }
        }
        jm = json.dumps(message)
        # self.s.sendall(jm.encode('utf-8'))
        Dictionaries._AppVars['message'] = jm
        Dictionaries._AppVars['recon_dane'] = 'True'
        # self.s.close()
        self.tui.widgets.btn_STOP.setEnabled(False)


    def SPDR_progress(self, new_message):

        # self.tui.disable_enable_language_buttons_for_multithreading(make_active=False)
        #
        # self.tui.message_box.clear()
        # self.tui.infoBar.setStyleSheet("background:rgb(230,100,7)")
        # self.tui.message_box.moveCursor(QTextCursor.Start)
        # self.tui.message_box.insertPlainText(str(datetime.now().strftime('%H:%M:%S'))
        #                                      + " - Info: "
        #                                      + new_message)
        # self.tui.clear_infoBar()
        # self.tui.update_message_box(new_message=s)
        print(new_message)


    def SPDR_complete(self, s=None):
        if s == None:
            s = "Done"
        self.tui.update_message_box(new_message=s)


    def send_param_do_recon(self):

        worker = Worker(self.send_param)
        worker.signals.progress.connect(self.tui.update_message_box)
        worker.signals.finished.connect(self.SPDR_complete)
        self.threadpool.start(worker)

        # self.send_param()
        # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #
        # while Dictionaries._AppVars['recon_dane'] == False:
        #
        #     try:
        #         self.s.connect((self.host, self.port))
        #         self.tui.widgets.btn_STOP.setEnabled(True)
        #         # QMessageBox.warning(self, "Connection", "Connection made")
        #         Dictionaries._AppVars['Device active'] = 1
        #         total_frame = ''
        #         t = 0  # dla samej ramiki danych jest 1 dla początkowych wartości jest 0
        #         # message = Dictionaries._AppVars['message']
        #         # wyślij ustawienia urządzenia
        #         # print('Wysyłam')
        #         # print(message.encode())
        #         # self.s.sendall(message.encode())
        #         # urządznie odsyła że zostało poprawnie skonfigurowane
        #         # print('odbieram')
        #         # data = self.s.recv(1024)
        #
        #         # data = data.data()
        #         # print(data.decode())
        #         # self.tui.update_message_box(new_message=data.decode())
        #         while Dictionaries._AppVars['recon_dane'] == False:
        #
        #             message = Dictionaries._AppVars['message']
        #             if t == 0:
        #                 # M = Dictionaries._AppNotifications['Send param device'][Dictionaries._AppVars['Language']]
        #                 # progress_callback.emit(M)
        #                 print('wysyłam ustawienia urządzenia')
        #                 # self.tui.update_message_box(new_message=M)
        #                 meas_Dicit = json.loads(message.encode())
        #                 Keys = meas_Dicit['payload'].keys()
        #
        #                 for k in Keys:
        #                     new_message = {
        #                         'sequence': {},
        #                         'payload': {
        #                             k: meas_Dicit['payload'][k]
        #                         }
        #                     }
        #                     jm = json.dumps(new_message) + '\r\n'
        #                     nr_prub = 0
        #                     while nr_prub <= 3:
        #                         self.s.sendall(jm.encode())
        #                         data_recev = self.s.recv(1024)
        #                         recev_Dicit = json.loads(data_recev.decode('utf-8'))
        #                         nr_prub = 0
        #                         if recev_Dicit['payload'][k] == meas_Dicit['payload'][k]:
        #                             print(k +' zaktualizowano')
        #                             nr_prub = 10
        #                         else:
        #                             nr_prub += 1
        #                             if nr_prub > 3:
        #                                 print('dla ' + k + ' wykonano 3 pruby ustawienia urzadenia')
        #                 print('ustawiono parametry urządzenia')
        #             else:
        #                 self.sendmessage_newFrame()
        #                 # print('Pobieram ustawienia ramki')
        #                 message = Dictionaries._AppVars['message']
        #                 print('wysyłam ustawienia ramki')
        #                 # M = Dictionaries._AppNotifications['Send param frames'][Dictionaries._AppVars['Language']]
        #                 # progress_callback.emit(M)
        #                 # self.tui.update_message_box(new_message=M)
        #
        #                 # self.s.sendall(message.encode())
        #                 meas_Dicit = json.loads(message.encode())
        #                 Keys = meas_Dicit['payload'].keys()
        #
        #                 for k in Keys:
        #                     new_message = {
        #                         'sequence': {},
        #                         'payload': {
        #                             k: meas_Dicit['payload'][k]
        #                         }
        #                     }
        #                     jm = json.dumps(new_message) + '\r\n'
        #                     nr_prub = 0
        #                     while nr_prub <= 3:
        #                         self.s.sendall(jm.encode())
        #                         data_recev = self.s.recv(1024)
        #                         recev_Dicit = json.loads(data_recev.decode('utf-8'))
        #                         nr_prub = 0
        #                         if recev_Dicit['payload'][k] == meas_Dicit['payload'][k]:
        #                             print(k +' zaktualizowano')
        #                             nr_prub = 10
        #                         else:
        #                             nr_prub += 1
        #                             if nr_prub > 3:
        #                                 print('dla ' + k + ' wykonano 3 pruby ustawienia urzadenia')
        #                 print('ustawiono parametry ramki')
        #     except:
        #         M = Dictionaries._AppNotifications['Connection field'][Dictionaries._AppVars['Language']]
        #         self.tui.update_message_box(new_message=M)
                # progress_callback.emit(M)

        # self.connection()


        # worker_process.start()

        # Oczekiwanie na zakończenie workera
        # worker_process.join()
        # worker = Worker(self.send_param)
        # # worker = Worker(self.tui.solve_inverse_problem_device)
        # worker.signals.progress.connect(self.SPDR_progress)
        # # worker.signals.result.connect(self.SPDR_results)
        # worker.signals.finished.connect(self.SPDR_complete)
        # self.threadpool.start(worker)


    def buttonReconstructionDeviceClick(self):
        # while Dictionaries._AppVars['recon_dane'] == False:
        # self.receivemessage()
        # t = Thread(target=self.receivemessage)
        # t.daemon = True
        # t.start()
        serie = self.tui.widgets.LineEdit_int_frame.value()
        live = '1' if (self.tui.widgets.Live_check_box.isChecked()) else '0'
        Dictionaries._AppVars['recon_dane'] = False
        Dictionaries._AppVars['start_recon'] = True
        # if live == '0':
        #     worker_waitting_for_all_frames = Worker(self.collecting_frames)
        #     worker_waitting_for_all_frames.signals.progress.connect(self.progress_collecting)
        #     worker_waitting_for_all_frames.signals.finished.connect(self.finished_collecting)
        #     self.threadpool.start(worker_waitting_for_all_frames)
        #     worker = Worker(self.receivemessage)
        #     worker.signals.progress.connect(self.tui.update_message_box)
        #     worker.signals.finished.connect(self.SPDR_complete)
        #     self.threadpool.start(worker)
        # else:
        #     worker = Worker(self.receivemessage_live)
        #     worker.signals.progress.connect(self.tui.update_message_box)
        #     worker.signals.finished.connect(self.SPDR_complete)
        #     self.threadpool.start(worker)



    def send_param(self, progress_callback=None):
        # region wczytanie ustawień wybranych przez urzytkownika na aplikacji
        type = self.tui.widgets.ComboBox_tryb.currentText()
        mode = 0 if type == 'EIT' else 1 if type == 'ECT' else 2
        sequence = self.tui.widgets.ComboBox_stim_pattern.currentText()
        excitation = 0 if sequence == '32(0-4)' else 1 if sequence == '32(0-8)' else 2 if sequence == '32(0-16)' else 3
        frequency = self.tui.widgets.ComboBox_frequency.currentText()[:-3]
        interval_frame = self.tui.widgets.LineEdit_interval_frame.value()
        amp = self.tui.widgets.Slider_amp.slider.value()
        serie = self.tui.widgets.LineEdit_int_frame.value()
        n_frame = serie
        # live = 'True' if (serie >= 1) else 'false'


        dictionary = {
            "sequence": {},
            "payload": {
                "mode": str(mode),
                "excitation": str(excitation),
                "frequency": frequency,
                "current": str(amp),
                # "int_interval": str(interval_frame),
                # "measurement_count": str(serie),
            }
        }
        finite_element_mesh = self.tui.new_page.reconstruction_page.Label_load_model.text()
        mesh = load_mesh_from_mat_file_v2(finite_element_mesh)

        if sequence != '32(3D)':

            stim_structure = {
                'n_electrodes': len(mesh['electrodes_nodes']),
                'd_stim': int(sequence[-2]),
                'd_meas': 1,
                'z_contact': mesh['z_contact'],
                'amp': amp,
            }
        else:
            stim_structure = {
                'n_electrodes': len(mesh['electrodes_nodes']),
                'd_stim': 8,
                'd_meas': 8,
                'z_contact': mesh['z_contact'],
                'amp': amp,
            }
        # ustawienie danych modelu
        stimulation = stim_pattern3D(stim_structure)
        Dictionaries._AppModel['stim_pattern'] = stimulation
        eit_3D = Image_EIT_3D_tetra(mesh, stimulation=stimulation, shape_ele='surface')
        eit_3D.set_up()
        Dictionaries._AppModel['Model'] = eit_3D

        message = json.dumps(dictionary)
        Dictionaries._AppVars['message'] = message
        TUIFunctions.tofNewPage_StackPages(self, "reconstruction_page")
        # endregion
        # self.tui.new_page.btn_recontruction_frame.clicked()
        # region łaczymy się z serwerem
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # endregion
        t = 0
        # region wysyłanie parametrów urządzenia i ustawień ramki
        while t < 1:

            try:
                self.s.connect((self.host, self.port))
                self.tui.widgets.btn_STOP.setEnabled(True)
                # QMessageBox.warning(self, "Connection", "Connection made")
                Dictionaries._AppVars['Device active'] = 1


                message = Dictionaries._AppVars['message']
                for t in range(2):
                    if t == 0:

                        progress_callback.emit('wysyłam ustawienia urządzenia')
                        # self.tui.update_message_box(new_message=M)
                        meas_Dicit = json.loads(message.encode())
                        Keys = meas_Dicit['payload'].keys()

                        for k in Keys:
                            new_message = {
                                'sequence': {},
                                'payload': {
                                    k: meas_Dicit['payload'][k]
                                }
                            }
                            jm = json.dumps(new_message) + '\r\n'
                            nr_prub = 0
                            while nr_prub <= 3:
                                self.s.sendall(jm.encode())
                                data_recev = self.s.recv(1024)
                                recev_Dicit = json.loads(data_recev.decode('utf-8'))
                                nr_prub = 0
                                if recev_Dicit['payload'][k] == meas_Dicit['payload'][k]:
                                    # print(k + ' zaktualizowano')
                                    nr_prub = 10
                                else:
                                    nr_prub += 1
                                    if nr_prub > 3:
                                        print('dla ' + k + ' wykonano 3 pruby ustawienia urzadenia')
                        progress_callback.emit('ustawiono parametry urządzenia')

                    else:
                        self.sendmessage_newFrame()
                        # print('Pobieram ustawienia ramki')
                        message = Dictionaries._AppVars['message']
                        progress_callback.emit('wysyłam ustawienia ramki')
                        # M = Dictionaries._AppNotifications['Send param frames'][Dictionaries._AppVars['Language']]
                        # progress_callback.emit(M)
                        # self.tui.update_message_box(new_message=M)

                        # self.s.sendall(message.encode())
                        meas_Dicit = json.loads(message.encode())
                        Keys = meas_Dicit['payload'].keys()

                        for k in Keys:
                            new_message = {
                                'sequence': {},
                                'payload': {
                                    k: meas_Dicit['payload'][k]
                                }
                            }
                            jm = json.dumps(new_message) + '\r\n'
                            nr_prub = 0
                            while nr_prub <= 3:
                                self.s.sendall(jm.encode())
                                if k != 'start':
                                    data_recev = self.s.recv(1024)
                                    recev_Dicit = json.loads(data_recev.decode('utf-8'))
                                    nr_prub = 0
                                    if recev_Dicit['payload'][k] == meas_Dicit['payload'][k]:
                                        # print(k + ' zaktualizowano')
                                        nr_prub = 10
                                    else:
                                        nr_prub += 1
                                        if nr_prub > 3:
                                            progress_callback.emit('dla ' + k + ' wykonano 3 pruby ustawienia urzadenia')
                                else:
                                    nr_prub = 10
                        progress_callback.emit('ustawiono parametry ramki')

            except:
                M = Dictionaries._AppNotifications['Connection field'][Dictionaries._AppVars['Language']]
                self.tui.update_message_box(new_message=M)
        # endregion
        # Przystepujemy do rekonstrukcji
        while Dictionaries._AppVars['recon_dane'] == False:

            if Dictionaries._AppVars['start_recon']:
                ch_live = self.tui.widgets.Live_check_box.isChecked()
                # region Czy mamy doczynienia z zgromadzeniem ramek na urządzeniu
                if not ch_live:
                    collecting = True

                    # self.s.connect((self.host, self.port))
                    # self.tui.widgets.btn_STOP.setEnabled(True)
                    # komunikat rozpoczęcia zbieranie ramki danych
                    msg = {
                        "sequence": {},
                        "payload": {
                            'start': '1'}}
                    jm_msg = json.dumps(msg)
                    # self.s.sendall(jm_msg.encode())
                    # czekamy aż wyślą nam komunikat
                    msg_return = {
                        "sequence": {},
                        "payload": {
                            'start': '0'}
                    }
                    ProgessWindow = ProgessDialog()
                    ProgessWindow.exec_()

                    while collecting:

                        data = self.s.recv(1024)
                        recev_Dicit = json.loads(data.decode('utf-8'))
                        try:
                            if recev_Dicit['payload']['start'] == '0':
                                collecting = False
                                ProgessWindow.ProgressBar.setValue(100)
                                print('zebrano całą serię')
                        except:
                            new_value = recev_Dicit['payload']['measurementsCollected']
                            ProgessWindow.ProgressBar.setValue(int(new_value / serie * 100))
                # endregion

                Dictionaries._AppVars['Device active'] = 1
                total_frame = b''
                t = 2  # dla samej ramiki danych jest 1 dla początkowych wartości jest 0
                # message = Dictionaries._AppVars['message']
                # wyślij ustawienia urządzenia
                # print('Wysyłam')
                # print(message.encode())
                # self.s.sendall(message.encode())
                # urządznie odsyła że zostało poprawnie skonfigurowane
                # print('odbieram')
                # data = self.s.recv(1024)

                # data = data.data()
                # print(data.decode())
                # self.tui.update_message_box(new_message=data.decode())
                # region rekonstruujemy ramka po ramce
                while Dictionaries._AppVars['recon_dane'] == False:
                    data = self.s.recv(2067)

                    total_frame += data
                    try:
                        recev_Dicit = json.loads(total_frame.decode('utf-8'))
                        progress_callback.emit(json.dumps(recev_Dicit['payload']))

                    except:
                        try:
                            total_frame = self.Voltages_from_json(total_frame)
                            self.buttonReconstructionClick()

                            time.sleep(7)
                        except:
                            zero = 0

                    # Dictionaries._AppVars['message'] = jm
                    if n_frame != 1 and t == n_frame:
                        Dictionaries._AppVars['recon_dane'] = False
                        self.STOP_device()
                        message = Dictionaries._AppVars['message']
                        self.s.sendall(message.encode())
                        self.s.close()
                        M = Dictionaries._AppNotifications['Recon n done'][Dictionaries._AppVars['Language']]
                        progress_callback.emit(M)
                        # self.tui.update_message_box(new_message=M)
                        Dictionaries._AppVars['start_recon'] = False
                        break

                    t += 1
                # endregion

            else:
                progress_callback.emit('przyciśnij przycisk recon na zakłatce poniżej bierzącej')
                time.sleep(5)


    def collecting_frames(self, progress_callback=None):

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serie = self.tui.widgets.LineEdit_int_frame.value()
        collecting = True

        while collecting:

            try:
                self.s.connect((self.host, self.port))
                # self.tui.widgets.btn_STOP.setEnabled(True)
                # komunikat rozpoczęcia zbieranie ramki danych
                msg = {
                    "sequence": {},
                    "payload": {
                        'start': '1'}}
                jm_msg = json.dumps(msg)
                self.s.sendall(jm_msg.encode())
                # czekamy aż wyślą nam komunikat
                msg_return = {
                    "sequence": {},
                    "payload": {
                        'start': '0'}
                }
                ProgessWindow = ProgessDialog()
                ProgessWindow.exec_()


                data = self.s.recv(1024)
                recev_Dicit = json.loads(data.decode('utf-8'))
                try:
                    if recev_Dicit['payload']['start'] == '0':
                        collecting = False
                        ProgessWindow.ProgressBar.setValue(100)
                        print('zebrano całą serię')
                except:
                    new_value = recev_Dicit['payload']['measurementsCollected']
                    ProgessWindow.ProgressBar.setValue(int(new_value/serie*100))


            except:
                print('bład przy zbieraniu ramek danych')


        ProgessWindow = ProgessDialog()
        ProgessWindow.exec_()

    def progress_collecting(self, value):
        print(value)

    def finished_collecting(self):
        print('Done')


    def Voltages_from_json(self, total_frame_str):
        V = total_frame_str
        # czy mamy ciapki
        if V[0] == '"':
            V = V[1:-1]

        # Wyznaczamy zanaki początku i końca ramki
        ind_b = find_FFFE(V)
        ind_e = find_FEFF(V[ind_b+4:])
        if ind_e != None:
            ind_e += ind_b+4
            VV = V[ind_b+2+2+2:ind_e]  # dwa na FFFE dwa na początek 2 na zanak wczytywania
            model = Dictionaries._AppModel['Model']
            N_ele = model.electrodes[0].__len__()
            N_meas = int(N_ele**2)
            voltages = np.zeros(N_meas)
            for x in range(N_meas):
                voltages[x] = int.from_bytes(VV[2*x:2*x+2], byteorder='big')
            voltages_array = voltages.reshape(N_ele, N_ele)
            stim_p = np.row_stack([x.toarray() for x in model.stim['stim_pattern']])
            p_minus = np.argwhere(stim_p < 0)[:, 1]
            p_plus = np.argwhere(stim_p > 0)[:, 1]
            amp = np.ones(N_ele) * stim_p.max()
            Dictionaries._AppModel['raw_data'] = np.block([amp.reshape(-1, 1),
                                                           p_plus.reshape(-1, 1),
                                                           p_minus.reshape(-1, 1),
                                                           voltages_array])
            self.tui.new_page.meas_page.model._data = voltages_array
            self.change_colorMap()
            return V[ind_e:]
        else:
            return total_frame_str


    def buttonClick(self):



        btn = self.sender()  # get button
        btnName = btn.objectName()  # pass button name

        # show home page
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)  # set page
            # reset another buttons
            TUIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(
                TUIFunctions.selectMenu(
                    btn.styleSheet()))  # select menu

        # show widgets page
        if btnName == "btn_widgets":

            self.tui.keyboardwidget.setSource(QUrl.fromLocalFile("src/keyboard.qml"))
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            TUIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))

        # show new page
        if btnName == "btn_new":
            self.tui.keyboardwidget.setSource(QUrl.fromLocalFile("src/empty.qml"))
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)
            TUIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))
        # # show new page
        # if btnName == "btn_grid":
        #     widgets.new_page.newPage_StackedWidget.setCurrentWidget(widgets.new_page.grid_page)
        #     TUIFunctions.resetStyle(self, btnName)
        #     btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))
        # # show new page
        # if btnName == "btn_meas":
        #     widgets.new_page.newPage_StackedWidget.setCurrentWidget(widgets.new_page.meas_page)
        #     TUIFunctions.resetStyle(self, btnName)
        #     btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))

        # show settings
        if btnName == "btn_settings":
            widgets.stackedWidget.setCurrentWidget(widgets.setting_page)
            TUIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))

        # print btn name
        # print(f'Button "{btnName}" pressed!')

    def languageButtonClick(self):

        btn = self.sender()  # get button
        btnName = btn.objectName()  # pass button name

        # change language to english
        if btnName == "btnLangEnglish":
            Dictionaries._AppVars['Language'] = 0
            self.tui.retranslate_tui(self)

        # change language to polish
        if btnName == "btnLangPolish":
            Dictionaries._AppVars['Language'] = 1
            self.tui.retranslate_tui(self)

        # send info to infoBar
        self.tui.update_message_box(
            new_message=Dictionaries._AppNotifications['LanguageChange'][Dictionaries._AppVars['Language']] )

    def change_colorMap(self):
        cmap_str = self.tui.new_page.meas_page.Set_of_colorMap.currentText()
        A = np.array(self.tui.new_page.meas_page.model._data)
        color_palette = build_color_palette(A, cmap_str)
        delegate = ColorDelegate(color_palette)
        self.tui.new_page.meas_page.table.setItemDelegate(delegate)
        self.tui.new_page.meas_page.table.show()

    def axisV_mausePressEvent(self, s):
        # print("click", s)
        dlg = VoltagesDialog()

        dlg.exec_()
        # dlg.win.addLegend()


    def axis_sliceX_mausePressEvent(self, s):
        Wx = Dictionaries._AppModel['Wx']
        dlg = SliceDialog(Wx)
        dlg.exec_()
        pass

    def axis_sliceY_mausePressEvent(self, s):
        W = Dictionaries._AppModel['Wy']
        dlg = SliceDialog(W)
        dlg.exec_()
        pass

    def axis_sliceZ_mausePressEvent(self, s):
        Wx = Dictionaries._AppModel['Wz']
        dlg = SliceDialog(Wx)
        dlg.exec_()
        pass


    def axis_slices_maousePressEvent(self, s):
        dlg = SlicesDialog()
        dlg.exec_()
        pass


    def saveVis(self):
        if not os.path.exists('Reconstructions'):
            os.makedirs('Reconstructions')
        TimeLabel = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
        path = 'Reconstructions\\Recon_' + TimeLabel
        if not os.path.exists(path):
            os.makedirs(path)
        dlg = VoltagesDialog()
        pixmap = dlg.win.grab()
        image = pixmap.toImage()
        image.save(path + '\\' + 'Voltages.png')

        W = Dictionaries._AppModel['Wx']
        dlg = SliceDialog(W)
        pixmap = dlg.label.grab()
        imageX = pixmap.toImage()

        W = Dictionaries._AppModel['Wy']
        dlg = SliceDialog(W)
        pixmap = dlg.label.grab()
        imageY = pixmap.toImage()

        W = Dictionaries._AppModel['Wz']
        dlg = SliceDialog(W)
        pixmap = dlg.label.grab()
        imageZ = pixmap.toImage()

        imageX.save(path + '\\' + 'sliceX.png')
        imageY.save(path + '\\' + 'sliceY.png')
        imageZ.save(path + '\\' + 'sliceZ.png')

        dlg = SlicesDialog()
        fig_slices = Dictionaries._AppModel['fig_slices']
        fig_slices.write_image(path + '\\' + 'slices.png', width=800, height=800)

        dlg.close()

        str_message = Dictionaries._AppNotifications['Save Visualization'][Dictionaries._AppVars['Language']] + path

        self.tui.update_message_box(new_message=str_message)




    def reconstruction_results(self, s):
        print('wyswietlanie')
        colormap = np.load('cm/cm_seismic_plotly.npy')
        sm = [[float(colormap[x][0]), colormap[x][1]] for x in range(256)]
        fig = s.display(middle_value=s.value_elems.mean(), colormap=sm)

        Dictionaries._AppModel['Model'] = s
        # self.tui.EIT_3D = s


        self.tui.new_page.reconstruction_page.inputGraph.webview.setHtml(fig.to_html(include_plotlyjs='cdn'))
        fig.write_html("recon_html/figure.html")
        self.tui.change_axis_slices()
        self.tui.change_slicer_x(axis3D=False)
        self.tui.change_slicer_y(axis3D=False)
        self.tui.change_slicer_z(axis3D=False)
        self.tui.new_page.grid_page.btn_saveVis.setEnabled(True)


        if not os.path.exists('data'):
            os.makedirs('data')

        TimeLabel = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
        fig.write_html('data\\reconstruction_' + TimeLabel + '.html')


    def reconstruction_progress(self, s):
        self.tui.new_page.reconstruction_page.Info_box.moveCursor(QTextCursor.Start)
        self.tui.new_page.reconstruction_page.Info_box.insertPlainText(str(s) + '\n')
        self.tui.new_page.reconstruction_page.Info_box.moveCursor(QTextCursor.Start)


    def buttonReconstructionClick(self):
        Dictionaries._AppVars['start_recon'] = True

        if Dictionaries._AppVars['Device active'] == 0:
            worker = Worker(self.tui.solve_inverse_problem)
        else:
            worker = Worker(self.tui.solve_inverse_problem_device)
        worker.signals.progress.connect(self.reconstruction_progress)
        worker.signals.result.connect(self.reconstruction_results)
        worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(worker)


    def thread_complete(self):
        self.tui.update_message_box(new_message='Dane')
        # Dictionaries._AppVars['recon_dane'] = True

    def buttonModelClick(self):
        # btn = self.sender()
        # btnName = btn.objectName()
        # widgets.stackedWidget.setCurrentWidget(widgets.new_page2)
        # TUIFunctions.resetStyle(self, btnName)
        # btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))
        # print('cos tam')
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Files (*.mat)')

        self.Model = fname[0]

    def buttonVoltagesClick(self):
        # btn = self.sender()
        # btnName = btn.objectName()
        # widgets.stackedWidget.setCurrentWidget(widgets.new_page2)
        # TUIFunctions.resetStyle(self, btnName)
        # btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))
        fname = QFileDialog.getOpenFileName(
            self, 'Open file', '', 'Files (*.csv)')
        self.Voltages = fname[0]
        AA = read_csv(fname[0], sep=';', header=None).to_numpy()
        self.tui.new_page.meas_page.model._data = AA[:, 3:-1].tolist()

    # def buttonModelClick(self):
    #     btn = self.sender()  # get button
    #
    #     btnName = btn.objectName()
    #     widgets.stackedWidget.setCurrentWidget(widgets.btn_Model)
    #     TUIFunctions.resetStyle(self, btnName)
    #     btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))
    #
    # #     załaduj model
    #
    #
    #
    #     fname = QFileDialog.getOpenFileName(
    #         self, 'Open file', '', 'Files (*.mat)')
    #
    #     self.model_path = fname[0]
    #     mesh = load_mesh_from_mat_file_v2(fname[0])
    #     self.mesh = mesh
    #     # w = gl.GLViewWidget()
    #     # ww = gl.GLVolumeItem(mesh['elems'])
    #     # w.addItem(ww)
    #     # self.inputGraph.addItem(w)
    #
    # def buttonVoltagesClick(self):
    #     btn = self.sender()  # get button
    #
    #     btnName = btn.objectName()
    #     widgets.stackedWidget.setCurrentWidget(widgets.btn_voltages_EIT)
    #     TUIFunctions.resetStyle(self, btnName)
    #     btn.setStyleSheet(TUIFunctions.selectMenu(btn.styleSheet()))
    #
    #     fname = QFileDialog.getOpenFileName(
    #         self, 'Open file', '', 'Files (*.npz)')
    #
    #     self.voltages_path = fname[0]

    # mouse click event




    def mousePressEvent(self, event):

        # drag position event
        self.dragPos = event.pos()
        # print(event.pos())

        # print mouse click event
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')

        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    def check_virtual_keyboard_visibility(self):

        # Get the virtual keyboard widget using its object name
        virtual_keyboard = QApplication.instance().inputMethod()
        virtual_keyboard.reset()

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

        # test

        # Dictionaries._AppVars['Language'] = 1
        # self.tui.retranslate_tui(self)

        retval = self.msgShutDownBox.exec_()

        if retval == 0:
            # os.system('shutdown -s -t 0')
            print('ok')


if __name__ == "__main__":
    import os
    os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("nx_logo.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
