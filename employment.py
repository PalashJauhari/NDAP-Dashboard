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
                                            {"label":"Distribution of Job Sector","value":"distribution_job_sector"},
                                            {"label":"Distribution of Households Income","value":"distribution_household_income"},
                                            {"label":"Average Monthly Salary - Salaried Employee","value":"average_salary_salaried"},
                                            {"label":"Average Daily Salary - Casual Labour","value":"average_salary_casual"},
                                            {"label":"Unemployment Rate","value":"unemployment_rate"}],
                                           value=inputDict["value_employment_all_states_metric_dropdown"],
                                           id="employment_all_states_metric_dropdown",
                                           maxHeight=175)
    
    if inputDict["value_employment_all_states_metric_dropdown"] in ["income_tax"]:

        var1 = 'Income Tax'
        df = df_employment_type.copy()
        df = df.sort_values(var1,ascending=True)
        x = list(np.round(df[var1].values,1))
        y = list(df["State"].values)
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',text=[str(int(i))+" %" for i in x],
                               textposition='inside',marker=dict(color=x,colorscale='turbo_r')))
        fig.update_layout(title={"text":"<b>{} : {} %</b>".format(var1,int(np.mean(df[var1])))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df[var1]), line_width=3, line_dash="dash", line_color="black")
    
    if inputDict["value_employment_all_states_metric_dropdown"] in ["unemployment_rate"]:

        var1 = 'Unemployment Rate %'
        df = df_labourforce_participation_age.copy()
        df = df.sort_values(var1,ascending=True)
        df = df[df["Residence_Type"]=="Total"]
        df = df[df["Age group"]=="all ages"]
        df = df[df["Gender"]=="Person"]

        x = list(np.round(df[var1].values,1))
        y = list(df["State"].values)
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',text=[str(int(i))+" %" for i in x],
                               textposition='inside',marker=dict(color=x,colorscale='turbo')))
        fig.update_layout(title={"text":"<b>{} : {} %</b>".format(var1,int(np.mean(df[var1])))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df[var1]), line_width=3, line_dash="dash", line_color="black")
    
    if inputDict["value_employment_all_states_metric_dropdown"] in ["average_salary_salaried","average_salary_casual"]:
        
        mapping_dict = {"average_salary_salaried":'Average Salaried Earnings',"average_salary_casual":'Average Casual Labour Earning'}
        var1 = mapping_dict[inputDict["value_employment_all_states_metric_dropdown"]]
        df = df_labourforce_earning.copy()
        df = df[df["Residence_Type"]=="Total"]
        df = df[df["Gender"]=="Person"]
        df = df.sort_values(var1,ascending=True)
        x = list(np.round(df[var1].values,1))
        y = list(df["State"].values)
        fig = go.Figure(go.Bar(x=x,y=y,orientation='h',text=["Rs."+str(int(i)) for i in x],
                               textposition='inside',marker=dict(color=x,colorscale='turbo_r')))
        fig.update_layout(title={"text":"<b> {} : Rs.{} </b>".format(var1,int(np.mean(df[var1])))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df[var1]), line_width=3, line_dash="dash", line_color="black")
    
    if inputDict["value_employment_all_states_metric_dropdown"] == "distribution_job_sector":

        df = df_employment_type.copy()
        
        df = df.sort_values( 'Government Job',ascending=True)
        x1 = list(df[ 'Government Job'].values)
        y1 = list(df["State"].values)

        x2 = list(df['Pubic Sector Job'].values)
        y2 = list(df["State"].values)

        x3 = list(df['Private Sector Job'].values)
        y3 = list(df["State"].values)

        x4 = list(df["Other Jobs"].values)
        y4 = list(df["State"].values)

        x5 = list(df["Casual Labour"].values)
        y5 = list(df["State"].values)

        text1 = [str(np.round(i,1))+" %" for i in x1]
        text2 = [str(np.round(i,1))+" %" for i in x2]
        text3 = [str(np.round(i,1))+" %" for i in x3]
        text4 = [str(np.round(i,1))+" %" for i in x4]
        text5 = [str(np.round(i,1))+" %" for i in x5]

        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name='Government Job',text=text1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='Pubic Sector Job',text=text2,textposition='inside'))
        fig.add_trace(go.Bar(x=x3,y=y3,orientation='h',name='Private Sector Job',text=text3,textposition='inside'))
        fig.add_trace(go.Bar(x=x5,y=y5,orientation='h',name="Casual Labour",text=text5,textposition='inside'))
        fig.add_trace(go.Bar(x=x4,y=y4,orientation='h',name="Other Jobs",text=text4,textposition='inside'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    if inputDict["value_employment_all_states_metric_dropdown"] == "distribution_household_income":

        df = df_employment_type.copy()
        
        df = df.sort_values( 'Househld Income < 5000',ascending=True)
        x1 = list(df[ 'Househld Income < 5000'].values)
        y1 = list(df["State"].values)

        x2 = list(df['Househld Income Between 5000 & 10000'].values)
        y2 = list(df["State"].values)

        x3 = list(df[ 'Househld Income > 10000'].values)
        y3 = list(df["State"].values)

        text1 = [str(np.round(i,1))+" %" for i in x1]
        text2 = [str(np.round(i,1))+" %" for i in x2]
        text3 = [str(np.round(i,1))+" %" for i in x3]

        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name='Income < 5k',text=text1,textposition='inside'))
        fig.add_trace(go.Bar(x=x2,y=y2,orientation='h',name='Income 5k-10k',text=text2,textposition='inside'))
        fig.add_trace(go.Bar(x=x3,y=y3,orientation='h',name= 'Income > 10k',text=text3,textposition='inside'))
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    graph_figure = dcc.Graph(figure=fig)  
    graph_div = html.Div([graph_figure],id="employment-all_states-graph_div")
    all_states = html.Div([metric_dropdown, graph_div ],id="employment-all_states")
    # statewise 
    state_list = [{'label': i, 'value': i} for i in list(np.unique(df_employment_type["State"]))]
    state_wise_state_dropdown = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_employment_state_wise_state_dropdown"],
                                            id="employment_state_wise_state_dropdown",
                                            maxHeight=175)
    
    state_wise_state_dropdown_1 = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_employment_state_wise_state_dropdown_1"],
                                            id="employment_state_wise_state_dropdown_1",
                                            maxHeight=175)

    state_wise_metric_dropdown = dcc.Dropdown(options=[
                                            {"label":"Average Monthly Salary","value":"average_salary"},
                                            {"label":"Unemployment Rate By Age","value":"unemployment_rate_age"},
                                            {"label":"Unemployment Rate By employment Level","value":"unemployment_rate_employment"}],                                       
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
    

    if inputDict["value_employment_state_wise_metric_dropdown"] in ["average_salary"]:
        
        df1 = df_labourforce_earning.drop(columns='Average Salaried Earnings')
        df1 = df1.rename(columns = {'Average Casual Labour Earning':"Salary"})
        df1["Employment_Type"] = "Casual Labour"
        df1["Salary"] = df1["Salary"].apply(lambda x : 26*x) # 26 is multiplied because for casula labour daily wages is given.
        
        df2 = df_labourforce_earning.drop(columns='Average Casual Labour Earning')
        df2 = df2.rename(columns = {'Average Salaried Earnings':"Salary"})
        df2["Employment_Type"] = "Salaried Employee"
        df = pd.concat([df1,df2],axis=0)

        var1 = "Employment_Type"
        var2 = "Salary"
        
        df1 = df[df["Residence_Type"]==inputDict["value_employment_state_residence_type_dropdown"]]
        df1 = df1[df1["Gender"]==inputDict["value_employment_state_gender_dropdown"]]
        df1 = df1[df1["State"]==inputDict["value_employment_state_wise_state_dropdown"]]
        
        df2 = df[df["Residence_Type"]==inputDict["value_employment_state_residence_type_dropdown"]]
        df2 = df2[df2["Gender"]==inputDict["value_employment_state_gender_dropdown"]]
        df2 = df2[df2["State"]==inputDict["value_employment_state_wise_state_dropdown_1"]]

        labels = list(np.unique(df1[var1]))

        y1, y2 = [],[]
        for i in labels:
            y1.append(df1[df1[var1]==i][var2].values[0])
            y2.append(df2[df2[var1]==i][var2].values[0])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=y1,y=labels,orientation='h',name=inputDict["value_employment_state_wise_state_dropdown"],textposition='inside'))
        fig.add_trace(go.Bar(x=y2,y=labels,orientation='h',name=inputDict["value_employment_state_wise_state_dropdown_1"],textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)
    
    if inputDict["value_employment_state_wise_metric_dropdown"] in ["unemployment_rate_age"]:
        
        
        df = df_labourforce_participation_age.copy()

        var1 = "Age group"
        var2 = 'Unemployment Rate %'
        
        df1 = df[df["Residence_Type"]==inputDict["value_employment_state_residence_type_dropdown"]]
        df1 = df1[df1["Gender"]==inputDict["value_employment_state_gender_dropdown"]]
        df1 = df1[df1["State"]==inputDict["value_employment_state_wise_state_dropdown"]]
        
        df2 = df[df["Residence_Type"]==inputDict["value_employment_state_residence_type_dropdown"]]
        df2 = df2[df2["Gender"]==inputDict["value_employment_state_gender_dropdown"]]
        df2 = df2[df2["State"]==inputDict["value_employment_state_wise_state_dropdown_1"]]

        labels = list(np.unique(df1[var1]))

        y1, y2 = [],[]
        for i in labels:
            y1.append(df1[df1[var1]==i][var2].values[0])
            y2.append(df2[df2[var1]==i][var2].values[0])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=y1,y=labels,orientation='h',name=inputDict["value_employment_state_wise_state_dropdown"],textposition='inside'))
        fig.add_trace(go.Bar(x=y2,y=labels,orientation='h',name=inputDict["value_employment_state_wise_state_dropdown_1"],textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)
    
    if inputDict["value_employment_state_wise_metric_dropdown"] in ["unemployment_rate_employment"]:
        
        
        df = df_labourforce_participation_education.copy()

        var1 = 'Education level'
        var2 = 'Unemployment Rate %'
        
        df1 = df[df["Residence_Type"]==inputDict["value_employment_state_residence_type_dropdown"]]
        df1 = df1[df1["Gender"]==inputDict["value_employment_state_gender_dropdown"]]
        df1 = df1[df1["State"]==inputDict["value_employment_state_wise_state_dropdown"]]
        
        df2 = df[df["Residence_Type"]==inputDict["value_employment_state_residence_type_dropdown"]]
        df2 = df2[df2["Gender"]==inputDict["value_employment_state_gender_dropdown"]]
        df2 = df2[df2["State"]==inputDict["value_employment_state_wise_state_dropdown_1"]]

        labels = list(np.unique(df1[var1]))

        y1, y2 = [],[]
        for i in labels:
            y1.append(df1[df1[var1]==i][var2].values[0])
            y2.append(df2[df2[var1]==i][var2].values[0])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=y1,y=labels,orientation='h',name=inputDict["value_employment_state_wise_state_dropdown"],textposition='inside'))
        fig.add_trace(go.Bar(x=y2,y=labels,orientation='h',name=inputDict["value_employment_state_wise_state_dropdown_1"],textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)

    graph_figure_bottom = dcc.Graph(figure=fig)
    graph_div_bottom = html.Div([graph_figure_bottom],id="employment_state_wise_metrics_graph_div_bottom")

    state_dropdown_div = html.Div([state_wise_state_dropdown,html.Div(html.P("Vs"),id="employment_vs"),
                                  state_wise_state_dropdown_1],
                                  id="employment_state_dropdown_div")
    selection_div_down = html.Div([state_wise_metric_dropdown,residence_type_state_dropdown,
                                   gender_type_state_dropdown],id="employment_state_selection_div_down")

    state_wise_metrics = html.Div([state_dropdown_div,selection_div_down,graph_div_bottom],
                                 id="employment_state_wise_metrics")
    
    return html.Div([all_states,state_wise_metrics])
