import pygame
import sys
from math import atan2, cos, sin
from random import randint
from pygame.math import Vector2

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

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, angle):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius  # Set the bullet radius here
        self.color = color    # Set the bullet color here
        self.angle = angle
        self.vel = 8
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.x += self.vel * cos(self.angle)
        self.y += self.vel * sin(self.angle)
        self.rect.center = (self.x, self.y)

    def draw(self, win):
        win.blit(self.image, self.rect)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        sprites_sorted = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)
        for sprite in sprites_sorted:
            window.blit(sprite.image, sprite.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, target):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.speed = speed
        self.target = target
        self.left = False
        self.right = False
        self.walkCount = 0
        self.path = []

        self.walkLeft = [pygame.image.load(f'ENEMY RUN\EnemyRun{i}.png') for i in range(1, 7)]
        self.walkRight = [pygame.transform.flip(pygame.image.load(f'ENEMY RUN\EnemyRun{i}.png'), True, False) for i in range(1, 7)]
        self.image = self.walkLeft[0]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        walking = True
        if self.target.pos.distance_to(self.pos) < 300:
            self.move_towards_player()
        else:
            self.wander()
        
        if self.target.pos.x > self.pos.x:
            self.right = True
            self.left = False
        elif self.target.pos.x < self.pos.x:
            self.right = False
            self.left = True
        
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
                self.image = self.walkRight[0]
            elif self.left:
                self.image = pygame.transform.flip(self.walkRight[0], True, False)

    def move_towards_player(self):
        direction = self.target.pos - self.pos
        direction.normalize_ip()
        self.pos += direction * self.speed
        self.rect.center = self.pos

    def wander(self):
        if not self.path or self.pos.distance_to(self.path[0]) < 5:
            random_offset = Vector2(randint(-40, 40), randint(-40, 40))
            self.path = [Vector2(randint(0, ScreenWidth), randint(0, ScreenHeight)) + random_offset]
        else:
            direction = self.path[0] - self.pos
            direction.normalize_ip()
            self.pos += direction * self.speed
            self.rect.center = self.pos

# Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x_diff = self.width / 2 - target.rect.centerx
        y_diff = self.height / 2 - target.rect.centery
        self.camera = pygame.Rect(x_diff, y_diff, self.width, self.height)

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

player = Player(250, 250, 5)
camera_group.add(player)

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ENEMY_SPAWN_INTERVAL = 60
MAX_ENEMIES = 10

camera = Camera(ScreenWidth // 8, ScreenHeight // 8)
enemy_spawn_counter = 0
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    if not player.isdash:
        player.speed = player.speedBase
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = atan2(mouse_y - player.pos.y, mouse_x - player.pos.x)
                if len(bullets) < 5:
                    bullet = Projectile(player.pos.x, player.pos.y, 3, (255, 255, 255), angle)
                    bullets.add(bullet)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.cooldown == 0 and not player.isdash:
                player.speed += player.dash
                player.cooldown = player.cooldownTime
                player.isdash = True
    player.update(events)
    for enemy in enemies:
        enemy.update()

    # Spawn enemies
    if len(enemies) < MAX_ENEMIES:
        enemy_spawn_counter -= 1
        if enemy_spawn_counter <= 0:
            random_x = randint(0, ScreenWidth)
            random_y = randint(0, ScreenHeight)
            enemy = Enemy(random_x, random_y, 2, player)
            enemies.add(enemy)
            camera_group.add(enemy)
            enemy_spawn_counter = ENEMY_SPAWN_INTERVAL

    # Check collisions between bullets and enemies
    for bullet in bullets:
        for enemy in enemies:
            if pygame.sprite.collide_rect(bullet, enemy):
                enemies.remove(enemy)
                camera_group.remove(enemy)
                bullets.remove(bullet)
                break

    # Check collisions between enemies and the player
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            # Calculate the vector from the player to the enemy
            collision_vector = enemy.pos - player.pos
            # Calculate the overlap distance
            overlap_distance = (player.rect.width + enemy.rect.width) / 2 - collision_vector.length()
            # Move both the player and the enemy away from each other along the collision vector
            player.pos -= collision_vector.normalize() * overlap_distance / 2
            enemy.pos += collision_vector.normalize() * overlap_distance / 2

    # Check collisions between enemies
    for enemy1 in enemies:
        for enemy2 in enemies:
            if enemy1 != enemy2:
                if pygame.sprite.collide_rect(enemy1, enemy2):
                    # Calculate the vector between the two enemies
                    collision_vector = enemy2.pos - enemy1.pos
                    # Calculate the overlap distance
                    overlap_distance = (enemy1.rect.width + enemy2.rect.width) / 2 - collision_vector.length()
                    # Move the colliding enemies away from each other along the collision vector
                    enemy1.pos -= collision_vector.normalize() * overlap_distance / 2
                    enemy2.pos += collision_vector.normalize() * overlap_distance / 2

    for bullet in bullets:
        if 0 < bullet.x < ScreenWidth and 0 < bullet.y < ScreenHeight:
            bullet.update()
        else:
            bullets.remove(bullet)
    if player.isdash:
        player.isdash = False
    redrawGameWindow()

pygame.quit()
sys.exit()
