async function startAudioSync(element) {
    var audio_device = document.getElementById('audio_device_selector').value;
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
