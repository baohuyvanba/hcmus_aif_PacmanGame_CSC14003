#INSTALL THE GAME'S AGENT: PACMAN (), FOOD (GOAL), MONSTERS (COMPETITORS)
import pygame.image
from constant_value import *

#PACMAN -----------------------------------------------------------------------------------------------------------------------------------------------
class Pacman:
    def __init__(self, app, start_position):
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

    #Pacman Function
    def coor_to_pixel(self):
        pixel = ((self.co_or_pos[0] + 1) * 20, (self.co_or_pos[1] + 2) * 20)
        return pixel

    def pacman_call(self):
        #Call pacman for the first time
        self.display_character()

    #Display pacman go in map
    def display_character(self):
        #Display pacman
        if self.direction == s_direction_R:
            pygame.display.update(self.app.screen.blit(self.character_img_R, self.pixel_pos))
        elif self.direction == s_direction_L:
            pygame.display.update(self.app.screen.blit(self.character_img_L, self.pixel_pos))

    #Pacman Control
    def pacman_control(self, togo_pos):
        self.update(togo_pos)
        self.display_character()

    def update(self, togo_pos):
        pygame.display.update(self.app.screen.blit(self.blank_space, self.pixel_pos))
        self.get_direction(togo_pos)
        self.co_or_pos = togo_pos
        self.pixel_pos = self.coor_to_pixel()

    def get_direction(self, togo_pos):
        if togo_pos[0] - self.co_or_pos[0] == 1:      #Move Right
            self.direction = s_direction_R
        elif togo_pos[0] - self.co_or_pos[0] == -1:   #Move Left
            self.direction = s_direction_L

#GOAL/FOOD -----------------------------------------------------------------------------------------------------------------------------------------------

class Food:
    def __init__(self, app, goal_pos):
        self.app = app
        self.co_or_pos = goal_pos
        self.pixel_pos = self.coor_to_pixel()
        #Food
        self.icon_image = pygame.image.load(s_food_path)
        self.blank_space = pygame.image.load(s_blank_space)

    def coor_to_pixel(self):
        pixel = ((self.co_or_pos[0] + 1) * 20, (self.co_or_pos[1] + 2) * 20)
        return pixel

    def food_display(self):
        pygame.display.update(self.app.screen.blit(self.icon_image, self.pixel_pos))

    def food_disappear(self):
        pygame.display.update(self.app.screen.blit(self.blank_space, self.pixel_pos))


#MONSTER -----------------------------------------------------------------------------------------------------------------------------------------------

class Monster():
    def __init__(self, app, start_position):
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

        # Pacman Function

    def coor_to_pixel(self):
        pixel = ((self.co_or_pos[0] + 1) * 20, (self.co_or_pos[1] + 2) * 20)
        return pixel

    def monster_call(self):
        # Call pacman for the first time
        self.display_character()

        # Display pacman go in map

    def display_character(self):
        # Display pacman
        if self.direction == s_direction_R:
            pygame.display.update(self.app.screen.blit(self.character_img_R, self.pixel_pos))
        elif self.direction == s_direction_L:
            pygame.display.update(self.app.screen.blit(self.character_img_L, self.pixel_pos))

        # Pacman Control

    def monster_control(self, togo_pos):
        self.update(togo_pos)
        self.display_character()

    def update(self, togo_pos):
        pygame.display.update(self.app.screen.blit(self.blank_space, self.pixel_pos))
        self.get_direction(togo_pos)
        self.co_or_pos = togo_pos
        self.pixel_pos = self.coor_to_pixel()

    def get_direction(self, togo_pos):
        if togo_pos[0] - self.co_or_pos[0] == 1:  # Move Right
            self.direction = s_direction_R
        elif togo_pos[0] - self.co_or_pos[0] == -1:  # Move Left
            self.direction = s_direction_L