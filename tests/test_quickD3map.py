#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_quickD3map
----------------------------------

Tests for `quickD3map` module.
"""

import nose.tools as nt
import pandas as pd
from itertools import combinations
from jinja2 import Environment, PackageLoader
from quickD3map import MultiColumnMap, PointMap, LineMap
from quickD3map import check_data


#To add: 
#Datachecking tests.
#MapWriting test
# these aren't supergreat but they at least run data through each of the three current classes

def testPointMap():
    df = pd.read_csv('../examples/data/omdf.csv')
    p =  (PointMap(df))
    nt.assert_is_instance(p, PointMap)
    
def testWeather_data():
    df = pd.read_csv('../examples/data/weatherstations.csv')
    mc = MultiColumnMap(df, columns = ['LAT','LON','ELEV'] ,scale_exp = 3)
    nt.assert_is_instance(mc, MultiColumnMap)
    
def testPopulation_data():
    df = pd.read_csv('../examples/data/city_population.csv')    
    smalldf = df.sort('population_2010', ascending=False)[:15]
    def return_top(group):
        return group[:1]
    smalldf = smalldf.groupby('city').apply(return_top)
    top_comb = combinations( list(smalldf.city) ,2)
    comb = [ [c[0],c[1],1 ] for c in top_comb ]
    distance_df = pd.DataFrame(comb)
    lm = LineMap( smalldf, "city", distance_df)
    nt.assert_is_instance(lm, LineMap)