import streamlit as st
import pandas as pd

from lib import *

df = pd.read_csv("WPP2024_Demographic_Indicators_Medium.csv.gz")

st.markdown(
"""## Task

Generate top 5 region/country/etc by population for a given year.

* Use selection box to select location type (see column `LocTypeName`).
* Use selection box to select year (see column `time`), and default to current year.
""")


st.markdown(
"""## Implementation Outline

* Loading the dataset

To avoid problems with columns being incorrectly converted. 
The data is imported with `dtype=str` option (so all columns are treated as string).

```
df = pd.read_csv("WPP2024_Demographic_Indicators_Medium.csv.gz", dtype=str)
```

* We want to select the year, so we convert column containing the year 
(column `Time`) to integer and build a list of unique values. 

```
df.Time = df.Time.astype(int)
years = df.Time.unique().tolist(
```

Then build selection box and set default value (by setting the index to the 
position of the required default value in the list `years`.)

```
year = st.selectbox("Year:", years, index=years.index(2024))
```

* We want to select the region type (column `LocTypeName`)

We can follow the same process as for year above, but in column `LocTypeName` 
there are missing values which we want to exclude. So we have

```
locations = df.LocTypeName.dropna().unique().tolist()
```

We should remove location `World` from list as we have not taken over enough 
planets to generate top 5 yet. (and we won't be on Mars within 4 years, Elon)

```
locations.remove("World")
```

Finally selection box is created using

```
location = st.selectbox("Location Type:", locations)
```

* Now we want to filter and sort our data.  First, for clearer code,
define the criteria (for filtering) and the columns to be used in output.

```
criteria = f"LocTypeName=='{location}' and Time=={year}"
columns = ['Location', 'TPopulation1Jan']
```

Then apply filtering and sorting, creating a temporary data frame

```
df_tmp = (df
    .query(criteria)
    .sort_values("TPopulation1Jan", ascending=False)
    [columns]
)
```

We now have the data to display the 5, using 

```
st.dataframe(df_tmp.head(5))
```

Or we could pimp the output by renaming the columns

```
df_tmp.columns = ["Location", "Total Population (on Jan 1st)"]
```

and using `st.table` after setting the index to be `Location` 

```
st.table(df_tmp.set_index("Location").head(5))
```

Finally we should add table caption that reflects the data.
(This is left as a exercise.)""")

st.markdown(
"""## Result
""")

df.Time = df.Time.astype(int)
years = df.Time.unique().tolist()

year = st.selectbox("Year:", years, index=years.index(2024))

locations = df.LocTypeName.dropna().unique().tolist()
locations.remove("World")

location = st.selectbox("Location Type:", locations, index=locations.index('Country/Area'))


criteria = f"LocTypeName=='{location}' and Time=={year}"
columns = ['Location', 'TPopulation1Jan']

df_tmp = (df
    .query(criteria)
    .sort_values("TPopulation1Jan", ascending=False)
    [columns]
)
df_tmp.columns = ["Location", "Total Population (on Jan 1st)"]

label = location_label(location)
st.write(f"### Top five {label} in {year} (by population)")
st.table(df_tmp.set_index("Location").head(5))

