class GameMain{

    constructor(manager, display){
        this.display = display
        this.manager = manager
    }
    main(){

    }
    init(){

    }

    ready(){

    }

    start(){

    }
    play(){


    }
    end(){

    }


}

class PlayManager {
    constructor(navigator, msg_handler, pid) {
        this.color_frame = document.getElementById('user-canvas-frame')
        this.canvas = document.getElementById('userCanvas'),
        this.context = this.canvas.getContext('2d'),
        this.video = document.getElementById('userVideo'),
        this.play_video = document.getElementById('playVideo'),
        this.playCanvas = document.getElementById('playCanvas')
        // this.playContext = this.playCanvas.getContext('2d'),
        if(this.video.getAttribute('data-play-mode') === 'realtime'){
            this.navigator = navigator
            this.navigator.getMedia = navigator.mediaDevices.getUserMedia || navigator.mediaDevices.webkitGetUserMedia || navigator.mediaDevices.mozGetuserMedia || navigator.mediaDevices.msGetUserMedia;
        }
        this.rec = null
        this.fps = 30
        this.loopID = null
        this.score = 0
       
        this.msg_handler = msg_handler
        this.config = {
            pid: pid,
            id: this.msg_handler.clientID,
            start_date: new Date(Date.now()).toString()
        }
        this.URL = this.msg_handler.URL
        this.start_flag = false 
    }
    main(){
        this.init()
    }
    load(){

    }
    init() {
        window.onresize = this.resizeCanvas.bind(this);
        this.resizeCanvas.bind(this)()

        this.video.addEventListener('play', e => {
            console.log('play')
            if(this.start_flag){
                return
            }else{
                this.start_flag = true
            }
            this.play_video.pause()
            
            if(this.video.getAttribute('data-play-mode') === 'realtime'){
                this.draw_intro(3)
            }else if(this.video.getAttribute('data-play-mode') === 'upload'){
                console.log('upload')
                this.video.pause()
                this.draw_intro(3)
            }else{
                console.log('error')
            }
            // this.draw_play()
        }, false);

        // this.play_video.addEventListener('play', e=>{

        // })
      
        if(this.video.getAttribute('data-play-mode') === 'realtime'){
            this.initCaptureVideo(this.video);
        }else if(this.video.getAttribute('data-play-mode') === 'upload'){
            // this.video.play()
            // this.play_video.play()
        }
    }

    init_handler(){
        this.msg_handler.setReceiveCallBack(data=>{
            console.log(data)
            switch (data.type) {
                case 'message':
                    break;
                case 'update_score':
                    this.updateScore(data.score)
                    break
            }
        })
        console.log(this.msg_handler.receivedCallBack)
    }

