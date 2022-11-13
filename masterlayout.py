import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc

def masterlayout():

    """
    This function return master layout of dashboard.
    
    """

    # Read Style JSON
    f = open('styles.json')
    style_dict = json.load(f)
    style_dict = style_dict["masterlayout"]


    heading = html.Div([html.H4("Socio Economic Status of Indian States")],
                       style=style_dict["masterlayout-heading"],
                       id="masterlayout-heading")

    selection_tabs = html.Div(dcc.Tabs(id="masterlayout-selection-tabs-parent", value='population_census', 
                              children=[dcc.Tab(label='Populdation Census', value='population_census',className="masterlayout-selection-tabs-children"),
                                       dcc.Tab(label='Socio Economic Condition', value='socio_economic_condition',className="masterlayout-selection-tabs-children"),
                                       dcc.Tab(label='Education', value='education',className="masterlayout-selection-tabs-children"),
                                       dcc.Tab(label='Health', value='health',className="masterlayout-selection-tabs-children"),
                                       dcc.Tab(label='Employment', value='employment',className="masterlayout-selection-tabs-children")]),
                                       id="masterlayout-selection-tabs")

    dynamic_layout = html.Div([],id="masterlayout-dynamic-layout")
    layout = html.Div([heading,selection_tabs,dynamic_layout])


    return layout

