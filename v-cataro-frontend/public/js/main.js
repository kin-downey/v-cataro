const FACE = {};

FACE.EXPRESSION = () => {
  const cameraArea = document.getElementById('cameraArea'),
        camera = document.getElementById('camera'),
        canvas = document.getElementById('canvas'),
        test = document.getElementById('test'),
        emoticon = document.getElementById('emoticon'),
        ctx = canvas.getContext('2d'),
        canvasW = 640,
        canvasH = 480,
        intervalTime = 500,
        emoticonTxt = [':)',':|'],
        test_smile = ['test', 'smile'];

  const init = async () => {
    setCanvas();
    setCamera();
    await faceapi.nets.tinyFaceDetector.load("js/weights/");
    await faceapi.nets.faceExpressionNet.load("js/weights/");
  },

  setCanvas = () => {
    canvas.width = canvasW;
    canvas.height = canvasH;
  },

  setCamera = async () => {
    var constraints = {
      audio: false,
      video: {
        width: canvasW,
        height: canvasH,
        facingMode: 'user'
      }
    };
    await navigator.mediaDevices.getUserMedia(constraints)
    .then((stream) => {
      camera.srcObject = stream;
      camera.onloadedmetadata = (e) => {
        playCamera();
      };
    })
    .catch((err) => {
      console.log(err.name + ': ' + err.message);
    });
  },

  playCamera = () => {
    camera.play();
    setInterval(async () => {
      canvas.getContext('2d').clearRect(0, 0, canvasW, canvasH);
      checkFace();
    }, intervalTime);
  },

  checkFace = async () => {
    let faceData = await faceapi.detectAllFaces(
      camera, new faceapi.TinyFaceDetectorOptions()
    ).withFaceExpressions();
    if(faceData.length){
      const setDetection = () => {
        let box = faceData[0].detection.box;
            x = box.x,
            y = box.y,
            w = box.width,
            h = box.height;

        ctx.beginPath();
        ctx.rect(x, y, w, h);
        ctx.strokeStyle = '#76FF03';
        ctx.lineWidth = 2;
        ctx.stroke();
      },

      setExpressions = () => {
        let neutral = faceData[0].expressions.neutral,
            happy = faceData[0].expressions.happy,
            sad = faceData[0].expressions.sad,
            angry = faceData[0].expressions.angry,
            fearful = faceData[0].expressions.fearful,
            disgusted = faceData[0].expressions.disgusted,
            surprised = faceData[0].expressions.surprised;

        test.innerHTML = "<br>" + "happy: " + happy + "</br>"
                       + "<br>" + "sad: " + sad  +"</br>"
                       + "<br>" + "neutral: " + neutral  +"</br>"
                       + "<br>" + "angry: " + angry  +"</br>"
                       + "<br>" + "fearful: " + fearful  +"</br>"
                       + "<br>" + "disgusted: " + disgusted  +"</br>"
                       + "<br>" + "surprised: " + surprised +"</br>"
      };
      setDetection();
      setExpressions();
    }
  };

  init();
};
FACE.EXPRESSION();