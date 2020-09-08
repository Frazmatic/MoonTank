import pygame
import game_pieces
import coord_math

def initialize():
    info = pygame.display.Info()
    res = (info.current_w, info.current_h)
    screen = pygame.display.set_mode((1000,1000))
    #, flags = pygame.FULLSCREEN
    pygame.display.set_caption("MoonTank")
    return screen

def show_board(player, view_height, board, screen):
    w, h = pygame.display.get_surface().get_size()
    wh_ratio = float(w) / h
    view_width = int(wh_ratio * view_height)
    #used to scale up images; view width/height relative to screen width/height
    x_scale_ratio, y_scale_ratio = float(w) / view_width, float(h) / view_height 
    tiles, pieces = board.get_sub_section_lists(player.get_coordinates(), view_width, view_height)

    screen.fill((0,0,0))
    for t in tiles:
        x, y = t[0]
        tile = t[1]
        image = pygame.image.load(tile.stats["image"])
        
        #drawing y coordinate starts at top instead of bottom
        y = view_height - y - 100

        x *= x_scale_ratio
        y *= y_scale_ratio

        #scale up image size
        image_width, image_height = int(image.get_width() * x_scale_ratio), int(image.get_height() * y_scale_ratio)
        image = pygame.transform.scale(image, (image_width, image_height))

        screen.blit(image, (x, y))

    for p in pieces:
        x, y = p[0]
        piece = p[1]
        
        image = pygame.image.load(piece.stats["image"])

        y = view_height - y

        x *= x_scale_ratio
        y *= y_scale_ratio

        image_width, image_height = int(image.get_width() * x_scale_ratio), int(image.get_height() * y_scale_ratio)
        image = pygame.transform.scale(image, (image_width, image_height))

        image = pygame.transform.rotate(image, 360 - piece.stats["angle"])

        x -= image.get_width() // 2
        y -= image.get_height() // 2

        piece.stats["screen coordinates"] = (x, y)

        image.set_alpha(None)
        image.set_colorkey((255,255,255))

        screen.blit(image, (x, y))


    pygame.display.flip()

        
        
        
        
        
        
        
    
