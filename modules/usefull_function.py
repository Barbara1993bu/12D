import numpy as np

from PySide2.QtGui import *

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvas
import scipy.sparse as sp
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


def find_FFFE(str):
    N = len(str)
    for x in range(N-2):
        if str[x:x+2] == b'\xff\xfe':
            ind = x
            break
        else:
            ind = None
    return ind


def find_FEFF(str):
    N = len(str)
    for x in range(N):
        if str[x:x+2] ==b'\xfe\xff':
            ind = x
            break
        else:
            ind = None
    return ind



def stim_pattern3D(stim_structure):
    n_electrodes = stim_structure['n_electrodes']
    d_stim = stim_structure['d_stim']
    d_meas = stim_structure['d_meas']
    z_contact = stim_structure['z_contact']
    amp = stim_structure['amp']

    stim = {
        'stim_pattern': list([]),
        'meas_pattern': list([]),
        'z_contact': z_contact
    }
    ele_half = int(n_electrodes/2)
    ele_minus_stim = np.int32(np.linspace(0, n_electrodes - 1, n_electrodes))
    ele_plus_stim = np.array([(x+d_stim) % ele_half + int(x/ele_half)*ele_half for x in ele_minus_stim])
    n_projection = ele_minus_stim.size
    if d_stim == d_meas:
        ele_minus_meas = ele_minus_stim
        ele_plus_meas = ele_plus_stim
    else:
        ele_minus_meas = np.int32(np.linspace(0, n_electrodes - 1, n_electrodes))
        ele_plus_meas = np.array([(x+d_meas)%ele_half + int(x/ele_half)*ele_half for x in ele_minus_stim])
    value = np.ones([1, n_projection])
    stim_plus_stim = [
        sparse_row(np.int32(np.array([ele_plus_stim[x]])), np.array([-1 * amp * value[0, x]]), n_electrodes)
        for x in range(0, n_projection)]
    stim_minus_stim = [
        sparse_row(np.int32(np.array([ele_minus_stim[x]])), np.array([amp * value[0, x]]), n_electrodes)
        for x in range(0, n_projection)]
    stim["stim_pattern"] = [stim_plus_stim[x] + stim_minus_stim[x] for x in range(0, n_projection)]
    ind_dele = np.row_stack([ele_plus_stim, ele_minus_stim])
    stim_plus_meas = [sparse_matrix_meas_pattern(ele_plus_meas, value, n_electrodes, ind_dele[:, x]) for x in
                      range(0, n_projection)]
    stim_minus_meas = [sparse_matrix_meas_pattern(ele_minus_meas, -1 * value, n_electrodes, ind_dele[:, x]) for x in
                       range(0, n_projection)]
    Z = [(stim_plus_meas[x] + stim_minus_meas[x]) for x in range(0, n_projection)]

    stim["meas_pattern"] = [delate_zeros_rows(Z[x]) for x in range(0, n_projection)]
    return stim



def sparse_row(ind_y, value, len_row):
    ind_x = np.int32(np.array(np.zeros_like(ind_y)))
    return sp.csc_matrix((value, (ind_x, ind_y)), shape=(1, len_row))


def sparse_matrix_meas_pattern(ind_y, value, len_matrix, ind_delete):
    ind_x = np.linspace(0, len_matrix - 1, len_matrix)
    X = sp.csc_matrix((value.reshape(-1), (ind_x, ind_y)), shape=(len_matrix, len_matrix))
    X = X.toarray()
    X[:, ind_delete] = 0

    return sp.csc_matrix(X)


def delate_zeros_rows(Z):
    ZN = Z.toarray()
    ind_zero_row = np.argwhere(np.sum(abs(ZN), axis=1) < 2)
    ZN = np.delete(ZN, ind_zero_row, axis=0)

    return sp.csc_matrix(ZN)