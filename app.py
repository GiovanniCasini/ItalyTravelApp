from flask import Flask
import dash
from dash import dcc, html, Input, Output, State
from get_ontology import get_destinations, get_activities

# Lista di città italiane
destinations = get_destinations()

# Inizializza l'applicazione Flask
app_flask = Flask(__name__)

# Inizializza l'applicazione Dash e connettila all'app Flask
app_dash = dash.Dash(__name__, server=app_flask)

# Funzione per ottenere le attività di una città
def get_activities_for_city(dest):
    return get_activities(dest)

# Definisci la layout della dashboard Dash
def generate_city_button(city, index):
    return html.Button(
        city,
        id={'type': 'button', 'index': index},
        n_clicks=0,
        className='city-button',
        style={
            'width': '120px',
            'height': '120px',
            'background-color': 'lightblue',
            'margin': '10px',
            'fontSize': '16px',
            'fontWeight': 'bold'
        }
    )

app_dash.layout = html.Div(children=[
    html.H1("Choose your destination", style={'textAlign': 'center'}),
    html.Div([generate_city_button(city, idx) for idx, city in enumerate(destinations)],
             className='button-container', style={'text-align': 'center'}),
    html.Div(id='activity-output'),
    dcc.Store(id='selected-button', data=0)
])

# Modifica il callback per centrare l'output delle attività
@app_dash.callback(
    [Output('activity-output', 'children'),
     Output({'type': 'button', 'index': dash.ALL}, 'style')],
    [Input({'type': 'button', 'index': dash.ALL}, 'n_clicks')],
    [State('activity-output', 'children'),
     State('selected-button', 'data')]
)
def update_activities(selected_city_clicks, current_output, selected_button):
    # Trova l'indice del pulsante cliccato
    ctx = dash.callback_context
    clicked_button_index = int(ctx.triggered_id['index'])

    # Ottieni la città selezionata
    destination = str(destinations[clicked_button_index])

    # Ottieni le attività per la città selezionata
    activities, is_similar_to = get_activities_for_city(destination)

    # Aggiorna l'output con le attività della città selezionata, centrato
    updated_output = [
        html.H1(f'{destination}', style={'color': 'red'}),
        html.H2(f'Explore {destination} - Information:', style={'marginTop': '20px'}),
        html.P(f"Discover some interesting activities in {destination}:"),
        html.Ul([html.Li(activity) for activity in activities]),
        html.H2(f"Consider visiting {is_similar_to}, a destination similar to {destination}."),
    ]

    # Aggiorna lo stile dei pulsanti
    updated_button_style = [{'width': '120px', 'height': '120px', 'background-color': 'lightblue',
                             'margin': '10px', 'fontSize': '16px', 'fontWeight': 'bold'}] * len(destinations)
    updated_button_style[clicked_button_index] = {'width': '120px', 'height': '120px', 'background-color': 'lightgreen',
                                                   'margin': '10px', 'fontSize': '16px', 'fontWeight': 'bold'}

    return updated_output, updated_button_style

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
