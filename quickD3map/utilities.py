# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 11:52:51 2014

@author: zachpowers
"""

import codecs
from flask import Flask, render_template_string

## Global Variables
#####################################################
latitude =  ['lat', 'lattitude', 'latitude']
longitude = ['lon','long', 'longitude']
 
projections = [ 'airy', 'aitoff', 'albers', 'albersUsa', 'armadillo', 'august', 'azimuthalEqualArea',
 'azimuthalEquidistant', 'baker', 'berghaus', 'boggs', 'bonne', 'bromley', 'chamberlin', 'collignon',
 'conicEqualArea', 'conicConformal', 'conicEquidistant', 'equirectangular', 'craig', 'craster',
 'cylindrical-equal-area', 'cylindrical-stereographic', 'eckert1', 'eckert2', 'eckert3', 'eckert4',
 'eckert5', 'eckert6', 'eisenlohr', 'elliptic', 'fahey', 'foucaut', 'gilbert', 'ginzburg-polyconic',
 'ginzburg4', 'ginzburg5', 'ginzburg6', 'ginzburg8', 'ginzburg9', 'gnomonic', 'gringorten', 'guyou',
 'hammer-retroazimuthal', 'hammer', 'hatano', 'healpix', 'hill', 'homolosine', 'hyperbolic', 'kavrayskiy7', 'lagrange',
 'larrivee', 'laskowski', 'littrow', 'loximuthal', 'mercator', 'miller',
 'modified-stereographic', 'mollweide', 'mt-flat-polar-parabolic', 'mt-flat-polar-quartic',
 'mt-flat-polar-sinusoidal', 'natural-earth', 'nell-hammer', 'orthographic', 'parallel1', 'parallel2',
 'peirce-quincuncial', 'polyconic', 'quincuncial', 'rectangular-polyconic', 'robinson', 'satellite',
 'sinu-mollweide', 'sinusoidal', 'stereographic', 'times', 'transverseMercator', 'two-point-azimuthal',
 'two-point-equidistant', 'van-der-grinten', 'van-der-grinten2', 'van-der-grinten3', 'van-der-grinten4', 'wagner4', 'wagner6',
 'wagner7', 'wiechel', 'winkel3']

## Display Funcitons
#####################################################
def create_map(self, path='map.html'):
    ''' utility function used by all map classes 
        to write Map to file
    
    Parameters:
    -----------
    path: string, default 'map.html'
        Path for HTML output for map
    '''
    self._build_map()
    with codecs.open(path, 'w') as f:
        f.write(self.HTML)
        
def display_map(self):
    ''' utility function used by all map classes 
        to display map. Creates a Flask App.
        Down the line maybe an Ipyhon Widget as well?
    '''
    app = Flask(__name__)
    self._build_map()
    @app.route('/')
    def index():
        return render_template_string(self.HTML)
    app.run()