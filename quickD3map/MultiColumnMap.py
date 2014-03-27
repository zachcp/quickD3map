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
from geojson import Point, Feature, FeatureCollection, LineString
from jinja2 import Environment, PackageLoader
from .utilities import build_map, create_map, display_map, projections, latitude,longitude
from .check_data import  check_column, check_center, check_samplecolumn, check_projection


class MultiColumnMap(object): 
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
             
        # Check Inputs For Bad or Inconsistent Data
        assert isinstance(df, pd.core.frame.DataFrame)
        self.df  = df
        self.lat = check_column(self.df, latitude,  'latitude')
        self.lon = check_column(self.df, longitude, 'longitude')
        self.map = map
        self.center= check_center(center)
        self.projection = check_projection(projection)
        self.columns = columns
        self.scale_exp = scale_exp 
        
        
        #Template Information Here
        self.env = Environment(loader=PackageLoader('quickD3map', 'templates'))
        self.template_vars = {'width': width, 'height': height, 
                              'center': self.center, 'projection':self.projection,
                              'columns': self.columns, 'scale_exp': self.scale_exp}
        
        self.map_templates =  {'us_states': {'json': 'us_states.json',
                                           'template':'us_map.html'},
                               'world_map': {'json': 'world-50m.json',
                                               'template':'world_map.html'},
                               'world_map_multiple_samples': {'json': 'world-50m.json',
                                               'template':'world_map_multiplesamples.html'}}
        
        #JS Libraries and CSS Styling
        self.template_vars['d3_projection'] =  self.env.get_template('d3.geo.projection.v0.min.js').render()
        self.template_vars['topojson'] =  self.env.get_template('topojson.v1.min.js').render()
        self.template_vars['d3js'] =  self.env.get_template('d3.v3.min.js').render()
        self.template_vars['style'] =  self.env.get_template('style.css').render()
        
        
        
    def _convert_to_geojson(self, df, lat, lon, distance_df=None, index_col=None):
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
        
MultiColumnMap.build_map   = build_map   
MultiColumnMap.create_map  = create_map
MultiColumnMap.display_map = display_map
