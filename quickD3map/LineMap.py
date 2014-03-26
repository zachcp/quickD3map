#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function )

import pandas as pd
import geojson
from geojson import Point, Feature, FeatureCollection, LineString
from jinja2 import Environment, PackageLoader
from .utilities import build_map,create_map, display_map, projections, latitude, longitude
from .check_data import  check_column, check_center, check_samplecolumn, check_projection, verify_dfs_forLineMap, check_for_NA


class LineMap(object): 
    ''' Create a PointMap with quickD3map '''
    def __init__(self, df, samplecolumn, distance_df,  width=960, height=500, scale=100000, 
                 geojson="", attr=None, map="world_map", center=None, projection="mercator"):
                    
        '''
        LineMap is a class that takes a dataframe and returns an html webpage that
        can optionally be viewed as a Flask Webapp. Pointmap requires a pandas dataframe
        with latitude and longitude options.
        
         Parameters
        ----------
        df: pandas dataframe, required.
            dataframe with latitude and longitude columns.
        distance_df: pandas dataframe, required
           distance dataframe must be thtree columns where the first 
           two are locations found in the samplecolumn, and the third
           is a numeric weight.
        samplecolumn: str,  required
           samplecolumn is the name of a column in df. This columns must have the names 
           of all of the samples in the first two columns of distance_df and it must be unique

        width: int, default 960
            Width of the map.
        height: int, default 500
            Height of the map.
        scale: int, default 100000.
            scale factor for the size plotted points
        map: str, default "world_map".
           template to be used for mapping.

        For Future Implementation:
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
        
        ##  Support Functions to Verify Data
        ################################################################################
        
        # Check Inputs and make assignments of data
        assert isinstance(df, pd.core.frame.DataFrame)
        assert isinstance(distance_df, pd.core.frame.DataFrame)
        
        if verify_dfs_forLineMap(df, samplecolumn, distance_df):
            self.distdf = distance_df
        self.lat = check_column(df, latitude,  'latitude')
        self.lon = check_column(df, longitude, 'longitude')
        self.df  = check_for_NA(df, self.lat, self.lon)
        self.map = map
        self.center= check_center(center)
        self.projection = check_projection(projection)
        self.samplecolumn = check_samplecolumn(self.df, samplecolumn)
        
        
        #Templates
        self.env = Environment(loader=PackageLoader('quickD3map', 'templates'))
        self.template_vars = {'width': width, 'height': height, 'scale': scale, 
                              'center': self.center, 'projection':self.projection}


        self.map_templates = {'us_states': {'json': 'us_states.json',
                                       'template':'us_map.html'},
                              'world_map': {'json': 'world-50m.json',
                                       'template':'world_map_Line.html'}}
        

    def _convert_to_geojson(self, df, lat, lon, distance_df=None, index_col=None):
        ''' Dataconversion happens here. Process Dataframes and get 
            necessary information into geojson which is put into the template 
            var dictionary for later'''
        
        ## Support Functions For processing to geojson
        ################################################################################
        def feature_from_row(row):
            if pd.notnull(row[lat]) and pd.notnull(row[lon]):
                return Feature(geometry=Point(( row[lon], row[lat] )))

        def line_feature_from_distance_df():
            """
            create a geojson feature collection of lines from a dataframe with three columns: source/dest/weight
            """
            
            #Create the lookup for lat/long
            ref_df = self.df.set_index( self.samplecolumn )
            
            def create_line_feature(source, target, weight, ref_df=ref_df):
                lat = self.lat
                lon = self.lon
                
                lat1 = ref_df.loc[source][lat]
                lon1 = ref_df.loc[source][lon]
                lat2 = ref_df.loc[target][lat]
                lon2 = ref_df.loc[target][lon]
                return Feature(geometry=LineString([(lon1, lat1), (lon2, lat2)]))
                    
            line_featurelist =  [ create_line_feature( row[0],row[1],row[2] ) for idx,row in self.distdf.iterrows() ]
            return line_featurelist
        
        featurelist= [ feature_from_row(row) for idx, row in df.iterrows() ]
        self.template_vars['geojson'] = geojson.dumps( FeatureCollection(featurelist) )
        line_featurelist = line_feature_from_distance_df() 
        self.template_vars['lines_geojson'] = geojson.dumps( FeatureCollection(line_featurelist) )

LineMap.build_map = build_map
LineMap.create_map = create_map
LineMap.display_map = display_map