import pandas as pd
from quickD3map import MultiColumnMap

df = pd.read_csv('data/city_population.csv')

MultiColumnMap(df, columns = df.columns, scale_exp=8).display_map()