#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function )

import codecs
import warnings
import pandas as pd


from jinja2 import Environment, PackageLoader
from flask  import Flask, render_template_string
from IPython.display import HTML

from .utilities import  latitude,longitude, map_templates
from .check_data import  check_column, check_center, check_projection


class BaseMap(object): 
    ''' Check DataFrame Accuracy And Setup Maps '''
    def __init__(self, df, width=960, height=500, map="world_map", 
                 center=None, projection="mercator", title= None,
                 scale_exp=2, graticule=False, ipython=False):       
        '''
        The BaseMap class is here to handle all of the generic aspects of
        setting up a Latitude and Longitude based map. These aspects are:
            1. Verifying the Pandas Dataframe (lat/long columns, NAs)
            2. Setting up and holding template information.
            
        This is a private class used by other classes but not the User.
    
         Parameters
        ----------
        df: pandas dataframe, required.
            dataframe with latitude and longitude columns.
        width: int, default 960
            Width of the map.
        height: int, default 500
            Height of the map.
        map: str, default "world_map".
           template to be used for mapping.
        scale_exp: int, default 2
            used to define the size scaling exponent for circles. 3 = 10^3, 6=10^6
        projection: str, default="mercator"
           a projection that is one of the projecions recognized by d3.js
        center: tuple or list of two. default=None
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
        self.title=  title
        self.scale_exp = scale_exp
        self.ipython = ipython
        self.graticule = graticule
    
        #Template Information Here
        self.env = Environment(loader=PackageLoader('quickD3map', 'templates'))
        self.template_vars = {'width': width, 'height': height, 'center': self.center,
                              'projection':self.projection, "title":self.title, "ipython":self.ipython,
                               'scale_exp':self.scale_exp, 'graticule':self.graticule}
                              
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
        

    def create_map(self, path='map.html'):
        ''' utility function used by all map classes 
            to write Map to file

        Parameters:
        -----------
        path: string, default 'map.html'
            Path for HTML output for map
        '''
        self.build_map()
        with codecs.open(path, 'w','utf-8') as f:
            f.write(self.HTML)

    def display_map(self):
        ''' utility function used by all map classes 
            to display map. Creates a Flask App.
            Down the line maybe an IPython Widget as well?
        '''
        
        try:
            #pass
            warnings.warn("display map sumthin")
            self.build_map()
            return HTML( self.HTML )
        except:
            print("IPython not found: plotting in a webserver")
            app = Flask(__name__)
            self.build_map()
            @app.route('/')
            def index():
                return render_template_string(self.HTML)
            app.run()

        print("IPython not found: plotting in a webserver")
        app = Flask(__name__)
        self.build_map()
        @app.route('/')
        def index():
            return render_template_string(self.HTML)
        app.run()
        
        
    def _repr_html_(self):
            """Build the HTML representation for IPython."""
            vis_id = str(uuid4()).replace("-", "")
            html = """<div id="vis%s"></div>
            <script>
               ( function() {
                 var _do_plot = function() {
                   if (typeof vg === 'undefined') {
                     window.addEventListener('vincent_libs_loaded', _do_plot)
                     return;
                   }
                   vg.parse.spec(%s, function(chart) {
                     chart({el: "#vis%s"}).update();
                   });
                 };
                 _do_plot();
               })();
            </script>
            <style>.vega canvas {width: 100%%;}</style>
            """ % (vis_id, self.to_json(pretty_print=False), vis_id)
            return html
