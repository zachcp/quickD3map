#!/usr/bin/env python

import pandas as pd
from quickD3map import PointMap, MultiColumnMap
 
#load data and rename incompatible columns
# you could also rename axis using rename_axis(lambda x: x.split(' ')[0,axis = 1])
stations = pd.read_csv('data/weatherstations.csv')
station_data  = pd.read_csv('data/weatherdata.csv')

#merge the data and Plot
df = pd.merge(stations, station_data, left_on="USAF", right_on="STN---")

#points are too small try:
#PointMap(df).display_map() \
#PointMap(df, scale = 1000000).display_map()

columns = ['TEMP', 'DEWP', 'SLP', 'STP', 'VISIB', 'WDSP', 'MXSPD']
MultiColumnMap(df, columns = columns,scale = 1000000).display_map()

#too many points. and too big. more on that later