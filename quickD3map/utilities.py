# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 11:52:51 2014

@author: zachpowers
"""


## Global Variables
#####################################################
latitude =  ['lat', 'lattitude', 'latitude']
longitude = ['lon','long', 'longitude']


#set global json/html combinations here. In the class specify allowable subsets.
map_templates = {'us_states': 
                        {'json':      'us_states.json',
                         'template':  'us_map.html'},
                 'world_map': 
                        {'json':      'world-110m.json',
                         'template':   'world_map.html'},
                 'world_map_50m': 
                        {'json':  'world-50m.json',
                         'template':  'world_map.html'},                              
                 'world_map_zoom': 
                        {'json': 'world-50m.json',
                         'template': 'world_map_Line_zoom.html'},
                 'world_map_multiple': 
                        {'json': 'world-110m.json',
                         'template': 'world_map_multiplesamples.html'}}
        
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

