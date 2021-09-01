
/*
    Mode Option template
*/
Vue.component('df-option-mode',{
    template:`
    <section class="pricing-card-area section-padding30 section-bg" data-background="assets/img/gallery/section_bg1.png">
        <div class="container">
                <!-- Section Tittle -->
                <div class="row d-flex justify-content-center">
                <div class="col-lg-8">
                    <div class="section-tittle text-center mb-70">
                        <h2 style = "color : #A65BF8 ">Play Mode</h2>
                    </div>
                </div>
            </div>
            <section class="class1">
                <div class="row align-items-end">
                    <div class="col-xl-4 col-lg-4 col-md-6" style="width: 330px !important;">
                        <div class="single-card text-center mb-30" style="
                        padding-left: 0px;
                        padding-right: 0px;
                        border-left-width: 0px;
                        border-right-width: 0px;
                        padding-top: 30px;
                    ">
                            <div class="card-top">
                                <span></span>
                                <h4>Practice</h4>
                            </div>
                            <div class="card-bottom" >
                                <ul>
                                    <div style="background-color: #C1A0D9;height: 143px;padding-top: 5px;">
                                    <strong><h6>Real Time</h6></strong></br>
                                    <strong></h6>or</h6></strong></br></br>
                                    <strong><h6>Upload A Video</h6></strong>
                                </div>
                                </br>
                                <strong>Lorem ipsum dolor sit amet,</strong></br>
                                <strong>consectetur</strong>
                                </ul>
                            </div>
                            <div class="card-buttons mt-30">
                                <a href="#" class="btn card-btn1"  >Select</a>
                            </div>
                        </div>
                    </div>
                   
                    <div class="col-xl-4 col-lg-4 col-md-6" style="width: 330px !important;">
                        <div class="single-card text-center mb-30" style="
                        padding-left: 0px;
                        padding-right: 0px;
                        border-left-width: 0px;
                        border-right-width: 0px;
                        padding-top: 30px;
                    ">
                            <div class="card-top">
                                <span></span>
                                <h4>Random</h4>
                            </div>
                            <div class="card-bottom">
                                <ul>
                                    <div style="background-color: #C1A0D9;height: 144px;padding-top: 8px;">
                                        <strong>　</strong></br></br>
                                        <strong><h6>Only Real Time Mode</h6></strong></br>
                                        <strong>　</strong>
                                    </div>
                                </br>
                                <strong>Lorem ipsum dolor sit amet,</strong></br>
                                <strong>consectetur</strong>
                                </ul>
                            </div>
                            <div class="card-buttons mt-30">
                                <a href="#" class="btn card-btn1">Select</a>
                            </div>
                        </div>
                    </div>

                </section>
            </div>
        </div>
    </section>
    `
});



let app_option_mode = new Vue({
    el: "#app-option-mode"
});


/*
    Upload Option Template
*/
Vue.component('df-option-upload', {
    template:`
    <section class="pricing-card-area section-padding30 section-bg" data-background="assets/img/gallery/section_bg1.png">
        <div class="container">
                <!-- Section Tittle -->
                <div class="row d-flex justify-content-center">
                <div class="col-lg-8">
                    <div class="section-tittle text-center mb-70">
                        <h2 style = "color : #A65BF8 ">Play Mode</h2>
                        <!-- <img src="assets/img/gallery/tittle_img.png" alt=""> -->
                        <!-- <p style = "color : #1994AF">Select Real time or Random</p> -->
                    </div>
                </div>
            </div>
            <div class="row align-items-end">
                <div class="col-xl-4 col-lg-4 col-md-6" style="width: 330px !important;">
                    <div class="single-card text-center mb-30" style="padding-top: 30px;padding-right: 0px;padding-left: 0px;border-right-width: 0px;border-left-width: 0px;">
                        <div class="card-top">
                            <span></span>
                            <h4>Real time</h4>
                        </div>
                        <div class="card-bottom">
                            <ul>
                                <div style="background-color: #C1A0D9;height: 150px;">
                                </br>
                            
                            </div>
                            </br>
                            <strong>Lorem ipsum dolor sit amet,</strong></br>
                                <strong>consectetur</strong>
                            
                            </ul>
                        </div>
                        <div class="card-buttons mt-30" style="padding-bottom: 25px;">
                            <a href="#" class="btn card-btn1">Select</a>
                        </div>
                    </div>
                </div>
            
                <div class="col-xl-4 col-lg-4 col-md-6" style="width: 330px !important;">
                    <div class="single-card text-center mb-30" style="padding-top: 30px;padding-right: 0px;padding-left: 0px;border-right-width: 0px;border-left-width: 0px;border-bottom-width: 26px;">
                        <div class="card-top">
                            <span></span>
                            <h4>Upload</h4>
                        </div>
                        <div class="card-bottom">
                            <ul>
                                <div style="background-color: #C1A0D9;height: 150px;">
                                </br>
                                <strong><h6>Drag & Drop</h6></strong></br></br>
                                <li><button style = "background-color: #211A4D ">Choose a File</button></li>
                            </br>
                                <strong>Lorem ipsum dolor sit amet,</strong></br>
                                <strong>consectetur</strong>
                            <li>　</li>
                            </div>
                            </ul>
                        </div>
                    </br></br></br>
                        <div class="card-buttons mt-30" >
                            <a href="#" class="btn card-btn1">Select</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    `
});

