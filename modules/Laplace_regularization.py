import numpy as np
import scipy.sparse as sps
import matplotlib.tri as tri


def simple_laplacea(neighboor, N_elems):
    Len_neighboor = np.array([len(x) for x in neighboor])
    ind_elems = np.r_[0:N_elems]
    nei_array = np.row_stack(neighboor)
    L = sps.coo_matrix((Len_neighboor, (ind_elems, ind_elems)), shape=(N_elems, N_elems))
    ind_elems = np.repeat(ind_elems, Len_neighboor)
    L += sps.coo_matrix((-1 * np.ones_like(ind_elems), (nei_array.reshape(-1), ind_elems)),
                        shape=(N_elems, N_elems))
    return L


def square_laplacea(neighboor1, neighboor2, N_elems):
    Len_neighboor1 = np.array([len(x) for x in neighboor1])
    Len_neighboor2 = np.array([len(x) for x in neighboor2])
    ind_elems = np.r_[0:N_elems]
    nei_array1 = np.row_stack(neighboor1)
    nei_array2 = np.row_stack(neighboor2)

    L = sps.coo_matrix((1/4*Len_neighboor1, (ind_elems, ind_elems)), shape=(N_elems, N_elems))
    L += sps.coo_matrix((1/2*Len_neighboor2, (ind_elems, ind_elems)), shape=(N_elems, N_elems))

    ind_elems1 = np.repeat(ind_elems, Len_neighboor1)
    L += sps.coo_matrix((-1/4 * np.ones_like(ind_elems1), (nei_array1.reshape(-1), ind_elems1)),
                        shape=(N_elems, N_elems))

    ind_elems2 = np.repeat(ind_elems, Len_neighboor2)
    L += sps.coo_matrix((-1/2 * np.ones_like(ind_elems2), (nei_array2.reshape(-1), ind_elems2)),
                        shape=(N_elems, N_elems))
    return L


def cube_laplacea(neighboor1, neighboor2, neighboor4, N_elems):
    Len_neighboor1 = np.array([len(x) for x in neighboor1])
    Len_neighboor2 = np.array([len(x) for x in neighboor2])
    Len_neighboor4 = np.array([len(x) for x in neighboor4])
    ind_elems = np.r_[0:N_elems]

    L = sps.coo_matrix((N_elems, N_elems))

    nei_array1 = np.row_stack(neighboor1)
    nei_array2 = np.row_stack(neighboor2)
    nei_array4 = np.row_stack(neighboor4)

    L += sps.coo_matrix((2 / 26 * Len_neighboor1, (ind_elems, ind_elems)), shape=(N_elems, N_elems))
    L += sps.coo_matrix((3 / 26 * Len_neighboor2, (ind_elems, ind_elems)), shape=(N_elems, N_elems))
    L += sps.coo_matrix((6 / 26 * Len_neighboor4, (ind_elems, ind_elems)), shape=(N_elems, N_elems))

    ind_elems1 = np.repeat(ind_elems, Len_neighboor1)
    ind_elems2 = np.repeat(ind_elems, Len_neighboor2)
    ind_elems4 = np.repeat(ind_elems, Len_neighboor4)

    L += sps.coo_matrix((-2 / 26 * np.ones_like(ind_elems1), (nei_array1.reshape(-1), ind_elems1)),
                        shape=(N_elems, N_elems))
    L += sps.coo_matrix((-3 / 26 * np.ones_like(ind_elems2), (nei_array2.reshape(-1), ind_elems2)),
                        shape=(N_elems, N_elems))
    L += sps.coo_matrix((-6 / 26 * np.ones_like(ind_elems4), (nei_array4.reshape(-1), ind_elems4)),
                        shape=(N_elems, N_elems))
    return L


