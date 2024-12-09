window.onload = function () {
    var body = document.getElementsByTagName("body")[ 0 ]
    var errorMessage = document.getElementById("error-wrapper")

    body.addEventListener("click", function () {
        errorMessage.style.visibility = 'hidden';
    }, false);

    errorMessage.addEventListener("click", function (ev) {
        ev.stopPropagation();
    }, false);

}
