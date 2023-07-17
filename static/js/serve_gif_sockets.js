
var refreshRate = 5000 // time between fetches in ms

window.addEventListener('load', function() {
    adjustBackgroundImage();

    window.addEventListener('resize', adjustBackgroundImage);
});

function adjustBackgroundImage() {
    var imageDiv = document.getElementById('fullscreen-image');
    var windowWidth = window.innerWidth;
    var windowHeight = window.innerHeight;
    var imageAspect = imageDiv.offsetWidth / imageDiv.offsetHeight;
    var windowAspect = windowWidth / windowHeight;

    if (windowAspect > imageAspect) {
        imageDiv.style.backgroundSize = '100% auto';
        imageDiv.style.backgroundPosition = 'center top';
    } else {
        imageDiv.style.backgroundSize = 'auto 100%';
        imageDiv.style.backgroundPosition = 'center center';
    }
}


function updateBackgroundImage(url) {
    var imageDiv = document.getElementById('fullscreen-image');
    imageDiv.style.backgroundImage = "url('" + url + "')";

    // Wait for 5 seconds before sending the next Socket.IO request
    setTimeout(function() {
        socket.emit('requestNewImage');
    }, refreshRate);
}

// Establish Socket.IO connection
var socket = io();

// Connection established
socket.on('connect', function() {
    console.log('Socket.IO connection established');
    socket.emit('requestNewImage');
});

// Listen for image response
socket.on('imageResponse', function(imageUrl) {
    updateBackgroundImage(imageUrl);
});
