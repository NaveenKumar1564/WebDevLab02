# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

st.info("Data Loading Logic:" \
"So first the data file are tried to open with try and except block to handle File Not found error " \
"Then the panda library is used to read the csv file using its .read_csv methodn and json.load() is used to load the data from json file.")

try:
    StudyHourData =  pd.read_csv(r'/workspaces/WebDevLab02/WebDevLab02/Lab02/data.csv')
except FileNotFoundError:
    print("File not found:/")
except Exception as err:
    print(f"Did not handle: {err} error.")

try:
    json_fn = r'/workspaces/WebDevLab02/WebDevLab02/Lab02/data.json'
    infile = open(json_fn)
    json_data = json.load(infile)
    infile.close()
except FileNotFoundError:
    print("File not found:/")
except Exception as err:
    print(f"Did not handle: {err} error.")


# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

st.divider()

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Static Line Chart for Average Study Hours Per Day")

StudyHourAverage = StudyHourData.mean() 
st.line_chart(StudyHourAverage) # NEW 
st.caption("This is static line chart that shows avergae study hours per day of all user that filled the survey.") #NEW
st.divider()


# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Dynamic Bar Chart for World Population") 

countries = [] 

for val in json_data: 
    country_name = val["country"]  
    countries.append(country_name)  

selected = st.multiselect( 
    "Select countries to display",
    options=countries,
    default=countries,
    key='selected_countries'
)

filtered_data = []

for val in json_data:
    if val["country"] in st.session_state.selected_countries:
        filtered_data.append(val)


filtered_df = pd.DataFrame(filtered_data)
filtered_df = filtered_df.set_index('country')

st.bar_chart(data=filtered_df)

st.caption("This is a dynamic bar chart that shows population of a few countries. User can interact" \
"with the graph using the multi select option. They can chose the countries of which they want to see population of" 
"by using the multi-select dropdown.")


# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Dynamic Scatter Chart for Average Study Hours Per Day") 


average = StudyHourData.mean()
chart_data = pd.DataFrame(average)

if "min_hours" not in st.session_state:
    st.session_state.min_hours = 3  

min_hours = st.slider(
    "Select minimum study hours to display: ",
    min_value=1,
    max_value=12,
    value=st.session_state.min_hours,
    key = "Hour_slider"
)

st.session_state.min_hours = min_hours
filtered_df = chart_data[chart_data >= min_hours]
st.scatter_chart(filtered_df)

st.caption("This is dynamic scatter chart that shows avergae study hours per day of all user that filled the survey." \
"The user can interact with this graph by using the slider feature. They can chose the minimum number of hours using the slider" \
"which would then display on the days on which students average study hour is greater than the min value.")
