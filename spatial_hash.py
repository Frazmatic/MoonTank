"""Utilizing a spatial-hash rather than array saves complexity and runtime for display, collicsion detection, etc.

Maps each coordinate to a cell. Two-dimensional objects can cross cell borders and are therefore
added to or removed from multiple cells (buckets).
"""
from math import sin, cos, radians
#faster than using setdefault() with a regular dict; prevents key errors:
from collections import defaultdict

class SpatialHash:
    def __init__(self, bucket_diameter):
        self.bucket_diameter = bucket_diameter
        self.buckets = defaultdict(set)

    def hash(self, coordinate):
        #(x, y)
        return (int(coordinate[0] // self.bucket_diameter), int(coordinate[1] // self.bucket_diameter))

    #tiles work a bit differently. Their coordinates are for bottom left, not center, and they have
    #same width as the buckets. Ideally one tile per bucket; exceptions possible if needed.
    def add_tile(self, tile):
        self.buckets[self.hash(tile.coordinates)].add(tile)

    #2-dimensional rectangular pieces may be overlapping buckets, and may be rotated
    #I could just use the larger of w or h, but thought it would be interesting to do the math
    def bucket_list(self, piece):
        """returns all key values relevant to a piece on the board"""
        x, y = piece.coordinates
        w, h = piece.dimensions
        angle = radians(piece.angle)
        x_term = (abs(sin(angle) * h) + abs(cos(angle) * w))//2
        y_term = (abs(sin(angle) * w) + abs(cos(angle) * h))//2
        x_min = int(x - x_term)
        x_max = int(x + x_term)
        y_min = int(y - y_term)
        y_max = int(y + y_term)
        keys = []
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                k = self.hash((x, y))
                if k not in keys:
                    keys.append(k)
        return keys

    def add_piece(self, piece):
        keys = self.bucket_list(piece)
        for key in keys:
            self.buckets[key].add(piece)

    def remove_piece(self, piece):
        keys = self.bucket_list(piece)
        for key in keys:
            self.buckets[key].remove(piece)

    def get_set_for_piece(self, piece):
        """finds all pieces occupying the same buckets as given piece"""
        keys = self.bucket_list(piece)
        output = set()
        for key in keys:
            output = output.union(self.buckets[key])
        return output

    def get_set_for_coordinates(self, coord):
        """returns pieces for a given coordinate"""
        return self.buckets[self.hash(coord)]

def main():
    """testing goes here"""
    import json
    from tile import Tile
    with open("Stats/terrain_defaults.json", mode = 'r') as f:
        terrain_stats_dict = json.loads(f.read())
        
    tile_sh = SpatialHash(100)
    for x in range(0, 1000, 100):
        for y in range(0, 1000, 100):
            tile_sh.add_tile(Tile((x, y), terrain_stats_dict))

    s = tile_sh.get_set_for_coordinates((500, 500))
    print(s)

    import game_pieces
    p = game_pieces.BasicVehicle((500,500))
    pieces_sh = SpatialHash(100)
    b = pieces_sh.bucket_list(p)
    pieces_sh.add_piece(p)
    
if __name__ == "__main__":
    main()
