#https://dash.plotly.com/layout

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# import geo data
import json
with open('./data/temp_json.json') as json_file:
    continental_states_plot = json.load(json_file)
df_total_crimes_district = pd.read_csv('./data/total_crimes_district.tsv',sep='\t')



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'background': '#19181A',
    'text': '#B19F9E'
}


#def generate_table(dataframe, max_rows=10):
#    return html.Table([
#        html.Thead(
#            html.Tr([html.Th(col) for col in dataframe.columns])
#        ),
#        html.Tbody([
#            html.Tr([
#                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#            ]) for i in range(min(len(dataframe), max_rows))
#        ]),
#    ])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_crimes_year = pd.read_csv('./data/crimes_per_year.tsv',sep='\t')
df_table = pd.read_csv('./data/table_crimes.tsv',sep='\t')
min_year = min(df_crimes_year['year'])
df_table_temp = df_table.loc[df_table['dateyear'].values == min_year]

fig = px.bar(df_crimes_year, x="year", y="0")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig_plot = px.choropleth(
    df_total_crimes_district,
    locations="Distrito",
    geojson=continental_states_plot,
    featureidkey="properties.district",
    color='crimes',
    projection="mercator",
    hover_name="Distrito")
fig_plot.update_geos(fitbounds = "locations", visible = False)
fig_plot.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Feminicídio à Vista',
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
    html.Pre(id='output'),
    html.H6("Clica numa barra para ver as notícias desse ano."),
    dash_table.DataTable(
        id='table_output',
        columns=[{"name": i, "id": i} for i in df_table.columns],
        data=df_table_temp.to_dict('records'),
    ),
    html.Div([
        html.P("Por distrito:"),
        dcc.Graph(
            id='choropleth',
            figure=fig_plot,
        ),
    ])
])


@app.callback(Output('table_output', 'data'), [
    Input('graph', 'clickData')])
def update_output(*args):
    year = args[0]['points'][0]['x']
    return df_table.loc[df_table['dateyear'].values == year].to_dict('records')


if __name__ == '__main__':
    app.run_server()
    app.run_server()

# map connecting to the table
# map with the cursor
# divide dashboard into pages
# design
# anotar mais algumas variaveis
# organize the code
# rebuild pipeline
# documentation