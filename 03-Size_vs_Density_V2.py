import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from lib import *

df = pd.read_csv("WPP2024_Demographic_Indicators_Medium.csv.gz", dtype=str)

st.markdown(
"""## Task

Generate a scatter plot showing the relationship between population size and density, 
but this time use the `plotly` graphing library so can have control over the `hover_over` text and other nice features.
""")

st.markdown(
"""## Implementation Outline

* Load dataset, prepare and filter as before.
* Switch to `plotly` scatter plot (called `px.scatter`)

```
import plotly.express as px 
```

Then replace the previous scatter plot command with 

```
fig = px.scatter(df_tmp, 
    x="Population",
    log_x=True,
    y="Density",
    hover_data=["Location"],)
scatter = st.plotly_chart(fig, key="scatter", on_select="rerun")
```

Notice that we did not apply log function to columns `Population` and `Density`.  Instead we passed options `log_x=True` and `log_y=True` to graphing function.  
This generated the more informative point distribution we saw in the previous task but also we have log-based tick marks.

The option `hover_data=["Location"]` adds the column `Location` to the hover over text as desired.
""")

st.markdown(
"""## Result
""")

# year 
df.Time = df.Time.astype(int)
years = df.Time.unique().tolist()
year = st.selectbox("Year:", years, index=years.index(2024))

# location
location_types = df.LocTypeName.dropna().unique().tolist()
location_types.remove("World")
location_type = st.selectbox("Location Type:", location_types, index=location_types.index('Country/Area'))
location_label = location_label(location_type)

# data
df.TPopulation1Jan = df.TPopulation1Jan.astype(float)
df.PopDensity = df.PopDensity.astype(float)

criteria = f"LocTypeName=='{location_type}' and Time=={year}"
columns = ['TPopulation1Jan', 'PopDensity', 'Location', 'ParentID']

df_tmp = (df
    .query(criteria)
    .sort_values("TPopulation1Jan", ascending=False)
    [columns]
).rename(columns={
    'TPopulation1Jan': 'Population',
    'PopDensity': 'Density',
})


st.write(f"### Population (Jan 1st) vs Density in {year} by {location_type}")
fig = px.scatter(df_tmp, 
    x="Population",
    log_x=True,
    y="Density",
    log_y=True,
    hover_data=["Location"],)
scatter = st.plotly_chart(fig, key="scatter", on_select="rerun")
