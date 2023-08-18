import os

import pyqtgraph
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



class nxQDoubleSpinBox(QSpinBox):

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


class SliderAmp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Tworzenie obiektu suwaka
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setFocusPolicy(Qt.NoFocus)  # Opcjonalnie, aby suwak nie miał fokusu

        # Ustawianie zakresu wartości suwaka
        self.slider.setMinimum(300)
        self.slider.setMaximum(10000)
        self.slider.setPageStep(10)

        # Ustawianie początkowej wartości suwaka
        self.slider.setValue(300)

        # Tworzenie etykiety
        self.label = QLabel(str(self.slider.value()) + '\u03BCA', self)
        self.label.setGeometry(QRect(0, -30, 40, 20))  # Ustawienie pozycji etykiety

        # Podpinanie sygnałów zmiany wartości suwaka do metod
        self.slider.valueChanged[int].connect(self.onSliderChange)
        self.slider.sliderMoved[int].connect(self.onSliderMove)

        # Tworzenie układu pionowego i dodawanie suwaka oraz etykiety do niego
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        # self.setWindowTitle('Slider Example')
        self.show()

    def onSliderChange(self, value):
        self.label.setText(str(value) + '\u03BCA')  # Aktualizacja wartości etykiety po zmianie suwaka

    def onSliderMove(self, value):
        self.label.move(value * (self.slider.width() - self.label.width()) / self.slider.maximum(), -30)  # Aktualizacja pozycji etykiety wraz z ruchem suwaka





