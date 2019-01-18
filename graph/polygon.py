from collections import namedtuple
Segment = namedtuple('Segment', 'begin end')
Vector = namedtuple('Vector', 'x y')


class Polygon:
    def __init__(self, points):
        self.points = points

    @property
    def segments(self):
        return self._get_segments()

    def is_intersection(self, other):
        return self._is_have_common_side(other) or \
               self._is_have_common_area(other) or \
               self._is_have_common_point(other)

    def point_in_polygon(self, point):
        flag = False
        points = self.points
        count_of_points = len(points)
        for i in range(count_of_points):
            flag = False
            i1 = i + 1 if i < count_of_points - 1 else 0
            while not flag:
                i2 = i1 + 1
                if i2 >= count_of_points:
                    i2 = 0
                if i2 == i + 1 if i < count_of_points - 1 else 0:
                    break
                sup_one = points[i1].x * (points[i2].y - points[i].y)
                sup_two = points[i2].x * (points[i].y - points[i1].y)
                sup_three = points[i].x * (points[i1].y - points[i2].y)
                S = abs(sup_one + sup_two + sup_three)
                sup_one = points[i1].x * (points[i2].y - point.y)
                sup_two = points[i2].x * (point.y - points[i1].y)
                sup_three = point.x * (points[i1].y - points[i2].y)
                S1 = abs(sup_one + sup_two + sup_three)
                sup_one = points[i].x * (points[i2].y - point.y)
                sup_two = points[i2].x * (point.y - points[i].y)
                sup_three = point.x * (points[i].y - points[i2].y)
                S2 = abs(sup_one + sup_two + sup_three)
                sup_one = points[i1].x * (points[i].y - point.y)
                sup_two = points[i].x * (point.y - points[i1].y)
                sup_three = point.x * (points[i1].y - points[i].y)
                S3 = abs(sup_one + sup_two + sup_three)
                if (S == S1 + S2 + S3):
                    flag = True
                    break
                i1 = i1 + 1
                if (i1 >= count_of_points):
                    i1 = 0
            if not flag:
                break
        return flag

    def _is_have_common_point(self, other):
        for point in other.points:
            if self.point_in_polygon(point):
                return True
        return False

    def _is_have_common_side(self, other):
        segments1 = self.segments
        segments2 = other.segments
        for s1 in segments1:
            for s2 in segments2:
                one_situation = \
                    self._point_is_on_the_segment(s1.begin, s2) and \
                    self._point_is_on_the_segment(s1.end, s2)
                two_situation = \
                    self._point_is_on_the_segment(s1.begin, s2) and \
                    self._point_is_on_the_segment(s2.end, s1)
                three_situation = \
                    self._point_is_on_the_segment(s2.begin, s1) and \
                    self._point_is_on_the_segment(s1.end, s2)
                four_situation = \
                    self._point_is_on_the_segment(s2.begin, s1) and \
                    self._point_is_on_the_segment(s2.end, s1)

                if one_situation or two_situation or \
                        three_situation or four_situation:
                    return True

    def _is_have_common_area(self, vertex):
        segments1 = self.segments
        segments2 = vertex.segments
        for s1 in segments1:
            for s2 in segments2:
                if self._is_interstection_segments(s1, s2) and\
                        self._is_interstection_segments(s2, s1):
                    return True

    def _is_interstection_segments(self, s1, s2):
        one = -(s2.end.x-s2.begin.x)*(s1.begin.y-s2.begin.y)
        two = (s2.end.y-s2.begin.y)*(s1.begin.x-s2.begin.x)
        one_side_of_point = one + two
        one = -(s2.end.x-s2.begin.x)*(s1.end.y-s2.begin.y)
        two = (s2.end.y-s2.begin.y)*(s1.end.x-s2.begin.x)
        two_side_of_point = one + two
        return (one_side_of_point > 0 and two_side_of_point < 0) or\
               (one_side_of_point < 0 and two_side_of_point > 0)

    def _get_segments(self):
        segments = list()
        if len(self.points) == 0:
            return []
        for i in range(len(self.points)-1):
            segments.append(Segment(self.points[i], self.points[i+1]))
        segments.append(Segment(self.points[-1], self.points[0]))
        return segments

    def _is_collinear_vectors(self, vector1, vector2):
        return vector2.x*vector1.y - vector2.y*vector1.x == 0

    def _point_is_on_the_segment(self, point, segment):
        vector_segment = Vector(segment.end.x - segment.begin.x,
                                segment.end.y - segment.begin.y)
        p1p = Vector(point.x - segment.begin.x, point.y - segment.begin.y)
        is_less = segment.begin.x <= point.x <= segment.end.x
        is_bigger = segment.begin.x >= point.x >= segment.end.x
        on_line = is_less or is_bigger
        return self._is_collinear_vectors(vector_segment, p1p) and on_line
