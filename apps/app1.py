import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from oligo_class import oligo

import sys 
sys.path.append('..')

from app import app
import style

# primer = 'atcg'

# mutations = 3
# class oligo():
#     """Functions for characterization of site-directed mutagenesis primers"""
#     def __init__(self, primer, mutations):
#         self._primer = self.prep(primer)
#         self._mutations = mutations

#     def prep(self, primer):
#         """
#         Function will provide a string value in all lowercases while removing all spaces

#         :param primer: Input primer sequence in string format
#         :return: Primer in string format without spaces and all lowercase letters
#         """
#         primer= ''.join(primer.split())
#         primer= primer.lower()
#         return(primer)

#     def comp(self):
#         """
#         Function will calculate total number of GC bases

#         :param primer: Input primer sequence in string format
#         :return: Integer value of total number of GC bases
#         """
#         GC= 0
#         for i in self._primer:
#             if i in 'gc':
#                 GC += 1
#         return GC

#     def F_lockdown(self):
#         """
#         Function will provide boolean answer to whether primer ends in GC pair

#         :param primer: Input primer sequence in string format
#         :return: Boolean answer to whether primer terminates with GC
#         """
#         if self._primer[-1] in 'gc':
#             return True
#         else:
#             return False

#     def R_lockdown(primer):
#         """
#         Function will provide boolean answer to whether primer begins with G or C

#         :param primer: Input primer sequence in string format
#         :return: Boolean answer to whether primer begins with G or C
#         """
#         if self._primer[0] in 'gc':
#             return True
#         else:
#             return False

#     def content(self):
#         """
#         Calculates percentage content of GC in primer

#         :param primer: Input primer sequence in string format
#         :return: Float value of GC%
#         """
#         gc = oligo.comp(self._primer)
#         size = len(self._primer)
#         gc_content = round(gc / size * 100)
#         return gc_content


#     def Tm_temp(self):
#         """
#         Calcualtes Tm using Strategene site-directed mutagenesis formula

#         :param primer: Input primer sequence in string format
#         :param mutations: Integer value representing total number of mutations to create
#         :return: Float value represent Tm (in C) of primer
#         """
#         Tm= 81.5 + ((0.41 * oligo.content(self._primer))) - (675 / (len(self._primer)) - (self._mutations))
#         Tm = round(Tm, 1)
#         return Tm


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
