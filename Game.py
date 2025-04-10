import pygame
import sys
from World import World
from Snake import Snake
from Apple import Apple
from PlayerController import PlayerController
from GreedyController import GreedyController

# Initialize Pygame
pygame.init()

# Set up display dimensions
WIDTH, HEIGHT = 1000, 750
WINDOW_TITLE = "Snake"

# Set up colors
BLACK = (0, 0, 0)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

clock = pygame.time.Clock()
FPS = 10

# Main game loop
def main():
    running = True
    
    apple = Apple(25)
    snake = Snake(25, 300, 300, WIDTH, HEIGHT)
    controller = PlayerController(snake)
    greedyController = GreedyController(snake)
    world = World(snake, apple, greedyController, WIDTH, HEIGHT)
    greedyController.giveWorldView(world)

    while running:
        clock.tick(FPS)

        # Check for events
        for event in pygame.event.get():
            # Quit if the close button is pressed
            if event.type == pygame.QUIT:
                running = False
            # Quit if the Escape key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Handle movement
                else:
                    world.doInput(event)
        
        world.doInput()
        world.doMovement()

        screen.fill(BLACK)
        
        world.doCollisions()
        world.draw(screen)
        
        # Update the display
        pygame.display.flip()
    
    # Clean up
    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()
