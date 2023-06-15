import os
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


class ColorDelegate(QItemDelegate):
    def __init__(self, color_palette):
        super().__init__()
        self.color_palette = color_palette

    def paint(self, painter, option, index):
        value = float(index.data(Qt.DisplayRole))

        if index.row() == index.column():
            color = QColor(0, 0, 0)
        else:
            color = self.get_color_from_palette(value)
        painter.fillRect(option.rect, color)

        super().paint(painter, option, index)

    def get_color_from_palette(self, value):
        min_value = min(self.color_palette.keys())
        max_value = max(self.color_palette.keys())

        if value <= min_value:
            return self.color_palette[min_value]
        elif value >= max_value:
            return self.color_palette[max_value]

        # range_values = max_value - min_value
        # normalized_value = (value - min_value) / range_values

        lower_value = max_key = min_key = None

        for key in sorted(self.color_palette.keys()):
            if key >= value:
                max_key = key
                break
            lower_value = key

        if lower_value is not None and max_key is not None:
            range_values = max_key - lower_value
            normalized_value = (value - lower_value) / range_values
            lower_color = self.color_palette[lower_value]
            max_color = self.color_palette[max_key]
            interpolated_color = self.interpolate_color(lower_color, max_color, normalized_value)
            return interpolated_color

    def interpolate_color(self, color1, color2, normalized_value):
        red = int((1 - normalized_value) * color1.red() + normalized_value * color2.red())
        green = int((1 - normalized_value) * color1.green() + normalized_value * color2.green())
        blue = int((1 - normalized_value) * color1.blue() + normalized_value * color2.blue())
        return QColor(red, green, blue)


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None



class meas_page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName(u"meas_page")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.Frame_meas = QFrame(self)
        # self.Frame_meas.setStyleSheet("background-color: rgba(90,90,250,90)")
        self.Frame_meas.setFixedSize(2000, 1000)
        # self.Frame_meas.setMaximumSize(2000, 1000)
        self.Layout_meas = QHBoxLayout(self.Frame_meas)
        self.Frame_meas.setLayout(self.Layout_meas)

        self.table = QTableView()
        self.table.setFixedSize(1000, 800)

        # QHeaderView
        data = np.zeros((32, 32)).tolist()
        color_palette = {
            0: QColor(255, 255, 255),
            1: QColor(255, 0, 0),  # Czerwony
            2: QColor(0, 255, 0),  # Zielony
            3: QColor(0, 0, 255)  # Niebieski
        }

        self.model = TableModel(data)

        # self.model.
        self.table.setModel(self.model)

        self.table.resizeColumnsToContents()
        delegate = ColorDelegate(color_palette)
        self.table.setItemDelegate(delegate)
        self.table.show()
        # self.table.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.Layout_meas.addWidget(self.table, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.Frame_colorMap = QFrame(self.Frame_meas)
        self.Frame_colorMap.setFixedSize(800, 110)
        self.Layout_colorMap = QVBoxLayout(self.Frame_colorMap)
        self.Frame_colorMap.setLayout(self.Layout_colorMap)

        self.Label_colorMap = QLabel(self.Frame_colorMap)
        self.Label_colorMap.setFixedSize(200, 50)
        self.Label_colorMap.setStyleSheet("color: black;"
                                          "font: bold;"
                                          "font-size: 15px")

        self.Set_of_colorMap = QComboBox(self.Frame_colorMap)
        self.Set_of_colorMap.setStyleSheet("color: white;"
                                           "background-color: rgb(147, 186, 249);"
                                           "selection-color: red;"
                                           "selection-background-color: rgb(40,40,250);")
        self.Set_of_colorMap.setFixedSize(500, 50)
        self.Layout_colorMap.addWidget(self.Label_colorMap)
        self.Layout_colorMap.addWidget(self.Set_of_colorMap)
        self.Layout_meas.addWidget(self.Frame_colorMap, alignment=Qt.AlignLeft | Qt.AlignTop)
