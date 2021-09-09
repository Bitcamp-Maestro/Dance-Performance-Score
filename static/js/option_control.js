/*
    Option Card Elements 
*/
const practice_card = document.querySelector('#practice-card');
const random_card = document.querySelector('#random-card');
const realtime_card = document.querySelector('#realtime-card');
const upload_card = document.querySelector('#upload-card');
const u_p_h_card = document.querySelector('#u-p-h-card');
const u_p_v_card = document.querySelector('#u-p-v-card');
const u_o_card = document.querySelector('#u-o-card');
const cards = document.querySelectorAll('.single-card')     // card list

const option_container = document.querySelectorAll('.option-container')     // option view

/*
    Button
 */ 
const prev_btn = document.querySelector('#prev-option-btn');
const next_btn = document.querySelector('#next-option-btn');
const start_btn = document.querySelector('#play-start-btn');
const select_btn = document.querySelectorAll('.select-btn')


/*
    Setting Values
*/
const ITEM_FOCUSED_CLASSNAME = 'item-focused';

const OPTION_SELECTOR = {
    'MODE': '.mode-option-card',
    'UPLOAD': '.upload-option-card',
    'DISPLAY': '.display-option-card',
    'SONG' : '.display-option-song',
    'MODE_C' : '#app-option-mode',
    'UPLOAD_C' : '#app-option-upload',
    'DISPLAY_C' : '#app-option-display',
    'SONG_C' : '#app-option-song',
}

// const OPTION_SET = {
//     'MODE' : {'PRACTICE' : practice_card, 'RANDOM' : random_card},
//     'UPLOAD' : {'REALTIME' : realtime_card, 'UPLOAD' : upload_card},
//     'DISPLAY' : {'UPH' : u_p_h_card, 'UPV' : u_p_v_card, 'UO' : u_o_card},
// }

// const OPTION_TYPE = {
//     'app-option-mode':,
//     'app-option-upload':,
//     'app-option-display':,
// }

let visible_target_option  = OPTION_SELECTOR.MODE; 


/*
    Option Form Value
*/
let options = {
    'mode' : '',
    'upload' : '',
    'upload_file' : '',
    'display' : '',
}


/*
    Card Event
*/

function switch_card(item){    
    const sets = document.querySelectorAll(visible_target_option)
    sets.forEach(i=>i.classList.remove(ITEM_FOCUSED_CLASSNAME));
    item.classList.add(ITEM_FOCUSED_CLASSNAME);
}

cards.forEach(item => {
    item.addEventListener('click', e => {
        switch_card(item);
    });
});
cards.forEach(item => {
    item.addEventListener('dblclick', e => {
        switch_card(item);
        next_btn.click();
    });
});

// browser 기본 drag drop 이벤트(ex file open) 를 막기 위해 preventdefault 호출
upload_card.addEventListener('dragover', e=>{
    e.preventDefault()
    upload_card.style.backgroundColor = '#C1A0D9'  
})
upload_card.addEventListener('dragleave', e=>{
    e.preventDefault()
    upload_card.style.backgroundColor = '#ffffff'  
})
upload_card.addEventListener('drop', e=>{
    e.preventDefault()
    // console.log(e.dataTransfer)
    console.log(e.dataTransfer.files)
    // console.log(e.dataTransfer.items)
    const video_file = e.dataTransfer.files[0]
    options.upload_file = video_file
    
    const data_zone = document.getElementById('droped-file-zone')
    data_zone.innerHTML = `<h6> ${video_file.name} Droped </h6>`
    e.target.click()
    next_btn.click()

})


/*
    Button Event
*/
select_btn.forEach(btn=>btn.addEventListener('click', e=>{
     next_btn.click()
}))

function switch_option (target_option) {
    option_container.forEach(i=>i.classList.remove('content-visible'))
    option_container.forEach(i=>i.classList.add('content-hide'))
    target_option.classList.add('content-visible')
}

prev_btn.addEventListener('click',e=>{
    switch(visible_target_option){
        case OPTION_SELECTOR.MODE:  
            console.error('logic error')
            break;
        case OPTION_SELECTOR.UPLOAD:
            switch_option(option_container[0])
            prev_btn.classList.remove('content-visible')
            prev_btn.classList.add('content-hide')
            visible_target_option = OPTION_SELECTOR.MODE;
            break;
        case OPTION_SELECTOR.DISPLAY:
            switch_option(option_container[1])
            visible_target_option = OPTION_SELECTOR.UPLOAD;
            break;
        case OPTION_SELECTOR.SONG:
            switch_option(option_container[2])
            next_btn.classList.add('content-visible')
            next_btn.classList.remove('content-hide')
            start_btn.classList.remove('content-visible')
            start_btn.classList.add('content-hide')
            visible_target_option = OPTION_SELECTOR.DISPLAY;
            break;
    }
});

next_btn.addEventListener('click',e=>{
    switch(visible_target_option){
        case OPTION_SELECTOR.MODE:  
            switch_option(option_container[1])  
            prev_btn.classList.add('content-visible')
            visible_target_option = OPTION_SELECTOR.UPLOAD;
            break;
        case OPTION_SELECTOR.UPLOAD:
            switch_option(option_container[2])
            visible_target_option = OPTION_SELECTOR.DISPLAY;
            break;
        case OPTION_SELECTOR.DISPLAY:
            switch_option(option_container[3])
            next_btn.classList.remove('content-visible')
            next_btn.classList.add('content-hide')
            start_btn.classList.add('content-visible')
            start_btn.classList.remove('content-hide')
            visible_target_option = OPTION_SELECTOR.SONG;
            break;
        case OPTION_SELECTOR.SONG:
            console.error('logic error') 
            break;
    }
});

start_btn.addEventListener('click', async e=>{
    const option_list = document.getElementsByClassName(ITEM_FOCUSED_CLASSNAME)
    if(option_list.length < 3){
        window.alert('옵션을 설정해주세요.')
        return
    }
    const data = new FormData()
    data.append('mode', option_list[0].getAttribute('data-value'))
    data.append('upload', option_list[1].getAttribute('data-value'))
    data.append('display', option_list[2].getAttribute('data-value'))
    data.append('video', options.upload_file, options.upload_file.name)
    data.append('songs', 'asdf')
    // options.mode = option_list[0].getAttribute('data-value')
    // options.upload = option_list[1].getAttribute('data-value')
    // options.display = option_list[2].getAttribute('data-value')
    console.log(data)
    let result = await sendOption(data)
    console.log('result')
    console.log(result)
    // location.href = '/play'
})


/*
    Server Request
*/
async function sendOption(options){
    console.log(options)
    const URL = 'http://127.0.0.1:8000'
    const request = new Request(URL + '/play/api/options', {
        headers:{
            'X-CSRFToken': getCookie("csrftoken"),
            // 'Content-Type' : 'multipart/form-data',
        }
    })
    let res = await fetch(request, {
        method : 'POST',
        mode : 'same-origin',
        body : options,
    })
    // console.log(res.json())
    console.log(res)
    return res
}

function getCookie(name) {
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

