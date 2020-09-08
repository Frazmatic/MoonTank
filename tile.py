import random

class Tile():
    #stats dict is loaded from a json file so that stats can be stored elsewhere
    def __init__(self, coordinate, stats_dict, category = None):
        if category != None:
            self.category = category
        else:
            n = random.random()
            if n < 0.8:
                self.category = "flat"
            elif n < 0.9:
                self.category = "crater"
            elif n < 0.95:
                self.category = "rock"
            else:
                self.category = "road"
        self.stats = stats_dict[self.category].copy()
        #coordinate represents bottom left of tile, tuple (x, y)
        self.stats["coordinates"] = coordinate

    def get_category(self):
        return self.category
    
    def get_coordinates(self):
        return self.stats["coordinates"]

    def get_x(self):
        return self.get_coordinates()[0]

    def get_y(self):
        return self.get_coordinates()[1]

    def get_cover_value(self):
        return self.stats["cover_value"]

    def get_movement_speed_modifier(self):
        return self.stats["movement speed"]

    def __str__(self):
        return "coordinates: {} \tcategory: {}".format(self.stats["coordinates"], self.category)

def main():
    #testing:
    import json
    with open("Stats/terrain_defaults.json", mode = "r") as f:
        terrains = json.loads(f.read())
    t = Tile((0,0),terrains, "flat")
    t_list = [Tile((i,0),terrains) for i in range(50)]
    for tile in t_list:
        print(tile)
if __name__ == "__main__":
    main()

    
