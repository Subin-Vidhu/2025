# Snake Game with Special Effects

A modern implementation of the classic Snake game using HTML5 Canvas and JavaScript, featuring special effects and interactive elements.

## Features

- 🐍 Classic snake movement and growth mechanics
- 🍎 Moving apple target that bounces off walls
- 💥 Particle explosion effects when eating food
- 🎨 Dynamic background color changes
- 📱 Responsive canvas design
- 🎮 Score tracking system

## Technical Implementation

### Project Structure

```
Snake_game/
├── index.html      # Game HTML structure and styling
├── game.js         # Game logic and rendering
└── README.md       # Documentation
```

### Core Components

#### 1. Game Objects

##### Snake
```javascript
let snake = {
    x: 10,              // Current X position
    y: 10,              // Current Y position
    dx: 0,              // X direction (-1, 0, 1)
    dy: 0,              // Y direction (-1, 0, 1)
    cells: [],          // Array of body segments
    maxCells: 4         // Initial length
};
```

##### Food (Apple)
```javascript
let food = {
    x: 15,              // Current X position
    y: 15,              // Current Y position
    dx: 1,              // X direction for movement
    dy: 1,              // Y direction for movement
    speed: 0.2          // Movement speed
};
```

#### 2. Special Effects

##### Particle System
The game implements a particle system for explosion effects when the snake eats food:

- `Particle` class: Manages individual particles with properties:
  - Position (x, y)
  - Velocity (dx, dy)
  - Alpha (transparency)
  - Size

```javascript
class Particle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.dx = (Math.random() - 0.5) * 4;
        this.dy = (Math.random() - 0.5) * 4;
        this.alpha = 1;
        this.size = Math.random() * 3 + 2;
    }
}
```

##### Background Effects
- Uses a predefined color palette
- Changes randomly upon food collection
```javascript
let backgroundColors = ['#FFE5E5', '#E5FFE5', '#E5E5FF', '#FFFFE5', '#FFE5FF', '#E5FFFF'];
```

#### 3. Core Functions

##### Game Loop (`drawGame`)
- Clears canvas with current background
- Updates snake position
- Handles wall wrapping
- Updates snake body segments
- Renders food (apple emoji)
- Updates and renders particles
- Checks collisions
- Updates score

##### Movement Functions
- `moveFood()`: Handles apple movement and wall bouncing
- `handleKeyPress(e)`: Processes keyboard input for snake direction

##### Collision Detection
- Snake-Food collision: Triggers growth, score increase, and effects
- Snake-Self collision: Triggers game reset

### Event Handling

The game uses keyboard event listeners for controls:
- Arrow Left: Move left
- Arrow Right: Move right
- Arrow Up: Move up
- Arrow Down: Move down

```javascript
document.addEventListener('keydown', handleKeyPress);
```

### Canvas Rendering

The game uses HTML5 Canvas for rendering:
- Canvas size: 400x400 pixels
- Grid size: 20x20 pixels
- Updates every 100ms

## How to Run

1. Clone or download the repository
2. Start a local server in the project directory:
   ```bash
   python -m http.server 8000
   ```
3. Open a web browser and navigate to `http://localhost:8000`

## Game Mechanics

1. **Snake Movement**
   - Snake moves continuously in the current direction
   - Cannot reverse direction directly (prevent self-collision)
   - Wraps around screen edges

2. **Scoring System**
   - +10 points for each apple collected
   - Score resets on self-collision

3. **Special Effects**
   - Particle explosion on food collection
   - Background color changes on food collection
   - Moving apple target with bounce physics

## Technical Notes

- The game uses requestAnimationFrame for smooth animation
- Particle effects are optimized by removing invisible particles
- Collision detection uses grid-based positioning
- Apple movement uses simple bounce physics
- Emoji rendering is handled using canvas text operations

## Future Enhancements

Possible improvements that could be added:
- Multiple difficulty levels
- Power-ups system
- High score persistence
- Mobile touch controls
- Sound effects
- Multiplayer support

## Contributing

Feel free to fork this project and submit pull requests for any enhancements.
