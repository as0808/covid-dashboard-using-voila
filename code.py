import pandas as pd
import numpy as np
import plotly.express as px
import folium

death_case=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
death_case

confirmed_case=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
confirmed_case

recovered_case=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
recovered_case

country_case=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv")
country_case

death_case.columns=map(str.lower,death_case.columns)
death_case=death_case.rename(columns={'province/state':'province','country/region':'country'})
death_case

confirmed_case.columns=map(str.lower,confirmed_case.columns)
confirmed_case=confirmed_case.rename(columns={'province/state':'province','country/region':'country'})
confirmed_case

recovered_case.columns=map(str.lower,recovered_case.columns)
recovered_case=recovered_case.rename(columns={'province/state':'province','country/region':'country'})
recovered_case

country_case.columns=map(str.lower,country_case.columns)
country_case=country_case.rename(columns={'province_state':'province','country_region':'country'})
countrt_case

sorted_country_case=country_case.sort_values('confirmed',ascending=False)
sorted_country_case

def highlight_col(x):
    r='background-color:purple'
    b='background-color:blue'
    y='background-color:green'
    temp_df=pd.DataFrame('',index=x.index,columns=x.columns)
    temp_df.iloc[:,4]=r
    temp_df.iloc[:,5]=b
    temp_df.iloc[:,6]=y
    return temp_df
sorted_country_case.style.apply(highlight_col,axis=None)

fig=px.scatter(sorted_country_case.head(10),x='country',y='confirmed',color='country',size='confirmed',hover_name='country',size_max=40)
fig.show()

confirmedcase=confirmed_case.loc[:,'country':]
confirmedcase=confirmedcase.dropna()
confirmedcase

deathcase=death_case.loc[:,'country':]
deathcase=deathcase.dropna()
deathcase

world_map=folium.Map(location=[11,0],tiles="cartodbpositron",zoom_start=2,max_zoom=6,min_zoom=2)

for i in range(len(confirmedcase)):
    folium.Circle(
    location=[confirmedcase.iloc[i]['lat'], confirmedcase.iloc[i]['long']],
    fill=True,
    radius=(int((np.log(confirmedcase.iloc[i,-1]+1.00001)))+0.2)*50000,
    fill_color='blue',
    color='red',
    tooltip="<div style='margin:0; background-color:black; color:white'>" +
        "<h4 style='text-align:center; font-weight:bold'>" + confirmedcase.iloc[i]['country'] + "</h4>" +
        "<hr style='margin:10px; color=white'>" +
        "<ul style='color:white; list-style-type:circle; align-item:left; padding-left:20px; padding-right:20px'>" +
        "<li> Confirmed:" + str(confirmedcase.iloc[i,-1])+ "</li>" +
        "<li> Deaths:" + str(deathcase.iloc[i,-1]) + "</li>" +
        "<li> Death Rate:" + str(np.round(deathcase.iloc[i,-1]/(confirmedcase.iloc[i,-1]+1.00001)*100,2)) + "</li>" +
        "</ul> </div>"
    ).add_to(world_map)
world_map

from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

import plotly.graph_objects as go

def plot_cases_for_country(country):
    labels=['confirmed','deaths']
    colors=['yellow','red']
    mode_size=[6,8]
    line_size=[4,10]
    
    df_list=[confirmedcase,deathcase]
    
    fig=go.Figure()
    
    for i, df in enumerate(df_list):
        if country=='World' or country=='world':
            x_data=np.array(list(df.iloc[:,5:].columns))
            y_data=np.sum(np.asarray(df.iloc[:,5:]), axis=0)
        else:
            x_data=np.array(list(df.iloc[:,5:].columns))
            y_data=np.sum(np.asarray(df[df['country']==country].iloc[:,5:]), axis=0)

        fig.add_trace(go.Scatter(x=x_data,y=y_data,mode='lines+markers',
                                 name=labels[i],
                                 line=dict(color=colors[i],width=line_size[i]),
                                 connectgaps=True,
                                 text="Total"+str(labels[i])+":"+str(y_data[-1])
                                ))

    fig.show()
interact(plot_cases_for_country,country='world');
