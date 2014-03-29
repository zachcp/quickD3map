#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function )

import codecs
import pandas as pd
import geojson
from geojson import Point, Feature, FeatureCollection, LineString
from jinja2 import Environment, PackageLoader
from .utilities import projections, latitude,longitude, map_templates
from .check_data import  check_column, check_center, check_samplecolumn, check_projection
from flask import Flask, render_template_string


class BaseMap(object): 
    ''' Check DataFrame Accuracy And Setup Maps '''
    def __init__(self, df, width=960, height=500, scale=100000, 
             geojson="", attr=None, map="world_map", 
             center=None, projection="mercator", title="quickD3Map"):       
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
        self.convert_to_geojson( self.df, self.lat, self.lon)
        map =  self.env.get_template( self.map_templates[self.map]['json'] )
        self.template_vars['map_data'] = map.render()
        #generate html
        html_templ = self.env.get_template(self.map_templates[self.map]['template'])
        self.HTML = html_templ.render(self.template_vars)

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
            


class PointMap(BaseMap): 
    ''' Create a PointMap with quickD3map '''
    def __init__(self, df, width=960, height=500, scale=100000, 
                 geojson="", attr=None, map="world_map", 
                 center=None, projection="mercator", title="quickD3Map"):
                    
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
        

    def convert_to_geojson(self, df, lat, lon, distance_df=None, index_col=None):
        ''' Dataconversion happens here. Process Dataframes and get 
            necessary information into geojson which is put into the template 
            var dictionary for later'''
        ## Support Functions For processing to geojson
        ##############################################
        def feature_from_row(row):
         if pd.notnull(row[lat]) and pd.notnull(row[lon]):
            return Feature(geometry=Point(( row[lon], row[lat] )))
                
        featurelist= [ feature_from_row(row) for idx, row in df.iterrows() ]
        self.template_vars['geojson'] = geojson.dumps( FeatureCollection(featurelist) )
    
#    # Display Fucntions from the BaseMap Class    
#    ###################################################################################
#    def build_map(self): 
#        super(PointMap, self).build_map(self)
#    def create_map(self, path='map.html'): 
#        super(PointMap, self).create_map(self, path=path)
#    def display_map(self): 
#        super(PointMap, self).display_map(self)
