import numpy as np
import scipy.sparse as sp

from pandas import read_csv
from itertools import combinations


def load_data_from_HT1( file_name ):
    
    raw_data = read_csv( file_name, sep = ';' )
    
    raw_data = raw_data[ raw_data.columns[ 0 ] ].index.to_list( )
    
    indices_DF = np.argwhere( np.array( ( [ e[ 0 ] == 'close' for e in raw_data ] ) ) ).flatten( )
    
    N_DF = indices_DF.size
    
    size_DF = sum( [ e[ 0 ] == 'EIT_M' for e in raw_data[ : indices_DF[ 0 ] ] ] )
    
    if ( sum( [ e[ 0 ] == 'EIT_M' for e in raw_data ] ) != N_DF * size_DF ): raise Exception( 'Data frames can not be recognized.' )
    
    raw_data = [ raw_data[ index - size_DF : index ] for index in indices_DF ]
    
    integer_type = np.int_
    
    stimulation_gnd = [ np.array( [ e[ 2 : 6 ] for e in data_frame ], dtype = integer_type ) for data_frame in raw_data ]
    
    if ( N_DF > 1 ):
        
        L = all( [ np.array_equal( stimulation_gnd[ i ], stimulation_gnd[ j ] ) for i, j in combinations( range( N_DF ), 2 ) ] )
        
        if ( L == False ): raise Exception( 'Data frames are not consistent.' )
    
    stimulation_gnd = stimulation_gnd[ 0 ]
    
    N = np.max( stimulation_gnd ) - np.min( stimulation_gnd ) + 1
    
    injection_electrodes, MP_EX = np.unique( stimulation_gnd[ :, 0 : 2 ], axis = 0, return_inverse = True )
    
    is_included = [ ]
    
    measurement_electrodes = [ ]
    
    float_type = np.float_
    
    voltages_gnd = [ np.array( [ e[ 6 ].replace( ',', '.' ) for e in data_frame ], dtype = float_type ) for data_frame in raw_data ]
    
    voltages = [ ]
    
    for index_EX in range( injection_electrodes.shape[ 0 ] ):
        
        select_excitation = ( MP_EX == index_EX )
        
        meas_pattern_gnd = stimulation_gnd[ select_excitation, 2 : 4 ]
        
        if ( meas_pattern_gnd.shape[ 0 ] < 2 ): raise Exception( 'Voltages can not be calculated.' )
        
        L = [ np.unique( e ).size for e in np.transpose( meas_pattern_gnd ) ]
        
        if ( set( L ) != { 1, meas_pattern_gnd.shape[ 0 ] } ): raise Exception( 'Voltages can not be calculated.' )
        
        electrodes_M = meas_pattern_gnd[ :, [ e > 1 for e in L ].index( True ) ]
        
        electrodes_P = np.mod( electrodes_M + 1, N )
        
        conditions = [ ]
        
        conditions.append( np.isin( electrodes_P, electrodes_M ) )
        
        conditions.append( np.any( np.isin( np.column_stack( [ electrodes_M, electrodes_P ] ), injection_electrodes[ index_EX ] ), axis = 1 ) == False )
        
        is_included.append( np.logical_and( *conditions ) )
        
        measurement_electrodes.append( { -1 : electrodes_M[ is_included[ -1 ] ], 1 : electrodes_P[ is_included[ -1 ] ] } )
        
        map_object = dict( zip( electrodes_M, np.arange( np.sum( select_excitation ) ) ) )
        
        indices_M = np.array( [ map_object[ key ] for key in electrodes_M[ is_included[ -1 ] ] ], dtype = integer_type )
        
        indices_P = np.array( [ map_object[ key ] for key in electrodes_P[ is_included[ -1 ] ] ], dtype = integer_type )
        
        voltages.append( [ np.reshape( U[ select_excitation ][ indices_P ] - U[ select_excitation ][ indices_M ], ( -1, 1 ) ) for U in voltages_gnd ] )
    
    voltages = np.block( voltages )
    
    stim_pattern = [ sp.csr_matrix( ( [ 1.0, -1.0 ], ( [ 0, 0 ], IE ) ), shape = ( 1, N ), dtype = float_type ) for IE in injection_electrodes ]
    
    measurement_electrodes_P = [ e[ +1 ] for e in measurement_electrodes ]
    measurement_electrodes_M = [ e[ -1 ] for e in measurement_electrodes ]
    
    rows = [ np.arange( 0, np.sum( L ), 1, dtype = integer_type ) for L in is_included ]
    
    meas_pattern_P = [ sp.csr_matrix( ( np.ones_like( R ), ( R, ME_P ) ), shape = ( R.size, N ), dtype = integer_type ) for ME_P, R in zip( measurement_electrodes_P, rows ) ]
    meas_pattern_M = [ sp.csr_matrix( ( np.ones_like( R ), ( R, ME_M ) ), shape = ( R.size, N ), dtype = integer_type ) for ME_M, R in zip( measurement_electrodes_M, rows ) ]
    
    meas_pattern = [ P - M for P, M in zip( meas_pattern_P, meas_pattern_M ) ]
    
    HT_data = { }
    
    HT_data[ 'file_name' ] = file_name
    
    HT_data[ 'raw_data' ] = raw_data
    
    HT_data[ 'injection_electrodes' ] = injection_electrodes
    
    HT_data[ 'is_included' ] = is_included
    
    HT_data[ 'measurement_electrodes' ] = measurement_electrodes
    
    HT_data[ 'stimulation' ] = { 'stim_pattern': stim_pattern, 'meas_pattern': meas_pattern }
    
    HT_data[ 'voltages' ] = voltages
    
    return HT_data


