import random
import time
import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue
from PIL import Image, ImageTk
import pygame

class Maze:
    def __init__(self, width, height):
        self.width = width // 2 * 2 + 1
        self.height = height // 2 * 2 + 1
        self.cells = [[True for _ in range(self.width)] for _ in range(self.height)]

    def set_path(self, x, y):
        self.cells[y][x] = False

    def is_wall(self, x, y):
        return not (0 <= x < self.width and 0 <= y < self.height) or self.cells[y][x]

    def create_maze(self, x, y):
        self.set_path(x, y)
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < self.width and 0 <= ny < self.height and self.is_wall(nx, ny):
                self.set_path(x + dx, y + dy)
                self.create_maze(nx, ny)

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Load sound effect
button_click_sound = pygame.mixer.Sound(r"C:\Users\Dell\OneDrive\Desktop\AI Maze\Maze_Simulator\sound\Click_effect.mp3")
open_sound = pygame.mixer.Sound(r"C:\Users\Dell\OneDrive\Desktop\AI Maze\Maze_Simulator\sound\Background_music.mp3")
open2_sound = pygame.mixer.Sound(r"C:\Users\Dell\OneDrive\Desktop\AI Maze\Maze_Simulator\sound\open_effect.mp3")
# Load sound effect for final path (replace with your actual sound file)
final_path_sound = pygame.mixer.Sound(r"C:\Users\Dell\OneDrive\Desktop\AI Maze\Maze_Simulator\sound\path_found.mp3")  # Replace with your sound file path

# Function to play sound when the final path is traced
def play_final_path_sound():
    final_path_sound.play()

# Function to play sound when button is clicked
def play_button_click_sound():
    button_click_sound.play()

# Function to play sound in loop until the page is displayed
def play_background_music():
    open_sound.play(loops=-1, maxtime=0)  # Loop indefinitely

# Function to stop background sound
def stop_background_music():
    open_sound.stop()

# Function to show the maze page
def show_maze_page():
    maze_frame.tkraise()

def center_window(window, width, height, offset=35):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2 - offset  # Adjust upward by subtracting offset
    window.geometry(f"{width}x{height}+{x}+{y}")

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def visualize(canvas, explored, cell_size, color):
    for x, y in explored:
        x0 = x * cell_size
        y0 = y * cell_size
        x1 = x0 + cell_size
        y1 = y0 + cell_size
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        canvas.update()
        time.sleep(0.04)


def draw_path(canvas, path, cell_size, color):
    for x, y in path:
        x0 = x * cell_size
        y0 = y * cell_size
        x1 = x0 + cell_size
        y1 = y0 + cell_size
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        canvas.update()


def a_star(maze, start, end, canvas, cell_size):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    explored = []

    while not open_set.empty():
        _, current = open_set.get()
        if current == end:
            visualize(canvas, explored, cell_size, color="yellow")
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            play_final_path_sound()
            return path

        x, y = current
        explored.append(current)

        for dx, dy in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            neighbor = (x + dx, y + dy)
            if maze.is_wall(*neighbor):
                continue
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                open_set.put((f_score[neighbor], neighbor))
    return None


def bfs(maze, start, end, canvas, cell_size):
    queue = [start]
    came_from = {start: None}
    explored = []

    while queue:
        current = queue.pop(0)
        if current == end:
            visualize(canvas, explored, cell_size, color="cyan")
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            play_final_path_sound()
            return path

        x, y = current
        explored.append(current)

        for dx, dy in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            neighbor = (x + dx, y + dy)
            if maze.is_wall(*neighbor) or neighbor in came_from:
                continue
            queue.append(neighbor)
            came_from[neighbor] = current
    return None


def dfs(maze, start, end, canvas, cell_size):
    stack = [start]
    came_from = {start: None}
    explored = []

    while stack:
        current = stack.pop()
        if current == end:
            visualize(canvas, explored, cell_size, color="magenta")
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            play_final_path_sound()
            return path

        x, y = current
        explored.append(current)

        for dx, dy in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            neighbor = (x + dx, y + dy)
            if maze.is_wall(*neighbor) or neighbor in came_from:
                continue
            stack.append(neighbor)
            came_from[neighbor] = current
    return None


def draw_maze(canvas, maze, cell_size):
    rows = len(maze)
    cols = len(maze[0])
    for row in range(rows):
        for col in range(cols):
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            color = "white" if not maze[row][col] else "black"
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")


# Function to display a message
def show_message(message):
    messagebox.showinfo("Error", message)

selecting_start = True

# Modified on_canvas_click function
def on_canvas_click(event):
    global start, end, selecting_start, current_algorithm
    x, y = event.x // cell_size, event.y // cell_size

    # Check if the clicked cell is a wall (assuming 1 represents a wall in the maze)
    if obj.cells[y][x] == 1:  # 1 represents a wall
        show_message("Can't select a wall cell as start or end.")
        return  # Don't allow selecting a wall cell

    if selecting_start:
        # If selecting start, set the start point
        start = (x, y)
        canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill="green", outline="")
        selecting_start = False
    else:
        # If selecting end, set the end point
        end = (x, y)
        canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill="blue", outline="")

        # Call the selected algorithm and get the path
        path = None
        if current_algorithm == "A*":
            path = a_star(obj, start, end, canvas, cell_size)
        elif current_algorithm == "BFS":
            path = bfs(obj, start, end, canvas, cell_size)
        elif current_algorithm == "DFS":
            path = dfs(obj, start, end, canvas, cell_size)

        # If a path is found, draw it
        if path:
            draw_path(canvas, path, cell_size, color="red" if current_algorithm == "A*" else "green" if current_algorithm == "BFS" else "blue")
        else:
            show_message(f"No path found using {current_algorithm} algorithm.")


