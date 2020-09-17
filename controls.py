import pygame
import pygame.locals as kbd

#eventually should replace this with player defined variables for custom controls
def keyboard(player, board):
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

def events(player, board, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            player.turret.shoot(board)
            
