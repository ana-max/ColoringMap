from collections import namedtuple
from visualization.colors import Colors
import random
Segment = namedtuple('Segment', 'begin end')
Vector = namedtuple('Vector', 'x y')


def bubble_sort(array):
    len_array = len(array)
    for i in range(len_array):
        for j in range(len_array - 1, i, -1):
            if array[j].deg > array[j - 1].deg:
                array[j], array[j - 1] \
                    = array[j - 1], array[j]


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.colors = Colors().get_colors()

    def _build_edges(self):
        for i in range(len(self.vertices)-1):
            for j in range(i+1, len(self.vertices)):
                if self.vertices[i].is_contiguous_vertex(self.vertices[j]):
                    self.vertices[i].deg += 1
                    self.vertices[j].deg += 1

    def get_color(self):
        number = random.randrange(0, len(self.colors))
        return self.colors[number]

    def _change_count_of_painting(self,
                                  used_colors,
                                  colors, count_of_painting):
        if len(used_colors) != 0:
            color = used_colors[0]
            used_colors.remove(color)
            for vertex in self.vertices:
                count_of_not_incident = 0
                if not vertex.is_painting:
                    for coloring_vertex in colors[color]:
                        one_condition = vertex\
                                .is_contiguous_vertex(coloring_vertex)
                        two_condition = coloring_vertex\
                            .is_contiguous_vertex(vertex)
                        if not one_condition and not two_condition:
                            count_of_not_incident += 1
                if count_of_not_incident == len(colors[color]):
                    colors[color].append(vertex)
                    vertex.is_painting = True
                    vertex.color = color
                    count_of_painting += 1
                    break
        else:
            color = self.get_color()
            colors[color] = list()
            for vertex in self.vertices:
                if not vertex.is_painting:
                    colors[color].append(vertex)
                    vertex.color = color
                    vertex.is_painting = True
                    count_of_painting += 1
                    break
        return count_of_painting, color

    def coloringGraph(self):
        colors = dict()
        self._build_edges()
        bubble_sort(self.vertices)
        expected_coloring_vertex = len(self.vertices)
        count_of_painting = 0
        used_colors = list()
        for vertex in self.vertices:
            if vertex.color is not None:
                c = vertex.color.replace('color=', '')
                colors[c] = list()
                colors[c].append(vertex)
                if c in self.colors:
                    self.colors.remove(c)
                vertex.is_painting = True
                count_of_painting += 1
                used_colors.append(c)
        count_of_painting, color = self\
            ._change_count_of_painting(used_colors,
                                       colors,
                                       count_of_painting)
        while count_of_painting != expected_coloring_vertex:
            for vertex in self.vertices:
                if vertex.is_painting:
                    continue
                count_of_not_incident = 0
                for coloring_vertex in colors[color]:
                    if not vertex.is_contiguous_vertex(coloring_vertex) and\
                            not coloring_vertex.is_contiguous_vertex(vertex):
                        count_of_not_incident += 1
                if count_of_not_incident == len(colors[color]):
                    colors[color].append(vertex)
                    vertex.color = color
                    vertex.is_painting = True
                    count_of_painting += 1
            if color in self.colors:
                self.colors.remove(color)
            count_of_painting, color = self\
                ._change_count_of_painting(used_colors,
                                           colors, count_of_painting)
        return self.clean_colors(colors)

    def clean_colors(self, colors):
        new_colors = dict()
        for color in colors:
            if len(colors[color]) != 0:
                new_colors[color] = colors[color]
        return new_colors, len(new_colors.keys())

    def add_vertex(self, vertex):
        self.vertices.append(vertex)


class CountryVertex:
    def __init__(self, regions, color=None):
        self.regions = regions
        self.deg = 0
        self.is_painting = False
        self.color = color.replace('color=', '') if color is not None else None

    def add_region(self, region):
        self.regions.update({len(self.regions): region})

    def is_contiguous_vertex(self, vertex):
        for region1 in self.regions:
            for region2 in vertex.regions:
                if self.regions[region1]\
                        .is_intersection(vertex.regions[region2]):
                    return True
