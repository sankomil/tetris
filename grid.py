import pygame
import random

from globals import top_left_x, top_left_y, play_height, play_width, block_size
from pieces import shapes, Piece

pygame.font.init()

def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for a in range(10)] for b in range(20)]

    for i in range(20):
        for j in range(10):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid

def convert_shape_format(shape):
    positions = []
    format_val = shape.shape[shape.rotation % len(shape.shape)]

    for i, a in enumerate(format_val):
        for j, b in enumerate(list(a)):
            if b == '0':
                positions.append((shape.x + j, shape.y + i ))
    
    for i, a in enumerate(positions):
        positions[i] = (a[0] - 2, a[1] - 4)
    
    return positions

def valid_space(shape, grid):
    allowed_spaces = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    allowed_spaces = [j for pos in allowed_spaces for j in pos]

    formatted_shape = convert_shape_format(shape)

    for position in formatted_shape:
        if position not in allowed_spaces:
            if position[1] > -1:
                return False
    
    return True


def check_lost(positions):
    for p in positions:
        x, y = p
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):  
    pass
   
def draw_grid(surface, grid):
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + i * block_size), (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (top_left_x + j * block_size, top_left_y), (top_left_x + j * block_size, top_left_y + play_height))


def clear_rows(grid, locked_positions):
    count = 0

    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]

        if not (0, 0, 0) in row:
            count += 1
            index = i

            for j in range(len(row)):
                try:
                    del locked_positions[(j, i)]
                except:
                    continue
        
        if count > 0:
            for key in sorted(list(locked_positions), key=lambda x: x[1], reverse=True):
                x, y = key
                if y < index:
                    locked_positions[(x, y + count)] = locked_positions.pop(key)
        

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render("Next shape", 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + play_height / 2 - 100
    formatted_shape = shape.shape[shape.rotation % len(shape.shape)]

    for i, row in enumerate(formatted_shape):
        for j, col in enumerate(list(row)):
            if col == '0':
                pygame.draw.rect(surface, shape.shape_colour, (start_x + j * block_size, start_y + i * block_size, block_size, block_size), 0)
    
    surface.blit(label, (start_x + 10, start_y - 30))

def draw_window(surface, grid):
    surface.fill((0,0,0))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))
 
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
 

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)

def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    curr_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    speed = 0.25

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > speed:
            fall_time = 0
            curr_piece.y += 1
            if not valid_space(curr_piece, grid) and curr_piece.y > 0:
                curr_piece.y -= 1
                change_piece = True
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    curr_piece.x -= 1
                    if not valid_space(curr_piece, grid):
                        curr_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    curr_piece.x += 1
                    if not valid_space(curr_piece, grid):
                        curr_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    curr_piece.y += 1
                    if not valid_space(curr_piece, grid):
                        curr_piece.y -= 1
                if event.key == pygame.K_UP:
                    curr_piece.rotation += 1
                    if not valid_space(curr_piece, grid):
                        curr_piece.rotation -= 1
                    curr_piece.rotation = curr_piece.rotation % len(curr_piece.shape)
        

        formatted_shape = convert_shape_format(curr_piece)

        for i in range(len(formatted_shape)):
            x, y = formatted_shape[i]
            if y > -1:
                grid[y][x] = curr_piece.shape_colour
        
        if change_piece:
            for pos in formatted_shape:
                p = (pos[0], pos[1])
                locked_positions[p] = curr_piece.shape_colour
            curr_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(grid, locked_positions)
    
        draw_window(win, grid)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False
    pygame.display.quit()

def main_menu(win):
    main(win)