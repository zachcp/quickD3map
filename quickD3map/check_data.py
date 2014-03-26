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
        
def load_distance_df(distance_df, df, samplecolumn=None):
    """
    check that the distance dataframe has indices that match the data dataframe
    """
    if distance_df is None:
        return None
    else:
        # check that the third column is a number and that the
        # first two columns of the distance dataframes have member belonging
        # to the main dataframe
        assert isinstance(distance_df, pd.core.frame.DataFrame)
        dtypes  = distance_df.dtypes
        columns = distance_df.columns
        assert len(dtypes)==3 #there should be three columns a source, destination and target
        assert dtypes[2] in ['float64','int64'] # the weight column needs to be numeric
        
        if samplecolumn:
            samplecolumn_values = list(df[samplecolumn])
        else:
            print("Using First Column as Sample Label Columns")
            samplecolumn_values = list(df[ df.columns[0] ])
            
        def inlist(c,ls): 
            if c in ls:
                return True
            else:
                return False
        
        col1  = [ inlist(c, samplecolumn_values) for c in distance_df[columns[0]]]
        col2  = [ inlist(c, samplecolumn_values) for c in distance_df[columns[1]]]
        
        if False in col1 or False in col2:
            raise ValueError("Distance Dataframe contains sample codes not found in Data dataframe. \
                              Check indices of both dataframes. ")
        
        return distance_df