# Global variable to store the current selected algorithm button
selected_button = None

def set_algorithm(algorithm):
    global selected_button, current_algorithm

    # Update the current algorithm
    current_algorithm = algorithm
    play_button_click_sound()  # Play sound on algorithm selection
    # Reset the style of the previously selected button if it exists
    if selected_button:
        selected_button.config(bg="#FF0060", fg="black")  # Reset to original style
    
    # Find the new selected button and highlight it
    if algorithm == "A*":
        selected_button = a_button
    elif algorithm == "BFS":
        selected_button = bfs_button
    elif algorithm == "DFS":
        selected_button = dfs_button

    # Highlight the selected button
    selected_button.config(bg="#416D19", fg="white")  # Highlight the selected button
    
    # Perform any additional actions needed based on the selected algorithm
    print(f"Selected algorithm: {algorithm}")

def clear_grid():
    play_button_click_sound() 
    global start, end, selecting_start
    # Reinitialize the maze and reset the state
    obj.create_maze(0, 0)
    start = None
    end = None
    selecting_start = True
    canvas.delete("all")
    draw_maze(canvas, obj.cells, cell_size)


def start_app():
    start_frame.pack_forget()
    maze_frame.pack()
    stop_background_music()
    open2_sound.play()  # Play sound on maze page transition

def sparkle_text(label, colors, index=0):
    # Update text color
    label.config(fg=colors[index])
    # Schedule the next color change
    next_index = (index + 1) % len(colors)
    label.after(600, sparkle_text, label, colors, next_index)

# Maze dimensions
maze_width = 21
maze_height = 21

# Create the maze
obj = Maze(maze_width, maze_height)
obj.create_maze(0, 0)

# GUI settings
cell_size = 20
rows = len(obj.cells)
cols = len(obj.cells[0])
canvas_width = cols * cell_size
canvas_height = rows * cell_size

# Initialize Tkinter
root = tk.Tk()
root.title("Maze Pathfinding Visualization")
root.geometry("800x600")

# Center the start frame window
center_window(root,700,735)

# Start screen
start_frame = tk.Frame(root)
start_frame.pack(fill="both", expand=True)

# Load and set the background image
bg_image = Image.open(r"C:\Users\Dell\OneDrive\Desktop\AI Maze\Maze_Simulator\images\bg2.jpeg")  # Replace with your image file path
bg_image = bg_image.resize((700, 660), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(start_frame, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add text and buttons on the start screen
welcome_label = tk.Label(
    start_frame,
    text="Welcome to Maze Pathfinding Visualization",
    font=("Pixel Emulator", 25, "bold"),
    fg="white",  # Text color
)

welcome_label.place(relx=0.5, rely=0.4, anchor="center")

# Start the sparkling effect with a list of colors
colors = [ "#72147E","#FF0060","#BE0000"]
sparkle_text(welcome_label, colors)

start_button = tk.Button(start_frame, text="Start", font=("Pixel Emulator", 15, "bold"),relief="ridge", bg="#FF0060", fg="white", command=start_app)
start_button.place(relx=0.5, rely=0.55, anchor="center")

# Maze Visualization Page
maze_frame = tk.Frame(root)

# Load and set the background image
bg_image_maze = Image.open(r"C:\Users\Dell\OneDrive\Desktop\AI Maze\Maze_Simulator\images\bg2.jpeg")  # Replace with your image file path
bg_image_maze = bg_image.resize((600,700), Image.Resampling.LANCZOS)
bg_image_maze = ImageTk.PhotoImage(bg_image_maze)

background_label = tk.Label(maze_frame, image=bg_image_maze)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas = tk.Canvas(maze_frame, width=canvas_width, height=canvas_height, bg="black")
canvas.pack(padx=60,pady=105)

a_button=tk.Button(maze_frame, text="A*",font=("Arial", 14), bg="#FF0060", fg="white", command=lambda: set_algorithm("A*"))
a_button.place(relx=0.05,rely=0.88)
bfs_button=tk.Button(maze_frame, text="BFS",font=("Arial", 14), bg="#FF0060", fg="white", command=lambda: set_algorithm("BFS"))
bfs_button.place(relx=0.135,rely=0.88)
dfs_button=tk.Button(maze_frame, text="DFS",font=("Arial", 14), bg="#FF0060", fg="white", command=lambda: set_algorithm("DFS"))
dfs_button.place(relx=0.25,rely=0.88)

clear_button = tk.Button(maze_frame, text="Clear", font=("Pixel Emulator", 14, "bold"), bg="#FF0060", fg="white", command=clear_grid)
clear_button.place(relx=0.82, rely=0.88)

# Draw the maze
draw_maze(canvas, obj.cells, cell_size)

# Global variables
start = None
end = None
current_algorithm = "A*"
selecting_start = True

# When the application starts, highlight A* by default
play_background_music()
set_algorithm("A*")

# Event bindings
canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()
