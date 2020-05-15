import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import style
from app import app
from apps import home, app1#, app2

app.layout = html.Div([
    html.Div([
    html.H1('Aren\'s Data Science Portfolio', className='logo', style=style.H1_style),
    html.Nav(className = "nav nav-pills", style=style.Nav_style,
        children=[
            html.A('Home', className="home", href='/', style=style.A_style),
            html.A('SDM Calculator', className="nav-stocker", href='/app1', style=style.A_style),
            html.A('Stock chart', className="nav-DNA", href='/app2', style=style.A_style)]),
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
    # elif pathname == '/app2':
    #      return app2.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)
