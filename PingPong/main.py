
import pygame
from random import randint
import math

pygame.init()
display_width = 800
display_height = 600
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pong!')
clock = pygame.time.Clock()
crashed = False

display_width = 800
display_height = 600
 
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

#dictionaries for the 2 sets of LEDs
P1LED = {17 : 1, 16 : 2, 13: 3, 12 : 4, 6 : 5}
P2LED = {18 : 1, 19 : 2, 20 : 3, 21 : 4, 22 : 5}


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
        self.xPos = float(xPos)
        self.yPos = float(yPos)
        self.xPosEnd = float(xPos+pygameImage.get_rect().bottomright[0])
        self.yPosEnd = float(yPos+pygameImage.get_rect().bottomleft[1])
        self.pygameImage = pygameImage
    #update is the BEHAVIOR of the entity. It is implemented in the entities subclass. it will raise NotImplementedError if it is not implemented in a subclass of entity
    def update(self):
        raise NotImplementedError()
    
    #render displays the entity's image to the screen
    def render(self):
        gameDisplay.blit(self.pygameImage,(self.xPos,self.yPos))

        
class GameState(object):
    def __init__(self): # background, music):
        global entities_list
        entities_list = []

        
    def update(self):
        raise NotImplementedError()


class MainMenu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.bg = pygame.image.load("intro_bg.png")
        self.currentScreen = 0
    def start_screen(self):
        if (self.currentScreen == 0):
            self.button("Start",150,450,100,50,green,bright_green,self.playerSelection)
            self.button("Exit",550,450,100,50,red,bright_red,self.quitgame)
        elif (self.currentScreen == 1):
            self.button("Only AI", 150, 200, 100, 50, green, bright_green, self.startPong, 0)
            self.button("One Player", 150, 300, 100, 50, green, bright_green, self.startPong, 1)
            self.button("Two Player", 150, 400, 100, 50, green, bright_green, self.startPong,2)

    def end_screen(self):
        if (self.currentScreen == 2):
            self.bg = pygame.image.load("win.png")
            self.button("Main Menu", 150,450,100,50,red,bright_red, self.MainMenu)
            self.button("Quit", 550, 450, 100, 50, red, bright_red, self.quitgame)
        elif (self.currentScreen == 3):
            self.bg = pygame.image.load("lose.png")
            self.button("Main Menu", 150,450,100,50,red,bright_red, self.MainMenu)
            self.button("Quit", 550, 450, 100, 50, red, bright_red, self.quitgame)

    def playerSelection(self):
        self.currentScreen = 1

    def playerWins(self):                
        self.currentScreen = 2

    def playerLoses(self):
        self.currentScreen = 3

    def startPong(self, args):
        #THIS IS WHERE I ENDED. WILL CONTINUE LATER
        global game
        game = PongGame(args)

    def button(self, msg, x, y, w, h, ic, ac, action = None, *args):
        mouse = pygame.mouse.get_pos() #allows for mouse interaction 
        click = pygame.mouse.get_pressed()
        # this is for interaction with the mouse
        # when the mouse hovers over a button it redraws the button with a different
        # color to show that it is selected
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

            if click[0] == 1 and action != None:
                action(*args)         
        else:
            pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

        smallText = pygame.font.SysFont("freesansbold.ttf",20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        gameDisplay.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
    
    def start_pong(self):
        global game
        game = PongGame()
        
    def quitgame(self):
        print ("quit");
        
    def update(self):
        gameDisplay.fill(white)
        gameDisplay.blit(self.bg,(0,0))
        self.start_screen()


#PONG GAME IMPLEMENTATION
class PongGame(GameState):
    def __init__(self, numPlayers):
        GameState.__init__(self)
        self.bg = pygame.image.load("background.png")
        self.isPaused = False
        self.pauseHandler = False
        #inherit from Gamestate class with music and background image
        
        global entities_list
        #TODO ask if 1 player or 2 players
        paddleOneIsPlayer=False
        paddleTwoIsPlayer=False
        if (numPlayers==1):
            paddleOneIsPlayer = True
        elif (numPlayers == 2):
            paddleOneIsPlayer = True
            paddleTwoIsPlayer = True
        #adds all of the required entities to the entities list
        #change "true" to "false" if you want the paddle to be an AI
        
        #Paddle(xPos, yPos, speed, team, isPlayer)
        #Ball(xPos, yPos, startingSpeed)
        paddle1 =Paddle(40, 4, 5, 1, paddleOneIsPlayer)
        paddle2 =Paddle(display_width-50, 20, 10, 2, paddleTwoIsPlayer)
        ball = Ball(display_width/2, display_height/2, 4)
        heart1 =Heart(60, 5, 5)
        heart2 =Heart(display_width-120, 5, 5)
        entities_list = [paddle1, paddle2, ball, heart1, heart2]

    def updateEntities(self):
        for entity in entities_list:
            entity.update()

    def renderEntities(self):
        for entity in entities_list:
            entity.render()
        
    def update(self):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if (self.pauseHandler == False):
                self.pauseHandler = True
                if self.isPaused:
                    self.isPaused = False
                else:
                    self.isPaused = True
        else:
            self.pauseHandler = False
        if (not self.isPaused):
            gameDisplay.fill(white)
            gameDisplay.blit(self.bg,(0,0))
            self.updateEntities()
            self.renderEntities()
        

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

class Heart(Entity):
    def __init__(self, xPos, yPos, lives):
        heartImg = pygame.image.load('heart.png')
        Entity.__init__(self, xPos, yPos, heartImg)
        self.lives = 5

    def update(self):
        pass

        

class Ball(Entity):
    def __init__(self, xPos, yPos, startingSpeed):
        ballImg=pygame.image.load('ball.png')
        Entity.__init__(self, xPos, yPos, ballImg)
        self.startingSpeed = startingSpeed
        self.speed = startingSpeed
        #the number of times the ball has hit a paddle
        self.bounces=0
        self.direction = randint(0,360)
        radians = (6.28*self.direction)/360
        self.xSpeed = self.speed*math.cos(radians)
        self.ySpeed = self.speed*math.sin(radians)
    
        
    #proceeds in the direction it's currently heading
    def go(self):
        #updates the balls position
        self.xPos += self.xSpeed
        self.xPosEnd+=self.xSpeed
        self.yPos += self.ySpeed
        self.yPosEnd +=self.ySpeed
        
    def calculateComponentSpeeds(self):
        radians = (6.28*self.direction)/360
        self.xSpeed = self.speed*math.cos(radians)
        self.ySpeed = self.speed*math.sin(radians)
    
    def hitSide(self):
        #is called when at the top or bottom of the screen
        #changes direction
        self.direction = 360-self.direction
        #recalculates the x and y speed
        self.calculateComponentSpeeds()

    def hitEnd(self):
        if self.xPos <= 0 or self.xPosEnd >= display_width:
                self.__init__(display_width/2, display_height/2,self.startingSpeed)#reset ball
                # score point to be added later #

    def hitPaddleDefault(self):
        self.direction = 180-self.direction
        self.calculateComponentSpeeds()

    def hitPaddle(self, paddle):
        self.bounces += 1
        #for now just calls the hitside function. It would be better if the direction depended on where the ball hits the paddle
        self.hitPaddleDefault()

        if (self.bounces % 5 == 0):
            self.speed +=2

        self.calculateComponentSpeeds()
        
    def update(self):
        #the behavior of the ball goes here
        #if the ball hits a paddle
        #entities_list[0] is player 1's paddle and entities_list[1] is player 2's paddle
        if(self.xPos <= entities_list[0].xPosEnd and entities_list[0].yPos <= self.yPos and self.yPosEnd <= entities_list[0].yPosEnd):
            self.hitPaddle(entities_list[0])

        if(self.xPosEnd >= entities_list[1].xPos and entities_list[1].yPos <= self.yPos and self.yPosEnd <= entities_list[1].yPosEnd):
            self.hitPaddle(entities_list[1])

        #every time the ball bounces x number of times, increase speed
        self.hitEnd()
        #ball bounces off walls
        if (self.yPosEnd>=display_height or self.yPos <=0):
            self.hitSide()
        self.go()
        

######################################
# MAIN PART OF THE PROGRAM
######################################

game = MainMenu()
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        #print(event)
    #updates all the entity behaviors
    game.update()
    pygame.display.update()
    clock.tick(60)
pygame.quit
quit()
