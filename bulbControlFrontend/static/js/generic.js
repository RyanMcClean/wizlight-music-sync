async function audioSync(element) {
    var audio_device = document.getElementById('audio_device_selector').value;
    var button = document.getElementById('activate-music-sync-button');
    var request;
    if (button.classList.contains('btn-outline-danger')) {
        button.classList.add('btn-danger');
        button.classList.remove('btn-outline-danger');
        request = '/activateSync/';
    } else {
        button.classList.remove('btn-danger');
        button.classList.add('btn-outline-danger');
        request = '/stopSync/';
    }
    response = await fetch('/activateSync/', {
        method: 'post',
        body: audio_device,
    }).then(function (response) {
        return response.json();
    });

    if (response['result']) {
        element.offsetParent.style.visibility = 'hidden';
    } else {
        var errorMessage = JSON.parse(
            document.getElementById('errorMessage').textContent,
        );
        errorMessage = 'Audio sync failed to start, please try again';
        error_wrapper = document.getElementById('error-wrapper');
        error_wrapper.style.visibility = 'visible';
        error_message = error_wrapper.getElementsByTagName('span')[0];
        error_message.textContent = errorMessage;
    }
}
