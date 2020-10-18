#IMPORTS--------------------------------------------------------------x

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import requests

import pycountry

import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import plotly.tools as tls

import json

"""datas"""

import matplotlib.pyplot as plt
""" import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xlrd """


#DEFINIR FUNCIONES----------------------------------------------------x

"codigo del pais"
def get_alpha_3(location):
    try:
        return pycountry.countries.get(name=location).alpha_3 #Obtener el nombre del pais
    except:
        return None

"leer los data frames"
def Datas(file_name):
  data=pd.read_csv(file_name)
  return data



#FORMATOS--------------------------------------------------------------x

"1er formato utilizado (style)"
external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
font={'size':9,'color':'rgb(30,30,30)'}

"colores"
colors = ['rgb(239,243,255)','rgb(189,215,231)','rgb(107,174,214)','rgb(33,113,181)']




#MAPA-------------------------------------------------------------------x

#Global

df_w=pd.read_excel('general.xlsx')
df_w=df_w.drop(columns=df_w.columns[2:-1])
df_w['P']=df_w['P'].str.replace(' ','')
df_w=df_w.pivot(index='P',columns='Banco',values='Satisfaccion').fillna(0)

df_w['code']=['COL','MEX','ESP']
bancos=df_w.columns[1:-1]
World = px.scatter_geo(df_w, locations="code",projection="natural earth",hover_data={'code':False})
for i in bancos:
    World.add_trace(go.Scattergeo(
        locations=df_w['code'],
        text = i,
        mode = 'markers',
    marker=dict(
            size = df_w[i]*120)
        ))




#Mexico
df_mex=pd.read_csv('MexicoData.csv')
mex_repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json' #Archivo GeoJSON
mx_regions_geo = requests.get(mex_repo_url).json()

Mexico = px.choropleth(data_frame=df_mex, 
                    geojson=mx_regions_geo, 
                    locations='Estado', # nombre de la columna del Dataframe
                    featureidkey='properties.name'  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                   )
    
Mexico.update_geos(fitbounds="locations",visible=False)

Mexico.update_layout(
    title_text = 'México',
    font=dict(
        family="serif",
        size=20,
        color="black"
    )
)

#Colombia
df_col=pd.read_csv('ColombiaData.csv',encoding='latin1')
df_col.columns=['dpt']

df_col['dpt']=df_col['dpt'].str.replace('\"','').str.upper()
df_col['dpt']=df_col['dpt'].str.normalize('NFKD')       .str.encode('ascii', errors='ignore')       .str.decode('utf-8')
df_col.loc[df_col['dpt']=='NARINO','dpt']='NARIÑO'

col_repo_url = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json' 

col_regions_geo = requests.get(col_repo_url).json()

Colombia = px.choropleth(data_frame=df_col, 
                    geojson=col_regions_geo, 
                    locations='dpt', # nombre de la columna del Dataframe
                    featureidkey='properties.NOMBRE_DPT',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                    scope="south america"
                   )

Colombia.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")

Colombia.update_layout(
    title_text = 'Colombia',
    font=dict(
        family="serif",
        size=20,
        color="black"
    )
)

#Spain
with open('comunidades-autonomas-espanolas.geojson') as f:
    data_spain = json.load(f)
    
#Extraemos cada ciudad:
ciudades=[dc['properties']['comunidade_autonoma'] for dc in  data_spain['features']]

df_spain=pd.Series(ciudades,name='comu_autono')


#Creamos figura
Spain = px.choropleth(data_frame=df_spain, 
                    geojson= data_spain, 
                    locations='comu_autono', # nombre de la columna del Dataframe
                    featureidkey='properties.comunidade_autonoma',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                    scope='europe'     
                    
                   )

Spain.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")

Spain.update_layout(
    title_text = u'España',
    font=dict(
        family="serif",
        size=20,
        color="black"
    )
)


#GRAFICAS---------------------------------------------------------------x
#grafica 1-world
df_1 = pd.read_excel("Interacciones.xlsx")
df_1.head(9)
    
Grafica_world_1 = px.pie(df_1, values = "Followers", names = "Tipo_Banco")

Grafica_world_1.update_layout(
    title_text= "FOLLOWERS - BANCOS - WORLD",
    font=dict(
        family="serif",
        size=20,
        color="Black"
    )
)
#grafica 2-world

    
Grafica_world_2 = px.bar(df_1, x="Tipo_Banco", y="Likes/day", color="Pais", barmode="group",
             category_orders={"Tipo de Banco": bancos})

Grafica_world_2.update_layout(
    title_text= "LIKES - BANCOS - WORLD",
    font=dict(
        family="serif",
        size=20,
        color="Black"
    )
)

#grafica 3-world



