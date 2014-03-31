#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function )

import codecs
import pandas as pd

from jinja2 import Environment, PackageLoader
from flask  import Flask, render_template_string

from .utilities import  latitude,longitude, map_templates
from .check_data import  check_column, check_center, check_projection


class BaseMap(object): 
    ''' Check DataFrame Accuracy And Setup Maps '''
    def __init__(self, df, width=960, height=500, scale=100000, 
             geojson="", attr=None, map="world_map", 
             center=None, projection="mercator", title="quickD3Map"):       
        '''
        The BaseMap class is here to handle all of the generic aspects of setting
        up a Latitude and Longitude based map. These aspects are:
            1. Verifying the Pandas Dataframe (lat/long columns, NAs)
            2. Setting up and holdign template information
    
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
    
        projection: str, default="mercator"
           a projection that is one of the projecions recognized by d3.js
    
        '''
        # Check Inputs For Bad or Inconsistent Data
        assert isinstance(df, pd.core.frame.DataFrame)
        self.df  = df
        self.lat = check_column(self.df, latitude,  'latitude')
        self.lon = check_column(self.df, longitude, 'longitude')
        self.map = map
        self.center= check_center(center)
        self.projection = check_projection(projection)
    
    
        #Template Information Here
        self.env = Environment(loader=PackageLoader('quickD3map', 'templates'))
        self.template_vars = {'width': width, 'height': height, 'scale': scale, 
                              'center': self.center, 'projection':self.projection}
        
        #add all template combinations. Specify Template Subsets in map classes
        self.map_templates = map_templates
                                   
        #JS Libraries and CSS Styling
        self.template_vars['d3_projection'] =  self.env.get_template('d3.geo.projection.v0.min.js').render()
        self.template_vars['topojson'] =  self.env.get_template('topojson.v1.min.js').render()
        self.template_vars['d3js'] =  self.env.get_template('d3.v3.min.js').render()
        self.template_vars['style'] =  self.env.get_template('style.css').render()
        self.template_vars['colorbrewer_css'] =  self.env.get_template('colorbrewer.css').render()
        self.template_vars['colorbrewer_js'] =  self.env.get_template('colorbrewer.js').render()

    ## Display Methods
    ########################################################################################   
    def build_map(self):
        '''Build HTML/JS/CSS from Templates given current map type'''
        self.convert_to_geojson()
        map =  self.env.get_template( self.map_templates[self.map]['json'] )
        self.template_vars['map_data'] = map.render()
        #generate html
        html_templ = self.env.get_template(self.map_templates[self.map]['template'])
        self.HTML = html_templ.render(self.template_vars)
        #print(self.template_vars)
        #print(self.template_vars.keys())
        

    def create_map(self, path='map.html'):
        ''' utility function used by all map classes 
            to write Map to file

        Parameters:
        -----------
        path: string, default 'map.html'
            Path for HTML output for map
        '''
        self.build_map()
        with codecs.open(path, 'w') as f:
            f.write(self.HTML)

    def display_map(self):
        ''' utility function used by all map classes 
            to display map. Creates a Flask App.
            Down the line maybe an Ipyhon Widget as well?
        '''
        app = Flask(__name__)
        self.build_map()
        @app.route('/')
        def index():
            return render_template_string(self.HTML)
        app.run()