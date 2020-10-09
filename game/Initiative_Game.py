"""
Sam Bernstein, 2015, Windward Senior Initiative 

"""
 
import pygame
from pygame.locals import *
import math
import copy
import random

printing = False
def p_dev(*strings):
    if printing:
        p = ''
        for f in strings:
            p += str(f)
        print(p)


p_dev("Game Started\n\n")

cycle = 0

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def gray(g):
    return (g,g,g)

GRAY = gray(100)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

PI = 3.141592653

pygame.init()
 
# Set the width and height of the screen [width, height]
size = (1200, 740)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Get Me Outta Here - Sam Bernstein Senior Initiative")
 
# Loop until the user clicks the close button.
done = False
pause = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def write_text(surface, text, text_color, length, height, x, y, size = 2): # used for dispalying level header
        font_size = size*int(length//len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))

# ----- Game Objects --------

class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = 2*int(length//len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        # return surface

    def draw_button(self, surface, color, length, height, x, y, width):           
        for i in range(1,10):
            s = pygame.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)  
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
        return False


y_value = 30
class LevelSelector:

    y_val = y_value
    over = 500
    l = 120
    h = 80

    def __init__(self, x, text, y = y_value, color = gray(50)):
        self.Button1 = Button()
        self.color = color
        self.x = x - LevelSelector.over
        self.y = y
        self.text = text

        self.l = LevelSelector.l
        self.h = LevelSelector.h
    #Update the display and show the button
    def draw_button(self):
        #Parameters:               surface,  color,    x,         y,   length, height,     width, text,      text_color
        self.Button1.create_button(screen, self.color, self.x, self.y, self.l, self.h,  0, self.text, gray(240))

last_level_button = LevelSelector(size[0]/2 - LevelSelector.l/2, "Last Level" )
next_level_button = LevelSelector(size[0]/2 + LevelSelector.l/2 + 10, "Next Level")
reset_all_button  = LevelSelector(size[0]/2, "Reset All", y = size[1] - 100)

button_text = ['Got it', ' OK ']

class LevelTextButton:

    y_val = 30
    over = 500
    l = 55
    h = 40

    def __init__(self, y, color = gray(50)):
        self.Button1 = Button()
        self.color = color
        self.x = size[0]/2 - 400
        self.y = y
        self.text = button_text[random.randint(1,2)%2]

        self.l = LevelTextButton.l
        self.h = LevelTextButton.h
    #Update the display and show the button
    def draw_button(self):
        #Parameters:               surface,  color,    x,         y,   length, height,     width, text,      text_color
        self.Button1.create_button(screen, self.color, self.x, self.y, self.l, self.h,  0, self.text, gray(240))


start_level_text_x = 5*(size[0] - size[0]%5)/10
start_level_text_y = 50

class LevelText():

    def __init__(self, start_txt = None, solved_txt = None, wait = False):
        self.start = start_txt
        self.solved = solved_txt
        self.wait = wait

def draw_check(x, y, size, color = (255,215,0)): # draws the checks for each level indicating completion
    angle_down = math.radians(45)
    angle_up   = math.radians(65)

    l_wid = size//2
    down_len = 1.0*size
    up_len   = 2.5*size

    bottom_x = x + math.cos(angle_down)*down_len
    bottom_y = y + math.sin(angle_down)*down_len

    pygame.draw.line(screen, color, (x, y), (bottom_x, bottom_y), l_wid)
    pygame.draw.line(screen, color, (bottom_x, bottom_y), (bottom_x + math.cos(angle_up)*up_len, bottom_y - math.sin(angle_up)*up_len), l_wid)


# Level variables and classes

# Player circle
player_color = RED
player_radius = 21

player_x = 300
player_y = 200

player_speed = 10

class Player():

    def __init__(self, x, y, speed = player_speed):

        self.c = player_color
        self.r = player_radius

        self.x = int(x)
        self.y = int(y)

        self.enclosing_square = pygame.Rect(self.x - self.r, self.y - self.r, 2*self.r, 2*self.r)

        self.allowed_basic_mov = {'up': False, 'down': False, 'left': False, 'right': False}
        self.allowed_combined_mov = {'up_left': False, 'up_right': False, 'down_left': False, 'down_right': False}

        self.moving_directions = {'up': False, 'down': False, 'left': False, 'right': False} # the directions in which the circle will move in (after processing)

        self.speed = speed
        self.v_x = 0
        self.v_y = 0

    def plug_in_x(self, x, side = 1):
        try:
            y_val = side*math.sqrt(self.r**2 - (x - self.x)**2) + self.y
            return y_val
        except ValueError:
            pass
        return self.y

    def plug_in_y(self, y, side = 1):
        try:
            x_val = side*math.sqrt(self.r**2 - (y - self.y)**2) + self.x
            return x_val
        except ValueError:
            pass
        return self.x

    def update_pos(self):
        dir_dict = self.moving_directions
        speed = self.speed

        self.v_y = 0
        self.v_x = 0

        if dir_dict['up']:
            self.v_y = -speed
        if dir_dict['down']:
            self.v_y = speed
        if dir_dict['left']:
            self.v_x = -speed
        if dir_dict['right']:
            self.v_x = speed

        self.x += int(self.v_x)
        self.y += int(self.v_y)
        self.enclosing_square = pygame.Rect(self.x - self.r, self.y - self.r, 2*self.r, 2*self.r)

        for key in self.moving_directions:
            self.moving_directions[key] = False

    def draw_player(self):
        player_circle = pygame.draw.circle(screen, self.c, (self.x, self.y), self.r, 0)


# Level colors
tile_size = 80

START_C = BLUE
END_C = GREEN
tlr = 230
BLOCK_C = (230, 230, 230)
clr = 60
TILE_C = (clr, clr, clr)

tile_color_dict = {0: TILE_C, 1: BLOCK_C, 2: BLACK, None: RED}

# Rotating Square object
rotate_speed = 10

class RotatingSquare(): # for rotation animation

    def __init__(self, level, direction):
        self.square_number = level.selected
        self.sqr = level.squares[level.selected]

        half_sqr_size = (self.sqr[1][1] - self.sqr[0][1] + 1)*0.5

        self.square_tiles = [[level.board[row][col] for col in range(self.sqr[0][1], self.sqr[1][1]+1)] for row in range(self.sqr[0][0], self.sqr[1][0] + 1)]

        self.tile_vertices = []
        pointlist = []

        for row in range(self.sqr[0][0], self.sqr[1][0] + 1):
            for col in range(self.sqr[0][1], self.sqr[1][1] + 1):
                top_left = (level.x + col*level.total_d, level.y + row*level.total_d)
                pointlist = [top_left, (top_left[0] + level.tile_size, top_left[1]), (top_left[0]+level.tile_size, top_left[1]+level.tile_size), (top_left[0],top_left[1]+level.tile_size)]
                
                ROT_COLOR = tile_color_dict[level.board[row][col]]

                self.tile_vertices.append([pointlist, ROT_COLOR])

        sqr = self.sqr
        start_x = level.x + sqr[0][1]*level.total_d
        start_y = level.y + sqr[0][0]*level.total_d

        end_x = start_x + (sqr[1][1] - sqr[0][1] + 1)*level.total_d
        end_y = start_y + (sqr[1][0] - sqr[0][0] + 1)*level.total_d

        self.outline_vertices = [(start_x, start_y), (start_x, end_y), (end_x, end_y), (end_x, start_y)]
        
        self.center_vector = (level.x + level.total_d*(half_sqr_size + self.sqr[0][1]), level.y + level.total_d*(half_sqr_size + self.sqr[0][0]))
        self.dir = direction
        self.angle_displacement = 0.0
        self.rotate_speed = level.rot_speed * direction

    def rotation_transform(self, vector):
        a = math.radians(self.rotate_speed)
        sqr_vector = (vector[0] - self.center_vector[0], vector[1] - self.center_vector[1])
        rotated_square_vector = (sqr_vector[0]*math.cos(a) + sqr_vector[1]*math.sin(a), -sqr_vector[0]*math.sin(a) + sqr_vector[1]*math.cos(a))
        new_vector = (rotated_square_vector[0] + self.center_vector[0], rotated_square_vector[1] + self.center_vector[1])
        return new_vector

# square outline colors
GREENISH = [3, 70, 2]
MAGENTISH = [78, 4, 9]
ORANGISH = [90, 49, 2]
TEALISH = [4, 18, 54]
YELLOWISH = [84, 84, 1]
outline_colors = [GREENISH, ORANGISH, TEALISH, MAGENTISH, YELLOWISH]
tttt = 200
SELECTED_MONOCHROME = (tttt,tttt,tttt)

# miscellaneous parameters

class Level(): # stores all information for each level

    margin = 10
    txt_length = 36
    font_size = 20
    spacing = 5

    def __init__(self, board, squares, txt = None, tile_size = tile_size):

        self.board = board # a two-dimensional list ([row][col]) where 0: empty, 1: block, 2: off the board
        self.squares = squares # a list of top left and bottom right tiles coordinate tuples for each square
        self.selected = 0 # selected square at any given moment

        self.tile_size = tile_size
        self.margin = (tile_size)//9
        self.total_d = self.tile_size + self.margin

        self.buffer = self.tile_size//14

        self.outline_width = self.margin - 1
        # for offsetting board grid to center
        self.x = .6*(size[0] - len(board)*(self.total_d))
        self.y = .6*(size[1] - len(board[0])*(self.total_d))

        self.rotating = []  # an ordered list of RotatingSquare() objects
        self.rot_speed = rotate_speed

        self.player = Player(self.x - self.total_d + self.tile_size/2, self.y + (len(self.board) - 1)*self.total_d + self.tile_size/2)
        self.started = False   # True after player confirms that they read the instructions
        self.completed = False # True when player reaches the end tile
        self.solved    = False # True once a path has been opened

        if txt != None:
            if txt.wait == False:
                self.started = True
        else:
            self.started = True

        self.instructions = txt
        self.start_button = None
        if txt != None:
            y_of_button = LevelSelector.y_val + 2*LevelSelector.h + (len(txt.start)//Level.txt_length + 1)*(Level.font_size + Level.spacing)
            self.start_button = LevelTextButton(y_of_button)

    def rotate_square(self, direction): # direction either 1 for counter-CC, -1 for CC, or 0 for 180 degrees
        
        if direction != None:
            sqr = self.squares[self.selected]
            p_dev("Square in question: ", sqr)

            if direction == 1:

                a = [[self.board[row][col] for col in range(sqr[0][1], sqr[1][1]+1)] for row in range(sqr[0][0], sqr[1][0] + 1)]

                n = len(a)
                for i in range(n/2):
                    for j in range(i, n-i-1):
                        tmp = a[i][j]
                        a[i][j] = a[j][n-i-1]
                        a[j][n-i-1] = a[n-i-1][n-j-1]
                        a[n-i-1][n-j-1] = a[n-j-1][i]
                        a[n-j-1][i]= tmp
               
                for row in range(n):
                    for col in range(n):
                        self.board[sqr[0][0]+row][sqr[0][1]+col] = a[row][col]

            elif direction == -1:

                a = [[self.board[row][col] for col in range(sqr[0][1], sqr[1][1]+1)] for row in range(sqr[0][0], sqr[1][0] + 1)]

                n = len(a)
                for i in range(n/2):
                    for j in range(i, n-i-1):
                        tmp = a[i][j]
                        a[i][j] = a[n-j-1][i]
                        a[n-j-1][i] = a[n-i-1][n-j-1]
                        a[n-i-1][n-j-1] = a[j][n-i-1]
                        a[j][n-i-1] = tmp
                    
                for row in range(n):
                    for col in range(n):
                        self.board[sqr[0][0]+row][sqr[0][1]+col] = a[row][col]
                
            elif direction == 0:
                for n in range(2):
                    self.rotate_square(1)

    def check_path(self):

        if self.board[len(self.board) - 1][0] != 0: # if tile next to start tile is blocked, return False
            return False

        path_heads = []
        new_path_heads = []
        next = []
        history = set()

        path_heads.append((len(self.board)-1, 0)) # initialize search in first enterable tile

        def check_adjacent(tile, d_x, d_y):
            try:
                next = (tile[0] + d_x, tile[1] + d_y)
                if self.board[next[0]][next[1]] == 0 and next not in history:
                    new_path_heads.append(next)

            except IndexError: # handles if tile is not on the board
                pass


        while len(path_heads) != 0:
            new_path_heads = []

            for head in path_heads:
                history.add(head)

            for head in path_heads:

                check_adjacent(head, 0, 1)
                check_adjacent(head, 0, -1)
                check_adjacent(head, 1, 0)
                check_adjacent(head, -1, 0)
            
            path_heads = new_path_heads

            for head in path_heads:
                if head == (0, len(self.board[0]) - 1): # if has reached tile adjacent to end tile
                    return True

        return False # if all path ends die out, return no open path

    def set_allowed_movements(self):
        global cycle

        player = self.player
        # reset to not allowed to move before each cycle
        for key in self.player.allowed_basic_mov:
            self.player.allowed_basic_mov[key] = False
        for key in self.player.allowed_combined_mov:
            self.player.allowed_combined_mov[key] = False

        if self.started:

            player_x = self.player.x
            player_y = self.player.y
            player_r = self.player.r

            current_tile_row = 0
            current_tile_col = 0

            current_tile_row = int((player.y - self.y)//self.total_d)
            current_tile_col = int((player.x - self.x)//self.total_d)

            if player.y - self.y <= 0:
                current_tile_row = 0
            if player.x - self.x <= 0:
                current_tile_col = -1

            curr_tile = (current_tile_row, current_tile_col)

            def check_nearby(d_y, d_x):
                tile = curr_tile
                try:
                    next = (tile[0] + d_y, tile[1] + d_x)
                    if next[0] == len(self.board) - 1 and next[1] == -1: # if it's the start tile
                        return True
                    if next[0] == 0 and next[1] == len(self.board[0]): # if it's the end tile
                        return True
                    # out of bounds of board
                    if next[0] < 0 or next[0] > len(self.board) - 1:
                        return False
                    if next[1] < 0 or next[1] > len(self.board[0]) - 1:
                        return False

                    if self.board[next[0]][next[1]] == 0: # returns true if it exists and is empty
                        return True 

                except IndexError: # handles if tile is not on the board
                    pass

                return False

            tiles_around = [False for t in range(8)] # for each tile around current occupied tile: True for empty, False for not

            tiles_around[0] = check_nearby(-1, 1)
            tiles_around[1] = check_nearby(-1, 0)
            tiles_around[2] = check_nearby(-1, -1)
            tiles_around[3] = check_nearby( 0, -1)
            tiles_around[4] = check_nearby( 1, -1)
            tiles_around[5] = check_nearby( 1, 0)
            tiles_around[6] = check_nearby( 1, 1)
            tiles_around[7] = check_nearby( 0, 1)

            if cycle%150 == 0:
                p_dev()
                p_dev( "row: ",curr_tile[0], "col: ", curr_tile[1])
                for k in range(len(tiles_around)):
                    p_dev(str(k)+" : "+str(tiles_around[k])+", ")

            # check all 4 sides for every possible case
            self.player.allowed_basic_mov['up'] = False
            if tiles_around[1] or (player_y - player_r) > self.y + (curr_tile[0])*self.total_d - self.margin + self.buffer:

                leftside  = self.x + (curr_tile[1])*self.total_d - self.margin
                rightside = self.x + (curr_tile[1] + 1)*self.total_d
                top =  self.y + (curr_tile[0])*self.total_d - self.margin

                if player_x - player_r < leftside:
                    if self.player.plug_in_x(leftside, -1) > top or tiles_around[2]:
                        self.player.allowed_basic_mov['up'] = True
                elif player_x + player_r > rightside:
                    if self.player.plug_in_x(rightside, -1) > top or tiles_around[0]:
                        self.player.allowed_basic_mov['up'] = True
                else:
                    self.player.allowed_basic_mov['up'] = True


            self.player.allowed_basic_mov['down'] = False
            if tiles_around[5] or (player_y + player_r) < self.y + (curr_tile[0] + 1)*self.total_d - self.buffer:

                leftside  = self.x + (curr_tile[1])*self.total_d - self.margin
                rightside = self.x + (curr_tile[1] + 1)*self.total_d
                bottom =  self.y + (curr_tile[0] + 1)*self.total_d

                if player_x - player_r < leftside:
                    if self.player.plug_in_x(leftside, 1) < bottom or tiles_around[4]:
                        self.player.allowed_basic_mov['down'] = True
                elif player_x + player_r > rightside:
                    if self.player.plug_in_x(rightside, 1) < bottom or tiles_around[6]:
                        self.player.allowed_basic_mov['down'] = True
                else:
                    self.player.allowed_basic_mov['down'] = True


            self.player.allowed_basic_mov['left'] = False
            if tiles_around[3] or (player_x - player_r) > self.x + (curr_tile[1])*self.total_d - self.margin + self.buffer:

                top  = self.y + (curr_tile[0])*self.total_d - self.margin
                bottom = self.y + (curr_tile[0] + 1)*self.total_d
                leftside =  self.x + (curr_tile[1])*self.total_d - self.margin

                if player_y - player_r < top:
                    if self.player.plug_in_y(top, -1) > leftside or tiles_around[2]:
                        self.player.allowed_basic_mov['left'] = True
                elif player_y + player_r > bottom:
                    if self.player.plug_in_y(bottom, -1) > leftside or tiles_around[4]:
                        self.player.allowed_basic_mov['left'] = True
                else:
                    self.player.allowed_basic_mov['left'] = True


            self.player.allowed_basic_mov['right'] = False
            if tiles_around[7] or (player_x + player_r) < self.x + (curr_tile[1] + 1)*self.total_d - self.buffer:
                        
                top  = self.y + (curr_tile[0])*self.total_d - self.margin
                bottom = self.y + (curr_tile[0] + 1)*self.total_d
                rightside =  self.x + (curr_tile[1] + 1)*self.total_d

                if player_y - player_r < top:
                    if self.player.plug_in_y(top, 1) < rightside or tiles_around[0]:
                        self.player.allowed_basic_mov['right'] = True
                elif player_y + player_r > bottom:
                    if self.player.plug_in_y(bottom, 1) < rightside or tiles_around [6]:
                        self.player.allowed_basic_mov['right'] = True
                else:
                    self.player.allowed_basic_mov['right'] = True


            allowed_basic = self.player.allowed_basic_mov

            vert = ['up', 'down']
            horiz = ['left', 'right']

            # set the allowed combined movements, which are just combinations of a vertical direction and a horizontal direction
            if cycle%50 == 0:
                p_dev("\nTrue combined directions:")
            for vert_dir in vert:
                for horiz_dir in horiz:
                    if allowed_basic[vert_dir] and allowed_basic[horiz_dir]:
                        self.player.allowed_combined_mov[vert_dir+'_'+horiz_dir] = True

                        if cycle%50 == 0:
                            p_dev(vert_dir+'_'+horiz_dir)


            if cycle%150 == 0:
                p_dev()
                p_dev(self.player.allowed_basic_mov)

    def set_movement(self, key_move_commands):
        player = self.player

        vert = ['up', 'down']
        horiz = ['left', 'right']

        vert_commands = []
        horiz_commands = []

        basic_dirs = []

        number_of_dirs = 0
        one_key = ''

        for key in key_move_commands:
            if key_move_commands[key]:
                number_of_dirs += 1
                one_key = key
                if key in vert:
                    vert_commands.append(key)
                elif key in horiz:
                    horiz_commands.append(key)


        if number_of_dirs == 1 and player.allowed_basic_mov[one_key]:
            self.player.moving_directions[one_key] = True
            return

        
        if len(vert_commands) == 1 and len(horiz_commands) == 1:
            comb_dir = vert_commands[0]+'_'+horiz_commands[0] # combined direction key
            if player.allowed_combined_mov[comb_dir]:
                self.player.moving_directions[vert_commands[0]] = True
                self.player.moving_directions[horiz_commands[0]] = True

            elif player.allowed_basic_mov[vert_commands[0]]:
                self.player.moving_directions[vert_commands[0]] = True

            elif player.allowed_basic_mov[horiz_commands[0]]:
                self.player.moving_directions[horiz_commands[0]] = True



    def check_finished(self):
        left = self.x + len(self.board[0])*self.total_d
        top = self.y
        
        end_tile_rect = pygame.Rect(left, top, self.tile_size, self.tile_size)

        there = end_tile_rect.contains(self.player.enclosing_square)

        return there

    def write_instructions(self):
        text_color = gray(230)

        length = Level.txt_length
        under_len = 8
        over_len = 7

        font_size = Level.font_size
        height = 20
        x = 200
        y = LevelSelector.y_val + 150

        text = self.instructions.start

        lines = []
        index = 0
        while index < len(text):

            current_line =''
            early_cutoff = 0
            for i in range(index, len(text)):
                if len(current_line) > length + over_len:
                    index = i - (len(current_line) - early_cutoff)
                    current_line = current_line[:early_cutoff]
                    break

                if text[i] == ' ': # if a space is found
                    early_cutoff = len(current_line)
                    if len(current_line) > length:
                        break
                        
                current_line += text[i]
                index += 1
            lines.append(current_line)
            
        myFont = pygame.font.SysFont("Calibri", font_size)

        for line in lines:
            myText = myFont.render(line, 1, text_color)
            screen.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
            y += font_size + Level.spacing

        if self.start_button != None:
            if self.instructions.wait:
                self.start_button.draw_button()

        if self.solved: # message to be displayed once the level is solved
            text_color = gray(230)

            length = 30

            font_size = 25
            height = 20
            x = self.x + 0.7*self.total_d*len(self.board[0])
            y = start_level_text_y + 80 

            text = self.instructions.solved
            myFont = pygame.font.SysFont("Calibri", font_size)
            myText = myFont.render(text, 1, text_color)
            screen.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
            

    def draw_board(self):

        if self.started:
            font_size = 60
            myFont = pygame.font.SysFont("Calibri", font_size)

            # draw start tile
            left = self.x - self.total_d
            top = self.y + (len(self.board) - 1)*self.total_d
            pygame.draw.rect(screen, START_C,[left, top, self.tile_size, self.tile_size], 0)
            
            myText = myFont.render("S", 1, WHITE)
            screen.blit(myText, (left + self.tile_size//3, top ))

            # draw end tile
            left = self.x + len(self.board[0])*self.total_d
            top = self.y
            pygame.draw.rect(screen, END_C,[left, top, self.tile_size, self.tile_size], 0)

            myText = myFont.render("E", 1, WHITE)
            screen.blit(myText, (left + self.tile_size//3 , top))

            # Draw tiles

            animating_sqr_rows = range(0,0)
            animating_sqr_cols = range(0,0)

            if len(self.rotating) > 0:
                animating_sqr = self.rotating[0].sqr
                animating_sqr_rows = range(animating_sqr[0][0], animating_sqr[1][0] + 1)
                animating_sqr_cols = range(animating_sqr[0][1], animating_sqr[1][1] + 1)

            for row in range(len(self.board)):
                for column in range(len(self.board[0])):

                    if not(column in animating_sqr_cols and row in animating_sqr_rows): # only draw if not part of a rotating square

                        left = self.x + column*self.total_d
                        top = self.y + row*self.total_d

                        TILE_COLOR = tile_color_dict[self.board[row][column]]
                        pygame.draw.rect(screen, TILE_COLOR,[left, top, self.tile_size, self.tile_size], 0)
                

            # DRAW SQUARE OUTLINES
            
            for i in range(len(self.squares)):
                run_it = True
                if i != self.selected:
                    if len(self.rotating) > 0:
                        if i == self.rotating[0].square_number:
                            run_it = False
                    
                    if run_it:
                        sqr = self.squares[i]

                        SHADE = copy.deepcopy(outline_colors[i%len(outline_colors)])
                        
                        for i in range(len(SHADE)):
                            SHADE[i] *= 1.4
                            if SHADE[i] > 255:
                                SHADE[i] = 255

                        NEW = (SHADE[0], SHADE[1], SHADE[2])

                        start_x = self.x + sqr[0][1]*self.total_d
                        start_y = self.y + sqr[0][0]*self.total_d

                        end_x = start_x + (sqr[1][1] - sqr[0][1] + 1)*self.total_d
                        end_y = start_y + (sqr[1][0] - sqr[0][0] + 1)*self.total_d

                        pygame.draw.line(screen, NEW, (start_x, start_y), (start_x, end_y), self.outline_width)
                        pygame.draw.line(screen, NEW, (start_x, end_y), (end_x, end_y), self.outline_width)
                        pygame.draw.line(screen, NEW, (end_x, end_y), (end_x, start_y), self.outline_width)
                        pygame.draw.line(screen, NEW, (end_x, start_y), (start_x, start_y), self.outline_width)

            # Draw rotating square tiles and outline last so they show up over other tiles
          
            i = self.selected
            rotating_is_selected = False

            if len(self.rotating) > 0:
                # tiles
                curr = self.rotating[0]
                for p in range(len(curr.tile_vertices)):
                    pygame.draw.polygon(screen, curr.tile_vertices[p][1], curr.tile_vertices[p][0], 0)

                    for point in range(len(curr.tile_vertices[p][0])):
                        curr.tile_vertices[p][0][point] = curr.rotation_transform(curr.tile_vertices[p][0][point]) # rotates points of square polygon for next frame

                self.rotating[0].angle_displacement += self.rotating[0].rotate_speed

                # outline
                """
                if self.rotating[0].square_number == i:
                    rotating_is_selected = True
                    curr = self.rotating[0]

                    sqr = self.squares[i]
                    SHADE = copy.deepcopy(outline_colors[i%len(outline_colors)])
                    
                    for v in range(len(SHADE)):
                        SHADE[v] *= 6
                        if SHADE[v] > 255:
                            SHADE[v] = 255
                    
                    NEW = (SHADE[0], SHADE[1], SHADE[2])

                    for vertex in range(len(curr.outline_vertices)):
                        curr.outline_vertices[vertex] = curr.rotation_transform(curr.outline_vertices[vertex])

                    vert = curr.outline_vertices

                    pygame.draw.line(screen, NEW, vert[0], vert[1], self.outline_width) # top left to bottom left
                    pygame.draw.line(screen, NEW, vert[1], vert[2], self.outline_width)     # bottom left to bottom right
                    pygame.draw.line(screen, NEW, vert[2], vert[3], self.outline_width)     # bottom right to top right
                    pygame.draw.line(screen, NEW, vert[3], vert[0], self.outline_width) # top right to top left
                    
                    for v in range(len(SHADE)):
                        SHADE[v] /= 6
                """

            # Draws highlighted outline last so it shows up over others

            if not rotating_is_selected:
                sqr = self.squares[i]
                SHADE = copy.deepcopy(outline_colors[i%len(outline_colors)])
                
                for v in range(len(SHADE)):
                    SHADE[v] *= 6
                    if SHADE[v] > 255:
                        SHADE[v] = 255
                
                NEW = (SHADE[0], SHADE[1], SHADE[2])
            
                start_x = self.x + sqr[0][1]*self.total_d
                start_y = self.y + sqr[0][0]*self.total_d

                end_x = start_x + (sqr[1][1] - sqr[0][1] + 1)*self.total_d
                end_y = start_y + (sqr[1][0] - sqr[0][0] + 1)*self.total_d

                pygame.draw.line(screen, NEW, (start_x, start_y), (start_x, end_y), self.outline_width) # top left to bottom left
                pygame.draw.line(screen, NEW, (start_x, end_y), (end_x, end_y), self.outline_width)     # bottom left to bottom right
                pygame.draw.line(screen, NEW, (end_x, end_y), (end_x, start_y), self.outline_width)     # bottom right to top right
                pygame.draw.line(screen, NEW, (end_x, start_y), (start_x, start_y), self.outline_width) # top right to top left
                
                for v in range(len(SHADE)):
                    SHADE[v] /= 6

            self.player.update_pos()
            self.player.draw_player()

        # Write text for level

        if self.instructions != None:
            self.write_instructions()


levels = [] # for storing every Level object. The data in each level object changes as player plays each level.
levels_const = [] # for storing a permanent copy of every level object
instr = {}
instr[0] = LevelText('Welcome to "Get Me Outta Here": a maze puzzle game. Your goal is to open up a path to move the circle through the dark tiles to the end tile ("E"). To do this, rearrange the board by rotating the highlighted square groups of tiles, called "squares". Press the "K" or "L" keys to rotate the squares.', 'Use the arrow keys to move your circle to the end tile.', True)
instr[1] = LevelText('To select between two or more squares, press the number keys or the "S" and "D" keys.', wait = True)
instr[2] = LevelText('Boards and squares can be of any size.')
instr[3] = LevelText('Some tiles are unchangeable.')
instr[4] = LevelText('Squares can live inside each other.')
instr[5] = LevelText('Press "T" to reset the current level.', wait = True)
instr[6] = LevelText('When there are more than 2 squares, you can use the number keys to select specific squares directly.', wait = True)

for f in range(51):
    levels_const.append(None)

levels_const[0] = Level(board = [[0,0],[1,0]], squares = [[(0,0),(1,1)]], txt = instr[0])
levels_const[1] = Level(board = [[0,0,1],[1,0,0]], squares = [[(0,0),(1,1)], [(0,1),(1,2)]], txt = instr[1])
levels_const[2] = Level(board = [[0,1,1],[0,0,1],[1,0,0]], squares = [[(0,0),(2,2)]], txt = instr[2])
levels_const[3] = Level(board = [[1,0,1],[0,1,0],[0,0,1]], squares = [[(1,0),(2,1)], [(0,1),(1,2)]])
levels_const[4] = Level(board = [[0,0,0,0,1,1],[0,1,0,0,0,0],[0,1,0,1,1,1],[0,0,0,0,1,1],[1,1,1,0,0,0],[0,0,0,1,1,1]], squares = [[(0,0),(2,2)],[(0,3),(2,5)],[(3,0),(5,2)],[(3,3),(5,5)]])
levels_const[5] = Level(board = [[0,0,0],[1,1,0],[0,1,1]], squares = [[(0,0),(2,2)], [(1,1),(2,2)]],txt = instr[4])
levels_const[6] = Level(board = [[1,1,1],[0,0,0],[0,0,0],[1,1,1]], squares = [[(0,0), (2,2)], [(1,0),(3,2)]], txt = instr[5])
levels_const[7] = Level(board = [[1,1,0,0],[1,1,0,0],[1,1,0,0],[1,1,0,1]], squares = [[(2,0),(3,1)],[(2,1),(3,2)],[(1,2),(2,3)],[(0,2),(1,3)]], txt=instr[6])
levels_const[8] = Level(board = [[1,1,1,0],[0,1,1,0],[0,1,1,1],[0,0,0,1]], squares = [[(1,0),(2,1)],[(0,1),(1,2)],[(1,2),(2,3)],[(2,1),(3,2)]])
levels_const[9] = Level(board = [[2,2,0,0],[0,1,0,0],[1,1,1,2],[0,1,0,2]], squares = [[(2,0),(3,1)],[(1,0),(3,2)],[(0,2),(1,3)]])
levels_const[10]= Level(board = [[0,1,1,1,0],[1,1,1,1,0],[1,0,0,0,0]], squares = [[(0,0),(2,2)],[(0,2),(2,4)]])
levels_const[11]= Level(board = [[2,0,0,0,1,1,0],[2,0,0,0,1,1,2],[0,0,0,0,2,2,2],[0,0,0,2,2,2,2],[1,1,1,2,2,2,2],[1,1,1,2,2,2,2],[1,1,1,2,2,2,2]], squares = [[(4,0),(6,2)],[(2,0),(4,2)],[(0,1),(2,3)],[(0,3),(1,4)],[(0,4),(1,5)]], tile_size = tile_size - 10)
levels_const[12]= Level(board = [[0,1,0,1],[1,0,1,0],[0,1,0,1],[1,0,1,0]], squares = [[(0,0),(3,3)],[(1,1),(3,3)],[(2,2),(3,3)]])
levels_const[13]= Level(board = [[1,1,1,1,1],[0,1,1,1,0],[0,1,0,1,0],[0,1,2,1,0]], squares = [[(0,0),(1,1)],[(0,1),(2,3)],[(0,3),(1,4)],[(2,0),(3,1)],[(2,3),(3,4)]])
levels_const[14]= Level(board = [[2,2,0,1,0,1],[1,0,1,0,1,0],[1,1,0,1,0,1],[1,1,1,0,1,0]], squares = [[(1,0),(3,2)],[(0,2),(3,5)],[(2,4),(3,5)]])
levels_const[15]= Level(board = [[2,2,2,1,1,0,0],[1,0,1,0,1,0,1],[0,0,0,1,0,0,0],[1,2,2,0,2,2,1],[0,1,0,1,0,1,0]], squares = [[(1,0),(4,3)],[(2,1),(3,2)],[(1,3),(4,6)],[(0,3),(1,4)]])
levels_const[16]= Level(board = [[2,2,2,1,1],[1,0,1,0,1],[0,0,0,1,0],[1,2,2,0,2],[0,1,0,1,0]], squares = [[(1,0),(4,3)],[(1,1),(4,4)],[(0,3),(1,4)]])

current = 16 # index of current level
last_level = 16

levels_const[40]= Level(board = [[0,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0]], squares = [[(1,0),(4,3)],[(0,1),(3,4)]]) # hard and really not fun


for index in range(len(levels_const)):  
    levels.append(None)
    levels[index] = copy.deepcopy(levels_const[index])

def reset_all():
    for index in range(len(levels)):
        levels[index] = copy.deepcopy(levels_const[index])
        p_dev("refresh all", index)
    p_dev("It tried refreshing all")

    current = 0

def reset_level(level_number):
    carried_over_started = False
    carried_over_started = levels[level_number].started

    levels[level_number] = copy.deepcopy(levels_const[level_number])
    levels[level_number].started = carried_over_started

    p_dev("It tried to refresh the level")


movement_allowed = False
# stores values for player circle movement commands (from arroy keys)
key_move_commands = {'up' : False, 'down' : False, 'left' : False, 'right' : False }

rot_dir = None
new_level = False
n = 0
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop

    # Path Check Algorithm
    movement_allowed = levels[current].check_path()

    if movement_allowed:
        levels[current].solved = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == MOUSEBUTTONDOWN:
            if next_level_button.Button1.pressed(pygame.mouse.get_pos()) and current < len(levels) - 1 and levels[current+1] != None:
                current += 1
            elif last_level_button.Button1.pressed(pygame.mouse.get_pos()) and current > 0:
                current -= 1
            elif reset_all_button.Button1.pressed(pygame.mouse.get_pos()):
                reset_all()
            elif levels[current].start_button != None:
                if levels[current].start_button.Button1.pressed(pygame.mouse.get_pos()):
                    levels[current].started = True


             # User pressed down on a key
        if event.type == pygame.KEYDOWN:


            if event.key == pygame.K_ESCAPE: # quit game
                pause = False
                done = True

            if event.key == pygame.K_p:
                pause = True

            while pause:

                for event in pygame.event.get():
                     if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_p:
                            pause = not pause

                        if event.key == pygame.K_ESCAPE: # quit game
                            pause = not pause
                            done = True

            if event.key == pygame.K_t:
                reset_level(current)

            if event.key == pygame.K_y and pygame.key.get_mods() and KMOD_SHIFT:
                reset_all()

            if levels[current].started:
                if event.key == pygame.K_s:  # square selector. This needs to come before the rotator below.
                    levels[current].selected -= 1
                if event.key == pygame.K_d:
                    levels[current].selected += 1

                if len(levels[current].squares) > 2:
                    if event.key == pygame.K_1:
                        levels[current].selected = 0
                    if event.key == pygame.K_2:
                        levels[current].selected = 1
                    if event.key == pygame.K_3:
                        levels[current].selected = 2
                    if event.key == pygame.K_4:
                        levels[current].selected = 3
                    if event.key == pygame.K_5:
                        levels[current].selected = 4
                    if event.key == pygame.K_6:
                        levels[current].selected = 5
                    if event.key == pygame.K_7:
                        levels[current].selected = 6
                else:
                    if event.key == pygame.K_1:
                        levels[current].selected -= 1 
                    if event.key == pygame.K_2:
                        levels[current].selected += 1

                levels[current].selected %= len(levels[current].squares) # keeps selected number within range of existing squares

                # Square rotation
                if event.key == pygame.K_k:
                    rot_dir = 1      #counter-clockwise
                    p_dev("rot_dir changed to 1")
                elif event.key == pygame.K_l:
                    rot_dir = -1     # clockwise
                    p_dev("rot_dir changed to -1")


            if movement_allowed:
                # If arrow key pressed, store that info for processing below
                if event.key == pygame.K_LEFT:
                    key_move_commands['left'] = True
                if event.key == pygame.K_RIGHT:
                    key_move_commands['right'] = True
                if event.key == pygame.K_UP:
                    key_move_commands['up'] = True
                if event.key == pygame.K_DOWN:
                    key_move_commands['down'] = True
     
        # User let up on a key
        if event.type == pygame.KEYUP:
            # If arrow key pressed, store that info for processing below
            if event.key == pygame.K_LEFT:
                key_move_commands['left'] = False
            if event.key == pygame.K_RIGHT:
                key_move_commands['right'] = False
            if event.key == pygame.K_UP:
                key_move_commands['up'] = False
            if event.key == pygame.K_DOWN:
                key_move_commands['down'] = False
    # --- Game logic should go here
    
    # Determine whether or not to move on to next level
    if levels[current].check_finished() and levels[current].started and not levels[current].completed and current < len(levels)-1:
        if levels[current+1] != None:
            levels[current].completed = True
            levels[current].player.v_x = 0 # stop player circle from moving
            levels[current].player.v_y = 0
            current += 1 # move on to next level
            key_move_commands = {'up' : False, 'down' : False, 'left' : False, 'right' : False }
        else:
            levels[current].completed = True

    if rot_dir != None: # it is crucial that this is stored before .rotate_square(rot_dir) below so that square info for animation is not destroyed
        levels[current].rotating.append(RotatingSquare(levels[current], rot_dir)) 

    # decide if and how to move player based on player keyboard arrow key input (key_move_commands)

    levels[current].set_allowed_movements()
    levels[current].set_movement(key_move_commands)
    ##

    # deals with rotating squares
    number_waiting = len(levels[current].rotating)
    if number_waiting > 0:
        p_dev("angle displacement: ", levels[current].rotating[0].angle_displacement)

        if number_waiting > 1:
            levels[current].rotating[0].rotate_speed += 15.0*levels[current].rotating[0].dir*number_waiting

        if abs(levels[current].rotating[0].angle_displacement) >= 90.0:  # if first square done rotating, pop out of list and let next square begin rotation animation
            levels[current].rotating.pop(0)
            p_dev("\nit popped out!\n")
 
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    # --- Drawing code should go here
    
    next_level_button.draw_button()
    last_level_button.draw_button()
    reset_all_button.draw_button()

    if levels[current].completed and current == last_level:
        game_completed = True
        for l in range(last_level + 1):
            if not levels[l].completed:
                game_completed = False
                break
        if game_completed:
            write_text(screen, "Game Completed! ", GREEN, 300, start_level_text_y, start_level_text_x, LevelSelector.y_val)
    else:
        write_text(screen, "Level "+str(current+1), gray(255), 300, start_level_text_y, start_level_text_x, LevelSelector.y_val)


    start_check_x = start_level_text_x + 300 + len(str(current+1))*30
    start_check_y = start_level_text_y + 40

    if levels[current].completed:
        draw_check(start_check_x, start_check_y, 40)


        #write_text(screen, + '', (200,100,100), 300, 50, start_level_text, LevelSelector.y_val)
   
    levels[current].rotate_square(rot_dir)  # sets new board tile values instantaneously
    rot_dir = None

    levels[current].draw_board()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)

    cycle += 1

 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()


"""
References:

For matrices: http://code.activestate.com/recipes/578131-a-simple-matrix-class/

http://www.emanueleferonato.com/2012/11/07/how-to-rotate-a-two-dimensional-array-by-90-degrees-clockwise-or-counter-clockwise-like-knightfall-game/

For buttons:  http://lagusan.com/button-drawer-python-2-6/

"""