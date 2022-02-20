time_display = document.getElementById('time_display');
let timer = 5;
time_display.innerText = timer;

score_display = document.getElementById('score_display');
let score = 0;
score_display.innerText = score;

let bug_speed = 1000;

const cells = document.querySelectorAll('.cell');

function randomBug() {
    removeBug();
    const rnd = Math.floor(Math.random() * cells.length)
    const cell = cells[rnd];
    cell.classList.add('bug');
}

// pulisci griglia
function removeBug() {
    for (let index = 0; index < cells.length; index++) {
        const element = cells[index];
        element.classList.remove('bug');
    }
}

const bugMovement = setInterval(randomBug, bug_speed);

for (let i = 0; i < cells.length; i++) {
    const cell = cells[i];
    cell.addEventListener('click', function(){
        if (cell.classList.contains('bug')) {
            score++;
            score_display.innerText = score;
            cell.classList.add('splat');
            setTimeout(function() {
                cell.classList.remove('splat');  
            }, 300);
        }
    });
}

function countDown() {
    timer--;
    time_display.innerText = timer;
    if (timer === 0) {
        clearInterval(bugMovement);
        clearInterval(tmr);
        showAlert(`game end: ${score} points`);
    }
}

// TIMER
const tmr = setInterval(countDown, 1000);