import math
def get_distance(coord_a, coord_b):
    x, y = coord_a
    x2, y2 = coord_b
    x_diff = x2 - x
    y_diff = y2 - y
    return (x_diff ** 2 + y_diff **2) ** 0.5

def get_relative_angle(coord_a, coord_b):
    x, y = coord_a
    x2, y2 = coord_b
    x_diff = x2 - x
    y_diff = y2 - y
    return -1 * math.degrees(math.atan2(y_diff, x_diff)) + 90

def translate(coord_a, angle, distance):
    x, y = coord_a
    x_delta = math.sin(math.radians(angle)) * distance
    y_delta = math.cos(math.radians(angle)) * distance
    x += x_delta
    y += y_delta
    return (x, y)
