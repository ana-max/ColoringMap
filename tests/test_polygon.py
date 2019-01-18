import unittest
from graph.polygon import Polygon, Segment
from parser_countries import Point


class PolygonTest(unittest.TestCase):
    def setUp(self):
        self.polygon = Polygon([Point(1, 1), Point(-2, -3), Point(-2, -6),
                                Point(1, -8), Point(5, -8), Point(7, -3)])
        self.other = Polygon([Point(1, 1), Point(-21, 20), Point(3, 10)])

    def test_point_not_in_the_polygon(self):
        is_in_polygon = \
            self.polygon.point_in_polygon(Point(-5, 5))
        self.assertFalse(is_in_polygon)

    def test_point_in_the_polygon(self):
        is_in_polygon = \
            self.polygon.point_in_polygon(Point(2, -3))
        self.assertTrue(is_in_polygon)

    def test_is_intersection(self):
        self.assertTrue(self.polygon.is_intersection(self.other))

    def test_is_have_common_point(self):
        self.assertTrue(self.polygon._is_have_common_point(self.other))

    def test_get_segments(self):
        segments = self.other._get_segments()
        true_segments = [Segment(Point(1, 1), Point(-21, 20)),
                         Segment(Point(-21, 20), Point(3, 10)),
                         Segment(Point(3, 10), Point(1, 1))]
        self.assertEqual(segments, true_segments)

    def test_is_have_common_side(self):
        other = Polygon([Point(1, 1), Point(-2, -3), Point(-2, -6)])
        self.assertTrue(self.polygon._is_have_common_side(other))

    def test_is_not_have_common_side(self):
        other = Polygon([Point(100, 100), Point(-201, 200), Point(30, 100)])
        self.assertFalse(self.polygon._is_have_common_side(other))


if __name__ == '__main__':
    unittest.main()
