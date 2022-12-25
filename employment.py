import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
import plotly.graph_objects as go

def employmentLayout(DataReader,inputDict):

    df_employment_type,df_labourforce_participation_age,df_labourforce_participation_education,df_labourforce_earning = DataReader.extractEmploymentData()
    
    metric_dropdown = dcc.Dropdown(options=[{"label":"Households Paying Income Tax","value":"income_tax"},
                                            {"label":"Distribution of Job Sector","value":"job_sector"},
                                            {"label":"Distribution of Households Income","value":"distribution_household_income"},
                                            {"label":"Average Salary - Salaried Employee","value":"average_salary_salaried"},
                                            {"label":"Average Salary - Casual Labour","value":"average_salary_casual"},
                                            {"label":"Unemployment Rate","value":"unemployment_rate"}],
                                           value=inputDict["value_employment_all_states_metric_dropdown"],
                                           id="employment_all_states_metric_dropdown",
                                           maxHeight=175)
    
    all_states = html.Div([metric_dropdown],id="employment-all_states")


    

    state_list = [{'label': i, 'value': i} for i in list(np.unique(df_employment_type["State"]))]
    state_wise_state_dropdown = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_employment_state_wise_state_dropdown"],
                                            id="employment_state_wise_state_dropdown",
                                            maxHeight=175)
    
    state_wise_state_dropdown_1 = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_employment_state_wise_state_dropdown_1"],
                                            id="employment_state_wise_state_dropdown_1",
                                            maxHeight=175)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{"label":"Households Paying Income Tax","value":"income_tax"},
                                            {"label":"Distribution of Job Sector","value":"job_sector"},
                                            {"label":"Distribution of Households Income","value":"distribution_household_income"},
                                            {"label":"Average Salary - Salaried Employee","value":"average_salary_salaried"},
                                            {"label":"Average Salary - Casual Labour","value":"average_salary_casual"},
                                            {"label":"Unemployment Rate By Age","value":"unemployment_rate_age"},
                                            {"label":"Unemployment Rate By Education Level","value":"unemployment_rate_education"}],                                       
                                           value=inputDict["value_employment_state_wise_metric_dropdown"],
                                           id="employment_state_wise_metric_dropdown",
                                           maxHeight=175)

    residence_type_state_dropdown = dcc.Dropdown(options=[{"label":"Rural","value":"Rural"},
                                                    {"label":"Urban","value":"Urban"},
                                                    {"label":"Combined","value":"Total"}],
                                           value=inputDict["value_employment_state_residence_type_dropdown"],
                                           id="employment_state_residence_type_dropdown",
                                           maxHeight=175)
    
    gender_type_state_dropdown = dcc.Dropdown(options=[{"label":"Male","value":"Male"},
                                                 {"label":"Female","value":"Female"},
                                                 {"label":"Male & Female","value":"Person"}],
                                           value=inputDict["value_employment_state_gender_dropdown"],
                                           id="employment_state_gender_dropdown",
                                           maxHeight=175)
    

    state_dropdown_div = html.Div([state_wise_state_dropdown,html.Div(html.P("Vs"),id="employment_vs"),
                                  state_wise_state_dropdown_1],
                                  id="employment_state_dropdown_div")
    selection_div_down = html.Div([state_wise_metric_dropdown,residence_type_state_dropdown,
                                   gender_type_state_dropdown],id="employment_state_selection_div_down")

    #all_selection_div = html.Div([state_dropdown_div,selection_div_down],id="employment_state_all_selection_div")

    state_wise_metrics = html.Div([state_dropdown_div,selection_div_down,],
                                 id="employment_state_wise_metrics")
    
    return html.Div([all_states,state_wise_metrics])