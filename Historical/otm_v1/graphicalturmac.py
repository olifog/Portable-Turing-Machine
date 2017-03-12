#A Pygame Turing Machine simulator

import pygame, sys, random
from textinput import TextInput
pygame.init()
pygame.font.init()

size = width, height = 600, 400
black = 0,0,0
white = 250,250,220

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Python Turing Machine Simulator")
myfont = pygame.font.SysFont("Arial", 35)
tapefonts = pygame.font.SysFont("Arial", 15)

while True:
    title = myfont.render('Turing Machine Simulator', True, black)
    foretape = tapefonts.render('Tape:', True, black)
    tape = tapefonts.render(str(random.randint(100,999) * random.randint(100,999)), False, black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(white)
    screen.blit(title, (40, 0))
    screen.blit(foretape, (0, 40))
    screen.blit(tape, ((600 / 2) - tape.get_rect().width / 2, 55))
    pygame.display.flip()
