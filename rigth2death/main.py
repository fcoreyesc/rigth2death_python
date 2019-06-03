import pygame
from pygame.constants import KEYDOWN, K_ESCAPE, KEYUP
from pygame.surface import Surface

import Constants
from rigth2death.characters import Player
from rigth2death.utils import Utils
from scenarios.Stages import TiledMap, Camera


def run():
    pygame.init()
    screen: Surface = pygame.display.set_mode((800, 600))
    running = True
    clock: pygame.time.Clock = pygame.time.Clock()
    zombie = Player.CustomSprite(Utils.img('zombies.png'), clock, 5, is_vertical=False)
    player = Player.Player(clock)
    stage = TiledMap(Constants.MAPS + "mapa_z.tmx")

    camara = Camera(stage.width, stage.height)
    image_map = stage.make_map()
    stage_rect = image_map.get_rect()
    moves = []
    print("blockers {}".format(stage.blockers))
    asd = 0
    ysd = 0
    while running:
        clock.tick(60)
        screen.fill(pygame.Color('black'))

        # screen.blit(image_map, (0 - asd, 0 - ysd))

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
            if event.type == KEYDOWN:
                # If the Esc key has been pressed set running to false to exit the main loop
                if event.key == K_ESCAPE:
                    running = False
                moves.append(event.key)
            if event.type == KEYUP:
                if event.key in moves:
                    moves.remove(event.key)
            # Check for QUIT event; if QUIT, set running to false
            elif event.type == pygame.QUIT:
                running = False
        if len(moves) > 0:
            a = moves.pop()
            player.move(a)
            moves.append(a)

        # Draw the player to the screen
        # Update the display
        camara.update(player.current_sprite)
        screen.blit(image_map, camara.apply_rect(stage_rect))
        screen.blit(player.current_sprite.image, camara.apply(player.current_sprite))
        screen.blit(zombie.image, camara.apply(zombie))

        zombie.play()
        pygame.display.flip()


if __name__ == '__main__':
    run()
