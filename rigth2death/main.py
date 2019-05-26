import pygame
from pygame import Color
from pygame.constants import KEYDOWN, K_ESCAPE, QUIT, K_RIGHT
from pygame.surface import Surface

from rigth2death.characters import Player
from rigth2death.utils import Utils


def run():
    pygame.init()
    screen: Surface = pygame.display.set_mode((800, 600))
    running = True
    clock: pygame.time.Clock = pygame.time.Clock()
    personaje2 = Player.NewSprite(Utils.img('zombies.png'), clock, 5, is_vertical=False)
    personaje = Player.NewSprite(Utils.img_player('derecha.png'), clock, 7)

    while running:
        clock.tick(60)
        screen.fill(Color('black'))

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
            if event.type == KEYDOWN:
                # If the Esc key has been pressed set running to false to exit the main loop
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_RIGHT:
                    personaje.move(personaje.rect.x + personaje.speed, personaje.rect.y)

            # Check for QUIT event; if QUIT, set running to false
            elif event.type == QUIT:
                running = False

        # Draw the player to the screen
        # Update the display

        screen.blit(personaje.image, personaje.rect)
        screen.blit(personaje2.image, (360, 360))
        personaje.play()
        personaje2.play()
        pygame.display.flip()


if __name__ == '__main__':
    run()
