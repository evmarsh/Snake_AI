import pygame
import sys
from World import World
from Snake import Snake
from Apple import Apple
from PlayerController import PlayerController
from GreedyController import GreedyController
from Controller import Controller
from UniformCostSearch import UniformCostSearchController
from AStarController import AStarSearchController
from RLController import RLController
print("\n" + "=" * 40)
print("Please choose agent algorithm")
print("=" * 40)
print("1. Player Controlled")
print("2. Greedy Algorithm (Manhattan)")
print("3. Reinforcement Algorithm")
print("4. A* Algorithm (Manhattan)")
print("5. Uniform Cost Search")

agent_algorithm_selection = input("Please enter your choice (1 / 2 / 3 / 4 / 5): ").strip()

# Initialize Pygame
pygame.init()

# Load a font
font = pygame.font.SysFont("Arial", 36)


# Set up display dimensions
WIDTH, HEIGHT = 500, 500
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
    
    match agent_algorithm_selection:
        case "1":
            controller = PlayerController(snake)
        case "2":
            controller = GreedyController(snake)
        case "3":
            controller = RLController(snake)
        case "4":
            controller = AStarSearchController(snake)
        case "5":
            controller = UniformCostSearchController(snake)
        case  _:
            controller = PlayerController(snake)
            print("Defaulting controller to player")


    world = World(snake, apple, controller, WIDTH, HEIGHT)
    
    controller.giveWorldView(world)

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
                    controller.plot_rewards(controller.reward_per_epoch)
                    controller.plot_costs(controller.cost)
                # Handle movement
                else:
                    world.doInput(event)
        
        world.doInput()
        world.doMovement()

        screen.fill(BLACK)

        # Get the score from the wordl class
        score = world.score
        max_score = world.maxScore

        # Render the score text
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
        max_score_surface = font.render(f"Max Score: {max_score}", True, (255, 255, 255))  # White text

        # Position it at the top-left corner
        screen.blit(score_surface, (10, 10))
        screen.blit(max_score_surface, (750, 10))
        
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
