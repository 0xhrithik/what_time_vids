 # pip install DateTime dash_bootstrap_components pandas numpy plotly-express plotly dash dash-renderer dash-html-components dash-core-components gunicorn 
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

df = pd.read_csv("export_dataframe.csv")    
# ------------------------------------------------------------------------------
# App layout\
app.layout = html.Div([
# dbc.Jumbotron(
#     [
        dbc.Container(
            [
                html.H1("Youtube Channel Analytics of MKBHD", className="display-4", style={'text-align': 'center'}),
                html.P(
                    "Check the time of the day at which does the channel uploads videos", style={'text-align': 'center'},className="lead",
                ),
            ],
            fluid=True,
        ),
#     ],
#     fluid=True,
# ),
    # html.H1("Youtube Channel Analytics of MKBHD", style={'text-align': 'center'},className="display-4"),
    # html.H2("Visual Representation of the time at which the channel uploads videos", style={'text-align': 'center'}),
    
    dbc.Select(id="slct_year",
                 options=[
                     {"label": "ALL", "value": 'ALL'},
                     {"label": "2008", "value": 2008},
                     {"label": "2009", "value": 2009},
                     {"label": "2010", "value": 2010},
                     {"label": "2011", "value": 2011},
                     {"label": "2012", "value": 2012},
                     {"label": "2013", "value": 2013},
                     {"label": "2014", "value": 2014},
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019},
                     {"label": "2020", "value": 2020}],
                #  multi=False,
                 value='ALL',
                 style={'width': "30%"}
                ),

    dbc.Container(
            [
                html.P(className="lead",id='output_container', children=[]
                ),
                html.P(className="lead",id='videos_count', children=[]
                ),
            ],
            fluid=True,
        ),
    # html.Br(),
    # html.Div(id='output_container', children=[]),
    # html.Br(),
    # html.Div(id='videos_count', children=[]),
    # html.Br(),
    dcc.Graph(id='mkbhd_timeline', config={
        'displayModeBar': False
        }, figure={})
])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
    # [Output(component_id='output_container', component_property='children'),
     [Output(component_id='mkbhd_timeline', component_property='figure'),
     Output(component_id='videos_count', component_property='children')
    ],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    # container = "You chose : {}".format(option_slctd) if (option_slctd != 'ALL') else None
    
    def parse_publish_timestamp(video):
        return (datetime.strptime(video, "%Y-%m-%dT%H:%M:%SZ")+ timedelta(hours=5, minutes=30))
    dff = df.copy()
    print(option_slctd)
    if (option_slctd != 'ALL') :
        dff = dff[dff["Year"] == int(option_slctd)]
    publish_timestamps = [parse_publish_timestamp(x) for x in dff['ts']]
    publish_times = [t.hour + t.minute/60 for t in publish_timestamps]

    if option_slctd != 'ALL':
        data = "MKBHD uploaded {} videos in {}".format(len(publish_times),option_slctd)
    else:
        data = "MKBHD uploaded {} videos from 2008-2020".format(len(publish_times))
    print(len(publish_times))
    counts, bins = np.histogram(publish_times, bins=24)
    bins = 0.5 * (bins[:-1] + bins[1:])

    fig = px.bar(x=bins, y=counts, template='plotly_dark', labels={'x':'24 Hours (IST)', 'y':'Videos count'})
    # fig.show()
    
    # fig = px.histogram(
    #     data_frame=dff,
    #     x=publish_times,
    #     nbins=24,
    #     title=f'Publish times of MKBHD',
    #     color_discrete_sequence=['indianred'],
    #     template='plotly_dark',
    # )
    return fig, data

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
