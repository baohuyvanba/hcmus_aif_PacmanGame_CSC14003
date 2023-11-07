#INSTALL THE GAME'S AGENT: PACMAN (), FOOD (GOAL), MONSTERS (COMPETITORS)
import pygame.image
import localsearch as ls
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

    #Level 3 & 4 Functions
    def scan_radar(self, map_graph):
        # Reset previous scanned data
        self.vision_food_list = []
        self.vision_mons_list = []
        mons_food_cell_list = []

        # Scan surounding (threestep area)
        scanned = [self.cell]
        for neighbor_1 in map_graph[self.cell]:
            scanned.append(neighbor_1)
            if neighbor_1.food_here() and neighbor_1 not in self.vision_food_list:
                self.vision_food_list.append(neighbor_1)
            elif neighbor_1.monster_here() and neighbor_1 not in self.vision_mons_list:
                self.vision_mons_list.append(neighbor_1)

        for n1 in scanned[1:]:
            for neighbor_2 in map_graph[n1]:
                if neighbor_2 not in scanned:
                    scanned.append(neighbor_2)
                    if neighbor_2.food_here() and neighbor_2 not in self.vision_food_list:
                        self.vision_food_list.append(neighbor_2)
                    elif neighbor_2.monster_here() and neighbor_2 not in self.vision_mons_list:
                        self.vision_mons_list.append(neighbor_2)

        for n2 in scanned[5:]:
            for neighbor_3 in map_graph[n2]:
                if neighbor_3 not in scanned:
                    scanned.append(neighbor_3)
                    if neighbor_3.food_here() and neighbor_3 not in self.vision_food_list:
                        self.vision_food_list.append(neighbor_3)
                    elif neighbor_3.monster_here() and neighbor_3 not in self.vision_mons_list:
                        self.vision_mons_list.append(neighbor_3)

        # End scan

        #Find all food have monsters nearby in visibility area.
        nearby_mons_food_list = []
        for food in self.vision_food_list:
            if self.monster_arround_food_detect(food):
                nearby_mons_food_list.append(food)
        #
        food_cell_index = []
        for index in range(len(self.detected_food)):
            if self.monster_arround_food_detect(self.detected_food[index]):
                food_cell_index.append(index)
        if len(food_cell_index) != 0:
            for index in reversed(food_cell_index):
                self.detected_food.pop(index)
                self.path_to_detected_food.pop(index)
        #
        for food in nearby_mons_food_list:
            self.vision_food_list.remove(food)

        #Update Pacman intelligent
        for food in self.vision_food_list:
            for index in range(len(self.detected_food)):
                if food == self.detected_food[index]:
                    self.detected_food.remove(self.detected_food[index])
                    self.path_to_detected_food.remove(self.path_to_detected_food[index])
                    break
            self.detected_food.append(food)
            self.path_to_detected_food.append([])

    #Detect nearby monster of food cell in visibility area
    def monster_arround_food_detect(self, food_cell):
        for mons in self.vision_mons_list:
            if abs(mons.position[0] - food_cell.position[0]) + abs(mons.position[0] - food_cell.position[0]) <= 2:
                return True
        return False

    #Check if food-list is empty
    def check_detected_food(self):
        return len(self.detected_food) == 0

    #Check if food is in visibility area
    def check_food(self):
        return len(self.vision_food_list) != 0

    # Check if monster is in visibility area
    def check_monster(self):
        return len(self.vision_mons_list) != 0

    #Add
    def add_path(self, previous_cell):
        for path_to_food in self.path_to_detected_food:
            path_to_food.append(previous_cell)

    #Backtracking
    def back_track(self, map_graph):
        next_cell = self.path_to_detected_food[-1][-1]
        for path_to_food in self.path_to_detected_food:
            path_to_food.pop(-1)
        return next_cell


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
        #

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
        # Call pacman for the first time
        self.display_character()

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


    def get_around_cells_of_initial_cell(self, graph_map):
        return graph_map[self.initial_cell]

    def get_around_cells(self, graph_map):
        return graph_map[self.cell]

    def monster_disappear(self):
        pygame.display.update(self.app.screen.blit(self.blank_space, self.pixel_pos))


