import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc, Input, Output
from masterlayout import masterLayout
from populationcensus import populationcensusLayout

def initialDisplay(value_selected_tab):

    """
    This function renders UI when new tab is selected
    
    """

    if value_selected_tab=="population_census":
        return populationcensusLayout()

    if value_selected_tab=="socio_economic_condition":
        return populationcensusLayout()

    if value_selected_tab=="education":
        return populationcensusLayout()

    if value_selected_tab=="health":
        return populationcensusLayout()
    
    if value_selected_tab=="employment":
        return populationcensusLayout()