class param_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(u"b")
        # Layout reconstruction EIT
        self.widgets = QFrame(self)
        # self.widgets.setBaseSize(700, 700)
        self.widgets.setMinimumSize(500,500)
        self.widgets.setMaximumSize(700, 1000)
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"b")

        self.vertLayoutWidgets = QVBoxLayout(self.widgets)
        self.vertLayoutWidgets.setObjectName(u"vertLayoutWidgets")

        # Tryb rekonstrukcji Ect lub EIT lub Bought
        self.Frame_tryb = QFrame(self.widgets)
        self.Frame_tryb.setMaximumSize(700, 100)
        self.Layout_tryb = QHBoxLayout(self.Frame_tryb)
        self.Frame_tryb.setLayout(self.Layout_tryb)
        self.Label_tryb = QLabel(self.Frame_tryb)
        self.Label_tryb.setMaximumSize(200, 50)
        self.Label_tryb.setStyleSheet("color: black;"
                                      "font: bold;"
                                      "font-size: 15px")
        self.ComboBox_tryb = QComboBox(self.Frame_tryb)
        self.ComboBox_tryb.addItems(['EIT', 'ECT', 'EIT + ECT'])
        self.ComboBox_tryb.setStyleSheet("color: white;"
                                         "background-color: rgb(147, 186, 249);"
                                         "selection-color: red;"
                                         "selection-background-color: rgb(40,40,250);")
        self.ComboBox_tryb.setFixedSize(500, 50)
        self.Layout_tryb.addWidget(self.Label_tryb)
        self.Layout_tryb.addWidget(self.ComboBox_tryb)

        self.vertLayoutWidgets.addWidget(self.Frame_tryb)

        # Wzorzec stymulacji 0-4, 0-8, 0-16, 3D
        self.Frame_stim_pattern = QFrame(self.widgets)
        self.Frame_stim_pattern.setMaximumSize(700, 100)
        self.Layout_stim_pattern = QHBoxLayout(self.Frame_stim_pattern)
        self.Frame_stim_pattern.setLayout(self.Layout_stim_pattern)
        self.Label_stim_pattern = QLabel(self.Frame_stim_pattern)
        self.Label_stim_pattern.setFixedSize(200, 50)
        self.Label_stim_pattern.setStyleSheet("color: black;"
                                              "font: bold;"
                                              "font-size: 15px")
        self.ComboBox_stim_pattern = QComboBox(self.Frame_stim_pattern)
        self.ComboBox_stim_pattern.addItems(['32(0-4)', '32(0-8)', '32(0-16)', '32 3D'])
        self.ComboBox_stim_pattern.setStyleSheet("color: white;"
                                                 "background-color: rgb(147, 186, 249);"
                                                 "selection-color: red;"
                                                 "selection-background-color: rgb(40,40,250);")
        self.ComboBox_stim_pattern.setMaximumSize(500, 50)
        self.Layout_stim_pattern.addWidget(self.Label_stim_pattern)
        self.Layout_stim_pattern.addWidget(self.ComboBox_stim_pattern)

        self.vertLayoutWidgets.addWidget(self.Frame_stim_pattern)

        # Częstotliwość  1kH, 10kH, 100kH, 200kH
        self.Frame_frequency = QFrame(self.widgets)
        self.Frame_frequency.setMaximumSize(700, 100)
        self.Layout_frequency = QHBoxLayout(self.Frame_frequency)
        self.Frame_frequency.setLayout(self.Layout_frequency)
        self.Label_frequency = QLabel(self.Frame_frequency)
        self.Label_frequency.setFixedSize(200, 50)
        self.Label_frequency.setStyleSheet("color: black;"
                                           "font: bold;"
                                           "font-size: 15px")
        self.ComboBox_frequency = QComboBox(self.Frame_frequency)
        self.ComboBox_frequency.addItems(['1kHz', '10kHz', '100kHz', '200kHz'])
        self.ComboBox_frequency.setStyleSheet("color: white;"
                                              "background-color: rgb(147, 186, 249);"
                                              "selection-color: red;"
                                              "selection-background-color: rgb(40,40,250);")
        self.ComboBox_frequency.setMaximumSize(500, 50)
        self.Layout_frequency.addWidget(self.Label_frequency)
        self.Layout_frequency.addWidget(self.ComboBox_frequency)

        self.vertLayoutWidgets.addWidget(self.Frame_frequency)

        # odstęp czasowy między ramkami 3mili s lub 6s
        self.Frame_interval_frame = QFrame(self.widgets)
        self.Frame_interval_frame.setMaximumSize(700,100)
        self.Layout_interval_frame = QHBoxLayout(self.Frame_interval_frame)
        self.Frame_interval_frame.setLayout(self.Layout_interval_frame)
        self.Label_interval_frame = QLabel(self.Frame_interval_frame)
        self.Label_interval_frame.setMaximumSize(200, 50)
        self.Label_interval_frame.setStyleSheet("color: black;"
                                                "font: bold;"
                                                "font-size: 15px")
        self.LineEdit_interval_frame = nxQDoubleSpinBox()
        self.LineEdit_interval_frame.setValue(3)
        self.LineEdit_interval_frame.setRange(3, 5000)
        self.Label_interval_unit = QLabel(self.Frame_interval_frame)
        self.Label_interval_unit.setMaximumSize(50, 50)
        self.Label_interval_unit.setStyleSheet("color: black;"
                                                "font-size: 15px")
        self.Layout_interval_frame.addWidget(self.Label_interval_frame)
        self.Layout_interval_frame.addWidget(self.LineEdit_interval_frame)
        self.Layout_interval_frame.addWidget(self.Label_interval_unit)
        self.Label_interval_unit.setText('\u03BCs')


        self.vertLayoutWidgets.addWidget(self.Frame_interval_frame)

        # prąd od 300mikro s lub 10 mili s co 10 mikro s
        self.Frame_amp = QFrame(self.widgets)
        self.Frame_amp.setMaximumSize(700, 100)
        self.Layout_amp = QHBoxLayout(self.Frame_amp)
        self.Frame_amp.setLayout(self.Layout_amp)
        self.Label_amp = QLabel(self.Frame_amp)
        self.Label_amp.setMaximumSize(200, 50)
        self.Label_amp.setStyleSheet("color: black;"
                                     "font: bold;"
                                     "font-size: 15px")
        # self.Slider_amp = ValueSlider(Qt.Horizontal)
        self.Slider_amp = SliderAmp()
        # self.Slider_amp = QSlider(Qt.Horizontal)
        # self.Slider_amp.setMaximumSize(500, 50)
        #
        # self.Slider_amp.setMinimum(300)
        # self.Slider_amp.setMaximum(10000)
        # self.Slider_amp.setPageStep(10)
        # self.Slider_amp.setValue(300)
        self.Layout_amp.addWidget(self.Label_amp)
        self.Layout_amp.addWidget(self.Slider_amp)

        self.vertLayoutWidgets.addWidget(self.Frame_amp)

        # liczba odczytanych ramek 1 lub int
        self.Frame_int_frame = QFrame(self.widgets)
        self.Frame_int_frame.setMaximumSize(700, 100)
        self.Layout_int_frame = QHBoxLayout(self.Frame_int_frame)
        self.Frame_int_frame.setLayout(self.Layout_int_frame)
        self.Label_int_frame = QLabel(self.Frame_int_frame)
        self.Label_int_frame.setMaximumSize(200, 50)
        self.Label_int_frame.setStyleSheet("color: black;"
                                           "font: bold;"
                                           "font-size: 15px")
        self.LineEdit_int_frame = nxQDoubleSpinBox()
        self.Layout_int_frame.addWidget(self.Label_int_frame)
        self.Layout_int_frame.addWidget(self.LineEdit_int_frame)

        self.vertLayoutWidgets.addWidget(self.Frame_int_frame)

        self.Frame_Live_check_box = QFrame(self.widgets)
        # self.Frame_Live_check_box.setMinimumSize(200, 50)
        self.Frame_Live_check_box.setMaximumSize(200, 50)
        self.Layout_Live_check_box = QHBoxLayout(self.Frame_Live_check_box)
        self.Frame_Live_check_box.setLayout(self.Layout_Live_check_box)
        self.Live_check_box = QCheckBox(self.Frame_Live_check_box)

        self.Text_Live = QLabel(self.Frame_Live_check_box)
        self.Text_Live.setStyleSheet("color: black;"
                                     "font: bold;"
                                     "font-size: 15px")

        self.Layout_Live_check_box.addWidget(self.Text_Live)
        self.Layout_Live_check_box.addWidget(self.Live_check_box)

        self.vertLayoutWidgets.addWidget(self.Frame_Live_check_box)


        self.Frame_btn_send_param = QFrame(self.widgets)
        self.Frame_btn_send_param.setMinimumSize(400, 50)
        self.Frame_btn_send_param.setMaximumSize(500, 300)
        self.Layout_btn_send_param = QHBoxLayout(self.Frame_btn_send_param)
        self.Frame_btn_send_param.setLayout(self.Layout_btn_send_param)
        self.btn_send_params = QPushButton(self.Frame_btn_send_param)
        self.btn_send_params.setMinimumSize(200, 50)
        self.btn_send_params.setStyleSheet(u"QPushButton {\n"
                                           "	background-color: rgb(147, 186, 249);\n"
                                           "background-repeat: no-repeat;\n"
                                           "border-radius: 10px;\n"
                                           "font-size: 15px;\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "	background-color: rgb(147, 186, 249);\n"
                                           "}\n"
                                           "QPushButton:pressed {	\n"
                                           "	background-color: rgb(40,40,250);\n"
                                           "}")
        self.Layout_btn_send_param.addWidget(self.btn_send_params)

        self.btn_STOP = QPushButton(self.Frame_btn_send_param)
        self.btn_STOP.setMinimumSize(100, 50)
        self.btn_STOP.setStyleSheet(u"QPushButton {\n"
                                    "	background-color: rgb(147, 186, 249);\n"
                                    "background-repeat: no-repeat;\n"
                                    "border-radius: 10px;\n"
                                    "font-size: 15px;\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "	background-color: rgb(147, 186, 249);\n"
                                    "}\n"
                                    "QPushButton:pressed {	\n"
                                    "	background-color: rgb(40,40,250);\n"
                                    "}")
        self.btn_STOP.setText('STOP')
        self.btn_STOP.setEnabled(False)
        self.Layout_btn_send_param.addWidget(self.btn_STOP)

        self.vertLayoutWidgets.addWidget(self.Frame_btn_send_param)
