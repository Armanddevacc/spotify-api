## Questions :
# 1. La popularité d'un artiste est-elle corrélée à son nombre de followers ?
# En général, pour mettre en évidence une corrélation, on utilise un graphique de dispersion (comme ce que faisaient les examinateurs en concours).
# Je ne savais pas comment coder cela, mais je me suis débrouillé.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('spotify_tracks.csv')

# Calcul de la corrélation (trouvé dans la documentation de pandas)
correlation = df['artist_popularity'].corr(df['artist_followers'])
print(f"Corrélation entre popularité et nombre de followers : {correlation}") # Sur cette échelle, 1 indique une corrélation parfaite, -1 une corrélation inversée, et 0 signifie absence de corrélation.

# Création du graphique de dispersion
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='artist_followers', y='artist_popularity', alpha=0.6)
plt.title("Relation entre la popularité et le nombre de followers des artistes")
plt.xlabel("Nombre de followers")
plt.ylabel("Popularité de l'artiste")
plt.show()

# Pour une meilleure visualisation, on peut utiliser une échelle logarithmique sur l'axe des x.

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='artist_followers', y='artist_popularity', alpha=0.6)
plt.title("Relation entre la popularité et le nombre de followers des artistes")
plt.xscale('log')  # Applique une échelle logarithmique à l'axe des x
plt.xlabel("Nombre de followers")
plt.ylabel("Popularité de l'artiste")
plt.show()

# La corrélation semble indiquer une relation positive entre le nombre de followers et la popularité de l'artiste.



# 2. La popularité de l'artiste est-elle corrélée avec la popularité de ses musiques ?
correlation = df['artist_popularity'].corr(df['track_popularity'])
print(f"Corrélation entre popularité de l'artiste et de ses musiques : {correlation}")

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='artist_followers', y='track_popularity', alpha=0.6)
plt.title("Relation entre la popularité de l'artiste et de ses musiques")
plt.xlabel("Nombre de followers")
plt.xscale('log')
plt.ylabel("Popularité d'une musique")
plt.show()

# Malgré une corrélation relativement élevée, le graphique ne montre pas de tendance nette.


# 3. Y a-t-il une évolution des genres les plus écoutés entre 2019 et 2023 ?

# Divisons les genres multiples dans des lignes distinctes car certains artistes ont plusieurs genres.
df_exploded = df.explode('artist_genres')

# Regroupons les données par année et genre pour compter les occurrences.
genre_counts = df_exploded.groupby(['playlist_year', 'artist_genres']).size().unstack(fill_value=0)

# Visualisation de l'évolution des genres par année
genre_counts.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title("Évolution des genres les plus écoutés entre 2019 et 2023")
plt.xlabel("Année")
plt.ylabel("Nombre de pistes")
plt.legend(title="Genres", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Pour éviter une surcharge visuelle, concentrons-nous sur les genres les plus populaires (par exemple, les 5 genres les plus écoutés sur cette période).

top_genres = df_exploded['artist_genres'].value_counts().head(5).index

# Filtrons les données pour ne garder que les genres les plus populaires.
filtered_data = df_exploded[df_exploded['artist_genres'].isin(top_genres)]

# Comptons les occurrences des genres populaires par année.
top_genre_counts = filtered_data.groupby(['playlist_year', 'artist_genres']).size().unstack(fill_value=0)

# Visualisation en barres groupées des genres les plus populaires
top_genre_counts.plot(kind='bar', figsize=(12, 8))
plt.title("Évolution des genres les plus populaires entre 2019 et 2023")
plt.xlabel("Année")
plt.ylabel("Nombre de pistes")
plt.legend(title="Genres", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
