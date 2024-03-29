import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
from masterlayout import masterLayout
from populationcensus import populationcensusLayout
from socioeconomic import socioeconomicLayout
from education import educationLayout
from health import healthLayout
from employment import employmentLayout

def UIDisplay(DataReader,inputDict):

    """
    This function renders UI when new tab is selected
    
    """

    value_selected_tab = inputDict["value_selected_tab"]

    if value_selected_tab=="population_census":
        return populationcensusLayout(DataReader,inputDict["population_census"])

    if value_selected_tab=="socio_economic_condition":
        return socioeconomicLayout(DataReader,inputDict["socio_economic_condition"])

    if value_selected_tab=="education":
        return educationLayout(DataReader,inputDict["education"])

    if value_selected_tab=="health":
        return healthLayout(DataReader,inputDict["health"])
    
    if value_selected_tab=="employment":
        return employmentLayout(DataReader,inputDict["employment"])