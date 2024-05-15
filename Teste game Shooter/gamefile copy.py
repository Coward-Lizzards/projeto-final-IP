import pygame
import sys
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
        super().__init__()
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
        self.idleCount = 0
        self.idleFrameDuration = 10

        # Load animation frames
        self.walkRight = [pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunRight1.png'),
                          pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunRight2.png'),
                          pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunRight3.png'),
                          pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunRight4.png'),
                          pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunRight5.png'),
                          pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunRight6.png')]
        self.walkLeft = [pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunLeft1.png'),
                         pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunLeft2.png'),
                         pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunLeft3.png'),
                         pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunLeft4.png'),
                         pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunLeft5.png'),
                         pygame.image.load('Game Art/SPRITE ANIMATION/RUN ANIM/pRunLeft6.png')]
        self.idle = [pygame.image.load('IDLE ANIM/idle1.png'),
                     pygame.image.load('IDLE ANIM/idle2.png'),
                     pygame.image.load('IDLE ANIM/idle3.png'),
                     pygame.image.load('IDLE ANIM/idle4.png')]

        # Set the initial image and position of the player
        self.image = self.idle[0]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Move player
        keys = pygame.key.get_pressed()
        walking = False  # Flag to indicate if the player is walking
        if keys[pygame.K_w]:
            self.pos.y -= self.speed
            self.left = False
            self.right = False
            walking = True
        if keys[pygame.K_a]:
            self.pos.x -= self.speed
            self.left = True
            self.right = False
            walking = True
        if keys[pygame.K_s]:
            self.pos.y += self.speed
            self.left = False
            self.right = False
            walking = True
        if keys[pygame.K_d]:
            self.pos.x += self.speed
            self.left = False
            self.right = True
            walking = True

        # Update walk animation
        if walking:  # Only update walkCount when walking
            if self.walkCount + 1 >= len(self.walkRight) * 3:
                self.walkCount = 0
            else:
                self.walkCount += 1
        else:  # Reset walkCount if player stops moving
            self.walkCount = 0

        # Update idle animation
        if not walking:  # If not moving
            if self.idleCount + 1 >= len(self.idle) * self.idleFrameDuration:
                self.idleCount = 0
            self.image = self.idle[self.idleCount // self.idleFrameDuration]  # Switch between idle frames
            self.idleCount += 1

        # Apply cooldown
        if self.cooldown > 0:
            self.cooldown -= 1

        # Update player position
        self.rect.center = self.pos

    def draw(self, window):
        if self.left:
            window.blit(self.walkLeft[self.walkCount // 3], self.rect)
        elif self.right:
            window.blit(self.walkRight[self.walkCount // 3], self.rect)
        else:
            window.blit(self.image, self.rect)

        font = pygame.font.SysFont(None, 20)
        if self.cooldown == 0:
            text = font.render("Dash Available", True, (255, 255, 255))
        else:
            text = font.render("Cooldown: " + str(self.cooldown), True, (255, 255, 255))
        window.blit(text, (10, 10))


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self, window):
        for sprite in self.sprite():
            window.blit(sprite.image, sprite.rect)


# Setup Camera
camera_group = CameraGroup()

for i in range(20):
    random_x = randint(0, 550)
    random_y = randint(0, 550)
    Tree((random_x, random_y), camera_group)


def redrawGameWindow():
    window.blit(bgGrass, (0, 0))
    player.draw(window)
    pygame.display.update()


# Main Loop
player = Player(250, 250, 5)
clock = pygame.time.Clock()
run = True
while run:
    # Limit frame rate to 60 FPS
    pygame.time.delay(25)
    clock.tick(60)

    # Reset player speed if dash is not active
    if not player.isdash:
        player.speed = player.speedBase

    # Check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Skills
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.cooldown == 0 and not player.isdash:
                player.speed += player.dash
                player.cooldown = player.cooldownTime
                player.isdash = True

    # Deactivate dash after one frame
    if player.isdash:
        player.isdash = False

    # Movement Keys
    player.update()

    # Draw
    redrawGameWindow()

pygame.quit()
sys.exit()