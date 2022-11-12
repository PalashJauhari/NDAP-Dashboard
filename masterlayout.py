import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc

def masterlayout():

    """
    This function return master layout of dashboard.
    
    """

    heading = html.Div([html.H3("Socio Economic Status of Indian States")],
                       id="masterlayout-heading")

    selection_tabs = html.Div(dcc.Tabs(id="masterlayout-selection-tabs", value='', 
                              children=[dcc.Tab(label='Populdation Census', value='population_census'),
                                       dcc.Tab(label='Socio Economic Condition', value='socio_economic_condition'),
                                       dcc.Tab(label='Education', value='education'),
                                       dcc.Tab(label='Health', value='health'),
                                       dcc.Tab(label='Employment', value='employment')]))

    dynamic_layout = html.Div([],id="masterlayout-dynamic-layout")
    layout = html.Div([heading,selection_tabs,dynamic_layout])


    return layout

