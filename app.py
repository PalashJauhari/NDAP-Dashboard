import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc
from masterlayout import masterlayout


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,external_stylesheets=external_stylesheets)
app.layout = masterlayout()


if __name__ == "__main__":
    app.run()