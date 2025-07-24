// Get the canvas element and its context
const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');

// Game settings
const gridSize = 20; // Size of each grid cell in pixels
const gameSpeed = 100; // Milliseconds between game updates

// Game state variables
let snake = [];
let food = {};
let direction = 'right';
let nextDirection = 'right';
let score = 0;
let gameRunning = false;
let gameLoop;

// Initialize the game
function initGame() {
    // Reset game state
    snake = [
        { x: 5, y: 5 },
        { x: 4, y: 5 },
        { x: 3, y: 5 }
    ];
    score = 0;
    direction = 'right';
    nextDirection = 'right';
    gameRunning = true;
    
    // Hide game over screen
    document.getElementById('game-over').style.display = 'none';
    
    // Update score display
    updateScoreDisplay();
    
    // Generate initial food
    generateFood();
    
    // Start game loop
    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(gameUpdate, gameSpeed);
    
    // Initial render
    render();
}

// Generate food at random position
function generateFood() {
    // Generate random coordinates
    const maxX = Math.floor(canvas.width / gridSize) - 1;
    const maxY = Math.floor(canvas.height / gridSize) - 1;
    
    food = {
        x: Math.floor(Math.random() * maxX),
        y: Math.floor(Math.random() * maxY)
    };
    
    // Make sure food doesn't spawn on snake
    for (let segment of snake) {
        if (segment.x === food.x && segment.y === food.y) {
            // If food spawns on snake, try again
            return generateFood();
        }
    }
}

// Update score display
function updateScoreDisplay() {
    document.getElementById('score-display').textContent = `Score: ${score}`;
}

// Main game update function
function gameUpdate() {
    // Update direction
    direction = nextDirection;
    
    // Get current head position
    const head = { ...snake[0] };
    
    // Update head position based on direction
    switch (direction) {
        case 'up':
            head.y -= 1;
            break;
        case 'down':
            head.y += 1;
            break;
        case 'left':
            head.x -= 1;
            break;
        case 'right':
            head.x += 1;
            break;
    }
    
    // Check for collisions
    if (checkCollision(head)) {
        gameOver();
        return;
    }
    
    // Add new head to snake
    snake.unshift(head);
    
    // Check if snake ate food
    if (head.x === food.x && head.y === food.y) {
        // Increase score
        score += 10;
        updateScoreDisplay();
        
        // Generate new food
        generateFood();
    } else {
        // Remove tail if snake didn't eat food
        snake.pop();
    }
    
    // Render the updated game state
    render();
}

// Check for collisions with walls or self
function checkCollision(head) {
    // Check wall collisions
    const maxX = Math.floor(canvas.width / gridSize) - 1;
    const maxY = Math.floor(canvas.height / gridSize) - 1;
    
    if (head.x < 0 || head.x > maxX || head.y < 0 || head.y > maxY) {
        return true;
    }
    
    // Check self collision (skip the last segment as it will be removed)
    for (let i = 0; i < snake.length - 1; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            return true;
        }
    }
    
    return false;
}

// Game over function
function gameOver() {
    gameRunning = false;
    clearInterval(gameLoop);
    
    // Show game over screen
    const gameOverScreen = document.getElementById('game-over');
    document.getElementById('final-score').textContent = `Your score: ${score}`;
    gameOverScreen.style.display = 'block';
}

// Render function
function render() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid (optional)
    drawGrid();
    
    // Draw snake
    ctx.fillStyle = '#4CAF50';
    for (let segment of snake) {
        ctx.fillRect(
            segment.x * gridSize,
            segment.y * gridSize,
            gridSize,
            gridSize
        );
        
        // Draw border around segment
        ctx.strokeStyle = '#45a049';
        ctx.strokeRect(
            segment.x * gridSize,
            segment.y * gridSize,
            gridSize,
            gridSize
        );
    }
    
    // Draw food
    ctx.fillStyle = '#FF5722';
    ctx.beginPath();
    ctx.arc(
        food.x * gridSize + gridSize / 2,
        food.y * gridSize + gridSize / 2,
        gridSize / 2,
        0,
        Math.PI * 2
    );
    ctx.fill();
}

// Draw grid lines (optional)
function drawGrid() {
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 0.5;
    
    // Draw vertical lines
    for (let x = 0; x <= canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    
    // Draw horizontal lines
    for (let y = 0; y <= canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}

// Handle keyboard input
document.addEventListener('keydown', (event) => {
    if (!gameRunning) return;
    
    // Prevent default behavior for arrow keys
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
        event.preventDefault();
    }
    
    // Update direction based on key press
    // Prevent 180-degree turns
    switch (event.key) {
        case 'ArrowUp':
            if (direction !== 'down') nextDirection = 'up';
            break;
        case 'ArrowDown':
            if (direction !== 'up') nextDirection = 'down';
            break;
        case 'ArrowLeft':
            if (direction !== 'right') nextDirection = 'left';
            break;
        case 'ArrowRight':
            if (direction !== 'left') nextDirection = 'right';
            break;
    }
});

// Handle restart button click
document.getElementById('restart-button').addEventListener('click', initGame);

// Start the game when the page loads
window.addEventListener('load', initGame);