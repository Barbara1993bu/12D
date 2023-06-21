import numpy as np
import scipy.sparse as sp
# import scipy
from scipy.sparse.linalg import spsolve

import plotly.graph_objects as go
# from plotly.offline import iplot
# from plotly.offline import init_notebook_mode
import matplotlib.colors
import matplotlib.cm
import vedo
import collections
import itertools
import time
from scipy.signal import argrelextrema
import functools
import copy
from numba import jit
from MatrixD import matrixD

# import matplotlib.pyplot as plt
# import pickle


def stim_pattern(stim_structure):
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
    ele_minus_stim = np.int32(np.linspace(0, n_electrodes - 1, n_electrodes))
    ele_plus_stim = np.int32(np.linspace(d_stim, n_electrodes + d_stim - 1, n_electrodes) % n_electrodes)
    n_projection = ele_minus_stim.size
    if d_stim == d_meas:
        ele_minus_meas = ele_minus_stim
        ele_plus_meas = ele_plus_stim
    else:
        ele_minus_meas = np.int32(np.linspace(0, n_electrodes - 1, n_electrodes))
        ele_plus_meas = np.int32(np.linspace(d_meas, n_electrodes + d_meas - 1, n_electrodes) % n_electrodes)
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


def l_curve(a_function, A, b, method='tikh'):
    n_points = np.int(500)
    lam = np.geomspace(30, 0.3e-11, n_points)

    x = np.array([a_function(b, lamb=t) for t in lam])

    x_norm = np.linalg.norm(x, axis=1)
    x_log = np.log(x_norm)
    x_diff = np.diff(x_log)
    # extremum_maxX = argrelextrema(x_diff, np.greater)
    # extremum_minX = argrelextrema(x_diff, np.less)

    res = np.array([A @ x[i, :] - b for i in range(0, n_points)])
    res_norm = np.linalg.norm(res, axis=1)
    res_log = np.log(res_norm)
    res_diff = np.diff(res_log)
    grad = x_diff + res_diff
    extremum_min = argrelextrema(grad, np.less)
    k = extremum_min[0][0]
    p = np.polyfit(x_log[np.r_[0, n_points - 1]], res_log[np.r_[0, n_points - 1]], deg=1)
    pv = np.polyval(p, x_log)
    dist = np.abs(pv - res_log)
    k1 = np.argmax(dist)

    # extremum_maxR = argrelextrema(res_diff, np.greater)
    # extremum_minR = argrelextrema(res_diff, np.less)
    #
    # D = np.array([np.abs(i-j) for i in extremum_maxR[0] for j in extremum_maxX[0]]).reshape(len(extremum_maxR[0]), len(extremum_maxX[0]))
    # id = np.argwhere(D < 50)
    #
    # Rid = extremum_maxR[0][id[:, 0]]
    # Xid = extremum_maxX[0][id[:, 1]]
    # k1 = np.argmin(np.abs(Rid-Xid))
    # k = np.int((Xid+Rid)[k1]*0.5)
    # if method == 'tikh' or method == 'lm' or method == 'dg':
    #     M = np.max([extremum_min[0][0], extremum_max[0][0]])
    #     m = np.min([extremum_min[0][0], extremum_max[0][0]])
    #     k = np.int(m + 1/3*(M - m))
    # if method == 'gn' or method == 'gs' or method == 'kotre':
    #     M = np.max([extremum_min[0][1], extremum_max[0][1]])
    #     m = np.min([extremum_min[0][1], extremum_max[0][1]])
    #     k = np.int(m + 1/3*(M - m))

    # k1 = np.argmax(res_diff)
    return lam[k].reshape(-1), x, x_log, res, lam[k1].reshape(-1)


def wrapper_time(a_function):
    def a_wrapped_function(*args, **kwargs):
        time_start = time.time()
        v = a_function(*args, **kwargs)
        time_stop = time.time()
        ts = time_stop - time_start
        print(">>>>>Function {} executed in {}".format(a_function.__name__, ts))
        # times.append(ts)
        return v

    return a_wrapped_function


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


