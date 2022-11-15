import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
import plotly.graph_objects as go

def populationcensusLayout(DataReader,inputDict):

    """
    This function return UI for population census tab.
    """

    # All States (Left Side Box)

    df = DataReader.extractPopulationCensusData()

    all_states_metric_dropdown = dcc.Dropdown(options=[{'label': 'Population', 'value': 'population'},
                                                       {'label': 'Caste Distribution', 'value': 'caste_distribution'},
                                                       {'label': 'Literacy', 'value': 'literacy'},
                                                       {'label': 'Working Population', 'value': 'employment'}],
                                                       value=inputDict["value_all_states_metric_dropdown"],
                                                       id="populationcensus-all_states-dropdown",
                                                       maxHeight=125)
    
    if inputDict["value_all_states_metric_dropdown"]=='population':
        
        df = df.sort_values("Population",ascending=True)
        x = list(df["Population"].values)
        y = list(df["State"].values)
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',marker=dict(color=x,colorscale='turbo')))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),height=1000)

    if inputDict["value_all_states_metric_dropdown"]=='caste_distribution':

        df = df.sort_values("Population",ascending=True)
        x1 = list(df["Gen/OBCs & Others %"].values)
        y1 = list(df["State"].values)

        x2 = list(df['Scheduled caste population %'].values)
        y2 = list(df["State"].values)

        x3 = list(df['Scheduled tribe population %'].values)
        y3 = list(df["State"].values)

        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name="Gen/OBCs"))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='SCs'))
        fig.add_trace(go.Bar(x=x3,y=y3,orientation='h',name='STs'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    if inputDict["value_all_states_metric_dropdown"]=='literacy':

        df = df.sort_values('Literate population %',ascending=True)
        x1 = list(df['Literate population %'].values)
        y1 = list(df["State"].values)

        x2 = list(df['Illiterate population %'].values)
        y2 = list(df["State"].values)

        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name="Literate"))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='Illiterate'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)

    if inputDict["value_all_states_metric_dropdown"]=='employment':
        df = df.sort_values("Working population %",ascending=True)
        x1 = list(df["Working population %"].values)
        y1 = list(df["State"].values)

        x2 = list(df['Non Working population %'].values)
        y2 = list(df["State"].values)

        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name="Working"))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='Non-Working'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)

    graph_figure = dcc.Graph(figure=fig)  
    graph_div = html.Div([graph_figure],id="populationcensus-all_states-graph_div")
    all_states = html.Div([all_states_metric_dropdown,graph_div],id="populationcensus-all_states")
    
    # State Wise (Right Side Box)
    
    state_wise_state_dropdown = dcc.Dropdown(options=[{'label': 'Madhya Pradesh', 'value': 'Madhya Pradesh'},
                                                      {'label': 'Maharashtra', 'value': 'Maharashtra'}],
                                                      value='Maharashtra',
                                            id="populationcensus_state_wise_state_dropdown",
                                            maxHeight=125)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{'label': 'Population', 'value': 'population'},
                                                       {'label': 'Caste Distribution', 'value': 'caste_distribution'},
                                                       {'label': 'Literacy', 'value': 'literacy'},
                                                       {'label': 'Working Population', 'value': 'employment'}],
                                                      value='population',
                                            id="populationcensus_state_wise_metric_dropdown",
                                            maxHeight=125)


  
    if inputDict["value_populationcensus_state_wise_metric_dropdown"]=="population":

        df = df.sort_values("Population",ascending=True)
        df_state = df[df["State"]==inputDict["value_populationcensus_state_wise_state_dropdown"]]

        labels = ["Male","Female"]
        values = [df_state['Male population'].values[0],df_state['Female population'].values[0]]

        fig_top = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig_top.update_layout(margin=dict(l=5, r=0, t=25, b=0),width=660,height=225)

        fig_bottom = go.Figure(go.Bar(x=[labels[0]],y=[values[0]],orientation='v',name="Male"))
        fig_bottom.add_trace(go.Bar(x=[labels[1]],y=[values[1]],orientation='v',name='Female'))
        fig_bottom.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),width=660,height=225)

    if inputDict["value_populationcensus_state_wise_metric_dropdown"]=='caste_distribution':

        df = df.sort_values("Population",ascending=True)
        df_state = df[df["State"]==inputDict["value_populationcensus_state_wise_state_dropdown"]]

        labels = ["Gen/OBCs & Others","SCs","STs"]
        values = [df_state["Gen/OBCs & Others"].values[0],
                  df_state['Scheduled caste population'].values[0],
                  df_state['Scheduled tribe population'].values[0]]

        fig_top = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig_top.update_layout(margin=dict(l=5, r=0, t=25, b=0),width=660,height=225)

        
        x_caste = ["Gen/OBCs & Others","SCs","STs"]

        y_male = [df_state["Male Gen/OBCs & Others %"].values[0],
                  df_state['Male scheduled caste population %'].values[0],
                  df_state['Male scheduled tribe population %'].values[0]]
        y_female = [df_state["Female Gen/OBCs & Others %"].values[0],
                  df_state['Female scheduled caste population %'].values[0],
                  df_state['Female scheduled tribe population %'].values[0]]
        
        
        y_male_country_mean = [np.mean(df["Male Gen/OBCs & Others %"]),
                               np.mean(df['Male scheduled caste population %']),
                               np.mean(df['Male scheduled tribe population %'])]

        y_female_country_mean = [np.mean(df["Female Gen/OBCs & Others %"]),
                                 np.mean(df['Female scheduled caste population %']),
                                 np.mean(df['Female scheduled tribe population %'])]

        fig_bottom = go.Figure()
        fig_bottom.add_trace(go.Bar(x=x_caste,y=y_male,name='Male'))
        fig_bottom.add_trace(go.Bar(x=x_caste,y=y_male_country_mean,name='Mean Male'))
        fig_bottom.add_trace(go.Bar(x=x_caste,y=y_female,name='Female'))
        fig_bottom.add_trace(go.Bar(x=x_caste,y=y_female_country_mean,name='Mean Female'))
        fig_bottom.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=225)

    
    graph_figure_top = dcc.Graph(figure=fig_top)
    graph_figure_bottom = dcc.Graph(figure=fig_bottom)
    graph_div_top = html.Div([graph_figure_top],id="populationcensus_state_wise_metrics_graph_div_top")
    graph_div_bottom = html.Div([graph_figure_bottom],id="populationcensus_state_wise_metrics_graph_div_bottom")

    state_wise_metrics = html.Div([state_wise_state_dropdown,state_wise_metric_dropdown ,
                                   graph_div_top,graph_div_bottom ],
                                   id="populationcensus_state_wise_metrics")

    return html.Div([all_states, state_wise_metrics])