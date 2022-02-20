const grid = document.getElementById('grid')
const error_count = document.getElementById('error_count');
const cards = [
    "alien",
    "bug",
    "duck",
    "rocket",
    "spaceship",
    "tiktac"
];

let pick = [];
let errors = 0;

const deck = [...cards, ...cards];
deck.sort(function () {
    return 0.5 - Math.random();
})

for (let index = 0; index < deck.length; index++) {
    const card = document.createElement('div');
    card.classList.add('card');
    card.setAttribute('data-name', deck[index]);
    card.addEventListener('click', flipCard)

    grid.appendChild(card);
}

function flipCard(event){
    const card = event.target;

    if (card.classList.contains('flipped')) return;

    card.classList.add(card.getAttribute('data-name'), 'flipped');

    pick.push(card);
    if (pick.length == 2){
        checkMatch();
    }
}

function checkMatch() {
    const card0 = pick[0];
    const card0name = card0.getAttribute('data-name');
    const card1 = pick[1];
    const card1name = card1.getAttribute('data-name');

    if (card0name === card1name) {
        console.log('match!!!');
        if (checkWin()) showAlert('vittoria');
    } else {
        setTimeout(function () {
            card0.classList.remove(card0.getAttribute('data-name'), 'flipped');
            card1.classList.remove(card1.getAttribute('data-name'), 'flipped');
            errors++;
            error_count.innerText = errors;
        }, '800')
        
    }
    pick = [];
}

function checkWin() {
    const flipped = document.querySelectorAll('.flipped');
    if (flipped.length == deck.length) return true;
    return false;
}