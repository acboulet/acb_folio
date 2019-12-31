import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import sys 
sys.path.append('..')

from app import app
import style

#primer = 'atcg'

#mutations = 3
class oligo():
    """Functions for characterization of site-directed mutagenesis primers"""
    def __init__(self, primer, mutations):
        self.primer = primer
        self.mutations = mutations

    def prep(primer):
        primer= ''.join(primer.split())
        primer= primer.lower()
        primer= str(primer)
        return(primer)

    def comp(primer):
        GC= 0
        for i in primer:
            if i == 'g' or i =='c':
                GC += 1
            else:
                GC += 0
        return GC

    def F_lockdown(primer):
        if primer[-1] == 'c' or primer[-1] == 'g':
            return True
        else:
            return False

    def R_lockdown(primer):
        if primer[0] == 'c' or primer[0] == 'g':
            return True
        else:
            return False

    def content(primer):
        gc = oligo.comp(primer)
        size = len(primer)
        gc_content = round(gc / size * 100)
        return gc_content


    def Tm_temp(primer, mutations):
        Tm= 81.5 + ((0.41 * oligo.content(primer))) - (675 / (len(primer)) - (mutations))
        Tm = round(Tm, 1)
        return Tm



layout = html.Div([
    html.Div([
        html.H2('Design primers for site-directed mutagenesis protocols'),
        html.P('Primer design')
        ], style=style.H2_style),
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
        html.H2(id='primer_size')
        ], style={'padding-left':'140px'})
])
#Input print
@app.callback(
    Output('primer-out', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('primer', 'value')])
def output(n_clicks, primer):
    primer=oligo.prep(primer)
    return '{} was input'.format(primer)

#Tm print
@app.callback(
    Output('Tm_calc', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('primer', 'value'),State('mutate', 'value')])
def output(n_clicks, primer, mutate):
    mutations = int(mutate)
    primer=oligo.prep(primer)
    return('Tm primer is: ' + str(oligo.Tm_temp(primer, mutations)) + '\xb0' + 'C')

#GC content
@app.callback(
    Output('GC_per', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('primer', 'value')])
def output(n_clicks, primer):
    primer=oligo.prep(primer)
    return('Primer GC% is: ' + str(oligo.content(primer)) + '%')

#Primer length
@app.callback(
    Output('primer_size', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('primer', 'value')])
def output(n_clicks, primer):
    primer=oligo.prep(primer)
    return('Primer size is ' + str(len(primer)) + 'bp')

if __name__ == '__main__':
    app.run_server()
