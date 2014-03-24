from quickD3map import PointMap
import statsmodels.api as sm
import pandas as pd

#import some data
#quakes = sm.datasets.get_rdataset('quakes','datasets')
#qdf = pd.DataFrame( quakes.data )
oldmaps = sm.datasets.get_rdataset('OldMaps','HistData')
omdf = pd.DataFrame(oldmaps.data)

#make a map
#PointMap(qdf).display_map()
PointMap(omdf).display_map()