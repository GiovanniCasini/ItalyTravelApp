from flask import Flask
import dash
from dash import dcc, html, Input, Output, State
from get_ontology import get_destinations, get_activities, get_class_activities, get_city_from_activity

# Lista di città italiane
destinations = get_destinations()
activities_list = get_class_activities()

# Inizializza l'applicazione Flask
app_flask = Flask(__name__, static_url_path='/static')

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

# Applica uno sfondo al layout direttamente in Python
app_dash.layout = html.Div(children=[
    html.H1("ITALY TRAVEL PLANNER", style={'textAlign': 'center','margin-top': '2%','font-family': 'Arial, sans-serif', 'font-size': '50px'}),
    html.H2("Choose your destination", style={'textAlign': 'center','font-family': 'Arial','margin-top': '5%'}),
    
    # Applica lo stile di sfondo al div del pulsante delle città
    html.Div([generate_city_button(city, idx) for idx, city in enumerate(destinations)],
             className='button-container', style={'text-align': 'center', 'background': 'linear-gradient(to right, #001F3F, #001C2E)'}),
    
    html.H2("...or choose which activity you would like to do in Italy", style={'textAlign': 'center','font-family': 'Arial','margin-top': '5%'}),
    
    # Applica lo stile di sfondo al div delle attività
    html.Div([generate_city_button(city, idx+len(destinations)) for idx, city in enumerate(activities_list)],
             className='button-container', style={'text-align': 'center', 'background': 'linear-gradient(to right, #001F3F, #001C2E)'}),

    # Div contenitore per attività e immagine
    html.Div([
        # Div per attività
        html.Div(id='activity-output', style={'width': '50%', 'display': 'inline-block', 'font-size': '20px',
                                               'margin-left': '5%', 'margin-top': '5%', 'vertical-align': 'top'}),
        
        # Div per l'immagine
        html.Div(id='destination-image', style={'width': '40%', 'display': 'inline-block', 'margin-right': '5%', 'margin-top': '5%'}),
    ]),

    # Store per il bottone selezionato
    dcc.Store(id='selected-button', data=0)
])

# Modifica il callback per centrare l'output delle attività
@app_dash.callback(
    [Output('activity-output', 'children'),
     Output({'type': 'button', 'index': dash.ALL}, 'style'),
     Output('destination-image', 'children')],
    [Input({'type': 'button', 'index': dash.ALL}, 'n_clicks')],
    [State('activity-output', 'children'),
     State('selected-button', 'data')]
)
def update_activities(selected_city_clicks, current_output, selected_button):
    # Trova l'indice del pulsante cliccato
    ctx = dash.callback_context
    clicked_button_index = int(ctx.triggered_id['index'])

    # Handle the case when the clicked button is related to an activity
    if clicked_button_index >= len(destinations):
        activity_index = clicked_button_index - len(destinations)
        destination = str(activities_list[activity_index])
        # Adjust the index for activities
        activities = get_city_from_activity(destination.replace(" ", "_"))
        # Adjust the clicked_button_index for styling
        clicked_button_index = activity_index + len(destinations)
        # Aggiorna l'output con le attività della città selezionata, centrato
        updated_output = [
            html.H1(f'{destination}', style={'color': 'red'}),
            html.H2(f'Explore {destination} - Information:', style={'marginTop': '20px'}),
            html.P(f"Here are some cities in which you can find {destination}:"),
            html.Ul([html.Li(activity) for activity in activities]),
        ]
    else:
        # The clicked button corresponds to a destination
        destination = str(destinations[clicked_button_index])
        # Get activities for the selected destination
        activities, is_similar_to = get_activities_for_city(destination.replace(" ", "_"))
        # Aggiorna l'output con le attività della città selezionata, centrato
        updated_output = [
            html.H1(f'{destination}', style={'color': 'red'}),
            html.H2(f'Explore {destination} - Information:', style={'marginTop': '20px'}),
            html.P(f"Discover some interesting activities in {destination}:"),
            html.Ul([html.Li(activity) for activity in activities]),
            html.H2(f"Consider visiting {is_similar_to}, a destination similar to {destination}."),
        ]

    # Aggiorna l'immagine della destinazione
    destination_image = html.Img(src=f'/static/images/{destination.lower().replace(" ", "_")}.jpg', style={'width': '100%'})

    # Aggiorna lo stile dei pulsanti
    updated_button_style = [{'width': '120px', 'height': '120px', 'background-color': 'lightblue',
                             'margin': '10px', 'fontSize': '16px', 'fontWeight': 'bold'}] * len(destinations + activities_list)
    updated_button_style[clicked_button_index] = {'width': '120px', 'height': '120px', 'background-color': 'lightgreen',
                                                   'margin': '10px', 'fontSize': '16px', 'fontWeight': 'bold'}

    return updated_output, updated_button_style, destination_image

# Aggiungi questa riga dopo la definizione di `app_dash`
if __name__ == '__main__':
    app_flask.run(debug=True)
