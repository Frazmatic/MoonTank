"""Handles playe input

Functions:

keyboard
events
"""
import pygame
import pygame.locals as kbd

def keyboard(player, board) -> bool:
    """keyboard input is continuous, just checks state of pressed keys"""
    keys = pygame.key.get_pressed()
    if keys[kbd.K_w]:
        player.accel_on = True
    if keys[kbd.K_s]:
        player.brake_on = True
    if keys[kbd.K_a]:
        player.rotate(-player.rotation_speed)
    if keys[kbd.K_d]:
        player.rotate(player.rotation_speed)
    if keys[kbd.K_ESCAPE]:
        pygame.quit()
        return False
    return True

def events(player, board, event) -> None:
    """Mouse button input is event based"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            player.turret.shoot(board)
            
