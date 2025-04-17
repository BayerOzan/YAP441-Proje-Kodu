import pygame
import random
import math
from pygame.math import Vector2
import heapq

grid = Vector2(20,15)
grid_size = 20
size = grid * 20
FPS = 40

class fruit:
    
    def __init__(self,map_size):
        self.x_range = int(map_size.x)
        self.y_range = int(map_size.y)
        self.size = grid_size
        self.type = "food"
        self.color = (150,200,0)
        self.move()
        
    def move(self):
        
        x = random.randint(0, self.x_range - grid_size)
        x = math.floor(x / grid_size) * grid_size
        y = random.randint(0, self.y_range - grid_size)
        y = math.floor(y / grid_size) * grid_size
        self.pos = Vector2(x,y)
class snake:
    #snake has the full body
    def __init__(self,map_size):
        v = map_size / 2 
        self.size = grid_size 
        self.type = "snake"
        self.body = [] # Base length of 3
        self.direction = Vector2(1,0)
        self.head_color = (150,200,200)
        self.body_color = (100,100,200)
        slen = 5
        for i in range(slen):
            self.body.append(Vector2(round(v.x / self.size) * self.size, round(v.y / self.size) * self.size) - Vector2(self.size * i,0))
        self.grow = False
    def move(self):
        if self.grow:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction * self.size)
            self.body = body_copy
            self.grow = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction * self.size)
            self.body = body_copy
    def man_dist(self, point1, point2):
        #manhattan distance heuristic between point1 and point2 
        return abs(point1[0] - point2[0]) / 20 + abs(point1[1] - point2[1]) / 20
    def astar(self,start,goal):
        
        start = (start.x, start.y)
        goal = (goal.x, goal.y)
        
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        
        g_score = {(x, y): float('inf') for x in range(int(grid.x)) for y in range(int(grid.y))}
        g_score[start] = 0
        
        # This stores f scores of all cells initialized as infinite
        f_score = {(x, y): float('inf') for x in range(int(grid.x)) for y in range(int(grid.y))}
        f_score[start] = self.man_dist(start, goal)
        open_set_hash = {start}
        
        while open_set:
            # Get  lowest f score
            current_f, current = heapq.heappop(open_set)
            open_set_hash.remove(current)
            
            # If goal is reached, reconstruct and return the path
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                # Reverse path from start to goal
                path.append(start)
                if len(path) > 1:
                    self.direction = - (Vector2(start) - Vector2(path[-2]) ) / 20 
                    
                return
            
            # Check all neighbors
            for dx, dy in [(0, grid_size), (grid_size, 0), (0, -grid_size), (-grid_size, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Check if neighbor is valid 
                if (0 <= neighbor[0] < size.x and 
                    0 <= neighbor[1] < size.y and 
                    not self.is_obstacle(neighbor)):
                    
                    # Calculate tentative g_score
                    tentative_g_score = g_score[current] + grid_size  # Cost is grid_size
                    
                    # If we found a better path to this neighbor
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        # Update the path
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + self.man_dist(neighbor, goal)
                        
                        # Add to open set if not already there
                        if neighbor not in open_set_hash:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
                            open_set_hash.add(neighbor)
            
        # If we get here, algorithm does not work
        return 
        
    def is_obstacle(self, position):
        """Check if a position contains an obstacle (wall or snake body)"""
        # Create a rectangle for position
        pos_rect = pygame.Rect(position[0], position[1], grid_size, grid_size)
        
        # Check collision with snake body except head
        for segment in self.body[1:]:
            if pos_rect.colliderect(pygame.Rect(segment.x, segment.y, grid_size, grid_size)):
                return True
                
        # Check if position is out of bounds
        if (position[0] < 0 or position[0] >= size.x or 
            position[1] < 0 or position[1] >= size.y):
            return True
            
        return False
main_fruit = fruit(size)
pygame.init()

screen = pygame.display.set_mode((size[0], size[1]))
pygame.display.set_caption("Sade A* Yılan Oyunu")
score = 0
score_font = pygame.font.SysFont("Arial", 20)
snAIke = snake(size)

running = True
counter = 0
while running:
    
    froot = pygame.Rect(main_fruit.pos.x,main_fruit.pos.y,main_fruit.size,main_fruit.size)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill((25, 0, 75))
    score_text = score_font.render("Score: " + str(score), True, (0, 255, 255))
    
    # Update text display
    text_rect = score_text.get_rect(topright=(size[0] - 10, 10))
    screen.blit(score_text, text_rect)
        
    #spawn fruit
    fruit = pygame.draw.rect(screen, main_fruit.color, froot)
    
    # Move the snake head
    head_rect = pygame.Rect(snAIke.body[0].x, snAIke.body[0].y, snAIke.size, snAIke.size)
    
    # Draw the snake body and head with different colors
    pygame.draw.rect(screen, snAIke.head_color, head_rect)
    segments = []
    for segment in snAIke.body[1:]:
        segment_rect = pygame.Rect(segment.x, segment.y, snAIke.size, snAIke.size)
        pygame.draw.rect(screen, snAIke.body_color, segment_rect)
        segments.append(segment_rect)
        
    #game over conditions
    if ( not 0 <= head_rect.x < size.x ) or ( not 0 <= head_rect.y < size.y ) or \
    head_rect.collidelist(segments) >= 0 :
        running = False
        
    if fruit.colliderect(head_rect):
        while fruit.collidelist(segments) >= 0 or fruit.colliderect(head_rect):
            main_fruit.move()
            froot = pygame.Rect(main_fruit.pos.x,main_fruit.pos.y,main_fruit.size,main_fruit.size)
            fruit = pygame.draw.rect(screen, main_fruit.color, froot)
        
        
        
        snAIke.grow = True
        score += 1
    counter += 1
    snAIke.astar(snAIke.body[0], main_fruit.pos)
    snAIke.move()
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)
    
print("game over. Score:",score, counter)    
pygame.quit()
