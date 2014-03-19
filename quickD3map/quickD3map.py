#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30

@author: zachpowers
@description: quick way to make maps from tables with Lat/Long columns
"""

from __future__ import print_function
from __future__ import division


import pandas as pd
import geojson
from geojson import Polygon, Point, Feature, FeatureCollection
from jinja2 import Environment, PackageLoader
from flask import Flask, render_template, Response
from flask_frozen import Freezer
from pkg_resources import resource_string, resource_filename


class PointMap(object):
    def __init__(self, df, location=None , width=960, height=500, scale=100000, geojson="", attr=None,
                 map="world_map"):

        # Check DataFrame for Lat/Lon columns
        assert isinstance(df, pd.core.frame.DataFrame)

        def has_lat(df):
            latitude = ['lat', 'lattitude', 'latitude']
            for col in df.columns:
                if col.strip().lower() in latitude:
                    return col
            raise ValueError("No Latitude Column Found")

        def has_lon(df):
            longitude = ['lon', 'longitude']
            for col in df.columns:
                if col.strip().lower() in longitude:
                    return col
            raise ValueError("No Longitude Value Found")

        self.lat = has_lat(df)
        self.lon = has_lon(df)
        self.df  = df
        self.map = map


        #Templates
        self.env = Environment(loader=PackageLoader('quickD3map', 'templates'))
        self.template_vars = {'width': width, 'height': height, 'scale': scale}


    def _convert_to_geojson(self, df, lat, lon):
        def feature_from_row(row):
            if pd.notnull(row[1][lat]) and pd.notnull(row[1][lon]):
                return Feature(geometry=Point(( row[1][lon], row[1][lat] )))

        featurelist= [ feature_from_row(row) for row in df.iterrows() ]
        self.template_vars['geojson'] = geojson.dumps( FeatureCollection(featurelist) )



    def _build_map(self, html_templ=None):
        '''Build HTML/JS/CSS from Templates given current map type'''

        map_types = {'us_states': {'json': 'us_states.json',
                                   'template':'us_map.html'},
                     'world_map': {'json': 'world-50m.json',
                                   'template':'world_map.html'}}

        self._convert_to_geojson( self.df, self.lat, self.lon)

        #set html and map data
        if self.map in map_types.keys():
            #map background
            map =  self.env.get_template(map_types[self.map]['json'])
            self.template_vars['map_data'] = map.render()
            #main CSS
            #css =  self.env.get_template('bostocks.css')
            #self.template_vars['css'] = css.render()
            #generate html
            html_templ = self.env.get_template(map_types[self.map]['template'])
            self.HTML = html_templ.render(self.template_vars)
        else:
            raise ValueError("Currently Supported Maps are: {}".format(','.join(map_types.keys())))


    def create_map(self, path='map.html', plugin_data_out=True, template=None):
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
            #print path, open(path,'r').read()
            return Response( open(path,'r').read() , mimetype="text/html")

        #config output directory
        #freezer.freeze()
        app.run()
