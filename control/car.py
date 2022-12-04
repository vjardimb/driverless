from utils import blit_rotate_center
import pygame
import time
import math
from utils import scale_image, blit_rotate_center

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

class AbstractCar:
	def __init__(self, max_vel, rotation_vel):
		self.img = self.IMG
		self.max_vel = max_vel
		self.vel = 0
		self.rotation_vel = rotation_vel
		self.angle = 0
		self.x, self.y = self.START_POS
		self.acceleration = 0.1
		self.old_error = 0

	def rotate(self, error, left=False, right=False):
		# kp = 0.07
		# kd = 0.7
		kp = 0.09
		kd = 1
		# if old_error == None:
		# 	old_error = 0

		if left:
			self.angle += kp*min(error, 15) + kd*(error - self.old_error)
			# self.angle += 2
			print(kp*min(error, 1500) - kd*(error - self.old_error))
		elif right:
			self.angle -= kp*min(error, 15) + kd*(error - self.old_error)
			# self.angle -= 2

		self.old_error = error

	def draw(self, win):
		blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

	def move_forward(self):
		self.vel = min(self.vel + self.acceleration, self.max_vel)
		self.move()

	def move(self):
		radians = math.radians(self.angle)
		vertical = math.cos(radians) * self.vel
		horizontal = math.sin(radians) * self.vel

		self.y -= vertical
		self.x -= horizontal

	def reduce_speed(self):
		self.vel = max(self.vel - self.acceleration / 2, 0)
		self.move()


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)