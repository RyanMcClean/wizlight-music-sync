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