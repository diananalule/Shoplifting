let runningMode = "IMAGE";
var video = document.createElement('video');
video.addEventListener("loadeddata", predictWebcam);
video.id = 'video';
video.setAttribute('autoplay', '');
video.setAttribute('muted', '');
video.setAttribute('playsinline', '');
video.style.borderRadius = '15px';

//let video = document.getElementById("webcam");
const liveView = document.getElementById("cameraView");
let enableWebcamButton;

const canvasOverlay = document.createElement('canvas');
canvasOverlay.style.position = 'absolute';
canvasOverlay.style.top = '0';
canvasOverlay.style.left = '0';
canvasOverlay.style.borderRadius = '15px';
liveView.appendChild(canvasOverlay);

// Check if webcam access is supported.
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

// Enable the live webcam view and start detection.
async function enableCam(event) {
    cameraButton.style.display = 'none';
    //recorded = document.getElementById('recorded');
    //recorded.style.display = 'none';

    // Hide the button.
    enableWebcamButton.classList.add("removed");

    // getUsermedia parameters
    const constraints = {
        video: true
    };

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


let lastVideoTime = -1;

async function detectShoplifting(imageBase64) {
    const response = await fetch("https://detect.roboflow.com/shoplifting-yefyu/1?api_key=pJthaltwzZ3xtYeQ7V9w", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: imageBase64
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
}




async function predictWebcam() {
    if (video.currentTime !== lastVideoTime) {
        lastVideoTime = video.currentTime;

        // Capture the current frame from the video
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageBase64 = canvas.toDataURL("image/jpeg").split(",")[1]; // Remove the data URL prefix

        try {
            const detectionData = await detectShoplifting(imageBase64);
            console.log(detectionData);
            displayVideoDetections(detectionData['predictions']);
        } catch (error) {
            console.log(error.message);
        }
    }

    // Call this function again to keep predicting when the browser is ready
    window.requestAnimationFrame(predictWebcam);
}

// function displayVideoDetections(detection) {
//     const ctx = canvasOverlay.getContext('2d');
//     ctx.clearRect(0, 0, canvasOverlay.width, canvasOverlay.height);
//     const confidence = detection[0]['confidence']
//     const x = detection[0]['x']
//     const y = detection[0]['y']
//     const width = detection[0]['width']
//     const height = detection[0]['height']

//     canvasOverlay.width = video.videoWidth;
//     canvasOverlay.height = video.videoHeight;

//     video.style.width = '100%';
//     video.style.height = '100%';
//     video.style.objectFit = 'cover';
//     liveView.appendChild(video);
//     drawBoundingBox(x, y, width, height, confidence);
//     video.play();
// }

// function drawBoundingBox(x, y, width, height, confidence) {
//     const ctx = canvasOverlay.getContext('2d');
//     ctx.strokeStyle = 'red';
//     ctx.lineWidth = 2;
//     console.log(x, y, width, height, confidence);
//     ctx.strokeRect(
//         x * canvasOverlay.width,
//         y * canvasOverlay.height,
//         width * canvasOverlay.width,
//         height * canvasOverlay.height
//     );
// }

function displayVideoDetections(detections) {

    for (let child of children) {
        liveView.removeChild(child);
    }
    children.splice(0);

    for (let detection of detections) {
        const p = document.getElementById('model_predictions');
        p.innerText =
        "Prediction: " + (detection['class_id'] != 0 ? 'Shoplifting' : 'No Shoplifting') + '\n' +
        "Confidence: " + Math.round(parseFloat(detection['confidence']) * 100) + "%.";
        // p.classList.add = ('absolute', 'text-white', 'text-lg', 'font-bold', 'bg-gray-800', 'p-2', 'rounded', 'border', 'border-gray-900', 'shadow-lg', 'top-0', 'left-0', 'm-2', 'z-10');

        const highlighter = document.createElement("div");
        highlighter.setAttribute("class", "highlighter");
        highlighter.style =
            "left: " +
            (video.offsetWidth -
                detection['width'] -
                detection['x']) +
            "px;" +
            "top: " +
            detection['y'] +
            "px;" +
            "width: " +
            (detection['weight'] - 10) +
            "px;" +
            "height: " +
            detection['height'] +
            "px;";

        //liveView.appendChild(highlighter);
        //liveView.appendChild(p);
        video.style.width = '100%';
        video.style.height = '100%';
        video.style.objectFit = 'cover';


        children.push(highlighter);
        liveView.appendChild(video);
        video.play();
        

        // function getCookie(name) {
        //     let cookieValue = null;
        //     if (document.cookie && document.cookie !== '') {
        //         const cookies = document.cookie.split(';');
        //         for (let i = 0; i < cookies.length; i++) {
        //             const cookie = cookies[i].trim();
        //             // Check if the cookie name matches the desired name
        //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
        //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        //                 break;
        //             }
        //         }
        //     }
        //     return cookieValue;
        // }

        // async function captureAndSendImage() {
        //     const canvas = document.createElement('canvas');
        //     const context = canvas.getContext('2d');
        //     canvas.width = video.videoWidth;
        //     canvas.height = video.videoHeight;
        //     context.drawImage(video, 0, 0, canvas.width, canvas.height);
        //     const csrftoken = getCookie('csrftoken');
        //     const imageDataURL = canvas.toDataURL('image/jpeg');
        //     const message = document.getElementById('message');
        //     const status = document.querySelector('.statusDiv');
        //     var is_allowed_to_send = true;
        //     if (is_allowed_to_send) {
        //         await fetch('/verify', {
        //             method: 'POST',
        //             headers: {
        //                 'Content-Type': 'application/json',
        //                 'X-CSRFToken': csrftoken
        //             },
        //             body: JSON.stringify({ image: imageDataURL })
        //         })
        //             .then(is_allowed_to_send = false)
        //             .then(response => response.json())
        //             .then(data => {
        //                 console.log(data);
        //                 if (data['status'] === 'success') {
        //                     is_allowed_to_send = false;
        //                     status.classList.remove('hidden')
        //                     message.textContent = data['message'];

        //                 }
        //                 else {
        //                     status.classList.remove('hidden')
        //                     message.textContent = data['message'];
        //                     is_allowed_to_send = true;
        //                 }

        //                 setTimeout(() => {
        //                     status.classList.add('hidden');
        //                 }, 5000);
                        
        //                 return data
        //             })
        //             .catch(error => {
        //                 console.error('Error sending image to backend:');
        //             });
        //     }
        // }

        // if (Math.round(parseFloat(detection.categories[0].score) * 100) > 90) {
        //     captureAndSendImage();
        // }
    }

}

