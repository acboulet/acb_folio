# Application page to import graph from saskatoonOverlayMap, and display
# Future work will allow users to compare results, and choose between different datasets

import dash
import dash_core_components as dcc
import dash_html_components as html


from index import app
from apps.saskatoonOverlayMap import createSaskMap

layout = html.Div([
    html.Div([
        html.H3('Title'),
    ], className="four columns"), # left side
    html.Div([
        dcc.Graph(figure = createSaskMap(), id = "saskMap"),
    ], className= "eight columns"), # right side
])