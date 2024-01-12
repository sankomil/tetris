import pygame

from globals import screen_height, screen_width
from grid import main_menu

if __name__ == '__main__':
    window_val = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tetris')
    main_menu(window_val)