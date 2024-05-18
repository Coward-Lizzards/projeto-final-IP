import pygame
import sys
from math import atan2, cos, sin
from random import randint

# Initialize Pygame
pygame.init()

# Set up Interface
ScreenWidth = 640
ScreenHeight = 640
window = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Shoot 'em up!")

# Sprites
bgGrass = pygame.image.load('bgGrass.png')

# Tree Class
class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('arvore.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.speedBase = speed
        self.speed = speed
        self.dash = 100
        self.isdash = False
        self.cooldown = 0
        self.cooldownTime = 10
        self.left = False
        self.right = False
        self.walkCount = 0

        # Load animation frames
        self.walkRight = [pygame.image.load(f'Game Art/SPRITE ANIMATION/RUN ANIM/pRunRight{i}.png') for i in range(1, 7)]
        self.walkLeft = [pygame.image.load(f'Game Art/SPRITE ANIMATION/RUN ANIM/pRunLeft{i}.png') for i in range(1, 7)]
        self.idle = [pygame.image.load(f'IDLE ANIM/idle{i}.png') for i in range(1, 5)]

        # Set the initial image and position of the player
        self.image = self.idle[0]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, events):
        # Move player
        keys = pygame.key.get_pressed()
        walking = False  # Flag to indicate if the player is walking

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.pos.y -= self.speed
            walking = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.pos.x -= self.speed
            self.left = True
            self.right = False
            walking = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.pos.y += self.speed
            walking = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.pos.x += self.speed
            self.left = False
            self.right = True
            walking = True

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.cooldown == 0 and not self.isdash:
                    self.speed += self.dash
                    self.cooldown = self.cooldownTime
                    self.isdash = True

        if walking:
            # Increment walkCount to smoothly transition between frames
            self.walkCount = (self.walkCount + 1) % len(self.walkRight)
            if self.right:
                self.image = self.walkRight[self.walkCount]
            elif self.left:
                self.image = self.walkLeft[self.walkCount]
        else:
            self.walkCount = 0
            if self.right:
                self.image = self.idle[1]
            elif self.left:
                self.image = pygame.transform.flip(self.idle[1], True, False)

        # Apply cooldown
        if self.cooldown > 0:
            self.cooldown -= 1

        # Update player position
        self.rect.center = self.pos

    def draw(self, window):
        window.blit(self.image, self.rect)
        font = pygame.font.SysFont(None, 20)
        if self.cooldown == 0:
            text = font.render("Dash Available", True, (255, 255, 255))
        else:
            text = font.render("Cooldown: " + str(self.cooldown), True, (255, 255, 255))
        window.blit(text, (10, 10))

class Projectile:
    def __init__(self, x, y, radius, color, angle):
        self.x = x
        self.y = y
        self.radius = radius  # Set the bullet radius here
        self.color = color    # Set the bullet color here
        self.angle = angle
        self.vel = 8

    def update(self):
        self.x += self.vel * cos(self.angle)
        self.y += self.vel * sin(self.angle)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        sprites_sorted = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)
        for sprite in sprites_sorted:
            window.blit(sprite.image, sprite.rect)

# Setup Camera
camera_group = CameraGroup()

for i in range(20):
    random_x = randint(0, 550)
    random_y = randint(0, 550)
    Tree((random_x, random_y), camera_group)

def redrawGameWindow():
    window.blit(bgGrass, (0, 0))
    camera_group.custom_draw()
    for bullet in bullets:
        bullet.update()
        bullet.draw(window)
    pygame.display.update()

# Main Loop
player = Player(250, 250, 5)
bullets = []
camera_group.add(player)
clock = pygame.time.Clock()
run = True
while run:
    # Limit frame rate to 60 FPS
    clock.tick(60)

    # Reset player speed if dash is not active
    if not player.isdash:
        player.speed = player.speedBase

    # Collect events
    events = pygame.event.get()

    # Check for quit event
    for event in events:
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = atan2(mouse_y - player.pos.y, mouse_x - player.pos.x)
                if len(bullets) < 5:
                    # Adjust the radius and color of the bullets here
                    bullets.append(Projectile(player.pos.x, player.pos.y, 3, (255, 255, 255), angle))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.cooldown == 0 and not player.isdash:
                player.speed += player.dash
                player.cooldown = player.cooldownTime
                player.isdash = True

    # Update player with events
    player.update(events)

    # Handle bullets
    for bullet in bullets:
        if 0 < bullet.x < ScreenWidth and 0 < bullet.y < ScreenHeight:
            bullet.update()
        else:
            bullets.remove(bullet)

    # Deactivate dash after one frame
    if player.isdash:
        player.isdash = False

    # Draw
    redrawGameWindow()

pygame.quit()
sys.exit()
