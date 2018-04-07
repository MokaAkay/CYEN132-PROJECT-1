
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
        
        #Paddle(xPos, yPos, speed, team, isPlayer)
        #Ball(xPos, yPos, startingSpeed)
        paddle1 =Paddle(40, 4, 5, 1, True)
        paddle2 =Paddle(display_width-50, 20, 10, 2, False)
        ball = Ball(display_width/2, display_height/2, 1)
        entities_list = [paddle1, paddle2, ball]


#Param xPos, the initial x position of the paddle
#Param yPos, the initial y position of the paddle
#Param team, what side the paddle is on
#Param isPlayer if it is a player, will allow player input
# if not, AI will take control of the paddle
class Paddle(Entity):
    def __init__(self, xPos, yPos, speed, team, isPlayer):
        paddleImg=pygame.image.load("paddle.png")
        Entity.__init__(self, xPos, yPos, paddleImg)
        self.team = team
        self.isPlayer = isPlayer
        self.speed = speed

    #in this method the paddle will try to chase the ball at it's speed. It does this by comparing the location of the ball to the location of the paddle
    def chaseBall(self):
            #NOTE: the ball object is in global variable entities_list[2]
            mid_of_ball = (entities_list[2].yPos + entities_list[2].yPosEnd)/2
            mid_of_paddle = (self.yPos + self.yPosEnd)/2
            #if the center of the ball is lower or higher on the screen than the center of the paddle, the paddle will change its position by its speed every time this entity updates
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
        #if the paddle is not a player(human) it will take control of itself
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
        #converts the direction from degrees to radians
        radians = (6.28*self.direction)/360
        #converts the radians and speed to x and y components
        xSpeed = self.speed*math.cos(radians)
        ySpeed = self.speed*math.sin(radians)
        #updates the balls position
        self.xPos += xSpeed
        self.xPosEnd+=xSpeed
        self.yPos += ySpeed
        self.yPosEnd +=ySpeed

    def hitSide(self):
        #is called when at the top or bottom of the screen
        self.direction = 360-self.direction

    def hitPaddle(self, paddle):
        self.bounces += 1
        #for now just calls the hitside function. It would be better if the direction depended on where the ball hits the paddle
        self.hitSide()
        
    def update(self):
        #the behavior of the ball goes here
        #if the ball hits a paddle
        #TODO fix this. Im not really sure how to detect when the ball hits the paddle if someone wants to figure it out?
        #entities_list[0] is player 1's paddle and entities_list[2] is player 2's paddle
        if(self.xPos <= entities_list[0].xPos and entities_list[0].yPos - self.yPos > 0 and self.yPosEnd - entities_list[0].yPosEnd):
            self.hitPaddle(entities_list[0])
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
