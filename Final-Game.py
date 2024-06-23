from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18  # Import the font
import time
import random
# Window dimensions
window_width, window_height = 700, 700
maze_rows, maze_cols = 10, 10
cell_size = window_width // maze_cols
padding = 20
button_size = 30
button_1x, button_2x, button_3x = padding, (window_width - button_size) // 2, window_width - button_size - padding
button_y = window_height - padding - button_size   # Adjusted button y position to avoid overlapping with maze
button_colors = (0.28, 0.82, 0.8), (1, 0.76, 0), (1, 0, 0)

# Global variables for the player's position
player_x, player_y = 105, 30  # Initial player position
player_size = 20
head_radius = 8
arm_length = 12
leg_length = 15
neck_length = 8
game_over, paused, reached_end = False , False , False
score = 0
sections_passed = 0
max_sections_to_pass = 10  # Maximum number of sections to pass before game over
move_amount = 10 
max_time_per_level = 3
start_time = 0
# Global variable to store the positions of powerup points
powerup_positions = []
num_powerups = 7  # Number of powerup points to generate
powerup_radius = 10  # Radius of the powerup circles
powerup_points_collected = 0  # Counter for powerup points collected
powerup_colors = {}
invulnerable = False
invulnerability_time = 7  # The duration of invulnerability in seconds
invulnerability_start_time = 0  # The start time of the invulnerability

    



# Function to generate a randomized maze
def generate_maze():
    # Initialize maze with all walls
    maze = [[1] * maze_cols for _ in range(maze_rows)]

    # Recursive backtracking algorithm to create maze
    def create_maze(row, col):
        maze[row][col] = 0  # Mark current cell as empty

        # Define the order in which directions will be explored
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        # Explore each direction
        for dx, dy in directions:
            new_row, new_col = row + 2 * dx, col + 2 * dy  # New cell position after jumping over a wall
            if 0 <= new_row < maze_rows and 0 <= new_col < maze_cols and maze[new_row][new_col] == 1:
                maze[row + dx][col + dy] = 0  # Remove wall between current cell and next cell
                create_maze(new_row, new_col)  # Recursively explore next cell

    # Start maze generation from the top-left corner
    create_maze(1, 1)

    # Ensure there is  clear path from the starting point to the ending point
    maze[1][1] = 0  # Make the starting point open
    maze[maze_rows - 2][maze_cols - 2] = 0  # Make the ending point open

    return maze


maze = generate_maze()  # Generate the maze



# Generate powerup points randomly in the maze if needed
while len(powerup_positions) < num_powerups:
    row = random.randint(0, maze_rows - 1)
    col = random.randint(0, maze_cols - 1)
    if maze[row][col] == 0:  # Check if the cell is empty
        center_x = col * cell_size + cell_size // 2
        center_y = (maze_rows - row - 1) * cell_size + cell_size // 2
        powerup_positions.append((center_x, center_y))  # Add powerup position to the list

