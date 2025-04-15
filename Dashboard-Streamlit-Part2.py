
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
from numerize.numerize import numerize
from PIL import Image

########################### Setting Up the Dashboard ################################################

#Configure the page
st.set_page_config(page_title = 'New York CitiBike Strategy Dashboard', layout='wide')

#Add a title
st.title("New York CitiBike Strategy Dashboard")

#Define a side bar/ dropdown menu in Streamlit
st.sidebar.title("Dashboard Sections")
page = st.sidebar.selectbox('Select a Section of the Analysis',
  ["Introduction",
   "Bike Usage and Weather",
   "Most Popular Stations",
   "Interactive Map with Aggregated Bike Trips",
   "Recommendations"])

########################## Import data ###########################################################################################

#The selected reduced columns dataset
df = pd.read_csv('rand_reduced_data_for_plot.csv', index_col = 0)

#The top 20 stations dataset
top_20 = pd.read_csv('top20.csv',index_col = 0)


####################################### DEFINE THE PAGES #####################################################################

### Introduction/Title Page ###

if page == "Introduction":
    
    #Add Markdown Text - explain the purpose of the dashboard
    st.markdown("This dashboard addresses the distribution challenges faced by New York CitiBike and identifies potential expansion opportunities.")
    st.markdown("Currently, CitiBike encounters issues like insufficient bikes at popular stations and stations overcrowded with docked bikes, complicating the process of returning hired bikes. Additionally, customers often complain about bike unavailability at certain locations. This analysis seeks to pinpoint the root causes of these distribution problems, improve bike availability, and reinforce CitiBike's role as a leader in eco-friendly transportation solutions in the city.")
    st.markdown("The dashboard is divided into the following four sections:")
    st.markdown("* Most Popular Stations")
    st.markdown("* Bike Usage and Weather")
    st.markdown("* Interactive Map with Aggregated Bike Trips")
    st.markdown("* Recommendations")
    st.markdown("The dropdown menu on the left, labeled 'Dashboard Sections', will navigate you to the different areas of the analysis that were investigated.")
    st.markdown("**Note:** The final steps of the analysis display a random sample comprising 8% of the dataset. This is done to facilitate easier data manipulation and accommodate resource limitations.")

    #Add an image    
    myImage = Image.open("NY_CitiBike.png") #Source: ny1.com
    st.image(myImage)

#Test the Output
#streamlit run Dashboard-Streamlit-Part2.py

########################################## THE CHARTS ##############################################################################################

##########################################
##########################################
### Bike Usage and Weather Page ###
##########################################

elif page == 'Bike Usage and Weather':

################################
#### Dual axis Line chart ####
################################

#Create a "fig" object for the make_subplots function
    fig_2 = make_subplots(specs = [[{"secondary_y": True}]]) #there will be a dual axis

#Assign go.Scatter(() to the “fig” object and apply settings customization **Colors**
    fig_2.add_trace(
        go.Scatter(x = df['date'], y = df['daily_bike_rides'], name = 'Daily bike rides', 
               marker={'color': df['daily_bike_rides'],'color': 'blue'}),
        secondary_y = False
    )

    fig_2.add_trace(
        go.Scatter(x=df['date'], y = df['avgTemp'],
                   name = 'Daily temperature', 
                   marker={'color': df['avgTemp'],
                           'color': 'red'}),
        secondary_y=True
    )

#Line chart updated [title, labels, wideness] **directly access and change the settings
    fig_2.update_layout(
        title = 'Daily bike rides and temperature in 2022',
        xaxis_title = '2022',
        width = 900, height = 600
    )
    st.plotly_chart(fig_2, use_container_width=True)

    #Add Markdown Text
    st.markdown("* There is a correlation between temperature changes and daily bike trip frequency.")
    st.markdown("* As temperature rises, bike usage increases, peaking between May and September.")
    st.markdown("* Conversely, during the colder months, usage decreases, with the lowest levels in January and February.")
    st.markdown("* This insight suggests that the shortage may primarily occur in the warmer months, roughly from May to October.")

########################################################################################################################################################################################################################################################################################################

##########################################
##########################################
### Most Popular Stations Page ###
##########################################

elif page == 'Most Popular Stations':

##############################
###### Seasons Filter ######
##############################
#Create a filter that sorts the resutls by the season variable

    #Create a sidebar to add widgets for user input.
    with st.sidebar:
        #Select multiple options from the unique values
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
default=df['season'].unique())  #more than one season can be selected simultaneously.
        
        #Add a link that filter to the dataframe based in the user selection, and store the resutls in "df1"
        df1 = df.query('season == @season_filter') #reference to the season_filter variable that stores the filtered selected seasons 

##############################
###### Total Rides Icon ######  
##############################

    #Define the total rides and store the number in the object total_rides.
    #Get the total number from daily_bike_rides column using count() after apply the float() to correctly display.
    total_rides = float(df1['daily_bike_rides'].count())

    #Store the results/ numbers using **st.metric()** to display
    st.metric(label = 'Total Bike Rides',
              value= numerize(total_rides)) #Show the number as a readable string

#This metrics icon shows the he total number of rides and is connected to the seasons filter.
#Show the metric with a label and a value.
#Displaying key performance indicators (KPIs) *** the number of bikes ***

