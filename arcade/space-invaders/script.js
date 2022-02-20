const grid = document.querySelector('#grid');
const gridSize = 8;
let cells = []


/* formazione aliena a diamante
    *
  *   *
*   *   *
  *   *
    *
*/
let aliens = [
    2,
    gridSize + 1, gridSize + 3,
    gridSize*2, gridSize*2 + 2, gridSize*2 + 4,
    gridSize*3 + 1, gridSize*3 + 3,
    gridSize*4 + 2,
]


let step = 1;
let spaceshipPosition = Math.floor(gridSize * gridSize - gridSize / 2);
let aliensSpeed = 700;
let aliensMovement = null;

function drawGameArea() {
    for (let i = 0; i < gridSize * gridSize; i++) {
        const cell = document.createElement('div');
        cell.innerText = i;
        cells.push(cell);
        grid.appendChild(cell);
    }
}

function leftmostAlien() {
    let min = gridSize;
    let idx = 0;
    for (let i = 0; i < aliens.length; i++) {
        if (aliens[i] % gridSize <= min) {
            min = aliens[i] % gridSize;
            idx = i;
        }       
    }
    return idx;
}

function rightmostAlien() {
    let max = 0;
    let idx = aliens.length - 1;
    for (let i = aliens.length - 1; i >= 0; i--) {
        if (aliens[i] % gridSize >= max) {
            max = aliens[i] % gridSize;
            idx = i;
        }       
    }
    return idx;
}

function drawAliens() {
    for (let i = 0; i < aliens.length; i++) {
        if (cells[aliens[i]].classList.contains('spaceship')) {
            cells[aliens[i]].classList.remove('spaceship');
            cells[aliens[i]].classList.add('boom');
            showAlert('ALIENS WINS');
            clearInterval(aliensMovement);
            return;
        }
        cells[aliens[i]].classList.add('alien');
    }
}

function deleteAliens() {
    for (let i = 0; i < aliens.length; i++) {
        cells[aliens[i]].classList.remove('alien');
    }
}

function moveAliens() {
    const leftAlien = leftmostAlien();
    const rightAlien = rightmostAlien();
    const leftEdge = aliens[leftAlien] % gridSize === 0;
    const rightEdge = aliens[rightAlien] % gridSize === gridSize - 1;

    deleteAliens();

    if(step > 0 && rightEdge) {
        for (let i = 0; i < aliens.length; i++) {
            aliens[i] += gridSize;
            step = -1;
        }
    } else if(step < 0 && leftEdge) {
        for (let i = 0; i < aliens.length; i++) {
            aliens[i] += gridSize;
            step = 1;
        }
    } else {
        for (let i = 0; i < aliens.length; i++) {
            aliens[i] += step;
        }
    }
    drawAliens();
}

function moveSpaceship(event) {
    const leftEdge = spaceshipPosition % gridSize === 0;
    const rightEdge = spaceshipPosition % gridSize === gridSize - 1;
    
    cells[spaceshipPosition].classList.remove('spaceship');
    if (event.code === 'ArrowRight' && !rightEdge) {
        spaceshipPosition++;
    } else if (event.code === 'ArrowLeft' && !leftEdge) {
        spaceshipPosition--;
    }
    cells[spaceshipPosition].classList.add('spaceship');
}

function shootLaset(event) {
    if (event.code !== 'Space') return;

    let laserPosition = spaceshipPosition;
    let laserInterval = null;
    function moveLaser() {
        cells[laserPosition].classList.remove('laser');
        laserPosition -= gridSize;
        if (laserPosition < 0) {
            clearInterval(laserInterval);
            return;
        }
        if (cells[laserPosition].classList.contains('alien')) {
            cells[laserPosition].classList.remove('alien');
            cells[laserPosition].classList.add('boom');
            aliens = aliens.filter(function(v) { return v != laserPosition });

            setTimeout(function(){
                cells[laserPosition].classList.remove('boom');
            }, 200)

            clearInterval(laserInterval);

            if (aliens.length === 0) {
                showAlert('VITTORIA UMANI');
            }

            return;
        } else {
            cells[laserPosition].classList.add('laser');
        }
    }
    laserInterval = setInterval(moveLaser, 200);
}

// disegna area di gioco
document.documentElement.style.setProperty('--grid-size', gridSize);
drawGameArea();

// disegna navicella e assegna tasti
cells[spaceshipPosition].classList.add('spaceship');
document.addEventListener('keydown', moveSpaceship);
document.addEventListener('keydown', shootLaset);

// disegna alieni e inizia moviemento
drawAliens();
aliensMovement = setInterval(moveAliens, aliensSpeed);