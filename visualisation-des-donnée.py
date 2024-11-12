## questions: 
#1. La popularité d’un artiste est-elle corrélée à son nombre de followers ?
# généralement pour mettre en valeur une corrélation on fait un graphique dispersion (ce que les examinateurs fessaient au concours). je ne savais pas comment coder ça, mais je me suis dérbouillé
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('spotify_tracks.csv')

# Calcul de la corrélation (j'ai trouvé ça chez panda)
correlation = df['artist_popularity'].corr(df['artist_followers'])
print(f"Corrélation entre popularité et nombre de followers : {correlation}") # sur cette echelle on vise 1, -1 est une corrélation inversé et 0 absence de corélation

# Création du graphique de dispersion
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='artist_followers', y='artist_popularity', alpha=0.6)
plt.title("Relation entre la popularité et le nombre de followers des artistes")
plt.xlabel("Nombre de followers")
plt.ylabel("Popularité de l'artiste")
plt.show()

# à vrai dire pour une meilleur visualisation on peut faire la même chose avec une echelle log


plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='artist_followers', y='artist_popularity', alpha=0.6)
plt.title("Relation entre la popularité et le nombre de followers des artistes")
plt.xscale('log')  # Applique une échelle logarithmique à l'axe des x
plt.xlabel("Nombre de followers")
plt.ylabel("Popularité de l'artiste")
plt.show()


#On peut ainsi repondre oui à la question 

#2. Ou à la popularité de ses tracks ? 
correlation = df['artist_popularity'].corr(df['track_popularity'])
print(f"Corrélation entre popularité de l'artiste et des tracks : {correlation}") 

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='artist_followers', y='track_popularity', alpha=0.6)
plt.title("Relation entre la popularité de l'artiste de ces musiques")
plt.xlabel("Nombre de followers")
plt.xscale('log')
plt.ylabel("Popularité d'une musique d'un artiste")
plt.show()
# malgres une corrélation haute on observe rien graphiquement


#Y a-t-il une évolution des genres les plus écoutés entre 2019 et 2023 ? 


# Diviser les genres multiples dans des lignes distinctes car certains artiste ont plusieurs genre
df_exploded = df.explode('artist_genres')


# Regrouper les données par année et genre pour compter
genre_counts = df_exploded.groupby(['playlist_year', 'artist_genres']).size().unstack(fill_value=0)

# Visualisation
genre_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title("Évolution des genres les plus écoutés entre 2019 et 2023")
plt.xlabel("Année")
plt.ylabel("Nombre de pistes")
plt.legend(title="Genres", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()







#Pour éviter un graphique surchargé, nous pouvons nous concentrer sur les genres les plus populaires (par exemple, les 5 genres les plus écoutés sur la période)

top_genres = df_exploded['artist_genres'].value_counts().head(5).index

# Filtrer les données pour ne garder que les genres les plus populaires
filtered_data = df_exploded[df_exploded['artist_genres'].isin(top_genres)]

# Compter les occurrences des genres populaires par année
top_genre_counts = filtered_data.groupby(['playlist_year', 'artist_genres']).size().unstack(fill_value=0)

# Visualisation en barres groupées
top_genre_counts.plot(kind='bar', figsize=(12, 8))
plt.title("Évolution des genres les plus populaires entre 2019 et 2023")
plt.xlabel("Année")
plt.ylabel("Nombre de pistes")
plt.legend(title="Genres", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()