    initCaptureVideo(video) {
        this.navigator.mediaDevices
            .getUserMedia({audio: false, video: true})
            .then(gotStream)
            .catch(error => console.error(error));

        function gotStream(stream) {
            // video.src = window.URL.createObjectURL(stream);
            console.log(stream.getTracks())
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

        // this.playCanvas.width = width;
        // this.playCanvas.height = height;
    }
    draw_intro(count=3){
        count += 1

        this.context.strokeStyle= '#a65bf8'
        this.context.lineWidth = 6
        this.context.fillStyle = 'white'

        // this.context.globalAlpha = 0.2;
        // this.context.font = 'white'
        // this.context.fillRect(0, 0, this.canvas.width, this.canvas.height)

        function intro(count){
            console.log(count)

            this.context.clearRect(this.canvas.width/4+100,this.canvas.height/3-50, this.canvas.width/2-150, this.canvas.height/2-50);

            
            // this.context.globalAlpha = 0.2;
            // this.context.fillRect(this.canvas.width/4+100, this.canvas.height/3-50, this.canvas.width/2-150, this.canvas.height/2-50)

            this.context.font = `${0.0055*this.canvas.width}rem Brush Script MT`;
            this.context.strokeText(`Ready...`, this.canvas.width/2-50, this.canvas.height/2-80);
            this.context.fillText(`Ready...`, this.canvas.width/2-50, this.canvas.height/2-80);
    
            if (count > 0){
                this.context.strokeText(`${count}`, this.canvas.width/2-30, this.canvas.height/2-20);
                this.context.fillText(`${count}`, this.canvas.width/2-30, this.canvas.height/2-20);
            }
            else{
                this.context.strokeText(`Start !`, this.canvas.width/2-50, this.canvas.height/2-20);
                this.context.fillText(`Start !`, this.canvas.width/2-50, this.canvas.height/2-20);
            }
                            


            if (count < 0) {
                this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.play_video.play()
                if(this.video.getAttribute('data-play-mode')  === 'upload'){
                    this.video.play()
                }
                this.init_handler()
                this.loopID = window.requestAnimationFrame(this.draw_play.bind(this))
                this.record()
            }
            else{
                setTimeout(intro.bind(this), 1000, count-1)
            }
        }
        setTimeout(intro.bind(this), 1000, count-1)
    }
    draw_play(timestamp) {        

        this.context.save()
        
        // mirror mode 
        this.context.scale(-1, 1)
        this.context.translate(-this.canvas.width, 0)

        // user display
        this.context.drawImage(this.video, 0,0, this.video.videoWidth*2, this.video.videoHeight, this.canvas.width/2, 0, this.canvas.width, this.canvas.height);
        
        this.context.restore()

        // model diaplay
        this.context.drawImage(this.play_video, 0, 0, this.play_video.videoWidth*2, this.play_video.videoHeight, this.canvas.width/2, 0, this.canvas.width, this.canvas.height);

        //text
        this.context.font = `${0.003*this.canvas.width}rem Brush Script MT`;
        this.context.strokeStyle= '#1994af'
        this.context.strokeText('PLAY  DISPLAY', this.canvas.width/2+10, 50);
        this.context.fillText('PLAY  DISPLAY', this.canvas.width/2+10, 50);
        
        this.context.font = `${0.003*this.canvas.width}rem Brush Script MT`;
        this.context.strokeStyle= '#ffbb54'
        this.context.strokeText('USER  DISPLAY', 20, 50);
        this.context.fillText('USER  DISPLAY', 20, 50);
        
        this.context.font = `${0.0025*this.canvas.width}rem Brush Script MT`;
        this.context.strokeText('Score', 20, this.canvas.height - 60);
        this.context.fillText('Score', 20, this.canvas.height - 60);
        
        this.context.font = `${0.0035*this.canvas.width}rem Brush Script MT`;
        this.context.strokeText(this.score, 20, this.canvas.height - 30);
        this.context.fillText(this.score, 20, this.canvas.height - 30);
        
        this.loopID = window.requestAnimationFrame(this.draw_play.bind(this))
    }
    updateScore(score) {
        this.score += score
        console.log(this.score)
        this.context.font = `${0.0035*this.canvas.width}rem Brush Script MT`;
        this.context.strokeStyle= '#ffbb54'
        this.context.strokeText(this.score, 20, this.canvas.height - 30);
        this.context.fillText(this.score, 20, this.canvas.height - 30);
    
        this.color_frame.classList.remove('score-bad')
        this.color_frame.classList.remove('score-good')
        this.color_frame.classList.remove('score-perfect')

        if(score > 300){
            this.color_frame.classList.add('score-perfect')
        }else if(score > 100){
            this.color_frame.classList.add('score-good')
        }else{
            this.color_frame.classList.add('score-bad')
        }
    }
    
    record() {
        const chunks = [];
        const text_enc = new TextEncoder() // utf-8
        const stream = this.canvas.captureStream();
        this.rec = new MediaRecorder(stream);
        console.log(stream)
        console.log(this.rec)

        function datatoBlob(dataURL, stamp=null) {
            let array, binary, i, len;
            i = 0;
            binary = atob(dataURL.split(',')[1]);
            if (stamp !== null)
            array = [];
            while( i < stamp.length){
                array.push(stamp.charCodeAt(i))
                i++
            }
            array.push(',')
            i = 0;
            len = binary.length;
            while (i < len) {
                array.push(binary.charCodeAt(i));
                i++;
            }
            return new Blob([new Uint8Array(array)], {type: 'image/png'});
        };

        function send_chunk(){
            let recorder = new MediaRecorder(stream);
            let chunks = [];
            recorder.ondataavailable = e => chunks.push(e.data);
            recorder.onstop = e => {
                // this.msg_handler.send(data)
                let data =new File(chunks,`${this.config.pid}_${e.timeStamp}.mp4`, {type: 'video/mp4'})
                data.arrayBuffer().then(buf=>{
                    let text_buf = text_enc.encode(`${this.config.pid}_${e.timeStamp};`)
                    let text_buf2 = text_enc.encode(`ajsdf_${this.config.pid}_${e.timeStamp};`)
                    let media_buf = new Uint8Array(buf)
                    let data = new Uint8Array(text_buf.length + media_buf.length)
                    data.set(text_buf)
                    data.set(media_buf, text_buf.length)
                    this.msg_handler.send(data)
                    
                    // const videoDownloadlink = document.createElement("a");
                    // videoDownloadlink.href = URL.createObjectURL(data);
                    // videoDownloadlink.innerText = `${this.config.pid}_${e.timeStamp}`
                    // videoDownloadlink.download = `${this.config.pid}_${e.timeStamp}.webm`;
                    // document.body.appendChild(videoDownloadlink);
                    // document.body.appendChild(document.createElement('br'))
                })
            
            }
            setTimeout(()=> recorder.stop(), 2000); // we'll have a 2s media file
            recorder.start();
         }
         if (this.video.getAttribute('data-play-mode') == 'upload'){
             // generate a new file every 5s
             setInterval(send_chunk.bind(this), 2000);
         }
          
        this.rec.addEventListener('dataavailable', e=>{
            chunks.push(e.data)
            console.log(e)
            console.log(e.data)

            return
            let blob = new Blob([chunks[0], e.data], {type: 'video/mp4'})
            console.log(chunks)
            console.log(blob)
            console.log(chunks.slice(chunks.length-1))
            // this.msg_handler.send(blob)
            this.msg_handler.send(blob)
     
            blob.arrayBuffer().then(buf=>{
                let text_buf = text_enc.encode(`${this.config.pid}_${e.timeStamp};`)
                let text_buf2 = text_enc.encode(`ajsdf_${this.config.pid}_${e.timeStamp};`)
                let media_buf = new Uint8Array(buf)
                let data = new Uint8Array(text_buf.length + media_buf.length)
                data.set(text_buf)
                data.set(media_buf, text_buf.length)
                this.msg_handler.send(new Blob([data]))
            })
        })


        this.rec.addEventListener('stop', e=>{
            console.log('stopped')
            cancelAnimationFrame(this.loopID)
            this.msg_handler.close(this.config.pid)
            let video_title = this.video.getAttribute('data-title') + `_playvideo.mp4`
            this.exportVid(new Blob(chunks, {type: 'video/mp4'}), video_title)
            
            const play_data = new FormData()
            const file = new File(chunks, video_title, {'type':'video/mp4'})
            play_data.append('video', file, file.name)
            play_data.append('score', this.score)
            play_data.append('datetime', new Date(Date.now()).toString())
            this.msg_handler.sendResult('http://220.123.224.95:9000/play/?pid=' + this.config.pid, play_data)
        })

        this.play_video.addEventListener('ended', e => {
            this.rec.stop()
            this.endGame() 
        })

        this.rec.start(2000);

    }
    exportVid(blob, title) {
        const video_preview = document.querySelector('#play-video-preview')     
        const line = document.querySelectorAll('.button-line')[0]
        const vid = document.createElement('video');
        const a = document.createElement('a');
        
        vid.src = URL.createObjectURL(blob);
        vid.controls = true;
        vid.classList.add('user_video')

        a.download = title;
        a.href = vid.src;
        
        const btn = document.createElement('button')
        btn.className = 'w-btn w-btn-gra1'
        btn.textContent = 'Download Play Video'

        a.appendChild(btn)
        line.appendChild(a);
        video_preview.appendChild(vid);

        line.classList.remove('content-hide')
        line.classList.add('content-visible')
        
        return vid
    }
    endGame(){
        
        this.context.font = `${0.0055*this.canvas.width}rem Brush Script MT`;
        this.context.strokeStyle= '#a65bf8'
        this.context.strokeText('Play Done...', 20, 50);
        this.context.fillText('Play Done...', 20, 50);

        setTimeout(this.redirectToShare, 1500)
    }
    redirectToShare(){
        // result share section
        const share_page = document.querySelector('#result-share')
        const play_content = document.querySelector('#play-content')
  
        share_page.classList.remove('content-hide')
        share_page.classList.add('content-visible')
        play_content.classList.remove('content-visible')
        play_content.classList.add('content-hide')

        window.location = (""+window.location).replace(/#[A-Za-z0-9_]*$/,'')+"#result-share"        
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
            this.sendMessage('check', 'connected with client : ' + this.clientID)
            // this.socket.send({'pid' : 'pyj1234', 'path' : 'module/sample_data/result_test.mp4'})
        }
        this.socket.onmessage = e => {
            const data = JSON.parse(e.data)
            try{
                this.receivedCallBack(data)
            }catch(error){
                console.log(error)
            }
        }
        this.socket.onclose = e=>{
            console.log('disconnected')
            this.socket.close()
        }
    }
    send(data){
        this.socket.send(data)
    }
    sendJSON(obj){
        this.socket.send(JSON.stringify(obj))
    }
    sendData(type, stamp, data){
        console.log(data)
        // let datas = new Uint8Array({
        //     'type' : type,
        //     'stamp' : stamp,
        //     'data': data,
        // })
        // console.log(datas)
        // this.socket.send(datas)
        this.socket.send(JSON.stringify({
            'type' : type,
            'stamp' : stamp,
            'data': data,
        }))
    }
    sendMessage(type, msg) {
        this.socket.send(JSON.stringify({
            'type' : type,
            'message': msg,
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
    // let msg_handler = new MessageHandler('ws://192.168.0.12:5050')
    let msg_handler = new MessageHandler('ws://220.123.224.95:9000/ws/play/' + pid)
    const manager = new PlayManager(navigator, msg_handler, pid)
    manager.main()
}
main()