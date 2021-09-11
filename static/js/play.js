class PlayMain {
    constructor(navigator, msg_handler, pid) {
        this.canvas = document.getElementById('userCanvas'),
        this.context = this.canvas.getContext('2d'),
        this.video = document.getElementById('userVideo'),
        this.play_video = document.getElementById('playVideo'),
        this.playCanvas = document.getElementById('playCanvas'),
        this.playContext = this.playCanvas.getContext('2d'),
        this.navigator = navigator
        this.navigator.getMedia = navigator.mediaDevices.getUserMedia || navigator.mediaDevices.webkitGetUserMedia || navigator.mediaDevices.mozGetuserMedia || navigator.mediaDevices.msGetUserMedia;
        this.rec = null
        
        this.score = 0
       
        this.msg_handler = msg_handler
        this.config = {
            pid: pid,
            id: this.msg_handler.clientID,
            start_date: Date.now()
        }
    }
    init_handler(){
        this.msg_handler.setReceiveCallBack(data=>{
            switch (data.type) {
                case 'message':
                    break;
                case 'update_score':
                    this.updateScore(data.score)
                    break
            }
        })
    }
    main() {
        this.init_handler()
        this.video.addEventListener('play', e => {
            this.draw();
            this.record();
        }, false);
        this.play_video.addEventListener('ended', e => {
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
        console.log('resizing')
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

        this.context.font = '0.5 rem serif';
        this.context.strokeText('Score', 20, this.canvas.height - 100);

        this.context.font = '1 rem serif';
        this.context.strokeText(this.score, 20, this.canvas.height - 50);

        // play diaplay
        this.playContext.drawImage(this.play_video, 0, 0, this.canvas.width, this.canvas.height);
        this.playContext.font = '2.5rem serif';
        this.playContext.strokeText('PLAY DISPLAY', 20, 50);

        setTimeout(this.draw.bind(this), 1000 / 30); //30 fps
    }
    updateScore(score) {
        this.score += score
        console.log(this.score)
        this.context.font = '1 rem serif';
        this.context.strokeText(this.score, 20, this.canvas.height - 50);
    }

    record() {
        const chunks = [];
        const stream = this.canvas.captureStream(30);
        this.rec = new MediaRecorder(stream);

        this.rec.ondataavailable = e => chunks.push(e.data);

        this.rec.onstop = e => {
            this.msg_handler.close(this.config.pid)
            let title = this.video.getAttribute('data-title')
            let video_title = `${title}_playvideo.mp4`
            const vid = this.exportVid(new Blob(chunks, {type: 'video/mp4'}), video_title)
            const play_data = new FormData()
            const file = new File(chunks, video_title, {'type':'video/mp4'})
            play_data.append('video', file, file.name)
            play_data.append('datetime', new Date(Date.now()).toString())
            this.msg_handler.sendResult('http://127.0.0.1:8000/play/?pid=' + this.config.pid, play_data)
        };
        this.rec.start();

    }
    exportVid(blob, title) {
        const vid = document.createElement('video');
        vid.src = URL.createObjectURL(blob);
        vid.controls = true;
        document.body.appendChild(vid);
        const a = document.createElement('a');
        a.download = title;
        a.href = vid.src;
        a.textContent = 'download the video';
        document.body.appendChild(a);
        return vid
    }
}

class MessageHandler {
    constructor(URL, pid=null) {
        this.clientID = "client 1"
        this.URL = URL
        this.socket = new WebSocket(this.URL)
        this.receivedCallBack = null
        this.init()
    }
    init() {
        this.socket.onopen = e => {
            this.sendMessage('check', 'connected with client : ' + this.msg.pid)
            this.sendMessage('check', this.msg)
        }
        this.socket.onmessage = e => {
            const data = JSON.parse(e.data)
            this.receivedCallBack(data)
        }
        this.socket.onclose = e=>{
            this.socket.close()
            console.log('disconnected')
        }
    }
    sendMessage(type, msg) {
        this.socket.send(JSON.stringify({
            'type' : type,
            'message': msg
        }))
    }
    setReceiveCallBack(callback){
        this.receivedCallBack = callback
    }
    close(pid=null) {
        this.socket.send(JSON.stringify({
            'type' : 'close',
            'pid' : pid,
            'message': 'close',
        }))
        this.socket.close()
    }
    makeMessage(func) {
        func()
    }
    async sendResult(URL, datas) {
        const request = new Request(URL + '', {
            headers: {
                'X-CSRFToken': this.getCookie("csrftoken")
            }
        })
        let res = await fetch(request, {
            method: 'POST',
            mode: 'same-origin',
            body: datas
        })
        return res
    }

    getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

function main() {
    const pid = document.querySelector('#userVideo').getAttribute('data-pid')
    let msg_handler = new MessageHandler('ws://127.0.0.1:8000/ws/play/' + pid)
    new PlayMain(navigator, msg_handler, pid).main()
}
main()