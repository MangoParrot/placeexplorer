import pandas as pd
import pygame
from pygame.locals import *
import sys
import datetime
import numpy as np
import pyautogui

# Getting screen size and setting it to full screen
WINWIDTH,WINHEIGHT= pyautogui.size()

df = pd.read_csv("2022_place_canvas_history-000000000000.csv")
datetime.datetime = df['timestamp']
WIN = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
CAMERA_SPEED = 500
# board = np.zeros((2000,2000))
def Hex2RGB(h):
    # We strip the colour of the thing in another place
    h = h.lstrip('#')
    return  tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
print(Hex2RGB('#FFA800'))
Board = [[(0,0,0) for i in range(2000)]for i in range(2000)]
CurrTime = 1175316
for i in range(CurrTime):
    # Assigns the proper colour to each pixel
    coords = df['coordinate'][i].split(',')
    coords[0]= int(coords[0])
    coords[1]= int(coords[1])
    colour = Hex2RGB(df['pixel_color'][i])
    # Every pixel under board has the colour which it needs to have
    Board[coords[0]][coords[1]]=colour

def manage_camera(keys_pressed,xoffset,yoffset):
    if keys_pressed[K_w]:
        yoffset -= CAMERA_SPEED

    if keys_pressed[K_s]:
        yoffset += CAMERA_SPEED

    if keys_pressed[K_d]:
        xoffset += CAMERA_SPEED

    if keys_pressed[K_a]:
        xoffset -= CAMERA_SPEED
    return [xoffset,yoffset]

def Draw(cameraxoffset,camerayoffset):
    for row in range(len(Board)):
        for pixel in range(len(Board[row])):
            CurPixel = pygame.Rect(pixel+cameraxoffset,row+camerayoffset,1,1)
            pygame.draw.rect(WIN,Board[row][pixel],CurPixel)
    pygame.display.update()
def main():
    xoffset = 0
    yoffset = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        # Possible optimization here, function is running twice.
        xoffset = manage_camera(keys_pressed,xoffset,yoffset)[0]
        yoffset = manage_camera(keys_pressed,xoffset,yoffset)[1]
        Draw(xoffset,yoffset)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
