import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
import plotly.graph_objects as go

def healthLayout(DataReader,inputDict):

    """
    This function return UI for health tab.

    """

    df_health_status,df_children_immunisation,df_health_infrastructure  = DataReader.extractHealthData()
    
    all_states_metric_dropdown = dcc.Dropdown(options=[{"label":"Children Wasted","value":"children_wasted"},
                                                       {'label': 'Infant Mortality Rate', 'value': 'imr'},
                                                       {'label': 'Fertility Rate', 'value': 'fertility_rate'},
                                                       {'label': 'Sex Ratio', 'value': 'sex_ratio'},
                                                       {"label":'Fully Immunised Children',"value":"fully_immunised"},
                                                       {"label":'Health Facilities / Population',"value":"health_facility"},
                                                       {'label': 'Women Overweight', 'value': 'women_overweight'},
                                                       {'label': 'Men Overweight', 'value': 'men_overweight'},
                                                       {'label': 'Women with High B.P', 'value': 'women_high_bp'},
                                                       {'label': 'Men with High B.P', 'value': 'men_high_bp'},
                                                       {'label': 'Women with High Sugar', 'value': 'women_high_sugar'},
                                                       {'label': 'Men with High Sugar', 'value': 'men_high_sugar'}],                                                      
                                                       value=inputDict["value_all_states_metric_dropdown"],
                                                       id="health-all_states-dropdown",
                                                       maxHeight=175)

    if inputDict["value_all_states_metric_dropdown"] in ['women_overweight',"women_high_bp", 'women_high_sugar',
                                                         'men_overweight','men_high_bp','men_high_sugar',"children_wasted",
                                                         "imr",'fertility_rate']:

        var1 = inputDict["value_all_states_metric_dropdown"] 
        df = df_health_status
        df = df[df["Residence_Type"]=="Total"]
        df = df.sort_values(var1,ascending=True)
        df = df.reset_index().drop(columns="index")
        
        x1 = list(np.abs(df[var1].values))
        y1 = list(df["State"].values)
        text1 = [str(np.round(i,1))+" %" for i in x1]
        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name=var1,text=text1,textposition='inside',
                               marker=dict(color=x1,colorscale='turbo')))
        fig.update_layout(title={"text":"<b>{} : {} %</b>".format(var1,np.round(np.mean(df[var1]),1))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df[var1]), line_width=3, line_dash="dash", line_color="black")
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),height=1000)
        
    if inputDict["value_all_states_metric_dropdown"] in ['sex_ratio']:

        var1 = inputDict["value_all_states_metric_dropdown"] 
        df = df_health_status
        df = df[df["Residence_Type"]=="Total"]
        df = df.sort_values(var1,ascending=True)
        df = df.reset_index().drop(columns="index")
        
        x1 = list(np.abs(df[var1].values))
        y1 = list(df["State"].values)
        text1 = [str(np.round(i,1)) for i in x1]
        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name=var1,text=text1,textposition='inside',
                               marker=dict(color=x1,colorscale='turbo_r')))
        fig.update_layout(title={"text":"<b>{} : {}</b>".format(var1,np.round(np.mean(df[var1]),1))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df[var1]), line_width=3, line_dash="dash", line_color="black")
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),height=1000)

    if inputDict["value_all_states_metric_dropdown"] in ["fully_immunised"]:

        var1 = inputDict["value_all_states_metric_dropdown"] 
        df = df_children_immunisation
        df = df[df["Residence_Type"]=="Total"]
        df = df.sort_values(var1,ascending=True)
        df = df.reset_index().drop(columns="index")
        
        x1 = list(np.abs(df[var1].values))
        y1 = list(df["State"].values)
        text1 = [str(np.round(i,1))+" %" for i in x1]
        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name=var1,text=text1,textposition='inside',
                               marker=dict(color=x1,colorscale='turbo_r')))
        fig.update_layout(title={"text":"<b>{} : {} %</b>".format(var1,np.round(np.mean(df[var1]),1))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df[var1]), line_width=3, line_dash="dash", line_color="black")
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    if inputDict["value_all_states_metric_dropdown"] in ["health_facility"]:

        var1 = inputDict["value_all_states_metric_dropdown"] 
        df = df_health_infrastructure.copy()
        df = df.sort_values(var1,ascending=True)
        df = df.reset_index().drop(columns="index")
        
        x1 = list(np.abs(df[var1].values))
        y1 = list(df["State"].values)
        text1 = [str(np.round(i*1e3,3)) for i in x1]
        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name=var1,text=text1,textposition='inside',
                               marker=dict(color=x1,colorscale='turbo_r')))
        fig.update_layout(title={"text":"<b>{} Per Thousand Population : {} </b>".format(var1,np.round(1e3*np.mean(x1),3))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df[var1]), line_width=3, line_dash="dash", line_color="black")
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    graph_figure = dcc.Graph(figure=fig)  
    graph_div = html.Div([graph_figure],id="health-all_states-graph_div")
    all_states = html.Div([all_states_metric_dropdown,graph_div ],id="health-all_states")

    # State Wise (Right Side Box)
    
    state_list = [{'label': i, 'value': i} for i in np.unique(df_health_status["State"].values)]
    state_wise_state_dropdown = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_health_state_wise_state_dropdown"],
                                            id="health_state_wise_state_dropdown",
                                            maxHeight=175)

    state_wise_state_dropdown_1 = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_health_state_wise_state_dropdown_1"],
                                            id="health_state_wise_state_dropdown_1",
                                            maxHeight=175)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{"label":"Children Wasted","value":"children_wasted"},
                                                       {'label': 'Infant Mortality Rate', 'value': 'imr'},
                                                       {'label': 'Fertility Rate', 'value': 'fertility_rate'},
                                                       {'label': 'Sex Ratio', 'value': 'sex_ratio'},
                                                       {"label":'Fully Immunised Children',"value":"fully_immunised"},
                                                       {'label': 'Women Overweight', 'value': 'women_overweight'},
                                                       {'label': 'Men Overweight', 'value': 'men_overweight'}],
                                                      value=inputDict["value_health_state_wise_metric_dropdown"],
                                            id="health_state_wise_metric_dropdown",
                                            maxHeight=175)


    state_dropdown_div = html.Div([state_wise_metric_dropdown],id="health_metric_dropdown_div")

    selection_div_down = html.Div([state_wise_state_dropdown,html.Div(html.P("Vs"),id="health_vs"),
                                   state_wise_state_dropdown_1],
                                   id="health_state_selection_div_down")

    all_selection_div = html.Div([state_dropdown_div,selection_div_down],id="health_state_all_selection_div")
    

    if inputDict["value_health_state_wise_metric_dropdown"] in ['women_overweight',"women_high_bp", 'women_high_sugar',
                                                                'men_overweight','men_high_bp','men_high_sugar',"children_wasted",
                                                                "imr",'fertility_rate','sex_ratio']:

        var1 = inputDict["value_health_state_wise_metric_dropdown"]
        state1 = inputDict["value_health_state_wise_state_dropdown"]
        state2 = inputDict["value_health_state_wise_state_dropdown_1"]
        
        df = df_health_status.copy()

        df1 = df[df["Residence_Type"]=="Rural"]
        df2 = df[df["Residence_Type"]=="Urban"]
        df3 = df[df["Residence_Type"]=="Total"]
        
        x1 = [df1[df1["State"]==inputDict["value_health_state_wise_state_dropdown"]][var1].values[0],
              df2[df2["State"]==inputDict["value_health_state_wise_state_dropdown"]][var1].values[0],
              df3[df3["State"]==inputDict["value_health_state_wise_state_dropdown"]][var1].values[0]]
        
        x2 = [df1[df1["State"]==inputDict["value_health_state_wise_state_dropdown_1"]][var1].values[0],
              df2[df2["State"]==inputDict["value_health_state_wise_state_dropdown_1"]][var1].values[0],
              df3[df3["State"]==inputDict["value_health_state_wise_state_dropdown_1"]][var1].values[0]]

        labels = ["Rural","Urban","Combined"]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=x1,y=labels,orientation='h',name=state1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=labels,orientation='h',name=state2,textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)
    
    if inputDict["value_health_state_wise_metric_dropdown"] in ["fully_immunised"]:

        var1 = inputDict["value_health_state_wise_metric_dropdown"]
        state1 = inputDict["value_health_state_wise_state_dropdown"]
        state2 = inputDict["value_health_state_wise_state_dropdown_1"]
        
        df = df_children_immunisation.copy()

        df1 = df[df["Residence_Type"]=="Rural"]
        df2 = df[df["Residence_Type"]=="Urban"]
        df3 = df[df["Residence_Type"]=="Total"]
        
        x1 = [df1[df1["State"]==inputDict["value_health_state_wise_state_dropdown"]][var1].values[0],
              df2[df2["State"]==inputDict["value_health_state_wise_state_dropdown"]][var1].values[0],
              df3[df3["State"]==inputDict["value_health_state_wise_state_dropdown"]][var1].values[0]]
        
        x2 = [df1[df1["State"]==inputDict["value_health_state_wise_state_dropdown_1"]][var1].values[0],
              df2[df2["State"]==inputDict["value_health_state_wise_state_dropdown_1"]][var1].values[0],
              df3[df3["State"]==inputDict["value_health_state_wise_state_dropdown_1"]][var1].values[0]]

        labels = ["Rural","Urban","Combined"]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=x1,y=labels,orientation='h',name=state1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=labels,orientation='h',name=state2,textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)
    
    
    graph_figure_bottom = dcc.Graph(figure=fig)
    graph_div_bottom = html.Div([graph_figure_bottom],id="health_state_wise_metrics_graph_div_bottom")
    
    state_wise_metrics = html.Div([all_selection_div,graph_div_bottom ],id="health_state_wise_metrics")
    
    return html.Div([all_states, state_wise_metrics])