def get_data_from_array( raw_data, electrodes=None):
    if np.all(np.isnan(raw_data[:, -1])): raw_data = np.delete(raw_data, -1, 1)

    indices_NaN = np.argwhere(np.isnan(raw_data[:, 0]))

    if (indices_NaN.size != 0): raw_data = raw_data[: np.min(indices_NaN)].copy()

    raw_data = np.delete(raw_data, raw_data[:, 0] == 0, 0)

    if (raw_data.size == 0): raise Exception("File: '" + file_name + "' is not valid.")

    integer_type = np.int_

    injection_electrodes = np.asarray(raw_data[:, 1: 3], dtype=integer_type)

    N_max = np.max(injection_electrodes) + 1

    if (electrodes == None): electrodes = np.arange(0, N_max, 1, dtype=integer_type)

    electrodes = np.unique(np.reshape(np.asarray(electrodes, dtype=integer_type), -1))

    if (np.all(np.isin(electrodes, np.arange(0, N_max, 1, dtype=integer_type))) == False): raise ValueError(
        "Array 'electrodes' is not valid.")

    N = electrodes.size

    indices = np.arange(0, N, 1, dtype=integer_type)

    map_object = dict(zip(electrodes, indices))

    select_excitations = np.all(np.isin(injection_electrodes, electrodes), axis=1)

    injection_electrodes = np.array([[map_object[e] for e in IE] for IE in injection_electrodes[select_excitations, :]],
                                    dtype=integer_type)

    float_type = np.float_

    currents = np.asarray(raw_data[select_excitations, 0], dtype=float_type)

    voltages_gnd = np.asarray(raw_data[np.ix_(select_excitations, electrodes + 3)], dtype=float_type)

    electrodes_P = np.roll(indices, -1)

    electrodes_M = indices

    is_included = [np.any(np.isin(np.column_stack((electrodes_P, electrodes_M)), IE), axis=1) == False for IE in
                   injection_electrodes]

    measurement_electrodes_P = [electrodes_P[L] for L in is_included]
    measurement_electrodes_M = [electrodes_M[L] for L in is_included]

    voltages = [np.reshape(U[ME_P] - U[ME_M], (-1, 1)) for U, ME_P, ME_M in
                zip(voltages_gnd, measurement_electrodes_P, measurement_electrodes_M)]

    voltages = np.vstack(voltages)

    stim_pattern = [sp.csr_matrix(([I, -I], ([0, 0], IE)), shape=(1, N), dtype=float_type) for IE, I in
                    zip(injection_electrodes, currents)]

    rows = [np.arange(0, np.sum(L), 1, dtype=integer_type) for L in is_included]

    meas_pattern_P = [sp.csr_matrix((np.ones_like(R), (R, ME_P)), shape=(R.size, N), dtype=integer_type) for ME_P, R in
                      zip(measurement_electrodes_P, rows)]
    meas_pattern_M = [sp.csr_matrix((np.ones_like(R), (R, ME_M)), shape=(R.size, N), dtype=integer_type) for ME_M, R in
                      zip(measurement_electrodes_M, rows)]

    meas_pattern = [P - M for P, M in zip(meas_pattern_P, meas_pattern_M)]

    HT_data = {}

    # HT_data['file_name'] = file_name

    HT_data['electrodes'] = electrodes

    HT_data['raw_data'] = raw_data

    HT_data['injection_electrodes'] = injection_electrodes

    HT_data['is_included'] = is_included

    HT_data['measurement_electrodes'] = [{-1: ME_M, 1: ME_P} for ME_P, ME_M in
                                         zip(measurement_electrodes_P, measurement_electrodes_M)]

    HT_data['stimulation'] = {'stim_pattern': stim_pattern, 'meas_pattern': meas_pattern}

    HT_data['voltages'] = voltages

    return HT_data


