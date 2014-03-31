#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_quickD3map
----------------------------------

Tests for `quickD3map` module.
"""

import nose.tools as nt
from nose.tools import raises
import pandas as pd
import numpy as np
from itertools import combinations
import geojson
from quickD3map import MultiColumnMap, PointMap, LineMap

from quickD3map.utilities import latitude, longitude, projections
from quickD3map.check_data import check_column, check_center, check_for_NA


#To add: 
#Datachecking tests.
#MapWriting test
# these aren't supergreat but they at least run data through each of the three current classes


## Test That Check DataFrames
#######################################################

@raises(ValueError)
def test_for_Lat_Lon1():
    df = pd.DataFrame( np.random.randn(3,2), columns =["A","B"])
    check_column(df, latitude,"Latitude")

def test_for_Lat_Lon2():
    df = pd.DataFrame( np.random.randn(3,2), columns=["Latitude","Longitude"])
    nt.assert_equal( check_column (df, latitude,"Latitude"), "Latitude" )

@raises(ValueError)   
def test_for_NAs1():
    df = pd.DataFrame( np.random.randn(3,2), columns=["Latitude","Longitude"])
    df.ix[3,'Latitude'] = np.nan
    print(df)
    check_for_NA(df, "Latitude","Longitude")
        
class testcheck_center():
    nt.assert_equals((100,0), check_center( (100,0)) )
    nt.assert_equals([100,0], check_center( [100,0] ) )
    nt.assert_equals( None,   check_center([100,0,10] ))


## Tests That Check GeoJsonConversion
#######################################################
#def test_PointMap_to_geojson():
#    df = pd.DataFrame( {"Latitude": [82.85,87.65,-83.03], "Longitude": [41.68,41.62, -41.12]})
#    pm = PointMap(df)
#    expected_output ="""{"type": "FeatureCollection", "features": [
#              {"geometry": {"type": "Point", "coordinates": [82.85, 41.68]}, "type": "Feature", "id": null, "properties": {}}, 
#              {"geometry": {"type": "Point", "coordinates": [87.67, 41.62]}, "type": "Feature", "id": null, "properties": {}}, 
#              {"geometry": {"type": "Point", "coordinates": [-83.03, -41.12]}, "type": "Feature", "id": null, "properties": {}}] }  
#              """
#    geojson_out = pm.convert_to_geojson()
##    print( geojson.loads(geojson_out) ) 
##    print("okay")
##    print(geojson_out)
##    print(geojson.loads(geojson_out))
##    print("okay")
##    print(geojson.loads(expected_output))
#    nt.assert_equal(geojson.loads(expected_output), geojson.loads(geojson_out))
#    ### Fails becoase of differences in the lenght of the numbers. native pyhton has lon number
#    #but the typed answer has only two digits. SHould I add rounding/decimal to the progrma
#    # or use a different test

## Test That Check BaseMap Object Funcitonality
#######################################################
    

## Test That Check Map Object Funcitonality
#######################################################
def testPointMap():
    df = pd.read_csv('../examples/data/omdf.csv')
    p =  PointMap(df)
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