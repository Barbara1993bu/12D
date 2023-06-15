import numpy as np

from PySide2.QtGui import *

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvas
# matplotlib.use('Qt5Agg')

from mpl_toolkits.axes_grid1 import make_axes_locatable


def rotation_ZY(alpha, beta):
    alpha_radian = alpha*np.pi/180
    beta_radian = beta*np.pi/180
    cos_alpha = np.cos(alpha_radian)
    sin_alpha = np.sin(alpha_radian)
    cos_beta = np.cos(beta_radian)
    sin_beta = np.sin(beta_radian)
    Rz = np.array([[cos_alpha, -sin_alpha, 0],
                   [sin_alpha, cos_alpha, 0],
                   [0, 0, 1]])
    Ry = np.array([[cos_beta, 0, sin_beta],
                   [0, 1, 0],
                   [-sin_beta, 0, cos_beta]])
    return np.matmul(Rz, Ry)


def build_tri(W_i, reference_level=None, width=4, hight=4):

    # sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

    # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
    # toolbar = NavigationToolbar(sc, self)
    # figure, axes = plt.subplots(1, 1)
    distribution = W_i[2].copy()
    colormap = np.load('cm/cm_seismic.npy')
    cm = np.flip(colormap, 0)
    sm = matplotlib.colors.LinearSegmentedColormap.from_list("kaczka", cm[:, :3].tolist(), 256)

    if reference_level is None:
        reference_level = W_i[2].mean()


    fig = Figure((width, hight))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot()

    image_properties = {'linestyle': '-', 'linewidth': 0.15, 'edgecolor': 'black'}
    image = ax.tripcolor(np.array(W_i[0][:, 0].reshape(-1)), np.array(W_i[0][:, 1].reshape(-1)),
                         np.array(W_i[1]),
                         facecolors=np.array(distribution.reshape(-1)), cmap=sm,
                         shading='flat', **image_properties)
    delta_max = np.max(np.abs(distribution - reference_level))

    image.set_clim(reference_level - delta_max, reference_level + delta_max)

    ax.axis('equal')

    # ax.set_xlabel(lab_x)
    # ax.set_ylabel(lab_y)
    # ax.set_xlim(W_i[0][:, 0].min(), W_i[0][:, 0].max())
    # ax.set_ylim(W_i[0][:, 1].min(), W_i[0][:, 1].max())
    # fig.tight_layout()
    canvas.draw()
    # sc.axes.imshow()

    width, height = fig.figbbox.width, fig.figbbox.height
    img = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pix_map = QPixmap(img)

    # sc.tight_layout()
    return pix_map


def build_color_palette(A, cmap='default'):
    AA = np.triu(A) - np.diag(np.diag(A))
    MinA = np.nanmin(AA)
    MaxA = np.nanmax(AA)
    MaxAA = np.nanmax(A)

    N_colors = 6
    # ind = np.linspace(0, 255, 6, dtype=int)
    ind = np.linspace(MinA, MaxA, 5)
    # ind = value[ind]
    # colormap = np.load('cm/cm_seismic.npy')
    # color_palette = dict()
    if cmap == 'default':
        color_palette = {
            ind[0]: QColor(255, 255, 255),  # Biały
            ind[1]: QColor(255, 255, 0),    # Żółty
            ind[2]: QColor(0, 255, 0),      # Zielony
            ind[3]: QColor(0, 0, 200),      # Niebieski
            ind[4]: QColor(255, 0, 0),      # Czerwony
            MaxAA: QColor(255, 0, 255)      # Magenta
        }

    else:
        cm = matplotlib.cm.get_cmap(cmap)
        V1 = cm(0)
        V2 = cm(0.25)
        V3 = cm(0.5)
        V4 = cm(0.75)
        V5 = cm(1)
        color_palette = {
            ind[0]: QColor(int(V1[0]*255), int(V1[1]*255), int(V1[2]*255)),
            ind[1]: QColor(int(V2[0]*255), int(V2[1]*255), int(V2[2]*255)),
            ind[2]: QColor(int(V3[0]*255), int(V3[1]*255), int(V3[2]*255)),
            ind[3]: QColor(int(V4[0]*255), int(V4[1]*255), int(V4[2]*255)),
            ind[4]: QColor(int(V5[0]*255), int(V5[1]*255), int(V5[2]*255)),
            MaxAA: QColor(255, 0, 255)  # Magenta
        }


    # for x in range(N_colors):
    #     color_palette[value[x]] = QColor(colormap[ind[x]][0], colormap[ind[x]][1], colormap[ind[x]][2])
    return color_palette


def print_voltages(U1,U2):

    fig = Figure((16, 3))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot()
    ax.plot(U1.reshape(-1))
    ax.plot(U2.reshape(-1))
    fig.legend(['Voltages real', 'Voltages calculate'], loc ="lower right")

    canvas.draw()
    # sc.axes.imshow()

    width, height = fig.figbbox.width, fig.figbbox.height
    img = QImage(canvas.buffer_rgba(), width, height, QImage.Format_ARGB32)
    pix_map = QPixmap(img)

    # sc.tight_layout()
    return pix_map

