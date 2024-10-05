import streamlit as st
import pandas as pd
import glob

st.write("# World Population Tasks")

st.markdown("""This
is a collection of tasks requiring use of pandas (for data manipulation) 
and streamlit (for gui and visualisation). 

The data comes from [UN Dept of Economic and Social Affairs - Population division](https://population.un.org/wpp/Download/Standard/CSV/),
in particular the file [1950-2100, medium (GZ, 15.79 MB)](https://population.un.org/wpp/Download/Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz).          
""")

tasks = [
    st.Page("01-Top_5.py", title="Top 5 (by population)"),
    st.Page("02-Size_vs_Density.py", title="Population Size vs Density"),
    st.Page("03-Size_vs_Density_V2.py", title="Population Size vs Density (Fancy)"),
]
pg = st.navigation(tasks)
pg.run()
