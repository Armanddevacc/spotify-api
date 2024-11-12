import requests
import base64
import pandas as pd

client_id = 'dbd1fe4bb9ca407ea57f5f17a34581d4'
client_secret = '10487077aed44a0eb0f127c9197e7a5d' #cette clé serait normalement caché pour éviter des soucis



## recupérons d'abord le token/jeton pour faire des requetes, ils ont une durée d'une heure


# Encodez les identifiants en base64
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Obtenez le jeton d'accès
url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {encoded_credentials}"
}
data = {
    "grant_type": "client_credentials"
}

response = requests.post(url, headers=headers, data=data)
token = response.json().get("access_token")




## la doc nous donne comme ce formatage pour les requetes GET /playlists/{playlist_id}
## on ne connait pas les idées des requetes donc on utilise les requetes GET /search/q/type/market/limit

# pour intégrès le token d'accé à la requete on créé le header:
headers = {
    "Authorization": f"Bearer {token}"
}



def get_playlist_id():
    L = []
    for year in range(2019, 2024):
        params = {
            "q": f"Top Hits of {year}",
            "type": "playlist",
            "limit": 1  # Limite de 1 pour trouver une playlist représentative
        }  
        url = "https://api.spotify.com/v1/search"
        response = requests.get(url, headers=headers,params=params)
        print(year , "done")
        data = response.json()
        L.append((data['playlists']['items'][0]['id'],year))
    return L


def get_playlist_tracks(playlist_id,year):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = requests.get(url, headers=headers)
    track_data = response.json()

    tracks = []
    for item in track_data['items']:
        track_info = item['track']
        artist_info = track_info['artists'][0]  # en analysant les données on a ça, on ne prend pas en compte les feat
        
        # Obtenons des informations supplémentaires sur l'artiste
        artist_url = f"https://api.spotify.com/v1/artists/{artist_info['id']}"
        artist_response = requests.get(artist_url, headers=headers)
        artist_data = artist_response.json()
        
        # Collectons les données nécessaires
        track_details = {
            'track_name': track_info['name'],
            'album_name': track_info['album']['name'],
            'album_release_date': track_info['album']['release_date'],
            'track_duration_ms': track_info['duration_ms'],
            'track_popularity': track_info['popularity'],
            'artist_name': artist_data['name'],
            'artist_followers': artist_data['followers']['total'],
            'artist_genres': artist_data['genres'],
            'artist_popularity': artist_data['popularity'],
            'playlist_year': year

        }
        tracks.append(track_details)
    
    return tracks


# Récupérez les IDs des playlists et leurs pistes
playlists = get_playlist_id()
all_tracks = []
for playlist_id,year in playlists:
    tracks = get_playlist_tracks(playlist_id,year)
    all_tracks.extend(tracks)

# Convertir en DataFrame 
df = pd.DataFrame(all_tracks)

# Sauvegarde des données dans un fichier CSV pour un accès facile, en plus ça prend du temps de tout charger
df.to_csv('spotify_tracks.csv', index=False)

print("Données enregistrées dans 'spotify_tracks.csv'")