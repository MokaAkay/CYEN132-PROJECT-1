
import pygame
from random import randint

display_width = 800
display_height = 600
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pong!')
clock = pygame.time.Clock()
crashed = False

#The entities list manages all of the entities that currently exist in the gamestate.
entities_list = []


#THE ENTITY CLASS IS DONE. DON'T CHANGE THIS (unless you want to try to implement animations for each of the sprites.)
class Entity(object):
    def __init__(self, xPos, yPos, pygameImage):
        self.xPos = xPos
        self.yPos = yPos
        self.pygameImage = pygameImage
    #update is the BEHAVIOR of the entity. It is implemented in the entities subclass. it will raise NotImplementedError if it is not implemented in a subclass of entity
    def update(self):
        raise NotImplementedError()
    
    #render displays the entity's image to the screen
    def render(self):
        gameDisplay.blit(self.pygameImage,(self.xPos,self.yPos))

        
class GameState(object):
    def __init__(self): # background, music):
        pass
        #delete current entities
        #set background image
        #set music

    def updateEntities(self):
        for entity in entities_list:
            entity.update()

    def renderEntities(self):
        print (entities_list)
        for entity in entities_list:
            entity.render()

class MainMenu(GameState):
    pass



#PONG GAME IMPLEMENTATION
class PongGame(GameState):
    def __init__(self):
        GameState.__init__(self)
        #inherit from Gamestate class with music and background image
        
        global entities_list
        #TODO ask if 1 player or 2 players

        #adds all of the required entities to the entities list
        entities_list = [Paddle(20, 10, 1, True), Paddle(display_width-20, 20, 2, True), Ball(display_width/2, display_height/2, 4)]


#Param xPos, the initial x position of the paddle
#Param yPos, the initial y position of the paddle
#Param team, what side the paddle is on
#Param isPlayer if it is a player, will allow player input
# if not, AI will take control of the paddle
class Paddle(Entity):
    def __init__(self, xPos, yPos, team, isPlayer):
        paddleImg=pygame.image.load("paddle.png")
        Entity.__init__(self, xPos, yPos, paddleImg)
        self.team = team
        self.isPlayer = isPlayer
        self.speed = 10
    def update(self):
        #TODO paddles shouldn't be able to go off screen
        if (self.isPlayer):
            if (self.team == 1):
                #Player 1 input goes here
                #This stuff is for now, later we will use GPIO input instead with switches
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.yPos +=self.speed
                    elif event.key == pygame.K_UP:
                        self.yPos -= self.speed
            if (self.team == 2):
                pass
                #Player 1 input goes here
                #if up is held, decrease the y position by speed
                #if down is held, decrease the y position by speed
        if (not self.isPlayer):
            pass
            #Paddle AI goes here
            #paddle AI will "Chase" the ball's Y position

        

class Ball(Entity):
    def __init__(self, xPos, yPos, startingSpeed):
        ballImg=pygame.image.load('ball.png')
        Entity.__init__(self, xPos, yPos, ballImg)
        self.speed = startingSpeed
        #the number of times the ball has hit a paddle
        self.bounces=0
        self.direction = randint(0,360)

    def update(self):
        pass
        #the behavior of the ball goes here
        #if the ball hits a paddle
        #every time the ball bounces x number of times, increase speed
        #ball bounces off walls
        

######################################
# MAIN PART OF THE PROGRAM
######################################

game = PongGame()
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        print(event)
    gameDisplay.fill((0,0,0))
    #updates all the entity behaviors
    game.updateEntities()
    #renders the entities to the screen
    game.renderEntities()
    pygame.display.update()
    clock.tick(60)
pygame.quit
quit()
