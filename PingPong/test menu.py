import pygame
import time
import random
 
pygame.init()
 
display_width = 800
display_height = 600
 
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

def start_screen():

    intro = True
    introbg = pygame.image.load("intro_bg.png") #loads background for start screen
    while intro:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        gameDisplay.blit(introbg,(0,0)) #sets bg onto the screen
        # creates two buttons one to start and one to exit
        button("Start",150,450,100,50,green,bright_green,game_loop)
        button("Exit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

#function for button that takes in: 
#( Messege on button, xpos, ypos, width,heigt, inactive color, active color and the action when clicked)
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos() #allows for mouse interaction 
    click = pygame.mouse.get_pressed()
    print(click)
    # this is for interaction with the mouse
    # when the mouse hovers over a button it redraws the button with a different
    # color to show that it is selected
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

#prints text onto screen
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
def game_loop():
    print ("yes") #this will be replaced with the command to start the game
def quitgame():
    print ("quit") #this will run the quit command 


start_screen()
