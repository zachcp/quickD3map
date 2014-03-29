# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 19:40:24 2014

@author: zachpowers
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function )

import pandas as pd
import geojson
from geojson import Point, Feature, FeatureCollection
from .check_data import  check_column, check_center, check_samplecolumn, check_projection
from .BaseMap import BaseMap

class MultiColumnMap(BaseMap): 
    ''' Create a PointMap of multiple columns with d3.js'''
    def __init__(self, df, columns = None,width=900, height=500, scale_exp=3, 
                 geojson="", attr=None, map="world_map_multiple_samples", distance_df=None, 
                 center=None, projection="mercator"):
                    
        '''
        PointMap is a class that takes a dataframe and returns an html webpage that
        can optionally be viewed as a Flask Webapp. Pointmap requires a pandas dataframe
        with latitude and longitude options.
        
         Parameters
        ----------
        df: pandas dataframe, required.
            dataframe with latitude and longitude columns.
        columns: list, (default=None)
            list of columns required for the addiotn of the checkbox
            
        width: int, default 960
            Width of the map.
        height: int, default 500
            Height of the map.
        scale: int, default 100000.
            scale factor for the size plotted points
        map: str, default "world_map".
           template to be used for mapping.

        For Future Implementation:
        distance_df: pandas dataframe, optional (default = None)
           dataframe with infomraiton about the linkages between points.
           Line features not yet implemented!
        samplecolumn: str, optional but required for distance-based map. (default=None)
           sample column is the name of the column in df that contians the names of
           the features to be plotted. All members of the first two columns of
           distance_df must be in this column
        center: list of legth two: lat/long (default=[-100, 0])
           provides a new center for the map
        projection: str, default="mercator"
           a projection that is one of the projecions recognized by d3.js
        
        Returns
        -------
        D3.js Webpage using create_map() or a display of that map 
        using display_map() 
        
        
        Examples
        --------
        >>>from quickD3map import PointMap
        >>>import statsmodels.api as sm
        >>>import pandas as pd
        >>>#import some data
        >>>quakes = sm.datasets.get_rdataset('quakes','datasets')
        >>>qdf = pd.DataFrame( quakes.data )
        >>>#make a map
        >>>PointMap(qdf).display_map()

        '''
        super(MultiColumnMap, self).__init__(df=df,center=center, projection=projection)

        #Elements Unique to this template        
        self.columns = columns
        self.scale_exp = scale_exp 
        
        
#        self.map_templates =  {'us_states': {'json': 'us_states.json',
#                                           'template':'us_map.html'},
#                               'world_map': {'json': 'world-110m.json',
#                                               'template':'world_map.html'},
#                               'world_map_multiple_samples': {'json': 'world-110m.json',
#                                               'template':'world_map_multiplesamples.html'},
#                                'world_map_ocean': {'json': 'world-110m.json',
#                                                'template':'world_map_multiplesamples.html'}   
#                                       }
#        
   
        
    #unique geojson conversion
    def convert_to_geojson(self, df, lat, lon, distance_df=None, index_col=None):
        ''' Dataconversion happens here. Process Dataframes and get 
            necessary information into geojson which is put into the template 
            var dictionary for later'''
        
        ## Support Functions For processing to geojson
        ################################################################################
        def feature_from_row(row):
            if pd.notnull(row[lat]) and pd.notnull(row[lon]):
                properties = { k:v for k,v in row.iterkv() if k in self.columns}
                return Feature(geometry=Point(( row[lon], row[lat] )),
                               properties=properties)

        featurelist= [ feature_from_row(row) for idx, row in df.iterrows() ]
        self.template_vars['geojson'] = geojson.dumps( FeatureCollection(featurelist) )

