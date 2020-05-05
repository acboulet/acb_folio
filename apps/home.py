import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import style
from app import app

layout = html.Div([
    html.H2('Data analysis portfolio for Aren Boulet', style = style.H2_style),
    html.P("""My name is Aren Boulet, and I built this website to display a portfolio of my coding skillset. This website 
            and all subsequent data analysis was coded using Python."""),
], style={'padding-left':'120px'}
)



if __name__ == '__main__':
    app.run_server()
