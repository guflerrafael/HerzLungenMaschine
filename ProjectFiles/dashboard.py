from cmath import nan
from tempfile import SpooledTemporaryFile
import dash
from dash import Dash, html, dcc, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import utilities as ut
import numpy as np
import os
import re
import matplotlib.pyplot as plt

app = Dash(__name__)


list_of_subjects = []
subj_numbers = []
number_of_subjects = 0

folder_current = os.path.dirname(__file__) 
print(folder_current)
folder_input_data = os.path.join(folder_current, "input_data")
for file in os.listdir(folder_input_data):
    
    if file.endswith(".csv"):
        number_of_subjects += 1
        file_name = os.path.join(folder_input_data, file)
        print(file_name)
        list_of_subjects.append(ut.Subject(file_name))


df = list_of_subjects[0].subject_data


for i in range(number_of_subjects):
    subj_numbers.append(list_of_subjects[i].subject_id)

data_names = ["SpO2 (%)", "Blood Flow (ml/s)","Temp (C)"]
algorithm_names = ['min','max']
blood_flow_functions = ['CMA','SMA','Show Limits']


fig0= go.Figure()
fig1= go.Figure()
fig2= go.Figure()
fig3= go.Figure()

fig0 = px.line(df, x="Time (s)", y = "SpO2 (%)")
fig1 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")
fig2 = px.line(df, x="Time (s)", y = "Temp (C)")
fig3 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")

app.layout = html.Div(children=[
    html.H1(children='Cardiopulmonary Bypass Dashboard'),

    html.Div(children='''
        Hier könnten Informationen zum Patienten stehen....
    '''),

    dcc.Checklist(
    id= 'checklist-algo',
    options=algorithm_names,
    inline=False
    ),

    html.Div([
        dcc.Dropdown(options = subj_numbers, placeholder='Select a subject', value='1', id='subject-dropdown'),
    html.Div(id='dd-output-container')
    ],
        style={"width": "15%"}
    ),

    dcc.Graph(
        id='dash-graph0',
        figure=fig0
    ),

    dcc.Graph(
        id='dash-graph1',
        figure=fig1
    ),
    dcc.Graph(
        id='dash-graph2',
        figure=fig2
    ),

    dcc.Checklist(
        id= 'checklist-bloodflow',
        options=blood_flow_functions,
        inline=False
    ),
    dcc.Graph(
        id='dash-graph3',
        figure=fig3
    )
])

#----Funktion um Linien zu plotten
def plotLine(figure, x, y, color, name):
    figure.add_trace(
        go.Scatter(
            mode="lines",
            x=x,
            y=y,
            line=go.scatter.Line(color=color),
            name=name
        )
    )

#------

### Callback Functions ###
## Graph Update Callback
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph0', 'figure'),
    Output('dash-graph1', 'figure'),
    Output('dash-graph2', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-algo','value')
)

