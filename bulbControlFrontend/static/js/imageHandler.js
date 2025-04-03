/**
 *
 * @author Ryan McClean
 * @contact https://github.com/RyanMcClean
 */

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
