function updateCountdown(date, countdown_id) {
    var countdown = document.getElementById(countdown_id);

    var now = new Date().getTime();
    var distance = date - now;
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    countdown.innerHTML = "Finishes in: " + days.toString().padStart(2, '0') + ":"
        + hours.toString().padStart(2, '0') + ":" + minutes.toString().padStart(2, '0') + ":"
        + seconds.toString().padStart(2, '0');
    if (distance > 0)
        setTimeout(updateCountdown, 1000, date, countdown_id);
    else {
        countdown.innerHTML = "Finished";
        countdown.classList.add('text-danger');
    }
}
            