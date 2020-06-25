import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd

from index import app
from apps.oligo_predict import primer_main

layout = html.Div([
    html.Div([
        html.H3('Design predictions for site-directed mutagenesis protocols',),
        ], style={'padding-left':'120px', 'padding-right':'120px'}
    ),
    html.Div([
        html.H5("""The following script was coded in Python and relies Biopython for managing DNA sequences, translations, and additional functions. 
        """),
        html.H6('Computer science relevant information'),
        html.P("""The following script was coded in Python and relies Biopython for managing DNA sequences, translations, and additional functions. 
        The script uses indexing to select the specific region within the provided string (coding DNA sequence). It then recursively checks potential
        primer sequences for match to primer design recommendations (discussed below). The DNA sequence is progressively shortened and checked for
        design criteria. This list is returned, converted to a Pandas dataframe and
        displayed below using Plotly graphing. Full script can be found on github, user: acboulet.
        """),
        html.H6('Biochemical relevant information'),
        html.P("""The script will generate a list of potential primers that can be used for designing site-directed mutatagenesis primers. I have
        used this same formula to successfully generate dozens of mutant proteins for use in in-vitro functional assays, endogenous expression in
        mammalian cells, and import assays in bacterial systems. The Tm is calculated according to Stratagene's recommendations and the following formula:
        Tm = 81.5 + (0.41 * GC%) - (675 / (len_primer - no_mutations)). Primers with a Tm between 78 and 82 degrees have proven successful. In addition,
        only primers that terminate in a GC base pairing are recommended.
        """),
        html.H6('Using the program'),
        html.P("""All DNA sequences must only use ATGC nomenclature. Begin be pasting your gene information in the first box. Secondly, type in the 
        three nucleotide codon representing the new amino acid residue you want inserted (ie: ATG for M). Lastly, type in the target residue number
        you wish to mutate. For example, if you want to mutate the 175th residue to methionine, you would type ATG as the "New codon" and 175 as the "Target
        residue".
        """),
        ], style={'padding-left':'120px', 'padding-right':'120px'}
    ),
    html.Div([
        dcc.Textarea(
            id='primer',
            #value='',
            placeholder='Paste gene sequence here',
            style={'fontSize':20, 'width':'60%', 'height':'100px'}
            )
        ], style={'padding-left':'120px'}),
    html.Div([
        dcc.Input(
            id='mutant',
            #value='mutant codon',
            placeholder='New codon',
            style={'fontSize':20, 'width':'20%'}
            ),
        dcc.Input(
            id='target',
            #value='target residue',
            placeholder='Target residue',
            style={'fontSize':20, 'width':'20%'}
            ),
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':20}
            )
                ], style={'padding-left':'120px'}),
    html.Div([
        html.Br(),
        html.H6(id='SDM',
                style={'padding-left':'120px', 'padding-right':'120px'}),
        dcc.Graph(id='SDM_table')
    ]),
    html.Div([
        html.H6('Choosing your primer',),
        html.P("""This script will provide you a list of potential primers, and you will have to choose one set for your own work. 
        The highest priority is to ensure that your mutant codon is close to the middle of the primer. This provides optimal binding 
        on either side of the mutation. This script could identify primers where the mutant codon is towards either end of the sequence.
        In addition, you can take into account GC content or length for what's appropriate in your PCR reaction. 
        """),
        html.H6('Running the PCR itself',),
        html.P("""These primers have worked successfully using a 2-step PCR. The first 6-steps of a 30-step PCR are carried out in two separate 
        reactions with only the F_primer + template OR R_primer + template. After the 6th step, the two reactions are mixed and allowed to continue. 
        The default Phusion polymerase protocol in HF buffer with 8% DMSO has proved to be effective in these reactions. After the PCR, the template
        strand is digested with Dpn I followed by ethanol precipitation. The precipitate is resuspended in 10uL of water and 2uL of this reaction is 
        used for transformations.
        """)
    ], style={'padding-left':'120px', 'padding-right':'120px'})
]) #First div

# Call back function for SDM mutation
# Will adjust when it receives a button click as input, and use whateverthe state value of the TextArea, and two Input areas are above
# Input order: button, cDNA seq, target residue, and mutant codon
# Output order is the point mutant descriptor, then the table with all possible primers
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
    target_residue = int(target_residue)
    mutant_codon = mutant_codon.upper()
    result = primer_main(cDNA, target_residue, mutant_codon)
    mutant_ = result[1][1] + str(target_residue) + result[2][1]
    mutant_string = 'This is the mutation that you are planning to generate: '+ mutant_
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