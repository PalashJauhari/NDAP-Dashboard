import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc, Input, Output
from masterlayout import masterLayout
from populationcensus import populationcensusLayout
from callbacks import initialDisplay


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',"/assets/masterlayout.css"]
app = Dash(__name__,external_stylesheets=external_stylesheets)
app.layout = masterLayout()

@app.callback(Output(component_id='masterlayout-dynamic-layout', component_property='children'),
              Input(component_id='masterlayout-selection-tabs-parent', component_property='value'))

def renderFunction(value_selected_tab):
    return initialDisplay(value_selected_tab)

    


if __name__ == "__main__":
    app.run_server()