df_tree = pd.read_excel("freq_total_2.xlsx")
df_tree["Mundo"] = "Mundo" # in order to have a single root node
Grafica_world_3 = px.treemap(df_tree, path=['Mundo', 'pais', 'banco'], values='freq',
                  color='freq', #hover_data=['iso_alpha'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df_tree['freq'], weights=df_tree['freq']))


# grafica 4-world

Grafica_world_4 = px.treemap(df_tree, path=['Mundo', 'banco', 'palabra'], values='freq',
                  color='freq', #hover_data=['iso_alpha'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df_tree['freq'], weights=df_tree['freq']))


#------------------------------------------------------------------------------##
#GRAFICAS COLOMBIA

df = pd.read_excel("general2.xlsx")
df_col = df[df['P']== 'Colombia']
Grafica_col_1 = go.Figure(data = [
    go.Bar(name = 'Positivos', x = df_col['Banco'], y = df_col['Positivos']),
    go.Bar(name = 'Negativos', x = df_col['Banco'], y = df_col['Negativos']),
    go.Bar(name = 'Neutros', x = df_col['Banco'], y = df_col['Neutros'])
])

Grafica_col_1.update_layout(barmode = 'stack')



#------------------------------------------------------------------------------##
#GRAFICAS MEXICO
df_col = df[df['P']== 'México']
Grafica_mex_1 = go.Figure(data = [
    go.Bar(name = 'Positivos', x = df_col['Banco'], y = df_col['Positivos']),
    go.Bar(name = 'Negativos', x = df_col['Banco'], y = df_col['Negativos']),
    go.Bar(name = 'Neutros', x = df_col['Banco'], y = df_col['Neutros'])
])

Grafica_mex_1.update_layout(barmode = 'stack')

#------------------------------------------------------------------------------##
#GRAFICAS ESPAÑA
df_col = df[df['P']== 'España']
Grafica_esp_1 = go.Figure(data = [
    go.Bar(name = 'Positivos', x = df_col['Banco'], y = df_col['Positivos']),
    go.Bar(name = 'Negativos', x = df_col['Banco'], y = df_col['Negativos']),
    go.Bar(name = 'Neutros', x = df_col['Banco'], y = df_col['Neutros'])
])

Grafica_esp_1.update_layout(barmode = 'stack')

#-----------------------------------------------------------------------x
#Dash board y Layout (creacion de aplicacion web)

aplicacion = dash.Dash(__name__)

aplicacion.layout=html.Div([
                html.Div([
                    html.H1("Satisfaccion bancaria de paises hispano-hablantes"
                    ),
                    html.Img(src="/PICTURES/MACC_icon.png")
                ],className="banner"),
                
                    html.Div(
                    style={"width":"25%"}
                    ),
                    dcc.Dropdown(
                        id="dropdown",
                        options=[
                        {'label': 'World', 'value': 'World'},
                        {'label': 'Colombia', 'value': 'Colombia'},
                        {'label': 'Mexico', 'value': 'Mexico'},
                        {'label': 'Spain', 'value': 'Spain'}
                        ],
                        value='World'
                    ), 
                    #Grafica del mapa
                    dcc.Graph(
                        id="graph-court"
                    ),
                    html.H3("============================================================================= Mapa Global de satisfaccion ============================================================================="
                    ),
                    (html.H5("La idea del proyecto es analizar los comentarios de las quejas y reclamaciones de BBVA y otros dos bancos competidores en Colombia, México y España. Los datos los extraeremos de las páginas de opiniones (a través de scraping) y Twitter. Asimismo, analizaremos el impacto de BBVA y la pandemia del COVID-19 de acuerdo a los comentarios de Twitter de los tres países mencionados. Aplicaremos modelos de similitud con NLP y análisis de sentimientos. Finalmente, representaremos los resultados en un dashboard en python.")
                    ),dcc.Graph(id="Graph"
                    ),
                    html.H2("Informacion y graficas de bancos 2"
                    ),dcc.Graph(id="Graph2"),
                     html.H2("Informacion y graficas de bancos 3"
                    ),dcc.Graph(id="Graph3"),
                     html.H2("Informacion y graficas de bancos 4"
                    ),dcc.Graph(id="Graph4"),

                    ])

"Actualizar el mapa con la sleccion del dropdown"

@aplicacion.callback(Output('graph-court', 'figure'), 
              [Input('dropdown', 'value')])


def update_figure(selected_value):
    if selected_value == 'World':
        newf=World
    elif selected_value == 'Colombia':
        newf=Colombia
    elif selected_value == 'Mexico':
        newf=Mexico
    elif selected_value == 'Spain':
        newf=Spain
    return newf

@aplicacion.callback(Output('Graph', 'figure'), 
              [Input('dropdown', 'value')])

def update_figure_2(selected_value):
    if selected_value == 'World':
        newG=Grafica_world_1
    elif selected_value == 'Colombia':
        newG=Grafica_col_1
    elif selected_value == 'Mexico':
        newG=Grafica_mex_1
    elif selected_value == 'Spain':
        newG=Grafica_esp_1
    return newG

@aplicacion.callback(Output('Graph2', 'figure'), 
              [Input('dropdown', 'value')])

def update_figure_3(selected_value):
    if selected_value == 'World':
        newG=Grafica_world_2
    elif selected_value == 'Colombia':
        pass
    elif selected_value == 'Mexico':
        pass
    elif selected_value == 'Spain':
        pass
    return newG


@aplicacion.callback(Output('Graph3', 'figure'), 
              [Input('dropdown', 'value')])

def update_figure_4(selected_value):
    if selected_value == 'World':
        newG=Grafica_world_3
    elif selected_value == 'Colombia':
        newG=Grafica_world_3
    elif selected_value == 'Mexico':
        newG=Grafica_world_3
    elif selected_value == 'Spain':
        newG=Grafica_world_3
    return newG

@aplicacion.callback(Output('Graph4', 'figure'), 
              [Input('dropdown', 'value')])

def update_figure_5(selected_value):
    if selected_value == 'World':
        newG=Grafica_world_4
    elif selected_value == 'Colombia':
        newG=Grafica_world_4
    elif selected_value == 'Mexico':
        newG=Grafica_world_4
    elif selected_value == 'Spain':
        newG=Grafica_world_4
    return newG

if __name__=="__main__":
    aplicacion.run_server(debug=True, use_reloader=False)