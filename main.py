
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
import pickle
from sklearn.decomposition import randomized_svd

df = pd.read_csv("df_complete")
df_peliculas = pd.read_csv("df_titulos.csv")
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


# Recomendacion

# Vectorización de los títulos
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['title'])

# Descomposición en valores singulares aleatorios (randomized SVD)
u, s, vt = randomized_svd(X, n_components=100)

# Cálculo de la similitud de coseno
def cosine_similarities(x, y):
    return np.dot(x, y.T)

# Recomendación de títulos similares

@app.get("/get_recommendation/{title}")
def get_recommendation(title):
    # Vectorización del título de entrada
    title_vec = vectorizer.transform([title])

    # Reducción de dimensionalidad del título de entrada
    title_vec_reduced = title_vec.dot(vt.T)

    # Cálculo de la similitud de coseno
    sim = cosine_similarities(title_vec_reduced, u.dot(np.diag(s)))

    # Ordenamiento de los títulos según su similitud de coseno
    sim_scores = list(enumerate(sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Recomendación de títulos similares
    sim_scores = sim_scores[1:6]
    indices = [i[0] for i in sim_scores]
    titles = df.iloc[indices]['title']

    return {'recomendacion':titles.tolist()}