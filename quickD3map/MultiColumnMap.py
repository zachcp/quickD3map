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
import codecs
from geojson import Point, Feature, FeatureCollection, LineString
from jinja2 import Environment, PackageLoader

from .utilities import create_map, display_map, projections, latitude,longitude



class MultiColumnMap(object): 
    ''' Create a PointMap of multiple columns with d3.js'''
    def __init__(self, df, columns = None,width=900, height=500, scale_exp=3, 
                 geojson="", attr=None, map="world_map_multiple_samples", distance_df=None, 
                 samplecolumn= None, center=None, projection="mercator"):
                    
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
        
        ##  Support Functions to Verify Data
        ################################################################################
 
         def check_column(df, namelist, name):
            for col in df.columns:
                if col.strip().lower() in namelist:
                    return col
            raise ValueError("No {} Column Found in the Dataframe".format(name))
            
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
                
        def check_center(center):
            try:
                if isinstance(center, tuple):
                    return center
            except:
                print("Center Must be a Tuple")
                return None
            
        def check_samplecolumn(samplecolumn):
            if samplecolumn in self.df.columns:
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
        
        # Check Inputs and make assignemtns of data
        assert isinstance(df, pd.core.frame.DataFrame)
        self.df  = df
        self.lat = check_column(self.df, latitude,  'latitude')
        self.lon = check_column(self.df, longitude, 'longitude')
        self.map = map
        self.distdf = load_distance_df(distance_df, df) 
        self.samplecolumn = check_samplecolumn(samplecolumn)
        self.center= check_center(center)
        self.projection = check_projection(projection)
        self.columns = columns
        self.scale_exp = scale_exp 
        
        
        #Templates
        self.env = Environment(loader=PackageLoader('quickD3map', 'templates'))
        self.template_vars = {'width': width, 'height': height, 
                              'center': self.center, 'projection':self.projection,
                              'columns': self.columns, 'scale_exp': self.scale_exp}
        
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

        def line_feature_from_distance_df():
            """
            create a geojson feature collection of lines from a dataframe with three columns: source/dest/weight
            """
            
            #Create the lookup for lat/long
            if self.samplecolumn is None:
                try:
                    cols = self.df.columns 
                    ref_df = self.df.set_index( self.df[ cols[0] ] )
                    print("Without Explicit Sample Column, I will attempt to use the first column")
                except:
                    raise ValueError('First Column cannot be used as the Sample Index')
            else:
                try:
                    ref_df = self.df.set_index( self.samplecolumn )
                except:
                    raise ValueError("Issue with Index/Sample Column")
            

            def create_line_feature(source, target, weight, ref_df):
                lat = self.lat
                lon = self.lon
                
                lat1 = ref_df.loc[source][lat]
                lon1 = ref_df.loc[source][lon]
                lat2 = ref_df.loc[target][lat]
                lon2 = ref_df.loc[target][lon]
                
                nullcheck = [ pd.notnull( l ) for l in [lat1,lon1,lat2,lon2] ]
                
                if False not in nullcheck:
                    return Feature(geometry=LineString([(lon1, lat1), (lon2, lat2)]))
        
            line_featurelist =  [ create_line_feature( row[0],row[1],row[2], ref_df) for idx,row in self.distdf.iterrows() ]
            return line_featurelist
        
        
        featurelist= [ feature_from_row(row) for idx, row in df.iterrows() ]
        self.template_vars['geojson'] = geojson.dumps( FeatureCollection(featurelist) )
        
        if self.distdf is not None:
            line_featurelist = line_feature_from_distance_df() 
            self.template_vars['lines_geojson'] = geojson.dumps( FeatureCollection(line_featurelist) )

    def _build_map(self):
        '''Build HTML/JS/CSS from Templates given current map type'''

        map_types = {'us_states': {'json': 'us_states.json',
                                   'template':'us_map.html'},
                     'world_map': {'json': 'world-50m.json',
                                   'template':'world_map.html'},
                     'world_map_multiple_samples': {'json': 'world-50m.json',
                                   'template':'world_map_multiplesamples.html'}}

        self._convert_to_geojson( self.df, self.lat, self.lon)

        #set html and map data
        if self.map in map_types.keys():
            #map background
            map =  self.env.get_template(map_types[self.map]['json'])
            self.template_vars['map_data'] = map.render()
            #generate html
            html_templ = self.env.get_template(map_types[self.map]['template'])
            self.HTML = html_templ.render(self.template_vars)
            print(self.template_vars.keys())
        else:
            raise ValueError("Currently Supported Maps are: {}".format(','.join(map_types.keys())))

MultiColumnMap.create_map = create_map
MultiColumnMap.display_map = display_map
