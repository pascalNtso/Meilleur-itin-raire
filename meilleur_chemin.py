import itertools, random
import numpy as np
from scipy.spatial import distance
from sklearn.neighbors import DistanceMetric

#lecture de fichier
with open('lieux.txt', "r") as file : lines = file.readlines()

"""
Definition de la class Solver pour la résolution du problème
"""
class Solver:
    def __init__(self, distance_matrix, initial_route):
        self.distance_matrix = distance_matrix
        self.num_places = len(self.distance_matrix)
        self.initial_route = initial_route
        self.best_route = []
        self.best_distance = 0
        self.distances = []

    # mise à jour de la solution
    def update(self, new_route, new_distance):
        self.best_distance = new_distance
        self.best_route = new_route
        return self.best_distance, self.best_route

    def two_opt(self, improvement_threshold=0.01):
        self.best_route = self.initial_route
        self.best_distance = self.calculate_path_dist(self.distance_matrix, self.best_route)
        improvement_factor = 1

        while improvement_factor > improvement_threshold:
            previous_best = self.best_distance
            for swap_first in range(1, self.num_places - 2):
                for swap_last in range(swap_first + 1, self.num_places - 1):
                    new_route = self.swap(self.best_route, swap_first, swap_last)
                    new_distance = self.calculate_path_dist(self.distance_matrix, new_route)
                    self.distances.append(self.best_distance)
                    if 0 < self.best_distance - new_distance:
                        self.update(new_route, new_distance)

            improvement_factor = 1 - self.best_distance/previous_best
        return self.best_route, self.best_distance, self.distances

    @staticmethod
    def calculate_path_dist(distance_matrix, path):
        """
        This method calculates the total distance between the first city in the given path to the last city in the path.
        """
        return np.array([distance_matrix[path[i]][path[i+1]] for i in range(len(path[:-1]))]).sum()

    @staticmethod
    def swap(path, swap_first, swap_last):
        path_updated = np.concatenate((path[0:swap_first],
                                       path[swap_last:-len(path) + swap_first - 1:-1],
                                       path[swap_last + 1:len(path)]))
        return path_updated.tolist()
"""
Recherche du meilleur chemin
"""
class RouteFinder:
    def __init__(self, distance_matrix, places_names, begining=0,iterations=5, writer_flag=False):
        self.distance_matrix = distance_matrix
        self.iterations = iterations
        self.writer_flag = writer_flag
        self.places_names = places_names
        self.begining = begining

    def solve(self):
        iteration = 0
        best_distance = 0
        best_route = []
        best_distances = []

        while iteration < self.iterations:
            num_places = len(self.distance_matrix)
            tmp = random.sample(range(0, num_places), num_places)
            tmp.remove(places_names[self.begining])
            initial_route = [places_names[self.begining]] + tmp + [places_names[self.begining]]
            solution = Solver(self.distance_matrix, initial_route)
            new_route, new_distance, distances = solution.two_opt()

            if iteration == 0:
                best_distance = new_distance
                best_route = new_route

            if new_distance < best_distance:
                best_distance = new_distance
                best_route = new_route
                best_distances = distances

            iteration += 1

        if self.places_names:
            best_route = [self.places_names[i] for i in best_route]
            return best_distance, best_route
        else:
            return best_distance, best_route

# Recupération des coordonnées dan le fichier
points = []
for i,line in enumerate(lines) :
    spl = line.strip("\n\r").split(" ")
    if len(spl) == 2 :
        points.append ( (float(spl[0]), float(spl[1]) ) )
# On travail avec 10 points
extrait = points[:-10]

places_names = [i for i in range(len(points))] # dans notre cas les noms sont juste les numéros pour identifier les points

# Calcul des distances à partir des latitudes
pts = np.array(extrait)
# Metrique Haversine pour le calcul des distances en fonctions des coordonnées gps
dist = DistanceMetric.get_metric('haversine')
# Conversion en radians des coordonnées
pts[0] = np.radians(pts[0])
pts[1] = np.radians(pts[1])
# Calcul de la distance à partir de la métrique avec 6371 le rayon de la terre
dist_mat = dist.pairwise(pts)*6371
route_finder = RouteFinder(dist_mat, places_names, 2,iterations=100)
best_distance, best_route = route_finder.solve()

print('La meilleur distance obtenue: ', best_distance)
print('Le meilleur chemin: ', best_route)