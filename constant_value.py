#Declare all constant variable using in this project |
#----------------------------------------------------/

#Game Display Window
s_display_W = 600
s_display_H = 700
s_display_caption  = r'./Pacman Game'
s_display_iconpath = r'./Resources/Game Display/icon.png'
s_display_fps = 30

s_font_path  = r'./Resources/Font/Product_Sans_Regular.otf'

s_display_bg = r'./Resources/Game Display/PM-MainMenu.png'
s_display_ab = r'./Resources/Game Display/PM-About.png'
s_display_lv = r'./Resources/Game Display/PM-PickLevel.png'
s_display_al = r'./Resources/Game Display/PM-PickAlgorithm.png'
s_display_pm = r'./Resources/Game Display/PM-PickMap.png'
s_display_gp = r'./Resources/Game Display/PM-GameScreen.png'
s_display_victory  = r'./Resources/Game Display/PM-Victory.png'
s_display_gameover = r'./Resources/Game Display/PM-GameOver.png'

#Map Creator[level][map-index]
s_map_txt_path = [[r'./Resources/Map/Level_1/map1.txt', r'./Resources/Map/Level_1/map2.txt', r'./Resources/Map/Level_1/map3.txt', r'./Resources/Map/Level_1/map4.txt', r'./Resources/Map/Level_1/map5.txt'],
                  [r'./Resources/Map/Level_2/map1.txt', r'./Resources/Map/Level_2/map2.txt', r'./Resources/Map/Level_2/map3.txt', r'./Resources/Map/Level_2/map4.txt', r'./Resources/Map/Level_2/map5.txt'],
                  [r'./Resources/Map/Level_3/map1.txt', r'./Resources/Map/Level_3/map2.txt', r'./Resources/Map/Level_3/map3.txt', r'./Resources/Map/Level_3/map4.txt', r'./Resources/Map/Level_3/map5.txt'],
                  [r'./Resources/Map/Level_4/map1.txt', r'./Resources/Map/Level_4/map2.txt', r'./Resources/Map/Level_4/map3.txt', r'./Resources/Map/Level_4/map4.txt', r'./Resources/Map/Level_4/map5.txt']]

#Map Graphic[level][map-index]
s_map_gra_path = [[r'./Resources/Game Display/map/lv1_m1.png', r'Resources/Game Display/map/lv1_m2.png', r'Resources/Game Display/map/lv1_m3.png', r'Resources/Game Display/map/lv1_m4.png', r'Resources/Game Display/map/lv1_m5.png'],
                  [r'./Resources/Game Display/map/lv2_m1.png', r'Resources/Game Display/map/lv2_m2.png', r'Resources/Game Display/map/lv2_m3.png', r'Resources/Game Display/map/lv2_m4.png', r'Resources/Game Display/map/lv2_m5.png'],
                  [r'./Resources/Game Display/map/lv3_m1.png', r'Resources/Game Display/map/lv3_m2.png', r'Resources/Game Display/map/lv3_m3.png', r'Resources/Game Display/map/lv3_m4.png', r'Resources/Game Display/map/lv3_m5.png'],
                  [r'./Resources/Game Display/map/lv4_m1.png', r'Resources/Game Display/map/lv4_m2.png', r'Resources/Game Display/map/lv4_m3.png', r'Resources/Game Display/map/lv4_m4.png', r'Resources/Game Display/map/lv4_m5.png']]

#Color
s_color_black = (0, 0, 0)
s_color_while = (255, 255, 255)
s_color_rose  = (240, 128, 128)
s_color_dblue = (0, 15, 39)

#Stage
s_display_home  = "Home"
s_display_play  = "Play"
s_display_map   = "Map"
s_display_about = "About"
s_display_exit  = "Exit"
s_display_game  = "Playing"
s_display_f_vic = "Victory"
s_display_f_ove = "GameOver"

#Algorithm
s_algorithm_dfs = 0
s_algorithm_bfs = 1
s_algorithm_ucs = 2
s_algorithm_astart = 3

#Button
s_button_shade                = r'./Resources/Game Display/Button/Shade.png'
s_button_shade_mapplay        = r'./Resources/Game Display/Button/Shape_4.png'
s_button_shade_map_before     = r'./Resources/Game Display/Button/Shape_4_before.png'
s_button_shade_map_after      = r'./Resources/Game Display/Button/Shape_4_after.png'
s_button_shade_playhome       = r'./Resources/Game Display/Button/Shade_2.png'
s_button_shade_playhome_clean = r'./Resources/Game Display/Button/Shade_2_clean.png'
s_button_shade_playsped       = r'./Resources/Game Display/Button/Shade_3.png'
s_button_shade_playsped_clean = r'./Resources/Game Display/Button/Shade_3_clean.png'
s_button_inner_playsped       = r'./Resources/Game Display/Button/Shade_3_inner.png'

s_time_delay = 250

#Score Position
s_pos_score = (20, 665, 50, 20)
s_pos_scorevalue = (75, 665, 90, 20)
s_pos_speedvalue = (557, 665, 30, 20)
s_score_blank = r'./Resources/Game Display/blankspace_score.png'

#Node state
node_NotVisited = 0
node_Frontier = 1
node_Explored = 2

#Pacman
s_character_path = r'./Resources/Character/Pacman/PM_R.png'
s_character_R = r'./Resources/Character/Pacman/PM_R.png'
s_character_L = r'./Resources/Character/Pacman/PM_L.png'
s_direction_R = "Right"
s_direction_L = "Left"
s_blank_space = r'./Resources/Game Display/map/blankspace.png'

#Score
s_score_move = -1
s_score_gift = 20

#Food
s_food_path = r'./Resources/Character/Food/food.png'

#Monster
s_character_monster = r'./Resources/Character/Monster/monster.png'

#Cell state
s_state_food    = 2
s_state_monster = 3
s_state_pacman  = 4