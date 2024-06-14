import pygame
import sys
import subprocess

# Alunos: Marina Luisa Lemos Barcelos e Nicolas R. Emery 

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BARATALYPSE")

# Load background image
background = pygame.image.load('menu page.png')
Pixeloid = 'PixeloidMono.ttf'

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

# Function to update and save score
def update_score(score):
    with open("score.txt", "w") as file:
        file.write(str(score))

# Function to read score
def read_score():
    try:
        with open("score.txt", "r") as file:
            score_str = file.read().strip()  # Read and remove leading/trailing whitespace
            if score_str:
                return int(score_str)  # Convert to integer if not empty
            else:
                return 0  # Return 0 if the file was empty
    except FileNotFoundError:
        return 0  # Return 0 if the file does not exist
    except ValueError:
        return 0  # Return 0 if there was an issue converting to integer

# Create button instances

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

    # Get current score and display it above the start button
    current_score = read_score()
    font = pygame.font.Font(Pixeloid, 36)
    score_text = font.render("Score: {}".format(current_score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(width // 2, 400))
    screen.blit(score_text, score_rect)
    
    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
