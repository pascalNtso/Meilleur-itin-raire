# Meilleur-itin-raire
Étant donné qu'un ensemble de données contenant la latitude et la longitude des lieux qui doivent être visités par un véhicule (le véhicule revient à sa position initiale), nous proposons un algorithme optimisé écrit en python pour déterminer le meilleur itinéraire (distance parcourue la plus courte).

# Librairies
Les librairies suivantes ont été utilisées:
- *Numpy:* Pour faciité et optimiser l'utilisation des arrays.
- *Sklearn:* Pour générer les métriques de calcul de distance
- *scipy.spatial:* Pour le calcul des distances à partir des coordonnées gps. Celle est ainsi facilité

Nous utilisons la méthode 2opt décrite dans cet article: https://towardsdatascience.com/how-to-solve-the-traveling-salesman-problem-a-comparative-analysis-39056a916c9f

Plus le nombre d'itération dans l'algorithme est grand, plus on se raproche de la solution optimale

## Exemple pour 100 itérations
<img src="exemple.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
