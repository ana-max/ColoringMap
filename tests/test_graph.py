import unittest
from graph.graph import CountryVertex, Graph, bubble_sort
from parser_countries import Parser
from graph.graph_generator import Generator


class GraphTest(unittest.TestCase):
    def setUp(self):
        country1 = '{[(5,3),(7,3),(5,5)],[(5,5),(7,7),(9,5),(7,3)]}' \
                   ',{[(1,1),(4,1),(4,3),(1,3)],[(2,3),(2,5),(5,5)' \
                   ',(5,3)],[(4,0),(7,0),(7,3),(4,3)]},{[(9,5),' \
                   '(11,7),(9,9),(7,7)]},{[(8,4),(8,0),(7,0)]},' \
                   '{[(4, 8),(4,5),(7,7),(6,9)]},' \
                   '{[(9, 7),(12,9),(14,6),(11,5)]}'
        country2 = '{[(3,1),(9,2),(3,-6),(3,-5),(1,-5),(1,-2)],' \
                   '[(7,4),(7,6),(9,6),(9,4)]},' \
                   '{[(1,-2),(3,1),(2,3),(-6,0),(-5,-2),(-3,-4)]},' \
                   '{[(1,-2),(-3,-4),(-5,-7),(-3,-10),' \
                   '(3,-6),(3,-5),(1,-5),(1,-2)]},' \
                   '{[(-3,-10),(-8,-12),(-7,-17),(-2,-14)]},' \
                   '{[(12,-5),(14,-9),(11,-12),(8,-8)]},' \
                   '{[(11,-12),(8,-8),(4,-12),(6,-16)]}'
        three1 = Parser(country1).get_tree()
        three2 = Parser(country2).get_tree()
        self.vertices1 = list()
        for country in three1:
            self.vertices1.append(CountryVertex(country))
        self.graph1 = Graph(self.vertices1)
        self.vertices2 = list()
        for country in three2:
            self.vertices2.append(CountryVertex(country))
        self.graph2 = Graph(self.vertices2)

    def test_incident_country(self):
        self.assertTrue(self.vertices1[0]
                        .is_contiguous_vertex(self.vertices1[1]))
        self.assertTrue(self.vertices1[1]
                        .is_contiguous_vertex(self.vertices1[0]))
        self.assertTrue(self.vertices1[0]
                        .is_contiguous_vertex(self.vertices1[2]))

        self.assertTrue(self.vertices2[0]
                        .is_contiguous_vertex(self.vertices2[1]))
        self.assertTrue(self.vertices2[0]
                        .is_contiguous_vertex(self.vertices2[2]))
        self.assertFalse(self.vertices2[0]
                         .is_contiguous_vertex(self.vertices2[3]))
        self.assertFalse(self.vertices2[0]
                         .is_contiguous_vertex(self.vertices2[4]))
        self.assertFalse(self.vertices2[0]
                         .is_contiguous_vertex(self.vertices2[5]))
        self.assertTrue(self.vertices2[1]
                        .is_contiguous_vertex(self.vertices2[2]))

    def test_deg_vertices(self):
        self.graph1._build_edges()
        self.assertEqual(self.graph1.vertices[0].deg, 4)
        self.assertEqual(self.graph1.vertices[1].deg, 3)
        self.assertEqual(self.graph1.vertices[2].deg, 3)

        self.graph2._build_edges()
        self.assertEqual(self.graph2.vertices[0].deg, 2)
        self.assertEqual(self.graph2.vertices[1].deg, 2)
        self.assertEqual(self.graph2.vertices[2].deg, 3)
        self.assertEqual(self.graph2.vertices[3].deg, 1)
        self.assertEqual(self.graph2.vertices[4].deg, 1)
        self.assertEqual(self.graph2.vertices[5].deg, 1)

    def test_bubble_sort_vertices(self):
        self.graph1._build_edges()
        bubble_sort(self.graph1.vertices)
        self.assertEqual(self.graph1.vertices[0].deg, 4)
        self.assertEqual(self.graph1.vertices[1].deg, 3)
        self.assertEqual(self.graph1.vertices[2].deg, 3)

        self.graph2._build_edges()
        bubble_sort(self.graph2.vertices)
        self.assertEqual(self.graph2.vertices[0].deg, 3)
        self.assertEqual(self.graph2.vertices[1].deg, 2)

        self.assertEqual(self.graph2.vertices[2].deg, 2)
        self.assertEqual(self.graph2.vertices[3].deg, 1)
        self.assertEqual(self.graph2.vertices[4].deg, 1)
        self.assertEqual(self.graph2.vertices[5].deg, 1)

    def test_coloring(self):
        self.assertEqual(self.graph1.coloringGraph()[1], 3)
        self.assertEqual(self.graph2.coloringGraph()[1], 3)

    def test_good_colors(self):
        drawing1 = self.graph1.coloringGraph()
        count1 = 0
        for color in drawing1[0]:
            count1 += len(drawing1[0][color])
        self.assertTrue(count1 == 6)

        drawing2 = self.graph2.coloringGraph()
        count2 = 0
        for color in drawing2[0]:
            count2 += len(drawing2[0][color])
        self.assertEqual(count2, 6)

    def test_good_generate(self):
        self.assertEqual(Generator(5)
                         .generate_map().coloringGraph()[1], 5)


if __name__ == '__main__':
    unittest.main()
