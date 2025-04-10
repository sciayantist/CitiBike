
################################################ New York CitiBike BIKES DASHABOARD ################################################

# 01. Import Libraries

import pandas as pd 
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

########################### Setting Up the Dashboard ################################################

#Configure the page
st.set_page_config(page_title = 'New York CitiBike Strategy Dashboard', layout='wide')

#Add a title
st.title("New York CitiBike Strategy Dashboard")

#Add Markdown Text - explain the purpose of the dashboard
st.markdown("This dashboard addresses the distribution challenges faced by New York CitiBike and identifies potential expansion opportunities.")
st.markdown("Currently, CitiBike encounters issues like insufficient bikes at popular stations and stations overcrowded with docked bikes, complicating the process of returning hired bikes. Additionally, customers often complain about bike unavailability at certain locations. This analysis seeks to pinpoint the root causes of these distribution problems, improve bike availability, and reinforce CitiBike's role as a leader in eco-friendly transportation solutions in the city.")

#Test the Output
#streamlit run Dashboard-Streamlit-Part1.py

########################## Import data ###########################################################################################

#The selected /reduced columns dataset
df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)

#The top 20 stations dataset
top_20 = pd.read_csv('top20.csv',index_col = 0)

########################################## DEFINE THE CHARTS #####################################################################

##########################################
#### Bar chart ####
##########################################

#Assign go.Bar() to the “fig” object and apply settings customization
fig = go.Figure(go.Bar(x = top_20['start_station_name'], y = top_20['value'], marker={'color': top_20['value'],'colorscale': 'Blues'}))
##Bar chart updated [title, labels, wideness] **directly access and change the settings
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
#Display the plotly chart with Streamlit and save the file 
st.plotly_chart(fig, use_container_width=True)


##########################################
#### Line chart ####
##########################################

#Create a "fig" object for the make_subplots function
fig_2 = make_subplots(specs = [[{"secondary_y": True}]]) #there will be a dual axis

#Assign go.Scatter(() to the “fig” object and apply settings customization **Colors**
fig_2.add_trace(
    go.Scatter(x = df['date'], y = df['daily_bike_rides'], name = 'Daily bike rides', 
               marker={'color': df['daily_bike_rides'],'color': 'blue'}),
    secondary_y = False)

fig_2.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily temperature', 
               marker={'color': df['avgTemp'],'color': 'red'}),
    secondary_y=True)

#Line chart updated [title, labels, wideness] **directly access and change the settings
fig_2.update_layout(
    title = 'Daily bike rides and temperature in 2022 - New York CitiBike',
    xaxis_title = '2022',
    width = 900, height = 600
)
st.plotly_chart(fig_2, use_container_width=True)


##########################################
#### Add the map ####
##########################################

#Assign the file to the variable
path_to_html = "NewYorkCitiBikeTripsAggregated.html" 

#Read the map/file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

#Add a header and render the map on the dashboard **Show in Webpage**
st.header("Aggregated CitiBike Trips in New York")
st.components.v1.html(html_data,height=1000)

##########################################
##########################################