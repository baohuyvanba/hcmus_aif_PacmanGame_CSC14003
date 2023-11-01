#Display and Game|
#----------------/
import sys
import pygame
import pygame.freetype
import timeit

import map_txt_reading as readmap
import astar_search as astar
import agent as ag
from constant_value import *
import random

class pacman_game:
    #INIT ---------------------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        pygame.init()
        #Setup window frame
        self.screen  = pygame.display.set_mode((s_display_W, s_display_H)) #pygame.NOFRAME
        self.caption = pygame.display.set_caption(s_display_caption, s_display_iconpath)
        self.font    = pygame.freetype.Font(r'Resources/Product_Sans_Regular.otf', 16)

        #Load Display Stage
        self.mainmenu_bg  = pygame.image.load(s_display_bg)
        self.button_shade = pygame.image.load(s_button_shade)
        self.about_bg     = pygame.image.load(s_display_ab)
        self.level_bg     = pygame.image.load(s_display_lv)
        self.map_bg       = pygame.image.load(s_display_pm)
        self.gameplay_bg  = pygame.image.load(s_display_gp)
        self.map_playbutton_shade = pygame.image.load(s_button_shade_mapplay)
        self.map_before_shade     = pygame.image.load(s_button_shade_map_before)
        self.map_after_shade      = pygame.image.load(s_button_shade_map_after)

        #Game play function
        self.button_playhome_shade = pygame.image.load(s_button_shade_playhome)
        self.button_playhome       = pygame.image.load(s_button_shade_playhome_clean)
        self.button_playsped_shade = pygame.image.load(s_button_shade_playsped)
        self.button_playsped       = pygame.image.load(s_button_shade_playsped_clean)
        self.button_playsped_inner = pygame.image.load(s_button_inner_playsped)
        self.score_blank           = pygame.image.load(s_score_blank)

        #Victory / GameOver
        self.game_victory_bg  = pygame.image.load(s_display_victory)
        self.game_gameover_bg = pygame.image.load(s_display_gameover)

        #Stage. Mouse and FPS Control
        self.stage = s_display_home
        self.clock = pygame.time.Clock()
        self.mouse = None

        #Load Map
        self.map_index = 0
        self.map = pygame.image.load(s_map_gra_path[self.map_index])

        #Game logic
        self.score = 0
        self.level = 1
        self.speed = 1


    #GAME RUNNING ------------------------------------------------------------------------------------------------------------------------------------------------
    def run(self):
        while True:
            # pygame.event.pump()
            #Main Menu
            if self.stage == s_display_home:
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
            #Pick Map
            elif self.stage == s_display_map:
                self.pickmap_display()
                self.map_get_action()
            #Play Game
            elif self.stage == s_display_game:
                self.playgame_display()
                #Set Value to default and Start Game
                self.score = 0
                #Text
                text_surf, text_rect = self.font.render("Score", s_color_while)
                self.screen.blit(text_surf, s_pos_score)
                pygame.display.update(s_pos_score)
                #Speed
                text_sped, text_rect = self.font.render("1x", s_color_while)
                self.screen.blit(text_sped, s_pos_speedvalue)
                pygame.display.update(s_pos_speedvalue)
                #
                if self.level == 1:
                    self.pacman_lv1()
                elif self.level == 2:
                    self.pacman_lv2()
                elif self.level == 3:
                    self.pacman_lv3()
                elif self.level == 4:
                    self.pacman_lv4()
            elif self.stage == s_display_f_vic:
                self.game_victory_screen()
                self.game_victory_action()
                pygame.display.update()
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

    #Display Map picking
    def pickmap_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.map_bg, (0,0))
        self.show_map_option()
        pygame.display.update()

    def show_map_option(self):
        self.map = pygame.image.load(s_map_gra_path[self.map_index])
        pygame.display.update(self.screen.blit(pygame.transform.scale(self.map, (350, 375)), (125, 162)))

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
                    self.stage = s_display_map
                    self.level = 1
                #Level 2
                elif 220 <= self.mouse[0] <= 380 and 260 <= self.mouse[1] <= 320:
                    self.stage = s_display_map
                    self.level = 2
                #Level 3
                elif 220 <= self.mouse[0] <= 380 and 350 <= self.mouse[1] <= 410:
                    self.stage = s_display_map
                    self.level = 3
                #Level 4
                elif 220 <= self.mouse[0] <= 380 and 440 <= self.mouse[1] <= 500:
                    self.stage = s_display_map
                    self.level = 4
            # Quit game :<
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

    # GAME LEVEL PLAY -------------------------------------------------------------------------------------------------

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

    # Level 1
    def pacman_lv1(self):
        graph_map, pacman_pos, food_pos = readmap.map_level1(s_map_txt_path[self.level-1][self.map_index])
        start = timeit.default_timer()
        pathway = astar.astar_search(graph_map, pacman_pos, food_pos)
        end = timeit.default_timer()
        print('Time: ', end - start)
        #Call Pacman
        pacman = ag.Pacman(self, pacman_pos)
        pacman.pacman_call()
        #Call Food
        food = ag.Food(self, food_pos)
        food.food_display()
        #Call Monster
            #Nothing to call :v
        #Set pathway, score(0)
        goal = pathway[-1]
        pathway_togoal = pathway[1:-1]
        self.pacman_scoring(0)
        pygame.time.delay(500)

        #Go
        for loc in pathway_togoal:
            print(loc)
            pacman.pacman_control(loc)
            self.pacman_scoring(s_score_move)
            pygame.time.delay(250//self.speed)
            #Detect event during playing game
            if self.play_get_action():
                go_home = 1
                break
            else:
                go_home = 0

        #Go to goal (if not pressed go home button)
        # if go_home != 1:
        #     food.food_disappear()
        #     pacman.pacman_control(goal)
        #     self.pacman_scoring(s_score_gift)
        #     pygame.time.delay(2000)
        #     self.stage = s_display_f_vic
        # else:
        #     self.stage = s_display_home

        pygame.time.delay(3000)
        self.stage = s_display_f_vic

    # Level 2
    def pacman_lv2(self):
        graph_map, pacman_pos, food_pos, monsters_pos_list = readmap.map_level2(s_map_txt_path[self.level-1][self.map_index])
        pathway = astar.astar_search(graph_map, pacman_pos, food_pos)

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
        # Set pathway, score(0)
        goal = pathway[-1]
        pathway_togoal = pathway[1:-1]
        self.pacman_scoring(0)
        pygame.time.delay(500)

        print(pathway_togoal)

        # Go
        for loc in pathway_togoal:
            print(loc)
            pacman.pacman_control(loc)
            # self.pacman_scoring(s_score_move)
            pygame.time.delay(250 // self.speed)
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
            self.stage = s_display_f_vic
        else:
            self.stage = s_display_home

        pygame.time.delay(4000)
        self.stage = s_display_f_vic


    # Level 3
    def heuristic_lv3_around(self,graph_map,position,food_pos,pre_pos,monster_pos):
        heu = 0
        if position in food_pos:
            heu+=2
        if position in monster_pos:
            heu -= 30
        for pos in graph_map[position]:
            if pos in pre_pos:
                continue
            if pos in food_pos and pos not in pre_pos:
                pre_pos.append(pos)
                heu+=2
            elif pos in monster_pos:
                heu-=15

        return heu

    def heuristic_lv3_2around(self,pacman_pos,graph_map,position,food_pos,monster_pos):
        heu = 0
        if position in food_pos:
            heu+=2
        if position in monster_pos:
            heu -= 50
        pre_pos = []
        pre_pos.append(position)
        pre_pos.append(pacman_pos)
        for pos in graph_map[position]: 
            if pos == pacman_pos:
                continue
            heu = heu + self.heuristic_lv3_around(graph_map,pos,food_pos,pre_pos,monster_pos)
        return heu     

    def pacman_lv3(self):
        graph_map, pacman_pos, food_pos, monster_list = readmap.map_level3(s_map_txt_path[self.level-1][self.map_index])
        count = 0 #Number of points need to get
        # Call Pacman
        pacman_pos_draw = [pacman_pos[1],pacman_pos[0]]
        pacman = ag.Pacman(self, pacman_pos_draw)
        pacman.pacman_call()
        # Call Food
        for food_pos_t in food_pos: 
            food_pos_draw_t = [food_pos_t[1],food_pos_t[0]]
            food = ag.Food(self, food_pos_draw_t)
            food.food_display()
        # Call Monster
        monsters = [ag.Monster(self, [pos[1],pos[0]]) for pos in list(monster_list.keys())]
        for mons in monsters:
            mons.monster_call()

        pre_pos = None
        time_visits = {}
        for key in list(graph_map.keys()):
            time_visits[key] = 0
        index = 0
        parity_index_monster = 0 #to keep monster in this 5 cells
        
        #Preprocessing
        #Position of monsters
        old_pos = []
        for name in list(monster_list.keys()):
            old_pos.append(name)

        new_pos = old_pos.copy()
        keys_monster = list(monster_list.keys())

        #Heuristics 
        heuristic_call = {}
        for pos in graph_map[pacman_pos]:
            heuristic_call[pos] = self.heuristic_lv3_2around(pacman_pos,graph_map,pos,food_pos,old_pos)
        
        heuristic_call = dict(sorted(heuristic_call.items(), key=lambda item: item[1],reverse=True))
        
        end = True
        count_test = 0

        backup_heuristic = None
        backup_old_pos = None
        while count<400 and end:
            # count_test += 1
        # for nam_3 in range(5000):
            pygame.event.pump()
            pygame.time.delay(20)

            #Display pacman
            new_pacman_pos = list(heuristic_call.keys())[0]
            if new_pacman_pos in food_pos:
                count += 1
                food = ag.Food(self, (new_pacman_pos[1], new_pacman_pos[0]))
                food.food_disappear()
                food_pos.remove(new_pacman_pos)   
            pre_pos = pacman_pos
            pacman_pos = new_pacman_pos
            pacman.pacman_control([pacman_pos[1],pacman_pos[0]])

            parity_index_monster +=1
            backup_old_pos = old_pos.copy()
            # for element in list(monster_list.keys()):
            for i in range(len(monster_list)):
                element = keys_monster[i]
                if (parity_index_monster%2==1):#move\
                    old_pos[i] = element
                    size = len(monster_list[element])
                    num = random.randint(0,size-1)
                    new_pos[i] = (monster_list[element][num][0],monster_list[element][num][1])
                    # print(new_pos[i])

                    monster = ag.Monster(self, (old_pos[i][1], old_pos[i][0]))    
                    monster.monster_disappear()

                    if ((old_pos[i][0],old_pos[i][1]) in food_pos):
                        food_pos_draw_t = [old_pos[i][1],old_pos[i][0]]
                        food = ag.Food(self, food_pos_draw_t)
                        food.food_display()                

                    monster = ag.Monster(self, (new_pos[i][1], new_pos[i][0]))
                    monster.monster_control([new_pos[i][1], new_pos[i][0]])

                    old_pos[i] = new_pos[i]
                else:
                    monster = ag.Monster(self, (old_pos[i][1], old_pos[i][0]))    
                    monster.monster_disappear()
                    if ((old_pos[i][0],old_pos[i][1]) in food_pos):
                        food_pos_draw_t = [old_pos[i][1],old_pos[i][0]]
                        food = ag.Food(self, food_pos_draw_t)
                        food.food_display()  

                    new_pos[i] = element
                    monster = ag.Monster(self, (new_pos[i][1], new_pos[i][0]))
                    monster.monster_control([new_pos[i][1], new_pos[i][0]])

                    old_pos[i] = new_pos[i]

            #Calculate heuristic for next move
            heuristic_call = {}
            for pos in graph_map[pacman_pos]:
                if pos == pre_pos:
                    time_visits[pos] += 2
                else:
                    time_visits[pos] +=1
                heuristic_call[pos] = (-1)*time_visits[pos] + self.heuristic_lv3_2around(pacman_pos,graph_map,pos,food_pos,old_pos)

            heuristic_call = dict(sorted(heuristic_call.items(), key=lambda item: item[1],reverse=True))

            # print('===============CHECK================')
            # print(pacman_pos)
            # print(old_pos)
            # print(heuristic_call)
            # print('===============CHEND================')
            if pacman_pos in old_pos:
                print("Pacman pos old:", pre_pos)
                print(backup_heuristic)
                print("Pacman pos:", pacman_pos)
                print(heuristic_call)
                print('monster pos old: ')
                print(backup_old_pos)
                print('monster pos: ')
                print(old_pos)
                end = False
                print("pacman died")
                break
            backup_heuristic = heuristic_call
            

        pygame.time.delay(3000)
        self.stage = s_display_f_vic

    # Level 4
    def heuristic_lv4_around(self,graph_map,position,food_pos,pre_pos,monster_pos):
        heu = 0
        if position in food_pos:
            heu+=5
        if position in monster_pos:
            heu += -2000
        elif position not in pre_pos and position not in food_pos:
            heu +=2
        
        for pos in graph_map[position]:
            if pos in pre_pos:
                return heu
            if pos in food_pos and pos not in pre_pos:
                pre_pos.append(pos)
                heu+=5
            if pos in monster_pos:
                heu+=-500
            elif pos not in pre_pos and position not in food_pos:
                heu += 2
        return heu

    def heuristic_lv4_2around(self,pacman_pos,graph_map,position,food_pos,monster_pos):
        heu = 0
        if position in food_pos:
            heu+=5
        if position in monster_pos:
            heu += -5000
        elif position not in food_pos:
            heu+=2
        
        pre_pos = []
        pre_pos.append(position)
        pre_pos.append(pacman_pos)
        for pos in graph_map[position]:
            if pos == pacman_pos:
                return heu
            heu += self.heuristic_lv4_around(graph_map,pos,food_pos,pre_pos,monster_pos)
        return heu 
    
    def heuristic(self, state, goal):  #Diagonal
        dx = abs(state[0] - goal[0])
        dy = abs(state[1] - goal[1])
        return dx + dy - min(dx, dy)
    
    def isValid(self,position,graph_map,monster_list):
        if (0<position[0]<30 and 0<position[1]<28 and ((position in graph_map) or (position in monster_list))):
            return True
        else:
            return False

    def heuristic_lv4_monster(self,position,graph_map,monster_list,pacman_pos,time_monster):
        heu = {}
        p1 = (position[0],position[1]-1) #Left
        p2 = (position[0]-1,position[1]) #Up
        p3 = (position[0],position[1]+1) #Right
        p4 = (position[0]+1,position[1]) #Down
        # print(p1,p2,p3,p4)
        if (self.isValid(p1,graph_map,monster_list)):
            if p1 not in time_monster:
                time_monster[p1] = 0
            heu[p1] = time_monster[p1]*2 + self.heuristic(p1,pacman_pos)
        else:
            heu[p1] = 10000

        if (self.isValid(p2,graph_map,monster_list)):
            if p2 not in time_monster:
                time_monster[p2] = 0
            heu[p2] =time_monster[p2]*2 + self.heuristic(p2,pacman_pos)
        else:
            heu[p2] = 10000

        if (self.isValid(p3,graph_map,monster_list)):
            if p3 not in time_monster:
                time_monster[p3] = 0
            heu[p3] =time_monster[p3]*2 + self.heuristic(p3,pacman_pos)
        else:
            heu[p3] = 10000

        if (self.isValid(p4,graph_map,monster_list)):
            if p4 not in time_monster:
                time_monster[p4] = 0
            heu[p4] =time_monster[p4]*2 + self.heuristic(p4,pacman_pos)
        else:
            heu[p4] = 10000
        
        heu = dict(sorted(heu.items(), key=lambda item: item[1],reverse=False))
        return heu


    def pacman_lv4(self):
        count = 0 #Number of points need to get
        number_point = 8

        graph_map, pacman_pos, food_pos, monster_list = readmap.map_level4(s_map_txt_path[self.level-1][self.map_index])
        #Position of monsters
        old_pos = []
        for name in list(monster_list.keys()):
            old_pos.append(name)
        new_pos = old_pos.copy()
        keys_monster = list(monster_list.keys())

        #Heuristics 
        heuristic_call = {}
        for pos in graph_map[pacman_pos]:
            heuristic_call[pos] = self.heuristic_lv4_2around(pos,graph_map,pos,food_pos,old_pos)
        
        heuristic_call = dict(sorted(heuristic_call.items(), key=lambda item: item[1],reverse=True))
        # print(heuristic_call)

        # Call Pacman
        pacman_pos_draw = [pacman_pos[1],pacman_pos[0]]
        pacman = ag.Pacman(self, pacman_pos_draw)
        pacman.pacman_call()
        # Call Food
        for food_pos_t in food_pos: 
            food_pos_draw_t = [food_pos_t[1],food_pos_t[0]]
            food = ag.Food(self, food_pos_draw_t)
            food.food_display()
        # Call Monster
        monsters = [ag.Monster(self, [pos[1],pos[0]]) for pos in list(monster_list.keys())]
        for mons in monsters:
            mons.monster_call()

        
        print("Hello level4")
        pre_pos = None
        time_visits = {}
        for key in list(graph_map.keys()):
            time_visits[key] = 0
        index = 0
        parity_index_monster = 0 #to keep monster in this 5 cells
        # index_monster = monsters_pos_list.copy()

        # print(monster_list[list(monster_list.keys())[0]][0])
        # while count<100:
        # pygame.event.pump()
        num_monster = len(keys_monster)
        for i in range(num_monster):
            old_pos[i] = keys_monster[i]
        time_monster = {}
        for nam_3 in range(20):
            pygame.event.pump()
            if (nam_3%10==0):
                print("Time: ",nam_3)
            print(heuristic_call)

            pygame.time.delay(300)

            new_pacman_pos = list(heuristic_call.keys())[0]
            if new_pacman_pos in food_pos:
                count += 1
                food = ag.Food(self, (new_pacman_pos[1], new_pacman_pos[0]))
                food.food_disappear()
                food_pos.remove(new_pacman_pos)
                        
            pre_pos = pacman_pos
            pacman_pos = new_pacman_pos
            pacman.pacman_control([pacman_pos[1],pacman_pos[0]])

            # For 1
            # print(monster_list)
            # print(keys_monster)
            # print(element)
            # print((21,6) in monster_list)
            # print((21,6) in graph_map)
            # print( pacman_pos)
            for i in range(num_monster):
                monster = ag.Monster(self, (old_pos[i][1], old_pos[i][0]))    
                monster.monster_disappear()
                if ((old_pos[i][0],old_pos[i][1]) in food_pos):
                    food_pos_draw_t = [old_pos[i][1],old_pos[i][0]]
                    food = ag.Food(self, food_pos_draw_t)
                    food.food_display()   

                heuristic_monster = self.heuristic_lv4_monster(new_pos[i],graph_map,monster_list,pacman_pos,time_monster)
                # print(heuristic_monster)
                # print(heuristic_monster)
                # stt = 0
                new_pos[i] = list(heuristic_monster.keys())[0]
                # while (old_pos[i] == new_pos[i]):
                #     stt += 1
                #     new_pos[i] = list(heuristic_monster.keys())[stt]

                if new_pos[i] not in time_monster:
                    time_monster[new_pos[i]] = 1
                else:
                    time_monster[new_pos[i]] += 1

                old_pos[i] = new_pos[i]
                monster = ag.Monster(self, (new_pos[i][1], new_pos[i][0]))
                monster.monster_control([new_pos[i][1], new_pos[i][0]])
                # print('run this: ?')
                # old_pos[i] = new_pos[i]
                # print(old_pos[i], new_pos[i])
            # print(old_pos)
            heuristic_call = {}
            for pos in graph_map[pacman_pos]:
                if pos == pre_pos:
                    time_visits[pos] += 1
                heuristic_call[pos] = (-1)*time_visits[pos] + self.heuristic_lv4_2around(pos,graph_map,pos,food_pos,old_pos)

            heuristic_call = dict(sorted(heuristic_call.items(), key=lambda item: item[1],reverse=True))

            #Position of pacman

        pygame.time.delay(3000)
        self.stage = s_display_f_vic



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