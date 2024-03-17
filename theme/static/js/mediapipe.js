// Copyright 2023 The MediaPipe Authors.

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//      http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import {
    FaceDetector,
    FilesetResolver,
  } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0";
  
  
let faceDetector;
let runningMode = "IMAGE";
var video = document.createElement('video');
video.addEventListener("loadeddata", predictWebcam);
video.setAttribute('autoplay', '');
video.setAttribute('muted', '');
video.setAttribute('playsinline', '');
video.style.borderRadius = '15px';
  
  // Initialize the object detector
const initializefaceDetector = async () => {
const vision = await FilesetResolver.forVisionTasks(
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm"
);
faceDetector = await FaceDetector.createFromOptions(vision, {
    baseOptions: {
    modelAssetPath: `https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite`,
    delegate: "GPU"
    },
    runningMode: runningMode
});
};
initializefaceDetector();
  
//let video = document.getElementById("webcam");
const liveView = document.getElementById("cameraView");
let enableWebcamButton;

// Check if webcam access is supported.
const hasGetUserMedia = () => !!navigator.mediaDevices?.getUserMedia;

// Keep a reference of all the child elements we create
// so we can remove them easilly on each render.
var children = [];

// If webcam supported, add event listener to button for when user
// wants to activate it.
if (hasGetUserMedia()) {
enableWebcamButton =  document.getElementById('cameraButton');
enableWebcamButton.addEventListener("click", enableCam);
} else {
console.warn("getUserMedia() is not supported by your browser");
}

// Enable the live webcam view and start detection.
async function enableCam(event) {
cameraButton.style.display = 'none';
//recorded = document.getElementById('recorded');
//recorded.style.display = 'none';
if (!faceDetector) {
    alert("Face Detector is still loading. Please try again..");
    return;
}

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
async function predictWebcam() {
// if image mode is initialized, create a new classifier with video runningMode
if (runningMode === "IMAGE") {
    runningMode = "VIDEO";
    await faceDetector.setOptions({ runningMode: "VIDEO" });
}
let startTimeMs = performance.now();

// Detect faces using detectForVideo
if (video.currentTime !== lastVideoTime) {
    lastVideoTime = video.currentTime;
    const detections = faceDetector.detectForVideo(video, startTimeMs)
    .detections;
    displayVideoDetections(detections);
}

// Call this function again to keep predicting when the browser is ready
window.requestAnimationFrame(predictWebcam);
}


function displayVideoDetections(detections) {
// Remove any highlighting from previous frame.

for (let child of children) {
    liveView.removeChild(child);
}
children.splice(0);

// Iterate through predictions and draw them to the live view
// liveView.innerHTML = "";
// liveView.classList = "";
for (let detection of detections) {
    const p = document.createElement("p");
    p.innerText =
    "Confidence: " +
    Math.round(parseFloat(detection.categories[0].score) * 100) +
    "% .";
    p.classList.add=('absolute', 'top-2', 'left-2');
    // p.style =
    // "left: " +
    // (video.offsetWidth -
    //     detection.boundingBox.width -
    //     detection.boundingBox.originX) +
    // "px;" +
    // "top: " +
    // (detection.boundingBox.originY - 30) +
    // "px; " +
    // "width: " +
    // (detection.boundingBox.width - 10) +
    // "px;";

    const highlighter = document.createElement("div");
    highlighter.setAttribute("class", "highlighter");
    highlighter.style =
    "left: " +
    (video.offsetWidth -
        detection.boundingBox.width -
        detection.boundingBox.originX) +
    "px;" +
    "top: " +
    detection.boundingBox.originY +
    "px;" +
    "width: " +
    (detection.boundingBox.width - 10) +
    "px;" +
    "height: " +
    detection.boundingBox.height +
    "px;";

    liveView.appendChild(highlighter);
    liveView.appendChild(p);
    video.style.width = '100%'; 
    video.style.height = '100%'; 
    video.style.objectFit = 'cover';
    

    // Store drawn objects in memory so they are queued to delete at next call
    children.push(highlighter);
    children.push(p);
    for (let keypoint of detection.keypoints) {
    const keypointEl = document.createElement("spam");
    keypointEl.className = "key-point";
    keypointEl.style.top = `${keypoint.y * video.offsetHeight - 3}px`;
    keypointEl.style.left = `${
        video.offsetWidth - keypoint.x * video.offsetWidth - 3
    }px`;
    liveView.appendChild(keypointEl);
    liveView.appendChild(video);
    video.play();
    children.push(keypointEl);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Check if the cookie name matches the desired name
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function captureAndSendImage() {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const csrftoken = getCookie('csrftoken');
        const imageDataURL = canvas.toDataURL('image/jpeg');
        fetch('/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken    
            },
            body: JSON.stringify({ image: imageDataURL })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch(error => {
            console.error('Error sending image to backend:');
        });
    }

    if(Math.round(parseFloat(detection.categories[0].score) * 100) > 90){
        captureAndSendImage();
    }
    }

}
