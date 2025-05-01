import pygame as pg

GREEN = (0, 255, 0)

class Snake:
    def __init__(self, size, startX, startY, screenWidth, screenHeight):
        self.size = size
        self.velocity = self.size
        self.direction = pg.math.Vector2(1, 0)
        vec = pg.math.Vector2()
        vec.xy = startX, startY
        self.body = [vec]
        self.last_direction = self.direction
        self.screen_width = screenWidth
        self.screen_height = screenHeight

    def init(self):
        pos = pg.math.Vector2()
        pos.xy = 300, 300
        self.body.append(pos)

    def length(self):
        return len(self.body)

    def draw(self, surface):
        for i in range(self.length()):
            rect = pg.Rect(self.body[i].x, self.body[i].y, self.size, self.size)
            pg.draw.rect(surface, GREEN, rect)
    
    def move(self):
        if (self.length() > 1):
            self.last_direction = (self.body[self.length()-1].xy - self.body[self.length()-2].xy) / 50
            for i in range(self.length()-1, 0, -1):
                self.body[i].xy = self.body[i-1].xy
        
        self.body[0].x += self.velocity * self.direction.x
        self.body[0].y += self.velocity * self.direction.y

    def change_direction(self, direction: pg.math.Vector2):
        # if (self.direction + direction != pg.math.Vector2(0,0)):
        #     self.direction = direction
        self.direction = direction

    def grow(self):
        p = pg.math.Vector2()
        p.x = self.body[-1].x - self.velocity * self.last_direction.x
        p.y = self.body[-1].y - self.velocity * self.last_direction.y
        self.body.append(p)
    
    def printBody(self):
        for i in self.body:
            print(f"PrintBody: {i.xy}")

    def colliding_wall(self):
        if (self.body[0].x < 0 or self.body[0].x >= self.screen_width):
            return True
        elif (self.body[0].y < 0 or self.body[0].y >= self.screen_height):
            return True
        
        return False
    
    def colliding_self(self):
        i = 0
        result = False
        for segment in self.body:
            if (self.body[0] == segment and i != 0):
                result = True
            i += 1
        return result
    
    def reset(self):
        self.body.clear()
        self.init()

    def x(self):
        return self.body[0].x
    
    def y(self):
        return self.body[0].y
    
    def x(self, index):
        return self.body[index].x
    
    def y(self, index):
        return self.body[index].y
    
    def get_size(self):
        return self.size
    
    def get_direction(self):
        return self.direction
    
    def check_danger(self, point: pg.math.Vector2):
        result = False
        if (point in self.body):
            result = True
        elif (point.x < 0):
            result = True
        elif (point.x > self.screen_width):
            result = True
        elif (point.y < 0):
            result = True
        elif (point.y > self.screen_height):
            result = True
        
        return result

    def check_wall(self, point: pg.math.Vector2):
        result = False
        if (point.x < 0):
            result = True
        elif (point.x >= self.screen_width):
            result = True
        elif (point.y < 0):
            result = True
        elif (point.y >= self.screen_height):
            result = True

        return result