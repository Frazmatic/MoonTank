#existing libraries/modules
import pygame
import json

#I wrote these:
from board import Board
import game_pieces
import display
import controls

clock = pygame.time.Clock()


def main():
    with open("Stats/terrain_defaults.json", mode = "r") as f:
        terrain_stats_dict = json.loads(f.read())

    pygame.init()
    screen = display.initialize()
    #section of board (game map) that is visible on screen:
    view_height = 500 #larger = zoomed 'out', smaller = zoomed 'in'

    start_location = (10000, 10000)
    primary_board = Board(start_location[0] * 2, start_location[1] * 2, terrain_stats_dict)
    player = game_pieces.BasicVehicle(start_location)
    primary_board.add_piece(player)
    enemy = game_pieces.EnemyTurret((10100,10000))
    primary_board.add_piece(enemy)
    
    running = True
    while running:
        clock.tick(60)
        controls.keyboard(player, primary_board)
        primary_board.update()
        display.show_board(player, view_height, primary_board, screen)

        for event in pygame.event.get():
            controls.events(player, primary_board, event)
            if event.type == pygame.QUIT:
                running = False
if __name__ == "__main__":
    main()