def load_data_from_HT2( file_name, electrodes = None ):
    
    raw_data = read_csv( file_name, sep = ';', header = None ).to_numpy( )
    
    if np.all( np.isnan( raw_data[ :, -1 ] ) ): raw_data = np.delete( raw_data, -1, 1 )
    
    indices_NaN = np.argwhere( np.isnan( raw_data[ :, 0 ] ) )
    
    if ( indices_NaN.size != 0 ): raw_data = raw_data[ : np.min( indices_NaN ) ].copy( )
    
    raw_data = np.delete( raw_data, raw_data[ :, 0 ] == 0, 0 )
    
    if ( raw_data.size == 0 ): raise Exception( "File: '" + file_name + "' is not valid." )
    
    integer_type = np.int_
    
    injection_electrodes = np.asarray( raw_data[ :, 1 : 3 ], dtype = integer_type )
    
    N_max = np.max( injection_electrodes ) + 1
    
    if ( electrodes == None ): electrodes = np.arange( 0, N_max, 1, dtype = integer_type )
    
    electrodes = np.unique( np.reshape( np.asarray( electrodes, dtype = integer_type ), -1 ) )
    
    if ( np.all( np.isin( electrodes, np.arange( 0, N_max, 1, dtype = integer_type ) ) ) == False ): raise ValueError( "Array 'electrodes' is not valid." )
    
    N = electrodes.size
    
    indices = np.arange( 0, N, 1, dtype = integer_type )
    
    map_object = dict( zip( electrodes, indices ) )
    
    select_excitations = np.all( np.isin( injection_electrodes, electrodes ), axis = 1 )
    
    injection_electrodes = np.array( [ [ map_object[ e ] for e in IE ] for IE in injection_electrodes[ select_excitations, : ] ], dtype = integer_type )
    
    float_type = np.float_
    
    currents = np.asarray( raw_data[ select_excitations, 0 ], dtype = float_type )
    
    voltages_gnd = np.asarray( raw_data[ np.ix_( select_excitations, electrodes + 3 ) ], dtype = float_type )
    
    electrodes_P = np.roll( indices, -1 )
    
    electrodes_M = indices
    
    is_included = [ np.any( np.isin( np.column_stack( ( electrodes_P, electrodes_M ) ), IE ), axis = 1 ) == False for IE in injection_electrodes ]
    
    measurement_electrodes_P = [ electrodes_P[ L ] for L in is_included ]
    measurement_electrodes_M = [ electrodes_M[ L ] for L in is_included ]
    
    voltages = [ np.reshape( U[ ME_P ] - U[ ME_M ], ( -1, 1 ) ) for U, ME_P, ME_M in zip( voltages_gnd, measurement_electrodes_P, measurement_electrodes_M ) ]
    
    voltages = np.vstack( voltages )
    
    stim_pattern = [ sp.csr_matrix( ( [ I, -I ], ( [ 0, 0 ], IE ) ), shape = ( 1, N ), dtype = float_type ) for IE, I in zip( injection_electrodes, currents ) ]
    
    rows = [ np.arange( 0, np.sum( L ), 1, dtype = integer_type ) for L in is_included ]
    
    meas_pattern_P = [ sp.csr_matrix( ( np.ones_like( R ), ( R, ME_P ) ), shape = ( R.size, N ), dtype = integer_type ) for ME_P, R in zip( measurement_electrodes_P, rows ) ]
    meas_pattern_M = [ sp.csr_matrix( ( np.ones_like( R ), ( R, ME_M ) ), shape = ( R.size, N ), dtype = integer_type ) for ME_M, R in zip( measurement_electrodes_M, rows ) ]
    
    meas_pattern = [ P - M for P, M in zip( meas_pattern_P, meas_pattern_M ) ]
    
    HT_data = { }
    
    HT_data[ 'file_name' ] = file_name
    
    HT_data[ 'electrodes' ] = electrodes
    
    HT_data[ 'raw_data' ] = raw_data
    
    HT_data[ 'injection_electrodes' ] = injection_electrodes
    
    HT_data[ 'is_included' ] = is_included
    
    HT_data[ 'measurement_electrodes' ] = [ { -1 : ME_M, 1 : ME_P } for ME_P, ME_M in zip( measurement_electrodes_P, measurement_electrodes_M ) ]
    
    HT_data[ 'stimulation' ] = { 'stim_pattern': stim_pattern, 'meas_pattern': meas_pattern }
    
    HT_data[ 'voltages' ] = voltages
    
    return HT_data