let app_option_upload = new Vue({
    el: '#app-option-upload'
})


/*
    Display Option Template
*/

Vue.component('df-option-display', {
    template:`
    <section class="pricing-card-area section-padding30 section-bg" data-background="assets/img/gallery/section_bg1.png">
        <div class="container">
                <!-- Section Tittle -->
                <div class="row d-flex justify-content-center">
                <div class="col-lg-8">
                    <div class="section-tittle text-center mb-70">
                        <h2 style = "color : #A65BF8 ">Display Mode</h2>
                        
                        <!-- <p style = "color : #1994AF">Select Your Display Mode</p> -->
                        
                    </div>
                </div>
            </div>
            <div class="row align-items-end">
                <div class="col-xl-4 col-lg-4 col-md-6" >
                    <div class="single-card text-center mb-30" style="
                    padding-top: 30px;
                ">
                        <div class="card-top">
                            <span></span>
                            <h4>User-Play Horizontal</h4>
                        </div>
                        <div class="card-bottom">
                            <ul>
                                <div style="display: flex;justify-content: center;">
                                <button style="background-color: #211A4D;width: 161px;height: 103px;">1</button>
                                <button style="background-color: white; width: 161px;height: 103px; color: black;">2</button>
                                 </div>
                            </br>
                            <strong>Lorem ipsum dolor sit amet,</strong></br>
                            <strong>consectetur</strong>
                            <li>　</li>
                            </ul>
                        </div>
                        
                    </div>
                </div>
                <div class="col-xl-4 col-lg-4 col-md-6">
                    <div class="single-card text-center mb-30" style="
                    padding-top: 30px;
                ">
                        <div class="card-top">
                            <span></span>
                            <h4>User-Play vertical</h4>
                        </div>
                        <div class="card-bottom">
                            <ul>
                                <div style="display: flex;flex-direction: column;">
                                <button style="background-color: #211A4D;height: 52px;">1</button>
                                <button style="background-color: white;height: 52px; color: black;">2</button>
                            </div>
                            </br>
                            <strong>Lorem ipsum dolor sit amet,</strong></br>
                            <strong>consectetur</strong>
                            <li>　</li>
                            </ul>
                        </div>
                        
                    </div>
                </div>
                <div class="col-xl-4 col-lg-4 col-md-6">
                    <div class="single-card text-center mb-30" style="
                    padding-top: 30px;
                ">
                        <div class="card-top">
                            <span></span>
                            <h4>Only User</h4>
                        </div>
                        <div class="card-bottom">
                            <ul>
                                <div style="display: flex;flex-direction: column;">
                                <button style="background-color: #211A4D;height: 106px;">1</button>
                            </div>
                            </br>
                            <strong>Lorem ipsum dolor sit amet,</strong></br>
                            <strong>consectetur</strong>
                            <li>　</li>
                            </ul>
                        </div>
                       
                    </div>
                </div>
    </section>
     
    `
});


let app_option_display = new Vue({
    el : '#app-option-display'
})

