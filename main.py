import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)


# Create a box
class Box:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.velocity = 5

    def move(self, vector):
        if vector.length() > 0:
            vector.normalize_ip()
        vector *= self.velocity
        self.rect.x += vector[0]
        self.rect.y += vector[1]

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


# Create a box
box = Box(screen_width // 2, screen_height // 2, 50, white)

# Set up the clock
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 30)

# Main game loop
running = True


def draw_objects():
    # Fill the screen with white
    screen.fill(black)
    # Draw the box
    box.draw()
    # Display current fps
    fps_text = font.render("FPS: " + str(int(clock.get_fps())), True, white)
    screen.blit(fps_text, (10, 10))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Get the keys that are currently held down
    keys = pygame.key.get_pressed()

    # Move the box based on the keys
    move_vector = pygame.math.Vector2(0, 0)
    if keys[pygame.K_w]:
        move_vector.y -= 1
    if keys[pygame.K_s]:
        move_vector.y += 1
    if keys[pygame.K_a]:
        move_vector.x -= 1
    if keys[pygame.K_d]:
        move_vector.x += 1
    box.move(move_vector)

    # draws the objects
    draw_objects()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(120)

# Quit the game
pygame.quit()
