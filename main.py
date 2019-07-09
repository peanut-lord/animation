import pygame
import itertools
from collections import namedtuple
sprites = namedtuple('sprites', ['left', 'right', 'up', 'down'])


# What do I need to know?
# Which direction (to + or - x and y)
# current coords (tuple with x, y)
# which sprite to draw and cycle through them
# if we know the direction, *but* no key press: standing still
def slice_sprites():
    left, right, up, down = list(), list(), list(), list()

    spritesheet = pygame.image.load('spritesheet.png')

    # We now our movements are five sprites long
    for i in range(5):
        sprite_size = pygame.Rect(i * 90, 0, 90, 90)
        sprite = pygame.Surface(sprite_size.size).convert()
        sprite.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        sprite.blit(spritesheet, (0, 0), sprite_size)

        left.append(sprite)

    for i in range(5):
        sprite_size = pygame.Rect(i * 90, 90, 90, 90)
        sprite = pygame.Surface(sprite_size.size).convert()
        sprite.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        sprite.blit(spritesheet, (0, 0), sprite_size)

        right.append(sprite)

    return sprites(left, right, up, down)


def main():
    pygame.init()

    # Our screen to work on
    screen = pygame.display.set_mode((800, 600))

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    left, right, _, _ = slice_sprites()

    def move_left():
        yield from itertools.cycle([1, 2, 3, 4])

    def move_right():
        yield from itertools.cycle([4, 3, 2, 1])

    clock = pygame.time.Clock()
    x = 710
    direction = move_left()
    while True:
        # One frame per second
        delta = clock.tick(8)
        print('time delta: %d' % delta)

        # Check only quit for now
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.K_RIGHT:
                direction = move_right()

            if event.type == pygame.K_LEFT:
                direction = move_left()

        x -= 100 * (delta / 1000)

        screen.blit(background, (0, 0))
        # I only care about the image to draw,
        screen.blit(left[next(direction)], (x, 0))
        pygame.display.flip()

    print('Quiting ')
    pygame.quit()


if __name__ == '__main__':
    main()
