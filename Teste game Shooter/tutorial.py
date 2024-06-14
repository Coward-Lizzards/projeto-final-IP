import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Menu")

# Load background image
background = pygame.image.load('tutorial page.png')

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Draw background image
    screen.blit(background, (0, 0))
    
    
    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()