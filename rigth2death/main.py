import pygame
from pygame.constants import KEYDOWN, K_ESCAPE, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE
from pygame.surface import Surface

import Constants
from items.Weapon import Bullet
from rigth2death.characters import Player
from rigth2death.utils import Utils
from scenarios.Stages import TiledMap, Camera
from utils.CustomSprite import CustomSprite


def run():
    allowed_moves = [K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE]

    pygame.init()
    screen: Surface = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT))
    running = True
    clock: pygame.time.Clock = pygame.time.Clock()
    zombie = CustomSprite(Utils.img('zombies.png'), 5, is_vertical=False)
    player = Player.Player()
    stage = TiledMap(Constants.MAPS + "mapa_z.tmx")

    camera = Camera(stage.width, stage.height)
    image_map = stage.make_map()
    stage_rect = image_map.get_rect()
    moves = []
    bullets = []
    print("blockers {}".format(stage.blockers))

    while running:
        fps = clock.tick(60) / 1000
        screen.fill(pygame.Color('black'))

        # screen.blit(image_map, (0 - asd, 0 - ysd))

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
            if event.type == KEYDOWN:
                # If the Esc key has been pressed set running to false to exit the main loop
                if event.key == K_ESCAPE:
                    running = False
                if event.key in allowed_moves:
                    moves.append(event.key)
            if event.type == KEYUP:
                if event.key in moves:
                    moves.remove(event.key)
            # Check for QUIT event; if QUIT, set running to false
            elif event.type == pygame.QUIT:
                running = False
        if len(moves) > 0:
            a = moves.pop()
            possible_bullet = player.move(a)
            if isinstance(possible_bullet, Bullet):
                bullets.append(possible_bullet)
            moves.append(a)

        # Draw the player to the screen
        # Update the display
        camera.update(player.current_sprite)
        screen.blit(image_map, camera.apply_rect(stage_rect))
        screen.blit(player.current_sprite.image, camera.apply(player.current_sprite))
        screen.blit(zombie.image, camera.apply(zombie))

        for bullet in bullets:
            if bullet.exist():
                bullet.move(fps)
                screen.blit(bullet.sprite.image, camera.apply(bullet.sprite))
            else:
                bullets.remove(bullet)

        zombie.play()
        pygame.display.flip()


if __name__ == '__main__':
    run()
