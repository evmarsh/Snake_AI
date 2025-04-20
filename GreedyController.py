from Controller import Controller
from Snake import Snake
from World import World
import pygame

class GreedyController(Controller):

    def __init__(self, s: Snake):
        self.snake = s
        self.world = None

    def move(self):
        self.snake.move()

    def giveWorldView(self, w: World):
        self.world = w

    def processInput(self, event):
        direction = pygame.math.Vector2()
        suggested_direction = self.get_next_move()
        direction.xy = suggested_direction[0], suggested_direction[1]
        
        print("Greedy Algorithm determined best direction was - ", direction)
        self.snake.change_direction(direction)

    def get_next_move(self):
        head = self.snake.body[0]  # Access the snake's head
        visited = set((segment.x, segment.y) for segment in self.snake.body)  # Use tuple (x, y)
        best_move = None
        min_distance = float('inf')
        world_size = self.world.getWorldSize()
        food_position = self.world.getApplePos()

        # Debug print
        print(f"Current head position: ({head.x}, {head.y})")
        print(f"World size: {world_size.x} x {world_size.y}")
        print(f"Food position: ({food_position.x}, {food_position.y})")

        # Check the 4 possible directions (left, right, up, down)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = head.x + dx * self.snake.size, head.y + dy * self.snake.size

            # Debug print for the new position
            print(f"Trying move: ({new_x}, {new_y})")

            # Check bounds
            if not (0 <= new_x < world_size.x and 0 <= new_y < world_size.y):
                print(f"Move ({new_x}, {new_y}) is out of bounds.")
                continue

            # Avoid self-collision by checking the tuple (new_x, new_y)
            # if (new_x, new_y) in visited:  # Check with tuple (x, y) for collision
            #    print(f"Move ({new_x}, {new_y}) collides with the snake's body.")
            #    continue

            # Manhattan distance to food
            distance = abs(new_x - food_position.x) + abs(new_y - food_position.y)
            print(f"Manhattan distance: {distance}")

            # Update best move if this is the best option
            if distance < min_distance:
                min_distance = distance
                best_move = (dx, dy)  # Store the direction as a tuple (dx, dy)

        return best_move  # Return the direction tuple (dx, dy)

