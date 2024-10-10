import pygame
import random
import math
from pygame.locals import *


## SPACE SHOOTER!  V 0.001 ##
#
#
# A scrolling space shooter game

pygame.init()

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1400

MOVE_SIZE = 7

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
my_font = pygame.font.Font(None, 40)

pygame.display.flip()

# Initialization of the game
screen.fill((5, 5, 5))
pygame.display.flip()

  
# set the image which to be displayed on screen 
SPACE_SHIP_IMG = pygame.image.load('images/space_ship.png') 
ASTEROID01_IMG = pygame.image.load('images/asteroid01.png')
ASTEROIDEXPLODE01_IMG = pygame.image.load('images/asteroidExplode01.png')
SPACE_BACKGROUND_IMG = pygame.image.load('images/space_background.png')
START_SCREEN_IMG = pygame.image.load('images/start01.png')


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
    
    def is_hit(self, asteroid):
        #WRITE collision code here...
        if ((self.loc.x > asteroid.loc.x and 
             self.loc.x < asteroid.loc.x+50) and 
             (self.loc.y > asteroid.loc.y - 50 and
              self.loc.y < asteroid.loc.y)):             
            print("write me... is_hit")
            asteroid.image = ASTEROIDEXPLODE01_IMG
            return True
        
        
    def move(self, ship):
        self.old_loc = Coordinate(self.loc.x, self.loc.y)
        self.loc = Coordinate(self.loc.x, self.loc.y - LASER_SPEED)        

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
    shooting = False
    points=0
    def draw(self, screen):
        self.clear_old_images(screen)
        self.draw_lasers(screen)
        self.draw_ship(screen)
        self.draw_score(screen)
        if self.shooting == True:
            self.shoot()
        
    def draw_ship(self, screen):       
        screen.blit(SPACE_SHIP_IMG, (self.x, SHIP_Y_POSITION))
        
    def draw_lasers(self, screen):
        for a_laser in self.lasers:
            a_laser.draw(screen)
            for asteroid in asteroid_list:
                if a_laser.is_hit(asteroid):
                    self.points = self.points + 1
                    print("HIT!")
                    print('i have ' + str(self.points))
                    
                    
    def draw_score(self, screen):
        #do stuff
        color = (0, 155, 0) #Green
        text = "Score " + str(self.points)
        
        #def draw_text_color(self, screen, text, loc, color):
        text_surface = my_font.render(text, False, color)
        screen.blit(text_surface, (0, 0))
                
    
    def clear_old_images(self, screen):
        if self.last_x != None:
            pygame.draw.rect(screen, (5, 5, 5), 
                 pygame.Rect(self.last_x, SHIP_Y_POSITION, SIZE,SIZE))
            self.last_x = None
            
    def shoot(self):
        #maybe draw muzzle blast?
        #maybe sound?
        if len(self.lasers) < 50:
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
        if self.is_off_screen():
          #remove from the game
          asteroid_list.remove(self)
        
    def is_off_screen(self):
        #ToDo
        return (self.loc.x > SCREEN_WIDTH+10 or
                self.loc.x < -10 or
                self.loc.y > SCREEN_HEIGHT or
                self.loc.y < -10)
        

#Start Screen

print("start screen....")
screen.fill((5, 5, 5))




class Button:
    label:'none'
    loc: None  #Coordinate of the top left corner of this button
    
    
    def __init__(self, the_label, the_loc):
        self.label = the_label
        self.loc = the_loc
        
    
    def draw(self, screen):
        button_color = (30,130,130) #purple
        pygame.draw.rect(screen, button_color, (self.loc.x, self.loc.y, self.loc.x + 200, self.loc.y + 50))
        
        color = (0, 0,0) #Black
        
        #def draw_text_color(self, screen, text, loc, color):
        text_surface = my_font.render(self.label, False, color)
        screen.blit(text_surface, (self.loc.x + 10, self.loc.y+10))
        
    def is_clicked(self, mouseloc):
            return mouseloc.x >= self.loc.x and mouseloc.x <= self.loc.x + 200 and mouseloc.y >= self.loc.y and mouseloc.y <= self.loc.y + 50
            
  
        
start_game_button = Button('Start Game!', Coordinate(0, 0))

screen.blit(START_SCREEN_IMG, (0,0))
start_game_button.draw(screen)
print("start screen rendered?...")        
pygame.display.update()

awesome_button = Button('awesome mode!!!!!',Coordinate(1000,0))

awesome_button.draw(screen)
print("awesome mode screen rendered?...")        
pygame.display.update()

awesome_mode = False
starting_game = True
while starting_game:
    
    for event in pygame.event.get():

        if awesome_mode:
            awesome_text = my_font.render('AWESOME MODE!', False, (55,55,55))
            screen.blit(awesome_text, (50, 50))   
            pygame.display.update()
            
            
        
        # Close window event
        if event.type == QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_loc = Coordinate(event.pos[0],event.pos[1])
            if start_game_button.is_clicked(mouse_loc):
                starting_game = False
            if awesome_button.is_clicked(mouse_loc):
                awesome_mode = True 
                #continue to the regular game loop below
        
print('is it awesome mode? ' + str(awesome_mode))
    
player = SpaceShip()
asteroid_list = [ Asteroid(50,50),  Asteroid(SCREEN_WIDTH/2, 50),  Asteroid(SCREEN_WIDTH-50, 50)]

background_pos = 0
#if False:
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
                player.shooting = True
                print('bang')
        elif event.type == KEYUP and event.key == K_SPACE:
            player.shooting = False
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                player.direction = None
            
           


    
    # Clear the screen for this render cycle
        
           
    if len(asteroid_list) < 50:
      asteroid_list.append(Asteroid(random.randrange(0,SCREEN_WIDTH), 5))
    
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
