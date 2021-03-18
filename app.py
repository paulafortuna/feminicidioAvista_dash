#https://dash.plotly.com/layout

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#19181A',
    'text': '#B19F9E'
}


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ]),
    ])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('./data/crimes_per_year.tsv',sep='\t')
df_table = pd.read_csv('./data/table_crimes_year_2016.tsv',sep='\t')

fig = px.bar(df, x="year", y="0")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Feminicidio à Vista',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='"Feminicidio à Vista" surge como uma plataforma de ativismo de dados (“datactivism”), que chama a atenção e reivindica uma resposta para o problema da violência de género em Portugal. ', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='graph',
        figure=fig
    ),
    html.Pre(id='output')
    #html.H6("Clica num ano para ver as notícias."),
    #generate_table(df_table)
])


@app.callback(Output('output', 'children'), [
    Input('graph', 'clickData')])
def update_output(*args):
    return json.dumps(args, indent=2)


if __name__ == '__main__':
    app.run_server()