########################################
### Data Manipulation for Bar Chart ####
########################################
    df1['value'] = 1 

    #Groupby **start_station_name** and count the number of entries in each group. **the count are the number of occurrences of each **start_station_name**
    df_group = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})

    #Aggregate the occurrences of the stations’ names to select the top 20 most visited stations 
    top20 = df_group.nlargest(20, 'value')

####################
#### Bar chart #####
####################
    #Assign go.Bar() to the “fig” object and apply settings customization
    fig = go.Figure(go.Bar(x = top_20['start_station_name'],
                           y = top_20['value'], 
                           marker={'color': top_20['value'],'colorscale': 'Blues'}))

##Bar chart updated [title, labels, wideness] **directly access and change the settings
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)

    #Display the plotly chart with Streamlit and save the file 
    st.plotly_chart(fig, use_container_width=True)

    #Add Markdown Text
    st.markdown("* The bar chart shows that certain start stations are more popular than others.")
    st.markdown("* The top four stations: Grove St Path, South Waterfront Walkway, Hoboken Terminal (River St & Hudson Pl) and Hoboken Terminal (Hudson St & Hudson Pl) —lead in popularity.")
    st.markdown("* Notably, the top stations have a markedly higher number of trips compared to others. The significant difference between the highest and lowest bars indicates a strong preference for these key stations.")
    st.markdown("* This suggests that bike unavailability is more likely at these locations due to insufficient supply at these stations.")
    st.markdown("* This observation can be cross-referenced with the interactive map accessible via the sidebar select box.")


########################################################################################################################################################################################################################################################################################################


###################################################
###################################################
### Interactive Map with Aggregated Bike Trips Page ###
###################################################

elif page == 'Interactive Map with Aggregated Bike Trips':

##############################
###### Create the Map ########
##############################

    st.write("Interactive Map Displaying Aggregated Bike Trips Across New York City")

    #Assign the file to the variable
    path_to_html = "NewYork_CitiBike_Trips_Aggregated.html.zip" 

    #Read the map/file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    #Add a header and render the map on the dashboard **Show in Webpage**
    st.header("Aggregated CitiBike Trips")
    st.components.v1.html(html_data,height=1000)

    #Add Markdown Text
    st.markdown("With the filter on the left side of the map, we can check if the most popular start stations are also among the top frequented trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("* Grove St Path, South Waterfront Walkway, and Hoboken Terminal (River St/Hudson Pl and Hudson St/Hudson Pl.")
    st.markdown("* With the aggregated bike trips filter enabled for Grove St Path, South Waterfront Walkway, and Hoboken Terminal (River St/Hudson Pl and Hudson St/Hudson Pl), the following observations can be made:")
    st.markdown("A. Trips from Grove St Path and Hoboken Terminal (Hudson St & Hudson Pl) are within New Jersey and don't include trips in New York City.")
    st.markdown("B. Most trips from South Waterfront Walkway (Sinatra Dr & 1 St) and Hoboken Terminal (River St & Hudson Pl) are also within New Jersey, with a few extending into New York City.")
    st.markdown("C. No trips start in New York, but many end there.")
    st.markdown("D. The most popular route, with 999K trips, is from Marshall St & 2 St to City Hall station (Washington St & 1 St). Other common routes, with over 990K trips, include Newport Pkwy to Washington St and Newport Path to Warren St, primarily along the waterfront.")


########################################################################################################################################################################################################################################################################################################

###################################################
###################################################
### Recommendations Page ###
###################################################

else:
    
    st.header("Conclusions and Recommendations")
    
    #Add an image     
    bikes = Image.open("CitiBike.jpg")  #source: nytimes.com
    st.image(bikes)

    #Add Markdown Text
    st.markdown("##### Our analysis suggests that New York CitiBikes should prioritize the following objectives to tackle challenges at specific stations and fulfill customer needs:")
    st.markdown("* Expanding and increasing the number of stations along the waterfronts of New Jersey and New York can help resolve the current bike distribution issues.")
    st.markdown("*  Specifically, it is strongly recommended to expand the stations at Marshall/City Hall, Newport Pkwy/Washington, and Newport Pkwy/Newport Path to Warren St, as these high-demand locations frequently face shortages at the start and challenges with bike returns at the end stations.")
    st.markdown("* Increase the number of stations in the Hoboken area, especially near the Hoboken train station and the Holland Tunnel on the New Jersey side. Additionally, add more stations on the New York side near City Hall, close to the Brooklyn Bridge.")
    st.markdown("*  Additional stations are also recommended along the New Jersey waterfront, from Liberty State Park to the Lincoln Tunnel.")
    st.markdown("* It's crucial to reallocate resources from less popular stations to areas with higher demand. During warmer months, ensure popular stations are fully stocked to meet increased demand, and consider reducing supply in colder months at less popular locations to minimize logistical costs.")
    st.markdown("* By focusing on these key New York CitiBike stations, we can alleviate distribution challenges, improve bike availability, and better meet customer needs and demands.")
    st.markdown("**Note:** The final steps of the analysis display a random sample comprising 8% of the dataset. This is done to facilitate easier data manipulation and accommodate resource limitations.")

##########################################
##########################################

#Test the Output
#streamlit run Dashboard-Streamlit-Part2.py
