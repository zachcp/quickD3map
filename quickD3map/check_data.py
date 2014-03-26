from .utilities import projections

def check_column(df, namelist, name):
    for col in df.columns:
        if col.strip().lower() in namelist:
            return col
    raise ValueError("No {} column found in the dataframe".format(name))
                    
def check_center(center):
    try:
        if isinstance(center, tuple) or isinstance(center, list) and len(center) == 2:
            return center
    except:
        print("Center Must be a Tuple or List")
        return None
    
def check_samplecolumn(df, samplecolumn):
    if samplecolumn in df.columns:
        return samplecolumn
    else:
        ### To do check this only when using distance df
        print('In the absence of an explicit sample column we are setting Samplecolumn to "None"')
        return None
        
def check_projection(projection):
    if projection in projections:
        return projection
    else:
        print('This is not a valid projection, using default=mercator')
        return "mercator"


def verify_dfs_forLineMap(df, samplecolumn, distance_df):
    """
    check 3 things:
      1: the dimensions of the distance_frame
      2: that samplecolumn is a column of df
      3: that all members of the first two columns of of distance_df are in df[samplecolumn]
    """
    
    #check shape of distance_df
    dtypes  = distance_df.dtypes
    columns = distance_df.columns
    assert len(dtypes)==3 #there should be three columns a source, destination and target
    assert dtypes[2] in ['float64','int64'] # the weight column needs to be numeric
    
    #check_samplecolumn
    check_samplecolumn(df, samplecolumn)
    
    #check agreement between df and distance_df
    samplecolumn_values = list(df[samplecolumn])
    distance_vales = list( distance_df[columns[0]]] ) + list( distance_df[columns[1]]] )  
    
    correct = True
    for d in distance_values:
        if not d in samplecolumn_values:
            correct = False
    
    if not correct:
        raise ValueError("Value mismatch between yout to dataframes.")
    else:
        return correct
