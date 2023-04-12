import pandas as pd
from datetime import datetime

df_amazon = pd.read_csv(r"Data\amazon_prime_titles.csv")
df_disney = pd.read_csv(r"Data\disney_plus_titles.csv")
df_hulu = pd.read_csv(r"Data\hulu_titles.csv")
df_netflix = pd.read_csv(r"Data\netflix_titles.csv")


df_amazon['show_id'] = 'a' + df_amazon['show_id'].astype(str)
df_disney['show_id'] = 'd' + df_disney['show_id'].astype(str)
df_hulu['show_id'] = 'h' + df_hulu['show_id'].astype(str)
df_netflix['show_id'] = 'n' + df_netflix['show_id'].astype(str)

df= pd.concat([df_amazon,df_disney,df_hulu,df_netflix])

df['rating'].fillna('G', inplace=True)

df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

df['type']= df['type'].astype(str)

df[['duration_int', 'duration_type.']] = df["duration"].str.split(n=1, expand=True)
df = df.drop(columns=["duration"])

df["show_id"] = df["show_id"].str.lower()
df["type"] = df["type"].str.lower()
df["title"] = df["title"].str.lower()
df["director"] = df["director"].str.lower()
df["cast"] = df["cast"].str.lower()
df["country"] = df["country"].str.lower()
df["rating"] = df["rating"].str.lower()
df["listed_in"] = df["listed_in"].str.lower()
df["description"] = df["description"].str.lower()
df["duration_type."] = df["duration_type."].str.lower()

df["duration_int"]=df["duration_int"].fillna(0)
df["duration_int"] = df["duration_int"].astype(int)
df["duration_type."] = df["duration_type."].astype(str)
df["duration_type."].replace("seasons","season",inplace=True)


# Se limpian los datos de los csv rating
# se importan los csv

df1=pd.read_csv(r"Data\rating\1.csv")
df2=pd.read_csv(r"Data\rating\2.csv")
df3=pd.read_csv(r"Data\rating\3.csv")
df4=pd.read_csv(r"Data\rating\4.csv")
df5=pd.read_csv(r"Data\rating\5.csv")
df6=pd.read_csv(r"Data\rating\6.csv")
df7=pd.read_csv(r"Data\rating\7.csv")
df8=pd.read_csv(r"Data\rating\8.csv")


df_rating= pd.concat([df1, df2,df3,df4,df5,df6,df7,df8])

df_rating = df_rating.drop(['timestamp', 'userId'], axis=1)

df_rating = df_rating.groupby('movieId')['rating'].mean().reset_index(name='rating_mean')

df_rating.rename(columns={'movieId': 'show_id'}, inplace=True)


# Volviendo al df principal

# Unimos el df de ratings al df

df = pd.merge(df, df_rating, on='show_id')

# agregamos una columna con la plataforma
def get_provider(show_id):
    if show_id.startswith('a'):
        return 'amazon'
    elif show_id.startswith('n'):
        return 'netflix'
    elif show_id.startswith('d'):
        return 'disney'
    else:
        return 'hulu'
    
df['platform'] = df['show_id'].apply(get_provider)

df.rename(columns={'rating_mean': 'scored'}, inplace=True)

df.to_csv('df_complete', index=False)

print(df)

