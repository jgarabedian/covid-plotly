
function animateIncrement(id, start, end, duration, step) {
    var range = end - start;
    var current = start;
    var increment = end > start ? step : 1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var ele = document.getElementById(id);
    var timer = setInterval(function() {
        current += increment;
        ele.innerHTML = numberWithCommas(current);
        if (current == end || current > end) {
            ele.innerHTML = numberWithCommas(end);
            clearInterval(timer)
        }
    }, stepTime)
}

function numberWithCommas(str) {
    return str.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

window.onload = function() {
    var totalPositiveEle = document.getElementById('total-positive')
    var targetPos = parseInt(totalPositiveEle.innerText);
    animateIncrement('total-positive', 0, targetPos, 500, 1000);

    var totalDeathEle = document.getElementById('total-death');
    var targetDeath = parseInt(totalDeathEle.innerText);
    animateIncrement('total-death', 0, targetDeath, 500, 100);

    var hospCurrentlyEle = document.getElementById('hosp-currently');
    var targetHosp = parseInt(hospCurrentlyEle.innerText);
    animateIncrement('hosp-currently', 0, targetHosp, 500, 50)
}
