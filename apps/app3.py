import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd

from app import app
from apps.oligo_predict import primer_main

layout = html.Div([
    html.Div([
        html.H3('Design predictions for site-directed mutagenesis protocols',),
        html.H4('Primer design')
        ], style={'padding-left':'120px'}
    ),
    html.Div([
        dcc.Input(
            id='primer',
            #value='---',
            style={'fontSize':20, 'width':'40%'}
            ),
        dcc.Input(
            id='mutant',
            value='M',
            style={'fontSize':20, 'width':'5%'}
            ),
        dcc.Input(
            id='target',
            value='175',
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
        html.H6(id='SDM'),
        dcc.Graph(id='SDM_table')
    ])
])

# Call back function for SDM mutation
@app.callback(
    [Output('SDM', 'children'),
        Output('SDM_table', 'figure')],        
    [Input('submit-button', 'n_clicks')],
    [State('primer', 'value'), 
        State('target', 'value'),
        State('mutant', 'value'),
        ]
)
def output_SDM(n_clicks, cDNA, target_residue, mutant_codon):
    print(target_residue)
    target_residue = int(target_residue)
    result = primer_main(cDNA, target_residue, mutant_codon)
    mutant_string = result[1][1] + str(target_residue) + result[2][1]
    df = pd.DataFrame.from_records(result[0])
    fig = go.Figure(data=[go.Table(
        header=dict(values=['For_primer', 'Tm (celsius)', 'GC%', 'length', 'Rev_primer'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.seq, df.Tm, df.GC, df.bp, df.rev],
                    fill_color='lavender',
                    align='left'))
    ])
    return mutant_string, fig