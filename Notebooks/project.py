from email.mime import image
import streamlit as st
import pandas as pd
import matplotlib.pylab as plt

import plotly.express as px
from PIL import Image

import pandas as pd
from streamlit_folium import st_folium
import folium
import plotly.express as px


st.set_page_config(layout="wide")

# Functions for each of the pages
def visitantes():
    # Add a title and intro text
    st.title('Visitantes')
    #st.text('grupo 193')
    #st.header('jose pardo')

    row1_1, row1_2, = st.columns((2,2))

    #Main reasons for entering the country
    base1=pd.read_csv("1. Microdatos de Migración Colombia (2021).csv",delimiter=";")
    table1=base1.groupby(["Motivo Viaje"])["Motivo Viaje"].count().sort_values(ascending=False).head(10)
    fig1 = px.bar(table1,orientation='h')
    row1_1.markdown("<h3 style='text-align: left; color: blue;'> Main reasons for entering the country </h3>", unsafe_allow_html=True)
    row1_1.plotly_chart(fig1)
 
    #Travelers per month
    table2=base1.groupby(['Meses1'])['Meses1'].count().sort_values(ascending=True)
    fig2 = px.bar(table2)
    row1_2.markdown("<h3 style='text-align: left; color: blue;'> Travelers per month </h3>", unsafe_allow_html=True)
    row1_2.plotly_chart(fig2)

    row2_1, row2_2, = st.columns((2,2))

    #Traveler’s Home Country
    table3=base1.groupby(['País Nacionalidad'])['País Nacionalidad'].count().sort_values(ascending=False).head(10)
    fig3 = px.bar(table3)
    row2_1.markdown("<h3 style='text-align: left; color: blue;'> Traveler’s Home Country</h3>", unsafe_allow_html=True)
    row2_1.plotly_chart(fig3)

    #Travelers by age range
    fig4 = px.pie(base1, values=base1.groupby(['Rango Edad'])['Rango Edad'].count(), names=base1.groupby(['Rango Edad'])['Rango Edad'].count().index,color_discrete_sequence=px.colors.sequential.dense)
    fig4.update_traces(hoverinfo='label+percent', textinfo='value')
    row2_2.markdown("<h3 style='text-align: left; color: blue;'> Travelers by age range</h3>", unsafe_allow_html=True)
    row2_2.plotly_chart(fig4)


def alojamiento():
    st.title('Alojamiento')
   
    df_turistic_places=pd.read_csv("turísticos.csv",encoding='latin1')

    #st.dataframe(df_turistic_places)
    df_turistic_places['color']=df_turistic_places["Tipo de Patrimonio"].replace({'Patrimonio cultural material inmueble':'lightblue','Patrimonio cultural inmaterial':'lightred',
                                                                              'Áreas protegidas':'orange',
                                                                              'Patrimonio Cultural Mueble':'green',
                                                                              'Aguas lénticas':'pink',
                                                                              'Montañas':'lightgreen',
                                                                              'Aguas lóticas':'lightgray',
                                                                              'Formaciones cársicas':'gray'
                                                                              }
                                                                            )
    #https://matplotlib.org/3.5.0/gallery/color/named_colors.html página de colores






    bog_coords = [4.60971,-74.08175] # lat, long
    my_map4 = folium.Map(
        location=bog_coords
    )



    for i in range(0,len(df_turistic_places)):
        html=f"""
            <h1> {df_turistic_places.iloc[i]['Tipo de Patrimonio']}</h1>
            <p></p>
            {df_turistic_places.iloc[i]['Nombre']}
            <li>{df_turistic_places.iloc[i]['Direccion Atractivo']}</li>
            </ul>
            </p>
            """
        marker=folium.Marker(location=[df_turistic_places["Latitud"].iloc[i],df_turistic_places["Longitud"].iloc[i]],
                                #popup=df_turistic_places["Nombre"].iloc[i],
                                popup=html,
                                icon=folium.Icon(color=df_turistic_places['color'].iloc[i])
                                )
        marker.add_to(my_map4)
    st.markdown("<h3 style='text-align: left; color: blue;'> Lugares Turisticos </h3>", unsafe_allow_html=True)
    st_data = st_folium(my_map4)

def seguridad():
    st.header('Seguridad ')
    st.markdown("<h3 style='text-align: left; color: blue;'> Wi-Fi hotspots </h3>", unsafe_allow_html=True)
    df_wifi=pd.read_csv('8. Base de puntos de WiFi gratuitos en Bogotá (2021).csv', delimiter=';',encoding='latin-1')
        #show df
        #st.dataframe(df_wifi.style.highlight_max(axis=0))
    df_wifi.columns=["municipio","nombre_zona_wifi","direccion","longitud","latitud"]
    df_wifi["latitud"]=df_wifi["latitud"].str.replace(",",".")
    df_wifi["longitud"]=df_wifi["longitud"].str.replace(",",".")
    df_wifi["longitud"]=df_wifi["longitud"].str.replace(" ", "")
    df_wifi["latitud"]=df_wifi["latitud"].astype(float)
    df_wifi["longitud"]=df_wifi["longitud"].astype(float)
    some_map=folium.Map(location=[df_wifi["latitud"].mean(),df_wifi["longitud"].mean()],zoom_start=10)

    for row in df_wifi.itertuples():
    
        some_map.add_child(folium.Marker(location=[row.latitud,row.longitud],popup=row.municipio))

    st_folium(some_map)



# Sidebar setup

logo = Image.open('logo.png')
st.sidebar.image(logo)
st.sidebar.title('Turismo Bogota')
st.sidebar.title('Navigation')
options = st.sidebar.radio('titulito', ['🛬Visitantes', '🏨Alojamiento', '🚓Seguridad y turismo'])

#logo_end = Image.open('ds4a.png')
#st.sidebar.image(logo_end)




# Navigation options
if options == '🛬Visitantes':
    visitantes()
elif options == '🏨Alojamiento':
    alojamiento()
elif options == '🚓Seguridad y turismo':
    seguridad()
