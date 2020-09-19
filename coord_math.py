"""Helper module for coordinate based math

Classes:
Coordinates
"""
import math

class Coordinates:

    @staticmethod
    def get_distance(coord_a: tuple, coord_b: tuple) -> float:
        """takes two coordinates as tuples of integers. Returns distance between them."""
        x, y = coord_a
        x2, y2 = coord_b
        x_diff = x2 - x
        y_diff = y2 - y
        return (x_diff ** 2 + y_diff **2) ** 0.5

    @staticmethod
    def get_relative_angle(coord_a: tuple, coord_b: tuple) -> float:
        """Returns the angle from point a to point b."""
        x, y = coord_a
        x2, y2 = coord_b
        x_diff = x2 - x
        y_diff = y2 - y
        return -1 * math.degrees(math.atan2(y_diff, x_diff)) + 90

    @staticmethod
    def translate(coord_a: tuple, angle: float, distance: float) -> tuple:
        """Finds new position given origin coordinate, angle, and distance."""
        x, y = coord_a
        x_delta = math.sin(math.radians(angle)) * distance
        y_delta = math.cos(math.radians(angle)) * distance
        x += x_delta
        y += y_delta
        return (x, y)
