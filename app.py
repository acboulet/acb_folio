import dash


#Pulling dash v2.0 css from chriddyp on codepen
# Will try to make my own sometime in the future, but can adjust anything directly in the future.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
