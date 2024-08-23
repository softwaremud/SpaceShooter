import pygame
import random
import math
from pygame.locals import *


## SPACE SHOOTER!  V 0.001 ##
#
#
# A scrolling space shooter game


SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1400

MOVE_SIZE = 7

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

# Initialization of the game
screen.fill((5, 5, 5))
pygame.display.flip()

  
# set the image which to be displayed on screen 
SPACE_SHIP_IMG = pygame.image.load('images/space_ship.png') 
ASTEROID01_IMG = pygame.image.load('images/asteroid01.png')
SPACE_BACKGROUND_IMG = pygame.image.load('images/space_background.png')


# Set the size for the image
SIZE = 50  #50 is the default, but it is a bit choppy/big
DEFAULT_IMAGE_SIZE = (SIZE, SIZE)
START_LOCATION = (150, SCREEN_WIDTH/2)


def scale_to_game(image):
    return pygame.transform.scale(image, (SIZE, SIZE))



# Scale the image to your needed size
if SIZE != 50:
    space_ship_img = scale_to_game(space_ship_img)

class Coordinate:
    x = 0
    y = 0
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

LASER_SPEED = 25

class Laser:
    loc = 0
    old_loc = 0
    color = (255, 10,10) #"red"
    def __init__(self, x, y):
        self.loc = Coordinate(x, y)
        self.old_loc = Coordinate(x,y)
    
    def is_hit(asteroid):
        #WRITE collision code here...
        print("write me... is_hit")
        
    def move(self, ship):
        self.old_loc = Coordinate(self.loc.x, self.loc.y)
        self.loc = Coordinate(self.loc.x, self.loc.y - LASER_SPEED)        
        #ToDo: incorporate laser aserteroid collision detection here...
        
        
        #Laser is off-screen
        if self.loc.y < -100:
            ship.lasers.remove(self)
            
    def draw(self, screen):
        #clear-old left
        pygame.draw.rect(screen, (5,5,5), 
                 pygame.Rect(self.old_loc.x+10, self.old_loc.y, 2,20))
        #clear-old right
        pygame.draw.rect(screen, (5,5,5), 
                 pygame.Rect(self.old_loc.x+40, self.old_loc.y, 2,20))
        
        #draw left
        pygame.draw.rect(screen, self.color, 
                 pygame.Rect(self.loc.x+10, self.loc.y, 2,20))
        #draw right
        pygame.draw.rect(screen, self.color, 
                 pygame.Rect(self.loc.x+40, self.loc.y, 2,20))
        
        
    
SHIP_Y_POSITION = SCREEN_HEIGHT - 150

# In scrolling space games, the ship is always in the same "Y" spot
# and the world moves around the ship.
class SpaceShip:
    x = SCREEN_WIDTH/2
    last_x = None
    direction = None
    lasers = []
    def draw(self, screen):
        self.clear_old_images(screen)
        self.draw_lasers(screen)
        self.draw_ship(screen)
        
    def draw_ship(self, screen):       
        screen.blit(SPACE_SHIP_IMG, (self.x, SHIP_Y_POSITION))
        
    def draw_lasers(self, screen):
        for a_laser in self.lasers:
            a_laser.draw(screen)
            
    
    def clear_old_images(self, screen):
        if self.last_x != None:
            pygame.draw.rect(screen, (5, 5, 5), 
                 pygame.Rect(self.last_x, SHIP_Y_POSITION, SIZE,SIZE))
            self.last_x = None
            
    def shoot(self):
        #maybe draw muzzle blast?
        #maybe sound?
        self.lasers.append(Laser(self.x, SHIP_Y_POSITION))
        
    def move(self):
        self.last_x = self.x
        if self.direction == "left":
            self.x = self.x - MOVE_SIZE
        elif self.direction == "right":
            self.x = self.x + MOVE_SIZE
        for a_laser in self.lasers:
            a_laser.move(self)
        

class Vector:
    direction = 0 #A degree where the top of the screen is 0 degrees
    speed = 0
    next_x = 0.00
    next_y =  0.00
    def __init__(self, speed, dir):
        self.speed = speed
        self.direction = dir
        self.next_x = math.cos(dir) * self.speed
        self.next_y = math.sin(dir) * self.speed
        
    # given coordinates, return next coordinates
    def next(self, x, y):
        return Coordinate(x + self.next_x, y + self.next_y)
        

#Asteroids in our Space Shooter
class Asteroid:
    loc = Coordinate(0, 0)
    last_loc = None
    direction = None
    image = None
    def __init__(self, x_pos, y_pos):
        self.loc = Coordinate(x_pos, y_pos)
        self.last_loc = Coordinate(x_pos, y_pos)
        self.direction = Vector(random.randrange(1,15), random.randrange(0, 360))
        self.image = ASTEROID01_IMG
        

    def draw(self, screen):
        a_rect = pygame.Rect(self.last_loc.x, self.last_loc.y, SIZE, SIZE)
        pygame.draw.rect(screen, (5, 5, 5), a_rect)
        screen.blit(self.image, (self.loc.x, self.loc.y))
        

    def move(self):
        self.last_loc = Coordinate(self.loc.x, self.loc.y)
        self.loc = self.direction.next(self.loc.x, self.loc.y)
        
    def is_off_screen(self):
        #ToDo
        print("todo")
    
    
player = SpaceShip()
asteroid_list = [ Asteroid(50,50),  Asteroid(SCREEN_WIDTH/2, 50),  Asteroid(SCREEN_WIDTH-50, 50)]

background_pos = 0

# Snf%ake Game animation loop
while True:
    
    
    #screen.fill((5, 5, 5))
    for event in pygame.event.get():
        # Close window event
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        #elif event.type == KEYDOWN and event.key == K_DOWN: 
        #elif event.type == KEYUP and event.key == K_UP:
        elif event.type == KEYDOWN and event.key == K_LEFT:
                player.direction = "left"
        elif event.type == KEYDOWN and event.key == K_RIGHT:
                player.direction = "right"
        elif event.type == KEYDOWN and event.key == K_SPACE:
                player.shoot()
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                player.direction = None
            
                

    
    # Clear the screen for this render cycle
        
            
    
    player.move()
        
    pygame.display.update()    
    for rock in asteroid_list:
        rock.move()
        
        
        
    background_pos = background_pos + 8
    #if background_pos % 10 == 0:
        #move background
    screen.blit(SPACE_BACKGROUND_IMG, (0,  background_pos - (4000-SCREEN_HEIGHT)))
    if background_pos % (4000-SCREEN_HEIGHT) == 0:
       #scroll after we hit the edge of the size to restart
       background_pos = 0
    for rock in asteroid_list:
        rock.draw(screen)
    player.draw(screen)
        
    pygame.display.flip()