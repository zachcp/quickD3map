#quickD3map

### D3 Point Maps from Pandas DataFrames

quickD3map allows you to rapidly generate D3.js maps from data from within 
the pandas/ipython ecosystem by converting Latitude/Longitude Data in to points


####Note: this is an experimental repo and not ready for use.
With that said, basic maps can be generated and below are a few examples of how they are made.


#### To make the following interactive map:
![Examplemap](https://dl.dropboxusercontent.com/u/1803062/quickD3map/map1.png)

#### Install and Use form the Examples Directory

```python
import pandas as pd
from quickD3map import PointMap, MultiColumnMap
 
#load data and plot 
stations = pd.read_csv('data/weatherstations.csv')
MultiColumnMap(stations, columns = ['LAT','LON','ELEV']).display_map()
````
 
quickD3map creates a template file and then runs Flask App to display it.
```python
from quickD3map import PointMap
import statsmodels.api as sm
import pandas as pd

#import some data
quakes = sm.datasets.get_rdataset('quakes','datasets')
qdf = pd.DataFrame( quakes.data )
oldmaps = sm.datasets.get_rdataset('OldMaps','HistData')
omdf = pd.DataFrame(oldmaps.data)

#make a map
PointMap(qdf).display_map()
PointMap(omdf).display_map()
````

###Project Goals
The goal of this project is rather limited in scope: 
  - be able to rapidly plot location data from Pandas dataframes
  - be able to color by another column
  - be able to scale by another column
  - be able to plot connections between plots
  
I intend to include several map templates (geojson files) and will try to 
figure out a template style that can provide the ability to include maps of many types.
Just thinking aloud here but the best way to do this would be to standardize the 
geojson input types for features so that loading of data (as JSOn strings) can be seperated
from everything else (transformation,scaling, etc.)


###Thanks.
To Mike Bostocks and the D3JS team, as well as to Rob Story and the Folium libary.
