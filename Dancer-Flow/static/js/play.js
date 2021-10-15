
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
        this.chunkLoopID = null
        this.total_score = 0
        this.parts_score = {
            'face_body' : 0,
            'left_arm' : 0,
            'right_arm' : 0,
            'left_leg' : 0,
            'right_leg' : 0,
        }
        this.msg_handler = msg_handler
        this.config = {
            pid: pid,
            id: this.msg_handler.CLIENT_ID,
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
        // window.onresize = this.resizeCanvas.bind(this)
        this.resizeCanvas.bind(this)()
        this.init_share_form()

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

        if(this.video.getAttribute('data-play-mode') === 'realtime'){
            this.initCaptureVideo(this.video);
        }else if(this.video.getAttribute('data-play-mode') === 'upload'){
            // this.video.play()
            // this.play_video.play()
        }
    }

    init_share_form(){
        const form = document.getElementById('shareForm')
        form.addEventListener('sendButton', e=>{
            
        })

    }

    init_handler(){
        this.msg_handler.setReceiveCallBack(data=>{
            console.log(data)
            switch (data.type) {
                case 'message':
                    break;
                case 'update_score':
                    this.updateScore(data.score, data.parts_score)
                    break
            }
        })
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
        let width = parseInt(window.innerWidth * 1.);
        let height = parseInt(window.innerHeight * 0.6);

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
            this.context.clearRect(0,0, this.canvas.width, this.canvas.height);

            // this.context.globalAlpha = 0.2;
            // this.context.fillRect(this.canvas.width/4+100, this.canvas.height/3-50, this.canvas.width/2-150, this.canvas.height/2-50)

            this.context.font = `${0.004*this.canvas.width}rem Brush Script MT`;
            this.context.strokeText(`Ready...`, (this.canvas.width * 0.818) /2, (this.canvas.height*0.798) / 2);
            this.context.fillText(`Ready...`, (this.canvas.width * 0.818) /2, (this.canvas.height * 0.798) /2);
    
            if (count > 0){
                this.context.strokeText(`${count}`, (this.canvas.width * 0.919) /2, (this.canvas.height * 1.2519) /2);
                this.context.fillText(`${count}`, (this.canvas.width * 0.919) /2, (this.canvas.height * 1.2519) /2);
            }
            else{
                this.context.strokeText(`Start !`, (this.canvas.width * 0.819) /2, (this.canvas.height * 1.2519) /2);
                this.context.fillText(`Start !`, (this.canvas.width * 0.819) /2, (this.canvas.height * 1.2519) /2);
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
        this.context.font = `${0.00255*this.canvas.width}rem Brush Script MT`;
        this.context.strokeStyle= '#1994af'
        this.context.strokeText('PLAY  DISPLAY', (this.canvas.width * 1.0155) /2, this.canvas.height * 0.105);
        this.context.fillText('PLAY  DISPLAY', (this.canvas.width * 1.0155) /2, this.canvas.height * 0.105);
        
        this.context.font = `${0.00255*this.canvas.width}rem Brush Script MT`;
        this.context.strokeStyle= '#ffbb54'
        this.context.strokeText('USER  DISPLAY', this.canvas.width * 0.0155, this.canvas.height * 0.105);
        this.context.fillText('USER  DISPLAY', this.canvas.width * 0.0155, this.canvas.height * 0.105);
        
        this.context.font = `${0.00205*this.canvas.width}rem Brush Script MT`;
        this.context.strokeText('Score', this.canvas.width * 0.0155, this.canvas.height * 0.805 );
        this.context.fillText('Score', this.canvas.width * 0.0155, this.canvas.height * 0.805 );
        
        this.context.font = `${0.00255*this.canvas.width}rem Brush Script MT`;
        this.context.strokeText(this.total_score, this.canvas.width * 0.0155, this.canvas.height * 0.925);
        this.context.fillText(this.total_score, this.canvas.width * 0.0155, this.canvas.height * 0.925);
        
        this.loopID = window.requestAnimationFrame(this.draw_play.bind(this))
    }
    updateScore(score, parts_score) {
        this.total_score += score
        this.parts_score['face_body'] += parts_score['face_body']
        this.parts_score['left_arm'] += parts_score['left_arm']
        this.parts_score['right_arm'] += parts_score['right_arm']
        this.parts_score['left_leg'] += parts_score['left_leg']
        this.parts_score['right_leg'] += parts_score['right_leg']

        this.context.font = `${0.00255*this.canvas.width}rem Brush Script MT`;
        this.context.strokeStyle= '#ffbb54'
        this.context.strokeText(this.total_score, this.canvas.width * 0.0515, this.canvas.height * 0.925);
        this.context.fillText(this.total_score, this.canvas.width * 0.0515, this.canvas.height * 0.925);
    
        this.color_frame.classList.remove('score-bad')
        this.color_frame.classList.remove('score-good')
        this.color_frame.classList.remove('score-perfect')

        if(score > 4){
            this.color_frame.classList.add('score-perfect')
        }else if(score > 2.5){
            this.color_frame.classList.add('score-good')
        }else{
            this.color_frame.classList.add('score-bad')
        }
    }
    
    record() {
        const chunks = [];
        const stream = this.canvas.captureStream();
        this.rec = new MediaRecorder(stream);

        function send_chunk(){
            let recorder = new MediaRecorder(stream);
            let chunks = [];
            recorder.ondataavailable = e => chunks.push(e.data);
            recorder.onstop = e => {
                // this.msg_handler.send(data)
                console.log(e)
                console.log(e.timeStamp)
                let data =new File(chunks,`${this.config.pid}_${e.timeStamp}.mp4`, {type: 'video/mp4'})
                this.msg_handler.send(data)
            }
            setTimeout(()=> recorder.stop(), 1500); 
            recorder.start();
         }

         const CHUNK_LOOP_ID = setInterval(send_chunk.bind(this), 1500) // have a 1.5s media file
         this.msg_handler.setChunkLoopID(CHUNK_LOOP_ID) 
          
        this.rec.addEventListener('dataavailable', e=>{
            chunks.push(e.data)
        })

        this.rec.addEventListener('stop', e=>{
            console.log('stopped')
            cancelAnimationFrame(this.loopID)
            clearInterval(this.msg_handler.CHUNK_LOOP_ID)
            this.msg_handler.close(this.config.pid)
            let video_title = this.video.getAttribute('data-title') + `_playvideo.mp4`
            this.exportVid(new Blob(chunks, {type: 'video/mp4'}), video_title)
            
            const play_data = new FormData()
            const file = new File(chunks, video_title, {'type':'video/mp4'})
            play_data.append('pid', this.config.pid)
            play_data.append('play_video', file, file.name)
            play_data.append('total_score', this.total_score)
            play_data.append('parts_score', JSON.stringify(this.parts_score))
            play_data.append('datetime', new Date(Date.now()).toString())
            this.msg_handler.sendResult('http://127.0.0.1:8000/play/?pid=' + this.config.pid, play_data)
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
        
        this.context.font = `${0.0045*this.canvas.width}rem Brush Script MT`;
        this.context.strokeStyle= '#a65bf8'
        this.context.strokeText('Play Done...', (this.canvas.width * 0.818) /2, (this.canvas.height * 0.798) /2);
        this.context.fillText('Play Done...', (this.canvas.width * 0.818) /2, (this.canvas.height * 0.798) /2);
        
        const scoreText = document.getElementById('scoreText')
        scoreText.innerText = 'Score : ' + this.total_score 

        let polygon_chart_el = document.getElementById("polygon-chart");
        console.log(this.parts_score)
        let parts_list = Object.values(this.parts_score)
        parts_list = parts_list.map(item=>{
            return parseFloat('0.' + item)
        })
        parts_list.push(parts_list.shift())
        console.log(parts_list)
        // play_result.js function
        create_polygon_chart(polygon_chart_el, [parts_list]).init()

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
        this.CLIENT_ID = "client 1"
        this.URL = URL
        this.socket = new WebSocket(this.URL)
        this.receivedCallBack = null
        this.CHUNK_LOOP_ID = null
        this.init()
    }
    init() {
        this.socket.onopen = e => {
            this.sendMessage('check', 'connected with client : ' + this.CLIENT_ID)
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
    setChunkLoopID(loopID){
        this.CHUNK_LOOP_ID = loopID
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
    // let msg_handler = new MessageHandler('ws://192.168.0.28:8000/ws/play/' + pid)
    let msg_handler = new MessageHandler('ws://127.0.0.1:8000/ws/play/' + pid)
    console.log(navigator)
    const manager = new PlayManager(navigator, msg_handler, pid)
    manager.main()

}
main()