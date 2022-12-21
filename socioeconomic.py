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

    df_household,df_electricity_toilets,df_cooking_gas,df_banking,df_ginni = DataReader.extractSocioEconomicData()

    all_states_metric_dropdown = dcc.Dropdown(options=[{'label': 'Homeless Households', 'value': 'homeless_household'},
                                                       {'label': 'Electricity and Sanitisation', 'value': 'electricity_toilets'},
                                                       {'label': 'Cooking Gas', 'value': 'cooking_gas'},
                                                       {'label': 'Bank Accounts', 'value': 'bank_account'}],
                                                       value=inputDict["value_all_states_metric_dropdown"],
                                                       id="socioeconomic-all_states-dropdown",
                                                       maxHeight=125)
    
    if inputDict["value_all_states_metric_dropdown"]=='homeless_household':
        
        df = df_household.sort_values("Houseless Households %",ascending=True)
        x = list(df["Houseless Households %"].values)
        y = list(df["State"].values)
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',text=list(df["Houseless Households %"].values),
                               textposition='inside',marker=dict(color=x,colorscale='turbo')))
        fig.update_layout(title={"text":"<b>Houseless Households : {} %</b>".format(int(np.sum(df["Houseless Households %"])))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df['Houseless Households %']), line_width=3, line_dash="dash", line_color="black")
    



    graph_figure = dcc.Graph(figure=fig)  
    graph_div = html.Div([graph_figure],id="socioeconomic-all_states-graph_div")
    all_states = html.Div([all_states_metric_dropdown,graph_div],id="socioeconomic-all_states")

    # State Wise (Right Side Box)
    state_list = [{'label': i, 'value': i} for i in np.unique(df_household["State"].values)]
    
    state_wise_state_dropdown = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_socioeconomic_state_wise_state_dropdown"],
                                            id="socioeconomic_state_wise_state_dropdown",
                                            maxHeight=125)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{'label': 'Homeless Households', 'value': 'homeless_household'},
                                                       {'label': 'Electricity and Sanitisation', 'value': 'electricity_toilets'},
                                                       {'label': 'Cooking Gas', 'value': 'cooking_gas'},
                                                       {'label': 'Bank Accounts', 'value': 'bank_account'}],
                                                      value=inputDict["value_socioeconomic_state_wise_metric_dropdown"],
                                            id="socioeconomic_state_wise_metric_dropdown",
                                            maxHeight=125)

    state_wise_metrics = html.Div([state_wise_state_dropdown,state_wise_metric_dropdown],
                                   id="socioeconomic_state_wise_metrics")
    
    
    return html.Div([all_states, state_wise_metrics])