def powerup():
    global score, powerup_positions,powerup_radius,powerup_points_collected,powerup_colors, move_amount, head_radius, arm_length, leg_length, neck_length, invulnerable, invulnerability_start_time, invulnerability_time


    # Bounding boxes for player parts, as defined in is_collision
    body_box = (player_x - player_size // 2, player_y - player_size // 2, player_size, player_size)
    head_box = (player_x - head_radius, player_y + player_size // 2 + neck_length, head_radius * 2, head_radius * 2)
    left_arm_box = (player_x - player_size // 2 - arm_length, player_y + player_size // 2 - 10, arm_length, 5)
    right_arm_box = (player_x + player_size // 2, player_y + player_size // 2 - 10, arm_length, 5)
    left_leg_box = (player_x - 5, player_y - player_size // 2 - leg_length, 5, leg_length)
    right_leg_box = (player_x + player_size - 5, player_y - player_size // 2 - leg_length, 5, leg_length)
    
    player_parts_boxes = [body_box, head_box, left_arm_box, right_arm_box, left_leg_box, right_leg_box]



    # Draw powerup points
    for position in powerup_positions[:]:
        center_x, center_y = position
        for part_box in player_parts_boxes:
            part_x, part_y, part_width, part_height = part_box
            # Check if the powerup is within any part of the player's bounding box
            if (center_x >= part_x - powerup_radius and center_x <= part_x + part_width + powerup_radius and
                center_y >= part_y - powerup_radius and center_y <= part_y + part_height + powerup_radius):
                score += 1  # Increment score
                powerup_points_collected += 1  # Increment powerup points collected
                powerup_positions.remove(position)  # Remove the powerup from the list
                break  # Break out of the loop after collecting the powerup
        # Generate random RGB values for the color of the powerup point
        
        if position not in powerup_colors:
            powerup_colors[position] = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
        
        # Check if the player has become invulnerable
        
        if powerup_points_collected == 3:
            invulnerable = True  # Make player invulnerable
            invulnerability_start_time = time.time()  # Record the start time
            move_amount += 5  # Increase player speed by 5 (as per your existing code)
            powerup_points_collected = 0  # Reset powerup points collected counter

        color = powerup_colors[position]  # Get the color for this powerup point


        draw_midpoint_circle(center_x, center_y, powerup_radius, color)  # Draw powerup point

        # Check if the player collects the powerup point
        if abs(player_x - center_x) <= powerup_radius and abs(player_y - center_y) <= powerup_radius:
            score += 1  # Increment score by 1
            powerup_points_collected += 1  # Increment powerup points collected
            powerup_positions.remove(position)  # Remove the collected powerup point

# Global varial
# Function to check if a point is inside a rectangle
def point_inside_rect(x, y, rect_x, rect_y, rect_width, rect_height):
    return x >= rect_x and x <= rect_x + rect_width and y >= rect_y and y <= rect_y + rect_height

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black and opaque
    glPointSize(5.0)  # Set the point size to 5x5 pixels
    gluOrtho2D(0, window_width, 0, window_height)  # Set the coordinate system
    glEnable(GL_DEPTH_TEST)  # Enable depth testing

def draw_line(x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        draw_point(x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
def draw_midpoint_line(x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    
    while True:
        draw_point(x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def draw_midpoint_circle(center_x, center_y, radius, color):
    x = radius
    y = 0
    err = 0

    while x >= y:
        draw_point(center_x + x, center_y + y, color)
        draw_point(center_x + y, center_y + x, color)
        draw_point(center_x - y, center_y + x, color)
        draw_point(center_x - x, center_y + y, color)
        draw_point(center_x - x, center_y - y, color)
        draw_point(center_x - y, center_y - x, color)
        draw_point(center_x + y, center_y - x, color)
        draw_point(center_x + x, center_y - y, color)

        if err <= 0:
            y += 1
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1



def draw_point(x, y, color):
    glBegin(GL_POINTS)
    glColor3f(*color)
    glVertex2f(x, y)
    glEnd()

wall_color = (random.uniform(0.7, 1), random.uniform(0.7, 1), random.uniform(0.7, 1))  # Randomize wall color

def draw_maze():
    global wall_color
    button_top_y = button_y + button_size  # Top y-coordinate of the buttons
    
    for row in range(maze_rows):
        for col in range(maze_cols):
            if maze[row][col] == 1:  # If there is a wall
                cell_top_left = (col * cell_size, (maze_rows - row - 1) * cell_size)
                cell_top_right = ((col + 1) * cell_size, (maze_rows - row - 1) * cell_size)
                cell_bottom_left = (col * cell_size, (maze_rows - row) * cell_size)
                cell_bottom_right = ((col + 1) * cell_size, (maze_rows - row) * cell_size)
                
                # Check if the cell is below the buttons
                if cell_bottom_left[1] < button_top_y:
                    
                    draw_line(cell_top_left[0], cell_top_left[1], cell_top_right[0], cell_top_right[1], wall_color)
                    draw_line(cell_bottom_left[0], cell_bottom_left[1], cell_bottom_right[0], cell_bottom_right[1], wall_color)
                    draw_line(cell_top_left[0], cell_top_left[1], cell_bottom_left[0], cell_bottom_left[1], wall_color)
                    draw_line(cell_top_right[0], cell_top_right[1], cell_bottom_right[0], cell_bottom_right[1], wall_color)

def draw_player():
    global player_size, head_radius, arm_length, leg_length, neck_length # Size of the player square
    start_x = player_x - player_size // 2
    start_y = player_y - player_size // 2
    
    # Draw player body using midpoint line algorithm
    draw_midpoint_line(start_x, start_y, start_x + player_size, start_y, (0.0, 1.0, 0.0))  # Top line
    draw_midpoint_line(start_x + player_size, start_y, start_x + player_size, start_y + player_size, (0.0, 1.0, 0.0))  # Right line
    draw_midpoint_line(start_x + player_size, start_y + player_size, start_x, start_y + player_size, (0.0, 1.0, 0.0))  # Bottom line
    draw_midpoint_line(start_x, start_y + player_size, start_x, start_y, (0.0, 1.0, 0.0))  # Left line

    # Draw player head using midpoint circle algorithm
    
    head_center_x = player_x
    head_center_y = player_y + player_size + head_radius
    draw_midpoint_circle(head_center_x, head_center_y, head_radius, (1.0, 1.0, 0.0))  # Yellow color
    
    # Draw neck
    neck_start_x = player_x
    neck_start_y = player_y + player_size
    neck_end_x = player_x
    neck_end_y = neck_start_y - 8  # Adjust the length of the neck here
    draw_midpoint_line(neck_start_x, neck_start_y, neck_end_x, neck_end_y, (1.0, 1.0, 1.0))  # Neck color
    # Draw player arms and legs
    
    draw_midpoint_line(start_x - 5, start_y + player_size - 10, start_x - 5 - arm_length, start_y + player_size - 10, (1.0, 1.0, 1.0))  # Left arm
    draw_midpoint_line(start_x + player_size + 5, start_y + player_size - 10, start_x + player_size + 5 + arm_length, start_y + player_size - 10, (1.0, 1.0, 1.0))  # Right arm
    draw_midpoint_line(start_x, start_y - leg_length, start_x - 5, start_y + player_size - 20, (1.0, 1.0, 1.0))  # Left leg
    draw_midpoint_line(start_x + player_size, start_y - leg_length, start_x + player_size + 5, start_y + player_size - 20, (1.0, 1.0, 1.0))  # Right leg

def draw_timer():
    global window_width, window_height, start_time, max_time_per_level, game_over
    
    if not game_over and not reached_end and not paused:
        # Calculate time elapsed since the last layer crossing
        elapsed_time = time.time() - start_time
        remaining_time = max(0, max_time_per_level - elapsed_time)
        
        if start_time != 0 and remaining_time <= 0:  # Check if start time is not zero before triggering game over
            game_over = True
            print("Game Over! Time's up!")  # Print game over message
            return  # Exit the function immediately
        
        if remaining_time <= 0:
            return  # If start time is zero, return without further processing
        
        if remaining_time <= 2:
            glColor3f(1.0, 0.0, 0.0)  # Set text color to red
        else:
            glColor3f(0.0, 1.0, 0.0)  # Set text color to green

        glRasterPos2f(window_width - 150, window_height - 60)  # Position the timer text
        timer_text = f"Time: {int(remaining_time)}s"
        for character in timer_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))  # Render each character

def draw_invulnerability_timer():
    global invulnerable, invulnerability_start_time, invulnerability_time, paused 

    if invulnerable and not paused:
        # Calculate the remaining invulnerability time
        elapsed_time = time.time() - invulnerability_start_time
        remaining_time = max(0, invulnerability_time - elapsed_time)

        if remaining_time <= 0:
            invulnerable = False
        else:
            glColor3f(1.0, 0.5, 0.0)  # Set text color to orange
            glRasterPos2f(10, window_height - 50)  # Position the invulnerability timer text
            invulnerability_text = f"Invulnerability: {remaining_time:.1f}s"
            for character in invulnerability_text:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))

def draw_buttons():
    draw_restart()
    draw_playpause()
    draw_exit()

def draw_restart():
    global button_1x, button_y, button_size, button_colors
    x, y = button_1x, button_y
    point_1 = x, y + button_size // 2
    point_2 = x + button_size // 2, y
    point_3 = x + button_size, y + button_size // 2
    point_4 = x + button_size // 2, y + button_size
    draw_line(*point_1, *point_2, button_colors[0])
    draw_line(*point_1, *point_3, button_colors[0])
    draw_line(*point_1, *point_4, button_colors[0])

def draw_playpause():
    global button_2x, button_y, button_size, button_colors, paused
    x, y = button_2x, button_y
    if not paused:
        temp = (button_size // 3)
        point_1 = x + temp, y + button_size - 10
        point_2 = x + temp, y
        point_3 = x + button_size - temp, y + button_size - 10
        point_4 = x + button_size - temp, y
        draw_line(*point_1, *point_2, button_colors[1])
        draw_line(*point_3, *point_4, button_colors[1])
    else:
        point_1 = x, y
        point_2 = x, y + button_size
        point_3 = x + button_size, y + button_size // 2
        draw_line(*point_2, *point_1, button_colors[1])
        draw_line(*point_2, *point_3, button_colors[1])
        draw_line(*point_1, *point_3, button_colors[1])

def draw_exit():
    global button_3x, button_y, button_size, button_colors
    x, y = button_3x, button_y
    point_1 = x, y + button_size
    point_2 = x, y
    point_3 = x + button_size, y
    point_4 = x + button_size, y + button_size
    draw_line(*point_1, *point_3, button_colors[2])
    draw_line(*point_2, *point_4, button_colors[2])

def draw_game_over_screen():
    global window_width, window_height, score, player_y, remaining_time, max_time_per_level
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(window_width // 2 - 170, window_height - 20)
    text = f"Game Over!"
    elapsed_time = time.time() - start_time
    remaining_time = max(0, max_time_per_level - elapsed_time)
    if remaining_time <=0 :
        text += " Times Up! "
    
    glColor3f(0.0, 0.0, 1.0)
    glRasterPos2f(window_width // 2 - 170, window_height - 20)
    if  player_y >= 400 :
        text=f"Congratulations! You completed the maze."
    # text = f"Game Over! Score: {score}"
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))
def draw_win_screen():
    global window_width, window_height, score, player_y, game_over
    if  player_y > 600 :
        game_over= True
        glColor3f(0.0, 0.0, 1.0)
        glRasterPos2f(window_width // 2 - 170, window_height - 20)
        text=f"Congratulations! You completed the maze."
    # text = f"Game Over! Score: {score}"
        for character in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))

def mouse_click(button, state, x, y):
    global game_over, score, sections_passed
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if point_inside_rect(x, window_height - y, button_1x, button_y, button_size, button_size):
            restart_game()
        elif point_inside_rect(x, window_height - y, button_2x, button_y, button_size, button_size):
            toggle_pause()
        elif point_inside_rect(x, window_height - y, button_3x, button_y, button_size, button_size):
            exit_game()

def restart_game():
    global game_over, score, sections_passed, player_x, player_y, maze, start_time, powerup_points_collected, invulnerability_start_time,  invulnerable, powerup_colors, powerup_positions
    game_over = False
    score = 0
    sections_passed = 0
    powerup_points_collected = 0  # Reset powerup points collected
    invulnerable = False  # Reset invulnerability
    start_time = time.time()  # Reset start time
    powerup_positions = []  # Clear existing powerup positions
    powerup_colors = {}  # Clear existing powerup colors

    # Regenerate powerup points randomly in the maze
    while len(powerup_positions) < num_powerups:
        row = random.randint(0, maze_rows - 1)
        col = random.randint(0, maze_cols - 1)
        if maze[row][col] == 0:  # Check if the cell is empty
            center_x = col * cell_size + cell_size // 2
            center_y = (maze_rows - row - 1) * cell_size + cell_size // 2
            powerup_positions.append((center_x, center_y))  # Add powerup position to the list


    # Randomly select a starting position until it finds an empty cell in the maze
    while True:
        player_x = random.randint(0, maze_cols - 1) * cell_size + cell_size // 2
        player_y = cell_size // 2
        if maze[maze_rows - 1 - player_y // cell_size][player_x // cell_size] == 0:
            break
    
    # Reset other game parameters if needed
    start_time = time.time()  # Reset start time
    invulnerability_start_time = 0  # Reset invulnerability start time
    # Reset other game parameters if needed

def toggle_pause():
    global paused
    paused = not paused  # Toggle the paused state
    
    if not paused:
        glutPostRedisplay()


def exit_game():
    glutLeaveMainLoop()

# import time

def is_collision(x, y):
    global game_over, invulnerable, maze, cell_size, maze_rows, maze_cols, player_size, head_radius, arm_length, leg_length, neck_length
    if invulnerable:
        return False
    # Define bounding boxes for each part of the player
    body_box = (x - player_size // 2, y - player_size // 2, player_size, player_size)
    head_box = (x - head_radius, y + player_size // 2 + neck_length, 2 * head_radius, 2 * head_radius)
    left_arm_box = (x - player_size // 2 - arm_length, y + player_size // 2 - 10, arm_length, 5)
    right_arm_box = (x + player_size // 2, y + player_size // 2 - 10, arm_length, 5)
    left_leg_box = (x - 5, y - player_size // 2 - leg_length, 5, leg_length)
    right_leg_box = (x + player_size - 5, y - player_size // 2 - leg_length, 5, leg_length)

    parts_boxes = [body_box, head_box, left_arm_box, right_arm_box, left_leg_box, right_leg_box]

    for box in parts_boxes:
        part_x, part_y, part_width, part_height = box
        col_left = int(part_x // cell_size)
        col_right = int((part_x + part_width) // cell_size)
        row_top = maze_rows - 1 - int(part_y // cell_size)
        row_bottom = maze_rows - 1 - int((part_y + part_height) // cell_size)

        # Check if any part touches the wall
        if (maze[row_top][col_left] == 1 or maze[row_top][col_right] == 1 or
            maze[row_bottom][col_left] == 1 or maze[row_bottom][col_right] == 1):
            if not invulnerable:
                game_over = True
                print("Game Over! You touched the maze!")
                return True

    return False

def check_game_end():
    global sections_passed, max_sections_to_pass, reached_end, game_over, score
    # Check if the player reaches or exceeds the last section of the maze
    if sections_passed >= max_sections_to_pass - 1:
        reached_end = True
        # game_over = True
        print(f"Congratulations! You completed the maze. Total Score: {score}")

def keyboard_listener(key, x, y):
    global player_x, player_y, score, start_time, invulnerable, game_over

    if game_over:
        return

    dx, dy = 0, 0
    if key == b'w':
        dy = move_amount
    elif key == b's':
        dy = -move_amount
    elif key == b'a':
        dx = -move_amount
    elif key == b'd':
        dx = move_amount

    new_x, new_y = player_x + dx, player_y + dy

    # Check boundaries
    if 0 <= new_x < window_width and 0 <= new_y < window_height:
        if not is_collision(new_x, new_y):
            # Track cell transitions for scoring
            old_cell_x, old_cell_y = player_x // cell_size, player_y // cell_size
            new_cell_x, new_cell_y = new_x // cell_size, new_y // cell_size

            # Move player
            player_x, player_y = new_x, new_y

            # Increment score and reset timer if new cell is entered
            if old_cell_x != new_cell_x or old_cell_y != new_cell_y:
                score += 1
                start_time = time.time()  # Reset the timer for new cell entry
                print(f"Crossed into a new section. Score: {score}, Time reset.")

        glutPostRedisplay()

def display():
    global window_width, window_height, game_over, score, sections_passed, max_sections_to_pass, reached_end, paused
    
    if sections_passed >= max_sections_to_pass:
        reached_end = True

    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the color buffer
    glLoadIdentity()  # Reset the model-view matrix
    powerup()
    draw_maze()  # Draw the maze
    draw_player()  # Draw the player
    draw_buttons()  # Draw the buttons
    
    glColor3f(1.0, 1.0, 1.0)  # Set text color to white
    glRasterPos2f(window_width - 150, window_height - 30)  # Position the score text
    score_text = f"Score: {score}"
    for character in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))  # Render each character
    
    draw_win_screen()
    # if not game_over:
    #     draw_invulnerability_timer()

    if game_over:
        draw_game_over_screen()

    if paused or game_over:  # Check if the game is paused or over
        glutSwapBuffers()  # Swap buffers for double buffering
        return
    

    glColor3f(1.0, 1.0, 1.0)  # Set text color to white
    glRasterPos2f(window_width - 150, window_height - 30)  # Position the score text
    score_text = f"Score: {score}"
    for character in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))  # Render each character

    if not game_over:
        draw_timer()
        draw_invulnerability_timer()

    glutSwapBuffers()  # Swap buffers for double buffering

# Initialize GLUT and create window
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)  # Enable double buffering
glutInitWindowSize(window_width, window_height)
glutCreateWindow(b"2D Maze Game")

init()  # Initialize OpenGL settings

# Register callback functions
glutDisplayFunc(display)
glutIdleFunc(display)  # For continuous rendering
glutKeyboardFunc(keyboard_listener)  # Register keyboard listener
glutMouseFunc(mouse_click)  # Register mouse click listener

# Start the main loop
glutMainLoop()