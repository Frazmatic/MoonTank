'''
A utility file to get the initial JSON values created.
Should no longer need to be used.
'''

import json

def create_terrain_dict():
    terrains = {"crater": {}, "flat": {}, "rock": {}, "road": {}}
    terrains["crater"]["image"] = "Images/Terrain/crater.bmp"
    terrains["flat"]["image"] = "Images/Terrain/flat.bmp"
    terrains["rock"]["image"] = "Images/Terrain/rock.bmp"
    terrains["road"]["image"] = "Images/Terrain/road.bmp"
    terrains["crater"]["cover_value"] = 0.5
    terrains["flat"]["cover_value"] = 0.0
    terrains["rock"]["cover_value"] = 0.9
    terrains["road"]["cover_value"] = 0.0
    terrains["crater"]["movement_speed"] = 0.5
    terrains["flat"]["movement_speed"] = 1.0
    terrains["rock"]["movement_speed"] = 0.25
    terrains["road"]["movement_speed"] = 2.0

    for key in terrains:
        terrains[key]["coordinates"] = (0, 0)

    return terrains

with open('Stats/terrain_defaults.json', mode = 'w') as f:
    json_string = json.dumps(create_terrain_dict(), indent = 4)
    f.write(json_string)

