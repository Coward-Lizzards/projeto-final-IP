import pygame
import sys
from math import atan2, cos, sin
from random import randint
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Set up Interface
ScreenWidth = 1080
ScreenHeight = 720
window = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Shoot 'em up!")

PixeloidMono = 'PixeloidMono.ttf'
# Sprites
bgmenu = pygame.image.load('bgGrass.png')

def redrawMenuWindow():
    window.blit(bgmenu, (0, 0))
    pygame.display.update()


clock = pygame.time.Clock()
run = True
while run:
    pygame.time.delay(25)
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    redrawMenuWindow()