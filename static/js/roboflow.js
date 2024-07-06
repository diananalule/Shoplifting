var video = document.createElement('video');
video.addEventListener("loadeddata", predictWebcam);
video.id = 'video';
video.setAttribute('autoplay', '');
video.setAttribute('muted', '');
video.setAttribute('playsinline', '');
video.style.borderRadius = '15px';

const liveView = document.getElementById("cameraView");
let enableWebcamButton;

const hasGetUserMedia = () => !!navigator.mediaDevices?.getUserMedia;

// Keep a reference of all the child elements we create
// so we can remove them easilly on each render.
var children = [];
const stopButton = document.getElementById('camera-stop');

// If webcam supported, add event listener to button for when user
// wants to activate it.
if (hasGetUserMedia()) {
    enableWebcamButton = document.getElementById('cameraButton');
    enableWebcamButton.addEventListener("click", enableCam);
    stopButton.classList.remove("hidden");
} else {
    console.warn("getUserMedia() is not supported by your browser");
}

async function enableCam(event) {
    cameraButton.style.display = 'none';
    console.log("Cam enabled")
    // Hide the button.
    enableWebcamButton.classList.add("removed");

    // Activate the webcam stream.
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch((err) => {
            console.error(err);
        });
}