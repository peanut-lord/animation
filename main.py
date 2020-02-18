import itertools

import pygame

SPRITE_SIZE = 90
DISTANCE_PER_FRAME = 80


def load_sprites(location):
    sprite_sheet = pygame.image.load(location)

    sprites = []
    for i in range(4):
        for j in range(5):
            # left top width height
            coords = (j * SPRITE_SIZE, i * SPRITE_SIZE)
            size = (SPRITE_SIZE, SPRITE_SIZE)

            sprite_rect = pygame.Rect(coords, size)
            sprite = pygame.Surface(sprite_rect.size).convert()
            sprite.set_colorkey((0, 0, 0), pygame.RLEACCEL)
            sprite.blit(sprite_sheet, (0, 0), sprite_rect)

            sprites.append(sprite)

    return sprites


def main():
    pygame.init()

    # Our screen to work on
    screen = pygame.display.set_mode((800, 600))

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # left, right, up, down
    sprites = load_sprites("spritesheet.png")

    def move_left():
        yield from itertools.cycle([4, 3, 2, 1])

    def move_right():
        yield from itertools.cycle([0, 1, 2, 3])

    def move_up():
        yield from itertools.cycle([1, 2, 3, 4])

    def move_down():
        yield from itertools.cycle([1, 2, 3, 4])

    clock = pygame.time.Clock()
    player = (0, 0)
    direction = move_right()
    sprite_key = 2
    while True:
        # Our frames per second
        delta = clock.tick(8)
        print('time delta: %d' % delta)

        # the player coords
        x, y = player

        # The keys the ur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # TODO drain the queue properly per frame (last one counts),
            #  so we don't block after this frame
            if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if direction.__name__ is not move_left.__name__:
                        direction = move_left()

                    sprite_key = next(direction)
                    x -= DISTANCE_PER_FRAME * (delta / 1000)

                if event.key == pygame.K_RIGHT:
                    if direction.__name__ is not move_right.__name__:
                        direction = move_right()

                    # First 5 are moving left and standing still
                    sprite_key = 5 + next(direction)
                    x += DISTANCE_PER_FRAME * (delta / 1000)

                if event.key == pygame.K_UP:
                    if direction.__name__ is not move_up.__name__:
                        direction = move_up()

                    sprite_key = 10 + next(direction)
                    y -= DISTANCE_PER_FRAME * (delta / 1000)

                if event.key == pygame.K_DOWN:
                    if direction.__name__ is not move_down.__name__:
                        direction = move_down()

                    sprite_key = 15 + next(direction)
                    y += DISTANCE_PER_FRAME * (delta / 1000)

        screen.blit(background, (0, 0))
        screen.blit(sprites[sprite_key], (x, y))
        pygame.display.flip()

        player = x, y


if __name__ == "__main__":
    main()
