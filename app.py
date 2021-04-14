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

#################################
# Load plots
#################################

# Animation plot
fig_anim = plotly.io.read_json('./data_to_visualize/plot_animation.json')

# Bar plot
fig = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_year.json')

# Cloropleth plot
fig_plot = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_district_bar.json')  # to bar
#fig_plot = plotly.io.read_json('./data_to_visualize/plot_feminicide_per_district.json') # to cloropeth



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
                            children='Feminicídio à Vista surge como uma plataforma de ativismo de dados. Esta chama a atenção '
                                     'e reivindica uma resposta para o problema da violência de género em Portugal, que leva muitas '
                                     'vezes ao extermínio de mulheres. Define-se como uma plataforma open-source para questionar relações de poder.',
                    ),

                ],
            ),# Change app order
            html.Div(
                    id='continue',
                    children='Continuar a explorar abaixo',
            ),
        ],
    ),
    html.Div(
        id='manifesto_container',
        children=[
            html.Div(
                id='manifesto',
                children=[
                    html.H3("MANIFESTO"),
                    html.P(
                        id='manifesto_description',
                        children='O objetivo da plataforma Feminicídio à Vista é dar visibilidade ao problema do feminicídio e '
                                 'não deixar que as mulheres assassinadas sejam esquecidas. '
                                    'Estes crimes não podem ser vistos como desligados das questões de género e da intencionalidade de controlar a '
                                 'existência e comportamento femininos. Em alguns países, o termo feminicídio passou a estar contemplado na lei. '
                                 'Contudo, em Portugal existe um vazio legal [1] e falta de estudos a respeito do feminicídio [2]. ',
                    ),
                    html.P(
                        id='manifesto_description3',
                        children=['Se, por um lado, os dados apresentados fazem referência a casos individuais, '
                                 'por outro lado, o feminicídio é um problema que requer uma resposta da sociedade. Para isso é '
                                 'necessário agir e os primeiros passos são:',
                                dcc.Markdown('''1. reconhecer o feminicídio legalmente;'''),
                                dcc.Markdown('''2. recolher dados e identificar a ausência de dados também como informação;'''),
                                dcc.Markdown('''3. analisar dados para informar políticas e intervenções;'''),
                                dcc.Markdown('''4. e fazê-lo colaborativamente através de uma plataforma open-source;'''),
                                 'Guiado por estes princípios, o Feminicídio À Vista apresenta um conjunto de dados e estatísticas '
                                 'sobre o feminicídio em Portugal Continental.',]
                    ),
                ],
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
                            children='Na maioria dos casos de feminicídio encontrados, os intervenientes têm algum tipo de relação. '
                                     'Contudo, a multiplicidade de histórias demostra a diversidade destes crimes que não devemos esquecer.',
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
        id='frequencies_plot_section_container',
        children=[
                    html.Div(
                        id='frequencies_plot',
                        children=[
                            html.H3("NOTÍCIAS NO TEMPO"),
                            html.P(
                                id='time_description',
                                children='O número de notícias referentes a casos de feminicídio parece estar a aumentar ao longo do tempo. '
                                         'Isto pode indicar um aumento de feminicídios, um maior interesse jornalístico no tema, '
                                         'ou também uma maior facilidade em aceder a notícias mais recentes através do Arquivo.pt.',
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
        id='regions_plot_section_container',
        children=[
            html.Div(
                id='regions_plot',
                children=[
                    html.H3("NOTÍCIAS POR DISTRITOS"),
                    html.P(
                        id='regions_description',
                        children='Mais feminicídios têm ocorrido nas regiões mais populosas do país. Contudo, a relação '
                                 'entre crime e número de habitantes não é linear. Por exemplo, Braga é a terceira região '
                                 'mais populosa do país, mas aparece atrás de Setúbal e Santarém com menos casos que estes distritos.',
                    ),
                    dcc.Loading(
                        id="loading-1",
                        type="graph",
                        children=html.Div(id="loading-output-1"),
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
                        columns=[{"name": i, "id": i} for i in ['Notícia','Ano']],
                        data=df_crimes_continental_table_temp,
                        style_cell={'textAlign': 'left', 'backgroundColor': colors['table_background'],
                                    'color': colors['table_font_color_header']},
                        style_header={'backgroundColor': colors['table_background_header'], 'fontWeight': 'bold',
                                      'color': colors['table_font_color_header']},
                    ),
                ],
            ),
        ],
    ),
    html.Div(
        id='dataset_container',
        children=[
            html.Div(
                id='dataset_section',
                children=[
                    html.H3("DATASET E DETALHES"),
                    html.P(
                        id='dataset_description1',
                        children='O projecto Feminicidio à Vista complementa outros esforços de investigação [3] ao utilizar o '
                                 'Arquivo.pt para recuperar as histórias de feminicídios em Portugal e anotar um conjunto de dados '
                                 'que se disponibiliza à comunidade. Assente nos princípios de open-source, nesta plataforma é possível '
                                 'relembrar as vítimas e de uma forma dinâmica ver a relação entre as notícias individuais '
                                 'e estatísticas no tempo e espaço. ',
                    ),
                    html.P(
                        id='dataset_description2',
                        children='Estes dados podem ser utilizados não só por investigadores de diversas áreas, mas também '
                                 'para construir modelos com tecnologias de inteligência artificial e anotar novas notícias '
                                 'e propriedades das notícias referentes a feminicídios.'
                    ),

                    html.P(
                        id='dataset_description3',
                        children= [ dcc.Markdown('''O dataset pode ser acedido aqui: [dataset](https://feminicidioavistaen.herokuapp.com/)'''),
                                    '*Este projeto não é*: um conjunto de estatísticas oficiais sobre o feminicídio em Portugal. '
                                 'Neste projeto foram recolhidas notícias no Arquivo.pt como fonte de informação. '
                                 'Este método pode por si só conter erros e deixar de fora alguns casos. Apresenta-se aqui '
                                 'um esforço inicial de recolha de dados, que aponta a necessidade de documentar estes crimes '
                                 'oficialmente e de forma mais estruturada. ',
                                   '',
                                    html.H4("Fontes:"),
                                   dcc.Markdown('''\[1\] [A transversalidade dos crimes de femicídio/feminicídio no Brasil e em Portugal](https://hdl.handle.net/10216/123178)'''),
                                   dcc.Markdown('''\[2\] [Femminicidio in Europa un confronto tra paesi](https://www.europeandatajournalism.eu/ita/Notizie/Data-news/Femminicidio-in-Europa-un-confronto-tra-paesi)'''),
                                   dcc.Markdown('''\[3\] [Observatorio de mulheres assassinadas](http://www.umarfeminismos.org/index.php/observatorio-de-mulheres-assassinadas)'''),
                                   ]
                    )
                ],
            ),
        ],
    ),
    html.Div(
        id='contacto',
        children=[
            html.H3("+INFO"),
            html.P(
                id='contacto_description',
                children= [
                           dcc.Markdown(''' Para saber mais sobre o projeto e entrar em contacto com a autora podem visitar:
                           [GitHub](https://github.com/paulafortuna/feminicidioAvista) e [LinkedIn](https://pt.linkedin.com/in/paula-fortuna-a6b75a7a).'''),

                            dcc.Markdown(''' [English Version](https://feminicidioavistaen.herokuapp.com/)'''),
                           ]
            )
        ],
    ),

])


@app.callback(Output('table_year_output', 'data'), [
    Input('graph', 'clickData')])
def update_output(*args):
    year = args[0]['points'][0]['x']
    return dict_tables_per_year[str(year)]


@app.callback(Output('table_region_output', 'data'), [
    Input('choropleth', 'clickData')])
def update_output(*args):
    #district = args[0]['points'][0]['location'] #instruction to cloropeth
    district = args[0]['points'][0]['x'] #instruction to barplot
    return dict_tables_per_district[district]


if __name__ == '__main__':
    app.run_server()
    app.run_server()