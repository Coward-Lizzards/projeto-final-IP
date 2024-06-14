import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BARATALYPSE")

# Load background image
background = pygame.image.load('menu page.png')

# Define the Button class
class Button:
    def __init__(self, x, y, width, height, image_path, text="", font=None, font_size=36, font_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        
        # Text attributes
        self.text = text
        self.font_path = 'PixeloidMono.ttf'  # Path to your PixeloidMono font file
        self.font_size = font_size
        self.font_color = font_color
        self.font = pygame.font.Font(self.font_path, self.font_size)
        
        # Calculate text position
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.text_image = text_surface
        self.text_rect = text_rect

    def draw(self, screen):
        # Draw button image
        screen.blit(self.image, self.rect)

        # Draw button text
        screen.blit(self.text_image, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button click
                if self.rect.collidepoint(event.pos):
                    return True
        return False

# Create button instances
start_button = Button(358, 452, 364, 88, 'botao-grande.png', text="Start")
tutorial_button = Button(358, 566, 364, 88, 'botao-grande.png', text="Tutorial")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button click
                if start_button.handle_event(event):
                    print("Start button clicked!")
                    # Run the game script
                    subprocess.run(["python", "gamefile_copy_4.py"])
                elif tutorial_button.handle_event(event):
                    print("Tutorial button clicked!")
                    # Run the tutorial script
                    subprocess.run(["python", "tutorial.py"])

    # Draw background image
    screen.blit(background, (0, 0))
    
    # Draw the buttons
    start_button.draw(screen)
    tutorial_button.draw(screen)
    
    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
