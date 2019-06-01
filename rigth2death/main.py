import pygame
from pygame import Color
from pygame.constants import KEYDOWN, K_ESCAPE, KEYUP
from pygame.surface import Surface

from rigth2death.characters import Player
from rigth2death.utils import Utils


def run():
    pygame.init()
    screen: Surface = pygame.display.set_mode((800, 600))
    running = True
    clock: pygame.time.Clock = pygame.time.Clock()
    zombie = Player.CustomSprite(Utils.img('zombies.png'), clock, 5, is_vertical=False)
    player = Player.Player(clock)

    moves = []
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
                moves.append(event.key)
                print(moves)
            if event.type == KEYUP:
                print("leave keyup")
                if event.key in moves:
                    moves.remove(event.key)
            # Check for QUIT event; if QUIT, set running to false
            elif event.type == pygame.QUIT:
                running = False
        if len(moves) > 0:
            a = moves.pop()
            print("I entered {}".format(a))
            player.move(a)
            moves.append(a)

        # Draw the player to the screen
        # Update the display

        screen.blit(player.current_sprite.image, player.current_sprite.rect)
        screen.blit(zombie.image, (360, 360))

        zombie.play()
        pygame.display.flip()


if __name__ == '__main__':
    run()
