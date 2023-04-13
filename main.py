
# python -m uvicorn main:app --reload
# http://127.0.0.1:8000

from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
import pandas as pd

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

    return title

 # http://127.0.0.1:8000/get_max_duration/?year=2019&platform=amazon&duration_type=min

 


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
    
    return int(count)


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
    
    # Obtener el nombre del actor que más se repite
    top_actor = max(actor_freq, key=actor_freq.get)
    
    return top_actor



@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):
    df_filtered = df.loc[(df['type'] == tipo) & (df['country'].str.contains(pais)) & (df['release_year'] == anio)]
    cantidad = df_filtered["show_id"].nunique()
    return {'pais': pais, 'anio': anio, 'peliculas': cantidad}



@app.get("/get_contents/{rating}")
def get_contents(rating: str):     
    # Controlamos que el rating ingresado sea correcto     
    rating = rating.lower()     
    ratings = ["g", "pg", "pg-13", "r", "tv-ma"]     
    if rating not in ratings:         
        return ("Rating incorrecto! Debe ingresar uno de los siguientes: g, pg, pg-13, r, tv-ma")         
    # Filtrar las películas para el rating especificado     
    df_filtered = df[(df.rating == rating)]          
    # Agrupar por rating y contar el número de filas resultantes     
    count = df_filtered.groupby('rating').size()          
    # Verificar que hay al menos una película que cumpla con los filtros     
    if df_filtered.empty:         
        return("No hay peliculas para ese rating")     
    return count.to_dict()

