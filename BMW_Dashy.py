import pandas as pd
import os
import numpy as  np
import pdfkit
os.chdir(r'\\')


import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import random 
data =pd.read_csv(r"D:\Pavan\BMW Data Analysis\BMW_Data_Analysis.csv")

# Define the number of bins
num_bins = 3

# Perform equal width binning
bin_labels = ['Low', 'Medium', 'Top']
data["Speed"] = pd.cut(data['Velocity [km/h]'], bins=num_bins, labels=bin_labels)
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
img = r"assets\data-collection.png"
img1 = r"assets\channels.png"
img2 = r'assets\vehicle ran time.jpg'
img3 = r'assets\voltage.png'
img4 = r'assets\current.png'




##############KPI##################################
# Define the content of the KPI card with an online image
kpi_card_vehicle_RanTime = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img2, style={"width": "100px", "height": "100px"}),
            html.H4('vehicle ran time', className="card-title"),
            html.P("{:.2f}".format(data['Time [s]'].max()/ 3600), className="card-text"),
        ]
    ),),





# Define the content of the KPI card with an online image
kpi_card_no_of_channels = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img1, style={"width": "100px", "height": "100px"}),
            html.H4('No of Channels', className="card-title"),
            html.P( f"{len(data.columns)}", className="card-text"),
        ]
    ),),


# Define the content of the KPI card with an online image
kpi_card_no_of_samples = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img, style={"width": "100px", "height": "100px"}),
            html.H4('No of samples', className="card-title"),
            html.P(f"{len(data)}", className="card-text"),
        ]
    ),)


kpi_card_no_of_max_volt = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img3, style={"width": "100px", "height": "100px"}),
            html.H4('Max Heater Voltage', className="card-title"),
            html.P("{:.2f}".format(max(data['Heater Voltage [V]'].unique())), className="card-text"),
        ]
    ),)
    


kpi_card_no_of_max_current = dbc.Card(
    dbc.CardBody(
        [
            dbc.CardImg(src=img4, style={"width": "100px", "height": "100px"}),
            html.H4('Max Heater Curent', className="card-title"),
            html.P("{:.2f}".format(max(data['Heater Current [A]'].unique())), className="card-text"),
        ]
    ),)



cards = dbc.Container(
    [
        dbc.Row([dbc.Col(kpi_card_no_of_samples),
                 dbc.Col(kpi_card_no_of_channels),
                 dbc.Col(kpi_card_vehicle_RanTime),
                 dbc.Col(kpi_card_no_of_max_volt),
                 dbc.Col(kpi_card_no_of_max_current)]),  # Adjust the width as needed
        
    ],
    fluid=True,
)
##############KPI##################################



###########Gauge Plots##################################
# Create custom gauge component (e.g., using Plotly)
def create_gauge(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge = {
        'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 250], 'color': 'cyan'},
            {'range': [250, 400], 'color': 'royalblue'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 490}}
    ))
    fig.update_layout(height=250) 
    return fig


#######plots

# Callback to update the line plot
@app.callback(
    Output('throttle-plot', 'figure'),
    [Input('throttle-plot', 'relayoutData')]
)
def update_line_plot(relayoutData):


    # Interpolate data to create more points
    # new_time = np.linspace(data['Time [s]'].min(), data['Time [s]'].max(), 100)  # You can adjust the number of points
    # throttle_smoothed = np.interp(new_time, data['Time [s]'], data['Throttle [%]'])
    fig = go.Figure(go.Scatter(x=data['Time [s]'], y=data['Throttle [%]'], mode='lines', name='Throttle'))
    fig.update_layout(title='Time vs. Throttle (Smoothed)', xaxis_title='Time', yaxis_title='Throttle')
    fig.update_layout(width=500     )
    #fig = px.line(data, x='Time [s]', y='Throttle [%]', title='Time vs. Throttle')
    return fig



#####plot2
@app.callback(
    Output('Longi_velo_plot', 'figure'),
    [Input('Longi_velo_plot', 'relayoutData')]
)
def update_line_plot(relayoutData):


    # Interpolate data to create more points
    new_time = np.linspace(data['Time [s]'].min(), data['Time [s]'].max(), 100)  # You can adjust the number of points
    velocity_smoothed = np.interp(new_time, data['Time [s]'], data['Longitudinal Acceleration [m/s^2]'])
    fig = go.Figure(data=go.Scatter(x=new_time, y=velocity_smoothed, mode='lines', name='Longitudinal Acceleration'))
    fig.update_layout(title='Time vs. Longitudinal Acceleration (Smoothed)', xaxis_title='Time', yaxis_title='Longitudinal Acceleration')
    fig.update_layout(width=500     )
    #fig = px.line(data, x='Time [s]', y='Throttle [%]', title='Time vs. Throttle')
    return fig

