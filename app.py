#https://dash.plotly.com/layout

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from utils import colors
from utils import font_for_plots
import json


#################################
# Dash variables
#################################

app = dash.Dash(__name__)
app.title = 'Feminicídio à Vista'
server = app.server

#################################
# Load data
#################################


# Load news per year
with open('./data_to_visualize/dict_tables_news_per_year.json') as json_file:
    dict_tables_per_year = json.load(json_file)


min_year = min([int(i) for i in dict_tables_per_year.keys()])
df_table_temp = dict_tables_per_year[str(min_year)]

# Load news per location
with open('./data_to_visualize/dict_tables_news_per_district.json') as json_file:
    dict_tables_per_district = json.load(json_file)

df_crimes_continental_table_temp = dict_tables_per_district["LISBOA"]

##### for dot plot
#df_crimes_continental_sorted = pd.read_csv('./data/crimes_location_continental_ordered.tsv',sep='\t')


#################################
# Load plots
#################################

# Bar plot
fig = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_year.json')


# Cloropleth plot

fig_plot = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_district.json')



# Animation plot
fig_anim = plotly.io.read_json('./data_to_visualize/plot_animation.json')


###############################
# Layout
###############################

app.layout = html.Div(children=[
    html.Div(
        id='initial_page',
        children=[
            html.Div(
                id='container',
                children=[
                    html.H1(
                            id='pagename',
                            children='FEMINICÍDIO À VISTA',
                            ),
                    html.P(
                            id='pagedescription',
                            children='"Feminicidio à Vista" surge como uma plataforma de ativismo de dados (“datactivism”), que chama a atenção e reivindica uma resposta para o problema da violência de género em Portugal. ',
                    ),

                ],
            ),
            html.Div(
                    id='continue',
                    children='Continuar a explorar abaixo',
            ),
        ],
    ),
    html.Div(
        id='frequencies_plot_section_container',
        children=[
                    html.Div(
                        id='frequencies_plot',
                        children=[
                            html.H3("NOTÍCIAS NO TEMPO"),
                            html.P(
                                id='time_description',
                                children='O número de notícias referentes a casos de feminicídio parece estar a aumentar ao longo do tempo. Isto pode indicar um aumento de feminicídios, um maior interesse jornalístico no tema, ou também uma maior facilidade em aceder a notícias mais recentes.',
                            ),
                            dcc.Graph(
                                id='graph',
                                figure=fig,
                            ),
                            html.Div(
                                id='instruction_freq_plot_container',
                                children=[
                                    html.P(
                                        id="instruction_freq_plot",
                                        children="Clique numa barra do gráfico para ver as notícias desse ano na tabela",
                                    ),
                                ],
                            ),
                            html.Div(id='instruction_freq_plot_container_fill'),
                            dash_table.DataTable(
                                id='table_year_output',
                                columns=[{"name": i, "id": i} for i in ['Notícia','Distrito']],
                                data=df_table_temp,
                                editable=False,
                                style_cell={'textAlign': 'left','backgroundColor': colors['table_background'],'color': colors['table_font_color_header']},
                                style_header={'backgroundColor': colors['table_background_header'],'fontWeight': 'bold','color': colors['table_font_color_header']},
                            ),
                        ],
                    ),
                ],
    ),
    html.Div(
        id='regions_plot',
        children=[
            html.H3("NOTÍCIAS POR DISTRITOS"),
            html.P(
                id='regions_description',
                children='Mais feminicídios tèm ocorrido nas regiões mais populosas do país. Contudo, a relação entre crime e número de habitantes não é linear. ...',
            ),
            dcc.Graph(
                id='choropleth',
                figure=fig_plot,
            ),
            html.Div(id='pre_instruction_map_container_fill'),
            html.Div(
                id='instruction_map_container',
                children=[
                    html.P(
                        id="instruction_map",
                        children="Clique num distrito no mapa para ver as notícias na tabela",
                    ),
                ],
            ),
            html.Div(id='instruction_map_container_fill'),
            dash_table.DataTable(
                id='table_region_output',
                #columns=[{"name": i, "id": i} for i in df_crimes_continental_table.columns],
                columns=[{"name": i, "id": i} for i in ['Notícia','Ano']],
                data=df_crimes_continental_table_temp,
                style_cell={'textAlign': 'left', 'backgroundColor': colors['table_background'],
                            'color': colors['table_font_color_header']},
                style_header={'backgroundColor': colors['table_background_header'], 'fontWeight': 'bold',
                              'color': colors['table_font_color_header']},
            ),
        ],
    ),
    html.Div(
        id='animation_plot_section_container',
        children=[
                html.Div(
                    id='animation_plot',
                    children=[
                        html.H3("NEM UMA A MENOS!"),
                        html.P(
                            id='animation_description',
                            children='Nesta animacao coisas acontecem.Nesta animacao coisas acontecem.Nesta animacao coisas acontecem.Nesta animacao coisas acontecem.Nesta animacao coisas acontecem.Nesta animacao coisas acontecem.Nesta animacao coisas acontecem.',
                        ),
                        html.Div(id='animation_description_container_fill'),
                        html.Div(id='animation_container',
                                 children=[
                                    dcc.Graph(
                                        id='animation',
                                        figure=fig_anim,
                                    ),
                                 ],
                        ),
                    ],
                ),
        ],
    ),
    html.Div(
        id='manifesto',
        children=[
            html.H3("MANIFESTO"),
            html.P(
                id='manifesto_description',
                children='Neste manifesto.',
            )
        ],
    ),
    html.Div(
        id='contacto',
        children=[
            html.H3("CONTATO"),
            html.P(
                id='contacto_description',
                children='Contato.',
            )
        ],
    ),

])


@app.callback(Output('table_year_output', 'data'), [
    Input('graph', 'clickData')])
def update_output(*args):
    year = args[0]['points'][0]['x']
    return dict_tables_per_year[str(year)]

"""
@app.callback(Output('table_region_output', 'data'), [
    Input('choropleth', 'clickData')])
def update_output(*args):
    district = args[0]['points'][0]['location']
    return dict_tables_per_district[district]
"""


if __name__ == '__main__':
    app.run_server()
    app.run_server()


# anotar mais algumas variaveis
# organize the code
# rebuild pipeline
# documentation