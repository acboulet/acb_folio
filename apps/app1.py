import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


from app import app
from apps.oligo_class import oligo
import style

layout = html.Div([
    html.Div([
        html.H2('Design primers for site-directed mutagenesis protocols', style=style.H2_style),
        html.P('Primer design')
        ], style={'padding-left':'120px'}
    ),
    html.Div([
        dcc.Input(
            id='primer',
            #value='',
            style={'fontSize':20, 'width':'40%'}
            ),
        dcc.Input(
            id='mutate',
            value='0',
            style={'fontSize':20, 'width':'5%'}
            ),
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':20}
            )
                ], style={'padding-left':'120px'}),
    html.Div([
        html.H2(id='primer-out'),
        html.H2(id='Tm_calc'),
        html.H2(id='GC_per'),
        html.H2(id='primer_size'),
        ], style={'padding-left':'140px'})
])


#Input print
@app.callback(
    Output('primer-out', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('primer', 'value')])
def output(n_clicks, primer):
    primer= oligo(primer)._primer
    return '{} was input'.format(primer)

#Tm print
@app.callback(
    Output('Tm_calc', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('primer', 'value'),State('mutate', 'value')])
def output(n_clicks, primer, mutate):
    mutations = int(mutate)
    primer= oligo(primer)
    return('Tm primer is: ' + str(primer.Tm_temp(mutations)) + '\xb0' + 'C')

#GC content
@app.callback(
    Output('GC_per', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('primer', 'value')])
def output(n_clicks, primer):
    primer= oligo(primer)
    return('Primer GC% is: ' + str(primer.content()) + '%')

#Primer length
@app.callback(
    Output('primer_size', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('primer', 'value')])
def output(n_clicks, primer):
    primer= oligo(primer)
    return('Primer size is ' + str(len(primer._primer)) + 'bp')

if __name__ == '__main__':
    app.run_server()
