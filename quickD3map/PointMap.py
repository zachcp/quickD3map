#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function )

import pandas as pd
import geojson

from geojson import Point, Feature, FeatureCollection

from .BaseMap import BaseMap

class PointMap(BaseMap): 
    ''' Create a PointMap with quickD3map '''
    def __init__(self, df, columns = None, legend=False, scale_exp=4, width=960, height=500, scale=100000, 
                 geojson="", attr=None, map="world_map_multiple", center=None, projection="mercator", title="quickD3Map"):
                    
        '''
        PointMap is a class that takes a dataframe and returns an html webpage that
        can optionally be viewed as a Flask Webapp. Pointmap requires a pandas dataframe
        with latitude and longitude options.
        
         Parameters
        ----------
        df: pandas dataframe, required.
            dataframe with latitude and longitude columns.
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
        super(PointMap, self).__init__(df=df,center=center, projection=projection)
        self.columns = columns
        self.scale_exp = scale_exp
        self.legend = legend
        self.map = map
         
        
        self.template_vars['legend'] = self.legend
        self.template_vars['columns'] = self.columns
        self.template_vars['title'] = title
        self.template_vars['scale_exp'] = scale_exp
        
        #TODO
        #check that the column values do not have have NAs in them.


#    def convert_to_geojson(self ):
#        ''' Dataconversion happens here. Process Dataframes and get 
#            necessary information into geojson which is put into the template 
#            var dictionary for later'''
#        lat = self.lat
#        lon = self.lon
#        df  = self.df
#        ## Support Functions For processing to geojson
#        ##############################################
#        def feature_from_row(row):
#         if pd.notnull(row[lat]) and pd.notnull(row[lon]):
#            return Feature(geometry=Point(( row[lon], row[lat] )))
#                
#        featurelist= [ feature_from_row(row) for idx, row in df.iterrows() ]
#        geojson_out = geojson.dumps( FeatureCollection(featurelist) )
#        self.template_vars['geojson'] = geojson_out
    
    def convert_to_geojson(self):
        ''' Dataconversion happens here. Process Dataframes and get 
            necessary information into geojson which is put into the template 
            var dictionary for later'''
        lat, lon, df, columns = self.lat, self.lon, self.df, self.columns
        
        ## Support Functions For processing to geojson
        ################################################################################
        def feature_from_row(row):
            """ Check for NA in Lat and Lon.
                Check for Columns. Return GeoJson for inclusion as points.
            """
            if pd.notnull( row[lat]) and pd.notnull(row[lon]):
                if columns:                
                    properties = { k:v for k,v in row.iterkv() if k in columns}
                    return Feature(geometry=Point(( row[lon], row[lat] )),
                                   properties=properties)
                else:
                    return Feature(geometry=Point(( row[lon], row[lat] )))
                    

        featurelist= [ feature_from_row(row) for idx, row in df.iterrows() ]
        self.template_vars['geojson'] = geojson.dumps( FeatureCollection(featurelist) )

        