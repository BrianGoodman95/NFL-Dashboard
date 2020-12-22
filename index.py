# -*- coding: utf-8 -*-
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server

import pandas as pd
import os

import frontend
from parsers.setup import Directory_setup, Dashboard_setup
setup = Directory_setup.Create_Directories()
project_path = setup.project_path

season, week = Dashboard_setup.This_Week()
if os.path.exists(os.path.join(os.getcwd(), f'{project_path}/raw data/{season}/Week {week}', 'Spread Targets.csv')): #If the latest week has data ready
    Weeks = [w for w in range(6,week+1)]
else:
    Weeks = [w for w in range(6,week)] #Don't display this week

Data = Dashboard_setup.Data(project_path, season)

colours = Dashboard_setup.colours

# app.layout = html.Div(style={'backgroundColor': colours['background']}, children=[
app.layout = html.Div([
    html.Div([
        html.H2("NFL Betting Predictor"),
        html.Img(src="/assets/newlogo.png")
    ], className="banner"),
    html.Div([
    #     html.H1('NFL Betting Predictor',
    #         style={
    #             'textAlign': 'center',
    #             'color': colours['title']
    #         }
    #     ),
        html.H4('A Data Based Model to Pick Games and Win $$$',
            style={
            'textAlign': 'center',
            'color': colours['font']
            }
        ),
    ]),
    html.Div([
        html.Div([
            html.H4(f'Weekly Betting Guide',
                style={
                'textAlign': 'left',
                'color': colours['font'],
                'margin-left': 65,
                }
            ),
            dcc.Dropdown(id='betting-guide',
                options=[{'label': f'Week {w}', 'value': w}
                        for w in Weeks],
                value=Weeks[-1],#+Data[1][-1],
                multi=False,
                style={
                    'width': '46%',
                    'margin-left': 25,
                    'margin-right': 300,
                }
            ),
            html.Div(children=html.Div(id='Betting_Guide')),
            dcc.Interval(
                    id='week-update',
                    interval=100),
            ], className="six columns"),
        html.Div([
            html.H4('2020 Betting Results',
                style={
                    'textAlign': 'center',
                    'color': colours['graph_text']
                }
            ),
            dcc.Dropdown(id='season-results',
                options=[{'label': s, 'value': s}
                        for s in list(Data[1])[:-4]],
                value=list(Data[1])[:2],#+Data[1][-1],
                multi=True,
                style={
                    'margin-right': 25,
                }
                ),
            html.Div(children=html.Div(id='Season_Results')),
            dcc.Interval(
                id='column_update',
                interval=100),
            ], className="six columns"),#,style={'width':'50%','margin-left':10,'margin-right':10,'max-width':50000})
    ], className="row"),
    # html.Div([
    #     html.Button('Save', id='save-button', style={'margin-left': 25}),
    #     html.P(id='editable-table-hidden', style={'display':'none'}),
    #     html.P(id='save-button-hidden', style={'display':'none'}),
    # ], className='row'),
    html.Div([
        html.Div([
            html.H4('Historical Data',
                style={
                    'textAlign': 'center',
                    'color': colours['graph_text']
                }
            ),
            html.Label(['Show Accuracy By:'], style={'font-weight': 'bold', "text-align": "center","offset":1}),
            html.Div([
                dcc.Dropdown(id='historical-results',
                    options=[{'label': s, 'value': s}
                            for s in list(Data[2])[:-3]],
                    # placeholder="Select a metric to analyze the models betting accuracy...",
                    value=list(Data[2])[0]
                )
            ],
            style={
                'width': '20%',
                'horizontalAlign':'middle',
                'margin-left': 575,
                'margin-right': 575,
            },
            ),
            html.Div(children=html.Div(id='Historical_Results')),
            dcc.Interval(
                id='data-update',
                interval=100),
            ], className="twelve columns",style={'width':'80%', 'height':'100ex', 'margin-left':175,'margin-right':175,'max-width':50000})
    ], className="row")
])

# @app.callback(Output('save-button-hidden', 'children'),
#             [Input('save-button', 'n_clicks')])
# def clicks(n_clicks):
#     Spread_Targets = pd.read_csv(f'{project_path}/raw data/{season}/Week {week}/Spread Targets.csv')
#     Spread_Targets = Spread_Targets.drop('Pick', 1)
#     Spread_Targets.columns = ['Game', 'Spread', 'Expected Game Outcome', 'Pick', 'Result']
#     print(n_clicks)
#     try:
#         int(n_clicks)
#         if n_clicks > 0:
#             print('save')
#             Spread_Targets.to_csv('df.csv', index=False, encoding='utf-8')
#     except:
#         pass

@app.callback(
    dash.dependencies.Output('Betting_Guide','children'),
    [dash.dependencies.Input('betting-guide', 'value')],
    events=[dash.dependencies.State('week-update', 'interval')]
    )
def weekly_bets(week):
    Spread_Targets = pd.read_csv(f'{project_path}/raw data/{season}/Week {week}/Spread Targets.csv')
    Spread_Targets = Spread_Targets.drop('Pick', 1)
    Spread_Targets.columns = ['Game', 'Spread', 'Expected Game Outcome', 'Pick', 'Result']
    Results = []
    Results.append(dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in Spread_Targets.columns],
        data=Spread_Targets.to_dict("rows"),
        style_cell={'textAlign': 'left'},
        style_table={
            'maxHeight': '75ex',
            'overflowY': 'scroll',
            'width': '85%',
            'minWidth': '75%',
            "margin-left": 50,
            'textAlign': 'center',
            'padding-bottom': 20,
        },
        export_format="csv",
    ))

    return Results


@app.callback(
    dash.dependencies.Output('Season_Results','children'),
    [dash.dependencies.Input('season-results', 'value')],
    events=[dash.dependencies.State('column-update', 'interval')]
    )
def season_data(data_names):
    # Data = Dashboard_setup.Data(project_path, season)
    Results = []
    # for res, data in enumerate(Data):
    Make_Figure = frontend.Plots()
    fig = Make_Figure.Season_Results(Data[1],data_names)
    # Prediction_Results = frontend.Season_Results(Data[1], season)
    # fig = Prediction_Results.fig
    Results.append(html.Div(dcc.Graph(id='season-data', figure=fig)))

    return Results


@app.callback(
    dash.dependencies.Output('Historical_Results','children'),
    [dash.dependencies.Input('historical-results', 'value')],
    events=[dash.dependencies.State('data-update', 'interval')]
    )
def historical_data(data_names):
    # Data = Dashboard_setup.Data(project_path, season)
    Results = []
    # for res, data in enumerate(Data):
    Make_Figure = frontend.Plots()
    fig = Make_Figure.Historical_Results(Data[2], data_names)
    Results.append(html.Div(dcc.Graph(id='historical-data', figure=fig)))

    return Results


if __name__ == '__main__':
    app.run_server(debug=True)
