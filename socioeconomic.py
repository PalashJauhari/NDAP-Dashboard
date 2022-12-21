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
    
    all_states = html.Div([all_states_metric_dropdown],id="socioeconomic-all_states")
    # State Wise (Right Side Box)
    state_list = [{'label': i, 'value': i} for i in np.unique(df_household["State"].values)]
    
    state_wise_state_dropdown = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_populationcensus_state_wise_state_dropdown"],
                                            id="socioeconomic_state_wise_state_dropdown",
                                            maxHeight=125)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{'label': 'Homeless Households', 'value': 'homeless_household'},
                                                       {'label': 'Electricity and Sanitisation', 'value': 'electricity_toilets'},
                                                       {'label': 'Cooking Gas', 'value': 'cooking_gas'},
                                                       {'label': 'Bank Accounts', 'value': 'bank_account'}],
                                                      value=inputDict["value_populationcensus_state_wise_metric_dropdown"],
                                            id="socioeconomic_state_wise_metric_dropdown",
                                            maxHeight=125)

    state_wise_metrics = html.Div([state_wise_state_dropdown,state_wise_metric_dropdown],
                                   id="socioeconomic_state_wise_metrics")
    
    
    return html.Div([all_states, state_wise_metrics])