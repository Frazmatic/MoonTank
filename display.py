import pygame
import json

#I wrote this:
import game_pieces

class Display:

    #class variables holding image objects for rendering:
    with open("Stats/terrain_defaults.json", mode = "r") as f:
        tile_stats_dict = json.loads(f.read())
    with open("Stats/piece_defaults.json", mode = "r") as f:
        piece_stats_dict = json.loads(f.read())

    #combined dict associating names with image objects:
    image_dict = {}
    for stats in tile_stats_dict.values():
        filename = stats["image"]
        image = pygame.image.load(filename)
        image_dict[filename] = image
    for stats in piece_stats_dict.values():
        filename = stats["image"]
        image = pygame.image.load(filename)
        image_dict[filename] = image

    def __init__(self, player, view_height, board):
        info = pygame.display.Info()
        self.res = (info.current_w, info.current_h)
        self.screen = pygame.display.set_mode(self.res, flags = pygame.FULLSCREEN)
        self.player = player
        self.view_height = view_height
        self.board = board

        self.w, self.h = pygame.display.get_surface().get_size()
        self.wh_ratio = float(self.w) / self.h
        self.view_width = int(self.wh_ratio * self.view_height)
        #used to scale up images; view width/height is relative to screen width/height
        self.x_scale_ratio, self.y_scale_ratio = float(self.w) / self.view_width, float(self.h) / self.view_height 
        pygame.display.set_caption("MoonTank")

    def show_board(self):
        
        #tiles & pieces are both lists of lists. list[0] are coordinates, list[1] are the objects
        tiles, pieces = self.board.get_sub_section_lists(self.player.coordinates, self.view_width, self.view_height)

        self.screen.fill((0,0,0))
        for t in tiles:
            x, y = t[0]
            tile = t[1]
            image = Display.image_dict[tile.image]
            
            #screen y coordinate starts at top instead of bottom
            y = self.view_height - y - 100

            x *= self.x_scale_ratio
            y *= self.y_scale_ratio

            #scale up image size
            image_width, image_height = int(image.get_width() * self.x_scale_ratio), int(image.get_height() * self.y_scale_ratio)
            image = pygame.transform.scale(image, (image_width, image_height))

            self.screen.blit(image, (x, y))

        for p in pieces:
            x, y = p[0]
            piece = p[1]

            image = Display.image_dict[piece.image]

            y = self.view_height - y

            x *= self.x_scale_ratio
            y *= self.y_scale_ratio

            image_width, image_height = int(image.get_width() * self.x_scale_ratio), int(image.get_height() * self.y_scale_ratio)
            image = pygame.transform.scale(image, (image_width, image_height))

            image = pygame.transform.rotate(image, 360 - piece.angle)

            x -= image.get_width() // 2
            y -= image.get_height() // 2

            piece.screen_coordinates = (x, y)

            image.set_alpha(None)
            image.set_colorkey((255,255,255))

            self.screen.blit(image, (x, y))

        pygame.display.flip()

        
        
        
        
        
        
        
    
