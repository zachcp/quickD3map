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
                         'template': 'world_map_Line.html'}}
        
projections = {'airy': 'airy',
 'aitoff': 'aitoff',
 'albers': 'albers',
 'albersUsa': 'albersUsa',
 'armadillo': 'armadillo',
 'august': 'august',
 'azimuthalEqualArea': 'azimuthalEqualArea',
 'azimuthalEquidistant': 'azimuthalEquidistant',
 'baker': 'baker',
 'berghaus': 'berghaus',
 'boggs': 'boggs',
 'bonne': 'bonne',
 'bromley': 'bromley',
 'chamberlin': 'chamberlin',
 'collignon': 'collignon',
 'conicConformal': 'conicConformal',
 'conicEqualArea': 'conicEqualArea',
 'conicEquidistant': 'conicEquidistant',
 'craig': 'craig',
 'craster': 'craster',
 'cylindrical-equal-area': 'cylindrical-equal-area',
 'cylindrical-stereographic': 'cylindrical-stereographic',
 'eckert1': 'eckert1',
 'eckert2': 'eckert2',
 'eckert3': 'eckert3',
 'eckert4': 'eckert4',
 'eckert5': 'eckert5',
 'eckert6': 'eckert6',
 'eisenlohr': 'eisenlohr',
 'elliptic': 'elliptic',
 'equirectangular': 'equirectangular',
 'fahey': 'fahey',
 'foucaut': 'foucaut',
 'gilbert': 'gilbert',
 'ginzburg-polyconic': 'ginzburg-polyconic',
 'ginzburg4': 'ginzburg4',
 'ginzburg5': 'ginzburg5',
 'ginzburg6': 'ginzburg6',
 'ginzburg8': 'ginzburg8',
 'ginzburg9': 'ginzburg9',
 'gnomonic': 'gnomonic',
 'gringorten': 'gringorten',
 'guyou': 'guyou',
 'hammer': 'hammer',
 'hammer-retroazimuthal': 'hammer-retroazimuthal',
 'hatano': 'hatano',
 'healpix': 'healpix',
 'hill': 'hill',
 'homolosine': 'homolosine',
 'hyperbolic': 'hyperbolic',
 'kavrayskiy7': 'kavrayskiy7',
 'lagrange': 'lagrange',
 'larrivee': 'larrivee',
 'laskowski': 'laskowski',
 'littrow': 'littrow',
 'loximuthal': 'loximuthal',
 'mercator': 'mercator',
 'miller': 'miller',
 'modified-stereographic': 'modified-stereographic',
 'mollweide': 'mollweide',
 'mt-flat-polar-parabolic': 'mt-flat-polar-parabolic',
 'mt-flat-polar-quartic': 'mt-flat-polar-quartic',
 'mt-flat-polar-sinusoidal': 'mt-flat-polar-sinusoidal',
 'natural-earth': 'naturalEarth',
 'nell-hammer': 'nell-hammer',
 'orthographic': 'orthographic',
 'parallel1': 'parallel1',
 'parallel2': 'parallel2',
 'peirce-quincuncial': 'peirce-quincuncial',
 'polyconic': 'polyconic',
 'quincuncial': 'quincuncial',
 'rectangular-polyconic': 'rectangular-polyconic',
 'robinson': 'robinson',
 'satellite': 'satellite',
 'sinu-mollweide': 'sinu-mollweide',
 'sinusoidal': 'sinusoidal',
 'stereographic': 'stereographic',
 'times': 'times',
 'transverseMercator': 'transverseMercator',
 'two-point-azimuthal': 'two-point-azimuthal',
 'two-point-equidistant': 'two-point-equidistant',
 'van-der-grinten': 'van-der-grinten',
 'van-der-grinten2': 'van-der-grinten2',
 'van-der-grinten3': 'van-der-grinten3',
 'van-der-grinten4': 'van-der-grinten4',
 'wagner4': 'wagner4',
 'wagner6': 'wagner6',
 'wagner7': 'wagner7',
 'wiechel': 'wiechel',
 'winkel3': 'winkel3'}


## IPython Functions
######################################################################

def initialize_notebook():
    """Initialize the IPython notebook display elements"""
    try:
        from IPython.core.display import display, HTML
    except ImportError:
        print("IPython Notebook could not be loaded.")

    # Thanks to @jakevdp:
    # https://github.com/jakevdp/mpld3/blob/master/mpld3/_display.py#L85
    load_lib = """
                function vct_load_lib(url, callback){
                      if(typeof d3 !== 'undefined' &&
                         url === 'http://d3js.org/d3.v3.min.js'){
                        callback()
                      }
                      var s = document.createElement('script');
                      s.src = url;
                      s.async = true;
                      s.onreadystatechange = s.onload = callback;
                      s.onerror = function(){
                        console.warn("failed to load library " + url);
                        };
                      document.getElementsByTagName("head")[0].appendChild(s);
                };
                var vincent_event = new CustomEvent(
                  "vincent_libs_loaded",
                  {bubbles: true, cancelable: true}
                );
                """
    lib_urls = [
        "'http://d3js.org/d3.v3.min.js'",
        "'http://d3js.org/d3.geo.projection.v0.min.js'",
        "'http://wrobstory.github.io/d3-cloud/d3.layout.cloud.js'",
        "'http://wrobstory.github.io/vega/vega.v1.3.3.js'"
    ]
    get_lib = """vct_load_lib(%s, function(){
                  %s
                  });"""
    load_js = get_lib
    ipy_trigger = "window.dispatchEvent(vincent_event);"
    for elem in lib_urls[:-1]:
        load_js = load_js % (elem, get_lib)
    load_js = load_js % (lib_urls[-1], ipy_trigger)
    html = """
           <script>
               %s
               function load_all_libs(){
                  console.log('Loading Vincent libs...')
                  %s
               };
               if(typeof define === "function" && define.amd){
                    if (window['d3'] === undefined ||
                        window['topojson'] === undefined){
                        require.config(
                            {paths: {
                              d3: 'http://d3js.org/d3.v3.min',
                              topojson: 'http://d3js.org/topojson.v1.min'
                              }
                            }
                          );
                        require(["d3"], function(d3){
                            console.log('Loading Vincent from require.js...')
                            window.d3 = d3;
                            require(["topojson"], function(topojson){
                                window.topojson = topojson;
                                load_all_libs();
                            });
                        });
                    } else {
                        load_all_libs();
                    };
               }else{
                    console.log('Require.js not found, loading manually...')
                    load_all_libs();
               };

           </script>""" % (load_lib, load_js,)
    return display(HTML(html))

