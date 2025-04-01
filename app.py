import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

url = 'https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals'
tables = pd.read_html(url)
df = tables[3]

df['Year'] = df['Year'].astype(str).str.extract(r'(\d{4})').astype(int)
df['Winners'] = df['Winners'].replace('West Germany', 'Germany')
df['Runners-up'] = df['Runners-up'].replace('West Germany', 'Germany')

win_counts = df['Winners'].value_counts().reset_index()
win_counts.columns = ['Country', 'Titles']

valid_winners = df['Winners'].dropna()
valid_winners = valid_winners[valid_winners.apply(lambda x: isinstance(x, str))]

app = Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={
        'textAlign': 'center',
        'marginTop': '20px',
        'color': '#1a1a1a',
        'fontWeight': 'bold'
    }),

    html.Div([
        html.Div([
            html.Label("Select a Country:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': c, 'value': c} for c in sorted(valid_winners.unique())],
                placeholder="Choose a country"
            ),
            html.Div(id='country-output', style={'marginTop': '10px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),

        html.Div([
            html.Label("Select a Year:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': y, 'value': y} for y in sorted(df['Year'].dropna().unique())],
                placeholder="Choose a year"
            ),
            html.Div(id='year-output', style={'marginTop': '10px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'})
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),

    html.Div([
        dcc.Graph(
            figure=px.choropleth(
                win_counts,
                locations='Country',
                locationmode='country names',
                color='Titles',
                title='FIFA World Cup Wins by Country',
                color_continuous_scale='Blues'
            ).update_layout(
                title_x=0.5,
                geo=dict(showframe=False, showcoastlines=True),
                margin=dict(t=60, l=0, r=0, b=0)
            )
        )
    ], style={'padding': '0 40px 40px 40px'})
])

@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def show_wins(country):
    if not country:
        return ""
    wins = df[df['Winners'] == country].shape[0]
    return f"🏆 {country} has won the World Cup {wins} time(s)."

@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def show_final(year):
    if not year:
        return ""
    row = df[df['Year'] == year]
    if row.empty:
        return "No data for that year."
    winner = row['Winners'].values[0]
    runner_up = row['Runners-up'].values[0]
    return f"📅 In {year}, {winner} won against {runner_up}."

if __name__ == '__main__':
    app.run(debug=True)
