import time
from datetime import datetime

import numpy as np
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer
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

import PySide2
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




# -----------------------------------------
# main TUI Window
# -----------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

        widgets.new_page.meas_page.Set_of_colorMap.currentIndexChanged.connect(self.change_colorMap)

        widgets.new_page.reconstruction_page.btn_Model.clicked.connect(self.buttonModelClick)
        widgets.new_page.reconstruction_page.btn_voltages_EIT.clicked.connect(self.buttonVoltagesClick)
        widgets.new_page.reconstruction_page.btn_reconstruction.clicked.connect(self.buttonReconstructionClick)
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
        # widgets.new_page.inputGraph.focused.connect(closeKeyboardTab)
        # widgets.new_page.inputGraph.noneFocused.connect(closeKeyboardTab)
        # widgets.keyboardwidget.

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

    # def MeasPage_mouseMove(self, s):
    #     color = Settings.BTN_RIGHT_BOX_COLOR
    #     style = widgets.stackedWidget.new_page.btn_meas.styleSheet()
    #     self.tui.new_page.btn_meas.setStyleSheet("background:rgba(90,90,250,90)")


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

        str_message = 'Visualization saved to ' + path

        self.tui.new_page.reconstruction_page.Info_box.moveCursor(QTextCursor.Start)
        self.tui.new_page.reconstruction_page.Info_box.insertPlainText(str_message + '\n')
        self.tui.new_page.reconstruction_page.Info_box.moveCursor(QTextCursor.Start)



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
        worker = Worker(self.tui.solve_inverse_problem)
        worker.signals.progress.connect(self.reconstruction_progress)
        worker.signals.result.connect(self.reconstruction_results)
        worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(worker)

    def thread_complete(self):
        print('Dane')

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
