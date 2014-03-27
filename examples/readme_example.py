from quickD3map import PointMap
import statsmodels.api as sm
import pandas as pd

#import some data
#quakes = sm.datasets.get_rdataset('quakes','datasets')
#qdf = pd.DataFrame( quakes.data )
#oldmaps = sm.datasets.get_rdataset('OldMaps','HistData')
#omdf = pd.DataFrame(oldmaps.data)

#omdf.to_csv('data/omdf.csv', index=False)
omdf = pd.read_csv('data/omdf.csv')
#make a map
#PointMap(qdf).display_map()
print len(omdf)
omdf = omdf[:100]
PointMap(omdf, width=1200, height=600).display_map()