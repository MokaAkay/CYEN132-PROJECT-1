
import RPi.GPIO as GPIO
import pygame
import random
import math
import time

pygame.init()
display_width = 800
display_height = 475
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pong!')
clock = pygame.time.Clock()
crashed = False

# Color RGB values for use later on
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

#Pins for buttons
pause = 27
p1 = [25,26]
p2 = [23,24]

#dictionaries for the 2 sets of LEDs
P1LED = [17 , 16 , 13, 12, 6]
P2LED = [18, 19, 20, 21, 22]

#GPIO button setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(pause, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(p1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(p2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO led setup
GPIO.setup(P1LED, GPIO.OUT)
GPIO.setup(P2LED, GPIO.OUT)

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

# The Main Menu class
class MainMenu(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.bg = pygame.image.load("intro_bg.png")
        self.currentScreen = 0
        GPIO.output(P1LED,False)
        GPIO.output(P2LED,False)
    #sets up the start screen and buttons
    def start_screen(self):
        if (self.currentScreen == 0):
            self.button("Start",150,350,100,50,green,bright_green,self.playerSelection)
            self.button("Exit",550,350,100,50,red,bright_red,self.quitgame)
        elif (self.currentScreen == 1):
            self.button("Only AI", 200, 300, 100, 50, green, bright_green, self.setPlayerCount, 0)
            self.button("One Player", 350, 300, 100, 50, green, bright_green, self.setPlayerCount, 1)
            self.button("Two Player", 500, 300, 100, 50, green, bright_green, self.setPlayerCount, 2)
        elif (self.currentScreen == 4):
            self.label("Select Paddle Speed", 345, 350, 20)
            self.button("Slow", 200, 400, 100, 50, green, bright_green, self.setPaddleSpeed, "slow")
            self.button("Average", 350, 400, 100, 50, green, bright_green, self.setPaddleSpeed, "average")
            self.button("Fast", 500, 400, 100, 50, green, bright_green, self.setPaddleSpeed, "fast")

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
        self.gameSelection = PongGame()
        self.currentScreen = 1

    def playerWins(self):                
        self.currentScreen = 2

    def playerLoses(self):
        self.currentScreen = 3

    def startPong(self):
        global game
        game = self.gameSelection

    #This sets the number of players in the gameSelection variable(which at this point would be Pong object)
    def setPlayerCount(self, args):
        time.sleep(0.25)
        if (args == 0):
            self.gameSelection.setPaddleOneIsPlayer(False)
            self.gameSelection.setPaddleTwoIsPlayer(False)
        elif (args == 1):
            self.gameSelection.setPaddleOneIsPlayer(True)
            self.gameSelection.setPaddleTwoIsPlayer(False)
        else:
            self.gameSelection.setPaddleOneIsPlayer(True)
            self.gameSelection.setPaddleTwoIsPlayer(True)
        self.currentScreen = 4

    #This sets the number of players in the gameSelection variable(which at this point would be a Pong object)
    #also starts the pong game
    def setPaddleSpeed(self, args):
        if (args == "slow"):
            self.gameSelection.setPaddleSpeeds(5)
        elif (args == "average"):
            self.gameSelection.setPaddleSpeeds(10)
        else:
            self.gameSelection.setPaddleSpeeds(15)
        self.startPong()
        
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

    def label(self, msg, x, y, size):
        myfont = pygame.font.SysFont("freesansbold.ttf", size)
        # render text
        label = myfont.render(msg, 1, (0,0,0))
        gameDisplay.blit(label, (x, y))

    def text_objects(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
        
    def quitgame(self):
        print ("quit")
        global crashed
        crashed = True
        
    def update(self):
        gameDisplay.fill(white)
        gameDisplay.blit(self.bg,(0,0))
        self.start_screen()


#PONG GAME IMPLEMENTATION
class PongGame(GameState):
    def __init__(self):
        GameState.__init__(self)
        self.bg = pygame.image.load("background.png")
        self.isPaused = False
        self.pauseHandler = False
        #inherit from Gamestate class with music and background image
        
        global entities_list

        #adds all of the required entities to the entities list
        #change "true" to "false" if you want the paddle to be an AI
        
        #Paddle(xPos, yPos, speed, team, isPlayer)
        #Ball(xPos, yPos, startingSpeed)
        #setPlayerLivesFull()
        paddle1 =Paddle(40, 4, 1, pygame.image.load("paddle1.png"))
        paddle2 =Paddle(display_width-50, 20, 2, pygame.image.load("paddle2.png"))
        ball = Ball(display_width/2, display_height/2, 4)
        entities_list = [paddle1, paddle2, ball]

    def setPlayerLivesFull(self):
        for i in range(0, len(P1LED)-1):
            GPIO.output(P1LED[i],GPIO.HIGH)
            GPIO.output(P1LED[i],GPIO.HIGH)

    def setPaddleSpeeds(self, speed):
        entities_list[0].setSpeed(speed)
        entities_list[1].setSpeed(speed)

    def setBallSpeed(self, speed):
        entities_list[3].setSpeed(speed)

    def setPaddleOneIsPlayer(self, isPlayer):
        entities_list[0].setIsPlayer(isPlayer)
        
    def setPaddleTwoIsPlayer(self, isPlayer):
        entities_list[1].setIsPlayer(isPlayer)

    def updateEntities(self):
        for entity in entities_list:
            entity.update()

    def renderEntities(self):
        for entity in entities_list:
            entity.render()
        
    def update(self):
        if ((event.type == pygame.KEYDOWN and (event.key == pygame.K_p)) or (GPIO.input(pause) == True)):
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
    def __init__(self, xPos, yPos, team, img):
        paddleImg = img
        Entity.__init__(self, xPos, yPos, paddleImg)
        self.team = team
        self.isPlayer = False
        self.speed = 5
        self.lives = 5
        self.scoreFont = pygame.font.Font('freesansbold.ttf',50)

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

    def setSpeed(self, value):
        self.speed = value
    def setIsPlayer(self, isPlayer):
        self.isPlayer = isPlayer

    def scoring(self):
        scoreDraw = self.scoreFont.render(str(self.lives),1,white)
        if (self.team == 1):
            gameDisplay.blit(scoreDraw, (85,7))
            for i in range(0,self.lives):
                GPIO.output(P1LED[i],True)
            for i in range(0,5-self.lives):
                GPIO.output(P1LED[i],False)
        if (self.team == 2):
            gameDisplay.blit(scoreDraw, (display_width-105,7))
            for i in range(0,self.lives):
                GPIO.output(P2LED[i],True)
            for i in range(0,5-self.lives):
                GPIO.output(P2LED[i],False)
    def update(self):
        if (self.isPlayer):
            if (self.team == 1):
                #Player 1 input goes here
                #This stuff is for now, later we will use GPIO input instead with switches
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_s):
                        if self.yPosEnd<display_height:
                            self.yPos +=self.speed
                            self.yPosEnd += self.speed
                    elif (event.key == pygame.K_w):
                        if self.yPos>=0:
                            self.yPos -= self.speed
                            self.yPosEnd -= self.speed
                if (GPIO.input(p1[0]) == True):
                    if self.yPosEnd<display_height:
                            self.yPos +=self.speed
                            self.yPosEnd += self.speed
                if (GPIO.input(p1[1]) == True):
                    if self.yPos>=0:
                            self.yPos -= self.speed
                            self.yPosEnd -= self.speed
                    
                    
            if (self.team == 2):
                #Player 1 input goes here
                #if up is held, decrease the y position by speed
                #if down is held, decrease the y position by speed
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_DOWN):
                        if self.yPosEnd<display_height:
                            self.yPos +=self.speed
                            self.yPosEnd += self.speed
                    elif (event.key == pygame.K_UP):
                        if self.yPos>=0:
                            self.yPos -= self.speed
                            self.yPosEnd -= self.speed
                if (GPIO.input(p2[0]) == True):
                        if self.yPosEnd<display_height:
                            self.yPos +=self.speed
                            self.yPosEnd += self.speed
                if (GPIO.input(p2[1]) == True):
                        if self.yPos>=0:
                            self.yPos -= self.speed
                            self.yPosEnd -= self.speed
        self.scoring()
        #if the paddle is not a player(human) it will take control of itself
        if (not self.isPlayer):
            self.chaseBall()


class Ball(Entity):
    def __init__(self, xPos, yPos, startingSpeed):
        ballImg=pygame.image.load('ball.png')
        Entity.__init__(self, xPos, yPos, ballImg)
        self.startingSpeed = startingSpeed
        self.speed = startingSpeed
        #the number of times the ball has hit a paddle
        self.bounces=0
        numbers = list(range(0,60)) + list(range(120,250)) + list(range(310,360))
        self.direction = random.choice(numbers)
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
        global game
        if self.xPos <= 0:
                self.__init__(display_width/2, display_height/2,self.startingSpeed)#reset ball
                entities_list[0].lives -= 1 #decrement p1 lives by 1
                if (entities_list[0].lives <=0):
                    game = MainMenu()
                    
                
        if self.xPosEnd >= display_width:
                self.__init__(display_width/2, display_height/2,self.startingSpeed)
                entities_list[1].lives -= 1 #decrement p2 lives by 1
                if (entities_list[1].lives <= 0):
                    game = MainMenu()
        

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

    def setSpeed(self, speed):
        self.speed = speed
        
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
