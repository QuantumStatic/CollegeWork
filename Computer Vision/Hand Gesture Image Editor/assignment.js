const imgWidth = 640, imgHeight = 480;
const widthCanvas = imgWidth*2, heightCanvas = imgHeight, blurImgStrength=7, unblur_height=96, unblur_width=128;;

let handpose, capture, detections, img, imgCpy, blurImg, freeHand=false, blurringMode=false, firstRun = false, circleMode=false, justBlurred=true;
var circles = [];

function gotResults(results){
    detections = results;
}
function createCopyImg(){
    console.log("Creating copy of original image at setup")
    imgCpy = loadImage("img.jpg");
    console.log("Copy of original image was created at setup")
}
function imgPrep(){
    console.log("Loading Image");
    img = loadImage("img.jpg");
    console.log("Image Loading complete");
}
function createBlurImage(){
    console.log("Creating Blured Image at Setup")
    blurImg = loadImage("img.jpg");
    setTimeout(() => {
        blurImg.filter(BLUR, blurImgStrength);
        console.log("Image was blurred successfully at setup");
    },300);
}
function videoPrep(){
    console.log("Preparing Video");
    capture = createCapture(VIDEO);
    capture.size(imgWidth, imgHeight);
    capture.hide();
    console.log("Video was prepared successfully")
}
function modelReady(){
    console.log('handpose ready');
}
function loadHandPoseModel(){
    handpose = ml5.handpose(capture, modelReady);
    handpose.on("hand", gotResults);
}
function setup() {
    createCanvas(widthCanvas, heightCanvas);
    imgPrep();
    createCopyImg();
    createBlurImage();
    videoPrep();
    loadHandPoseModel();
}

function keyPressed() {
    if (blurringMode === false && keyCode === 86)
        firstRun = true;

    freeHand = false;
    blurringMode = false;
    circleMode = false;
    circles = [];

    // V is pressed
    if (keyCode === 86) {
        console.log("Blurring the image");
        blurringMode = true;
        blurImage();
        console.log(`completed blurring the image with strength ${blurImgStrength}`);
    }

    // F is pressed
    else if (keyCode === 70){
        console.log("Changing to free hand mode");
        freeHand = true;
    }

    // C is pressed
    else if (keyCode === 67) {
        console.log("Changing to circle mode");
        circleMode = true;
    }

    // E is pressed - exit
    else if (keyCode === 69 || keyCode === 82){
        console.log("Resting the image");
        imgPrep();
    }
}

function blurImage(){
    img.filter(BLUR, blurImgStrength);
    image(img, imgWidth, 0, imgWidth, imgHeight);
}

function drawFreeHand(){
    const keyPoint = detections[0].landmarks[8]

    let sqSide = 4, X = 640 - keyPoint[0];
    const colour = img.get(X, keyPoint[1]);
    if (keyPoint[2] < 0)
        keyPoint[2] *= -1;

    const drawColour = color(colour[0]-12, colour[1]-12, colour[2]-12, 6*keyPoint[2]);
    for (let i=0; i < sqSide; i++)
        for (let j=0; j < sqSide; j++)
            img.set(X+i, keyPoint[1]+j, drawColour);

    img.updatePixels()
}

var prevPoint = [0, 640];
function blurUnblurImg(){
    var keyPoint = detections[0].landmarks[8];

    if (!firstRun)
        img.copy(blurImg, imgWidth-prevPoint[0] - 0.5*unblur_width, prevPoint[1]-0.5*unblur_height, unblur_width, unblur_height, imgWidth-prevPoint[0]-0.5*unblur_width, prevPoint[1]-0.5*unblur_height, unblur_width, unblur_height);
    prevPoint = keyPoint;

    img.copy(imgCpy, imgWidth-keyPoint[0] - 0.5*unblur_width, keyPoint[1]-0.5*unblur_height, unblur_width, unblur_height, imgWidth-keyPoint[0]-0.5*unblur_width, keyPoint[1]-0.5*unblur_height, unblur_width, unblur_height);
    image(img, imgWidth, 0, imgWidth, imgHeight);
    firstRun = false;
    justBlurred = false;
}
function blurAfterHandLeaveFrame(){
    img.copy(blurImg, imgWidth-prevPoint[0] - 0.5*unblur_width, prevPoint[1]-0.5*unblur_height, unblur_width, unblur_height, imgWidth-prevPoint[0]-0.5*unblur_width, prevPoint[1]-0.5*unblur_height, unblur_width, unblur_height);
    justBlurred = true;
}

function distBet(landmark1, landmark2){
    return Math.pow(Math.pow(landmark1[0] - landmark2[0], 2) + Math.pow(landmark1[1] - landmark2[1], 2), 0.5)
}
function createCircles(){
    const indexFinger = detections[0].landmarks[8], thumb = detections[0].landmarks[4];

    let distance = distBet(indexFinger, thumb);

    const circleCenterColour = imgCpy.get(640 - indexFinger[0], indexFinger[1]);
    if (indexFinger[2] < 0)
        indexFinger[2] = -1*indexFinger[2]

    circles.push([[indexFinger[0]-imgWidth, indexFinger[1], 0.6*distance], color(circleCenterColour[0], circleCenterColour[1], circleCenterColour[2], indexFinger[2]*4)])
}
function drawCircles(){
    circles.forEach(element => {
        const colorVals = element[1].levels;
        stroke(`rgba(${colorVals[0]-8}, ${colorVals[1]-8}, ${colorVals[2]-8}, ${colorVals[3]+3})`);
        strokeWeight(1.5);
        fill(element[1]);
        circle(element[0][0], element[0][1], element[0][2]);
    });
}

function draw() {
    image(img, imgWidth, 0, imgWidth, imgHeight);

    translate(capture.width, 0);
    scale(-1, 1);
    image(capture, 0, 0, imgWidth, imgHeight);

    if (detections && detections.length > 0) {
        drawKeypoint();

        if (freeHand)
            drawFreeHand();

        if (blurringMode)
            blurUnblurImg();

        if (circleMode)
            setTimeout(() => {
                createCircles();
            }, 100);
    }
    else if (blurringMode && !justBlurred)
        blurAfterHandLeaveFrame();

    if (circleMode)
        drawCircles();
}

function drawKeypoint(){
    noStroke();
    fill(255, 0, 0);

    const keyPoint = detections[0].landmarks[8]
    const thumb = detections[0].landmarks[4];

    ellipse(keyPoint[0], keyPoint[1], 10, 10);
    ellipse(keyPoint[0]-imgWidth, keyPoint[1], 10, 10);

    if (circleMode)
        ellipse(thumb[0], thumb[1], 10, 10);
}
