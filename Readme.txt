Proyecto ML_OPS

VIDEO EXPLICATIVO

https://drive.google.com/drive/folders/1b6rsgCz0kaxwTE7EDZ1LBr2jOaCBI0f0?usp=sharing

Data:

https://drive.google.com/drive/folders/1b49OVFJpjPPA1noRBBi1hSmMThXmNzxn

ETL
Se realizo el proceso de ETL. Se puede observar el procedimiento en ../ETL/Limpieza de datos.py

EDA
Luego se realizó un EDA, el cual tiene su informe en ETL/informe EDA.html

Se considera que la limpieza de datos wue se realizó es satisfactoria. Existen datos en la columna rating que corresponden a la duración. Se decidió no intervenir estos datos, ya que se pidió no hacerlo. Para el modelo de ML no se usará esta columna por lo que no tiene importancia.

API

Se desarrollo una api con el módulo FASTAPI

Documentación: https://deploy-ml-ops-980r.onrender.com/docs

Se formularon 6 funciones que pueden consultarse:

1- get_max_duration(year, platform, duration_type)
Película (sólo película, no serie, ni documentales, etc) con mayor duración según año, plataforma y tipo de duración. La función debe llamarse get_max_duration(year, platform, duration_type) y debe devolver sólo el string del nombre de la película.

2- get_score_count(platform, scored, year)
Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma, con un puntaje mayor a XX en determinado año. La función debe llamarse get_score_count(platform, scored, year) y debe devolver un int, con el total de películas que cumplen lo solicitado.

3- get_count_platform(platform)
Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma. La función debe llamarse get_count_platform(platform) y debe devolver un int, con el número total de películas de esa plataforma. Las plataformas deben llamarse amazon, netflix, hulu, disney.

4- get_actor(platform, year)
Actor que más se repite según plataforma y año. La función debe llamarse get_actor(platform, year) y debe devolver sólo el string con el nombre del actor que más se repite según la plataforma y el año dado.

5- prod_per_county(tipo,pais,anio)
La cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año. La función debe llamarse prod_per_county(tipo,pais,anio) deberia devolver el tipo de contenido (pelicula,serie,documental) por pais y año en un diccionario con las variables llamadas 'pais' (nombre del pais), 'anio' (año), 'pelicula' (tipo de contenido).

6- get_contents(rating)
La cantidad total de contenidos/productos (todo lo disponible en streaming, series, documentales, peliculas, etc) según el rating de audiencia dado (para que publico fue clasificada la pelicula). La función debe llamarse get_contents(rating) y debe devolver el numero total de contenido con ese rating de audiencias.

ML

El modelo de ML se encuentra en el archivo main.py
Consiste en un modelo de similitud de coseno, a la cual proporcionamos un título, y nos devuelve 5 titulos que se relacionan.
Se aplico el metodo SVD randomize previamente, para conseguir matrices de menor tamaño, y por ende un modelo más liviano.

Se agrego a la api la siguiente funcion de ML
7- get_recommendation(titulo: str)
Éste consiste en recomendar películas a los usuarios basándose en películas similares, por lo que se debe encontrar la similitud de puntuación entre esa película y el resto de películas, se ordenarán según el score y devolverá una lista de Python con 5 valores, cada uno siendo el string del nombre de las películas con mayor puntaje, en orden descendente.


DEPLOY

Se realizó el deploy del modelo mediante render.com

link:
https://deploy-ml-ops-980r.onrender.com/

Las consultas se efectuan mediante:
https://deploy-ml-ops-980r.onrender.com/nombre_funcion/parametro1/parametro2
Por Ejemplo:
https://deploy-ml-ops-980r.onrender.com/get_max_duration/2019/amazon/season

(consultar en la documentación las diferentes funciones y sus parametros -- https://deploy-ml-ops-980r.onrender.com/docs)