def cot_laplacea(nodes, elems):
    N_elems = len(elems)
    L = sps.coo_matrix((N_elems, N_elems))
    centers = centers_of_triangles(nodes, elems)
    mesh_dual = tri.Triangulation(centers[:, 0], centers[:, 1])
    nei = [np.argwhere(mesh_dual.edges == k)[:, 0] for k in range(len(mesh_dual.x))]
    for k in range(len(mesh_dual.x)):
        nei_k = nei[k]

        edges_k = mesh_dual.edges[nei_k, :]
        kk = edges_k[edges_k != k].reshape(-1)
        sum_cot = np.zeros(len(edges_k))
        for ind_edge in range(len(nei_k)):
            edge_k = edges_k[ind_edge, :]
            elems_with_edge_k0 = np.sum(mesh_dual.triangles == edge_k[0], axis=1).reshape(-1)
            elems_with_edge_k1 = np.sum(mesh_dual.triangles == edge_k[1], axis=1).reshape(-1)
            ind_elems_with_edge_k = np.argwhere(np.logical_and(elems_with_edge_k0, elems_with_edge_k1)).reshape(-1)
            elems_with_edge_k = mesh_dual.triangles[ind_elems_with_edge_k, :]
            ind_nodes_other_in_elems = np.argwhere(np.isin(elems_with_edge_k, edge_k) == False)[:, 1]
            ind_nodes_other_in_elems = [elems_with_edge_k[i, ind_nodes_other_in_elems[i]]
                                        for i in range(len(ind_nodes_other_in_elems))]

            for j in range(len(ind_nodes_other_in_elems)):
                ind_j = ind_nodes_other_in_elems[j]
                a = np.array([mesh_dual.x[ind_j] - mesh_dual.x[edge_k[0]],
                              mesh_dual.y[ind_j] - mesh_dual.y[edge_k[0]]])
                b = np.array([mesh_dual.x[ind_j] - mesh_dual.x[edge_k[1]],
                              mesh_dual.y[ind_j] - mesh_dual.y[edge_k[1]]])
                sum_cot[ind_edge] += -0.5 * (np.dot(a, b) / (np.linalg.norm(a) ** 2 * np.linalg.norm(b) ** 2 -
                                                             np.dot(a, b) ** 2) ** 0.5)
        L += sps.coo_matrix((sum_cot, (np.zeros_like(kk) + k, kk)), shape=(N_elems, N_elems))
        L += sps.coo_matrix((-1 * np.sum(sum_cot)*np.ones([1]), (k*np.ones([1]), k*np.ones([1]))), shape=(N_elems, N_elems))

    return L


def centers_of_triangles(nodes, tri):
    r_vector_nodes_i = nodes[tri[:, 0],:]
    r_vector_nodes_j = nodes[tri[:, 1],:]
    r_vector_nodes_k = nodes[tri[:, 2],:]

    length_ij = np.tile((np.sum((r_vector_nodes_i - r_vector_nodes_j)**2, axis=1))**0.5, [2, 1]).T
    length_jk = np.tile((np.sum((r_vector_nodes_j - r_vector_nodes_k)**2, axis=1))**0.5, [2, 1]).T
    length_ki = np.tile((np.sum((r_vector_nodes_k - r_vector_nodes_i)**2, axis=1))**0.5, [2, 1]).T

    incenter = (length_ij * r_vector_nodes_k) + (length_jk * r_vector_nodes_i) + (length_ki * r_vector_nodes_j)

    incenter = incenter / (length_ij + length_jk + length_ki)

    return incenter


def matrix_laplacea(elems, nodes, type_mesh, simple_laplacea_matrix=True):
    N_elems = len(elems)
    if simple_laplacea_matrix:
        if type_mesh == 'tri':
            neighboor = [np.argwhere(np.isin(elems, elems[k, :]).sum(axis=1) == 2) for k in range(N_elems)]

        elif type_mesh == 'square':
            neighboor = [np.argwhere(np.isin(elems, elems[k, :]).sum(axis=1) == 2) for k in range(N_elems)]

        elif type_mesh == 'tetra':
            neighboor = [np.argwhere(np.isin(elems, elems[k, :]).sum(axis=1) == 3) for k in range(N_elems)]

        elif type_mesh == 'cube':
            neighboor = [np.argwhere(np.isin(elems, elems[k, :]).sum(axis=1) == 4) for k in range(N_elems)]

        else:
            print('niewspierany rodzaj siatki')
        L = simple_laplacea(neighboor, N_elems)
    else:
        L = sps.coo_matrix((N_elems, N_elems))
        if type_mesh == 'tri':
            L = cot_laplacea(nodes, elems)
        elif type_mesh == 'square':
            neighboor2 = [np.argwhere(np.isin(elems, elems[k, :]).sum(axis=1) == 2) for k in range(len(elems))]
            neighboor1 = [np.argwhere(np.isin(elems, elems[k, :]).sum(axis=1) == 1) for k in range(len(elems))]
            L = square_laplacea(neighboor1, neighboor2, N_elems)
        elif type_mesh == 'cube':
            neighboor4 = [np.argwhere(np.isin(elems, elems[k, :]).sum(axis=1) == 4) for k in range(len(elems))]
            neighboor2 = [np.argwhere(np.isin(elems, elems[k, :]).sum(axis=1) == 2) for k in range(len(elems))]
            neighboor1 = [np.argwhere(np.isin(elems, elems[k, :]).sum(axis=1) == 1) for k in range(len(elems))]
            L = cube_laplacea(neighboor1, neighboor2, neighboor4, N_elems)
        elif type_mesh == 'tetra':
            print('pracujemy nad tym')


    return L
