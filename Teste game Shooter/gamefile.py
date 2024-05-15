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
walkRight = [pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight1.png'),
             pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight2.png'),
             pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight3.png'),
             pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight4.png'),
             pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight5.png'),
             pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight6.png')]
walkLeft = [pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft1.png'),
            pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft2.png'),
            pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft3.png'),
            pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft4.png'),
            pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft5.png'),
            pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft6.png')]
bgGrass = pygame.image.load('bgGrass.png')
idle = pygame.image.load('IDLE ANIM\idle1.png')


# Tree Class
class Tree(pygame.sprite.Sprite):
    def __init__ (self, pos, group):
        self.image = pygame.image.load('arvore.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speedBase = 5
        self.speed = 1
        self.dash = 100
        self.isdash = False
        self.cooldown = 0
        self.cooldownTime = 10
        self.left = False
        self.right = False
        self.walkCount = 0

    def update(self):
        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.left = True
            self.right = False
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
            self.right = True
            self.left = False

        # Apply cooldown
        if self.cooldown > 0:
            self.cooldown -= 1

        # Reset walkCount if player stops moving
        if not (keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]):
            self.walkCount = 0

    def draw(self, window):
        if self.walkCount + 1 >= 18:
            self.walkCount = 0

        if self.left:
            window.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            window.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            window.blit(idle, (self.x, self.y))

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
            window.blit(sprite.image,sprite.rect)

# Setup Camera
camera_group = CameraGroup()

for i in range(20):
    random_x = randint(0,550)
    random_y = randint(0,550)
    Tree((random_x,random_y),camera_group)

def redrawGameWindow():
    window.blit(bgGrass, (0, 0))
    player.draw(window)
    pygame.display.update()

# Main Loop
player = Player(250, 250, 48, 48)
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
