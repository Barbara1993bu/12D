import numpy as np
import scipy.io


def load_mesh_from_mat_file_v2( file_name, electrode_order = np.array( [ ] ) ):
    
    fwd_model = scipy.io.loadmat( file_name, struct_as_record = False )[ 'img' ][ 0, 0 ].fwd_model[ 0, 0 ]
    
    mesh = { }
    
    mesh[ 'nodes' ] = fwd_model.nodes.astype( np.float64 )
    
    mesh[ 'elems' ] = fwd_model.elems.astype( np.int64 ) - 1
    
    mesh[ 'boundary' ] = fwd_model.boundary.astype( np.int64 ) - 1
    
    fwd_model.electrode = np.squeeze( fwd_model.electrode )
    
    if np.array_equal( np.sort( electrode_order ), np.arange( 0, fwd_model.electrode.size ) ): fwd_model.electrode = fwd_model.electrode[ electrode_order ]
    
    mesh[ 'electrodes_nodes' ] = [ np.reshape( E.nodes, -1 ).astype( np.int64 ) - 1 for E in fwd_model.electrode ]
    
    mesh[ 'z_contact' ] = np.squeeze( np.array( [ E.z_contact for E in fwd_model.electrode ], dtype = np.float64 ) )
    
    mesh[ 'electrodes_elems' ] = [ np.reshape( np.argwhere( np.all( np.isin( mesh[ 'boundary' ], E_nodes ), axis = 1 ) ), -1 ) for E_nodes in mesh[ 'electrodes_nodes' ] ]
    
    FEs = [ np.isin( mesh[ 'elems' ], E_nodes ) for E_nodes in mesh[ 'electrodes_nodes' ] ]
    
    INDs = [ np.sum( element, axis = 1 ) == mesh[ 'boundary' ].shape[ 1 ] for element in FEs ]
    
    mesh[ 'electrodes_ind_nodes_elems' ] = [ np.hstack( [ np.argwhere( indices ), elements[ indices ] ] ).astype( np.int64 ) for indices, elements in zip( INDs, FEs ) ]
    
    mesh[ 'elem_data' ] = np.ones( mesh[ 'elems' ].shape[ 0 ], dtype = np.float64 )
    
    return mesh