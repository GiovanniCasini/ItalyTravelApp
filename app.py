from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery
from get_ontology import get_destinations, get_activities

# Lista di città italiane
destinations = get_destinations()

# Inizializza l'applicazione Flask
app_flask = Flask(__name__)

# Inizializza l'applicazione Dash e connettila all'app Flask
app_dash = dash.Dash(__name__, server=app_flask)

# Funzione per ottenere le attività di una città
def get_activities_for_city(city):
    return get_activities()

# Definisci la layout della dashboard Dash
# Modifica la parte relativa all'output delle attività nella layout della dashboard Dash
app_dash.layout = html.Div(children=[
    html.H1("Choose your destination", style={'textAlign': 'center'}),
    html.Div(
        [
            html.Button(città, id={'type': 'button', 'index': idx}, n_clicks=0, className='city-button', style={'width': '100px', 'height': '100px'})
            for idx, città in enumerate(destinations)
        ],
        className='button-container',
        style={'text-align': 'center'}
    ),
    html.Div(id='activity-output', style={'textAlign': 'center'})  # Aggiunto 'textAlign': 'center' qui
])

# Modifica il callback per centrare l'output delle attività
@app_dash.callback(
    Output('activity-output', 'children'),
    [Input({'type': 'button', 'index': ALL}, 'n_clicks')],
    [State('activity-output', 'children')]
)
def update_activities(selected_city_clicks, current_output):
    # Trova l'indice del pulsante cliccato
    ctx = dash.callback_context
    clicked_button_index = int(ctx.triggered_id['index'])

    # Ottieni la città selezionata
    selected_city = destinations[clicked_button_index]

    # Ottieni le attività per la città selezionata
    activities = get_activities_for_city(selected_city)

    # Aggiorna l'output con le attività della città selezionata, centrato
    return [
        html.H3(f'Activities in {selected_city}', style={'textAlign': 'center'}),
        html.Div([html.P(activity) for activity in activities], style={'textAlign': 'center'})
    ]

# Aggiungi una route per la tua dashboard Dash
@app_flask.route('/dashboard')
def dashboard():
    return app_dash.index()

# Aggiungi una route di esempio per l'app Flask
@app_flask.route("/")
def homepage():
    return "Hello World from Flask!"

# Esegui l'applicazione Flask
if __name__ == '__main__':
    app_flask.run(debug=True)