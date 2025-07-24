# Snake Game

A classic Snake game implemented using HTML5 Canvas and JavaScript. This simple yet addictive game challenges players to control a snake, eat food, and grow as long as possible without colliding with walls or itself.

## Table of Contents

- [Game Overview](#game-overview)
- [How to Play](#how-to-play)
- [Running the Game](#running-the-game)
- [Code Structure](#code-structure)
- [Game Features](#game-features)
- [Future Enhancements](#future-enhancements)

## Game Overview

This implementation of the Snake game features:

- Responsive canvas-based gameplay
- Score tracking
- Game over detection
- Restart functionality
- Clean, modern UI

## How to Play

1. Use the arrow keys (↑, ↓, ←, →) to control the snake's direction
2. Eat the red food dots to grow longer and increase your score
3. Avoid hitting the walls or colliding with your own body
4. Try to achieve the highest score possible

## Running the Game

### Using Python's HTTP Server

You can easily run this game using Python's built-in HTTP server. Follow these steps:

1. Make sure you have Python installed on your computer
2. Open a command prompt or terminal
3. Navigate to the directory containing the game files
4. Run one of the following commands based on your Python version:

   For Python 3.x:
   ```
   python -m http.server 8000
   ```

   For Python 2.x:
   ```
   python -m SimpleHTTPServer 8000
   ```

5. Open your web browser and go to: `http://localhost:8000`
6. Click on `index.html` or navigate directly to `http://localhost:8000/index.html`

### Alternative Methods

You can also run the game by:

- Opening the `index.html` file directly in a modern web browser
- Using any other web server of your choice (Node.js, Apache, etc.)

## Code Structure

The game consists of two main files:

### index.html

Contains the HTML structure and CSS styling for the game interface, including:

- Game canvas
- Score display
- Game over screen with restart button
- Embedded CSS for styling all elements

### game.js

Contains all the JavaScript game logic, including:

- Game initialization and setup
- Snake movement and control
- Food generation
- Collision detection
- Scoring system
- Rendering functions
- Event listeners for keyboard input

## Game Features

### Core Mechanics

- **Grid-Based Movement**: The snake moves on a grid system, with each cell being 20x20 pixels
- **Direction Control**: The snake's direction can be changed using arrow keys, with prevention of 180-degree turns
- **Food Generation**: Food spawns randomly on the grid, never on the snake's body
- **Growth Mechanism**: The snake grows longer each time it eats food
- **Collision Detection**: Game ends when the snake hits a wall or itself

### Visual Elements

- **Snake Rendering**: The snake is drawn as a series of green squares with subtle borders
- **Food Rendering**: Food is displayed as red circles
- **Grid Background**: Optional grid lines for better visual reference
- **Game Over Screen**: A modal appears when the game ends, showing the final score

### User Interface

- **Score Display**: Current score is shown below the game canvas
- **Restart Button**: Allows players to start a new game after losing
- **Responsive Design**: The game interface is centered and works well on various screen sizes

## Future Enhancements

Possible improvements for future versions:

- Different difficulty levels (speed settings)
- Mobile touch controls
- High score tracking using local storage
- Sound effects and background music
- Power-ups and special food items
- Multiple game modes

---

Enjoy playing the Snake game! Feel free to modify and enhance it as you like.