


/*
    Index page navigation template
*/
Vue.component('df-index-nav', {
    template : ` <!-- Navigation -->
    <nav id="navbar" class="navbar navbar-expand-lg fixed-top navbar-dark" aria-label="Main navigation">
        <div class="container">
            <!-- Image Logo -->
            <a class="navbar-brand logo-image" href="index.html"><img src="images/logo.png" alt="alternative"><span>DancerFlow</span></a> 

            <!-- Text Logo - Use this if you don't have a graphic logo -->
            <!-- <a class="navbar-brand logo-text" href="index.html">Elma</a> -->

            <button class="navbar-toggler p-0 border-0" type="button" id="navbarSideCollapse" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="navbar-collapse offcanvas-collapse" id="navbarsExampleDefault">
                <ul class="navbar-nav ms-auto navbar-nav-scroll">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#header">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#community">Community</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" aria-current="page" href="#aboutus">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#contact">Contact</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#howto">Ranking</a>
                    </li>
                    <li class="nav-item">
                        <a class="btn-solid-reg sign-btn" href="sign.html" >Sign in</a>
                    </li>
                </ul>
            </div> <!-- end of navbar-collapse -->
        </div> <!-- end of container -->
    </nav> <!-- end of navbar -->
    <!-- end of navigation -->`,

});



let app_index_nav = new Vue({
    el:'#app-index-nav'
});



/*
    Main-Content-Service page navigation template
*/
Vue.component('df-main-nav', {
    template : ` <!-- Navigation -->
    <nav id="navbar" class="navbar navbar-expand-lg fixed-top navbar-dark" aria-label="Main navigation">
        <div class="container">
            <!-- Image Logo -->
            <a class="navbar-brand logo-image" href="index.html"><img src="images/logo.png" alt="alternative"><span>DancerFlow</span></a> 

            <!-- Text Logo - Use this if you don't have a graphic logo -->
            <!-- <a class="navbar-brand logo-text" href="index.html">Elma</a> -->

            <button class="navbar-toggler p-0 border-0" type="button" id="navbarSideCollapse" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="navbar-collapse offcanvas-collapse" id="navbarsExampleDefault">
                <ul class="navbar-nav ms-auto navbar-nav-scroll">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="index.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="community.html">Community</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" aria-current="page" href="option_mode.html">Play</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#Ranking">Ranking</a>
                    </li>
                    <li class="nav-item">
                        <a class="btn-solid-reg sign-btn" href="sign.html" >Sign in</a>
                    </li>
                </ul>
            </div> <!-- end of navbar-collapse -->
        </div> <!-- end of container -->
    </nav> <!-- end of navbar -->
    <!-- end of navigation -->`,

});



let app_main_nav = new Vue({
    el:'#app-main-nav'
});



/*
    Play page navigation template
*/
Vue.component('df-play-nav', {
    template : `<!-- Navigation -->
    <nav id="navbar" class="navbar navbar-expand-lg fixed-top navbar-dark" aria-label="Main navigation">
        <div class="container">
            <!-- Image Logo -->
            <a class="navbar-brand logo-image" href="index.html"><img src="images/logo.png" alt="alternative"><span>DancerFlow</span></a> 

            <button class="navbar-toggler p-0 border-0" type="button" id="navbarSideCollapse" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="navbar-collapse offcanvas-collapse" id="navbarsExampleDefault">
                <ul class="navbar-nav ms-auto navbar-nav-scroll">
                    <li class="nav-item">
                        <a class="btn-solid-reg sign-btn" href="sign.html" >Sign in</a>
                    </li>
                </ul>
            </div> <!-- end of navbar-collapse -->
        </div> <!-- end of container -->
    </nav> <!-- end of navbar -->
    <!-- end of navigation -->
  `,

});



let app_play_nav = new Vue({
    el:'#app-play-nav'
});







