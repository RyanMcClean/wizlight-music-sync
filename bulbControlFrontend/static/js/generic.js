/**
 *
 * @author Ryan McClean
 * @contact https://github.com/RyanMcClean
 */

// Obtains csrf token for js fetch requests
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Clears error when it is shown
function clear_message() {
    var error_element = document.getElementById('error-toast');
    var success_element = document.getElementById('success-toast');
    if (typeof error_element != 'undefined' && error_element != null) {
        console.log('Clearing Error');
        fetch('/clearError/');
    }
    if (typeof success_element != 'undefined' && success_element != null) {
        console.log('Clearing Success');
        fetch('/clearSuccess/');
    }
}

// Launches audio sync
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
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
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
// Toggles light and dark themes
function toggleTheme() {
    var html = document.documentElement;
    html.setAttribute(
        'data-bs-theme',
        html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark',
    );
}

white = 'rgb(0, 0, 0)';
orange = 'rgb(255, 165, 0)';
grey = 'rgb(200, 200, 200)';

async function updateImage() {
    // element = document.getElementsByClassName(this.getAttribute('class'))[0];
    // console.log(element);
    ip = this.getAttribute('value');
    console.log(ip);
    response = await fetch('/toggleBulb/', {
        method: 'POST',
        body: JSON.stringify({ ip: ip }),
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    }).then(function (response) {
        return response.json();
    });
    console.log(response);
    if (response['state']) {
        if (response.hasOwnProperty('temp')) {
            console.log('added orange');
            this.style.color = orange;
        } else if (response.hasOwnProperty('r')) {
            this.style.color =
                'rgb(' +
                response['r'] +
                ', ' +
                response['g'] +
                ', ' +
                response['b'] +
                ')';
            console.log('added color');
        }
    } else {
        this.style.color = grey;
        console.log('removed color');
    }
}

async function backgroundUpdate() {
    bulbButtons = document.getElementsByClassName('fa-lightbulb');
    for (let x = 0; x < bulbButtons.length; x++) {
        console.log('Bulb name: ' + bulbButtons[x].getAttribute('name'));
        console.log('Bulb Ip: ' + bulbButtons[x].getAttribute('value'));
        response = await fetch('/queryBulb/', {
            method: 'post',
            body: JSON.stringify({ ip: bulbButtons[x].getAttribute('value') }),
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        }).then(function (response) {
            return response.json();
        });

        if (typeof response !== 'undefined') {
            var ip = response['ip'];
            response = response['result'];
            if (response.hasOwnProperty('temp') && response['state']) {
                console.log('added orange');
                document.querySelector(`[value="${ip}"]`).style.color = orange;
            } else if (response.hasOwnProperty('r') && response['state']) {
                r = response['r'];
                g = response['g'];
                b = response['b'];
                document.querySelector(`[value="${ip}"]`).style.color =
                    'rgb(' + r + ', ' + g + ', ' + b + ')';
                console.log('added color');
            }
        } else if ('state' in response && !response['state']) {
            document.querySelector(`[value="${ip}"]`).style.color = grey;

            console.log('removed color');
        }
    }
}
