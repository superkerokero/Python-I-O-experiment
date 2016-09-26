# coding: utf-8

""" polygonGen.py:
    This is a module used to generate quadrilateral sample points based on
    input: N points(N>=3) defining a polygon area inside the sampling space."""


class Polygon(object):
    def __init__(self, init_points):
        "Constructor of the class."
        self.points = init_points
        self.npoints = len(self.points)
        self.xmax = max(self.points, key = (lambda x: x[0]))[0]
        self.xmin = min(self.points, key = (lambda x: x[0]))[0]
        self.ymax = max(self.points, key = (lambda x: x[1]))[1]
        self.ymin = min(self.points, key = (lambda x: x[1]))[1]
    @staticmethod
    def _linearEquation(vector):
        """Convert vector to a line of infinite length.
        We want the line in linear equation standard form: a*x + b*y + c = 0
        See: http://en.wikipedia.org/wiki/Linear_equation"""
        a = vector[1][1] - vector[0][1]
        b = vector[0][0] - vector[1][0]
        c = (vector[1][0]*vector[0][1]) - (vector[0][0]*vector[1][1])
        return (a, b, c)
    def _areIntersecting(self, vector1, vector2):
        """Calculates whether two vectors are intersecting each other.
           0: not intersecting
           1: intersecting(once)
           2: collinear(arbitrary intersecting points)"""
        #calculate the line of vector1.
        line1 = self._linearEquation(vector1)
        #insert points of vector2 into line1 and check if vector2 intersects.
        d1 = line1[0]*vector2[0][0] + line1[1]*vector2[0][1] + line1[2]
        d2 = line1[0]*vector2[1][0] + line1[1]*vector2[1][1] + line1[2]
        #if d1 and d2 share the same sign, two vectors don't intersect.
        if d1*d2 > 0:
            return 0
        """The fact that vector 2 intersected the infinite line 1 above doesn't
           mean it also intersects the vector 1. Vector 1 is only a subset of that
           infinite line 1, so it may have intersected that line before the vector
           started or after it ended. To know for sure, we have to repeat the
           the same test the other way round. We start by calculating the 
           infinite line 2 in linear equation standard form."""
        line2 = self._linearEquation(vector2)
        d1 = line2[0]*vector1[0][0] + line2[1]*vector1[0][1] + line2[2]
        d2 = line2[0]*vector1[1][0] + line2[1]*vector1[1][1] + line2[2]
        if d1*d2 > 0:
            return 0
        """If we get here, only two possibilities are left. Either the two
           vectors intersect in exactly one point or they are collinear, which
           means they intersect in any number of points."""
        if line1[0]*line2[1] - line2[0]*line1[1] == 0.0e0:
            return 2
        #If they are not collinear, they must be intersecting once.
        return 1
    def rayCastingInside(self, polygon, point):
        """Calculates how often intersects the ray(defined by the given point
           and an arbitrary point outside the polygon) a polygon side. Then decide
           whether the point is within the polygon."""
        #avoid "vertex on the tip" problem.
        if point in polygon:
            return True
        #set the point that is outside of the polygon.
        bound = (min(polygon, key = (lambda x: x[0]))[0] - 1.e0, point[1])
        #initialize intersections counter.
        edge = (polygon[0], polygon[len(polygon) - 1])
        intersects = self._areIntersecting((bound, point), edge)
        #loop all edges of the polygon and count total intersections.
        for i in range (1, len(polygon)):
            edge = (polygon[i-1], polygon[i])
            intersects += self._areIntersecting((bound, point), edge)
        #check inside/outside by odd/even intersection counts.
        if intersects % 2 == 0:
            return False
        else:
            return True

