import numpy as np
from graph.polygon import Polygon
from graph.graph import CountryVertex, Graph
from parser_countries import Point
from math import ceil


class Generator:
    def __init__(self, wanted_count_of_color):
        self.color_count = wanted_count_of_color

    def generate_map(self):
        graph = Graph(list())
        coloring = 0
        while coloring < self.color_count:
            country = self.generate_country()
            count_of_neighbor = 0
            for vertex in graph.vertices:
                if vertex.is_contiguous_vertex(country) or \
                        country.is_contiguous_vertex(vertex):
                    count_of_neighbor += 1
            if count_of_neighbor == len(graph.vertices):
                graph.add_vertex(country)
                coloring += 1
        return graph

    def generate_country(self):
        count_of_region = np.random.randint(1, 3)
        regions = dict()
        country = CountryVertex(regions)
        count_of_generate_regions = 0
        while count_of_generate_regions < count_of_region:
            new_region = Polygon(self.generate_polygon())
            vertex = CountryVertex({0: new_region})
            if not vertex.is_contiguous_vertex(country) and \
                    not country.is_contiguous_vertex(vertex):
                country.add_region(new_region)
                count_of_generate_regions += 1
        return country

    def generate_polygon(self):
        count_of_points = np.random.randint(5, 6)
        x = np.random.randint(-30, 30, count_of_points)
        y = np.random.randint(-30, 30, count_of_points)
        center_point = [ceil(np.sum(x) / count_of_points),
                        ceil(np.sum(y) / count_of_points)]
        angles = np.arctan2(x - center_point[0], y - center_point[1])
        sort_tups =\
            sorted([(i, j, k)
                    for i, j, k in zip(x, y, angles)],
                   key=lambda t: t[2])
        x, y, angles = zip(*sort_tups)
        x = list(x)
        y = list(y)
        x.append(x[0])
        y.append(y[0])
        coordinates = list()
        for i in range(count_of_points):
            coordinates.append(Point(x[i], y[i]))
        return coordinates
