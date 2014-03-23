#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function )

#import json
import pandas as pd
import geojson
from geojson import Point, Feature, FeatureCollection, LineString
from jinja2 import Environment, PackageLoader
from flask import Flask, Response
from .projections import projections



class PointMap(object):
    def __init__(self, df, location=None , width=960, height=500, scale=100000, geojson="", attr=None,
                 map="world_map", distance_df=None, samplecolumn= None, center=None, projection="mercator"):

        # Check DataFrame for Lat/Lon columns
        assert isinstance(df, pd.core.frame.DataFrame)

        def has_lat(df):
            latitude = ['lat', 'lattitude', 'latitude']
            for col in df.columns:
                if col.strip().lower() in latitude:
                    return col
            raise ValueError("No Latitude Column Found")

        def has_lon(df):
            longitude = ['lon','long', 'longitude']
            for col in df.columns:
                if col.strip().lower() in longitude:
                    return col
            raise ValueError("No Longitude Value Found")

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
                print('In the absence of an explicit sample column we are setting Samplecolumn to "None"')
                return None
                
        
        def check_projection(projection):
            if projection in projections:
                return projection
            else:
                print('This is not a valid projection, using default=mercator')
                return "mercator"
                        
        self.lat = has_lat(df)
        self.lon = has_lon(df)
        self.df  = df
        self.map = map
        self.distdf = load_distance_df(distance_df, df) 
        self.samplecolumn = check_samplecolumn(samplecolumn)
        self.center= check_center(center)
        self.projection = check_projection(projection)
        
        
        #Templates
        self.env = Environment(loader=PackageLoader('quickD3map', 'templates'))
        self.template_vars = {'width': width, 'height': height, 'scale': scale, 
                              'center': self.center, 'projection':self.projection}


    def _convert_to_geojson(self, df, lat, lon, distance_df=None, index_col=None):
        
        
        def feature_from_row(row):
            if pd.notnull(row[lat]) and pd.notnull(row[lon]):
                return Feature(geometry=Point(( row[lon], row[lat] )))

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

    def _build_map(self, html_templ=None):
        '''Build HTML/JS/CSS from Templates given current map type'''

        map_types = {'us_states': {'json': 'us_states.json',
                                   'template':'us_map.html'},
                     'world_map': {'json': 'world-50m.json',
                                   'template':'world_map.html'},
                     'world_map_mercator': {'json': 'world-50m.json',
                                 'template':'world_map_mercator.html'},
                     'world_map_zoom': {'json': 'world-50m.json',
                                 'template':'world_map_zoom.html'}}

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

    def create_map(self, path='map.html', lines=False, plugin_data_out=True, template=None):
        '''Write Map output to HTML and data output to JSON if available

        Parameters:
        -----------
        path: string, default 'map.html'
            Path for HTML output for map
        plugin_data_out: boolean, default True
            If using plugins such as awesome markers, write all plugin
            data such as JS/CSS/images to path
        template: string, default None
            Custom template to render
        '''
        self._build_map(template)

        with open(path, 'w') as f:
            f.write(self.HTML)
            
    def display_map(self, path='map.html', template=None):
        app = Flask(__name__)
        
        self.create_map(path=path,template=template)
        @app.route('/', methods=['GET'])
        def index():
            return Response( open(path,'r').read() , mimetype="text/html")
        app.run()