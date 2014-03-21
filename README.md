#quickD3map

### D3 Point Maps from Pandas DataFrames

quickD3map allows you to rapidly generate D3.js maps from data from within 
the pandas/ipython ecosystem by converting Latitude/Longitude Data in to points


##Note: this is an experimental repo and not ready for use.
With that said, basic maps can be generated and below are a few examples of how they are made.


```python
#import some data
from quickD3map import PointMap
import statsmodels.api as sm
quakes = sm.datasets.get_rdataset('quakes','datasets')
qdf = pd.DataFrame( quakes.data )


PointMap(qdf).display_map()

````