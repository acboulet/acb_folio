import dash


#Pulling dash v2.0 css from chriddyp on codepen
# Will try to make my own sometime in the future, but can adjust anything directly in the future.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#from app import app
from apps import home, app1, app3#, app2

A_style={'paddingRight':'30px',
        'color':'#202020',
        'paddingLeft':'100px',
        'float':'left',
        'fontSize': '24px',
        'text-decoration':'none',
        'font-variant':'small-caps',
        'padding-top': '3px'
        }

header_style={'fontSize': '32px',
        'font-weight':'600',
        'text-transform': 'uppercase',
        'padding-left':'60px',
        'text-align':'Middle',
        'paddingTop':'5px',
        #'margin-top': '5px',
        #'margin-bottom': '5px',
        #'margin':'10px',
        }

Nav_style={'background-color': '#DFB887',
        'height': '35px',
        'width': '100%',
        'opacity': '.9',
        'margin-bottom': '10px'}

app.layout = html.Div([
    html.Div([
    html.H2('Aren\'s Data Science Portfolio', className='logo', style=header_style ),
    html.Nav(className = "nav nav-pills", style=Nav_style, 
        children=[
            html.A('Home', className="home", href='/', style=A_style ),
            html.A('SDM Calculator', className="nav-stocker", href='/app1',style=A_style),
            html.A('SDM Predictor', className="nav-DNA", href='/app3', style=A_style)]),
            ],style={'background-color':'#9c805e',
                        'height':'105px'}),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/app1':
        return app1.layout
    elif pathname == '/app3':
        return app3.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)