#####plot3
@app.callback(
    Output('Ambi_temp_plot', 'figure'),
    [Input('Ambi_temp_plot', 'relayoutData')]
)
def update_line_plot(relayoutData):


    # Interpolate data to create more points
    new_time = np.linspace(data['Time [s]'].min(), data['Time [s]'].max(), 100)  # You can adjust the number of points
    velocity_smoothed = np.interp(new_time, data['Time [s]'], data['Ambient Temperature [°C]'])
    fig = go.Figure(data=go.Scatter(x=new_time, y=velocity_smoothed, mode='lines', name='Ambient Temperature'))
    fig.update_layout(title='Time vs. Ambient Temperature  (Smoothed)', xaxis_title='Time', yaxis_title='Ambient Temperature')
    fig.update_layout(width=500     )
    #fig = px.line(data, x='Time [s]', y='Throttle [%]', title='Time vs. Throttle')
    return fig

#####plot4
@app.callback(
    Output('SoC_plot', 'figure'),
    [Input('SoC_plot', 'relayoutData')]
)
def update_line_plot(relayoutData):


    # Interpolate data to create more points
    new_time = np.linspace(data['Time [s]'].min(), data['Time [s]'].max(), 100)  # You can adjust the number of points
    velocity_smoothed = np.interp(new_time, data['Time [s]'], data['SoC [%]'])
    fig = go.Figure(data=go.Scatter(x=new_time, y=velocity_smoothed, mode='lines', name='State of discharge'))
    fig.update_layout(title='Time vs. State of discharge  (Smoothed)', xaxis_title='Time', yaxis_title='State of discharge')
    fig.update_layout(width=500     )
    #fig = px.line(data, x='Time [s]', y='Throttle [%]', title='Time vs. Throttle')
    return fig

#####plot5
@app.callback(
    Output('Cool_Temp', 'figure'),
    [Input('Cool_Temp', 'relayoutData')]
)
def update_line_plot(relayoutData):


    # Interpolate data to create more points
    new_time = np.linspace(data['Time [s]'].min(), data['Time [s]'].max(), 100)  # You can adjust the number of points
    Cool_temp_smoothed = np.interp(new_time, data['Time [s]'], data['Coolant Temperature Heatercore [°C]'])
    fig = go.Figure(data=go.Scatter(x=new_time, y=Cool_temp_smoothed, mode='lines', name='Coolant temperature'))
    fig.update_layout(title='Time vs. Coolant temperature  (Smoothed)', xaxis_title='Time', yaxis_title='Coolant temperature')
    fig.update_layout(width=500     )
    #fig = px.line(data, x='Time [s]', y='Throttle [%]', title='Time vs. Throttle')
    return fig



#####plot6  Coolant Volume Flow +500 [l/h]
@app.callback(
    Output('Coolant_volume_flow', 'figure'),
    [Input('Coolant_volume_flow', 'relayoutData')]
)
def update_line_plot(relayoutData):


    # Interpolate data to create more points
    new_time = np.linspace(data['Time [s]'].min(), data['Time [s]'].max(), 100)  # You can adjust the number of points
    Heat_temp_smoothed = np.interp(new_time, data['Time [s]'], data['Coolant Volume Flow +500 [l/h]'])
    fig = go.Figure(data=go.Scatter(x=new_time, y=Heat_temp_smoothed, mode='lines', name='Coolant Volume flow'))
    fig.update_layout(title='Time vs. Coolant Volume flow  (Smoothed)', xaxis_title='Time', yaxis_title='Coolant Volume flow')
    fig.update_layout(width=500     )
    #fig = px.line(data, x='Time [s]', y='Throttle [%]', title='Time vs. Throttle')
    return fig



####Funnel plots
@app.callback(
    Output('speed-plot', 'figure'),
    Input('speed-plot', 'relayoutData')
)
def update_graph(relayoutData):
    # Your filtering logic here, based on the user's interactions
    # For example, if you want to filter by category 'A':
    
    
    # Create the plot
    figure = {
        'data': [
            go.Scatter(
                x=data['Speed'],
                y=data['Throttle [%]'],
                mode='lines+markers',
                
            )
        ],
        'layout': {
            'title': 'Time vs Category Plot',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Value'}
        }
    }
    return figure






def create_gauge_speed(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge = {
        'axis': {'range': [None, 200], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 100], 'color': 'cyan'},
            {'range': [100, 200], 'color': 'royalblue'}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 200}}
    ))
    fig.update_layout(height=250)
    return fig




