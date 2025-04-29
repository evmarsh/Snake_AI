from Controller import Controller
from Snake import Snake
from World import World
import pygame
import heapq

class UniformCostSearchController(Controller):

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
        if suggested_direction is not None:
            direction.xy = suggested_direction[0], suggested_direction[1]
            print("Uniform Cost Search determined best direction was - ", direction)
            self.snake.change_direction(direction)
        else:
            print("No valid move found! Continuing current direction.")

    def get_next_move(self):
        head = self.snake.body[0]
        food_position = self.world.getApplePos()
        world_size = self.world.getWorldSize()

        # Priority queue: (total_cost, (x, y), path_so_far)
        frontier = []
        heapq.heappush(frontier, (0, (head.x, head.y), []))

        # Visited positions set. Used to track visited coordinates
        visited = set((segment.x, segment.y) for segment in self.snake.body)

        while frontier:
            cost_so_far, (current_x, current_y), path = heapq.heappop(frontier)

            if (current_x, current_y) == (food_position.x, food_position.y):
                if path:
                    # Return the first move in the found path
                    return path[0]
                else:
                    # Already at food position
                    return None

            # Check all nearby coordinate and determine
            # Which to add to the heap while also adding to visited set
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x = current_x + dx * self.snake.size
                new_y = current_y + dy * self.snake.size

                if not (0 <= new_x < world_size.x and 0 <= new_y < world_size.y):
                    continue

                if (new_x, new_y) in visited:
                    continue

                #Increment the total cost by 1
                new_cost = cost_so_far + 1
                new_path = path + [(dx, dy)]

                heapq.heappush(frontier, (new_cost, (new_x, new_y), new_path))
                visited.add((new_x, new_y))

        # If no path to food is found
        return None

