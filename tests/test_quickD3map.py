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

from quickD3map import MultiColumnMap, PointMap, LineMap

from quickD3map.utilities import latitude, longitude, projections
from quickD3map.check_data import check_column, check_for_NA


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
    check_for_NA(df, "Latitude","Longitude")


class testcheck_center():
    nt.assert_equals((100,0), check_center( (100,0)) )
    nt.assert_equals([100,0], check_center( [100,0] )
    nt.assert_equals( None,   check_center([100,0,10) )
    
    
#def test_for_NAs2():
#    df = pd.DataFrame( np.random.randn(3,2), columns=["Latitude","Longitude"])
#    nt.assert_equal(df, check_for_NA(df, "Latitude","Longitude"))
    
    

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