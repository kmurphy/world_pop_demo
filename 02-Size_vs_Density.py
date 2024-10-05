import streamlit as st
import pandas as pd
import numpy as np

from lib import *

df = pd.read_csv("WPP2024_Demographic_Indicators_Medium.csv.gz", dtype=str)

st.markdown(
"""## Task

Generate a scatter plot showing the relationship between population size and density.

* Use columns Use selection box to select location type (see column `LocTypeName`).
* Use selection box to select year (see column `time`), and default to current year.
""")

st.markdown(
"""## Implementation Outline

* Load dataset and filter as before.
* Use `scatter_chart` to generate scatter plot.

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

df_tmp["Log(Population)"] = np.log(df_tmp.Population)
df_tmp["Log(Density)"] = np.log(df_tmp.Density)


st.write(f"### Population (Jan 1st) vs Density in {year} by {location_type}")
st.scatter_chart(df_tmp, 
    x="Population", x_label="Population (as on Jan 1st)",
    y="Density", y_label="Density (population / sq km)")

st.markdown(
"""### Improvements

**Better Scale**

The above scatter plot is technically correct but practically useless, 
since range of data points is large and uneven. 
Better to switch to log scale. Define new columns using 
(you have already imported `numpy as np` haven't you), etc.

```
df_tmp["Log(Population)"] = np.log(df_tmp.Population)
```
""")

st.write("To generate the following:")

st.write(f"### Population (Jan 1st) vs Density in {year} by {location_type}")
st.scatter_chart(df_tmp, 
    x="Log(Population)", x_label="Log(Population) (as on Jan 1st)",
    y="Log(Density)", y_label="Log (Density) (population / sq km)",)

st.write("The point distribution is more informative but the axis labels are not ideal. (It would be nicer if the tick marks were log-based.)")
st.markdown(
"""**Better Hover over text**

If you hover over a point we see the data values. It would be nice if we could also see 
extra information such as the location name, etc. 
We need to switch to a more advanced plotting library for this - see next task.  
""")