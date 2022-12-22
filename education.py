import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
import plotly.graph_objects as go


def education_participation_layout(inputDict):


    metric_dropdown = dcc.Dropdown(options=[{"label":"Rural","value":"rual"},
                                                    {"label":"Urban","value":"urban"},
                                                    {"label":"Combined","value":"combined"}],
                                           value=inputDict["value_education_all_states_metric_dropdown"],
                                           id="education_all_states_metric_dropdown",
                                           maxHeight=175)

    residence_type_dropdown = dcc.Dropdown(options=[{"label":"Rural","value":"rual"},
                                                    {"label":"Urban","value":"urban"},
                                                    {"label":"Combined","value":"combined"}],
                                           value=inputDict["value_education_all_states_residence_type_dropdown"],
                                           id="education_all_states_residence_type_dropdown",
                                           maxHeight=175)
    
    gender_type_dropdown = dcc.Dropdown(options=[{"label":"Male","value":"male"},
                                                 {"label":"Female","value":"female"},
                                                 {"label":"Male & Female","value":"both"}],
                                           value=inputDict["value_education_all_states_gender_dropdown"],
                                           id="education_all_states_gender_dropdown",
                                           maxHeight=175)
    
    
    selection_div = html.Div([metric_dropdown,residence_type_dropdown ,gender_type_dropdown],id = "education_all_states_selection_div")
    all_states = html.Div([selection_div],id="education-all_states")
    
    
    return html.Div([all_states])


def educationLayout(DataReader,inputDict):

    """
    This function return UI for education census tab.

    """
    
    selection_tabs = dcc.Dropdown(options=[
        
           {"label": html.Div(
                [
                    html.Img(src="assets/paticipation.png", height=30),
                    html.Div("Participation", style={'font-size': 15, 'padding-left': 10}),
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ), "value":'participation'},
          
           {"label": html.Div(
                [
                    html.Img(src="assets/infrastructure.jpg", height=30),
                    html.Div("Infrastructure", style={'font-size': 15, 'padding-left': 10}),
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ), "value":'infrastructure'},
           
           
           {"label": html.Div(
                [
                    html.Img(src="assets/faculty.png", height=30),
                    html.Div("Faculty", style={'font-size': 15, 'padding-left': 10}),
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ), "value" : 'faculty'}],
            
            value=inputDict["value_education_dropdown"],
            id="education-all_states-dropdown",
            maxHeight=175)

    all_states = education_participation_layout(inputDict)


    state_wise_metrics = html.Div([],id="education_state_wise_metrics")

    return html.Div([selection_tabs,all_states,state_wise_metrics])
