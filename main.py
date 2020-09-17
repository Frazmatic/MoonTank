#existing libraries/modules
import pygame
import json

#I wrote these:
from board import Board
import game_pieces
from display import Display
import controls

clock = pygame.time.Clock()
#section of board (game map) that is visible on screen:
view_height = 1000 #larger = zoomed 'out', smaller = zoomed 'in'

def main():
    pygame.init()
      
    start_location = (10000, 10000)
    primary_board = Board(start_location[0] * 2, start_location[1] * 2)

    player = game_pieces.Vehicle(start_location, "BasicVehicle")
    primary_board.add_piece(player)

    enemy = game_pieces.EnemyTurret((10100,10000))
    primary_board.add_piece(enemy)

    screen = Display(player, view_height, primary_board)
    
    running = True
    while running:
        clock.tick(60)

        controls.keyboard(player, primary_board)
        primary_board.update()
        screen.show_board()

        for event in pygame.event.get():
            controls.events(player, primary_board, event)
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()
