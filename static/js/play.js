class PlayMain {
    constructor(navigator) {
        this.canvas = document.getElementById('userCanvas'),
        this.context = this.canvas.getContext('2d'),
        this.video = document.getElementById('userVideo'),
        this.play_video = document.getElementById('playVideo'),

        this.playCanvas = document.getElementById('playCanvas'),
        this.playContext = this.playCanvas.getContext('2d'),
        this.playVideo = document.getElementById('playVideo');
        this.navigator = navigator,
        this.navigator.getMedia = navigator.mediaDevices.getUserMedia || navigator.mediaDevices.webkitGetUserMedia || navigator.mediaDevices.mozGetuserMedia || navigator.mediaDevices.msGetUserMedia;
        this.rec = null
    }
    main() {

        
        this.video.addEventListener('play', e=> {
            this.draw();
            this.record();
            
        }, false);
        this.play_video.addEventListener('ended', e=>{
            this.rec.stop()
        })
        this.initCaptureVideo(this.video);
        
        window.onresize = this.resizeCanvas();
        this.resizeCanvas();
    }

    initCaptureVideo(video) {
        this.navigator.mediaDevices
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
    }

    draw() {
        // user display 
        this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
        this.context.font = '2.5rem serif';
        this.context.strokeText('USER DISPLAY', 20, 50);

        // play diaplay
        this.playContext.drawImage(this.play_video, 0, 0, this.canvas.width, this.canvas.height);
        this.playContext.font = '2.5rem serif';
        this.playContext.strokeText('PLAY DISPLAY', 20, 50);

        setTimeout(this.draw.bind(this), 1000 / 30); //30 fps
    }

    record(){
      const chunks = [];
      const stream = this.canvas.captureStream(30);
      this.rec = new MediaRecorder(stream);

      this.rec.ondataavailable = e=> chunks.push(e.data);

      this.rec.onstop = e=> this.exportVid(new Blob(chunks, {type:'video/mp4'}));
      this.rec.start();

    }
    exportVid(blob){
      const vid = document.createElement('video');
      vid.src = URL.createObjectURL(blob);
      vid.controls = true;
      document.body.appendChild(vid);
      const a = document.createElement('a');
      let title = this.video.getAttribute('data-title')
      a.download = `${title}_playvideo.mp4`;
      a.href = vid.src;
      a.textContent = 'download the video';
      document.body.appendChild(a);
    }
}

class MessageHandler{
    constructor(URL){
        this.clientID = "client 1"
        this.msg = {
            pid : document.querySelector('#userVideo').getAttribute('data-pid'),
            type : "message",
            text : "hello",
            id : this.clientID,
            date : Date.now()
        }
        this.PLAY_URL = URL + this.msg.pid
        this.socket = new WebSocket(this.PLAY_URL)
        this.init()
    }
    init(){
        this.socket.onopen = e=>{
            this.sendMessage('connected with client : ' + this.msg.pid)    
            this.sendMessage(this.msg)
        }
        this.socket.onmessage = e=>{
            console.log(e.data)
            const data = JSON.parse(e.data)
            console.log(data)
        }
    }
    sendMessage(msg){
        
        this.socket.send(JSON.stringify({
            'message' : msg
        }))  
        
    }
    receivedMessage(){
        switch(this.msg.type){
            case 'message':
                break;
        }
    }
    close(){
        this.socket.close()
    }
    
}

function main(){
    new PlayMain(navigator).main()
    let msg_handler = new MessageHandler('ws://127.0.0.1:8000/ws/play/')
}
main()