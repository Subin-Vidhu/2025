const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');

const gridSize = 20;
const tileCount = canvas.width / gridSize;

// Snake properties
let snake = {
    x: 10,
    y: 10,
    dx: 0,
    dy: 0,
    cells: [],
    maxCells: 4
};

// Food properties
let food = {
    x: 15,
    y: 15,
    dx: 1,
    dy: 1,
    speed: 0.2
};

let score = 0;
let backgroundColors = ['#FFE5E5', '#E5FFE5', '#E5E5FF', '#FFFFE5', '#FFE5FF', '#E5FFFF'];
let currentBgColor = backgroundColors[0];

// Particle system for explosion effect
let particles = [];
class Particle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.dx = (Math.random() - 0.5) * 4;
        this.dy = (Math.random() - 0.5) * 4;
        this.alpha = 1;
        this.size = Math.random() * 3 + 2;
    }

    update() {
        this.x += this.dx;
        this.y += this.dy;
        this.alpha -= 0.02;
    }

    draw() {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = '#FFD700';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}

function createExplosion(x, y) {
    for (let i = 0; i < 20; i++) {
        particles.push(new Particle(x, y));
    }
}

function moveFood() {
    // Move food
    food.x += food.dx * food.speed;
    food.y += food.dy * food.speed;

    // Bounce off walls
    if (food.x < 0 || food.x >= tileCount) food.dx *= -1;
    if (food.y < 0 || food.y >= tileCount) food.dy *= -1;
}

function drawGame() {
    // Clear canvas with current background color
    ctx.fillStyle = currentBgColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Move and draw snake
    snake.x += snake.dx;
    snake.y += snake.dy;

    // Wrap snake position
    if (snake.x < 0) snake.x = tileCount - 1;
    if (snake.x >= tileCount) snake.x = 0;
    if (snake.y < 0) snake.y = tileCount - 1;
    if (snake.y >= tileCount) snake.y = 0;

    // Keep track of where snake has been
    snake.cells.unshift({ x: snake.x, y: snake.y });
    if (snake.cells.length > snake.maxCells) {
        snake.cells.pop();
    }

    // Draw food (apple emoji)
    ctx.font = `${gridSize}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('🍎', (food.x + 0.5) * gridSize, (food.y + 0.5) * gridSize);

    // Draw snake
    ctx.fillStyle = 'green';
    snake.cells.forEach((cell, index) => {
        ctx.fillRect(cell.x * gridSize, cell.y * gridSize, gridSize - 1, gridSize - 1);
    });

    // Update and draw particles
    particles = particles.filter(particle => particle.alpha > 0);
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    // Check collision with food
    if (Math.abs(snake.x - food.x) < 1 && Math.abs(snake.y - food.y) < 1) {
        snake.maxCells++;
        score += 10;
        scoreElement.textContent = score;
        
        // Change background color
        currentBgColor = backgroundColors[Math.floor(Math.random() * backgroundColors.length)];
        
        // Create explosion effect
        createExplosion((food.x + 0.5) * gridSize, (food.y + 0.5) * gridSize);

        // Move food to new random position
        food.x = Math.floor(Math.random() * tileCount);
        food.y = Math.floor(Math.random() * tileCount);
    }

    // Move food
    moveFood();

    // Check collision with self
    for (let i = 1; i < snake.cells.length; i++) {
        if (snake.x === snake.cells[i].x && snake.y === snake.cells[i].y) {
            // Reset game
            snake.x = 10;
            snake.y = 10;
            snake.cells = [];
            snake.maxCells = 4;
            snake.dx = 0;
            snake.dy = 0;
            score = 0;
            scoreElement.textContent = score;
        }
    }
}

function handleKeyPress(e) {
    // Prevent snake from reversing
    if (e.key === 'ArrowLeft' && snake.dx === 0) {
        snake.dx = -1;
        snake.dy = 0;
    }
    else if (e.key === 'ArrowRight' && snake.dx === 0) {
        snake.dx = 1;
        snake.dy = 0;
    }
    else if (e.key === 'ArrowUp' && snake.dy === 0) {
        snake.dx = 0;
        snake.dy = -1;
    }
    else if (e.key === 'ArrowDown' && snake.dy === 0) {
        snake.dx = 0;
        snake.dy = 1;
    }
}

document.addEventListener('keydown', handleKeyPress);
setInterval(drawGame, 100);
