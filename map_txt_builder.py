from PIL import Image
from constant_value import *

# Load maze data from the file
def load_maze(file_name):
    with open(file_name, 'r') as file:
        maze_size = list(map(int, file.readline().split()))
        maze = [[int(num) if int(num) in (0, 1) else 0 for num in line.split()] for line in file]
        #maze = [[int(num) for num in line.split()] for line in file]
    return maze[:-1], maze_size

# Draw the maze into an image using PIL
def draw_maze_image(maze, maze_size, block_size):
    wall_color  = s_color_rose     # Color for walls
    empty_color = s_color_dblue    # Color for empty spaces

    width, height = maze_size[1] * block_size, maze_size[0] * block_size
    maze_image = Image.new("RGB", (width, height), empty_color)

    pixels = maze_image.load()
    for y in range(maze_size[0]):
        for x in range(maze_size[1]):
            for i in range(block_size):
                for j in range(block_size):
                    if x * block_size + i < width and y * block_size + j < height and maze[y][x] == 1:
                        pixels[x * block_size + i, y * block_size + j] = wall_color

    return maze_image

# Generate the maze image and save it to a file
def create_maze_image(file_name, output_file):
    maze, maze_size = load_maze(file_name)
    block_size = 20
    maze_image = draw_maze_image(maze, maze_size, block_size)
    maze_image.save(output_file)
