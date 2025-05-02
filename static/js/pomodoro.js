let timer;
let timeLeft;
let isRunning = false;

function startTimer() {
    if (isRunning) return;  // Prevent multiple timers from running
    isRunning = true;

    let customMinutes = document.getElementById("custom-time").value;
    timeLeft = customMinutes * 60;  // Convert minutes to seconds

    timer = setInterval(updateTimer, 1000);
}

function updateTimer() {
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;
    document.getElementById("timer-display").innerText =
        `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

    if (timeLeft === 0) {
        clearInterval(timer);
        isRunning = false;
        alert("Time's up!");
    } else {
        timeLeft--;
    }
}
