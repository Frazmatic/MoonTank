from spatial_hash import SpatialHash
import bin_search_add
from tile import Tile
import coord_math

class Board():
    def __init__(self, w, h, tiles_dict):
        #for processing updates
        self.pieces_l = []
        #for collision detection, display, etc
        self.pieces_sh = SpatialHash(100)
        self.tiles_sh = SpatialHash(100)
        self.tiles_stats = tiles_dict
        self.w = w
        self.h = h
        for x in range(0, w, 100):
            for y in range(0, h, 100):
                self.tiles_sh.add_tile(Tile((x, y), tiles_dict))

    def add_tile(self, tile):
        #reminder: one tile per key in this hash-map
        #note: this means the json method can just use the list of keys
        self.tiles_sh.add_tile(tile)

    def add_piece(self, piece):
        #keeps pieces list sorted which may be useful in future
        bin_search_add.bin_insert(self.pieces_l, piece, lambda p: p.get_coordinates())
        self.pieces_sh.add_piece(piece)

    def remove_piece(self, piece):
        self.pieces_l.remove(piece)
        self.pieces_sh.remove_piece(piece)

    #may not need this since add_pice() keeps it sorted, by just in case:
    def sort_pieces(self):
        self.pieces_l = sorted(self.pieces_l, key = lambda p: p.get_coordinates())

    #by only getting relevant buckets, we reduce runtime from all items to just
    #items on or near screen
    def get_sub_section_lists(self, center_coord, width, height):
        """
        Returns tuple (tiles_list, pieces_list). Each entry in a list is (screen_coordinate, the_object)
        Used to get screen output for a section of the game board.
        """

        #define rectangular area around center coordinates
        low_x, low_y = center_coord[0] - (width //2), center_coord[1] - (height // 2)
        top_x, top_y = low_x + width, low_y + height

        #list of coordinates for spatial-hash keys
        coordinates_list = []
        #100 is bucket diameter, this ensures all relevant buckets obtained
        for x in range(int(low_x - 100), int(top_x + 100), 100):
            for y in range(int(low_y - 100), int(top_y + 100), 100):
                coordinates_list.append((x, y))

        #each bucket has a set. union for all the sets
        tiles_set = set()
        pieces_set = set()
        for c in coordinates_list:
            tiles_set = tiles_set.union(self.tiles_sh.get_set_for_coordinates(c))
            pieces_set = pieces_set.union(self.pieces_sh.get_set_for_coordinates(c))
        
        #added adjsuted coordinates for each item, relative to subsection
        #append to output lists
        tiles_output = []
        pieces_output = []
        for tile in tiles_set:
            # (low_x, low_y) are (0, 0) for this subsection
            new_c = (tile.get_x() - low_x, tile.get_y() - low_y)
            tiles_output.append((new_c, tile))
        for piece in pieces_set:
            new_c = (piece.get_x() - low_x, piece.get_y() - low_y)
            pieces_output.append((new_c, piece))
            if "components" in piece.stats:
                for comp in piece.get_components():
                    new_c = (comp.get_x() - low_x, comp.get_y() - low_y)
                    pieces_output.append((new_c, comp))

        return (tiles_output, pieces_output)

    def get_pieces_in_range(self, center_coord, distance):
        #define rectangular area around center coordinates
        low_x, low_y = center_coord[0] - (distance //2), center_coord[1] - (distance // 2)
        top_x, top_y = low_x + distance, low_y + distance
        #list of coordinates for spatial-hash keys
        coordinates_list = []
        #100 is bucket diameter, this ensures all relevant buckets obtained
        for x in range(int(low_x), int(top_x + 1), 100):
            for y in range(int(low_y), int(top_y + 1), 100):
                coordinates_list.append((x, y))
        pieces_set = set()
        for c in coordinates_list:
            pieces_set = pieces_set.union(self.pieces_sh.get_set_for_coordinates(c))
        pieces_list = list(pieces_set)
        #return list sorted by distance to center
        pieces_list = sorted(pieces_list, key = lambda piece: coord_math.get_distance(center_coord, piece.get_coordinates()))
        return pieces_list
        
    def update(self):
        remove_list = []
        for p in self.pieces_l:
            if p.stats["health"] <= 0:
                remove_list.append(p)
                continue
            p.update(self)
        for p in remove_list:
            self.remove_piece(p)
            
def main():
    #testing goes here:
    import json
    with open("Stats/terrain_defaults.json", mode = 'r') as f:
        terrain_stats = json.loads(f.read())


    b = Board(10000, 10000, terrain_stats)
    #print(b.tiles_sh.buckets)

    import game_pieces
    p = game_pieces.BasicVehicle((5000,5000))
    b.add_piece(p)
    s = b.pieces_sh.get_set_for_piece(p)
    assert len(s) == 1
    l = b.pieces_sh.bucket_list(p)
    assert len(l) == 4
    assert len(b.pieces_sh.buckets) >= len(l)
    
    display_list = b.get_sub_section_lists(p.get_coordinates(), 2000, 1000)
    print(len(display_list[0]))    
    
if __name__ == "__main__":
    main()

    
        
        
        
        
