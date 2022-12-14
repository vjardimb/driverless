import pygame
import math
import numpy as np
from scipy.spatial import ConvexHull
from scipy import interpolate

class Dot:
    def __init__(self, screen, color, pos, size=8):
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size

    def update(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.size)


def gen_path(screen, dim):
    # generate 20 random points
    points = np.random.randint(dim*0.2, dim*0.8, size=(20, 2))
    hull = ConvexHull(points)

    x_vertices = np.r_[points[hull.vertices, 0], points[hull.vertices[0], 0]]
    y_vertices = np.r_[points[hull.vertices, 1], points[hull.vertices[0], 1]]

    corner_dots = []
    spl_dots = []

    # fit splines to x=f(u) and y=g(u), treating both as periodic. also note that s=0
    # is needed in order to force the spline fit to pass through all the input points.
    tck, u = interpolate.splprep([x_vertices, y_vertices], s=0, per=True)
    # evaluate the spline fits for 1000 evenly spaced distance values
    xi, yi = interpolate.splev(np.linspace(0, 1, 1000), tck)

    for [x, y] in zip(xi, yi):
        spl_dots.append(Dot(screen, "yellow", (x, y), 3))

    return spl_dots, np.concatenate((xi.reshape((xi.shape[0], 1)), yi.reshape((yi.shape[0], 1))), axis=1)


def get_closest_point(pose, spl_array, screen):
    position = np.array([pose[0], pose[1]]).reshape((1, 2))
    position = np.repeat(position, len(spl_array), axis=0)

    dists_sqrd = np.sum((position - spl_array)**2, axis=1)
    closest_index = np.argmin(dists_sqrd)

    return Dot(screen, "red", (spl_array[closest_index, 0], spl_array[closest_index, 1]), 8), (spl_array[closest_index, 0], spl_array[closest_index, 1])


def right_or_left_1(pose, closest_point):
    x = pose[0]
    y = pose[1]
    angle = math.radians(pose[2])

    c_x = closest_point[0]
    c_y = closest_point[1]

    rotation_matrix = [[math.cos(angle), -math.sin(angle), 0],
                       [math.sin(angle), math.cos(angle), 0],
                       [0, 0, 1]]

    transl_vector = [[x],
                     [y],
                     [0]]

    position = [[c_x],
                [c_y],
                [0]]

    new_closest = np.dot(rotation_matrix, np.array(position)-np.array(transl_vector))

    # multiplier = 1 if math.sin(angle) > 0 else -1

    # return "right" if new_closest[1]*multiplier > 1 else "left", (new_closest[0], new_closest[1])
    return "right" if new_closest[0] > 0 else "left", abs(new_closest[0])


def right_or_left_2(pose, closest_point):
    r_x = pose[0]
    r_y = pose[1]
    angle = math.radians(pose[2])

    s = math.sin(angle)
    c = math.cos(angle)

    c_x = closest_point[0]
    c_y = closest_point[1]

    def line(x):
        # get the line function for the car pose. format: y=a*x+b
        a = math.tan(angle)
        b = r_y - math.tan(angle) * r_x

        # print("\n\n\na: ", a, "b: ", b)

        return a*x+b

    # print("r_y:", r_y, "c_x:", r_x)

    above = c_y > line(c_x)

    if (s<0 and above) or (s>0 and not above):
       return "right"
    else:
        return "left"


def turn(car, side, error):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        car.rotate(40, left=True)
    if keys[pygame.K_d]:
        car.rotate(40, right=True)
    # if keys[pygame.K_w]:
    if True:
        moved = True
        car.move_forward()

    if not moved:
        car.reduce_speed()

    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        # if False:
        print(side)
        if side == "left":
            car.rotate(error, left=True)
        else:
            car.rotate(error, right=True)

if __name__ == "__main__":
    # win = pygame.display.set_mode((810, 810))
    #
    # spl_dots, spl_array = gen_path(win, 810)
    #
    # get_closest_point((30, 50, 100), spl_array, win)
    pass