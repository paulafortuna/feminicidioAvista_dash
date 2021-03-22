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
df_crimes_continental_table = pd.read_csv('./data/df_crimes_continental_save.tsv',sep='\t')
df_crimes_continental_table_temp = df_crimes_continental_table.loc[df_crimes_continental_table['district'].values == 'LISBOA']

df_crimes_continental_sorted = pd.read_csv('./data/crimes_location_continental_ordered.tsv',sep='\t')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


df_crimes_year = pd.read_csv('./data/crimes_per_year.tsv',sep='\t')
df_table = pd.read_csv('./data/table_crimes.tsv',sep='\t')
min_year = min(df_crimes_year['year'])
df_table_temp = df_table.loc[df_table['dateyear'].values == min_year]

###############################
# Color variables
##############################

colors = {
    'background': '#b2ffd7',
    'text': '#22262b',
    'plot_bar': '#22262b',
    'title': '#e2005a'
}

###############################
# Bar plot
###############################


fig = px.bar(df_crimes_year, x="year", y="0")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
)

fig.update_traces(marker_color=colors['plot_bar'])
fig.update_yaxes(showgrid=False,title='Total de Notícias')
fig.update_xaxes(title='Ano')

###############################
# Cloropleth plot
###############################

fig_plot = px.choropleth(
    df_total_crimes_district,
    locations="Distrito",
    geojson=continental_states_plot,
    featureidkey="properties.district",
    color='crimes',
    projection="mercator",
    hover_name="Distrito",
    color_continuous_scale=[colors['background'],colors['title']],)
fig_plot.update_geos(fitbounds = "locations", visible = False)
fig_plot.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                       plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'],
                       font_color=colors['text'],
                       dragmode=False,
                       geo=dict(bgcolor=colors['background'])
                       )


###############################
# Animation plot
###############################

fig_anim = px.scatter_geo(df_crimes_continental_sorted,
                     lat="lat",
                     lon="lon",
                     projection="mercator",
                     hover_name="news_site_title",
                     animation_frame="arquivo_date",
                     title="Hello"
                    )
fig_anim.update_geos(center=dict(lat=39.68, lon=-8.03),scope="europe",
    visible=True, resolution=50,showocean=True,oceancolor="#3399FF",showrivers=True,
    projection_scale=15, #this is kind of like zoom
    )

sliders = [dict(
    currentvalue={"prefix": "Data: "}
)]

fig_anim.update_layout(height=500,
                  width=750,
                  sliders=sliders,
                  title=df_crimes_continental_sorted['news_site_title'].iloc[0],
                  margin={"r":0,"t":30,"l":0,"b":0})

fig_anim.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500


for button in fig_anim.layout.updatemenus[0].buttons:
    button['args'][1]['frame']['redraw'] = True

for k in range(0,df_crimes_continental_sorted.shape[0]):
    fig_anim.frames[k]['layout'].update(title_text=df_crimes_continental_sorted['news_site_title'].iloc[k])





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
                            children='"Feminicidio à Vista" surge como uma plataforma de ativismo de dados (“datactivism”), que chama a atenção e reivindica uma resposta para o problema da violência de género em Portugal. ',
                    ),
                ],
            ),
            html.Div(
                    id='continue',
                    children='Continuar a explorar',
            ),
        ],
    ),
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
            html.P("Clique numa barra do gráfico para ver as notícias desse ano na tabela"),
            dash_table.DataTable(
                id='table_year_output',
                columns=[{"name": i, "id": i} for i in df_crimes_continental_table.columns],
                data=df_table_temp.to_dict('records'),
                style_cell={'textAlign': 'left','backgroundColor': colors['background']},
                style_header={'backgroundColor': colors['background'],'fontWeight': 'bold'},
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
            html.P("Clique num distrito no mapa para ver as notícias na tabela"),
            dash_table.DataTable(
                id='table_region_output',
                columns=[{"name": i, "id": i} for i in df_crimes_continental_table.columns],
                data=df_crimes_continental_table_temp.to_dict('records'),
                style_cell={'textAlign': 'left','backgroundColor': colors['background']},
                style_header={'backgroundColor': colors['background'],'fontWeight': 'bold'},
            ),
        ],
    ),
    html.Div([
        html.P("Por distrito:"),
        dcc.Graph(
            id='animation',
            figure=fig_anim,
        ),
    ]),
])


@app.callback(Output('table_year_output', 'data'), [
    Input('graph', 'clickData')])
def update_output(*args):
    year = args[0]['points'][0]['x']
    return df_table.loc[df_table['dateyear'].values == year].to_dict('records')


@app.callback(Output('table_region_output', 'data'), [
    Input('choropleth', 'clickData')])
def update_output(*args):
    district = args[0]['points'][0]['location']
    return df_crimes_continental_table.loc[df_crimes_continental_table['district'] == district].to_dict('records')


if __name__ == '__main__':
    app.run_server()
    app.run_server()


# divide dashboard into pages
# design
# anotar mais algumas variaveis
# organize the code
# rebuild pipeline
# documentation