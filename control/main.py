import pygame
import time
import math

from car import PlayerCar
from path import gen_path, get_closest_point, right_or_left_1, right_or_left_2
from utils import scale_image, blit_rotate_center


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

if __name__ == "__main__":
    run = True
    clock = pygame.time.Clock()

    GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
    TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
    TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.6)

    # images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
    # images = [(TRACK, (0, 0))]
    images = []
    player_car = PlayerCar(4, 4)

    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Racing Game!")

    FPS = 60

    spl_dots, spl_array = gen_path(WIN, WIDTH)

    WIN.fill(0)

    while run:
        clock.tick(FPS)

        draw(WIN, images, player_car)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:
            player_car.rotate(left=True)
        if keys[pygame.K_d]:
            player_car.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            player_car.move_forward()

        if not moved:
            player_car.reduce_speed()

        closest_dot, coords = get_closest_point((player_car.x, player_car.y, player_car.angle), spl_array, WIN)

        for dot in spl_dots+[closest_dot]:
            dot.update()
            # the_dot.update()

        # side, (x, y) = right_or_left_2((player_car.x, player_car.y, player_car.angle), coords)
        # side, (x,y) = right_or_left((20, 10, 30), (50, 50))

        # print("\n\nx: ",player_car.x, "\ny: ",player_car.y, "\norientation: ", player_car.angle)
        # print(player_car.angle)
        # print("\n\nx: ",player_car.x, "\ny: ",player_car.y, "\norientation: ", player_car.angle)
        # print(side)
        # print("ccords", coords)

    pygame.quit()
