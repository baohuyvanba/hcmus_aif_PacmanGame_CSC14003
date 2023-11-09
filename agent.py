#INSTALL THE GAME'S AGENT: PACMAN (), FOOD (GOAL), MONSTERS (COMPETITORS)
import pygame.image
from constant_value import *

#PACMAN -----------------------------------------------------------------------------------------------------------------------------------------------
class Pacman:
    def __init__(self, app, start_position, cell=None):
        self.app = app
        #Start position
        self.co_or_pos = start_position
        self.pixel_pos = self.coor_to_pixel()
        self.direction = s_direction_R
        #Pacman
        self.character_image = pygame.image.load(s_character_path)
        self.character_img_R = pygame.image.load(s_character_R)
        self.character_img_L = pygame.image.load(s_character_L)
        self.blank_space     = pygame.image.load(s_blank_space)

        #Cell
        self.cell = cell

        #Pacman Memory
        self.detected_food = []             #Save all food detected by pacman
        self.path_to_detected_food = []     #Save pathway to detected food in memory

        # Limited visibility
        self.vision_food_list = []          # all food in pacman's threestep vision
        self.vision_mons_list = []          # all monsters in pacman's threestep vision


    #PACMAN FUNCTIONS -----------------------------------------------------------------------------

    #From Co-ordinare -> Pixel position to display
    def coor_to_pixel(self):
        pixel = ((self.co_or_pos[0] + 1) * 20, (self.co_or_pos[1] + 2) * 20)
        return pixel

    #Call pacman to display
    def pacman_call(self):
        #Call pacman for the first time
        self.display_character()

    #Display pacman in map with facing direction
    def display_character(self):
        #Display pacman
        if self.direction == s_direction_R:
            pygame.display.update(self.app.screen.blit(self.character_img_R, self.pixel_pos))
        elif self.direction == s_direction_L:
            pygame.display.update(self.app.screen.blit(self.character_img_L, self.pixel_pos))

    #Pacman control
    def pacman_control(self, togo_pos):
        self.update(togo_pos)
        self.display_character()

    #Update pacman's data with new position
    def update(self, togo_pos):
        #Fill blank space to old position
        pygame.display.update(self.app.screen.blit(self.blank_space, self.pixel_pos))
        #Get direction data
        self.get_direction(togo_pos)
        #Get position data
        self.co_or_pos = togo_pos
        self.pixel_pos = self.coor_to_pixel()

    #Get pacman direction
    def get_direction(self, togo_pos):
        if togo_pos[0] - self.co_or_pos[0] == 1:      #Move Right
            self.direction = s_direction_R
        elif togo_pos[0] - self.co_or_pos[0] == -1:   #Move Left
            self.direction = s_direction_L

#GOAL/FOOD -----------------------------------------------------------------------------------------------------------------------------------------------
class Food:
    def __init__(self, app, goal_pos, cell=None):
        self.app = app
        self.co_or_pos = goal_pos
        self.pixel_pos = self.coor_to_pixel()
        #Food
        self.icon_image = pygame.image.load(s_food_path)
        self.blank_space = pygame.image.load(s_blank_space)
        #
        self.cell = cell

    def coor_to_pixel(self):
        pixel = ((self.co_or_pos[0] + 1) * 20, (self.co_or_pos[1] + 2) * 20)
        return pixel

    def food_display(self):
        pygame.display.update(self.app.screen.blit(self.icon_image, self.pixel_pos))

    def food_disappear(self):
        pygame.display.update(self.app.screen.blit(self.blank_space, self.pixel_pos))


#MONSTER -----------------------------------------------------------------------------------------------------------------------------------------------
class Monster():
    def __init__(self, app, start_position, cell=None):
        self.app = app
        # Start position
        self.co_or_pos = start_position
        self.pixel_pos = self.coor_to_pixel()
        self.direction = s_direction_R
        # Monster
        self.character_image = pygame.image.load(s_character_monster)
        self.character_img_R = pygame.image.load(s_character_monster)
        self.character_img_L = pygame.image.load(s_character_monster)
        self.blank_space = pygame.image.load(s_blank_space)
        #
        self.cell = cell
        self.initial_cell = cell

    # Monster Function
    def coor_to_pixel(self):
        pixel = ((self.co_or_pos[0] + 1) * 20, (self.co_or_pos[1] + 2) * 20)
        return pixel

    def monster_call(self):
        self.display_character()

    def display_character(self):
        if self.direction == s_direction_R:
            pygame.display.update(self.app.screen.blit(self.character_img_R, self.pixel_pos))
        elif self.direction == s_direction_L:
            pygame.display.update(self.app.screen.blit(self.character_img_L, self.pixel_pos))

    def monster_control(self, togo_pos):
        self.update(togo_pos)
        self.display_character()

    def update(self, togo_pos):
        pygame.display.update(self.app.screen.blit(self.blank_space, self.pixel_pos))
        self.get_direction(togo_pos)
        self.co_or_pos = togo_pos
        self.pixel_pos = self.coor_to_pixel()

    def get_direction(self, togo_pos):
        if togo_pos[0] - self.co_or_pos[0] == 1:     # Move Right
            self.direction = s_direction_R
        elif togo_pos[0] - self.co_or_pos[0] == -1:  # Move Left
            self.direction = s_direction_L

    def get_around_cells_of_initial_cell(self, graph_map):
        return graph_map[self.initial_cell]

    def get_around_cells(self, graph_map):
        return graph_map[self.cell]

    def monster_disappear(self):
        pygame.display.update(self.app.screen.blit(self.blank_space, self.pixel_pos))
