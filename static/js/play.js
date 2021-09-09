class PlayMain {

    constructor(navigator) {
        this.canvas = document.getElementById('userCanvas'),
        this.context = this.canvas.getContext('2d'),
        this.video = document.getElementById('userVideo'),

        this.playCanvas = document.getElementById('playCanvas'),
        this.playContext = this.playCanvas.getContext('2d'),
        this.playVideo = document.getElementById('playVideo');
        this.navigator = navigator,
        this.navigator.getMedia = navigator.mediaDevices.getUserMedia || navigator.mediaDevices.webkitGetUserMedia || navigator.mediaDevices.mozGetuserMedia || navigator.mediaDevices.msGetUserMedia;
        
    }
    main() {

        this.initVideo(this.video);

        this.video
            .addEventListener('play', e=> {
                this.draw();
                this.record();
            }, false);

        window.onresize = this.resizeCanvas();
        this.resizeCanvas();
    }

    initVideo(video) {
        this
            .navigator
            .mediaDevices
            .getUserMedia({audio: false, video: true})
            .then(gotStream)
            .catch(error => console.error(error));

        function gotStream(stream) {
            // video.src = window.URL.createObjectURL(stream);
            video.srcObject = stream;
            video.play();
        }
    }

    resizeCanvas() {
        let width = parseInt(window.innerWidth * 0.5);
        let height = parseInt(window.innerHeight * 0.8);

        this.canvas.width = width;
        this.canvas.height = height;

        this.playCanvas.width = width;
        this.playCanvas.height = height;
        console.log(width);
        console.log(height);
    }

    draw() {
        // user display 
        this
            .context
            .drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
        this.context.font = '2.5rem serif';
        this
            .context
            .strokeText('USER DISPLAY', 20, 50);

        // play diaplay
        // var stream = this.video.captureStream(30);
        // let stream = this.canvas.captureStream();
        // this.playVideo.srcObject = stream;
        this
            .playContext
            .drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
        this.playContext.font = '2.5rem serif';
        this
            .playContext
            .strokeText('PLAY DISPLAY', 20, 50);

        setTimeout(this.draw.bind(this), 1000 / 30); //30 fps
    }

    record(){
      const chunks = [];
      const stream = this.canvas.captureStream(30);
      const rec = new MediaRecorder(stream);

      rec.ondataavailable = e=> chunks.push(e.data);

      rec.onstop = e=> this.exportVid(new Blob(chunks, {type:'video/mp4'}));
      rec.start();
      setTimeout(()=>rec.stop(), 5000) ; // 5초 기록 stop 시점은 나중에 수정 

    }
    exportVid(blob){
      const vid = document.createElement('video');
      vid.src = URL.createObjectURL(blob);
      vid.controls = true;
      document.body.appendChild(vid);
      const a = document.createElement('a');
      a.download = 'myvid.mp4';
      a.href = vid.src;
      a.textContent = 'download the video';
      document.body.appendChild(a);
    }
}

new PlayMain(navigator).main()