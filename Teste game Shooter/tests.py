import pygame
import sys
import random
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_SPEED = 1
ENEMY_SPAWN_INTERVAL = 60
MAX_ENEMIES = 10
TILE_SIZE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Top-Down Shooter")

# Load assets
player_image = pygame.Surface((30, 30))
player_image.fill(WHITE)
enemy_image = pygame.Surface((30, 30))
enemy_image.fill((255, 0, 0))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.position = Vector2(self.rect.center)
        self.velocity = Vector2(0, 0)

    def update(self):
        self.position += self.velocity
        self.rect.center = self.position

    def draw_front_and_back(self, screen):
        # Draw green line in front
        pygame.draw.line(screen, (0, 255, 0), self.rect.center, (self.rect.centerx + 15, self.rect.centery), 2)
        # Draw blue line in back
        pygame.draw.line(screen, (0, 0, 255), self.rect.center, (self.rect.centerx - 15, self.rect.centery), 2)


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
        self.position = Vector2(self.rect.center)
        self.target = target
        self.path = []

    def update(self):
        if self.target.position.distance_to(self.position) < 300:
            self.move_towards_player()
        else:
            self.wander()

    def move_towards_player(self):
        direction = self.target.position - self.position
        direction.normalize_ip()
        self.position += direction * ENEMY_SPEED
        self.rect.center = self.position

    def wander(self):
        if not self.path or self.position.distance_to(self.path[0]) < 5:
            # Add a bit of randomness to the target position
            random_offset = Vector2(random.randint(-40, 40), random.randint(-40, 40))
            self.path = [Vector2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) + random_offset]
        else:
            direction = self.path[0] - self.position
            direction.normalize_ip()
            self.position += direction * ENEMY_SPEED
            self.rect.center = self.position

# Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Calculate the difference between the player's position and the center of the screen
        x_diff = SCREEN_WIDTH / 2 - target.rect.centerx
        y_diff = SCREEN_HEIGHT / 2 - target.rect.centery

        # Adjust the camera's position to keep the player in the center
        self.camera = pygame.Rect(x_diff, y_diff, self.width, self.height)

# Create objects
player = Player()
enemies = pygame.sprite.Group()
camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

# Main loop
enemy_spawn_counter = ENEMY_SPAWN_INTERVAL
clock = pygame.time.Clock()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    player.velocity = Vector2(0, 0)
    if keys[pygame.K_a]:
        player.velocity.x = -PLAYER_SPEED
    if keys[pygame.K_d]:
        player.velocity.x = PLAYER_SPEED
    if keys[pygame.K_w]:
        player.velocity.y = -PLAYER_SPEED
    if keys[pygame.K_s]:
        player.velocity.y = PLAYER_SPEED

    # Update
    player.update()
    camera.update(player)
    for enemy in enemies:
        enemy.update()

    # Spawn enemies
    if len(enemies) < MAX_ENEMIES:
        enemy_spawn_counter -= 1
        if enemy_spawn_counter <= 0:
            enemies.add(Enemy(player))
            enemy_spawn_counter = ENEMY_SPAWN_INTERVAL

    # Check collisions between enemies and the player
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            # Calculate the vector from the player to the enemy
            collision_vector = enemy.position - player.position
            # Calculate the overlap distance
            overlap_distance = (player.rect.width + enemy.rect.width) / 2 - collision_vector.length()
            # Move both the player and the enemy away from each other along the collision vector
            player.position -= collision_vector.normalize() * overlap_distance / 2
            enemy.position += collision_vector.normalize() * overlap_distance / 2

    # Check collisions between enemies
    for enemy1 in enemies:
        for enemy2 in enemies:
            if enemy1 != enemy2:
                if pygame.sprite.collide_rect(enemy1, enemy2):
                    # Calculate the vector between the two enemies
                    collision_vector = enemy2.position - enemy1.position
                    # Calculate the overlap distance
                    overlap_distance = (enemy1.rect.width + enemy2.rect.width) / 2 - collision_vector.length()
                    # Move the colliding enemies away from each other along the collision vector
                    enemy1.position -= collision_vector.normalize() * overlap_distance / 2
                    enemy2.position += collision_vector.normalize() * overlap_distance / 2

    # Draw
    screen.fill(BLACK)
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            if (x // TILE_SIZE + y // TILE_SIZE) % 2 == 0:
                pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    for entity in list(enemies):
        screen.blit(entity.image, camera.apply(entity))

    # Draw front and back lines for player
    player.draw_front_and_back(screen)

    pygame.display.flip()


    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
