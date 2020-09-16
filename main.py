#existing libraries/modules
import pygame
import json

#I wrote these:
from board import Board
import game_pieces
import display
import controls

clock = pygame.time.Clock()
#section of board (game map) that is visible on screen:
view_height = 1000 #larger = zoomed 'out', smaller = zoomed 'in'

def main():
    with open("Stats/terrain_defaults.json", mode = "r") as f:
        tile_stats_dict = json.loads(f.read())

    image_dict = {}
    for tile in tile_stats_dict:
        filename = tile_stats_dict[tile]["image"]
        image = pygame.image.load(filename)
        image_dict[filename] = image

    pygame.init()
    screen = display.initialize()
             
    start_location = (10000, 10000)
    primary_board = Board(start_location[0] * 2, start_location[1] * 2, tile_stats_dict)

    player = game_pieces.BasicVehicle(start_location)
    primary_board.add_piece(player)

    enemy = game_pieces.EnemyTurret((10100,10000))
    primary_board.add_piece(enemy)
    
    running = True
    while running:
        clock.tick(60)
        controls.keyboard(player, primary_board)
        primary_board.update()
        display.show_board(player, view_height, primary_board, screen, image_dict)

        for event in pygame.event.get():
            controls.events(player, primary_board, event)
            if event.type == pygame.QUIT:
                running = False
if __name__ == "__main__":
    main()
