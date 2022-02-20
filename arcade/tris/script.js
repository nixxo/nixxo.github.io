console.log('script init')

const cells = document.querySelectorAll('.cell');

let playerGrid = [];
const simbols = ['X', 'O']
let turn = 0;

for (let index = 0; index < cells.length; index++) {
    const cell = cells[index];
    cell.addEventListener('click', function () {
        turn++;
        simbol = simbols[turn % 2]
        playerGrid[index] = simbol;
        cell.innerHTML = simbol;
        const victory = checkVictory();
        if (victory) {
            showAlert(`${simbol} ha vinto`);
        }
        else if (turn == 9) {
            showAlert(`pareggio`);
        }

    })
}

function checkVictory() {
    const victoryConditions = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6],
    ];

    for (let index = 0; index < victoryConditions.length; index++) {
        const condition = victoryConditions[index];

        const a = condition[0];
        const b = condition[1];
        const c = condition[2];
        
        // console.log(`cond: ${a} ${b} ${c}`)
        if (playerGrid[a] && playerGrid[a] === playerGrid[b] && playerGrid[b] === playerGrid[c]){
            return true;
        }

    }
    return false;

}
