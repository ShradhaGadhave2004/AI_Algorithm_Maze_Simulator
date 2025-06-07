# Maze Pathfinding Visualization

An interactive Python application that visualizes pathfinding algorithms like A*, BFS, and DFS on a randomly generated maze using `Tkinter`.

---

## 🧩 Description

**Maze Pathfinding Visualization** is a desktop GUI application built with Python. It creates a randomized maze and allows users to visualize how different pathfinding algorithms work. The user can select start and end points and observe the traversal path with animations and sound effects.

---

## 🎯 Features

- Generates a random maze using recursive backtracking.
- Interactive GUI using **Tkinter**.
- Sound effects for user interactions and pathfinding completion using **Pygame**.
- Visualize the following algorithms:
  - A* (A-star)
  - BFS (Breadth-First Search)
  - DFS (Depth-First Search)
- Select start and end points with mouse clicks.
- Clear and regenerate the maze.
- Welcome screen with background music and transition effect.

---

## 🛠️ Tech Stack

- **Python 3**
- **Tkinter** for GUI
- **Pygame** for sound
- **Pillow (PIL)** for image handling
- **PriorityQueue** from `queue` module for A*

---

## 📦 Requirements

- Python 3.6 or higher
- Required Python packages:
  ```bash
  pip install pygame Pillow

---

## 🚀 Getting Started

1. Clone the Repository
 ```bash
 git clone https://github.com/yourusername/AI_Algorithm_Maze_Simulator.git
 cd Maze_Simulator
 ```
2. **🔊 Sound Effects :**
Ensure your sound/ directory contains:
Click_effect.mp3
Background_music.mp3
path_found.mp3
You may change these with your preferred sound files, but update the paths accordingly in maze.py.
3. **🖼️ Visual Assets :**
The GUI uses background images (bg2.jpeg) located in the images/ folder. Replace this with your own image for customization.

## 📌 How to Use

1. Run the script:
```bash
python maze.py
```
2. A welcome screen appears with background music.
3. Click Start to enter the maze viewer.
4. Select a pathfinding algorithm (A*, BFS, DFS).
5. Click on a start point (green) and then an end point (blue) on the maze grid.
6. The algorithm will visualize the traversal with animations and sounds.
7. Use Clear to reset and try a new path.

## 🧠 Algorithms
***A* (A-star):**
Uses heuristics for optimal and efficient pathfinding.

Color path: Red

**BFS (Breadth-First Search):**
Explores equally in all directions, ensures shortest path.

Color path: Green

**DFS (Depth-First Search):**
Explores deeply first, may not find the shortest path.

Color path: Blue

## 👩‍💻 Author
Shradha Gadhave
