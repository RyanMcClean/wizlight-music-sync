white = 'rgb(0, 0, 0)'
orange = 'rgb(255, 165, 0)'
grey = 'rgb(200, 200, 200)'

async function updateImage() {
    element = document.getElementsByName(this.getAttribute('name'))[ 0 ]
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
        element.style.color = orange
        console.log('added color')
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
                bulbButtons[ x ].style.color = 'rgb(' + response[ 'r' ] + ', ' + response[ 'g' ] + ', ' + response[ 'b' ] + ')'
                console.log('added color')
            }
        } else {
            bulbButtons[ x ].style.color = grey
            console.log('removed color')
        }
    }
}
