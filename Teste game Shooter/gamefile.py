import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up Interface
ScreenWidth = 640
ScreenHeight = 640
window = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Shoot 'em up!")

# Set Player
walkRight = [pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight1.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight2.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight3.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight4.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight5.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunRight6.png')]
walkLeft = [pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft1.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft2.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft3.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft4.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft5.png'),pygame.image.load('Game Art\SPRITE ANIMATION\RUN ANIM\pRunLeft6.png')]
bgGrass = pygame.image.load('bgGrass.png')
idle = pygame.image.load('IDLE ANIM\idle1.png')

PlayerLeft = False
PlayerRight = False
walkCount = 0

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = x
        self.width = width
        self.height = height
        self.speedBase = 20
        self.speed = 20
        self.dash = 100
        self.isdash = False
        self.cooldown = 0
        self.cooldownTime = 10

    def update(self):
        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        elif keys[pygame.K_a]:
            self.x -= self.speed
            PlayerLeft = True
            PlayerRight = False
        else:
            PlayerRight = False
            PlayerLeft = False
            walkCount = 0
        if keys[pygame.K_s]:
            self.y += self.speed
        elif keys[pygame.K_d]:
            self.x += self.speed
            PlayerRight = True
            PlayerLeft = False
        else:
            PlayerRight = False
            PlayerLeft = False
            walkCount = 0

        # Apply cooldown
        if self.cooldown > 0:
            self.cooldown -= 1

        # Reset walkCount if player stops moving
        if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
            self.walkCount = 0
    
def redrawGameWindow():
    global walkCount

    window.blit(bgGrass, (0,0))
    
    if walkCount + 1 >= 27:
        walkCount = 0

    if PlayerLeft:
        window.blit(walkLeft[walkCount//3],(player.x, player.y))
        walkCount += 1

    elif PlayerRight:
        window.blit(walkRight[walkCount//3],(player.x, player.y))
        walkCount += 1

    else:
        window.blit(idle, (player.x, player.y))

    font = pygame.font.SysFont(None, 20)
    if player.cooldown == 0:
        text = font.render("Dash Available", True, (255, 255, 255))
    else:
        text = font.render("Cooldown: " + str(player.cooldown), True, (255, 255, 255))
    window.blit(text, (10, 10))
    pygame.display.update()

    

# Main Loop
player = Player(250, 250, 48, 48)
clock = pygame.time.Clock()
run = True
while run:
    # Limit frame rate to 60 FPS
    pygame.time.delay(100)
    clock.tick(60)

    # Reset player speed if dash is not active
    if not player.isdash:
       player.speed = player.speedBase

    # Skill timer
        # Ensure timer is positive before decrementing
    #    if timer > 0 and player.isdash == True:  
     #       timer -= 1
      #  else:
       #     timer = 0
        #if timer == 0:
         #   player.isdash = False
          #  player.cooldown = True
           # timer = basetimer

    # check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Skills
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.cooldown == 0 and player.isdash == False:
                player.speed += player.dash
                player.cooldown = player.cooldownTime
                player.isdash = True

    # Deactivate dash after one frame
    if player.isdash == True:
        player.isdash = False


    # Movement Keys
    player.update()

    # Draw
    redrawGameWindow()


pygame.quit()
sys.exit()