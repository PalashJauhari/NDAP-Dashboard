import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
import plotly.graph_objects as go


def education_participation_layout(DataReader,inputDict):


    df_attendence_age,df_attendence_education_level,df_courses,df_enrollement_education_level,df_institute_type,df_course_level  = DataReader.extractEducationParticipationData()


    #metric_dropdown = dcc.Dropdown(options=[{"label":"Attendance As Per Age Groups","value":"attendence_age_group"},
    #                                        {"label":"Attendance As Per Education Level","value":"attendence_education_level"},
    #                                        {"label":"Enrollement As Per Education Level","value":"enrollement_education_level"},
    #                                        {"label":"Distribution As Per Education Level","value":"distribution_education_level"},
    #                                        {"label":"Distribution As Per Different Courses","value":"distribution_courses"}],
    #                                       
    #                                       value=inputDict["value_education_all_states_metric_dropdown"],
    #                                       id="education_all_states_metric_dropdown",
    #                                       maxHeight=175)
    
    
    
    metric_dropdown = dcc.Dropdown(options=[{"label":"Enrollement","value":"enrollement_education_level"},
                                            {"label":"Attendance","value":"attendence_age_group"},
                                            {"label":"Distribution As Per Education Level","value":"distribution_education_level"},
                                            {"label":"Distribution As Per Courses","value":"distribution_courses"}],
                                           value=inputDict["value_education_all_states_metric_dropdown"],
                                           id="education_all_states_metric_dropdown",
                                           maxHeight=175)

    residence_type_dropdown = dcc.Dropdown(options=[{"label":"Rural","value":"Rural"},
                                                    {"label":"Urban","value":"Urban"},
                                                    {"label":"Combined","value":"Total"}],
                                           value=inputDict["value_education_all_states_residence_type_dropdown"],
                                           id="education_all_states_residence_type_dropdown",
                                           maxHeight=175)
    
    gender_type_dropdown = dcc.Dropdown(options=[{"label":"Male","value":"Male"},
                                                 {"label":"Female","value":"Female"},
                                                 {"label":"Male & Female","value":"Person"}],
                                           value=inputDict["value_education_all_states_gender_dropdown"],
                                           id="education_all_states_gender_dropdown",
                                           maxHeight=175)
    
    if inputDict["value_education_all_states_metric_dropdown"]=='attendence_age_group':

        df = df_attendence_age.copy()
        df = df[df["Residence_Type"] == inputDict["value_education_all_states_residence_type_dropdown"]]
        df = df[df["Gender"] == inputDict["value_education_all_states_gender_dropdown"]]
        df = df.drop(columns=["Residence_Type","Gender","Age group"]).groupby("State").mean().reset_index()
        df["Attendance ratio"]=df["Attendance ratio"].apply(lambda x : int(x))
        df = df.sort_values("Attendance ratio",ascending=True)

        x = list(df["Attendance ratio"].values)
        y = list(df["State"].values)
        
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',text=list(df["Attendance ratio"].values),
                               textposition='inside',marker=dict(color=x,colorscale='turbo')))
        fig.update_layout(title={"text":"<b>Average Attendance Ratio : {} %</b>".format(int(np.mean(df["Attendance ratio"])))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df["Attendance ratio"]), line_width=3, line_dash="dash", line_color="black")
    
    if inputDict["value_education_all_states_metric_dropdown"]=='enrollement_education_level':

        df = df_enrollement_education_level.copy()
        df = df[df["Residence_Type"] == inputDict["value_education_all_states_residence_type_dropdown"]]
        df = df[df["Gender"] == inputDict["value_education_all_states_gender_dropdown"]]
        df = df.drop(columns=["Residence_Type","Gender","Level of current enrolment"]).groupby("State").mean().reset_index()
        df["Gross enrolment ratio ( ger )"]=df["Gross enrolment ratio ( ger )"].apply(lambda x : int(x))
        df = df.sort_values("Gross enrolment ratio ( ger )",ascending=True)

        x = list(df["Gross enrolment ratio ( ger )"].values)
        y = list(df["State"].values)
        
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',text=list(df["Gross enrolment ratio ( ger )"].values),
                               textposition='inside',marker=dict(color=x,colorscale='turbo')))
        fig.update_layout(title={"text":"<b>Average Gross Enrolment : {} %</b>".format(int(np.mean(df["Gross enrolment ratio ( ger )"])))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df["Gross enrolment ratio ( ger )"]), line_width=3, line_dash="dash", line_color="black")
    
    if inputDict["value_education_all_states_metric_dropdown"]=="distribution_courses":

        df = df_courses.copy()

        df = df[df["Residence_Type"] == inputDict["value_education_all_states_residence_type_dropdown"]]
        df = df[df["Gender"] == inputDict["value_education_all_states_gender_dropdown"]]

        all_values = ['Science','Engineering','Medical','IT','Law','Management','Humanities',
                      'Commerce','Medical','ITI','Upto X','Others']
        
        fig = go.Figure()
        for i in all_values:
            x = list(df[i].values)
            y = list(df["State"].values)
            text = [str(np.round(i,1))+" %" for i in x]
            fig.add_trace(go.Bar(x=x,y=y,orientation='h',name=i,text=text,textposition='inside'))
        
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    
    graph_figure = dcc.Graph(figure=fig)  
    graph_div = html.Div([graph_figure],id="education-all_states-graph_div")
    selection_div = html.Div([metric_dropdown,residence_type_dropdown ,gender_type_dropdown],id = "education_all_states_selection_div")
    all_states = html.Div([selection_div,graph_div],id="education-all_states")
    

    return html.Div([all_states])


def educationLayout(DataReader,inputDict):

    """
    This function return UI for education census tab.

    """
    
    selection_tabs = dcc.Dropdown(options=[
        
           {"label": html.Div(
                [
                    html.Img(src="assets/paticipation.png", height=30),
                    html.Div("Student Participation", style={"font-weight":"bold",'font-size': 16, 'padding-left': 10}),
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ), "value":'participation'},
          
           {"label": html.Div(
                [
                    html.Img(src="assets/infrastructure.jpg", height=30),
                    html.Div("Infrastructure", style={"font-weight":"bold",'font-size': 16, 'padding-left': 10}),
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ), "value":'infrastructure'},
           
           
           {"label": html.Div(
                [
                    html.Img(src="assets/faculty.png", height=30),
                    html.Div("Faculty", style={"font-weight":"bold",'font-size': 16, 'padding-left': 10}),
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ), "value" : 'faculty'}],
            
            value=inputDict["value_education_dropdown"],
            id="education_dropdown",
            maxHeight=175)

    all_states = education_participation_layout(DataReader,inputDict)


    state_wise_metrics = html.Div([],id="education_state_wise_metrics")

    return html.Div([selection_tabs,all_states,state_wise_metrics])
