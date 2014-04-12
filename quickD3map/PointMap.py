#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function )

import pandas as pd
import geojson
from geojson import Point, Feature, FeatureCollection
from .BaseMap import BaseMap
from .utilities import map_templates


class PointMap(BaseMap): 
    ''' Create a PointMap with quickD3map '''
    def __init__(self, df, columns = None, title="quickD3Map", legend=False, scale_exp=4,  
                  map="world_map", projection="mercator", **kwargs):
                    
        '''
        The PointMap class takes a dataframe with Lat/lon columns and maps the point onto a map.
        The optional `columns` argument will provide an interactive map that can be scaled by column values.
        
        Parameters
        ----------
        df: pandas dataframe, required.
            dataframe with latitude and longitude columns.
        columns: list of columsn in the df, default None
            if columns are specified, the map created by create_map or 
            display_map will allwo scaling of points based on column values.
        scale_exp: int, default 4
            scale factor for the sizing plotted points. This is a d3.range that determines the scale
            over which values will be plotted. Using "3" will provide an appropriate scale for features
            with values going to 10^3; "6" would be good for values going to  10^6
        map: str, default "world_map".
           template to be used for mapping. 
       
       For Future Implementation: Currently Mercator is the default.
        center: list of legth two: lat/long (default=[-100, 0])
           provides a new center for the map
        projection: str, default="mercator"
           a projection that is one of the projecions recognized by d3.js
        
        Returns
        -------
        PointMap object that can be used with the two methods below.
        
        
        Methods
        -------
        create_map(path="map.html")
            creates a single HTML file with with all JS/CSS/geojson included.
        display_map()
            will run a Flask Webapp displaying your map.
        
        
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
        super(PointMap, self).__init__(df=df, projection=projection, **kwargs)
        self.columns = columns
        self.scale_exp = scale_exp
        self.legend = legend
        
        if map in map_templates.keys():
            self.map = map
        else:
            raise ValueError("Map type must be one of the following:{}".format(map_templates.keys()))
        
        self.template_vars['legend'] = self.legend
        self.template_vars['columns'] = self.columns
        self.template_vars['title'] = title
        self.template_vars['scale_exp'] = scale_exp
        
    
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

        