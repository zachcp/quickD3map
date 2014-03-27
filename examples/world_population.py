#datasources for city data
#http://www.geohive.com/earth/cy_aggmillion2.aspx
#http://dev.maxmind.com/geoip/geoip2/geolite2/

import pandas as pd
from itertools import combinations
from quickD3map import MultiColumnMap, LineMap

df = pd.read_csv('data/city_population.csv')

#Try the MultiColumn Map, only really useful to view the populations
#MultiColumnMap(df, columns = df.columns, scale_exp=8).display_map()

#Take the Top N Cities And create a distance dataframe
smalldf = df.sort('population_2010', ascending=False)[:15]

def return_top(group):
    return group[:1]
    
smalldf = smalldf.groupby('city').apply(return_top)
print smalldf
top_comb = combinations( list(smalldf.city) ,2)
comb = [ [c[0],c[1],1 ] for c in top_comb ]
distance_df = pd.DataFrame(comb)

LineMap( smalldf, "city", distance_df, width=1200,height=700).display_map()