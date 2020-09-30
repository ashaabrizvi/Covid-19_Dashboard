# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:45:17 2020

@author: ASHAAB
"""
import streamlit as st
from streamlit_folium import folium_static
import json
import folium
import requests
import mimetypes
import http.client
import pandas as pd
from folium.plugins import HeatMap
from pandas.io.json import json_normalize
import plotly
import plotly.express as px

def main():
    
    st.markdown("<h1 style='text-align: center; color: #ff634d;'><strong><u>Covid 19 Dashboard</u></strong></h1>", unsafe_allow_html=True)
    st.sidebar.markdown("<h1 style='text-align: center; color: #aaccee;'><strong><u>Covid 19 Dashboard</u></strong></h1>", unsafe_allow_html=True)
    st.markdown("This Web App is a live Covid 19 Dashboard which access Data sourced from Johns Hopkins CSSE")
    
    
    conn = http.client.HTTPSConnection("api.covid19api.com")
    payload =''
    headers={}
    conn.request("GET","/summary",payload,headers)
    res = conn.getresponse()
    data=res.read().decode('UTF-8')
    covid = json.loads(data)
    
    
    df=pd.DataFrame(covid['Countries'])
    
    covid1=df.drop(columns=['CountryCode','Slug','Date','Premium'],axis=1)
    covid1.head()
    
    dfn=covid1.drop(['NewConfirmed','NewDeaths','NewRecovered'],axis=1)
    dfn = dfn.groupby('Country')['TotalConfirmed','TotalDeaths','TotalRecovered'].sum().sort_values(by='TotalConfirmed',ascending=False)
    dfn.style.background_gradient(cmap='Oranges')
    
    dfc = covid1.groupby('Country')['TotalConfirmed','TotalDeaths','TotalRecovered'].max().sort_values(by='TotalConfirmed',ascending=False).reset_index()
 
    m = folium.Map(tiles='Stamen Terrain',min_zoom=1.5)
    url='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    country_shapes = f'{url}/world-countries.json'
    folium.Choropleth(
    geo_data=country_shapes,
    min_zoom=2,
    name='Covid-19',
    data=covid1,
    columns=['Country','TotalConfirmed'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    nan_fill_color='black',
    legend_name='Total Confirmed Cases',
    ).add_to(m)
    
    m1 = folium.Map(tiles='Stamen Terrain',min_zoom=1.5)
    url='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    country_shapes = f'{url}/world-countries.json'
    folium.Choropleth(
    geo_data=country_shapes,
    min_zoom=2,
    name='Covid-19',
    data=covid1,
    columns=['Country','TotalRecovered'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    nan_fill_color='black',
    legend_name='Total Recovered Cases',
    ).add_to(m1)
    
    coordinates = pd.read_csv('https://raw.githubusercontent.com/VinitaSilaparasetty/covid-map/master/country-coordinates-world.csv')
    covid_final = pd.merge(covid1,coordinates,on='Country')
    
    dfn
    
    
    
    
    
    
    
           
    
    
    st.sidebar.subheader('Analysis through Map')
    
    select = st.sidebar.selectbox('Choose Map Type',['Confirmed Cases','Recovered Cases','Deaths'],key='1')
    
    
    if not st.sidebar.checkbox("Hide Map",True):
        
        if select == "Confirmed Cases": 
           folium_static(m)
           
           
           
        elif select == "Recovered Cases":
            
           folium_static(m1)
           
           
        else:
           m2 = folium.Map(tiles='StamenToner',min_zoom=1.5)
           deaths=covid_final['TotalDeaths'].astype(float)
           lat=covid_final['latitude'].astype(float)
           long=covid_final['longitude'].astype(float)
          
           m2.add_child(HeatMap(zip(lat,long,deaths),radius=0))
           folium_static(m2)
           
    st.sidebar.subheader('Analysis through Bar Chart')
    
    select = st.sidebar.selectbox('Choose Bar Chart',['Confirmed Cases','Recovered Cases','Deaths'],key='2')
    
           
           
    if not st.sidebar.checkbox("Hide Bar Chart",True):
        
        if select == "Confirmed Cases": 
           fig = px.bar(dfc.head(10), y='TotalConfirmed',x='Country',color='Country',height=400)
           fig.update_layout(title='Comparison of Total Confirmed Cases of 10 Most Affected Countries',xaxis_title='Country',yaxis_title='Total Confirmed Case',template="plotly_dark")
           st.plotly_chart(fig)
           
           
           
        elif select == "Recovered Cases":
            
           fig = px.bar(dfc.head(10), y='TotalRecovered',x='Country',color='Country',height=400)
           fig.update_layout(title='Comparison of Total Recovered of 10 Most Affected Countries',xaxis_title='Country',yaxis_title='Total Recovered',template="plotly_dark")
           st.plotly_chart(fig)
            
           
        else:
          fig = px.bar(dfc.head(10), y='TotalDeaths',x='Country',color='Country',height=400)
          fig.update_layout(title='Comparison of Total Deaths of 10 Most Affected Countries',xaxis_title='Country',yaxis_title='Total Deaths',template="plotly_dark")
          st.plotly_chart(fig)
          
          
    st.sidebar.subheader('Analysis through 3D Plot')
    
    if not st.sidebar.checkbox("Hide 3D plot",True):
        
        fig = px.scatter_3d(dfc.head(10), x='TotalConfirmed', y='TotalDeaths', z='TotalRecovered',
              color='Country')
        fig.update_layout(title='3D Plot of Total Cases, Total Deaths and Total Recovered of Top 20 Affected Countries')
        st.plotly_chart(fig)
          
                 
        

    
    
    
    
    
    if st.sidebar.checkbox("Show Raw Data",False):
        st.subheader("Covid 19 Data")
        st.write(covid1)

     
     
     
     
     
     
     
     
     
if __name__ == '__main__':
    main()
