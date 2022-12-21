import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
import plotly.graph_objects as go

def socioeconomicLayout(DataReader,inputDict):

    """
    This function return UI for socio-economic tab.

    """

    df_household,df_electricity_toilets,df_cooking_gas,df_banking,df_gini = DataReader.extractSocioEconomicData()

    all_states_metric_dropdown = dcc.Dropdown(options=[{'label': 'Homeless Households', 'value': 'homeless_household'},
                                                       {'label': 'Electricity and Sanitisation', 'value': 'electricity_toilets'},
                                                       {'label': 'Cooking Gas', 'value': 'cooking_gas'},
                                                       {'label': 'Bank Accounts', 'value': 'banking'},
                                                       {'label': 'Gini Coefficient', 'value': 'gini'}],
                                                       value=inputDict["value_all_states_metric_dropdown"],
                                                       id="socioeconomic-all_states-dropdown",
                                                       maxHeight=175)
    
    if inputDict["value_all_states_metric_dropdown"]=='homeless_household':
        
        df = df_household.sort_values("Houseless Households %",ascending=True)
        x = list(df["Houseless Households %"].values)
        y = list(df["State"].values)
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',text=list(df["Houseless Households %"].values),
                               textposition='inside',marker=dict(color=x,colorscale='turbo')))
        fig.update_layout(title={"text":"<b>Houseless Households : {} %</b>".format(np.round(np.mean(df["Houseless Households %"]),2))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df['Houseless Households %']), line_width=3, line_dash="dash", line_color="black")
    
    if inputDict["value_all_states_metric_dropdown"]=='electricity_toilets':

        df = df_electricity_toilets
        df = df[df["Residence_Type"]=="All"]
        df = df.sort_values("Electricity & Toilets %",ascending=True)
        df = df.reset_index().drop(columns="index")
        
        x1 = list(df["Electricity & Toilets %"].values)
        y1 = list(df["State"].values)

        x2 = list(df["Only Electricity %"].values)
        y2 = list(df["State"].values)

        x3 = list(df["Only Toilets %"].values)
        y3 = list(df["State"].values)

        x4 = list(df["None %"].values)
        y4 = list(df["State"].values)

        text1 = [str(np.round(i,1))+" %" for i in x1]
        text2 = [str(np.round(i,1))+" %" for i in x2]
        text3 = [str(np.round(i,1))+" %" for i in x3]
        text4 = [str(np.round(i,1))+" %" for i in x4]

        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name="Electricity & Toilets %",text=text1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name="Only Electricity %",text=text2,textposition='inside'))
        fig.add_trace(go.Bar(x=x3,y=y3,orientation='h',name="Only Toilets %",text=text3,textposition='inside'))
        fig.add_trace(go.Bar(x=x4,y=y4,orientation='h',name="None %",text=text4,textposition='inside'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    if inputDict["value_all_states_metric_dropdown"]=='cooking_gas':

        df = df_cooking_gas
        df = df[df["Residence_Type"]=="All"]
        df = df.sort_values('Gas Cylinder %',ascending=True)
        df = df.reset_index().drop(columns="index")
        
        x1 = list(df['Gas Cylinder %'].values)
        y1 = list(df["State"].values)

        x2 = list(df['Cowdung/Coal/Wood %'].values)
        y2 = list(df["State"].values)

        x3 = list(df['Kerosene %'].values)
        y3 = list(df["State"].values)

        x4 = list(df['Others %'].values)
        y4 = list(df["State"].values)

        text1 = [str(np.round(i,1))+" %" for i in x1]
        text2 = [str(np.round(i,1))+" %" for i in x2]
        text3 = [str(np.round(i,1))+" %" for i in x3]
        text4 = [str(np.round(i,1))+" %" for i in x4]

        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name='Gas Cylinder %',text=text1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='Cowdung/Coal/Wood %',text=text2,textposition='inside'))
        fig.add_trace(go.Bar(x=x3,y=y3,orientation='h',name='Kerosene %',text=text3,textposition='inside'))
        fig.add_trace(go.Bar(x=x4,y=y4,orientation='h',name='Others %',text=text4,textposition='inside'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    if inputDict["value_all_states_metric_dropdown"]=='banking':

        df = df_banking
        df = df[df["Residence_Type"]=="All"]
        df = df.sort_values('Bank Account %',ascending=True)
        df = df.reset_index().drop(columns="index")
        
        x1 = list(df['Bank Account %'].values)
        y1 = list(df["State"].values)

        x2 = list(df['Post Office Account %'].values)
        y2 = list(df["State"].values)

        x3 = list(df['No Deposit Account %'].values)
        y3 = list(df["State"].values)


        text1 = [str(np.round(i,1))+" %" for i in x1]
        text2 = [str(np.round(i,1))+" %" for i in x2]
        text3 = [str(np.round(i,1))+" %" for i in x3]

        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name='Bank Account %',text=text1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='Post Office Account %',text=text2,textposition='inside'))
        fig.add_trace(go.Bar(x=x3,y=y3,orientation='h',name='No Deposit Account %',text=text3,textposition='inside'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    if inputDict["value_all_states_metric_dropdown"]=='gini':
        
        df = df_gini[df_gini["Residence_Type"]=="All"]
        df = df.sort_values("Gini's coefficient",ascending=False)
        df = df.reset_index().drop(columns="index")

        x = list(df["Gini's coefficient"].values)
        y = list(df["State"].values)
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',text=x,
                               textposition='inside',marker=dict(color=x,colorscale='turbo')))
        fig.update_layout(title={"text":"<b>Gini Coefficient : {}</b>".format(np.round(np.mean(df["Gini's coefficient"]),2))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df["Gini's coefficient"]), line_width=3, line_dash="dash", line_color="black")


    graph_figure = dcc.Graph(figure=fig)  
    graph_div = html.Div([graph_figure],id="socioeconomic-all_states-graph_div")
    all_states = html.Div([all_states_metric_dropdown,graph_div],id="socioeconomic-all_states")

    # State Wise (Right Side Box)
    state_list = [{'label': i, 'value': i} for i in np.unique(df_household["State"].values)]
    
    state_wise_state_dropdown = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_socioeconomic_state_wise_state_dropdown"],
                                            id="socioeconomic_state_wise_state_dropdown",
                                            maxHeight=175)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{'label': 'Homeless Households', 'value': 'homeless_household'},
                                                       {'label': 'Electricity and Sanitisation', 'value': 'electricity_toilets'},
                                                       {'label': 'Cooking Gas', 'value': 'cooking_gas'},
                                                       {'label': 'Bank Accounts', 'value': 'bank_account'}],
                                                      value=inputDict["value_socioeconomic_state_wise_metric_dropdown"],
                                            id="socioeconomic_state_wise_metric_dropdown",
                                            maxHeight=175)

    state_wise_metrics = html.Div([state_wise_state_dropdown,state_wise_metric_dropdown],
                                   id="socioeconomic_state_wise_metrics")
    
    
    return html.Div([all_states, state_wise_metrics])