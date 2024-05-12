import pygame

# Initialize Pygame
pygame.init()

# Set up Interface
ScreenWidth = 500
ScreenHeight = 500
window = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Shoot 'em up!")

# Set Player
playerx = 250
playery = 250
playerheight = 30
playerwidth = 30
playerspeedbase = 10
playerspeed = 10
dash = 100

# Skill Timers 
isdash = False
basetimer = 5000
timer = 5000
candash = True

# Main Loop
run = True
while run:
    pygame.time.delay(60)

    # Reset player speed if dash is not active
    if not isdash:
        playerspeed = playerspeedbase

    # Skill timer
    if isdash:
        if timer <= 0:
            isdash = False
            timer = basetimer
            candash = True

    # check for event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Skills
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and candash:
                isdash = True
                playerspeed += dash
                candash = False

    # Deactivate dash after one frame
    if isdash:
        isdash = False

    if not candash:
        timer -= 1

    # Movement Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and playery > playerspeed:
        playery -= playerspeed
    if keys[pygame.K_a] and playerx > playerspeed:
        playerx -= playerspeed
    if keys[pygame.K_s] and playery < ScreenHeight - playerheight - playerspeed:
        playery += playerspeed
    if keys[pygame.K_d] and playerx < ScreenWidth - playerwidth - playerspeed:
        playerx += playerspeed

    # Draw
    window.fill((0,0,0))
    pygame.draw.rect(window, (255,0,0), (playerx, playery, playerwidth, playerheight))
    font = pygame.font.SysFont(None, 20)
    if candash:
        text = font.render("Dash Available", True, (255, 255, 255))
    else:
        text = font.render("Cooldown: " + str(timer // 60), True, (255, 255, 255))
    window.blit(text, (10, 10))
    pygame.display.update()

    print(timer)
pygame.quit()