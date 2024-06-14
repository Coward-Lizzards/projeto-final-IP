import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Menu")

# Load background image
background = pygame.image.load('menu page.png')

# Define the Button class
class Button:
    def __init__(self, x, y, width, height, image_path):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.is_hovered = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# Create a button instance
start_button = Button(358, 452, 364, 88, 'botao-grande.png')
tutorial_button = Button(358, 566, 364, 88, 'botao-grande.png')

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if start_button.handle_event(event):
            print("Start button clicked!")
            # Run the game script
            subprocess.run(["python", "gamefile_copy_4.py"])
        if tutorial_button.handle_event(event):
            print("Tutorial button clicked!")
            # Run the game script
            subprocess.run(["python", "tutorial.py"])

    # Draw background image
    screen.blit(background, (0, 0))
    
    # Draw the start button
    start_button.draw(screen)
    
    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
