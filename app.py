from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)
app_dash = dash.Dash(__name__, server=app)

italian_cities = ["Roma", "Milano", "Firenze", "Napoli", "Torino"]

# Dati per la mappa dell'Italia
italian_cities_coordinates = {
    "Roma": {"lat": 41.9028, "lon": 12.4964},
    "Milano": {"lat": 45.4642, "lon": 9.1900},
    "Firenze": {"lat": 43.7696, "lon": 11.2558},
    "Napoli": {"lat": 40.8522, "lon": 14.2681},
    "Torino": {"lat": 45.0703, "lon": 7.6869},
}

# Dati per il grafico a torta degli artisti
artists_data = {
    "Leonardo da Vinci": 30,
    "Michelangelo": 25,
    "Raffaello": 20,
    "Caravaggio": 15,
    "Botticelli": 10,
}

# Dati per le attività e i ristoranti (da sostituire con i tuoi dati reali)
activities_data = ["Visitare il Colosseo", "Museo Uffizi", "Galleria degli Uffizi", "Pompei", "Piazza San Marco"]
restaurants_data = [
    {"name": "Trattoria da Mario", "rating": 4.5},
    {"name": "Osteria Francescana", "rating": 5.0},
    {"name": "L'Antica Pizzeria da Michele", "rating": 4.2},
    {"name": "Ristorante Il Palagio", "rating": 4.8},
    {"name": "Ristorante La Pergola", "rating": 4.9},
]

app_dash.layout = html.Div(children=[
    html.Div([
        # Menu a tendina per le città italiane
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in italian_cities],
            value=italian_cities[0],
            style={'width': '50%'}
        ),
    ], style={'textAlign': 'center', 'margin-top': '20px'}),

    html.Div([
        # Mappa dell'Italia
        dcc.Graph(
            id='italy-map',
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Grafico a torta degli artisti
        dcc.Graph(
            id='artists-pie-chart',
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Lista di possibili attività
        html.H3("Possibili Attività:"),
        html.Ul(id='activities-list'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Lista di ristoranti con rating associato
        html.H3("Ristoranti con Rating:"),
        html.Ul(id='restaurants-list'),
    ], style={'width': '48%', 'display': 'inline-block'}),
])

# Callback per aggiornare la mappa dell'Italia
@app_dash.callback(
    Output('italy-map', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_italy_map(selected_city):
    fig = px.scatter_geo(
        locations=[selected_city],
        locationmode='country names',
        lon=[italian_cities_coordinates[selected_city]["lon"]],
        lat=[italian_cities_coordinates[selected_city]["lat"]],
        title=f'Mappa di {selected_city}',
        projection='natural earth',
    )
    return fig

# Callback per aggiornare il grafico a torta degli artisti
@app_dash.callback(
    Output('artists-pie-chart', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_artists_pie_chart(selected_city):
    fig = px.pie(
        names=list(artists_data.keys()),
        values=list(artists_data.values()),
        title=f'Percentuale dei Principali Artisti da Visitare a {selected_city}',
    )
    return fig

# Callback per aggiornare la lista di possibili attività
@app_dash.callback(
    Output('activities-list', 'children'),
    [Input('city-dropdown', 'value')]
)
def update_activities_list(selected_city):
    activities = activities_data  # Sostituisci con la logica per ottenere le attività reali
    activity_items = [html.Li(activity) for activity in activities]
    return activity_items

# Callback per aggiornare la lista di ristoranti con rating associato
@app_dash.callback(
    Output('restaurants-list', 'children'),
    [Input('city-dropdown', 'value')]
)
def update_restaurants_list(selected_city):
    restaurants = restaurants_data  # Sostituisci con la logica per ottenere i ristoranti reali
    restaurant_items = [html.Li(f"{restaurant['name']} - Rating: {restaurant['rating']}") for restaurant in restaurants]
    return restaurant_items

@app.route('/dashboard')
def dashboard():
    return app_dash.index()

@app.route("/")
def homepage():
    return "Hello World from Flask!"

if __name__ == '__main__':
    app.run(debug=True)