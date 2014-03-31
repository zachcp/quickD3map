#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function )

import pandas as pd
import geojson

from geojson import Point, Feature, FeatureCollection, LineString

from .check_data import check_samplecolumn, verify_dfs_forLineMap 
from .BaseMap import BaseMap

class LineMap(BaseMap): 
    ''' Create a PointMap with quickD3map '''
    def __init__(self, df, samplecolumn, distance_df,  scale=100000, 
                 map="world_map_zoom", center=None, projection="mercator", title=None):
                    
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
        # Basic Data Check Using the BaseClass        
        super(LineMap, self).__init__(df=df,center=center, projection=projection)
        
        ##  Support Functions to Verify Data
        ################################################################################
        
        # Check Inputs and make assignments of data
        assert isinstance(df, pd.core.frame.DataFrame)
        assert isinstance(distance_df, pd.core.frame.DataFrame)
        
        if verify_dfs_forLineMap(df, samplecolumn, distance_df):
            self.distdf = distance_df
        self.samplecolumn = check_samplecolumn(self.df, samplecolumn)
        self.title= title
        self.map = map

    def convert_to_geojson(self):
        ''' Dataconversion happens here. Process Dataframes and get 
            necessary information into geojson which is put into the template 
            var dictionary for later'''
        lat, lon, df = self.lat, self.lon, self.df
        
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