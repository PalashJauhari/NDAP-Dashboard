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
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',text=list(df["Population %"].values),
                               textposition='inside',marker=dict(color=x,colorscale='turbo')))
        fig.update_layout(title={"text":"<b>Total Population : {} M</b>".format(int(np.sum(df["Population"])/1e6))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df['Population']), line_width=3, line_dash="dash", line_color="black")

    if inputDict["value_all_states_metric_dropdown"]=='caste_distribution':

        df = df.sort_values("Population",ascending=True)
        x1 = list(df["Gen/OBCs & Others %"].values)
        y1 = list(df["State"].values)

        x2 = list(df['Scheduled caste population %'].values)
        y2 = list(df["State"].values)

        x3 = list(df['Scheduled tribe population %'].values)
        y3 = list(df["State"].values)

        text1 = [str(np.round(i,1))+" %" for i in list(df["Gen/OBCs & Others %"].values)]
        text2 = [str(np.round(i,1))+" %" for i in list(df['Scheduled caste population %'].values)]
        text3 = [str(np.round(i,1))+" %" for i in list(df['Scheduled tribe population %'].values)]

        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name="Gen/OBCs",text=text1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='SCs',text=text2,textposition='inside'))
        fig.add_trace(go.Bar(x=x3,y=y3,orientation='h',name='STs',text=text3,textposition='inside'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    if inputDict["value_all_states_metric_dropdown"]=='literacy':

        df = df.sort_values('Literate population %',ascending=True)
        x1 = list(df['Literate population %'].values)
        y1 = list(df["State"].values)

        x2 = list(df['Illiterate population %'].values)
        y2 = list(df["State"].values)

        text1 = [str(np.round(i,1))+" %" for i in list(df['Literate population %'].values)]
        text2 = [str(np.round(i,1))+" %" for i in list(df['Illiterate population %'].values)]
        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name="Literate",text=text1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='Illiterate',text=text2,textposition='inside'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)

    if inputDict["value_all_states_metric_dropdown"]=='employment':
        df = df.sort_values("Working population %",ascending=True)
        x1 = list(df["Working population %"].values)
        y1 = list(df["State"].values)

        x2 = list(df['Non Working population %'].values)
        y2 = list(df["State"].values)

        text1 = [str(np.round(i,1))+" %" for i in list(df['Working population %'].values)]
        text2 = [str(np.round(i,1))+" %" for i in list(df['Non Working population %'].values)]
        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name="Working",text=text1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='Non Working',text=text2,textposition='inside'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)

    graph_figure = dcc.Graph(figure=fig)  
    graph_div = html.Div([graph_figure],id="populationcensus-all_states-graph_div")
    all_states = html.Div([all_states_metric_dropdown,graph_div],id="populationcensus-all_states")
    
    # State Wise (Right Side Box)
    
    state_list = [{'label': i, 'value': i} for i in df["State"].values]
    
    state_wise_state_dropdown = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_populationcensus_state_wise_state_dropdown"],
                                            id="populationcensus_state_wise_state_dropdown",
                                            maxHeight=125)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{'label': 'Population', 'value': 'population'},
                                                       {'label': 'Caste Distribution', 'value': 'caste_distribution'},
                                                       {'label': 'Literacy', 'value': 'literacy'},
                                                       {'label': 'Working Population', 'value': 'employment'}],
                                                      value=inputDict["value_populationcensus_state_wise_metric_dropdown"],
                                            id="populationcensus_state_wise_metric_dropdown",
                                            maxHeight=125)


  
    if inputDict["value_populationcensus_state_wise_metric_dropdown"]=="population":

        df = df.sort_values("Population",ascending=True)
        df_state = df[df["State"]==inputDict["value_populationcensus_state_wise_state_dropdown"]]

        labels = ["Male","Female"]
        values = [df_state['Male population'].values[0],df_state['Female population'].values[0]]

        fig_top = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig_top.update_layout(margin=dict(l=5, r=0, t=25, b=0),width=660,height=225)

        fig_bottom = go.Figure(go.Bar(x=[labels[0]],y=[values[0]],orientation='v',text="Male",textposition='inside'))
        fig_bottom.add_trace(go.Bar(x=[labels[1]],y=[values[1]],orientation='v',text="Female",textposition='inside'))
        fig_bottom.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),width=660,height=225)
        fig_bottom.update_layout(showlegend=False)

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
        
        
        y_country_mean = [np.mean(df["Gen/OBCs & Others %"]),
                          np.mean(df['Scheduled caste population %']),
                          np.mean(df['Scheduled tribe population %'])]

        fig_bottom = go.Figure()
        fig_bottom.add_trace(go.Bar(x=x_caste,y=y_male,text="Male",textposition='inside'))
        fig_bottom.add_trace(go.Bar(x=x_caste,y=y_female,text="Female",textposition='inside'))
        fig_bottom.add_trace(go.Bar(x=x_caste,y=y_country_mean,text="Average",textposition='inside'))
        fig_bottom.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=225)
        fig_bottom.update_layout(showlegend=False)


    if inputDict["value_populationcensus_state_wise_metric_dropdown"]=='literacy':

        df = df.sort_values("Population",ascending=True)
        df_state = df[df["State"]==inputDict["value_populationcensus_state_wise_state_dropdown"]]

        labels = ["Literate","Illiterate"]
        values = [df_state['Literate population '].values[0],
                  df_state['Illiterate population'].values[0]]
        
        fig_top = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig_top.update_layout(margin=dict(l=5, r=0, t=25, b=0),width=660,height=225)

        x_literacy = ["Literate","Illiterate"]

        y_male = [df_state['Male literate population %'].values[0],
                  df_state['Male illiterate population %'].values[0]]

        y_female = [df_state['Female literate population %'].values[0],
                    df_state['Female illiterate population %'].values[0]]
        
        y_country_mean = [np.mean(df['Literate population %']),
                               np.mean(df['Illiterate population %'])]
        

        
        fig_bottom = go.Figure()
        fig_bottom.add_trace(go.Bar(x=x_literacy,y=y_male,text="Male",textposition='inside'))
        fig_bottom.add_trace(go.Bar(x=x_literacy,y=y_female,text="Female",textposition='inside'))
        fig_bottom.add_trace(go.Bar(x=x_literacy,y=y_country_mean,text="Average",textposition='inside'))
        fig_bottom.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=225)
        fig_bottom.update_layout(showlegend=False)

    if inputDict["value_populationcensus_state_wise_metric_dropdown"]=='employment':

        df = df.sort_values("Population",ascending=True)
        df_state = df[df["State"]==inputDict["value_populationcensus_state_wise_state_dropdown"]]

        labels = ["Working","Not Working"]
        values = [df_state['Working population'].values[0],
                  df_state['Non Working population'].values[0]]

        x_working = ["Working","Non Working"]

        y_male = [df_state['Male working population %'].values[0],
                  df_state['Male non working population %'].values[0]]

        y_female = [df_state['Female woking population %'].values[0],
                    df_state['Female non woking population %'].values[0]]
        
        y_country_mean = [np.mean(df['Working population %']),
                               np.mean(df['Non Working population %'])]
        
        fig_top = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig_top.update_layout(margin=dict(l=5, r=0, t=25, b=0),width=660,height=225)
        
        fig_bottom = go.Figure()
        fig_bottom.add_trace(go.Bar(x=x_working,y=y_male,text="Male",textposition='inside'))
        fig_bottom.add_trace(go.Bar(x=x_working,y=y_female,text="Female",textposition='inside'))
        fig_bottom.add_trace(go.Bar(x=x_working,y=y_country_mean,text="Average",textposition='inside'))
        fig_bottom.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=225)
        fig_bottom.update_layout(showlegend=False)
    

    graph_figure_top = dcc.Graph(figure=fig_top)
    graph_figure_bottom = dcc.Graph(figure=fig_bottom)
    graph_div_top = html.Div([graph_figure_top],id="populationcensus_state_wise_metrics_graph_div_top")
    graph_div_bottom = html.Div([graph_figure_bottom],id="populationcensus_state_wise_metrics_graph_div_bottom")

    state_wise_metrics = html.Div([state_wise_state_dropdown,state_wise_metric_dropdown ,
                                   graph_div_top,graph_div_bottom ],
                                   id="populationcensus_state_wise_metrics")
            


    return html.Div([all_states, state_wise_metrics])