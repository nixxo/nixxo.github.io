road = document.querySelectorAll('#grid > div');
gameScore = document.querySelector('#game-score');

// Riferimenti duck
const duckIdx = 1;
const duck = road[duckIdx];
duck.classList.add('duck');

function jump(event){
    if (event.code === 'Space' && !event.repeat) {
        duck.classList.add('duck-jump');
        setTimeout(function() {
            duck.classList.remove('duck-jump');
        }, 400);
        
    }
}

document.addEventListener('keydown', jump);
let speed = 400;
let score = 0;

function addPlant() {
    let plantIdx = road.length - 1;
    road[plantIdx].classList.add('plant');

    const plantMovement = setInterval(() => {
        // console.log(plantIdx);
        score++;
        gameScore.innerText = score;
        road[plantIdx].classList.remove('plant');
        plantIdx--;
        if (plantIdx < 0) {
            clearInterval(plantMovement);
            addPlant();
            return;
        }
        road[plantIdx].classList.add('plant');

        if (
            duckIdx === plantIdx &&
            !road[plantIdx].classList.contains('duck-jump')
        ) {
            showAlert(`CRASH with score: ${score}`);
            clearInterval(plantMovement);
            return;
        } else if (duckIdx === plantIdx) console.log('JUMP');

    }, speed);
}

addPlant();