class Image_EIT_3D_tetra:
    profiler = {
        'objective_function': False,
        'reconstruction': False,
        'reconstruction_gn': False,
        'pom_obj_fun': False,
        'calculate_alpha': False,
        'matrix_of_sensitivity': False,
        'change_ms_inv': False,
        'simulation': False,
        'potential': False,
        'state_matrix': False,
        'state_matrix_line': False,
        'state_matrix_surface': False,
        'state_matrix_point': False,
    }
    numba_profiler = {
        'objective_function': True,
        'reconstruction': True,
        'reconstruction_gn': True,
        'pom_obj_fun': True,
        'calculate_alpha': True,
        'matrix_of_sensitivity': True,
        'change_ms_inv': True,
        'simulation': True,
        'potential': True,
        'state_matrix': True,
        'state_matrix_line': True,
        'state_matrix_surface': True,
        'state_matrix_point': True,
    }
    electrodes_line_segments = np.array([])
    RtR = np.array([])

    def wrapper(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            if any([x == func.__name__ for x in self.numba_profiler.keys()]):
                if self.numba_profiler[func.__name__][0]:
                    if self.numba_profiler[func.__name__][1] is None:
                        self.numba_profiler[func.__name__][1] = jit(func, forceobj=True)
                    func1 = self.numba_profiler[func.__name__][1]
                else:
                    func1 = func
            else:
                func1 = func
            if any([x == func.__name__ for x in self.profiler.keys()]):
                if self.profiler[func1.__name__]:
                    # config.DISABLE_JTR = not self.numba_profiler
                    t0 = time.time()
                    v = func1(self, *args, **kwargs)
                    ts = time.time() - t0
                    print(">>>>>Function {} executed in {}".format(func.__name__, ts))
                else:
                    # config.DISABLE_JTR = not self.numba_profiler
                    v = func1(self, *args, **kwargs)

            else:
                v = func1(self, *args, **kwargs)
            return v

        return wrap

    def __init__(self, mesh, stimulation=None, shape_ele='point'):
        if isinstance(mesh, str):
            I = dict(np.load(mesh, allow_pickle=True))
            for x in I.keys():
                if I[x].shape == ():
                    value = I[x].tolist()
                else:
                    value = I[x]
                setattr(self, x, value)
            self.electrodes = self.electrodes.tolist()
            for k in range(len(self.electrodes)):
                if not isinstance(self.electrodes[k], int):
                    for i in range(len(self.electrodes[k])):
                        self.electrodes[k][i] = np.int64(self.electrodes[k][i])
        else:
            self.elems = mesh['elems']
            self.nodes = mesh['nodes']
            self.boundary = mesh['boundary']
            if shape_ele == 'surface':
                self.electrodes = [mesh['electrodes_nodes'], mesh['electrodes_elems']]
            else:
                self.electrodes = mesh['electrodes_nodes']

            if (shape_ele == 'line'): self.line_segments_for_1D_electrodes()

            self.stim = { }

            if stimulation is None:
                self.stim['meas_pattern'] = mesh['meas_pattern']
                self.stim['stim_pattern'] = mesh['meas_pattern']
                self.z_contact = mesh['z_contact']
            else:
                values = ['stim_pattern', 'meas_pattern', 'z_contact']
                values2 = ['n_electrodes', 'd_stim', 'd_meas', 'amp', 'z_contact']
                if all(np.array([i == k for i, k in zip(stimulation.keys(), values)])):
                    for k in stimulation.keys():
                        self.stim[k] = stimulation[k]
                elif all(np.array([i == k for i, k in zip(stimulation.keys(), values2)])):
                    self.get_stim_pattern(stimulation)
            self.n_electrode = len(mesh['electrodes_nodes'])
            self.shape_ele = shape_ele
            self.value_elems = mesh['elem_data']
            self.mesh_variables()

        self.iteration_solution = []
        self.value_of_obj_fun = []
        self.change_numba_profiler(start=True, profiler=False)
        self.volumes_of_tetrahedra()
        self.up_grade_value_elems(self.value_elems)

    @wrapper
    def set_up(self, method='kotre', lamb=1e-4, p=0.5, calculate_SVD=False):
        self.method = method
        self.lamb = lamb
        self.p = p
        self.state_matrix()
        self.potential(self.sources_for_adjoint_fields_PSI())
        self.matrix_of_sensitivity(decomp_svd=calculate_SVD)
        self.change_ms_inv(method=method, lamb=lamb, p=p)

    def change_numba_profiler(self, start=False, key=None, value=None, profiler=None):
        if start:
            for k in self.numba_profiler.keys():
                if self.numba_profiler[k]:
                    self.numba_profiler[k] = [False, None]

        else:
            if key is not None:
                self.numba_profiler[key][0] = value
        if profiler is not None:
            for k in self.profiler.keys():
                self.profiler[k] = profiler

    @wrapper
    def mesh_variables(self):

        i = self.elems[:, 0].reshape(-1)
        j = self.elems[:, 1].reshape(-1)
        k = self.elems[:, 2].reshape(-1)
        l = self.elems[:, 3].reshape(-1)

        nodes = self.nodes
        x = nodes[:, 0]

        y = nodes[:, 1]

        z = nodes[:, 2]

        mx = 0.25 * (x[i] + x[j] + x[k] + x[l])
        my = 0.25 * (y[i] + y[j] + y[k] + y[l])
        mz = 0.25 * (z[i] + z[j] + z[k] + z[l])

        middle = np.array([mx, my, mz]).T

        tri1 = np.row_stack([i, j, k]).T
        tri2 = np.row_stack([i, j, l]).T
        tri3 = np.row_stack([i, k, l]).T
        tri4 = np.row_stack([j, k, l]).T
        tri = np.row_stack([tri1, tri2, tri3, tri4])
        tri_S = np.sort(tri, axis=1)
        tri_unique, index, ind_nonunique, counts = np.unique(tri_S, axis=0, return_counts=True,
                                                             return_inverse=True, return_index=True)

        # fig = plt.figure(figsize=plt.figaspect(0.5))
        # ax = fig.add_subplot(1, 2, 1, projection='3d')
        #
        # for i in range(0, len(tri_unique)):
        #     czw = np.block([tri_unique[i, :], tri_unique[i, :]]).reshape(-1)
        #     ax.plot(x[czw], y[czw], z[czw])
        #     input('enter')
        #     print(np.str(i))
        D = collections.Counter(ind_nonunique)
        ind = [np.argwhere(ind_nonunique == k) for k in D.keys()]
        L = np.array([len(x) for x in ind])
        ind2 = np.array([ind[x].reshape(-1) if L[x] == 2 else np.tile(ind[x], [2, 1]).reshape(-1)
                         for x in range(0, len(L))])
        K = np.array([np.argwhere(ind2 == x)[0, 0] for x in index])

        # elektrody
        if self.shape_ele == 'surface':
            electrode_elems = self.electrodes[1]
            idx_ele_tri = np.asarray(list(itertools.chain(*electrode_elems)))

            e_tri = self.boundary[idx_ele_tri, :]
            self.mesh = {
                'surface_unique': tri_unique,
                'ind_nonunique': ind_nonunique,
                'ind': ind2[K, :],
                'dict_caunt_surfaces': D,
                'middle': middle,
                'index': index,
                'ele_tri': e_tri,
                'value_tri_elems': np.ones(len(tri_unique))
            }
        else:
            electrode_node = self.electrodes
            ele_nodes = np.array(electrode_node)
            self.mesh = {
                'surface_unique': tri_unique,
                'ind_nonunique': ind_nonunique,
                'ind': ind2[K, :],
                'dict_caunt_surfaces': D,
                'middle': middle,
                'index': index,
                'ele_tri': self.nodes[ele_nodes.reshape(-1), :],
                'value_tri_elems': np.ones(len(tri_unique))
            }

    @wrapper
    def volumes_of_tetrahedra(self):

        indices_i = self.elems[:, 0]
        indices_j = self.elems[:, 1]
        indices_k = self.elems[:, 2]
        indices_l = self.elems[:, 3]

        x_1 = self.nodes[indices_i, 0]
        x_2 = self.nodes[indices_j, 0]
        x_3 = self.nodes[indices_k, 0]
        x_4 = self.nodes[indices_l, 0]

        y_1 = self.nodes[indices_i, 1]
        y_2 = self.nodes[indices_j, 1]
        y_3 = self.nodes[indices_k, 1]
        y_4 = self.nodes[indices_l, 1]

        z_1 = self.nodes[indices_i, 2]
        z_2 = self.nodes[indices_j, 2]
        z_3 = self.nodes[indices_k, 2]
        z_4 = self.nodes[indices_l, 2]

        D = (x_2 - x_1) * ((y_3 - y_1) * (z_4 - z_1) - (y_4 - y_1) * (z_3 - z_1)) + \
            (x_3 - x_1) * ((y_4 - y_1) * (z_2 - z_1) - (y_2 - y_1) * (z_4 - z_1)) + \
            (x_4 - x_1) * ((y_2 - y_1) * (z_3 - z_1) - (y_3 - y_1) * (z_2 - z_1))

        self.V_elems = np.abs(D.flatten()) / 6.0

    @wrapper
    def line_segments_for_1D_electrodes(self):

        triangles = self.boundary.copy()

        rows = list(range(triangles.shape[0]))

        C = [(0, 1), (1, 2), (2, 0)]

        edges = np.vstack(tuple([triangles[np.ix_(rows, columns)] for columns in C]))

        _, index = np.unique(np.sort(edges, 1), axis=0, return_index=True)

        edges = edges[index]

        line_segments = [edges[np.sum(np.isin(edges, E_nodes), axis=1) == edges.shape[1], :] for E_nodes in
                         self.electrodes]

        self.electrodes_line_segments = line_segments

    @staticmethod
    def determine_boundary_elements(volume_elements):

        rows = list(range(volume_elements.shape[0]))

        L = list(range(volume_elements.shape[1]))

        C = list(itertools.combinations(L, len(L) - 1))

        surface_elements = np.vstack(tuple([volume_elements[np.ix_(rows, columns)] for columns in C]))

        surface_elements, indices, counts = np.unique(np.sort(surface_elements, 1), return_index=True,
                                                      return_counts=True, axis=0)

        boundary_elements = surface_elements[counts == 1, :]

        indices_VE = np.tile(np.array(rows), len(C))

        indices_VE = indices_VE[indices[counts == 1]]

        return boundary_elements, indices_VE

    @wrapper
    def display(self, colormap='picnic', middle_value=None):
        x = self.nodes[:, 0]
        y = self.nodes[:, 1]
        z = self.nodes[:, 2]
        tri = self.mesh['surface_unique']
        i = tri[:, 0]
        j = tri[:, 1]
        k = tri[:, 2]
        if self.shape_ele == 'surface':
            e_i = self.mesh['ele_tri'][:, 0]
            e_j = self.mesh['ele_tri'][:, 1]
            e_k = self.mesh['ele_tri'][:, 2]
        elif self.shape_ele == 'line':
            L_ele = np.array([len(x) for x in self.electrodes_line_segments])
            electrodes_line_segments = np.row_stack(self.electrodes_line_segments)
            x_e1 = self.nodes[electrodes_line_segments[:, 0], 0]
            x_e2 = self.nodes[electrodes_line_segments[:, 1], 0]

            y_e1 = self.nodes[electrodes_line_segments[:, 0], 1]
            y_e2 = self.nodes[electrodes_line_segments[:, 1], 1]

            z_e1 = self.nodes[electrodes_line_segments[:, 0], 2]
            z_e2 = self.nodes[electrodes_line_segments[:, 1], 2]
        else:
            x_e = self.mesh['ele_tri'][:, 0]
            y_e = self.mesh['ele_tri'][:, 1]
            z_e = self.mesh['ele_tri'][:, 2]

        # fig = plt.figure(figsize=plt.figaspect(0.5))
        # ax = fig.add_subplot(1, 2, 1, projection='3d')

        # DD = np.argwhere(self.mesh['value_tri_elems']==10).reshape(-1)
        # tri_DD = tri[DD, :]

        # for i in range(0, len(tri_DD)):
        #     czw = np.block([tri_DD[i, :], tri_DD[i, 0]]).reshape(-1)
        #     ax.plot(x[czw], y[czw], z[czw])
        #     # input('enter')
        #     print(np.str(i))

        fig = go.Figure(data=[
            go.Mesh3d(
                # vertices of a cube
                # colorscale=[[0, 'gold'],
                #             [0.5, 'mediumturquoise'],
                #             [1, 'magenta']],
                x=x, y=y, z=z,
                i=i, j=j, k=k,
                facecolor=self.mesh['value_tri_elems'],
                intensity=self.mesh['value_tri_elems'],
                intensitymode='cell',
                opacity=0.1
            )
        ])

        if (colormap is not None): fig.data[0]['colorscale'] = colormap

        if (middle_value is not None): fig.data[0]['cmid'] = middle_value

        if self.shape_ele == 'surface':
            fig.add_trace(go.Mesh3d(
                # colorscale=[[0, 'gold'],
                #             [0.5, 'mediumturquoise'],
                #             [1, 'magenta']],
                x=x, y=y, z=z,
                i=e_i, j=e_j, k=e_k,
                # facecolor=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
                # intensity=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
            )
            )

        elif self.shape_ele == 'line':
            normalizer = matplotlib.colors.Normalize(vmin=1, vmax=self.n_electrode)
            mapper = matplotlib.cm.ScalarMappable(norm=normalizer, cmap='Greens')
            E_indices = np.arange(self.n_electrode)
            E_color = np.linspace(0, 16, 16) * 1000
            E_color = np.repeat(E_color, L_ele)
            for k in range(len(x_e1)):
                fig.add_trace(go.Scatter3d(
                    # colorscale=[[0, 'gold'],
                    #             [0.5, 'mediumturquoise'],
                    #             [1, 'magenta']],
                    x=[x_e1[k], x_e2[k]], y=[y_e1[k], y_e2[k]], z=[z_e1[k], z_e2[k]],
                    mode='lines',
                    marker=dict(
                        color=E_color[k],
                        colorscale='Viridis',
                        line_width=20
                    )

                    # facecolor=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
                    # intensity=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
                )
                )

        else:
            fig.add_trace(go.Scatter3d(
                # colorscale=[[0, 'gold'],
                #             [0.5, 'mediumturquoise'],
                #             [1, 'magenta']],
                x=x_e, y=y_e, z=z_e,
                mode='markers',
                # facecolor=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
                # intensity=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
            )
            )

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
        scene = dict(camera=dict(eye=dict(x=1.25, y=1.25, z=1.25)),  # the default values are 1.25, 1.25, 1.25
                     xaxis=dict(),
                     yaxis=dict(),
                     zaxis=dict(),
                     aspectmode='data',  # this string can be 'data', 'cube', 'auto', 'manual'
                     # a custom aspectratio is defined as follows:
                     aspectratio=dict(x=1, y=1, z=0.95)
                     )

        fig.update_layout(scene=scene)
        fig.update_layout(showlegend=False)
        # fig.show()

        return fig

    @wrapper
    def display_tetrahedrons(self, reference_level, distribution=None, threshold=None, colormap='bwr',
                             show_electrode_numbers=False, use_FXAA=False):

        """
        Example - render finite element mesh, write image to png file and show window:

        figure = eit_3D.display_tetrahedrons( 1.0, show_electrode_numbers = True, use_FXAA = True )

        figure.screenshot( filename = 'tetrahedrons.png', scale = 4, returnNumpy = False )

        figure.show( interactive = True ) """

        boundary = vedo.Mesh([self.nodes, self.boundary], alpha=0.1)

        # boundary.lineColor(lc='black')

        boundary.lineWidth(lw=1.0)

        if (distribution is None): distribution = self.value_elems.copy()

        if (distribution.size != self.elems.shape[0]): raise Exception(
            "Number of elements in array 'distribution' is not appropriate.")

        if (np.iscomplexobj(distribution) == True): raise TypeError(
            "Array 'distribution' is complex. Select real or imaginary part.")

        distribution = distribution.flatten()

        distribution_min = np.min(distribution)
        distribution_max = np.max(distribution)

        if (distribution_min != distribution_max):

            if (threshold is None): threshold = 0.08 * (distribution_max - distribution_min)

            delta = np.abs(distribution - reference_level)

            finite_element_is_visible = np.logical_not(delta < threshold)

            D = distribution[finite_element_is_visible].copy()

            if (D.size > 0):

                T = self.elems[finite_element_is_visible, :].copy()

                B, I = Image_EIT_3D_tetra.determine_boundary_elements(T)

                tetrahedrons = vedo.Mesh([self.nodes, B], alpha=1.0)

                tetrahedrons.lineWidth(lw=0.5)

                delta_max = np.max(delta)

                interval = [reference_level - delta_max, reference_level + delta_max]

                tetrahedrons.cmap(colormap, input_array=D[I], on='cells', vmin=interval[0],
                                  vmax=interval[1]).addScalarBar3D()

            else:
                tetrahedrons = None

        else:
            tetrahedrons = None

        electrodes_type = self.shape_ele

        if (any([electrodes_type == S for S in ['point', 'line', 'surface']]) == False): raise Exception(
            'Unknown type of electrodes.')

        if (electrodes_type == 'surface'):
            electrodes = self.electrodes[0]

        else:
            electrodes = self.electrodes

        E_x = np.array([self.nodes[nodes, 0].mean() for nodes in electrodes])
        E_y = np.array([self.nodes[nodes, 1].mean() for nodes in electrodes])
        E_z = np.array([self.nodes[nodes, 2].mean() for nodes in electrodes])

        E_xyz = np.column_stack((E_x, E_y, E_z))

        normalizer = matplotlib.colors.Normalize(vmin=1, vmax=len(electrodes))

        mapper = matplotlib.cm.ScalarMappable(norm=normalizer, cmap='Greens')

        E_indices = np.arange(len(electrodes))

        E_color = 255.0 * mapper.to_rgba(E_indices + 1)

        if (electrodes_type == 'point'):

            electrodes_0D = vedo.Points(E_xyz, r=10, c=E_color)

            electrodes_1D = []
            electrodes_2D = []

        elif (electrodes_type == 'line'):

            electrodes_0D = None

            electrodes_1D = [vedo.Lines(self.nodes[E[:, 0]], endPoints=self.nodes[E[:, 1]], c=C, lw=5) for E, C in
                             zip(self.electrodes_line_segments, E_color[:, 0: -1])]

            electrodes_2D = []

        elif (electrodes_type == 'surface'):

            electrodes_0D = None

            electrodes_1D = []

            electrodes_2D = [vedo.Mesh([self.nodes, self.boundary[E, :]], c=C, alpha=0.7) for E, C in
                             zip(self.electrodes[1], E_color[:, 0: -1])]

        if (show_electrode_numbers == True):

            text_3D = [vedo.Text3D(str(index + 1), E_xyz[index], c='black', alpha=1.0) for index in E_indices]

            multiplier = boundary.diagonalSize() / (70.0 * text_3D[0].diagonalSize())

            [electrode_index.scale(multiplier) for electrode_index in text_3D]

        else:
            text_3D = []

        actors_3D = [boundary, tetrahedrons, electrodes_0D] + electrodes_1D + electrodes_2D + text_3D

        vedo.settings.useFXAA = use_FXAA

        default_parameters = { 'roll': -75.0, 'azimuth': 50.0, 'elevation': -20.0, 'axes': True, 'interactive': False, 'new': True, 'offscreen': True }

        figure = vedo.show(actors_3D, **default_parameters)

        figure.default_parameters = default_parameters

        if (tetrahedrons is not None):
            L_x = figure.axes_instances[0].GetXRange()[1] - figure.axes_instances[0].GetXRange()[0]
            L_y = figure.axes_instances[0].GetYRange()[1] - figure.axes_instances[0].GetYRange()[0]

            # colorbar_scale = 0.9 * L_y / figure.scalarbars[0].GetLength()

            colorbar_x = figure.axes_instances[0].GetXRange()[1] + 0.05 * L_x
            colorbar_y = figure.axes_instances[0].GetYRange()[0] + 0.53 * L_y
            colorbar_z = figure.axes_instances[0].GetZRange()[0]

            # figure.scalarbars[0].scale(colorbar_scale).x(colorbar_x).y(colorbar_y).z(colorbar_z)

        return figure

    @wrapper
    def build_slice(self, axis, value):
        n_elems = len(self.elems)
        # middle = self.mesh['middle']
        if axis == 0:
            x = self.nodes[self.elems, 0]
            distSign = np.sign(x - value)
        elif axis == 1:
            y = self.nodes[self.elems, 1]
            distSign = np.sign(y - value)
        else:
            z = self.nodes[self.elems, 2]
            distSign = np.sign(z - value)
        value_in_elem = np.array([(1 if all([len(np.argwhere(distSign[x, :] == 1)) >= 1,
                                             len(np.argwhere(distSign[x, :] == -1)) >= 1])
                                   else 0) for x in range(0, n_elems)])
        ind_elem_with_value = np.argwhere(value_in_elem == 1)

        if (ind_elem_with_value.size == 0): return None

        value_elem_with_value = []
        n_nodes = []
        n_elems = []
        i = 0
        for x in ind_elem_with_value:
            sign = distSign[x, :].reshape(-1)
            elem_x = self.elems[x, :].reshape(-1)
            sign_plus = np.argwhere(sign == 1).reshape(-1)
            sign_min = np.argwhere(sign <= 0).reshape(-1)
            if len(sign_plus) == 3:
                A = self.nodes[elem_x[sign_min], :]
                A = np.tile(A, 3).reshape(3, 3)
                B = self.nodes[elem_x[sign_plus], :]
            elif len(sign_min) == 3:
                A = self.nodes[elem_x[sign_min], :]
                B = self.nodes[elem_x[sign_plus], :]
                B = np.tile(B, 3).reshape(3, 3)
            else:
                A = self.nodes[elem_x[sign_min], :]
                B = self.nodes[elem_x[sign_plus], :]
                A = np.tile(A, 2).reshape(4, 3)
                B = np.tile(B.T, 2).T.reshape(4, 3)

            k = A - B
            if len(A) == 3:
                if axis == 0:
                    t = (value - A[:, 0]) / k[:, 0]
                    x_e = value * np.ones([3, 1]).reshape(-1)
                    y_e = A[:, 1] + t * k[:, 1]
                    z_e = A[:, 2] + t * k[:, 2]
                elif axis == 1:
                    t = (value - A[:, 1]) / k[:, 1]
                    y_e = value * np.ones([3, 1]).reshape(-1)
                    x_e = A[:, 0] + t * k[:, 0]
                    z_e = A[:, 2] + t * k[:, 2]
                else:
                    t = (value - A[:, 2]) / k[:, 2]
                    z_e = value * np.ones([3, 1]).reshape(-1)
                    x_e = A[:, 0] + t * k[:, 0]
                    y_e = A[:, 1] + t * k[:, 1]
                n_nodes.append(np.row_stack([x_e, y_e, z_e]).T)
                n_elems.append(np.r_[i:i + 3])
                value_elem_with_value.append(self.value_elems[x])
                i += 3
            else:
                if axis == 0:
                    t = (value - A[:, 0]) / k[:, 0]
                    x_e = value * np.ones([4, 1]).reshape(-1)
                    y_e = A[:, 1] + t * k[:, 1]
                    z_e = A[:, 2] + t * k[:, 2]
                elif axis == 1:
                    t = (value - A[:, 1]) / k[:, 1]
                    y_e = value * np.ones([4, 1]).reshape(-1)
                    x_e = A[:, 0] + t * k[:, 0]
                    z_e = A[:, 2] + t * k[:, 2]
                else:
                    t = (value - A[:, 2]) / k[:, 2]
                    z_e = value * np.ones([4, 1]).reshape(-1)
                    x_e = A[:, 0] + t * k[:, 0]
                    y_e = A[:, 1] + t * k[:, 1]
                n_nodes.append(np.row_stack([x_e, y_e, z_e]).T)
                n_elems.append([i, i + 1, i + 3])
                n_elems.append([i, 3 + i, 2 + i])
                value_elem_with_value.append(self.value_elems[x])
                value_elem_with_value.append(self.value_elems[x])
                i += 4
        n_nodes_array = np.asarray(list(itertools.chain(*n_nodes)))
        n_elems_array = np.array(n_elems)
        value_elem_with_value = np.array(value_elem_with_value)
        n_nodes_unique, index, index0 = np.unique(n_nodes_array, axis=0, return_inverse=True, return_index=True)
        n_elems_unique = index0[n_elems_array]
        return n_nodes_unique, n_elems_unique, value_elem_with_value

    @wrapper
    def display_slice(self, axis=0, value=0.0, colormap=None, middle_value=None):

        if np.isscalar(axis): axis = np.array([axis])

        if np.isscalar(value): value = np.array([value])

        W = [e for a, v in zip(axis, value) if (e := self.build_slice(a, v)) is not None]

        if (len(W) == 0): return None

        N = np.cumsum(np.array([0] + [e[0].shape[0] for e in W[0: -1]]))

        nodes = np.vstack([e[0] for e in W])

        elements = np.vstack([e[1] + n for e, n in zip(W, N)])

        distribution = np.vstack([e[2] for e in W])

        mesh = dict(
            zip(['x', 'y', 'z', 'i', 'j', 'k'], [C.flatten() for C in np.hsplit(nodes, 3) + np.hsplit(elements, 3)]))

        figure = go.Figure(data=[
            go.Mesh3d(**mesh, intensity=distribution, intensitymode='cell', opacity=0.8, lighting={'diffuse': 0.0})])

        if (colormap is not None): figure.data[0]['colorscale'] = colormap

        if (middle_value is not None): figure.data[0]['cmid'] = middle_value

        if self.shape_ele == 'surface':

            e_i = self.mesh['ele_tri'][:, 0]
            e_j = self.mesh['ele_tri'][:, 1]
            e_k = self.mesh['ele_tri'][:, 2]

            figure.add_trace(go.Mesh3d(
                # colorscale=[[0, 'gold'],
                #             [0.5, 'mediumturquoise'],
                #             [1, 'magenta']],
                x=self.nodes[:, 0], y=self.nodes[:, 1], z=self.nodes[:, 2],
                i=e_i, j=e_j, k=e_k,
                # facecolor=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
                # intensity=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
            )
            )

        elif self.shape_ele == 'line':
            pass

        else:
            x_ele = self.mesh['ele_tri'][:, 0]
            y_ele = self.mesh['ele_tri'][:, 1]
            z_ele = self.mesh['ele_tri'][:, 2]

            figure.add_trace(go.Scatter3d(
                # colorscale=[[0, 'gold'],
                #             [0.5, 'mediumturquoise'],
                #             [1, 'magenta']],
                x=x_ele, y=y_ele, z=z_ele,
                mode='markers',
                marker=dict(
                    size=6,
                    color=np.r_[0:len(x_ele)],  # set color to an array/list of desired values
                    colorscale='Viridis',  # choose a colorscale
                    opacity=0.8
                )
                # facecolor=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
                # intensity=np.ones_like(e_i)*self.mesh['value_tri_elems'].min(),
            )
            )

        figure.update_layout(margin=dict(l=0, r=0, b=0, t=0))

        # figure.show( )

        return figure, W

    @wrapper
    def up_grade_value_elems(self, value):

        self.value_elems = value
        n_elems = len(self.elems)
        K = np.tile(np.r_[0:n_elems], 4)
        value_tri = value[K]
        const_error_num = np.abs(np.ceil(np.log10(self.V_elems.min()))) + 1
        V_tri = np.int64(self.V_elems[K] * 10 ** const_error_num)
        ind = self.mesh['ind']
        Sum = np.sum(V_tri[ind], axis=1)

        value_tri_N = np.array([np.sum(V_tri[ind[x]] / Sum[x] * value_tri[ind[x]])
                                for x in range(len(Sum))])

        # D = self.mesh['dict_caunt_surfaces']
        # ind = self.mesh['ind']
        #
        # tri_unique = self.mesh['surface_unique']
        # index = self.mesh['index']

        # value_elems_tri = np.zeros([len(index)])
        # i = 0
        # for idx in range(0, len(ind)):
        #     value = np.sum((np.sum(V_tri[ind[idx, :]]) - V_tri[ind[idx, :]])*value_tri[ind[idx, :]])\
        #             /np.sum(V_tri[ind[idx, :]])
        #     value_elems_tri[i] = value
        #     i += 1
        self.mesh['value_tri_elems'] = value_tri_N

    @wrapper
    def state_matrix_point(self):
        elems = self.elems
        N_elems = len(elems)

        ind1 = elems[:, 0].reshape(-1)
        ind2 = elems[:, 1].reshape(-1)
        ind3 = elems[:, 2].reshape(-1)
        ind4 = elems[:, 3].reshape(-1)

        X = self.nodes[:, 0].reshape(-1)
        Y = self.nodes[:, 1].reshape(-1)
        Z = self.nodes[:, 2].reshape(-1)
        N_nodes = len(X)

        x1 = X[ind1].reshape(-1)
        x2 = X[ind2].reshape(-1)
        x3 = X[ind3].reshape(-1)
        x4 = X[ind4].reshape(-1)

        y1 = Y[ind1].reshape(-1)
        y2 = Y[ind2].reshape(-1)
        y3 = Y[ind3].reshape(-1)
        y4 = Y[ind4].reshape(-1)

        z1 = Z[ind1].reshape(-1)
        z2 = Z[ind2].reshape(-1)
        z3 = Z[ind3].reshape(-1)
        z4 = Z[ind4].reshape(-1)

        J_11 = x1 - x4
        J_12 = x2 - x4
        J_13 = x3 - x4

        J_21 = y1 - y4
        J_22 = y2 - y4
        J_23 = y3 - y4

        J_31 = z1 - z4
        J_32 = z2 - z4
        J_33 = z3 - z4

        detJ = np.zeros(N_elems)
        invJ = []
        for x in range(N_elems):
            J = np.array([[J_11[x], J_21[x], J_31[x]],
                          [J_12[x], J_22[x], J_32[x]],
                          [J_13[x], J_23[x], J_33[x]]])
            detJ[x] = np.linalg.det(J)
            invJ.append(np.linalg.inv(J))

        value = detJ * self.value_elems / 12
        K_1 = np.zeros(N_elems)
        K_2 = np.zeros(N_elems)
        K_3 = np.zeros(N_elems)
        k_12 = np.zeros(N_elems)
        k_13 = np.zeros(N_elems)
        k_23 = np.zeros(N_elems)
        for i, x in enumerate(invJ):
            K_1[i] = (x[0, 0] ** 2 + x[1, 0] ** 2 + x[2, 0] ** 2) * value[i]
            K_2[i] = (x[0, 1] ** 2 + x[1, 1] ** 2 + x[2, 1] ** 2) * value[i]
            K_3[i] = (x[0, 2] ** 2 + x[1, 2] ** 2 + x[2, 2] ** 2) * value[i]

            k_12[i] = (x[0, 0] * x[0, 1] + x[1, 0] * x[1, 1] + x[2, 0] * x[2, 1]) * 2 * value[i]
            k_13[i] = (x[0, 0] * x[0, 2] + x[1, 0] * x[1, 2] + x[2, 0] * x[2, 2]) * 2 * value[i]

            k_23[i] = (x[0, 2] * x[0, 1] + x[1, 2] * x[1, 1] + x[2, 2] * x[2, 1]) * 2 * value[i]
        k_14 = -2 * K_1 - k_12 - k_13

        k_24 = -2 * K_2 - k_12 - k_23

        k_34 = -2 * K_3 - k_13 - k_23

        K_4 = 0.5 * (-1 * k_14 - k_24 - k_34)

        H = sp.csc_matrix((N_nodes, N_nodes))
        H += sp.csc_matrix((K_1, (ind1, ind1)), shape=(N_nodes, N_nodes))
        H += sp.csc_matrix((K_2, (ind2, ind2)), shape=(N_nodes, N_nodes))
        H += sp.csc_matrix((K_3, (ind3, ind3)), shape=(N_nodes, N_nodes))

        H += sp.csc_matrix((k_12, (ind1, ind2)), shape=(N_nodes, N_nodes))
        H += sp.csc_matrix((k_13, (ind1, ind3)), shape=(N_nodes, N_nodes))
        H += sp.csc_matrix((k_14, (ind1, ind4)), shape=(N_nodes, N_nodes))

        H += sp.csc_matrix((k_23, (ind2, ind3)), shape=(N_nodes, N_nodes))
        H += sp.csc_matrix((k_24, (ind2, ind4)), shape=(N_nodes, N_nodes))

        H += sp.csc_matrix((k_34, (ind3, ind4)), shape=(N_nodes, N_nodes))

        H += sp.csc_matrix((K_4, (ind4, ind4)), shape=(N_nodes, N_nodes))

        H += H.T

        self.State_matrix_points = H
        self.jacobians = invJ
        self.detJ = detJ

    @wrapper
    def state_matrix_surface(self):
        electrode_elems = self.electrodes[1]
        elems = self.boundary

        X = self.nodes[:, 0].reshape(-1)
        Y = self.nodes[:, 1].reshape(-1)
        Z = self.nodes[:, 2].reshape(-1)
        N_nodes = len(X)

        N_electrodes = len(electrode_elems)
        S = (N_nodes + N_electrodes, N_nodes + N_electrodes)
        H = sp.csr_matrix(S)
        z_l = self.stim['z_contact']

        for e in range(0, N_electrodes):

            elems_e = elems[electrode_elems[e], :]
            if len(elems_e.shape) == 1:
                e_1 = elems_e[0]
                e_2 = elems_e[1]
                e_3 = elems_e[2]

                x_1 = X[e_1]
                x_2 = X[e_2]
                x_3 = X[e_3]

                y_1 = Y[e_1]
                y_2 = Y[e_2]
                y_3 = Y[e_3]

                z_1 = Z[e_1]
                z_2 = Z[e_2]
                z_3 = Z[e_3]

                vec1 = np.ones([1])

                J_11 = x_1 - x_3
                J_21 = x_2 - x_3
                J_12 = y_1 - y_3
                J_22 = y_2 - y_3
                J_13 = z_1 - z_3
                J_23 = z_2 - z_3

                J_xyz = np.sqrt((J_12 * J_23 - J_22 * J_13) ** 2 +
                                (J_11 * J_23 - J_21 * J_13) ** 2 +
                                (J_11 * J_22 - J_21 * J_12) ** 2)

                J_xyz_3 = J_xyz / (-6 * z_l[e]) * vec1

                J_xyz_12 = J_xyz / (24 * z_l[e]) * vec1

                H += sp.csc_matrix((J_xyz_12, (e_1 * vec1, e_1 * vec1)), shape=S)
                H += sp.csc_matrix((J_xyz_12, (e_2 * vec1, e_2 * vec1)), shape=S)
                H += sp.csc_matrix((J_xyz_12, (e_3 * vec1, e_3 * vec1)), shape=S)

                H += sp.csc_matrix((J_xyz_3, (e_1 * vec1, N_nodes * vec1 + e)), shape=S)
                H += sp.csc_matrix((J_xyz_3, (e_2 * vec1, N_nodes * vec1 + e)), shape=S)
                H += sp.csc_matrix((J_xyz_3, (e_3 * vec1, N_nodes * vec1 + e)), shape=S)

                H += sp.csc_matrix((J_xyz_12, (e_1 * vec1, e_2 * vec1)), shape=S)
                H += sp.csc_matrix((J_xyz_12, (e_1 * vec1, e_3 * vec1)), shape=S)
                H += sp.csc_matrix((J_xyz_12, (e_3 * vec1, e_2 * vec1)), shape=S)

                # pochodna po U_l

                P = 0.25 * np.sum(J_xyz) / z_l[e]
                H += sp.csc_matrix((P * vec1, (N_nodes * vec1 + e, N_nodes * vec1 + e)),
                                   shape=S)
            else:
                e_1 = elems_e[:, 0].reshape(-1)
                e_2 = elems_e[:, 1].reshape(-1)
                e_3 = elems_e[:, 2].reshape(-1)

                x_1 = X[e_1]
                x_2 = X[e_2]
                x_3 = X[e_3]

                y_1 = Y[e_1]
                y_2 = Y[e_2]
                y_3 = Y[e_3]

                z_1 = Z[e_1]
                z_2 = Z[e_2]
                z_3 = Z[e_3]

                vec1 = np.ones_like(x_1)

                J_11 = x_1 - x_3
                J_21 = x_2 - x_3
                J_12 = y_1 - y_3
                J_22 = y_2 - y_3
                J_13 = z_1 - z_3
                J_23 = z_2 - z_3

                J_xyz = np.array([np.sqrt((J_12[x] * J_23[x] - J_22[x] * J_13[x]) ** 2 +
                                          (J_11[x] * J_23[x] - J_21[x] * J_13[x]) ** 2 +
                                          (J_11[x] * J_22[x] - J_21[x] * J_12[x]) ** 2) for x in range(0, len(x_1))])

                J_xyz_3 = J_xyz / (-6 * z_l[e])

                J_xyz_12 = J_xyz / (24 * z_l[e])

                H += sp.csc_matrix((J_xyz_12, (e_1, e_1)), shape=S)
                H += sp.csc_matrix((J_xyz_12, (e_2, e_2)), shape=S)
                H += sp.csc_matrix((J_xyz_12, (e_3, e_3)), shape=S)

                H += sp.csc_matrix((J_xyz_3, (e_1, N_nodes * vec1 + e)), shape=S)
                H += sp.csc_matrix((J_xyz_3, (e_2, N_nodes * vec1 + e)), shape=S)
                H += sp.csc_matrix((J_xyz_3, (e_3, N_nodes * vec1 + e)), shape=S)

                H += sp.csc_matrix((J_xyz_12, (e_1, e_2)), shape=S)
                H += sp.csc_matrix((J_xyz_12, (e_1, e_3)), shape=S)
                H += sp.csc_matrix((J_xyz_12, (e_3, e_2)), shape=S)

                # pochodna po U_l

                P = 0.25 * np.sum(J_xyz) / z_l[e]
                H += sp.csc_matrix((P * np.ones([1]), (N_nodes * np.ones([1]) + e, N_nodes * np.ones([1]) + e)),
                                   shape=S)
        H += H.T
        self.State_matrix_surface = H

    @wrapper
    def state_matrix_line(self):
        # nie działa skorzystaj z zmiennej electrodes_line_segments
        n_nodes = self.nodes.shape[0]
        n_electrode = len(self.electrodes)
        # n_elems = self.elems.shape[0]
        x = self.nodes[:, 0].reshape(-1)
        y = self.nodes[:, 1].reshape(-1)
        z = self.nodes[:, 2].reshape(-1)
        H = sp.csc_matrix((n_nodes + n_electrode, n_nodes + n_electrode))
        z_l = self.stim['z_contact']

        L_electrode = np.array([len(x) for x in self.electrodes_line_segments])
        L_cumsum = np.block([0, np.cumsum(L_electrode)]).reshape(-1)

        electrodes_line_segments = np.row_stack(self.electrodes_line_segments)

        e1 = electrodes_line_segments[:, 0].reshape(-1)
        e2 = electrodes_line_segments[:, 1].reshape(-1)

        J_xyz = np.sqrt(
            (x[e1] - x[e2]) ** 2 +
            (y[e1] - y[e2]) ** 2 +
            (z[e1] - z[e2]) ** 2
        )
        z_l = np.repeat(z_l, L_electrode)
        value_1 = np.r_[0:self.n_electrode].reshape(-1)
        value = np.repeat(value_1, L_electrode).reshape(-1)

        J3 = 1 / (6 * z_l) * J_xyz
        J6 = 1 / (6 * z_l) * J_xyz
        J2 = - 1 / (2 * z_l) * J_xyz

        D = np.array([-1 * np.sum(J2[L_cumsum[x]:L_cumsum[x + 1]]) for x in range(self.n_electrode)]).reshape(-1)

        H += sp.csc_matrix((J3, (e1, e1)), shape=H.shape) + sp.csc_matrix((J3, (e2, e2)), shape=H.shape) + \
             sp.csc_matrix((J6, (e1, e2)), shape=H.shape) + \
             sp.csc_matrix((J2, (e1, n_nodes + value)), shape=H.shape) + \
             sp.csc_matrix((J2, (e2, n_nodes + value)), shape=H.shape)
        # pochodna po U_l
        H += sp.csc_matrix((D, (n_nodes + value_1, n_nodes + value_1)),
                           shape=H.shape)
        H += H.T

        self.State_matrix_line = H

    @wrapper
    def state_matrix(self):
        if self.shape_ele == 'point':
            self.state_matrix_point()
            self.State_matrix = self.State_matrix_points
        elif self.shape_ele == 'surface':
            self.state_matrix_point()
            self.state_matrix_surface()
            H_point = self.State_matrix_points
            H_surface = self.State_matrix_surface

            H = H_surface.copy()
            ind_NN = H_point.nonzero()
            H += sp.csc_matrix((H_point.data, (ind_NN[0], ind_NN[1])), shape=H.shape)
            # H[0:N, 0:N] = H_NN
            self.State_matrix = H
        elif self.shape_ele == 'line':
            self.state_matrix_point()
            self.state_matrix_line()
            H_point = self.State_matrix_points
            H_line = self.State_matrix_line

            H = H_line.copy()
            ind_NN = H_point.nonzero()
            H += sp.csc_matrix((H_point.data, (ind_NN[0], ind_NN[1])), shape=H.shape)
            # H[0:N, 0:N] = H_NN
            self.State_matrix = H

    @wrapper
    def get_stim_pattern(self, stim_structure):

        values = ['stim_pattern', 'meas_pattern', 'z_contact']
        values2 = ['n_electrodes', 'd_stim', 'd_meas', 'amp', 'z_contact']
        if all(np.array([i == k for i, k in zip(stim_structure.keys(), values)])):
            for k in stim_structure.keys():
                self.stim[k] = stim_structure[k]
        elif all(np.array([i == k for i, k in zip(stim_structure.keys(), values2)])):
            self.stim = stim_pattern(stim_structure)

    @wrapper
    def sources_for_adjoint_fields_PSI(self):

        meas_pattern = np.transpose(sp.vstack(self.stim['meas_pattern']))

        meas_pattern_UC, ind_ununique = np.unique(meas_pattern.toarray(), axis=1, return_inverse=True)

        meas_pattern_UC = sp.csr_matrix(meas_pattern_UC)

        if self.shape_ele == 'point':

            electrodes_0D = np.array(self.electrodes).reshape(-1)

            indices_E, indices_PA, currents = sp.find(meas_pattern_UC)

            nodes_E = electrodes_0D[indices_E]

            sources_AF = sp.csc_matrix((currents, (nodes_E, indices_PA)),
                                       shape=(self.nodes.shape[0], meas_pattern_UC.shape[1]))

        else:  # wersja dla elektrod niepunktowych

            sources_AF = sp.csc_matrix(
                sp.vstack([sp.csr_matrix((self.nodes.shape[0], meas_pattern_UC.shape[1])),
                           meas_pattern_UC]))

        self.ind_ununique = ind_ununique

        return sources_AF

    @wrapper
    def potential(self, sources_AF=None):

        n_nodes = self.nodes.shape[0]

        n_stim = len(self.stim['stim_pattern'])

        stim_pattern = []

        for I in self.stim['stim_pattern']:

            if sp.issparse(I):
                stim_pattern.append(I.toarray())

            else:
                stim_pattern.append(I)

        stim_pattern = np.transpose(np.vstack([I.reshape(1, -1) for I in stim_pattern]))

        if self.shape_ele == 'point':

            electrodes_0D = np.array(self.electrodes).reshape(-1)

            indices = np.argwhere(stim_pattern != 0)

            indices_E = indices[:, 0]

            nodes_E = electrodes_0D[indices_E]

            indices_PA = indices[:, 1]

            currents = np.array(stim_pattern[indices_E, indices_PA]).flatten()

            sources_EP = sp.csc_matrix((currents, (nodes_E, indices_PA)), shape=(n_nodes, n_stim))

            rows_E = electrodes_0D

        else:  # wersja dla elektrod niepunktowych

            sources_EP = sp.csc_matrix(sp.vstack([sp.csr_matrix((n_nodes, n_stim)), stim_pattern]))

            rows_E = range(n_nodes, n_nodes + self.n_electrode)

        if (sources_AF is not None):
            sources = sp.hstack([sources_EP, sources_AF])

        else:
            sources = sources_EP

        H = self.State_matrix.tocoo()

        N_max = H.shape[0] - 1

        select_data = np.logical_and(H.row != N_max, H.col != N_max)

        H_reduced = sp.csc_matrix((H.data[select_data], (H.row[select_data], H.col[select_data])),
                                  shape=(N_max, N_max))

        sources = sources.tocoo()

        select_rows = (sources.row != N_max)

        sources_reduced = sp.csc_matrix(
            (sources.data[select_rows], (sources.row[select_rows], sources.col[select_rows])),
            shape=(N_max, sources.shape[1]))

        scalar_fields_reduced = spsolve(H_reduced, sources_reduced).toarray()

        ground = np.zeros((1, sources_reduced.shape[1]), dtype=np.float_)

        scalar_fields = np.vstack((scalar_fields_reduced, ground))

        residues = H @ scalar_fields - sources

        factors = 1.0 / sp.linalg.norm(sources, axis=0)

        factors[np.isinf(factors)] = 1.0

        relative_errors = factors * np.linalg.norm(residues, axis=0)

        if np.any( relative_errors > 1.0E-9 ): raise Exception( 'The solution of a system of linear equations is not accurate.' )

        U = np.reshape(scalar_fields[np.ix_(rows_E, range(n_stim))], -1, order='F')

        self.sources_for_scalar_fields = sources

        self.Potential = scalar_fields

        self.U = U

    @wrapper
    def simulation(self, sources_AF=None):
        self.state_matrix()
        self.potential(sources_AF=sources_AF)
        meas_pattern_pom = self.stim["meas_pattern"]
        U = self.U
        V = sp.block_diag(meas_pattern_pom) @ U
        return V

    @wrapper
    def change_ms_inv(self, method='kotre', lamb=None, p=0.5, RtR=None):
        """
        Pseudo odwrotność macierzy wrażliwości:
            H = (MS.T*MS + lamb*R)^(-1) * MS.T
        Parametry
        ----------
        p, lamb: float
            parametry regularyzacji
        method: str, optional
            metoda wyznaczania pseudoodwrotnej macierzy
        Wartości
        -------
        H: NDArray
            pseudo odwrotność macierzy MS
        """
        j_w_j = np.dot(self.MS.transpose(), self.MS)
        if RtR is None:
            if lamb is None:
                if method == 'kotre':
                    lamb = 1e-4
                if method == 'lm':
                    lamb = 1
                if method == 'dg':
                    lamb = 1e-8

            if method == 'kotre':
                # see adler-dai-lionheart-2007
                # p=0   : noise distribute on the boundary ('dgn')
                # p=0.5 : noise distribute on the middle
                # p=1   : noise distribute on the center ('lm')
                RtR = np.diag(np.diag(j_w_j)) ** p
            elif method == 'lm':
                # Marquardt–Levenberg, 'lm' for short
                # or can be called NOSER, DLS
                RtR = np.diag(np.diag(j_w_j))
            else:
                # Damped Gauss Newton, 'dgn' for short
                RtR = np.eye(self.MS.shape[1])
        else:
            assert (RtR.shape == np.array([len(self.elems), len(self.elems)])).all(), \
                'Niewłaściwy rozmiar macierzy regularyzacji.'
            if lamb is None:
                lamb = 1e-4

        # build H
        h_mat = np.dot(np.linalg.inv(j_w_j + lamb * RtR), self.MS.transpose())

        self.MS_inv = h_mat
        self.method = method
        self.lamb = lamb
        self.p = p
        self.RtR = RtR

    @wrapper
    def orthogonalization_voltages(self, V0, V1):
        a = np.dot(V1, V0) / np.dot(V0, V0)
        dv = (V1 - a * V0)
        self.dv = dv
        return dv

    @wrapper
    def matrix_of_sensitivity(self, decomp_svd=False):

        stim_pattern_pom = self.stim["stim_pattern"]

        I = np.max(stim_pattern_pom[0])
        n_stim = len(stim_pattern_pom)
        n_meas = np.size(self.stim["meas_pattern"][0], axis=0)

        # indeksy nodów elementów czworościannych
        ind_1 = self.elems[:, 0]
        ind_2 = self.elems[:, 1]
        ind_3 = self.elems[:, 2]
        ind_4 = self.elems[:, 3]
        # potencjał na węzłach dla wzorców pomiarowych i stymulacyjnych
        P = self.Potential
        # odwrotna macierz jakobiego
        J = self.jacobians
        J_a = np.array(J)

        P1 = P[ind_1, :].T
        P2 = P[ind_2, :].T
        P3 = P[ind_3, :].T

        fi_n_4 = P[ind_4, 0:n_stim]
        psi_m_4 = P[ind_4, n_stim:]

        ind = np.r_[0:n_stim]  # np.int32(np.linspace(0, n_stim - 1, n_stim))
        i_meas = np.repeat(ind, n_meas)

        fi_rep_4 = fi_n_4[:, i_meas].T

        i_steam = self.ind_ununique

        psi_rep_4 = psi_m_4[:, i_steam].T

        P1_J_k1 = P1[:, :, np.newaxis] * J_a[:, :, 0]
        P2_J_k2 = P2[:, :, np.newaxis] * J_a[:, :, 1]
        P3_J_k3 = P3[:, :, np.newaxis] * J_a[:, :, 2]

        fi_1_J_k1 = P1_J_k1[0:n_stim, :, :]
        fi_2_J_k2 = P2_J_k2[0:n_stim, :, :]
        fi_3_J_k3 = P3_J_k3[0:n_stim, :, :]

        psi_1_J_k1 = P1_J_k1[n_stim:, :, :]
        psi_2_J_k2 = P2_J_k2[n_stim:, :, :]
        psi_3_J_k3 = P3_J_k3[n_stim:, :, :]

        # sumy
        fi_J_1 = fi_1_J_k1[:, :, 0] + fi_2_J_k2[:, :, 0] + fi_3_J_k3[:, :, 0]
        fi_J_2 = fi_1_J_k1[:, :, 1] + fi_2_J_k2[:, :, 1] + fi_3_J_k3[:, :, 1]
        fi_J_3 = fi_1_J_k1[:, :, 2] + fi_2_J_k2[:, :, 2] + fi_3_J_k3[:, :, 2]

        fi_rep_J_1 = fi_J_1[i_meas, :]
        fi_rep_J_2 = fi_J_2[i_meas, :]
        fi_rep_J_3 = fi_J_3[i_meas, :]

        psi_J_1 = psi_1_J_k1[:, :, 0] + psi_2_J_k2[:, :, 0] + psi_3_J_k3[:, :, 0]
        psi_J_2 = psi_1_J_k1[:, :, 1] + psi_2_J_k2[:, :, 1] + psi_3_J_k3[:, :, 1]
        psi_J_3 = psi_1_J_k1[:, :, 2] + psi_2_J_k2[:, :, 2] + psi_3_J_k3[:, :, 2]

        psi_rep_J_1 = psi_J_1[i_steam, :]
        psi_rep_J_2 = psi_J_2[i_steam, :]
        psi_rep_J_3 = psi_J_3[i_steam, :]

        J_sum_row = J_a.sum(axis=2)

        # iloczyny

        prod_fi_psi_J_1 = fi_rep_J_1 * psi_rep_J_1
        prod_fi_psi_J_2 = fi_rep_J_2 * psi_rep_J_2
        prod_fi_psi_J_3 = fi_rep_J_3 * psi_rep_J_3

        prod_fi_J_psi_4 = (fi_J_1 * J_sum_row[:, 0] +
                           fi_J_2 * J_sum_row[:, 1] +
                           fi_J_3 * J_sum_row[:, 2])[i_meas, :] * psi_rep_4

        prod_psi_J_fi_4 = (psi_J_1 * J_sum_row[:, 0] +
                           psi_J_2 * J_sum_row[:, 1] +
                           psi_J_3 * J_sum_row[:, 2])[i_steam, :] * fi_rep_4

        fi_4_psi_4_J_d2 = np.sum(J_sum_row ** 2, axis=1) * fi_rep_4 * psi_rep_4

        # ostateczna macierz wrażliwości
        MS = -1 * self.detJ / (6 * I) * (prod_fi_psi_J_1 + prod_fi_psi_J_2 + prod_fi_psi_J_3
                                         - prod_fi_J_psi_4
                                         - prod_psi_J_fi_4
                                         + fi_4_psi_4_J_d2)

        # S = psi_rep_1.shape
        #
        # psi_rep_1 = psi_rep_1.reshape(S[0], S[1], 1, 1)
        # psi_rep_2 = psi_rep_2.reshape(S[0], S[1], 1, 1)
        # psi_rep_3 = psi_rep_3.reshape(S[0], S[1], 1, 1)
        # # psi_rep_4 = psi_rep_4.reshape(S[0], S[1], 1, 1)
        #
        # fi_rep_1 = fi_rep_1.reshape(S[0], S[1], 1, 1)
        # fi_rep_2 = fi_rep_2.reshape(S[0], S[1], 1, 1)
        # fi_rep_3 = fi_rep_3.reshape(S[0], S[1], 1, 1)
        # # fi_rep_4 = fi_rep_4.reshape(S[0], S[1], 1, 1)
        #
        # psi_m1 = np.concatenate([psi_rep_1, psi_rep_2, psi_rep_3], axis=2)
        # # psi_m1 = np.moveaxis(psi_m1, -1, 0)
        # psi_m2 = np.moveaxis(psi_m1, [0,1,2], [2,3,0])
        #
        # fi_n1 = np.concatenate([fi_rep_1, fi_rep_2, fi_rep_3], axis=3)
        # # fi_n1 = np.moveaxis(fi_n1, -1, 0)
        # fi_n2 = np.moveaxis(fi_n1, [0,1,2], [2,3,0])
        #
        # J_T_array = np.array(J_T)
        # J_T_a1 = np.moveaxis(J_T_array, [0,1], [2,1])
        # # J_T_a1 = np.moveaxis(J_T_a1, -1, 0)
        # J_array = np.array(J)
        # J_a1 = np.moveaxis(J_array, [0,1], [2,1])
        # # J_a1 = np.moveaxis(J_a1, -1, 0)
        #
        # sum_k_J_ki_J_kj = J_a1 * J_T_a1
        # # sum_k_J_ki_J_kj[0][0] = np.array([J[x][0, 0]**2 + J[x][0, 1]**2 + J[x][0, 2]**2 for x in range(0, n_elems)])
        # # sum_k_J_ki_J_kj[0][1] = np.array([J[x][0, 0] * J[x][1, 0] + J[x][0, 1] * J[x][1, 1] + J[x][0, 2] * J[x][1, 2]
        # #                                   for x in range(0, n_elems)])
        # # sum_k_J_ki_J_kj[0][2] = np.array([J[x][0, 0] * J[x][2, 0] + J[x][0, 1] * J[x][2, 1] + J[x][0, 2] * J[x][2, 2]
        # #                                   for x in range(0, n_elems)])
        # #
        # # sum_k_J_ki_J_kj[1][0] = sum_k_J_ki_J_kj[0][1]
        # # sum_k_J_ki_J_kj[1][1] = np.array([J[x][1, 0] ** 2 + J[x][1, 1] ** 2 + J[x][1, 2] ** 2 for x in range(0, n_elems)])
        # # sum_k_J_ki_J_kj[1][2] = np.array([J[x][1, 0] * J[x][2, 0] + J[x][1, 1] * J[x][2, 1] + J[x][1, 2] * J[x][2, 2]
        # #                                   for x in range(0, n_elems)])
        # #
        # # sum_k_J_ki_J_kj[2][0] = sum_k_J_ki_J_kj[0][2]
        # # sum_k_J_ki_J_kj[2][1] = sum_k_J_ki_J_kj[1][2]
        # # sum_k_J_ki_J_kj[2][2] = np.array([J[x][2, 0] ** 2 + J[x][2, 1] ** 2 + J[x][2, 2] ** 2 for x in range(0, n_elems)])
        # sum_jk_J_ki_J_kj = sum_k_J_ki_J_kj.sum(axis=1)
        # sum_ik_J_ki_J_kj = sum_k_J_ki_J_kj.sum(axis=0)
        # sum_ijk_J_ki_J_kj = sum_ik_J_ki_J_kj.sum(axis=0)
        #
        # sum_k = np.moveaxis(sum_k_J_ki_J_kj, -1, 0)
        # sum_k = np.moveaxis(sum_k, -1, 0).reshape(n_elems, 3, 3, 1)
        # sum_k = np.moveaxis(sum_k, [0, 1, 2], [3, 0, 1])
        # # sum_k = np.moveaxis(sum_k, -1, 0)
        # # sum_k = np.moveaxis(sum_k, -1, 0)
        # # sum_k = np.moveaxis(sum_k, -1, 0)
        #
        # sum_ik = sum_ik_J_ki_J_kj.T.reshape(n_elems, 3, 1)
        # sum_ik = np.moveaxis(sum_ik, [0, 1], [2, 0])
        # # sum_ik = np.moveaxis(sum_ik, -1, 0)
        # # sum_ik = np.moveaxis(sum_ik, -1, 0)
        #
        # sum_jk = sum_jk_J_ki_J_kj.T.reshape(n_elems, 3, 1)
        # sum_jk = np.moveaxis(sum_jk, [0, 1], [2, 0])
        # # sum_jk = np.moveaxis(sum_jk, -1, 0)
        # # sum_jk = np.moveaxis(sum_jk, -1, 0)
        #
        # M_1 = (fi_n2*psi_m2*sum_k).sum(axis=0).sum(axis=0)
        # M_2 = fi_rep_4*psi_rep_4*sum_ijk_J_ki_J_kj
        # M_3 = psi_rep_4*(fi_n1.reshape(3, len(i_meas), n_elems)*sum_ik).sum(axis=0)
        # M_4 = fi_rep_4*(psi_m1.reshape(3, len(i_steam), n_elems)*sum_jk).sum(axis=0)
        #
        #
        # # sum_ijk_J_ki_J_kj = sum_k_J_ki_J_kj[0][0] + sum_k_J_ki_J_kj[0][1] + sum_k_J_ki_J_kj[0][2] + \
        # #                     sum_k_J_ki_J_kj[1][0] + sum_k_J_ki_J_kj[1][1] + sum_k_J_ki_J_kj[1][2] + \
        # #                     sum_k_J_ki_J_kj[2][0] + sum_k_J_ki_J_kj[2][1] + sum_k_J_ki_J_kj[2][2]
        # #
        # # sum_kj_J_ki_J_kj = np.empty([3, 1]).tolist()
        # # sum_kj_J_ki_J_kj[0] = sum_k_J_ki_J_kj[0][0] + sum_k_J_ki_J_kj[0][1] + sum_k_J_ki_J_kj[0][2]
        # # sum_kj_J_ki_J_kj[1] = sum_k_J_ki_J_kj[1][0] + sum_k_J_ki_J_kj[1][1] + sum_k_J_ki_J_kj[1][2]
        # # sum_kj_J_ki_J_kj[2] = sum_k_J_ki_J_kj[2][0] + sum_k_J_ki_J_kj[2][1] + sum_k_J_ki_J_kj[2][2]
        #
        # # M_1 = [(x,y) for x in a for y in b]
        # # M_1 = np.array([(fi13[x]*psi13[y]*sum_k_J_ki_J_kj[x][y]) for x in range(0, 3) for y in range(0, 3)]).sum(axis=0)
        # # M_2 = fi_rep_4 * psi_rep_4 * sum_ijk_J_ki_J_kj
        # # M_3 = np.array([psi13[x]*sum_kj_J_ki_J_kj[x] for x in range(0, 3)]).sum(axis=0)*fi_rep_4
        # # M_4 = np.array([fi13[x]*sum_kj_J_ki_J_kj[x] for x in range(0, 3)]).sum(axis=0)*psi_rep_4
        # #
        # MS = -self.detJ*self.V_elems*(M_1 + M_2 - M_3 - M_4)/(6*I)
        self.MS = MS
        if decomp_svd:
            (U, s, VT) = np.linalg.svd(MS, full_matrices=False)
            self.MS_svd = {
                'U': U,
                's': s,
                'VT': VT
            }
            self.MS_rank = np.linalg.matrix_rank(self.MS)

    @wrapper
    def objective_function(self, r0, x0, x_a):
        RtR = self.RtR
        p1 = 0.5 * np.linalg.norm(r0) ** 2
        delta = x0 - x_a
        p2 = 0.5 * self.lamb * (delta.T @ RtR @ delta)
        c = p1 + p2
        return c

    @wrapper
    def reconstruction_tikh(self, dv, lamb=1e-5, value_obj_fun=False):
        U = self.MS_svd['U']
        s = self.MS_svd['s']
        V = self.MS_svd['VT'].T
        f = s / (s ** 2 + lamb ** 2)
        S = U.shape

        sigma = np.array([f[t] * U[:, t].T @ dv * V[:, t] for t in range(0, S[1])])

        x = sigma.sum(0)

        self.up_grade_value_elems(x)

        self.iteration_solution = x
        c = []
        if value_obj_fun:
            r = self.simulation() - dv
            xa = np.ones_like(self.value_elems)
            c = self.objective_function(r, x, xa)
        self.value_of_obj_fun = c
        return x

    @wrapper
    def reconstruction_gs(self, dv, p=0.5, lamb=None, method=None, value_obj_fun=False):
        if method is None and lamb is None:
            MS_inv = self.MS_inv
        elif lamb is None:
            lamb = self.lamb
            self.change_ms_inv(p=p, lamb=lamb, method=method)
            MS_inv = self.MS_inv
        elif method is None:
            method = self.method
            self.change_ms_inv(p=p, lamb=lamb, method=method)
            MS_inv = self.MS_inv
        elif method == self.method and lamb == self.lamb:
            MS_inv = self.MS_inv
        # else:
        #     self.method = method
        #     self.lamb = lamb
        #     # self.change_ms_inv(p=p, lamb=lamb, method=method)
        #     MS_inv = self.MS_inv
        ds = np.dot(MS_inv, dv)
        x = np.real(ds)
        self.up_grade_value_elems(x)

        self.iteration_solution = x
        c = []
        if value_obj_fun:
            r = self.simulation() - dv
            xa = np.ones_like(self.value_elems)
            c = self.objective_function(r, x, xa)
        self.value_of_obj_fun = c
        return x

    @wrapper
    def calculate_alpha(self, proposed_alpha, x0, v, xa, dx, obj_fun, gtol):

        def f(c_alpha):
            return self.pom_obj_fun(c_alpha, x0, dx, v, xa, obj_fun)

        alpha = proposed_alpha
        tau = 1 / 2
        # l = 0
        f0 = f(0)
        while f0 < f(alpha):
            alpha *= tau
            # l += 1
            if alpha <= gtol**2:
                alpha = 0
                break
        return alpha

    def pom_obj_fun(self, alpha, x0, dx, v, xa, obj_fun):
        xn = x0 - alpha * dx
        self.up_grade_value_elems(xn)
        rn = self.simulation() - v
        if obj_fun is None:
            c = self.objective_function(rn, xn, xa)
        else:
            c = obj_fun(rn, xn, xa)
        return c

    @wrapper
    def reconstruction_gn(self, v, x0=None, maxiter=1, gtol=1e-3, obj_fun=None,
                          alpha=0.5, obj_fun_val=False, iteration_recon=False, progress_callback=None):
        # Przyjmowanie domyślnych wartości
        obj_fun_val_list = []
        recon = []
        if x0 is None:
            x0 = np.ones_like(self.value_elems)
        x1 = x0
        xa = x0

        lamb = self.lamb

        RtR = self.RtR

        # forward solver
        self.up_grade_value_elems(x0)
        fs = self.simulation(sources_AF=self.sources_for_adjoint_fields_PSI())

        # Residual
        r0 = fs - v

        # Iteration algorytm
        for i in range(maxiter):
            self.matrix_of_sensitivity()
            MS = self.MS

            if i == 0:
                if obj_fun is None:
                    c0 = self.objective_function(r0, x0, xa)
                    c = c0
                else:
                    c0 = obj_fun(r0, x0, xa)
                    c = c0

                if iteration_recon: recon.append(x0)
                if obj_fun_val: obj_fun_val_list.append(c)
            # else:
            #     x_pom = copy.deepcopy(x1)
            #     x1 = copy.deepcopy(x0)
            #     xa = x_pom

            # update
            a1 = np.linalg.inv(MS.T @ MS + lamb ** 2 * RtR)
            a2 = (MS.T @ r0 + lamb ** 2 * RtR @ (x0 - xa))
            dx = a1 @ a2

            # calculate alpha
            alpha = self.calculate_alpha(alpha, x0, v, xa, dx, obj_fun, gtol)

            if alpha <= gtol ** 2:
                print('alpha==0')
                break
            if progress_callback is None:
                print( 'step_size = {}'.format( alpha ) )
            else:
                progress_callback.emit( 'step_size = {}'.format( alpha ) )
            if c/c0 <= gtol:
                print('c/c0 <= gtol')
                break
            x0 = x0 - alpha*dx

            if iteration_recon: recon.append(x0)
            if obj_fun_val: obj_fun_val_list.append(c)

            self.up_grade_value_elems(x0)
            fs = self.simulation(sources_AF=self.sources_for_adjoint_fields_PSI())
            r0 = fs - v

            if obj_fun is None:
                if i == 0:
                    c0 = self.objective_function(r0, x0, xa)
                c = self.objective_function(r0, x0, xa)
            else:
                if i == 0:
                    c0 = obj_fun(r0, x0, xa)
                c = obj_fun(r0, x0, xa)
            er_new = c / c0
            if progress_callback is None:
                print('Iteration number ', str(i), ', c = ', str(c))
            else:
                progress_callback.emit('Iteration number ' + str(i) + ', c = ' + str(c))
            if er_new < gtol:
                break
        self.solution = x0
        self.fs = fs
        self.iteration_solution = recon
        self.value_of_obj_fun = obj_fun_val
        return x0

    @wrapper
    def reconstruction_total_variation(self, vol_meas, num_iterations=2, alpha_tv=1e-10, difference_reconstruction=False,
                                        tikhonov_as_first_step=False, alpha_tikhonov=1e-6, beta=1e-4):
        """
         Metoda regularyzacyjna Total Variation dla klasy ImageEIT_3D_tetra

        :param vol_meas: - ramka pomiarowa
        :param num_iterations: - liczba iteracji (domyślnie 2)
        :param alpha_tv: - parametr regularyzacyjny dla metody Total Vatiation (domyślnie 1e-10)
        :param difference_reconstruction: True or False - zdefiniowanie czy wprowadzamy różnicę ramek pomiarowych
                czy tylko samą pojedyńczą ramkę
        :param tikhonov_as_first_step: True or False - krok początkowy, jeśli True krok=0 liczony jest metodą
                Tikhonov'a, gdy False startujemy z ramki przewodnictwa będącej zerami
        :param alpha_tikhonov: - parametr regularyzacyjny dla metody Tikhonov'a (domyślnie 1e-6)
        :param beta: - parametr pomocniczy (domyślnie 1e-4)
        :return: "conductance_tv" - zmienna która jest listą wartości przewodnictwa otrymaną w ostatnim kroku algorytmu
        """
        MS = self.MS
        D_matrix = matrixD(self.elems, self.nodes)

        n_rows, n_columns = D_matrix.shape

        D_matrix = sp.csr_array(D_matrix)

        # regularization parameters

        min_difference = 1e-6

        delta_beta = 0.8

        epsilon = 10 ** (-6)

        # initial values of sigma

        conductance_tv = np.zeros(n_columns)

        # let's define begining conditions as tikhonov regularization

        if tikhonov_as_first_step == True:
            conductance_tv = self.reconstruction_tikh(vol_meas, alpha_tikhonov)

        # auxiliary variable

        temp_par = np.zeros(n_rows)

        # number list for the line search procedure from range 0-1

        temp_list = ([0, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 0.25, 0.5, 0.75, 1])

        # list of conductance for every step

        conductance_list = [np.zeros(conductance_tv.shape)] * (num_iterations + 1)

        conductance_list[0] = conductance_tv

        scale_par = 1

        # ---------------------------------
        # main loop

        finish_procedure = 0  # it closes the loop if it is equal to 1

        primal_desc_temp_old = np.inf

        itr_counter = 0

        while itr_counter < num_iterations and finish_procedure == 0:

            # try new values of voltages

            vol_sim = MS @ conductance_tv

            # calculate auxiliary variable

            temp_var = D_matrix @ conductance_tv

            # calculate other coeficient

            eta = np.sqrt(temp_var * temp_var + beta)

            # primal and dual coefficients

            primal = (np.abs(temp_var)).sum()

            dual = (temp_par * temp_var).sum()

            # close the loop is primal is not descending

            delta_vol = vol_sim - vol_meas

            primal_desc_temp = (np.linalg.norm(delta_vol)) ** 2 + alpha_tv * primal

            # check that the conductance is descending

            if np.abs(primal_desc_temp / primal_desc_temp_old - 1) < min_difference:

                print("New value of the conductance is the same as previous one!")
                print("Iteration number: " + str(itr_counter))

                break

            else:
                primal_desc_temp_old = primal_desc_temp

            # declaration of auxiliary matrices

            # E_matrix = np.zeros((n_rows, n_rows))
            E_matrix_inv = np.zeros((n_rows, n_rows))
            K_matrix = np.zeros((n_rows, n_rows))

            K_diag_elems = np.ones(n_rows) - (1 / eta) * temp_par * temp_var

            for i in range(0, n_rows):
                # E_matrix[i][i] = eta[i]
                E_matrix_inv[i][i] = 1 / eta[i]
                K_matrix[i][i] = K_diag_elems[i]

            # E_matrix = sp.csr_array(E_matrix)
            E_matrix_inv = sp.csr_array(E_matrix_inv)
            K_matrix = sp.csr_array(K_matrix)

            # precompute variable

            M1 = E_matrix_inv @ K_matrix @ D_matrix

            constant_var = MS.T @ MS + alpha_tv * D_matrix.T @ M1

            # compute conductance difference

            delta_conductance = -np.linalg.inv(constant_var) @ (
                        alpha_tv * D_matrix.T @ E_matrix_inv @ temp_var + MS.T @ (delta_vol))

            # try different regularizations

            reg_values = np.zeros(len(temp_list))

            for i in range(0, len(temp_list)):
                meas_itr = MS @ (conductance_tv + temp_list[i] * delta_conductance)

                reg_values[i] = 0.5 * (np.linalg.norm(meas_itr - vol_meas)) ** 2 + alpha_tv * (
                    np.abs(D_matrix @ (conductance_tv + temp_list[i] * delta_conductance))).sum()

            # value and position of minimum element

            temp, ind = reg_values.min(), np.argmin(reg_values)

            # update conductivity values

            conductance_tv = conductance_tv + temp_list[ind] * delta_conductance

            # difference od auxiliary parameter

            delta_temp_par = - temp_par + E_matrix_inv @ temp_var + M1 @ delta_conductance

            # dual variable step length rule

            limits = np.sign(delta_temp_par)  # sigmoid adds/subtracts delta_temp_par to/from temp_par

            distance_from_limits = limits - temp_par  # the distances from the limits

            # where zeros we put small value to protect against division by 0

            delta_temp_par[delta_temp_par == 0] = 1e-6

            # we avoid distances for which temp_par exceeds the limits of distance*delta_temp_par

            distances = distance_from_limits / delta_temp_par

            idxs = distances == 0

            distances[idxs] = delta_temp_par[idxs]

            # the smallest value of distances multiplied by delta_temp_par

            temp_par = temp_par + np.array((1, 0.99 * distances.min())).min() * delta_temp_par

            # if we do not perform difference reconstruction we need to scale the conductances

            if difference_reconstruction == True:
                conductance_tv[conductance_tv < 0.01 * scale_par] = 0.01 * scale_par

                conductance_tv[conductance_tv > 100 * scale_par] = 100 * scale_par

            # reduction of beta coefficient

            beta = beta * delta_beta

            delta_beta = 0.75 * delta_beta  # delta_beta adjustment

            # minimum beta declaration

            if beta < 2e-12:
                beta = 2e-12

            # the algorithm is stopped when primal-dual gap and ||vol_sim-vol_meas|| is smaller than the epsilon

            if (np.abs(temp_var) - temp_par * temp_var).sum() < epsilon and np.linalg.norm(delta_vol) < epsilon:
                finish_procedure = 1

            # increment the counter

            itr_counter += 1

            # write new conductance values to list

            conductance_list[itr_counter] = conductance_tv

        self.up_grade_value_elems(conductance_tv)

        return conductance_tv


    @wrapper
    def reconstruction(self, dv, lamb=None, p=0.5, method=None, value_obj_fun=False):
        # metody do wyboru: 'kotre', 'lm' - Marquardt–Levenberg, 'dg' - Damped Gauss Newton

        if method is None:
            method = self.method
        if lamb is None:
            lamb = self.lamb
        if method == self.method and lamb == self.lamb:
            MS_inv = self.MS_inv
        else:
            self.change_ms_inv(p=p, lamb=lamb, method=method)
            MS_inv = self.MS_inv
        x = np.dot(MS_inv, dv)
        self.up_grade_value_elems(x)
        self.iteration_solution = x
        c = []
        if value_obj_fun:
            r = self.simulation() - dv
            xa = np.ones_like(self.value_elems)
            c = self.objective_function(r, x, xa)
        self.value_of_obj_fun = c
        return x

    @wrapper
    def save_model_npz(self, name):
        V = vars(copy.deepcopy(self))
        for k in V.keys():
            V[k] = getattr(self, k)
        np.savez(name, np.array(V))


"""
Zmiany względem wersji dostępnej na repozytorium (2022.05.02):

1. linia 234  - dodano: self.stim = { }
2. linia 686  - dodano nowy element do słownika: 'offscreen': True
3. linia 872  - zakomentowano: figure.show( )
4. linia 1321 - zwiększono maksymalną wartość błędu do 1.0E-9
5. linia 1730 - modyfikacja - step_size """

