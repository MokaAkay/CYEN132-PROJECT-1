import pygame
from pygame.locals import *


pygame.init()

display_width = 800
display_height = 600

## Color list ##
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

clock = pygame.time.Clock() # clock for later use

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Pong')

# Function to allow exiting by pressing q or ESC
def event_handler():
    for event in pygame.event.get():
        if event.type == QUIT or (
             event.type == KEYDOWN and (
              event.key == K_ESCAPE or
              event.key == K_q
             )):
            pygame.quit()
            quit()
# function to display text to the upper center of the window
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',75)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/4))
    game_display.blit(TextSurf, TextRect)

# function to render text to be passed into message_display    
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()
    
while True:
    event_handler()

    # Basic window setup
    game_display.fill(black)
    message_display('Welcome to the Game')
    
    # Do Game Stuff here #


    pygame.display.update()
