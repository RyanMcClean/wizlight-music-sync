window.onload = function () {
    var error_wrapper = document.getElementById('error-wrapper');
    error_wrapper.addEventListener('hidden.bs.modal', function () {
        fetch('/clearError/');
    });
};

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
    response = await fetch(request, {
        method: 'post',
        body: audio_device,
    }).then(function (response) {
        return response.json();
    });

    if (response['result']) {
    } else {
        var errorMessage = JSON.parse(
            document.getElementById('errorMessage').textContent,
        );
        errorMessage = 'Audio sync failed to start, please try again';
        var error_wrapper = new bootstrap.Modal(
            document.getElementById('error-wrapper'),
            {
                keyboard: true,
            },
        );
        error_wrapper.show();
        error_message = document
            .getElementById('error-wrapper')
            .getElementsByTagName('p')[0];
        error_message.textContent = errorMessage;
    }
}
function toggleTheme() {
    var html = document.documentElement;
    html.setAttribute(
        'data-bs-theme',
        html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark',
    );
}