def update_figure(value, algorithm_checkmarks):
    print("Current Subject: ",value)
    print("current checked checkmarks are: ", algorithm_checkmarks)
    ts = list_of_subjects[int(value)-1].subject_data
    #SpO2
    fig0 = px.line(ts, x="Time (s)", y = data_names[0])
    # Blood Flow
    fig1 = px.line(ts, x="Time (s)", y = data_names[1])
    # Blood Temperature
    fig2 = px.line(ts, x="Time (s)", y = data_names[2])
    
    ### Aufgabe 2: Min / Max ###
    # Link zu dieser Aufgabe: https://plotly.com/python/creating-and-updating-figures/

    # Ermitteln der Extremwerte
    pat=ts[['SpO2 (%)','Temp (C)','Blood Flow (ml/s)']].agg(['min','idxmin','max','idxmax'])
    extremw=pat.loc[['min','max','idxmin','idxmax']]

    # Einsetzen der Extremwerte in die Plots. Es werden hierfür Linien verwendet, 
    # da die Maximalwerte mehrmals vorkommen können.

    # Wenn Checkmarker nicht None ist erst überprüfen, sonst kommt es zu Fehler
    if algorithm_checkmarks is not None:

        # Wenn min ausgewählt wurde
        if 'min' in algorithm_checkmarks:
            plotLine(
                fig0, 
                [0, extremw.loc['idxmin',data_names[0]], 480], 
                [extremw.loc['min',data_names[0]], extremw.loc['min',data_names[0]], extremw.loc['min',data_names[0]]], 
                "magenta", "Min (" + "{:.1f}".format(extremw.loc["min",data_names[0]]) +")"
            )

            plotLine(
                fig1, 
                [0, extremw.loc['idxmin',data_names[1]], 480], 
                [extremw.loc['min',data_names[1]], extremw.loc['min',data_names[1]], extremw.loc['min',data_names[1]]], 
                "magenta", "Min (" + "{:.1f}".format(extremw.loc["min",data_names[1]]) +")"
            )

            plotLine(
                fig2, 
                [0, extremw.loc['idxmin',data_names[2]], 480], 
                [extremw.loc['min',data_names[2]], extremw.loc['min',data_names[2]], extremw.loc['min',data_names[2]]], 
                "magenta", "Min (" + "{:.1f}".format(extremw.loc["min",data_names[2]]) +")"
            )

        # Wenn max ausgewählt wurde
        if 'max' in algorithm_checkmarks:
            plotLine(
                fig0, 
                [0, extremw.loc['idxmax',data_names[0]], 480], 
                [extremw.loc['max',data_names[0]], extremw.loc['max',data_names[0]], extremw.loc['max',data_names[0]]], 
                "green", "Max (" + "{:.1f}".format(extremw.loc["max",data_names[0]]) +")"
            )

            plotLine(
                fig1, 
                [0, extremw.loc['idxmax',data_names[1]], 480], 
                [extremw.loc['max',data_names[1]], extremw.loc['max',data_names[1]], extremw.loc['max',data_names[1]]], 
                "green", "Max (" + "{:.1f}".format(extremw.loc["max",data_names[1]]) +")"
            )

            plotLine(
                fig2, 
                [0, extremw.loc['idxmax',data_names[2]], 480], 
                [extremw.loc['max',data_names[2]], extremw.loc['max',data_names[2]], extremw.loc['max',data_names[2]]], 
                "green", "Max (" + "{:.1f}".format(extremw.loc["max",data_names[2]]) +")"
            )

    return fig0, fig1, fig2 


## Blodflow Simple Moving Average Update
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph3', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-bloodflow','value')
)

def bloodflow_figure(value, bloodflow_checkmarks):
    
    ## Calculate Moving Average: Aufgabe 2
    print(bloodflow_checkmarks)
    bf = list_of_subjects[int(value)-1].subject_data
    fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s)")

    # Berechnung des Mittelwerts und Limits: Aufgabe 3
    average = bf[data_names[1]].mean()
    upper_l = average * 1.15
    lower_l = average * 0.85

    # Ploten des SMA und CMA beim letzen Graphen:
    if bloodflow_checkmarks is not None:

        # Simple Moving Average:
        if "SMA" in bloodflow_checkmarks:
            bf["Blood Flow (ml/s) SMA"] = ut.calculate_SMA(bf["Blood Flow (ml/s)"], 5) 

            # SMA wird auf eigenrlichen Plot überlagert
            plotLine(fig3, bf["Time (s)"], bf["Blood Flow (ml/s) SMA"], "magenta", "SMA")

            # Andere Möglichkeit: (plot wird erzetzt, aus Aufgabenstellung nicht klar)
            # fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s) - SMA")

        # Calculating Moving Average:
        if "CMA" in bloodflow_checkmarks:
            bf["Blood Flow (ml/s) CMA"] = ut.calculate_CMA(bf["Blood Flow (ml/s)"], 2) 
            
            # CMA wird auf eigenrlichen Plot überlagert
            plotLine(fig3, bf["Time (s)"], bf["Blood Flow (ml/s) CMA"], "green", "CMA")

            # Andere Möglichkeit: (plot wird erzetzt, aus Aufgabenstellung nicht klar)
            # fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s) - CMA")
        
        # Durchschnitt und Limits auf Plot anzeigen
        if "Show Limits" in bloodflow_checkmarks:
            plotLine(fig3, [0, 480], [average, average], "red", "Avg (" + "{:.1f}".format(average) +")")
            plotLine(fig3, [0, 480], [upper_l, upper_l], "darkorange", "Upper (" + "{:.1f}".format(upper_l) +")")
            plotLine(fig3, [0, 480], [lower_l, lower_l], "darkorange", "Lower (" + "{:.1f}".format(lower_l) +")")

    return fig3

if __name__ == '__main__':
    app.run_server(debug=True)