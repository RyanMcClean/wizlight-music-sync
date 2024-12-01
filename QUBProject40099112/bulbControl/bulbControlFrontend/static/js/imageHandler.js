white = 'rgb(0, 0, 0)'
orange = 'rgb(255, 165, 0)'
grey = 'rgb(200, 200, 200)'

async function clickColor(hexCode, seltop, selleft) {
    element = document.getElementsByClassName('fa-lightbulb')[ 0 ]
    ip = '192.168.50.128'
    var r, g, b
    r = parseInt(hexCode.substring(1, 3), 16)
    g = parseInt(hexCode.substring(3, 5), 16)
    b = parseInt(hexCode.substring(5), 16)
    console.log(hexCode)
    console.log("#" + r + g + b)
    response = await fetch('/colorBulb/', {
        method: 'post',
        body: JSON.stringify({ 'ip': ip, 'r': r, 'g': g, 'b': b })
    })
        .then(function (response) {
            return response.json()
        })
    console.log(response)
    if ((seltop + 200) > -1 && selleft > -1) {
        document.getElementById("selectedhexagon").style.top = seltop - 5 + "px";
        document.getElementById("selectedhexagon").style.left = selleft + "px";
        document.getElementById("selectedhexagon").style.visibility = "visible";
    } else {
        document.getElementById("selectedhexagon").style.visibility = "hidden";
    }
    if (response[ 'state' ]) {
        if (response.hasOwnProperty('temp')) {
            console.log('added orange')
            element.style.color = orange
        } else if (response.hasOwnProperty('r')) {
            element.style.color = 'rgb(' + response[ 'r' ] + ', ' + response[ 'g' ] + ', ' + response[ 'b' ] + ')'
            console.log('added color')
        }
    } else {
        element.style.color = grey
        console.log('removed color')
    }
}

async function updateImage() {
    element = document.getElementsByClassName(this.getAttribute('class'))[ 0 ]
    console.log(element)
    ip = this.getAttribute('value')
    response = await fetch('/toggleBulb/', {
        method: 'post',
        body: JSON.stringify({ 'ip': element.getAttribute('value') })
    })
        .then(function (response) {
            return response.json()
        })
    console.log(response)
    if (response[ 'state' ]) {
        if (response.hasOwnProperty('temp')) {
            console.log('added orange')
            element.style.color = orange
        } else if (response.hasOwnProperty('r')) {
            element.style.color = 'rgb(' + response[ 'r' ] + ', ' + response[ 'g' ] + ', ' + response[ 'b' ] + ')'
            console.log('added color')
        }
    } else {
        element.style.color = grey
        console.log('removed color')
    }
}

async function backgroundUpdate() {
    bulbButtons = document.getElementsByClassName('fa-lightbulb')
    for (var x = 0; x < bulbButtons.length; x++) {
        console.log("Bulb name: " + bulbButtons[ x ].getAttribute('name'))
        response = await fetch('/queryBulb/', {
            method: 'post',
            body: JSON.stringify({ 'ip': bulbButtons[ x ].getAttribute('value') })
        })
            .then(function (response) {
                return response.json()
            })
        console.log(response)
        if (response[ 'state' ]) {
            if (response.hasOwnProperty('temp')) {
                console.log('added orange')
                bulbButtons[ x ].style.color = orange
            } else if (response.hasOwnProperty('r')) {
                r = response[ 'r' ]
                g = response[ 'g' ]
                b = response[ 'b' ]
                hexRed = Number(r).toString(16).toUpperCase()
                hexGreen = Number(g).toString(16).toUpperCase()
                hexBlue = Number(b).toString(16).toUpperCase()
                console.log(hexRed.length)
                hexRed = hexRed.length < 2 ? "0" + hexRed : hexRed
                hexGreen = hexGreen.length < 2 ? "0" + hexGreen : hexGreen
                hexBlue = hexBlue.length < 2 ? "0" + hexBlue : hexBlue
                hexcode = `#${hexRed}${hexGreen}${hexBlue}`
                document.querySelector('area[alt="' + hexcode + '"]').click()
                bulbButtons[ x ].style.color = 'rgb(' + r + ', ' + g + ', ' + b + ')'
                console.log('added color')
            }
        } else {
            bulbButtons[ x ].style.color = grey
            document.getElementById("selectedhexagon").style.visibility = 'hidden';
            console.log('removed color')
        }
    }
}
