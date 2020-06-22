import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

#from app import app

layout = html.Div([
    html.Div([
        html.H5('Data analysis portfolio for Aren Boulet'),
        html.P("""My name is Aren Boulet, and I built this website to display a portfolio of my coding skillset.  The idea of coming to work every day to solve new and interesting problems 
            is what motivates me. Part of what makes
            solving problems exciting to me is continously building my toolset to tackle these challenges. In the past that's involved reading papers, and learning new technical skills
            for experiments. To help expand my toolset, computer programming seemed like the perfect next step. The goal of this website is to display some of my projects, either those 
            designed to maximize my time at work or projects out of the enjoyment of coding.
            """),
        html.H6('Computer science skills'),
        html.P("""I began to learn Python by completing classes on Codeacademy, and Udemy. It was really exciting for me to learn this new skill, and felt like I was playing with LEGO again
            as a kid. Each LEGO block was a different piece of code, and my goal was to build something exciting. My first projects were ones focused on benefiting my job.
            I used pandas, matplotlib, and plotly libraries to examine and present my data in new ways, and I wrote my own scripts for primer design. I then started to use these skills on my
            own to solve challenges on adventofcode or build this website. I've recently been taking University courses to help build my theoretical understanding of computer program.
            This website was built using Dash, stored on Github, and subsequently deployed on Heroku. The applications within a built using Python and a variety of libraries.
            """),
        html.H6('Scientific accomplishments'),
        html.P("""Over my decade of research experience I have worked in academic research and biotechnology product development. I've successfully published in academic journals,
            presented at international conferences, and received multiple scholarships. I have a wide variety of technical skills involving molecular cloning, cell culture, mouse 
            models of human disease, antibody characterizations, and protein purification. Research provides a dynamic and challenging environment that motivates my own growth.
            """),
        html.H6('Links'),
    ], className='six columns'),
    html.Div([
        # Need to center image
        html.Img(src='assets/portrait.png')        
    ], className='six columns')
], style={'padding-left':'120px'}
)



if __name__ == '__main__':
    app.run_server()
