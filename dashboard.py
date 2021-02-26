from datetime import date
from random import choice, random

import dash
import dash_core_components as dcc
import dash_html_components as html


import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

test_data = pd.read_csv("data/world_data.csv")

today = date.today()

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

external_stylesheets= [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "COVID Dashboard - UK Edition"



app.layout = html.Div([
            html.Nav(className="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow", children=[
                html.A(className="navbar-brand col-sm-3 col-md-2 mr-0", children="COVID-19"),
                    
                    # dcc.DatePickerRange(className="date-and-location",
                    #                     id="month-picker",
                    #                     min_date_allowed=date(2020, 1, 30),
                    #                     max_date_allowed=date(today.year, today.month, today.day),
                    #                     start_date=date(2020, 3, 1),
                    #                     end_date=date(today.year, today.month, today.day),
                    #                     style={"height": "50%"}
                    #                     ),
                
                ]),
            html.Div(className="container-fluid", children=[
                html.Div(className="row", children=[
                    html.Nav(className="col-md-2 d-none d-md-block bg-light sidebar", children=[
                        
                        html.Div(className="sidebar-sticky", children=[
                            html.H6(className="sidebar-heading d-flex px-3 mt-4 mb-1 text-muted", children=[
                                html.Span("Custom Search"),
                            ]),
                            html.Ul(className="nav flex-column", children=[
                                html.Li(className="nav-item", children=[
                                    dcc.Link("User Search", href="/home"),
                                ])]),
                            html.H6(className="sidebar-heading d-flex px-3 mt-4 mb-1 text-muted", children=[
                                html.Span("Preset Search"),
                            ]),
                            dcc.Location(id="url", refresh=False),
                            html.Ul(className="nav flex-column", children=[
                                html.Li(className="nav-item", children=[
                        
                                    dcc.Link("Africa", href="/africa"),
                                        html.Span(className="sr-only"),
                                        ]),
                                html.Li(className="nav-item", children=[
                         
                                    dcc.Link("Asia", href="/asia"),
                                        html.Span(className="sr-only"),
                                        ]),
                                html.Li(className="nav-item", children=[
                                    dcc.Link("Europe", href="/europe"),
                                        html.Span(className="sr-only"),
                                        ]),
                                html.Li(className="nav-item", children=[
                                    dcc.Link("North America", href="/northamerica"),
                                        html.Span(className="sr-only"),
                                        ]),
                                html.Li(className="nav-item", children=[
                                    dcc.Link("South America", href="/southamerica"),
                                        html.Span(className="sr-only"),
                                        ]),
                                html.Li(className="nav-item", children=[
                                    dcc.Link("Oceania", href="/oceania"),
                                        html.Span(className="sr-only"),
                                        ]),
                                    ]),
                            html.Div(id='page-content'),
                          
                            html.Ul(className="nav flex-column mb-2")
                        ]),
                    ]),
                    html.Main(role="main", className="col-md-9 ml-sm-auto col-lg-10 px-4", children=[
                        html.Div(className="chartjs-size-monitor", style={"position": "absolute", "left": "0px", "top": "0px", "right": "0px", "bottom": "0px", "overflow": "hidden", "pointer-events": "none", "visibility": "hidden", "z-index": "-1"}),
                        
                        html.Div(className="box-shadow", children=[
               
                                 ]),
                        dbc.Row(
                                    [
                                        dbc.Col(children=[
                                            html.H1(children="Deaths"),
                                            html.Hr(className="lead"),
                                            html.Div(id="death-stats", children="######"),
                                            ]),
                                        dbc.Col(children=[
                                            html.H1(children="Cases"),
                                            html.Hr(className="lead"),
                                            html.Div(id="cases-stats", children="######"),
                                            ]),
                                        dbc.Col(children=[
                                            html.H1(children="Vaccines"),
                                            html.Hr(className="lead"),
                                            html.Div(id="vaccines-stats", children="######"),
                                        ]),
                                    ]
                        ),
                        
                                html.Div(className="graphs", children=[
                                        dcc.Graph(
                                        id="cases-graph"
                                        ),
                                        dcc.Graph(
                                        id="deaths-graph",
                                        ),
                                ]),
                    ])])])])






def dropdown(location, user_enabled, display):
    return dcc.Dropdown(
                                id="location",
                                options=[
                                    {"label": location, "value": location} for location in test_data["location"].unique()
                                ],
                                value=location,
                                searchable=False,
                                disabled=user_enabled,
                                style={"display": display}
                        ),



@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    
    if pathname == '/africa':
        return dropdown("Africa", True, "none")
    elif pathname == '/asia':
        return dropdown("Asia", True, "none")
    elif pathname == '/europe':
        return dropdown("Europe", True, "none")
    elif pathname == '/northamerica':
        return dropdown("North America", True, "none")
    elif pathname == '/southamerica':
        return dropdown("South America", True, "none")
    elif pathname == '/oceania':
        return dropdown("Oceania", True, "none")
    else:
        return dropdown("United Kingdom", False, "block")
        

@app.callback(
    [Output("cases-graph", "figure"), Output("deaths-graph", "figure"), Output("death-stats", "children"), Output("cases-stats", "children"), Output("vaccines-stats", "children")],
    [
        # Input('month-picker', "start_date"),
        # Input("month-picker", "end_date"),
        Input("location", "value"),
    ],
)
def update_personal_ouput(value):
    # start_date, end_date, ):




    filtered_data_cases = test_data.loc[(test_data["location"] == value)] 
    # //& (test_data["date"] >= start_date) & (test_data["date"] <= end_date)]

    fig_deaths = px.bar(filtered_data_cases, x="date", y=["new_deaths_smoothed"], color_discrete_sequence=["mediumaquamarine"], title=f"COVID Deaths - {value}", labels={"value": "Number of Deaths", "date": "Date", "variable": "Legend"})
    fig_deaths.update_layout(title_x=0.5, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig_deaths.add_scatter(x=filtered_data_cases["date"], y=filtered_data_cases["new_deaths_smoothed"].rolling(window=7, min_periods=7, center=True).mean().round(), name="Rolling Average")

    fig_cases = px.bar(filtered_data_cases, x="date", y=["new_cases_smoothed"], color_discrete_sequence=["mediumaquamarine"], title=f"COVID Cases - {value}", labels={"value": "Number of Cases", "date": "Date", "variable": "Legend"})
    fig_cases.update_layout(title_x=0.5, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    fig_cases.add_scatter(x=filtered_data_cases["date"], y=filtered_data_cases["new_cases_smoothed"].rolling(window=7, min_periods=7, center=True).mean().round(), name="Rolling Average")

    latest_deaths = f'{filtered_data_cases["new_deaths"].iloc[-1]:.0f} today'
    latest_cases = f'{filtered_data_cases["new_cases"].iloc[-1]:.0f} today'
    
    # last_vaccines_index = filtered_data_cases["new_vaccinations"].last_valid_index()
    # latest_vaccines = f'{filtered_data_cases["new_vaccinations"][last_vaccines_index]:.0f} today'
    latest_vaccines = f'{filtered_data_cases["new_vaccinations"].iloc[-2]:.0f} today'

    
    return fig_deaths, fig_cases, latest_deaths, latest_cases, latest_vaccines



if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_ui=False)
