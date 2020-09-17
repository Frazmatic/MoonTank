import random
import json

class Tile:

    #per Python ref, "__slots__ allow us to explicitly declare data members (like properties)
    #and deny the creation of __dict__ and __weakref__". Useful for contexts like this in which
    #I may have millions of instances with a few attributes each; saves memory.
    __slots__ = ['category', 'image', 'cover_value', 'drag', 'coordinates']
    with open("Stats/terrain_defaults.json", mode = "r") as f:
        stats_dict = json.loads(f.read())

    #stats dict is loaded from a json file so that stats can be stored elsewhere
    def __init__(self, coordinate, category = None):
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

        self.image = Tile.stats_dict[self.category]["image"]
        self.cover_value = Tile.stats_dict[self.category]["cover_value"]
        self.drag = Tile.stats_dict[self.category]["drag"]
        self.coordinates = coordinate

    @property
    def x(self):
        return self.coordinates[0]

    @property
    def y(self):
        return self.coordinates[1]

    def __str__(self):
        return "coordinates: {} \tcategory: {}".format(self.stats["coordinates"], self.category)

def main():
    #testing:
    pass
if __name__ == "__main__":
    main()

    
