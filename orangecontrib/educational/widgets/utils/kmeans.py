import Orange
import numpy as np
from Orange.distance import Euclidean
from scipy.spatial import distance

class Kmeans:

    max_iter = 100
    threshold = 1e-3

    def __init__(self, data, centroids=None, distance_metric=Orange.distance.Euclidean):
        self.data = data
        self.centroids = np.array(centroids) if centroids is not None else np.empty((0, 2))
        self.distance_metric = distance_metric
        self.stepNo = 0
        self.clusters = self.find_clusters(self.centroids)
        self.centroids_history = []

    @property
    def k(self):
        return len(self.centroids) if self.centroids is not None else 0

    @property
    def centroids_belonging_points(self):
        d = self.data.X
        closest_centroid = self.clusters
        return [d[closest_centroid == i] for i in range(len(self.centroids))]

    @property
    def converged(self):
        if len(self.centroids_history) == 0 or len(self.centroids) != len(self.centroids_history[-1]):
            return False
        distance = (np.sum(np.sqrt(np.sum((self.centroids - self.centroids_history[-1])**2 , axis=1)))
                    / len(self.centroids))
        return distance < self.threshold \
               or self.stepNo > self.max_iter

    @property
    def step_completed(self):
        return self.stepNo % 2 == 0

    def set_data(self, data):
        if len(data) > 0:
            self.data = data
            self.clusters = self.find_clusters(self.centroids)

            # with different data it does not make sense to have history, algorithm from begining
            self.centroids_history = []
            self.stepNo = 0
        else:
            self.data = None
            self.clusters = None
            self.centroids_history = []
            self.stepNo = 0

    def find_clusters(self, centroids):
        if self.k > 0:
            d = self.data.X
            dist = self.distance_metric(d, centroids)
            return np.argmin(dist, axis=1)
        else:
            return None

    def step(self):
        if self.step_completed:
            if len(self.centroids_history) < self.stepNo // 2 + 1:
                self.centroids_history.append(np.copy(self.centroids))
            else:
                self.centroids_history[self.stepNo // 2] = np.copy(self.centroids)
            d = self.data.X
            points = [d[self.clusters == i] for i in range(len(self.centroids))]
            for i in range(len(self.centroids)):
                c_points = points[i]
                self.centroids[i, :] = np.average(c_points, axis=0)
            # delete centroids that do not belong to any point
            self.centroids = self.centroids[~np.isnan(self.centroids).any(axis=1)]
        else:
            self.clusters = self.find_clusters(self.centroids)
        self.stepNo += 1

    def stepBack(self):
        if self.stepNo > 0:
            if not self.step_completed:
                self.centroids = self.centroids_history[self.stepNo // 2]
            else:
                self.clusters = self.find_clusters(self.centroids_history[self.stepNo // 2 - 1])
            self.stepNo -= 1

    def random_positioning(self):
        idx = np.random.choice(len(self.data), np.random.randint(1, np.min((5, len(self.data) + 1))))
        return np.mean(self.data.X[idx], axis=0)

    def add_centroids(self, points=None):
        if points is not None:
            self.centroids = np.vstack((self.centroids, np.array(points)))
        else:  # if no point provided add one centroid
            self.centroids = np.vstack((self.centroids, self.random_positioning()))
        self.clusters = self.find_clusters(self.centroids)

    def delete_centroids(self):
        self.centroids = self.centroids[:-1]
        self.clusters = self.find_clusters(self.centroids)

    def move_centroid(self, _index, x, y):
        self.centroids[_index, :] = np.array([x, y])
        self.clusters = self.find_clusters(self.centroids)