# Create the bullet chart figure
def create_bullet_chart(voltage):
    bullet_chart = go.Figure()

    bullet_chart.add_trace(go.Indicator(
        mode="number+gauge+delta",
        value=voltage,
        delta={'reference': 12, 'position': "top"},
        title="Battery Voltage",
        gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 300]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75, 'value': 270},
        'bgcolor': "white",
        'steps': [
            {'range': [0, 150], 'color': "cyan"},
            {'range': [150, 250], 'color': "royalblue"}],
        'bar': {'color': "darkblue"}}))
    bullet_chart.update_layout(height=250)


    return bullet_chart

# Create the bullet chart figure
def create_bullet_chart1(current):
    bullet_chart = go.Figure()

    bullet_chart.add_trace(go.Indicator(
        mode="number+gauge+delta",
        value=current,
        delta={'reference': 12, 'position': "top"},
        title="Battery Current",
        gauge = {
        'shape': "bullet",
        'axis': {'range': [None, 300]},
        'threshold': {
            'line': {'color': "red", 'width': 2},
            'thickness': 0.75, 'value': 270},
        'bgcolor': "white",
        'steps': [
            {'range': [0, 150], 'color': "cyan"},
            {'range': [150, 250], 'color': "royalblue"}],
        'bar': {'color': "darkblue"}}))
    bullet_chart.update_layout(height=250)



    return bullet_chart
#############Bullets Plots##############################
Bullet_plot_vol = ([
    
    dcc.Graph(id="bullet-chart", figure=create_bullet_chart(max(data['Battery Voltage [V]'].unique()),))
])
Bullet_plot_cur = ([
    
    dcc.Graph(id="bullet-chart1", figure=create_bullet_chart1(max(data['Battery Current [A]'].unique()),))
])

line_plot = dbc.Container([dbc.Row([ 
    dbc.Col(
    
    
    
    html.Div([
    
    dcc.Graph(id='throttle-plot'),]))
])


])


##plot2
line_plot2 = dbc.Container([dbc.Row([ 
    dbc.Col(
    
    
    
    html.Div([
    
    dcc.Graph(id='Longi_velo_plot'),]))
])


])


##plot3
line_plot3 = dbc.Container([dbc.Row([ 
    dbc.Col(
    
    
    
    html.Div([
    
    dcc.Graph(id='Ambi_temp_plot'),]))
])


])


##plot4
line_plot4 = dbc.Container([dbc.Row([ 
    dbc.Col(
    
    
    
    html.Div([
    
    dcc.Graph(id='SoC_plot'),]))
])


])



##plot5
line_plot5 = dbc.Container([dbc.Row([ 
    dbc.Col(
    
    
    
    html.Div([
    
    dcc.Graph(id='Cool_Temp'),]))
])


])


##plot6
line_plot6 = dbc.Container([dbc.Row([ 
    dbc.Col(
    
    
    
    html.Div([
    
    dcc.Graph(id='Coolant_volume_flow'),]))
])


])



##plot7
line_plot7 = dbc.Container([dbc.Row([ 
    dbc.Col(
    
    
    
    html.Div([
    
    dcc.Graph(id='speed-plot'),]))
])


])


print(max(data['Heater Current [A]'].unique()))
###########Gauge Plots##################################

Analog_plots =dbc.Container([
    dbc.Row([
             
             dbc.Col(dcc.Graph(id='gauge1', figure=create_gauge_speed(max(data['Velocity [km/h]'].unique()), "Vehicle Top Speed"))),
            dbc.Col(dcc.Graph(id='gauge2', figure=create_gauge(max(data['Motor Torque [Nm]'].unique()), "Maximum Motor Torque"))),
            dbc.Col(dcc.Graph(id='gauge3', figure=create_gauge(max(data['Throttle [%]'].unique()), "Throttle"))),
    
   
            
            
            ])


                        ])

Bullet_plots =  dbc.Container([dbc.Row([
    dbc.Col(Bullet_plot_vol),dbc.Col(Bullet_plot_cur)]) ])




temp_plot_container = [line_plot3,line_plot4,line_plot5]
TimeVsOther = [line_plot,line_plot2,line_plot6]




app.layout = html.Div([#title
                        html.H1('BATTERY  HEATING DATA IN REAL DRIVING CYCLES', className='dashboard-title'),
                        html.Div(cards,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        html.Div(html.H3('1. Speed,Torque,Throttle response analysis')),
                        html.Div(Analog_plots,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        html.Div(html.H3('2.Battery Current and Voltage Analysis')),
                        html.Div(Bullet_plots,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        html.H3("3.Time vs. Temperature"),
                        html.Div(temp_plot_container,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        html.H3("4.Time vs. Other"),
                        html.Div(TimeVsOther,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),
                        html.H3("5.Funnel Chart"),
                        html.Div(line_plot7,style={'display': 'flex','backgroundColor': 'lightblue', 'padding': '10px'}),

                      ])





if __name__ == '__main__':
    # Get the HTML content of the Dash app
    

    app.run_server(debug=True)