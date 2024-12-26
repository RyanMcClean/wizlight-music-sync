/**
 *
 * @author Ryan McClean
 * @contact https://github.com/RyanMcClean
 */

white = 'rgb(0, 0, 0)';
orange = 'rgb(255, 165, 0)';
grey = 'rgb(200, 200, 200)';

async function clickColor(element, hexCode, seltop, selleft) {
    var node = element;
    while (!node.classList.contains('bulb-container')) {
        var node = node.parentElement;
    }

    var bulb_element = node.getElementsByClassName('fa-solid')[0];
    var ip = bulb_element.getAttribute('value');

    var r, g, b;
    r = parseInt(hexCode.substring(1, 3), 16);
    g = parseInt(hexCode.substring(3, 5), 16);
    b = parseInt(hexCode.substring(5), 16);
    console.log(hexCode);
    response = await fetch('/colorBulb/', {
        method: 'post',
        body: JSON.stringify({ ip: ip, r: r, g: g, b: b }),
    })
        .catch(function (error) {
            console.log(error);
        })
        .then(function (response) {
            return response.text();
        });

    if (seltop + 200 > -1 && selleft > -1) {
        document.getElementById('selectedhexagon').style.top =
            seltop - 5 + 'px';
        document.getElementById('selectedhexagon').style.left = selleft + 'px';
    } else if (response['state']) {
        if (response.hasOwnProperty('temp')) {
            console.log('added orange');
            bulb_element.style.color = orange;
        } else if (response.hasOwnProperty('r')) {
            bulb_element.style.color =
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
        bulb_element.style.color = grey;
        console.log('removed color');
        document.getElementById('selectedhexagon').style.visibility = 'hidden';
    }
}

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
    for (var x = 0; x < bulbButtons.length; x++) {
        console.log('Bulb name: ' + bulbButtons[x].getAttribute('name'));
        console.log('Bulb Ip: ' + bulbButtons[x].getAttribute('value'));
        response = await fetch('/queryBulb/', {
            method: 'post',
            body: JSON.stringify({ ip: bulbButtons[x].getAttribute('value') }),
        }).then(function (response) {
            return response.json();
        });
        if (response['state']) {
            if (response.hasOwnProperty('temp')) {
                console.log('added orange');
                bulbButtons[x].style.color = orange;
            } else if (response.hasOwnProperty('r')) {
                r = response['r'];
                g = response['g'];
                b = response['b'];
                hexRed = Number(r).toString(16).toUpperCase();
                hexGreen = Number(g).toString(16).toUpperCase();
                hexBlue = Number(b).toString(16).toUpperCase();
                console.log(hexRed.length);
                hexRed = hexRed.length < 2 ? '0' + hexRed : hexRed;
                hexGreen = hexGreen.length < 2 ? '0' + hexGreen : hexGreen;
                hexBlue = hexBlue.length < 2 ? '0' + hexBlue : hexBlue;
                hexcode = `#${hexRed}${hexGreen}${hexBlue}`;
                try {
                    // document
                    //     .querySelector('area[alt="' + hexcode + '"]')
                    //     .click();
                } catch (error) {}
                bulbButtons[x].style.color =
                    'rgb(' + r + ', ' + g + ', ' + b + ')';
                console.log('added color');
            }
        } else if ('state' in response && !response['state']) {
            bulbButtons[x].style.color = grey;
            document.getElementById('selectedhexagon').style.visibility =
                'hidden';
            console.log('removed color');
        }
    }
}
