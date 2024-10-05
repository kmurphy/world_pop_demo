import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from lib import *

df = pd.read_csv("WPP2024_Demographic_Indicators_Medium.csv.gz", dtype=str)

st.markdown(
"""## Task
Construct a line graph showing the change in population over a specified time interval.

* Use `st.select_slider` to select the start and end year.
* Select Location type then select location. 
""")

st.markdown(
"""## Implementation Outline

* load dataset as usual.
* Get the year range using `st.select_slider` as in

```
df.Time = df.Time.astype(int)
years = df.Time.unique().tolist()
start_year, end_year = st.select_slider("Select year range", options=years, value=(2000, 2024))
```

* Select the location type (as in earlier tasks)

* Select the location limited based on the location type

Need to do a query to limited locations.

* Build chart using `st.line_chart`

""")

st.markdown(
"""## Result
""")

# Years
df.Time = df.Time.astype(int)
years = df.Time.unique().tolist()
start_year, end_year = st.select_slider("Select year range", options=years, value=(2000, 2024))
 
# location type
location_types = df.LocTypeName.dropna().unique().tolist()
location_type = st.selectbox("Location Type:", location_types, index=location_types.index('Country/Area'))

# location 
criteria = f"LocTypeName=='{location_type}'"
locations = df.query(criteria).Location.unique()
location = st.selectbox("Location:", locations)

# data
df.TPopulation1Jan = df.TPopulation1Jan.astype(float)
df.Time = df.Time.astype(str)

criteria = f"Location=='{location}' and Time>='{start_year}' and Time<='{end_year}'"
columns = ['Time', 'TPopulation1Jan', 'PopDensity']
df_tmp = (df
    .query(criteria)
    .sort_values("Time", ascending=False)
    [columns]
).rename(columns={
    'TPopulation1Jan': 'Population',
})

st.write(f"### Population from {start_year} to {end_year} in {location}")

st.line_chart(df_tmp, 
              x='Time', x_label='Year',
              y='Population', y_label='Population')
