
# python -m uvicorn main:app --reload
# http://127.0.0.1:8000

from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


df = pd.read_csv("df_complete")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


class ShowIDRequest(BaseModel):
    year: int
    platform: str
    duration_type: str

@app.get("/get_max_duration/{year}/{platform}/{duration_type}")
def get_max_duration(year: int , platform: str, duration_type: str):

    # Seleccionar las filas correspondientes a los parámetros de entrada
    filtered_df = df[(df['release_year'] == year) & (df['platform'] == platform) & (df['duration_type.'] == duration_type)]

    # Obtener el índice de la fila con la duración máxima
    max_duration_index = filtered_df['duration_int'].idxmax()

    # Obtener el valor de la columna "show_id" correspondiente a la fila con la duración máxima
    title = filtered_df.loc[max_duration_index, 'title']
    

    return {'pelicula': title}


 # http://127.0.0.1:8000/get_max_duration/?year=2019&platform=amazon&duration_type=min


@app.get("/get_score_count/{platform}/{scored}/{year}")
def get_score_count(platform: str, scored: float, year: int):
    # Seleccionar los registros que corresponden al año y al puntaje especificado
    df_filtered = df.loc[(df['release_year'] == year) & (df['scored'] > scored)]
    
    # Filtrar los registros para obtener solo las películas
    df_movies = df_filtered.loc[df['type'] == 'movie']
    
    # Filtrar los registros para obtener solo las películas que no son documentales
    df_no_doc = df_movies[~df_movies['listed_in'].str.contains('documentary', regex=False)]
    
    # Filtrar los registros para obtener solo las películas que se encuentran en la plataforma especificada
    df_platform = df_no_doc.loc[df['platform'] == platform]
    
    # Contar el número de registros que cumplen los criterios anteriores
    count = len(df_platform)

    return {
        'plataforma': platform,
        'cantidad': count,
        'anio': year,
        'score': scored
    }

@app.get("/get_count_platform/{platform}")
def get_count_platform(platform:str):
   
    # Filtrar los registros para obtener solo las películas
    df_movies = df.loc[df['type'] == 'movie']
    
    # Filtrar los registros para obtener solo las películas que no son documentales
    df_no_doc = df_movies[~df_movies['listed_in'].str.contains('documentary', regex=False)]
    
    # Filtrar los registros para obtener solo las películas que se encuentran en la plataforma especificada
    df_platform = df_no_doc.loc[df['platform'] == platform]
    
    # Contar el número de registros que cumplen los criterios anteriores
    count = len(df_platform)
    
    return {'plataforma': platform, 'peliculas': int(count)}



@app.get("/get_actor/{platform}/{year}")
def get_actor(platform:str, year:int):
    # Seleccionar los registros que corresponden a la plataforma y al año especificado
    df_filtered = df.loc[(df['platform'] == platform) & (df['release_year'] == year)]

    # Eliminar las filas con valores nulos en la columna "cast"
    df_filtered = df_filtered.dropna(subset=['cast'])
    
    # Separar los nombres de los actores en listas de strings
    actor_lists = df_filtered['cast'].str.split(', ')
    
    # Crear un diccionario que mapea cada actor con su frecuencia de aparición
    actor_freq = {}
    for actor_list in actor_lists:
        for actor in actor_list:
            if actor in actor_freq:
                actor_freq[actor] += 1
            else:
                actor_freq[actor] = 1
                
      # Crear una lista de tuplas con el nombre del actor y su frecuencia de aparición
    actor_tuples = [(actor, freq) for actor, freq in actor_freq.items()]
    
    # Ordenar la lista por frecuencia de aparición
    actor_tuples.sort(key=lambda x: x[1], reverse=True)

    actor_nombre = actor_tuples[0][0]
    actor_apariciones =  actor_tuples[0][1]
   
    return {
        'plataforma': platform,
        'anio': year,
        'actor': actor_nombre,
        'apariciones': actor_apariciones
    }


@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):
    df_filtered = df.loc[(df['type'] == tipo) & (df['country'].str.contains(pais)) & (df['release_year'] == anio)]
    cantidad = df_filtered["show_id"].nunique()
    return {'pais': pais, 'anio': anio, 'peliculas': cantidad}



@app.get("/get_contents/{rating}")
def get_contents(rating: str):        
    # Filtrar las películas para el rating especificado     
    df_filtered = df[(df.rating == rating)]          
    # Agrupar por rating y contar el número de filas resultantes     
    count = len(df_filtered)  

    return {'rating': rating, 'contenido': count}


@app.get("/get_recommendation/{titulo}")
def get_recommendation(titulo: str):
    # Paso 1: Cargar los datos
    df_peliculas = df

    # Paso 2: Preprocesamiento
    # Convertir el nombre de las películas a minúsculas y remover los caracteres especiales
    df_peliculas['title'] = df_peliculas['title'].str.lower().str.replace('[^\w\s]','')

    # Paso 3: Vectorización
    vectorizer = TfidfVectorizer()
    matriz_tfidf = vectorizer.fit_transform(df_peliculas['title'])

    # Paso 4: Calcular la similitud
    similitud_cos = cosine_similarity(matriz_tfidf)

    # Paso 5: Obtener las recomendaciones
    nombre_pelicula = titulo
    indice_pelicula = df_peliculas[df_peliculas['title'] == nombre_pelicula].index[0]

    similitud_pelicula = list(enumerate(similitud_cos[indice_pelicula]))
    similitud_pelicula_ordenada = sorted(similitud_pelicula, key=lambda x: x[1], reverse=True)

    peliculas_recomendadas = []
    for i, sim in similitud_pelicula_ordenada:
        if len(peliculas_recomendadas) == 5:
            break
        if i == indice_pelicula:
            continue
        peliculas_recomendadas.append(df_peliculas.iloc[i]['title'])

    return {'recomendacion':peliculas_recomendadas}

    