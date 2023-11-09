#Display and Game|
#----------------/
import sys
import pygame
import pygame.freetype
import timeit
import random
from math import inf

import map_txt_reading as readmap
import map_txt_builder as buildmap
import astar_search as astar
import bfs_dfs_ucs_search as bdu
import agent as ag
import localsearch as ls
import alpha_beta_pruning as ab
from constant_value import *

class pacman_game:
    #INIT ---------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        pygame.init()
        #Setup window frame
        self.screen  = pygame.display.set_mode((s_display_W, s_display_H))
        self.caption = pygame.display.set_caption(s_display_caption, s_display_iconpath)

        #Load Font
        self.font    = pygame.freetype.Font(s_font_path, 16)

        #Load Display Stage
        self.mainmenu_bg  = pygame.image.load(s_display_bg)
        self.button_shade = pygame.image.load(s_button_shade)
        self.about_bg     = pygame.image.load(s_display_ab)
        self.level_bg     = pygame.image.load(s_display_lv)
        self.algo_bg      = pygame.image.load(s_display_al)
        self.map_bg       = pygame.image.load(s_display_pm)
        self.gameplay_bg  = pygame.image.load(s_display_gp)

        # Victory / GameOver Stage
        self.game_victory_bg  = pygame.image.load(s_display_victory)
        self.game_gameover_bg = pygame.image.load(s_display_gameover)

        #Button shade
        self.map_playbutton_shade = pygame.image.load(s_button_shade_mapplay)
        self.map_before_shade     = pygame.image.load(s_button_shade_map_before)
        self.map_after_shade      = pygame.image.load(s_button_shade_map_after)

        #Game play function / button shade
        self.button_playhome_shade = pygame.image.load(s_button_shade_playhome)
        self.button_playhome       = pygame.image.load(s_button_shade_playhome_clean)
        self.button_playsped_shade = pygame.image.load(s_button_shade_playsped)
        self.button_playsped       = pygame.image.load(s_button_shade_playsped_clean)
        self.button_playsped_inner = pygame.image.load(s_button_inner_playsped)
        self.score_blank           = pygame.image.load(s_score_blank)

        #Stage, Mouse and FPS Control
        self.stage = s_display_home
        self.clock = pygame.time.Clock()
        self.mouse = None

        #MAP FUNCTION
        ##Map index:
        self.map_index = 0
        ##Build map:
        for map_level in s_map_txt_path:
            for map in map_level:
                img_path = r'Resources/Game Display/map/lv' + map[22] + r'_m' + map[27] + r'.png'
                buildmap.create_maze_image(map, img_path)
            #Load first map
        self.map = pygame.image.load(s_map_gra_path[1-1][0])

        #Game logic
        self.score = 0
        self.level = 1
        self.speed = 1
        self.algorithm = s_algorithm_dfs

        #Game time
        self.time_algorithm = 0
        self.time_play      = 0

    #GAME RUNNING ------------------------------------------------------------------------------------------------------------------------------------------------
    def run(self):
        while True:
            #Main Menu
            if self.stage == s_display_home:
                #set default
                self.level = 1
                self.score = 0
                self.map_index = 0
                self.speed = 1
                #Load and display home stage
                self.mainmenu_display()
                self.mainmenu_get_action()
            #About
            elif self.stage == s_display_about:
                self.aboutinfo_display()
                self.about_get_action()
            #Pick Level
            elif self.stage == s_display_play:
                self.picklevel_display()
                self.level_get_action()
            #Pick Algorithm
            elif self.stage == s_display_al:
                self.pickalgo_display()
                self.algo_get_action()
            #Pick Map
            elif self.stage == s_display_map:
                self.pickmap_display()
                self.map_get_action()
            #Play Game
            elif self.stage == s_display_game:
                #Show gameplay stage
                self.playgame_display()
                #Set Score_value to default and Start Game
                self.score = 0
                #Show Score text
                text_surf, text_rect = self.font.render("Score", s_color_while)
                self.screen.blit(text_surf, s_pos_score)
                pygame.display.update(s_pos_score)
                #Show Speed button
                text_sped, text_rect = self.font.render("1x", s_color_while)
                self.screen.blit(text_sped, s_pos_speedvalue)
                pygame.display.update(s_pos_speedvalue)
                #run game
                if self.level == 1:
                    if self.algorithm == s_algorithm_dfs:
                        self.pacman_lv1_dfs()
                    elif self.algorithm == s_algorithm_bfs:
                        self.pacman_lv1_bfs()
                    elif self.algorithm == s_algorithm_ucs:
                        self.pacman_lv1_ucs()
                    elif self.algorithm == s_algorithm_astart:
                        self.pacman_lv1_astar()
                elif self.level == 2:
                    if self.algorithm == s_algorithm_dfs:
                        self.pacman_lv2_dfs()
                    elif self.algorithm == s_algorithm_bfs:
                        self.pacman_lv2_bfs()
                    elif self.algorithm == s_algorithm_ucs:
                        self.pacman_lv2_ucs()
                    elif self.algorithm == s_algorithm_astart:
                        self.pacman_lv2_astar()
                elif self.level == 3:
                    self.pacman_lv3()
                elif self.level == 4:
                    self.pacman_lv4()
                #
            #Victory Stage
            elif self.stage == s_display_f_vic:
                self.game_victory_screen()
                self.game_victory_action()
                pygame.display.update()
            #Game Over Stage
            elif self.stage == s_display_f_ove:
                self.game_gameover_screen()
                self.game_gameover_action()
                pygame.display.update()

            self.clock.tick(s_display_fps)

    #DISPLAY STAGE (Menu, About, Level)---------------------------------------------------------------------------------
    #Display Main_Menu
    def mainmenu_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.mainmenu_bg, (0, 0))
        pygame.display.update()

    #Display About
    def aboutinfo_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.about_bg, (0, 0))
        pygame.display.update()

    #Display Level picking
    def picklevel_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.level_bg, (0, 0))
        pygame.display.update()

    #Display Algorithm Picking (Level 1 and Level 2)
    def pickalgo_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.algo_bg, (0, 0))
        pygame.display.update()

    #Display Map picking
    def pickmap_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.map_bg, (0,0))
        self.show_map_option()
        pygame.display.update()

    def show_map_option(self):
        self.map = pygame.image.load(s_map_gra_path[self.level - 1][self.map_index])
        orix, oriy = self.map.get_size()
        oriy, orix =350*oriy/orix, 350
        pygame.display.update(self.screen.blit(pygame.transform.scale(self.map, (orix-4, oriy-4)), (125+2, 162+2)))

    # STAGE ACTION (Menu, About, Level)---------------------------------------------------------------------------------
    #Main_Screen Action
    def mainmenu_get_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if x and y
                if 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
                    self.stage = s_display_play
                elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
                    self.stage = s_display_about
                elif 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
                    pygame.quit()
                    sys.exit()
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        #Create Button Shade
        if 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
            self.screen.blit(self.button_shade, (220, 350))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
            self.screen.blit(self.button_shade, (220, 440))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
            self.screen.blit(self.button_shade, (220, 530))
            pygame.display.update()

    # About_Screen Action
    def about_get_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
                    self.stage = s_display_home
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
            #self.screen.blit(self.button_shade, (220, 530))
            pygame.display.update(self.screen.blit(self.button_shade, (220, 530)))

    #Level_Screen Action
    def level_get_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Back
                if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
                    self.stage = s_display_home
                #Level 1
                elif 220 <= self.mouse[0] <= 380 and 170 <= self.mouse[1] <= 230:
                    self.stage = s_display_al
                    self.level = 1
                #Level 2
                elif 220 <= self.mouse[0] <= 380 and 260 <= self.mouse[1] <= 320:
                    self.stage = s_display_al
                    self.level = 2
                #Level 3
                elif 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
                    self.stage = s_display_map
                    self.level = 3
                #Level 4
                elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
                    self.stage = s_display_map
                    self.level = 4
            # Quit game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
            self.screen.blit(self.button_shade, (220, 530))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 170 <= self.mouse[1] <= 230:
            self.screen.blit(self.button_shade, (220, 170))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 260 <= self.mouse[1] <= 320:
            self.screen.blit(self.button_shade, (220, 260))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
            self.screen.blit(self.button_shade, (220, 350))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
            self.screen.blit(self.button_shade, (220, 440))
            pygame.display.update()

    #Algorithm_Screen Action
    def algo_get_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Back
                if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
                    self.stage = s_display_lv
                #dfs
                elif 220 <= self.mouse[0] <= 380 and 170 <= self.mouse[1] <= 230:
                    self.stage = s_display_map
                    self.algorithm = s_algorithm_dfs
                #bfs
                elif 220 <= self.mouse[0] <= 380 and 260 <= self.mouse[1] <= 320:
                    self.stage = s_display_map
                    self.algorithm = s_algorithm_bfs
                #ucs
                elif 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
                    self.stage = s_display_map
                    self.algorithm = s_algorithm_ucs
                #astar
                elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
                    self.stage = s_display_map
                    self.algorithm = s_algorithm_astart
            # Quit game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 220 <= self.mouse[0] <= 380 and 530 <= self.mouse[1] <= 590:
            self.screen.blit(self.button_shade, (220, 530))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 170 <= self.mouse[1] <= 230:
            self.screen.blit(self.button_shade, (220, 170))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 260 <= self.mouse[1] <= 320:
            self.screen.blit(self.button_shade, (220, 260))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
            self.screen.blit(self.button_shade, (220, 350))
            pygame.display.update()
        elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
            self.screen.blit(self.button_shade, (220, 440))
            pygame.display.update()

    #Map_Screen Action
    def map_get_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Play
                if 251 <= self.mouse[0] <= 349 and 555 <= self.mouse[1] <= 603:
                    self.stage = s_display_game
                #Before
                elif 186 <= self.mouse[0] <= 234 and 555 <= self.mouse[1] <= 603:
                    if self.map_index == 0:
                        self.map_index = 4
                    else:
                        self.map_index -= 1
                #After
                elif 366 <= self.mouse[0] <= 414 and 555 <= self.mouse[1] <= 603:
                    if self.map_index == 4:
                        self.map_index = 0
                    else:
                        self.map_index += 1
                #Back
                elif 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
                    self.stage = s_display_play
            # Quit game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 251 <= self.mouse[0] <= 349 and 555 <= self.mouse[1] <= 603:
            pygame.display.update(self.screen.blit(self.map_playbutton_shade, (250, 554)))
        elif 186 <= self.mouse[0] <= 234 and 555 <= self.mouse[1] <= 603:
            pygame.display.update(self.screen.blit(self.map_before_shade, (185, 554)))
        elif 366 <= self.mouse[0] <= 414 and 555 <= self.mouse[1] <= 603:
            pygame.display.update(self.screen.blit(self.map_after_shade, (365, 554)))
        elif 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
            pygame.display.update(self.screen.blit(self.map_playbutton_shade, (250, 624)))

    # GAME LEVEL PLAY --------------------------------------------------------------------------------------------------
    #Play Game Display
    def playgame_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.gameplay_bg, (0, 0))
        #LOAD MAP
        self.screen.blit(self.map, (20, 40))
        pygame.display.update()

    #Play Game Action
    def play_get_action(self):
        #Detect event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Home button
                if 480 <= self.mouse[0] <= 540 and 661 <= self.mouse[1] <= 681:
                    self.stage = s_display_home
                #Speed button
                elif 550 <= self.mouse[0] <= 580 and 661 <= self.mouse[1] <= 681:
                    #change game speed (change delay time)
                    if self.speed == 1:
                        self.speed = 2
                        pygame.display.update(self.screen.blit(self.button_playsped_inner, (549, 664)))
                        text_sped, text_rect = self.font.render("2x", s_color_while)
                        self.screen.blit(text_sped, s_pos_speedvalue)
                        pygame.display.update(s_pos_speedvalue)
                    elif self.speed == 2:
                        self.speed = 4
                        pygame.display.update(self.screen.blit(self.button_playsped_inner, (549, 664)))
                        text_sped, text_rect = self.font.render("4x", s_color_while)
                        self.screen.blit(text_sped, s_pos_speedvalue)
                        pygame.display.update(s_pos_speedvalue)
                    elif self.speed == 4:
                        self.speed = 1
                        pygame.display.update(self.screen.blit(self.button_playsped_inner, (549, 664)))
                        text_sped, text_rect = self.font.render("1x", s_color_while)
                        self.screen.blit(text_sped, s_pos_speedvalue)
                        pygame.display.update(s_pos_speedvalue)

        #Create button shade
        self.mouse = pygame.mouse.get_pos()
        if 480 <= self.mouse[0] <= 540 and 661 <= self.mouse[1] <= 681:
            pygame.display.update(self.screen.blit(self.button_playhome_shade, (479, 660)))
        elif 550 <= self.mouse[0] <= 580 and 661 <= self.mouse[1] <= 681:
            pygame.display.update(self.screen.blit(self.button_playsped_shade, (549, 660)))
        else:
            pygame.display.update(self.screen.blit(self.button_playhome, (479, 660)))
            pygame.display.update(self.screen.blit(self.button_playsped, (549, 660)))

        if self.stage == s_display_home:
            return True
        return False

    #LEVEL FUNCTION ====================================================================================================
    # Level 1-----------------------------------------------------------------------------------------------------------
    def pacman_lv1_astar(self):
        graph_map, pacman_pos, food_pos = readmap.map_level1(s_map_txt_path[self.level - 1][self.map_index])

        self.time_algorithm = 0
        self.time_play = 0

        start = timeit.default_timer()
        # Run A*
        pathway = astar.astar_search(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

        # Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        # Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        # Call Monster: No

        # Have pathway to goal
        if pathway is not None:
            # Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)
            go_home = 0
            # Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay // self.speed)
                # Detect event during playing game
                if self.play_get_action():
                    go_home = 1
                    break
                else:
                    go_home = 0

            # Go to goal (if not pressed go home button)
            if go_home != 1:
                food.food_disappear()
                pacman.pacman_control(goal)
                self.pacman_scoring(s_score_gift)
                pygame.time.delay(2000)
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_home
                print("Algorithm run time: ", self.time_algorithm)
        # Have no pathway to goal
        else:
            self.stage = s_display_f_ove
            print("Algorithm run time: ", self.time_algorithm)

    def pacman_lv1_bfs(self):
        graph_map, pacman_pos, food_pos = readmap.map_level1(s_map_txt_path[self.level - 1][self.map_index])

        self.time_algorithm = 0
        self.time_play = 0

        start = timeit.default_timer()
        # Run A*
        pathway = bdu.bfs(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

        # Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        # Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        # Call Monster: No

        # Have pathway to goal
        if pathway is not None:
            # Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)
            go_home = 0
            # Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay // self.speed)
                # Detect event during playing game
                if self.play_get_action():
                    go_home = 1
                    break
                else:
                    go_home = 0

            # Go to goal (if not pressed go home button)
            if go_home != 1:
                food.food_disappear()
                pacman.pacman_control(goal)
                self.pacman_scoring(s_score_gift)
                pygame.time.delay(2000)
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_home
                print("Algorithm run time: ", self.time_algorithm)
        # Have no pathway to goal
        else:
            self.stage = s_display_f_ove
            print("Algorithm run time: ", self.time_algorithm)

    def pacman_lv1_dfs(self):
        graph_map, pacman_pos, food_pos = readmap.map_level1(s_map_txt_path[self.level - 1][self.map_index])

        self.time_algorithm = 0
        self.time_play = 0

        start = timeit.default_timer()
        # Run A*
        pathway = bdu.dfs(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

        # Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        # Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        # Call Monster: No

        # Have pathway to goal
        if pathway is not None:
            # Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)
            go_home = 0
            # Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay // self.speed)
                # Detect event during playing game
                if self.play_get_action():
                    go_home = 1
                    break
                else:
                    go_home = 0

            # Go to goal (if not pressed go home button)
            if go_home != 1:
                food.food_disappear()
                pacman.pacman_control(goal)
                self.pacman_scoring(s_score_gift)
                pygame.time.delay(2000)
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_home
                print("Algorithm run time: ", self.time_algorithm)
        # Have no pathway to goal
        else:
            self.stage = s_display_f_ove
            print("Algorithm run time: ", self.time_algorithm)

    def pacman_lv1_ucs(self):
        graph_map, pacman_pos, food_pos = readmap.map_level1(s_map_txt_path[self.level - 1][self.map_index])

        self.time_algorithm = 0
        self.time_play = 0

        start = timeit.default_timer()
        # Run A*
        pathway = bdu.ucs(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

        # Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        # Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        # Call Monster: No

        # Have pathway to goal
        if pathway is not None:
            # Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)
            go_home = 0
            # Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay // self.speed)
                # Detect event during playing game
                if self.play_get_action():
                    go_home = 1
                    break
                else:
                    go_home = 0

            # Go to goal (if not pressed go home button)
            if go_home != 1:
                food.food_disappear()
                pacman.pacman_control(goal)
                self.pacman_scoring(s_score_gift)
                pygame.time.delay(2000)
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_home
                print("Algorithm run time: ", self.time_algorithm)
        # Have no pathway to goal
        else:
            self.stage = s_display_f_ove
            print("Algorithm run time: ", self.time_algorithm)

    # Level 2-----------------------------------------------------------------------------------------------------------
    def pacman_lv2_astar(self):
        graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(s_map_txt_path[self.level-1][self.map_index], True)

        self.time_algorithm = 0
        self.time_play = 0

        start = timeit.default_timer()
        #Run A*
        pathway = astar.astar_search(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

        # Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        # Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        # Call Monster
        monsters = [ag.Monster(self, pos) for pos in monsters_pos_list]
        for mons in monsters:
            mons.monster_call()

        start = timeit.default_timer()
        if pathway is not None:
            # Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)

            #Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay // self.speed)
                #Detect event during playing game
                if self.play_get_action():
                    go_home = 1
                    break
                else:
                    go_home = 0

            #Go to goal (if not pressed go home button)
            if go_home != 1:
                food.food_disappear()
                pacman.pacman_control(goal)
                self.pacman_scoring(s_score_gift)
                pygame.time.delay(2000)
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_home
                print("Algorithm run time: ", self.time_algorithm)

        #No possible pathway exists with monster is considered as wall. So, just go and die X_X, 100% game over
        else:
            #Build again without fake wall
            graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(s_map_txt_path[self.level - 1][self.map_index], False)
            start = timeit.default_timer()
            #Run A*
            pathway = astar.astar_search(graph_map, pacman_pos, food_pos)
            self.time_algorithm = timeit.default_timer() - start
            #
            if pathway is not None:
                # Set pathway, score(0)
                goal = pathway[-1]
                pathway_togoal = pathway[1:-1]
                self.pacman_scoring(0)
                pygame.time.delay(500)

                # Go
                for loc in pathway_togoal:
                    pacman.pacman_control(loc)
                    self.pacman_scoring(s_score_move)
                    pygame.time.delay(s_time_delay // self.speed)
                    # Detect event during playing game
                    if self.play_get_action():
                        go_home = 1
                        break
                    else:
                        go_home = 0

                    if loc in monsters_pos_list:
                        break

                # Go to goal (if possible)
                if go_home != 1:
                    pygame.time.delay(200)
                    self.stage = s_display_f_ove
                    print("Algorithm run time: ", self.time_algorithm)
                else:
                    self.stage = s_display_home
                    print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_f_ove
                print("Algorithm run time: ", self.time_algorithm)

    def pacman_lv2_bfs(self):
        graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(
            s_map_txt_path[self.level - 1][self.map_index], True)

        self.time_algorithm = 0
        self.time_play = 0

        start = timeit.default_timer()
        # Run BFS
        pathway = bdu.bfs(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

        # Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        # Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        # Call Monster
        monsters = [ag.Monster(self, pos) for pos in monsters_pos_list]
        for mons in monsters:
            mons.monster_call()

        start = timeit.default_timer()
        if pathway is not None:
            # Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)

            # Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay // self.speed)
                # Detect event during playing game
                if self.play_get_action():
                    go_home = 1
                    break
                else:
                    go_home = 0

            # Go to goal (if not pressed go home button)
            if go_home != 1:
                food.food_disappear()
                pacman.pacman_control(goal)
                self.pacman_scoring(s_score_gift)
                pygame.time.delay(2000)
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_home
                print("Algorithm run time: ", self.time_algorithm)

        # No possible pathway exists with monster is considered as wall. So, just go and die X_X, 100% game over
        else:
            # Build again without fake wall
            graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(
                s_map_txt_path[self.level - 1][self.map_index], False)
            start = timeit.default_timer()
            # Run BFS
            pathway = bdu.bfs(graph_map, pacman_pos, food_pos)
            self.time_algorithm = timeit.default_timer() - start
            #
            if pathway is not None:
                # Set pathway, score(0)
                goal = pathway[-1]
                pathway_togoal = pathway[1:-1]
                self.pacman_scoring(0)
                pygame.time.delay(500)

                # Go
                for loc in pathway_togoal:
                    pacman.pacman_control(loc)
                    self.pacman_scoring(s_score_move)
                    pygame.time.delay(s_time_delay // self.speed)
                    # Detect event during playing game
                    if self.play_get_action():
                        go_home = 1
                        break
                    else:
                        go_home = 0

                    if loc in monsters_pos_list:
                        break

                # Go to goal (if possible)
                if go_home != 1:
                    pygame.time.delay(200)
                    self.stage = s_display_f_ove
                    print("Algorithm run time: ", self.time_algorithm)
                else:
                    self.stage = s_display_home
                    print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_f_ove
                print("Algorithm run time: ", self.time_algorithm)

    def pacman_lv2_dfs(self):
        graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(
            s_map_txt_path[self.level - 1][self.map_index], True)

        self.time_algorithm = 0
        self.time_play = 0

        start = timeit.default_timer()
        # Run DFS
        pathway = bdu.dfs(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

        # Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        # Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        # Call Monster
        monsters = [ag.Monster(self, pos) for pos in monsters_pos_list]
        for mons in monsters:
            mons.monster_call()

        start = timeit.default_timer()
        if pathway is not None:
            # Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)

            # Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay // self.speed)
                # Detect event during playing game
                if self.play_get_action():
                    go_home = 1
                    break
                else:
                    go_home = 0

            # Go to goal (if not pressed go home button)
            if go_home != 1:
                food.food_disappear()
                pacman.pacman_control(goal)
                self.pacman_scoring(s_score_gift)
                pygame.time.delay(2000)
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_home
                print("Algorithm run time: ", self.time_algorithm)

        # No possible pathway exists with monster is considered as wall. So, just go and die X_X, 100% game over
        else:
            # Build again without fake wall
            graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(
                s_map_txt_path[self.level - 1][self.map_index], False)
            start = timeit.default_timer()
            # Run DFS
            pathway = bdu.dfs(graph_map, pacman_pos, food_pos)
            self.time_algorithm = timeit.default_timer() - start
            #
            if pathway is not None:
                # Set pathway, score(0)
                goal = pathway[-1]
                pathway_togoal = pathway[1:-1]
                self.pacman_scoring(0)
                pygame.time.delay(500)

                # Go
                for loc in pathway_togoal:
                    pacman.pacman_control(loc)
                    self.pacman_scoring(s_score_move)
                    pygame.time.delay(s_time_delay // self.speed)
                    # Detect event during playing game
                    if self.play_get_action():
                        go_home = 1
                        break
                    else:
                        go_home = 0

                    if loc in monsters_pos_list:
                        break

                # Go to goal (if possible)
                if go_home != 1:
                    pygame.time.delay(200)
                    self.stage = s_display_f_ove
                    print("Algorithm run time: ", self.time_algorithm)
                else:
                    self.stage = s_display_home
                    print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_f_ove
                print("Algorithm run time: ", self.time_algorithm)

    def pacman_lv2_ucs(self):
        graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(
            s_map_txt_path[self.level - 1][self.map_index], True)

        self.time_algorithm = 0
        self.time_play = 0

        start = timeit.default_timer()
        # Run UCS
        pathway = bdu.ucs(graph_map, pacman_pos, food_pos)
        #
        self.time_algorithm = timeit.default_timer() - start

        # Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        # Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        # Call Monster
        monsters = [ag.Monster(self, pos) for pos in monsters_pos_list]
        for mons in monsters:
            mons.monster_call()

        start = timeit.default_timer()
        if pathway is not None:
            # Set pathway, score(0)
            goal = pathway[-1]
            pathway_togoal = pathway[1:-1]
            self.pacman_scoring(0)
            pygame.time.delay(500)

            # Go
            for loc in pathway_togoal:
                pacman.pacman_control(loc)
                self.pacman_scoring(s_score_move)
                pygame.time.delay(s_time_delay // self.speed)
                # Detect event during playing game
                if self.play_get_action():
                    go_home = 1
                    break
                else:
                    go_home = 0

            # Go to goal (if not pressed go home button)
            if go_home != 1:
                food.food_disappear()
                pacman.pacman_control(goal)
                self.pacman_scoring(s_score_gift)
                pygame.time.delay(2000)
                self.time_play = timeit.default_timer() - start
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_home
                print("Algorithm run time: ", self.time_algorithm)

        # No possible pathway exists with monster is considered as wall. So, just go and die X_X, 100% game over
        else:
            # Build again without fake wall
            graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(
                s_map_txt_path[self.level - 1][self.map_index], False)
            start = timeit.default_timer()
            # Run UCS
            pathway = bdu.ucs(graph_map, pacman_pos, food_pos)
            self.time_algorithm = timeit.default_timer() - start
            #
            if pathway is not None:
                # Set pathway, score(0)
                goal = pathway[-1]
                pathway_togoal = pathway[1:-1]
                self.pacman_scoring(0)
                pygame.time.delay(500)

                # Go
                for loc in pathway_togoal:
                    pacman.pacman_control(loc)
                    self.pacman_scoring(s_score_move)
                    pygame.time.delay(s_time_delay // self.speed)
                    # Detect event during playing game
                    if self.play_get_action():
                        go_home = 1
                        break
                    else:
                        go_home = 0

                    if loc in monsters_pos_list:
                        break

                # Go to goal (if possible)
                if go_home != 1:
                    pygame.time.delay(200)
                    self.stage = s_display_f_ove
                    print("Algorithm run time: ", self.time_algorithm)
                else:
                    self.stage = s_display_home
                    print("Algorithm run time: ", self.time_algorithm)
            else:
                self.stage = s_display_f_ove
                print("Algorithm run time: ", self.time_algorithm)

    # Level 3-----------------------------------------------------------------------------------------------------------
    def pacman_lv3(self):
        graph_map, pacman_pos, foods_pos, monster_list = readmap.map_level3(
            s_map_txt_path[self.level - 1][self.map_index])
        count = 0  # Number of points need to get

        self.time_play = 0
        self.time_algorithm = 0

        # Call Pacman
        pacman_pos_draw = [pacman_pos[1], pacman_pos[0]]
        pacman = ag.Pacman(self, pacman_pos_draw)
        pacman.pacman_call()
        # Call Food
        for foods_pos_t in foods_pos:
            foods_pos_draw_t = [foods_pos_t[1], foods_pos_t[0]]
            food = ag.Food(self, foods_pos_draw_t)
            food.food_display()
        # Call Monster
        monsters = [ag.Monster(self, [pos[1], pos[0]]) for pos in list(monster_list.keys())]
        for mons in monsters:
            mons.monster_call()

        pre_pos = None
        time_visits = {}
        for key in list(graph_map.keys()):
            time_visits[key] = 0
        index = 0
        parity_index_monster = 0  # to keep monster in this 5 cells

        # Preprocessing
        # Position of monsters
        old_pos = []
        for name in list(monster_list.keys()):
            old_pos.append(name)

        new_pos = old_pos.copy()
        keys_monster = list(monster_list.keys())

        # Heuristics
        heuristic_call = {}
        start = timeit.default_timer()
        for pos in graph_map[pacman_pos]:
            heuristic_call[pos] = ls.heuristic_lv3_2around(pacman_pos, graph_map, pos, foods_pos, old_pos)
        heuristic_call = dict(sorted(heuristic_call.items(), key=lambda item: item[1], reverse=True))
        self.time_algorithm = timeit.default_timer() - start
        catch = 0
        go_home = 0
        while True:
            # Display pacman
            new_pacman_pos = list(heuristic_call.keys())[0]
            if new_pacman_pos in foods_pos:
                count += 1
                food = ag.Food(self, (new_pacman_pos[1], new_pacman_pos[0]))
                food.food_disappear()
                self.pacman_scoring(s_score_gift)
                foods_pos.remove(new_pacman_pos)

            if len(foods_pos) == 0:
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
                break

            pre_pos = pacman_pos
            pacman_pos = new_pacman_pos
            pacman.pacman_control([pacman_pos[1], pacman_pos[0]])
            self.pacman_scoring(s_score_move)

            for pos in new_pos:
                if (pacman.co_or_pos[1], pacman.co_or_pos[0]) == pos:
                    catch = 1
                    break

            parity_index_monster += 1
            backup_old_pos = old_pos.copy()

            # for element in list(monster_list.keys()):
            for i in range(len(monster_list)):
                element = keys_monster[i]
                if (parity_index_monster % 2 == 1):
                    old_pos[i] = element
                    size = len(monster_list[element])
                    num = random.randint(0, size - 1)
                    new_pos[i] = (monster_list[element][num][0], monster_list[element][num][1])

                    if ((old_pos[i][0], old_pos[i][1]) in foods_pos):
                        foods_pos_draw_t = [old_pos[i][1], old_pos[i][0]]
                        food = ag.Food(self, foods_pos_draw_t)
                        food.food_display()

                    monster = ag.Monster(self, (old_pos[i][1], old_pos[i][0]))
                    monster.monster_control([new_pos[i][1], new_pos[i][0]])

                    if monster.co_or_pos == pacman.co_or_pos:
                        catch = 1
                        break

                    old_pos[i] = new_pos[i]
                else:
                    if ((old_pos[i][0], old_pos[i][1]) in foods_pos):
                        foods_pos_draw_t = [old_pos[i][1], old_pos[i][0]]
                        food = ag.Food(self, foods_pos_draw_t)
                        food.food_display()

                    new_pos[i] = element
                    monster = ag.Monster(self, (old_pos[i][1], old_pos[i][0]))
                    monster.monster_control([new_pos[i][1], new_pos[i][0]])

                    if monster.co_or_pos == pacman.co_or_pos:
                        catch = 1
                        break

                    old_pos[i] = new_pos[i]

            if catch == 1:
                self.stage = s_display_f_ove
                break

            # Calculate heuristic for next move
            heuristic_call = {}
            start = timeit.default_timer()
            for pos in graph_map[pacman_pos]:
                if pos == pre_pos:
                    time_visits[pos] += 2
                else:
                    time_visits[pos] += 1
                heuristic_call[pos] = (-1) * time_visits[pos] + ls.heuristic_lv3_2around(pacman_pos, graph_map, pos,
                                                                                         foods_pos, old_pos)

            heuristic_call = dict(sorted(heuristic_call.items(), key=lambda item: item[1], reverse=True))
            self.time_algorithm += (timeit.default_timer() - start)
            backup_heuristic = heuristic_call

            # Detect event during playing game
            if self.play_get_action():
                go_home = 1
                break
            else:
                go_home = 0

            pygame.time.delay(s_time_delay // self.speed)

        if catch == 1:
            self.stage = s_display_f_ove
            print("Algorithm run time: ", self.time_algorithm)

        if go_home == 1:
            self.stage = s_display_home
            print("Algorithm run time: ", self.time_algorithm)


    # def pacman_lv3(self):
    #     graph_map, pacman_pos, foods_pos, monster_list = readmap.map_level3(s_map_txt_path[self.level - 1][self.map_index])
    #     count = 0  # Number of points need to get
    #
    #     self.time_play = 0
    #     self.time_algorithm = 0
    #
    #     # Call Pacman
    #     pacman_pos_draw = [pacman_pos[1], pacman_pos[0]]
    #     pacman = ag.Pacman(self, pacman_pos_draw)
    #     pacman.pacman_call()
    #     # Call Food
    #     for foods_pos_t in foods_pos:
    #         foods_pos_draw_t = [foods_pos_t[1], foods_pos_t[0]]
    #         food = ag.Food(self, foods_pos_draw_t)
    #         food.food_display()
    #     # Call Monster
    #     monsters = [ag.Monster(self, [pos[1], pos[0]]) for pos in list(monster_list.keys())]
    #     for mons in monsters:
    #         mons.monster_call()
    #
    #     pre_pos = None
    #     time_visits = {}
    #     for key in list(graph_map.keys()):
    #         time_visits[key] = 0
    #     index = 0
    #     parity_index_monster = 0  # to keep monster in this 5 cells
    #
    #     # Preprocessing
    #     # Position of monsters
    #     old_pos = []
    #     for name in list(monster_list.keys()):
    #         old_pos.append(name)
    #
    #     new_pos = old_pos.copy()
    #     keys_monster = list(monster_list.keys())
    #
    #     # Heuristics
    #     heuristic_call = {}
    #     start = timeit.default_timer()
    #     for pos in graph_map[pacman_pos]:
    #         heuristic_call[pos] = ls.heuristic_lv3_2around(pacman_pos, graph_map, pos, foods_pos, old_pos)
    #     heuristic_call = dict(sorted(heuristic_call.items(), key=lambda item: item[1], reverse=True))
    #     self.time_algorithm = timeit.default_timer() - start
    #     catch = 0
    #     go_home = 0
    #     while True:
    #         # Display pacman
    #         new_pacman_pos = list(heuristic_call.keys())[0]
    #         if new_pacman_pos in foods_pos:
    #             count += 1
    #             food = ag.Food(self, (new_pacman_pos[1], new_pacman_pos[0]))
    #             food.food_disappear()
    #             self.pacman_scoring(s_score_gift)
    #             foods_pos.remove(new_pacman_pos)
    #
    #         if len(foods_pos) == 0:
    #             self.stage = s_display_f_vic
    #             print("Algorithm run time: ", self.time_algorithm)
    #             break
    #
    #         pre_pos = pacman_pos
    #         pacman_pos = new_pacman_pos
    #         pacman.pacman_control([pacman_pos[1], pacman_pos[0]])
    #         self.pacman_scoring(s_score_move)
    #
    #         for pos in new_pos:
    #             if (pacman.co_or_pos[1], pacman.co_or_pos[0]) == pos:
    #                 catch = 1
    #                 break
    #
    #         parity_index_monster += 1
    #         backup_old_pos = old_pos.copy()
    #
    #         # for element in list(monster_list.keys()):
    #         for i in range(len(monster_list)):
    #             element = keys_monster[i]
    #             if (parity_index_monster % 2 == 1):
    #                 old_pos[i] = element
    #                 size = len(monster_list[element])
    #                 num = random.randint(0, size - 1)
    #                 new_pos[i] = (monster_list[element][num][0], monster_list[element][num][1])
    #
    #                 if ((old_pos[i][0], old_pos[i][1]) in foods_pos):
    #                     foods_pos_draw_t = [old_pos[i][1], old_pos[i][0]]
    #                     food = ag.Food(self, foods_pos_draw_t)
    #                     food.food_display()
    #
    #                 monster = ag.Monster(self, (old_pos[i][1], old_pos[i][0]))
    #                 monster.monster_control([new_pos[i][1], new_pos[i][0]])
    #
    #                 if monster.co_or_pos == pacman.co_or_pos:
    #                     catch = 1
    #                     break
    #
    #                 old_pos[i] = new_pos[i]
    #             else:
    #                 if ((old_pos[i][0], old_pos[i][1]) in foods_pos):
    #                     foods_pos_draw_t = [old_pos[i][1], old_pos[i][0]]
    #                     food = ag.Food(self, foods_pos_draw_t)
    #                     food.food_display()
    #
    #                 new_pos[i] = element
    #                 monster = ag.Monster(self, (old_pos[i][1], old_pos[i][0]))
    #                 monster.monster_control([new_pos[i][1], new_pos[i][0]])
    #
    #                 if monster.co_or_pos == pacman.co_or_pos:
    #                     catch = 1
    #                     break
    #
    #                 old_pos[i] = new_pos[i]
    #
    #         if catch == 1:
    #             self.stage = s_display_f_ove
    #             break
    #
    #         # Calculate heuristic for next move
    #         heuristic_call = {}
    #         start = timeit.default_timer()
    #         for pos in graph_map[pacman_pos]:
    #             if pos == pre_pos:
    #                 time_visits[pos] += 2
    #             else:
    #                 time_visits[pos] += 1
    #             heuristic_call[pos] = (-1) * time_visits[pos] + ls.heuristic_lv3_2around(pacman_pos, graph_map, pos, foods_pos, old_pos)
    #
    #         heuristic_call = dict(sorted(heuristic_call.items(), key=lambda item: item[1], reverse=True))
    #         self.time_algorithm += (timeit.default_timer() - start)
    #         backup_heuristic = heuristic_call
    #
    #         # Detect event during playing game
    #         if self.play_get_action():
    #             go_home = 1
    #             break
    #         else:
    #             go_home = 0
    #
    #         pygame.time.delay(s_time_delay // self.speed)
    #
    #     if catch == 1:
    #         self.stage = s_display_f_ove
    #         print("Algorithm run time: ", self.time_algorithm)
    #
    #     if go_home == 1:
    #         self.stage = s_display_home
    #         print("Algorithm run time: ", self.time_algorithm)

    # Level 4-----------------------------------------------------------------------------------------------------------
    def pacman_lv4(self):
        graph_map, pacman_pos, foods_pos, monster_list = readmap.map_level4(
            s_map_txt_path[self.level - 1][self.map_index])
        # Call Pacman
        pacman_pos_draw = [pacman_pos[1], pacman_pos[0]]
        pacman = ag.Pacman(self, pacman_pos_draw)
        pacman.pacman_call()
        # Call Food
        for foods_pos_t in foods_pos:
            foods_pos_draw_t = [foods_pos_t[1], foods_pos_t[0]]
            food = ag.Food(self, foods_pos_draw_t)
            food.food_display()
        # Call Monster
        monsters = [ag.Monster(self, [pos[1], pos[0]]) for pos in list(monster_list.keys())]
        for mons in monsters:
            mons.monster_call()

        self.time_play = 0
        self.time_algorithm = 0

        # Declare some temp
        keys_monster = list(monster_list.keys())
        point = 0
        time_visits = {}
        pre_pos = (-1, -1)
        game_state = ab.GameState(pacman_pos, foods_pos, keys_monster, point, time_visits, pre_pos)

        for key in list(graph_map.keys()):
            game_state.time_visits[key] = 0

        best_move = None
        best_score = float('-inf')
        depth = 16
        go_home = 0
        catch = 0
        while True:
            pygame.event.pump()
            if len(foods_pos) == 0:
                self.stage = s_display_f_vic
                break

            #Pacman
            start = timeit.default_timer()
            eval, best_move = ab.alpha_beta(graph_map, game_state, depth, 1, -inf, inf)
            self.time_algorithm += timeit.default_timer() - start
            game_state.pre_pos = game_state.pacman_pos
            if best_move in foods_pos:
                food = ag.Food(self, (best_move[1], best_move[0]))
                self.pacman_scoring(s_score_gift)
                food.food_disappear()
                foods_pos.remove(best_move)
            game_state.pacman_pos = best_move
            pacman_pos_draw = [best_move[1], best_move[0]]
            self.pacman_scoring(s_score_move)
            pacman.pacman_control(pacman_pos_draw)
            game_state.time_visits[best_move] += 1

            for pos in game_state.monsters_pos:
                if pacman.co_or_pos == (pos[0], pos[1]):
                    catch = 1
                    self.stage = s_display_f_ove
                    break

            # Monster
            start = timeit.default_timer()
            best_move_monster = ab.get_moves(graph_map, game_state, 0).monsters_pos
            self.time_algorithm += timeit.default_timer() - start
            random_move_monster = game_state.get_monster_move(graph_map)
            for j in range(len(game_state.monsters_pos)):
                k = random.randint(0, 1)
                if k == 0:
                    monster = ag.Monster(self, (game_state.monsters_pos[j][1], game_state.monsters_pos[j][0]))
                    monster.monster_disappear()

                    if (game_state.monsters_pos[j][0], game_state.monsters_pos[j][1]) in foods_pos:
                        foods_pos_draw_t = [game_state.monsters_pos[j][1], game_state.monsters_pos[j][0]]
                        food = ag.Food(self, foods_pos_draw_t)
                        food.food_display()

                    game_state.monsters_pos[j] = best_move_monster[j]
                    monster = ag.Monster(self, (game_state.monsters_pos[j][1], game_state.monsters_pos[j][0]))
                    monster.monster_control([game_state.monsters_pos[j][1], game_state.monsters_pos[j][0]])

                    if monster.co_or_pos == pacman.co_or_pos:
                        catch = 1
                        self.stage = s_display_f_ove
                        break
                else:
                    monster = ag.Monster(self, (game_state.monsters_pos[j][1], game_state.monsters_pos[j][0]))
                    monster.monster_disappear()

                    if (game_state.monsters_pos[j][0], game_state.monsters_pos[j][1]) in foods_pos:
                        foods_pos_draw_t = [game_state.monsters_pos[j][1], game_state.monsters_pos[j][0]]
                        food = ag.Food(self, foods_pos_draw_t)
                        food.food_display()

                    game_state.monsters_pos[j] = random_move_monster[j]
                    monster = ag.Monster(self, (game_state.monsters_pos[j][1], game_state.monsters_pos[j][0]))
                    monster.monster_control([game_state.monsters_pos[j][1], game_state.monsters_pos[j][0]])

                    if monster.co_or_pos == pacman.co_or_pos:
                        catch = 1
                        self.stage = s_display_f_ove
                        break

            if catch == 1:
                print("Algorithm run time: ", self.time_algorithm)
                break

            # Detect event during playing game
            if self.play_get_action():
                go_home = 1
                break
            else:
                go_home = 0
            if len(foods_pos) == 0:
                self.stage = s_display_f_vic
                print("Algorithm run time: ", self.time_algorithm)
                break
            pygame.time.delay(s_time_delay // self.speed)

        if go_home == 1:
            self.stage = s_display_home
            print("Algorithm run time: ", self.time_algorithm)

    #Scoring------------------------------------------------------------------------------------------------------------
    def pacman_scoring(self, score):
        #Write
        self.score += score
        if self.stage == s_display_game:
            pygame.display.update(self.screen.blit(self.score_blank, (s_pos_scorevalue[0], s_pos_scorevalue[1])))
            text_score, text_rect_score = self.font.render(str(self.score), s_color_while)
            self.screen.blit(text_score, s_pos_scorevalue)
            pygame.display.update(s_pos_scorevalue)

    #FINISH ------------------------------------------------------------------------------------------------------------
    def game_victory_screen(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.game_victory_bg, (0, 0))

        score_font = pygame.freetype.Font(r'Resources/Font/Product_Sans_Regular.otf', 40)
        text_score, text_rect_score = score_font.render(str(self.score), s_color_while)
        text_rect_score.center = (300, 450)
        self.screen.blit(text_score, text_rect_score)
        pygame.display.update()

    def game_victory_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Back
                if 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
                    self.stage = s_display_home
            # Quit game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
            pygame.display.update(self.screen.blit(self.map_playbutton_shade, (250, 624)))

    def game_gameover_screen(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.game_gameover_bg, (0, 0))

        score_font = pygame.freetype.Font(r'Resources/Font/Product_Sans_Regular.otf', 40)
        text_score, text_rect_score = score_font.render(str(self.score), s_color_while)
        text_rect_score.center = (300, 450)
        self.screen.blit(text_score, text_rect_score)

        pygame.display.update()

    def game_gameover_action(self):
        for event in pygame.event.get():
            # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Back
                if 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
                    self.stage = s_display_home
            # Quit game
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.mouse = pygame.mouse.get_pos()

        # Create Button Shade
        if 251 <= self.mouse[0] <= 349 and 625 <= self.mouse[1] <= 673:
            pygame.display.update(self.screen.blit(self.map_playbutton_shade, (250, 624)))