def separate_EIT_data_frame( data_frame ):
    
    N_excitations = len( data_frame[ 'stimulation' ][ 'stim_pattern' ] )
    
    if ( N_excitations != len( data_frame[ 'stimulation' ][ 'meas_pattern' ] ) ): raise Exception( 'Stimulation is not valid.' )
    
    meas_pattern_US = list( { A.shape for A in data_frame[ 'stimulation' ][ 'meas_pattern' ] } )
    
    if ( len( meas_pattern_US ) != 1 ): return { 'message': 400 }
    
    if ( N_excitations * meas_pattern_US[ 0 ][ 0 ] != data_frame[ 'voltages' ].size ): return { 'message': 401 }
    
    stim_pattern = [ ]
    meas_pattern = [ ]
    
    for S, M in zip( data_frame[ 'stimulation' ][ 'stim_pattern' ], data_frame[ 'stimulation' ][ 'meas_pattern' ] ):
        
        if ( type( S ).__name__ == 'ndarray' ): stim_pattern.append( S.copy( ) )
        
        else: stim_pattern.append( S.toarray( ) )
        
        if ( type( M ).__name__ == 'ndarray' ): meas_pattern.append( M.copy( ) )
        
        else: meas_pattern.append( M.toarray( ) )
    
    L = np.zeros( ( N_excitations, N_excitations ), dtype = np.bool_ )
    
    for index_i in range( 0, N_excitations ):
        
        for index_j in range( index_i, N_excitations ):
            
            L_sp = np.array_equal( stim_pattern[ index_i ], ( -1.0 ) * stim_pattern[ index_j ] )
            
            L_mp = np.array_equal( meas_pattern[ index_i ], meas_pattern[ index_j ] )
            
            L[ index_i, index_j ] = L_sp and L_mp
    
    if( 2 * np.sum( L ) != N_excitations or np.any( np.diag( L ) ) ): return { 'message': 402 }
    
    indices = np.argwhere( L )
    
    I = indices[ :, 0 ]
    J = indices[ :, 1 ]
    
    voltages = np.reshape( data_frame[ 'voltages' ], ( N_excitations, -1 ) )
    
    result = { }
    
    result[ 'stimulation' ] = { key: [ data_frame[ 'stimulation' ][ key ][ index ] for index in I ] for key in [ 'stim_pattern', 'meas_pattern' ] }
    
    result[ 'voltages_P' ] = voltages[ I ].flatten( )
    
    result[ 'voltages_M' ] = ( -1.0 ) * voltages[ J ].flatten( )
    
    result[ 'voltages_S' ] = 0.5 * ( result[ 'voltages_P' ] + result[ 'voltages_M' ] )
    
    return result

