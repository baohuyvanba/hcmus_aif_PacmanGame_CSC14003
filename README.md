# 🍗 hcmus_aif_PacmanGame
---
# Abstract
HCMUS - Artificial Intelligence Fundamentals.<br />
Project 01: Using Search Algorithm to control Pacman.<br />
Team 15, CSC14003, 09/2023, HCMC.<\br>
## Our team
👻 [Nguyen Duc Nam](https://github.com/nguyenducnam03)<br />
👻 [Nguyn Thi Gai](https://github.com/nguyenthigai1905)<br />
👻 [Van Ba Bao Huy](https://github.com/baohuyvanba)<br />
👻 [Nguyen Bich Khue](https://github.com/bichkhue23)<br />

## Environment
- Programming Language : `Python`
- Game Engine          : `Pygame`

# Requirements
- [ ] In the game Pac-Man, both Pac-Man and the monsters are constrained to moving in four directions: left, right, up, and down. They are not able to move through walls. The game is divided into four distinct levels, and each level has its own set of rules.
  - [ ] Level 1: Pac-Man is aware of the food's position on the map, and there are no monsters present. There is only one food item on the map.
  - [ ] Level 2: Monsters are stationary and do not move around. If Pac-Man and a monster collide with each other, the game ends. There is still one food item on the map, and Pac-Man knows its position.
  - [ ] Level 3: Pac-Man's visibility is limited to its nearest three steps. Foods outside this range are not visible to Pac-Man. Pac-Man can only scan the adjacent tiles within the 8 tiles x 3 range. There are multiple food items spread throughout the map. Monsters can move one step in any valid direction around their initial location at the start of the game. Both Pac-Man and monsters move one step per turn.
  - [ ] Level 4: involves an enclosed map where monsters relentlessly pursue Pac-Man. Pac-Man must gather as much food as possible while avoiding being overtaken by any monster. The monsters have the ability to pass through each other. Both Pac-Man and the monsters move one step per turn, and the map contains a multitude of food items.
- [ ] The calculation of game points follows these rules:
  - [ ] Each movement deducts 1 point from your score.
  - [ ] Collecting each food item awards you 20 points.

# Folder struct
Root<br />
 ┣ 📂 Resources<br />
 ┣  ┣ 📂 Character<br />
 ┣  ┣  ┣ 📂 Food<br />
 ┣  ┣  ┣ 📂 Monster<br />
 ┣  ┣  ┗ 📂 Pacman<br />
 ┣  ┣ 📂 Font<br />
 ┣  ┣ 📂 Game Display<br />
 ┣  ┣  ┣ 📂 Button<br />
 ┣  ┣  ┗ 📂 map<br />
 ┣  ┗ 📂 Map<br />
 ┣     ┣ 📂 Level_1<br />
 ┣     ┣ 📂 Level_2<br />
 ┣     ┣ 📂 Level_3<br />
 ┣     ┗ 📂 Level_4<br />
 ┣ agent.py<br />
 ┣ astart_search.py<br />
 ┣ alpha_beta_pruning.py<br />
 ┣ bfs_dfs_ucs_search.py<br />
 ┣ constant_value.py<br />
 ┣ game_logic_n_display.py<br />
 ┣ localsearch.py<br />
 ┣ main.py<br />
 ┣ map_txt_builder.py<br />
 ┗ map_txt_reading.py<br />

# Released Note:








 
