
from Controller import Controller
from Snake import Snake
from World import World
import pygame
import heapq

class AStarSearchController(Controller):

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
            print("A* Search determined best direction was - ", direction)
            self.snake.change_direction(direction)
        else:
            print("No valid move found! Continuing current direction.")

    def get_next_move(self):
        head = self.snake.body[0]
        food_position = self.world.getApplePos()
        world_size = self.world.getWorldSize()

        def heuristic(x, y):
            # Manhattan distance to food
            return abs(x - food_position.x) + abs(y - food_position.y)

        start = (head.x, head.y)
        g_scores = {start: 0}  # Cost from start to a node
        visited = {}  

        # Track the snake to avoid collisions
        body_positions = set((segment.x, segment.y) for segment in self.snake.body)

        # Priority queue for A* (f_score, g_score, position, path_taken)
        frontier = []
        heapq.heappush(frontier, (heuristic(head.x, head.y), 0, start, []))

        while frontier:
            f_score, g_score, current, path = heapq.heappop(frontier)
            current_x, current_y = current

            # Pull node with lowest f_score (cost)
            if current in visited and visited[current] <= g_score:
                continue
            visited[current] = g_score

            if current == (food_position.x, food_position.y):
                if path:
                    return path[0]

            # Explore logic 
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x = current_x + dx * self.snake.size
                new_y = current_y + dy * self.snake.size
                new_pos = (new_x, new_y)

                # Skip if outside grid 
                if not (0 <= new_x < world_size.x and 0 <= new_y < world_size.y):
                    continue

                # Skip if occupied by snake 
                if new_pos in body_positions:
                    continue

                new_g = g_score + 1
                new_h = heuristic(new_x, new_y)
                new_f = new_g + new_h
                new_path = path + [(dx, dy)]

                if new_pos not in visited or new_g < visited[new_pos]:
                    heapq.heappush(frontier, (new_f, new_g, new_pos, new_path)) # Add node back to queue 

        return None 
