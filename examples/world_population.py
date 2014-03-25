#datasources for city data
#http://www.geohive.com/earth/cy_aggmillion2.aspx
#http://dev.maxmind.com/geoip/geoip2/geolite2/

import pandas as pd
from quickD3map import MultiColumnMap

df = pd.read_csv('data/city_population.csv')

MultiColumnMap(df, columns = df.columns, scale_exp=8).display_map()