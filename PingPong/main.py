
import pygame
from random import randint
import math

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
        #xPos is the left of the entity
        #yPos is the top of the entity
        #xPosEnd is the right of the entity
        #yPosEnd is the bottom of the entity
        #xPosEnd and yPosEnd are untested I may have gotten these values incorrectly.
        self.xPos = xPos
        self.yPos = yPos
        self.xPosEnd = xPos+pygameImage.get_rect().bottomright[0]
        self.yPosEnd = yPos+pygameImage.get_rect().bottomleft[1]
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
        #change "true" to "false" if you want the paddle to be an AI
        entities_list = [Paddle(40, 10, 1, True), Paddle(display_width-50, 20, 2, False), Ball(display_width/2, display_height/2, 1)]


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


    def chaseBall(self):
            mid_of_ball = (entities_list[2].yPos + entities_list[2].yPosEnd)/2
            mid_of_paddle = (self.yPos + self.yPosEnd)/2
            if (mid_of_ball > mid_of_paddle):
                if self.yPosEnd<display_height:
                    self.yPos+=self.speed
                    self.yPosEnd += self.speed
            elif (mid_of_ball < mid_of_paddle):
                if self.yPos>=0:
                    self.yPos-=self.speed
                    self.yPosEnd -= self.speed
                
    def update(self):
        #TODO paddles shouldn't be able to go off screen
        if (self.isPlayer):
            if (self.team == 1):
                #Player 1 input goes here
                #This stuff is for now, later we will use GPIO input instead with switches
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if self.yPosEnd<display_height:
                            self.yPos +=self.speed
                            self.yPosEnd += self.speed
                    elif event.key == pygame.K_w:
                        if self.yPos>=0:
                            self.yPos -= self.speed
                            self.yPosEnd -= self.speed
            if (self.team == 2):
                #Player 1 input goes here
                #if up is held, decrease the y position by speed
                #if down is held, decrease the y position by speed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if self.yPosEnd<display_height:
                            self.yPos +=self.speed
                            self.yPosEnd += self.speed
                    elif event.key == pygame.K_UP:
                        if self.yPos>=0:
                            self.yPos -= self.speed
                            self.yPosEnd -= self.speed
        if (not self.isPlayer):
            self.chaseBall()

        

class Ball(Entity):
    def __init__(self, xPos, yPos, startingSpeed):
        ballImg=pygame.image.load('ball.png')
        Entity.__init__(self, xPos, yPos, ballImg)
        self.speed = startingSpeed
        #the number of times the ball has hit a paddle
        self.bounces=0
        self.direction = randint(0,360)

    
        
    #proceeds in the direction it's currently heading
    def go(self):
        radians = (6.28*self.direction)/360
        xSpeed = self.speed*math.cos(radians)
        ySpeed = self.speed*math.sin(radians)
        self.xPos += xSpeed
        self.xPosEnd+=xSpeed
        self.yPos += ySpeed
        self.yPosEnd +=ySpeed

    def hitSide(self):
        self.direction = 360-self.direction
        
    def update(self):
        #the behavior of the ball goes here
        #if the ball hits a paddle
        #every time the ball bounces x number of times, increase speed
        #ball bounces off walls
        if (self.yPosEnd>=display_height or self.yPos <=0):
            self.hitSide()
        self.go()
        

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
