
import pygame
import random
import math
from pygame.math import Vector2
import heapq

grid = Vector2(20,15)
grid_size = 20
size = grid * 20
FPS = 25

class fruit:
    
    def __init__(self,map_size):
        self.x_range = int(map_size.x)
        self.y_range = int(map_size.y)
        self.size = grid_size
        self.color = (150,200,0)
        self.move()
        
    def move(self):#used when the food is eaten
        
        x = random.randint(0, self.x_range - grid_size)
        x = math.floor(x / grid_size) * grid_size
        y = random.randint(0, self.y_range - grid_size)
        y = math.floor(y / grid_size) * grid_size
        
        self.pos = Vector2(x,y)
        
class snake:
    
    def __init__(self,map_size):
        
        self.size = grid_size
        self.body = []
        self.direction = Vector2(1,0)
        self.head_color = (150,200,200)
        self.body_color = (100,100,200)
        
        v = map_size / 2
        slen = 5 
        for i in range(slen):
            self.body.append(Vector2(round(v.x / self.size) * self.size, round(v.y / self.size) * self.size) - Vector2(self.size * i,0))
        
        self.grow = False
        self.last_element = []
    def move(self):
        #function responsible for growing and moving the snake
        if self.grow:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction * self.size)
            self.body = body_copy
            self.grow = False
        else:
            self.last_element = self.body[-1]
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction * self.size)
            self.body = body_copy
            
            
    def man_dist(self, point1, point2):
        #manhattan distance heuristic between point1 and point2 
        return abs(point1[0] - point2[0]) / 20 + abs(point1[1] - point2[1]) / 20
    
    
    def can_reach_tail(self, planned_path):
        # Step 1: Backup the original state
        original_body = self.body[:]
        original_direction = self.direction
    
        # Step 2: Create a simulated snake body from the original one
        simulated_body = self.body[:]
    
        # Step 3: Simulate the path by moving the snake along it
        for pos in planned_path:
            new_head = Vector2(pos)
            simulated_body.insert(0, new_head)  # Add new head
    
            if new_head == Vector2(planned_path[-1]):  # When the snake reaches the fruit (growth happens)
                break  # Don't remove the tail since the snake grows here
            else:
                simulated_body.pop()  # Simulate normal movement by removing the tail
    
        # Step 4: Prepare for DFS to check if the snake can reach its tail
        start = (int(simulated_body[0].x // grid_size), int(simulated_body[0].y // grid_size))
        tail = (int(simulated_body[-1].x // grid_size), int(simulated_body[-1].y // grid_size))
    
        snake_body_set = {(int(segment.x // grid_size), int(segment.y // grid_size)) for segment in simulated_body[:-1]}
    
        def bfs_reach_tail(self, start, tail, snake_body_set):
            """
            Simple Breadth-First Search to determine if there is a direct path from the head to the tail.
            Returns True if a path exists, otherwise False.
            """
            from collections import deque
            
            queue = deque([start])
            visited = set([start])
            
            while queue:
                current = queue.popleft()
                
                if current == tail:
                    return True
                
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    neighbor = (current[0] + dx, current[1] + dy)
                    
                    if (0 <= neighbor[0] < int(grid.x) and 0 <= neighbor[1] < int(grid.y)):
                        if neighbor not in visited and neighbor not in snake_body_set:
                            visited.add(neighbor)
                            queue.append(neighbor)
            
            return False
        
        if bfs_reach_tail(self, start, tail, snake_body_set):
            self.body = original_body
            self.direction = original_direction
            return True
        
        # Step 6: Restore original state
        self.body = original_body
        self.direction = original_direction
    
        return False
    
    def tail_chasing_mode(self):
        """
        This function is triggered when the snake finds a path to the fruit but cannot reach its tail from there.
        It ensures the snake stays alive by actively following its own tail until a safe path to the fruit becomes available.
        """
    
        # Step 1: Identify the current position of the snake's head and tail
        head = self.body[0]
        tail = self.last_element
    
        # Step 2: Use A* to find a path to the tail
        self.astar(head, tail, True)
        
    
            
    def astar(self,start,goal,tail_chasing = False):
        
        start = (start.x, start.y)
        goal = (goal.x, goal.y)
        
        if start == goal:#Assume this is for tail chasing!!!
            
            self.direction = - (Vector2(start) - Vector2(self.body[-1]) ) / 20
            self.planned_path = [tuple(self.direction * 20) + self.body[0]]
            for path in [(0, grid_size), (0, -grid_size), (grid_size, 0), (-grid_size, 0)]:
                part = Vector2(path) + self.body[0]
                self.planned_path = [part]
                if part == self.direction or self.is_obstacle(part):
                    continue
                if self.can_reach_tail(self.planned_path):
                    self.direction = Vector2(path) / 20
                    return
            self.planned_path = [tuple(self.direction * 20) + self.body[0]]
            return
        #priority queue for open set
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        #dictionary to store the most efficient steps
        came_from = {}
        
        #dictionary to store the distance cost
        g_score = {(x, y): float('inf') for x in range(int(grid.x)) for y in range(int(grid.y))}
        g_score[start] = 0
        
        #dictionary to store the estimated cost
        self.f_score = {(20 * x, 20 * y): float('inf') for x in range(int(grid.x)) for y in range(int(grid.y))}
        self.f_score[start] = self.man_dist(start, goal)
        open_set_hash = {start}
        
        while open_set:
            
            #get the node with the lowest f_score
            current_f, current = heapq.heappop(open_set)
            open_set_hash.remove(current)
            
            #if we are at goal, reconstruct and change direction
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                 
                path.append(start)
                self.planned_path = path[-2::-1]
                if len(path) > 1:
                    
                    if not self.can_reach_tail(self.planned_path):   
                        self.f_score[came_from[goal]] = float('inf')# Remove from list
                        for path in [(0, grid_size), (grid_size, 0), (0, -grid_size), (-grid_size, 0)]:
                            
                            space = tuple( Vector2(goal) + Vector2(path) )
                            if (0 <= space[0] < size.x and 0 <= space[1] < size.y 
                            and self.f_score[space] < float('inf') and space in came_from):
                                
                                came_from[goal] = space
                                heapq.heappush(open_set, (self.f_score[space] + 1, goal) )
                                open_set_hash.add(goal)
                                break
                        continue
                    self.direction = - (Vector2(start) - Vector2(path[-2]) ) / 20                    
                return
            
            #check all neighbors (4-directional movement)
            for dx, dy in [(0, grid_size), (grid_size, 0), (0, -grid_size), (-grid_size, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                #check if neighbor is valid (within grid and not a body part)
                if (0 <= neighbor[0] < size.x and 
                    0 <= neighbor[1] < size.y and 
                    not self.is_obstacle(neighbor)):
                    
                    #calculate tentative g_score
                    tentative_g_score = g_score[current] + 1  #movement cost increase
                    
                    #if there is a better path, update current path
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        #update the path
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        self.f_score[neighbor] = g_score[neighbor] + self.man_dist(neighbor, goal)
                        
                        #add to open set if not already there
                        if neighbor not in open_set_hash:
                            heapq.heappush(open_set, (self.f_score[neighbor], neighbor))
                            open_set_hash.add(neighbor)
        
        if not tail_chasing:
            self.tail_chasing_mode()
    
        
    def is_obstacle(self, position):
        #check if a position contains a snake body
        
        #create a rectangle for position with its coordinates
        pos_rect = pygame.Rect(position[0], position[1], grid_size, grid_size)
        
        #check collision with snake body (except the head)
        for segment in self.body[1:]:
            if pos_rect.colliderect(pygame.Rect(segment.x, segment.y, grid_size, grid_size)):
                return True
            
        return False

main_fruit = fruit(size)
pygame.init()

#game variables
screen = pygame.display.set_mode((size[0], size[1]))
pygame.display.set_caption("Yavaş Aracı Yılan Oyunu")
score_font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 11)
score = 0

#ai snake initialization
snAIke = snake(size)

#main game loop
running = True
paused = False  # Added variable to keep track of the game state
debugged = False
counter = 0
while running:
    
    #initialize fruit variable
    froot = pygame.Rect(main_fruit.pos.x,main_fruit.pos.y,main_fruit.size,main_fruit.size)
    
    #fill the screen with dark blue
    screen.fill((25, 0, 75))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #quit the game
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused  # Toggle pause state
                debugged = False
            if event.key == pygame.K_UP:
                FPS = 120
                print("FPS increased to", FPS)
            elif event.key == pygame.K_DOWN:
                FPS = 20
                print("FPS decreased to", FPS)      
    if paused:
        if debugged == True:
            continue
        fruit = pygame.draw.rect(screen, main_fruit.color, froot)
        
        
        #initialize snake head
        head_rect = pygame.Rect(snAIke.body[0].x, snAIke.body[0].y, snAIke.size, snAIke.size)
        
        #draw the snake head and body
        pygame.draw.rect(screen, snAIke.head_color, head_rect)
        segments = []
        for segment in snAIke.body[1:]:
            segment_rect = pygame.Rect(segment.x, segment.y, snAIke.size, snAIke.size)
            pygame.draw.rect(screen, snAIke.body_color, segment_rect)
            segments.append(segment_rect)
        
        for pos, weight in snAIke.f_score.items():
            if weight < float('inf'):
                text_surface = small_font.render(str(round(weight, 1)), True, (255, 255, 255))
                screen.blit(text_surface, (pos[0] + 2, pos[1] + 2))
                pygame.display.flip()
                pygame.time.Clock().tick(FPS)
        debugged = True
        continue
    
         
    #draw fruit in game
    fruit = pygame.draw.rect(screen, main_fruit.color, froot)
    
    
    #initialize snake head
    head_rect = pygame.Rect(snAIke.body[0].x, snAIke.body[0].y, snAIke.size, snAIke.size)
    
    #draw the snake head and body
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
    
    #move the snake
    if fruit.colliderect(head_rect):
        while fruit.collidelist(segments) >= 0 or fruit.colliderect(head_rect):
            #spawn the fruit where no collision occurs
            main_fruit.move()
            froot = pygame.Rect(main_fruit.pos.x,main_fruit.pos.y,main_fruit.size,main_fruit.size)
            fruit = pygame.draw.rect(screen, main_fruit.color, froot)
            
        #increase score and snake size
        score += 1
        snAIke.grow = True
    
    
    
    #move the snake according to the A* algorithm
    snAIke.astar(snAIke.body[0], main_fruit.pos)
    
    if snAIke.planned_path:
        for pos in snAIke.planned_path:
            # Convert grid/pixel positions if needed; here we assume each pos is a tuple (x, y)
            pygame.draw.circle(screen, (255, 255, 255), (int(pos[0]) + grid_size/2, int(pos[1]) + grid_size/2), 3)
    
    #print(snAIke.body[len(snAIke.body) - 1])
    snAIke.move()
    
    #render score as cyan
    score_text = score_font.render("Score: " + str(score), True, (0, 255, 255))
    
    #update text display
    text_rect = score_text.get_rect(topright=(size[0] - 10, 10))
    screen.blit(score_text, text_rect)
    
    counter += 1
    #update game screen and clock
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)
    
#clean up and quit pygame
print("game over. Score:",score, counter)
pygame.quit()