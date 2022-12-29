import pandas as pd
import numpy as np
import json

import matplotlib.pyplot as plt
import seaborn as sns
from dash import Dash, html, dcc 
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


def education_participation_layout(DataReader,inputDict):


    df_attendence_age,df_attendence_education_level,df_courses,df_courses_1 ,df_enrollement_education_level,df_institute_type,df_course_level,df_institute_type_1,df_course_level_1  = DataReader.extractEducationParticipationData()

    metric_dropdown = dcc.Dropdown(options=[{"label":"Enrollement","value":"enrollement_education_level"},
                                            {"label":"Attendance","value":"attendence_age_group"},
                                            {"label":"Distribution As Per Education Level","value":"distribution_education_level"},
                                            {"label":"Distribution As Per Courses","value":"distribution_courses"},
                                            {"label":"Distribution As Per Institute Type","value":"distribution_institute"}],
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
        df["Gross enrolment ratio ( ger )"]=df["Gross enrolment ratio ( ger )"].apply(lambda x : int(np.min([x,100])))
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
    
    if inputDict["value_education_all_states_metric_dropdown"]=="distribution_education_level":

        df = df_course_level.copy()

        df = df[df["Residence_Type"] == inputDict["value_education_all_states_residence_type_dropdown"]]
        df = df[df["Gender"] == inputDict["value_education_all_states_gender_dropdown"]]
        df = df.sort_values('Primary',ascending=True)
        all_values = ['Primary','Secondary & Higher','Diploma','Graduate & Above']
                                 
        fig = go.Figure()
        for i in all_values:
            x = list(df[i].values)
            y = list(df["State"].values)
            text = [str(np.round(i,1))+" %" for i in x]
            fig.add_trace(go.Bar(x=x,y=y,orientation='h',name=i,text=text,textposition='inside'))
        
        fig.update_layout(barmode='relative',margin=dict(l=0, r=0, t=25, b=0),height=1000)
    
    if inputDict["value_education_all_states_metric_dropdown"]=="distribution_institute":

        df = df_institute_type.copy()

        df = df[df["Residence_Type"] == inputDict["value_education_all_states_residence_type_dropdown"]]
        df = df[df["Gender"] == inputDict["value_education_all_states_gender_dropdown"]]
        df = df.sort_values('Government',ascending=True)
        all_values = ['Government', 'Private Unaided', 'Private aided']
         
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

    # State Wise (Right Side Box)

    state_list = [{'label': i, 'value': i} for i in np.unique(df_attendence_age["State"].values)]
    state_wise_state_dropdown = dcc.Dropdown(options=state_list,
                                             value=inputDict["value_education_state_wise_state_dropdown"],
                                            id="education_state_wise_state_dropdown",
                                            maxHeight=175)
    
    state_list_1 = [{'label': i, 'value': i} for i in np.unique(df_attendence_age["State"].values)]
    state_list_1.append({'label': "India", 'value': "Total"})
    state_wise_state_dropdown_1 = dcc.Dropdown(options=state_list_1,
                                             value=inputDict["value_education_state_wise_state_dropdown_1"],
                                            id="education_state_wise_state_dropdown_1",
                                            maxHeight=175)

    state_wise_metric_dropdown = dcc.Dropdown(options=[{"label":"Enrolement As Per Education Level","value":"enrolement_education_level"},
                                            {"label":"Attendance As Per Age Groups","value":"attendence_age_group"},
                                            {"label":"Distribution As Per Education Level","value":"distribution_education_level"},
                                            {"label":"Distribution As Per Different Courses","value":"distribution_courses"},
                                            {"label":"Distribution As Per Institute Type","value":"distribution_institute"}],                                       
                                           value=inputDict["value_education_state_wise_metric_dropdown"],
                                           id="education_state_wise_metric_dropdown",
                                           maxHeight=175)

    residence_type_state_dropdown = dcc.Dropdown(options=[{"label":"Rural","value":"Rural"},
                                                    {"label":"Urban","value":"Urban"},
                                                    {"label":"Combined","value":"Total"}],
                                           value=inputDict["value_education_state_residence_type_dropdown"],
                                           id="education_state_residence_type_dropdown",
                                           maxHeight=175)
    
    gender_type_state_dropdown = dcc.Dropdown(options=[{"label":"Male","value":"Male"},
                                                 {"label":"Female","value":"Female"},
                                                 {"label":"Male & Female","value":"Person"}],
                                           value=inputDict["value_education_state_gender_dropdown"],
                                           id="education_state_gender_dropdown",
                                           maxHeight=175)
    

    state_dropdown_div = html.Div([state_wise_state_dropdown,html.Div(html.P("Vs"),id="education_vs"),
                                  state_wise_state_dropdown_1],
                                  id="state_dropdown_div")
    selection_div_down = html.Div([state_wise_metric_dropdown,residence_type_state_dropdown,
                                   gender_type_state_dropdown],id="state_selection_div_down")

    all_selection_div = html.Div([state_dropdown_div,selection_div_down],id="state_all_selection_div")
    

    if inputDict["value_education_state_wise_metric_dropdown"]=="enrolement_education_level":

        df = df_enrollement_education_level.copy()
        df = df[df["Level of current enrolment"].isin(["Primary","Secondary","Higher Secondary","Post Higher Secondary"])]
        df["Gross enrolment ratio ( ger )"]=df["Gross enrolment ratio ( ger )"].apply(lambda x : int(np.min([x,100])))
        var1 = "Level of current enrolment"
        var2 = "Gross enrolment ratio ( ger )"
        
        df1 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df1 = df1[df1["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df1 = df1[df1["State"]==inputDict["value_education_state_wise_state_dropdown"]]
        
        df2 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df2 = df2[df2["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df2 = df2[df2["State"]==inputDict["value_education_state_wise_state_dropdown_1"]]

        labels = list(np.unique(df1[var1]))

        y1, y2 = [],[]
        for i in labels:
            y1.append(df1[df1[var1]==i][var2].values[0])
            y2.append(df2[df2[var1]==i][var2].values[0])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=y1,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown"],textposition='inside'))
        fig.add_trace(go.Bar(x=y2,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown_1"],textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)

    if inputDict["value_education_state_wise_metric_dropdown"]=="attendence_age_group":

        df = df_attendence_age.copy()
        var1 = "Age group"
        var2 = "Attendance ratio"
        
        df1 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df1 = df1[df1["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df1 = df1[df1["State"]==inputDict["value_education_state_wise_state_dropdown"]]
        
        df2 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df2 = df2[df2["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df2 = df2[df2["State"]==inputDict["value_education_state_wise_state_dropdown_1"]]

        labels = list(np.unique(df1[var1]))

        y1, y2 = [],[]
        for i in labels:
            y1.append(df1[df1[var1]==i][var2].values[0])
            y2.append(df2[df2[var1]==i][var2].values[0])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=y1,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown"],textposition='inside'))
        fig.add_trace(go.Bar(x=y2,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown_1"],textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)
    
    if inputDict["value_education_state_wise_metric_dropdown"]=="distribution_education_level":

        df = df_course_level_1.copy()
        var1 = "Course type"
        var2 = "Enrolement"
        
        df1 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df1 = df1[df1["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df1 = df1[df1["State"]==inputDict["value_education_state_wise_state_dropdown"]]
        
        df2 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df2 = df2[df2["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df2 = df2[df2["State"]==inputDict["value_education_state_wise_state_dropdown_1"]]

        labels = list(np.unique(df1[var1]))

        y1, y2 = [],[]
        for i in labels:
            y1.append(df1[df1[var1]==i][var2].values[0])
            y2.append(df2[df2[var1]==i][var2].values[0])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=y1,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown"],textposition='inside'))
        fig.add_trace(go.Bar(x=y2,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown_1"],textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)
    
    if inputDict["value_education_state_wise_metric_dropdown"]=="distribution_courses":

        df = df_courses_1.copy()
        df=df[~df["Course type"].isin(["All"])]
        var1 = "Course type"
        var2 = "Distribution of students pursuing various courses (%)"
        
        df1 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df1 = df1[df1["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df1 = df1[df1["State"]==inputDict["value_education_state_wise_state_dropdown"]]
        
        df2 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df2 = df2[df2["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df2 = df2[df2["State"]==inputDict["value_education_state_wise_state_dropdown_1"]]

        labels = list(np.unique(df1[var1]))

        y1, y2 = [],[]
        for i in labels:
            y1.append(df1[df1[var1]==i][var2].values[0])
            y2.append(df2[df2[var1]==i][var2].values[0])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=y1,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown"],textposition='inside'))
        fig.add_trace(go.Bar(x=y2,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown_1"],textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)
    
    if inputDict["value_education_state_wise_metric_dropdown"]=="distribution_institute":

        df = df_institute_type_1.copy()
        var1 = "Institution type"
        var2 = "Enrolement"
        
        df1 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df1 = df1[df1["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df1 = df1[df1["State"]==inputDict["value_education_state_wise_state_dropdown"]]
        
        df2 = df[df["Residence_Type"]==inputDict["value_education_state_residence_type_dropdown"]]
        df2 = df2[df2["Gender"]==inputDict["value_education_state_gender_dropdown"]]
        df2 = df2[df2["State"]==inputDict["value_education_state_wise_state_dropdown_1"]]

        labels = list(np.unique(df1[var1]))

        y1, y2 = [],[]
        for i in labels:
            y1.append(df1[df1[var1]==i][var2].values[0])
            y2.append(df2[df2[var1]==i][var2].values[0])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=y1,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown"],textposition='inside'))
        fig.add_trace(go.Bar(x=y2,y=labels,orientation='h',name=inputDict["value_education_state_wise_state_dropdown_1"],textposition='inside'))
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),width=660,height=380)
    
    
    

    graph_figure_bottom = dcc.Graph(figure=fig)
    graph_div_bottom = html.Div([graph_figure_bottom],id="education_state_wise_metrics_graph_div_bottom")
    
    state_wise_metrics = html.Div([state_dropdown_div,selection_div_down,graph_div_bottom ],
                                 id="education_state_wise_metrics")

    return html.Div([all_states,state_wise_metrics])

def education_teachers_layout(DataReader,inputDict):
    
    df_teachers = DataReader.extractEducationFacultyData()
    
    metric_dropdown = dcc.Dropdown(options=[{"label":"Number of Teachers Per 1000 Population","value":"teachers_per_population"},
                                            {"label":"Male Teachers %","value":"male_teachers_pct"},
                                            {"label":"Female Teachers %","value":"female_teachers_pct"},
                                            {"label":"Permanent Teachers %","value":"permanent_pct"}],
                                           value=inputDict["value_education_teachers_all_states_metric_dropdown"],
                                           id="education_teachers_all_states_metric_dropdown",
                                           maxHeight=175)


    title_dict = {"teachers_per_population":"Number of Teacher/1000 Population","male_teachers_pct":"Male Teachers %",
                  "female_teachers_pct":"Female Teachers %","permanent_pct":"Permanent Teachers %"}                   
    
    if inputDict["value_education_teachers_all_states_metric_dropdown"] in ['teachers_per_population',
                                                                            "male_teachers_pct",
                                                                            "female_teachers_pct",
                                                                            "permanent_pct"]:
        
        var1 = inputDict["value_education_teachers_all_states_metric_dropdown"]
        df = df_teachers.copy()
        df = df.sort_values(var1,ascending=True)
        df = df.reset_index().drop(columns="index")
        
        x1 = list(np.abs(df[var1].values))
        y1 = list(df["State"].values)
        text1 = [str(np.round(i,1)) for i in x1]
        fig = go.Figure(go.Bar(x=x1,y=y1,orientation='h',name=var1,text=text1,textposition='inside',
                               marker=dict(color=x1,colorscale="turbo_r")))
        fig.update_layout(title={"text":"<b>{} : {}</b>".format(title_dict[var1],np.round(np.mean(df[var1]),1))},
                          margin=dict(l=0, r=0, t=25, b=0),height=1000)
        fig.add_vline(x=np.mean(df[var1]), line_width=3, line_dash="dash", line_color="black")
        fig.update_layout(margin=dict(l=0, r=0, t=25, b=0),height=1000)
        
        # create right side graph

        # gender based
        df_state = df[df["State"]==inputDict["value_education_teachers_all_states_graph_hover"]]
        labels_gender = ["Male","Female"]
        values_gender = [df_state["male_teachers_pct"].values[0],df_state["female_teachers_pct"].values[0]]

        fig_gender = go.Figure(data=[go.Pie(labels=labels_gender, values=values_gender)])
        fig_gender.update_layout(margin=dict(l=0, r=0, t=25, b=0), autosize=False,width=331,height=300)
        fig_gender.update_layout(title={"text":"<b>Gender Distribution</b>","x":0.5,"y":1.0},
                                 legend=dict(bgcolor='rgba(0, 0, 0, 0)', orientation='h',x=0.25,y=0))
        fig_state_gender = dcc.Graph(figure = fig_gender,id="education_teachers_states_gender_graph_hover")
        

        # job based
        df_state = df[df["State"]==inputDict["value_education_teachers_all_states_graph_hover"]]
        labels_job = ["Permanent","Contract"]
        values_job = [df_state["permanent_pct"].values[0],df_state["contract_pct"].values[0]]
        #,df_state["part_time_pct"].values[0]

        fig_job = go.Figure(data=[go.Pie(labels=labels_job, values=values_job)])
        fig_job.update_layout(margin=dict(l=0, r=0, t=25, b=0), autosize=False,width=331,height=300)
        fig_job.update_layout(title={"text":"<b>Job Type Distribution</b>","x":0.5,"y":1.0},
                             legend=dict(bgcolor='rgba(0, 0, 0, 0)', orientation='h',x=0.20,y=0))
        fig_state_job = dcc.Graph(figure = fig_job,id="education_teachers_states_job_graph_hover")

    graph_figure = dcc.Graph(figure=fig,id="education_teachers-all_states_graph_hover")  
    graph_div = html.Div([graph_figure],id="education_teachers-all_states-graph_div")
    all_states = html.Div([metric_dropdown,graph_div],id="education-all_states")

    selected_state_name = html.Div([inputDict["value_education_teachers_all_states_graph_hover"]],id="education_teachers_statename")
    graph_div_state = html.Div([fig_state_gender,fig_state_job ],id="education_teachers-states-graph_div")


    metric  = np.round(np.mean(df_teachers["teachers_per_population"]),1)
    card_avergae_teacher_per_population = dbc.Card(dbc.CardBody(
        [
            
            html.P("National Average Teachers/Population", className="card-title",id="card-title-et"),
            html.P(str(metric),className="card-text",id="card-text-et")
        ]),className="card_average")
    
    metric  = np.round(np.mean(df_teachers["male_teachers_pct"]),1)
    card_male_pct = dbc.Card(dbc.CardBody(
        [
            html.P("National Male %", className="card-subtitle",id="card-title-et"),
            html.P(str(metric),className="card-text")
        ]),className="card_gender")

    metric  = np.round(np.mean(df_teachers["female_teachers_pct"]),1)
    card_female_pct = dbc.Card(dbc.CardBody(
        [
            
            html.P("National Female %", className="card-subtitle",id="card-title-et"),
            html.P(str(metric),className="card-text")
        ]),className="card_gender")
    

    metric  = np.round(np.mean(df_teachers["permanent_pct"]),1)
    card_permanent_pct = dbc.Card(dbc.CardBody(
        [
            html.P("National Permanent %", className="card-subtitle",id="card-title-et"),
            html.P(str(metric),className="card-text")
        ]),className="card_job")
    
    metric  = np.round(np.mean(df_teachers["contract_pct"]),1)
    card_contract_pct = dbc.Card(dbc.CardBody(
        [
            
            html.P("National Contract %", className="card-subtitle",id="card-title-et"),
            html.P(str(metric),className="card-text")
        ]),className="card_job")
    
    metric  = np.round(np.mean(df_teachers["part_time_pct"]),1)
    card_parttime_pct = dbc.Card(dbc.CardBody(
        [
            html.P("National Part-Time %", className="card-subtitle",id="card-title-et"),
            html.P(str(metric),className="card-text")
        ]),className="card_job")

    gender_pct = html.Div([card_male_pct,card_female_pct ],id="education_teacher_gender_pct")
    jobtype_pct = html.Div([card_permanent_pct,card_contract_pct,card_parttime_pct],id="education_teacher_jobtype_pct")
    teacher_avg = html.Div([card_avergae_teacher_per_population],id="education_teacher_avg_pct")

    summary_card_header_1 = html.Div([gender_pct,jobtype_pct ],id="education_teacher_summary_card_header_1")
    summary_card_header_2 = html.Div([teacher_avg,summary_card_header_1 ],id="education_teacher_summary_card_header_2")
    
    state_wise_metrics = html.Div([summary_card_header_2,selected_state_name,graph_div_state],id="education_state_wise_metrics")

    return html.Div([all_states,state_wise_metrics])



#{"label": html.Div(
#                [
#                    html.Img(src="assets/infrastructure.jpg", height=30),
#                    html.Div("Infrastructure", style={"font-weight":"bold",'font-size': 16, 'padding-left': 10}),
#                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
#            ), "value":'infrastructure'},
def educationLayout(DataReader,inputDict):

    """
    This function return UI for education census tab.

    """
    
    selection_tabs = dcc.Dropdown(options=[
        
           {"label": html.Div(
                [
                    html.Img(src="assets/paticipation.png", height=30,width=30),
                    html.Div("Student Participation", style={"font-weight":"bold",'font-size': 16, 'padding-left': 10}),
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ), "value":'participation'},
          
           {"label": html.Div(
                [
                    html.Img(src="assets/faculty.png", height=30,width=30),
                    html.Div("Teaching Staff", style={"font-weight":"bold",'font-size': 16, 'padding-left': 10}),
                ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
            ), "value" : 'faculty'}],
            
            value=inputDict["value_education_dropdown"],
            id="education_dropdown",
            maxHeight=175)

    if inputDict["value_education_dropdown"]=="participation":
        all_states = education_participation_layout(DataReader,inputDict)
    elif inputDict["value_education_dropdown"]=="faculty":
        all_states = education_teachers_layout(DataReader,inputDict)
    else:
        all_states = education_participation_layout(DataReader,inputDict)

    return html.Div([selection_tabs,all_states])
