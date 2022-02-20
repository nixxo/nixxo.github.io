function showAlert(message) {
    const messageBox = `
    <div class="alert-box">
        <div class="alert-message">${message}</div>
    </div>
    `;
    const element = document.querySelector('.game-area');
    element.innerHTML += messageBox;
}