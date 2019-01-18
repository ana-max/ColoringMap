import unittest
from graph.polygon import Polygon
from parser_countries import Parser
from parser_countries import Point


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser

    def test_give_three_points_of_regions(self):
        parser = self.parser('{[(0,0)]}')
        with self.assertRaises(ValueError):
            parser.get_tree()

    def test_get_three(self):
        parser = self.parser('{[(0,0),(0,2),(0,10)],'
                             '[(1,1),(0,3),(5,5)]},'
                             '{[(1,5),(2,3),(6,5)]}')
        result = [{0: Polygon([Point(x=0, y=0),
                               Point(x=0, y=2),
                               Point(x=0, y=10)]),
                   1: Polygon([Point(x=1, y=1),
                               Point(x=0, y=3),
                               Point(x=5, y=5)])},
                  {0: Polygon([Point(x=1, y=5),
                               Point(x=2, y=3),
                               Point(x=6, y=5)])}]
        tree = parser.get_tree()
        self.assertEqual(tree[0][0].points, result[0][0].points)
        self.assertEqual(tree[0][1].points, result[0][1].points)
        self.assertEqual(tree[1][0].points, result[1][0].points)


if __name__ == '__main__':
    unittest.main()
