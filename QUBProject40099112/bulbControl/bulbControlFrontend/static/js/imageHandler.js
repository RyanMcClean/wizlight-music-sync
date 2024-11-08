function updateImage() {
    var element = document.getElementsByName(this.getAttribute('name'))[ 0 ]
    ip = this.getAttribute('value')
    fetch('/toggleBulb/', {
        method: 'post',
        body: JSON.stringify({ 'ip': ip })
    })
        .then(function (response) {
            return response.json()
        })
        .then(function (json) {
            console.log(json[ 'state' ])
            if (json[ 'state' ]) {
                element.classList.remove('image-color')
                console.log('added color')
            } else {
                element.classList.add('image-color')
                console.log('removed color')
            }

        })
    console.log(ip);
}

async function backgroundUpdate() {
    bulbButtons = document.getElementsByClassName('fa-lightbulb')
    console.log(bulbButtons)
    for (var x = 0; x < bulbButtons.length; x++) {
        console.log(bulbButtons[ x ].getAttribute('name'))
        response = await fetch('/queryBulb/', {
            method: 'post',
            body: JSON.stringify({ 'ip': bulbButtons[ x ].getAttribute('value') })
        })
            .then(function (response) {
                return response.json()
            })
        if (response[ 'state' ]) {
            bulbButtons[ x ].classList.remove('image-color')
            console.log('added color')
        } else {
            bulbButtons[ x ].classList.add('image-color')
            console.log('removed color')
        }
    }
}
