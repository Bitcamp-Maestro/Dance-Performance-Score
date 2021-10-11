const username = document.querySelector('#username');
const feedBackArea = document.querySelector('.invalid-feedback');
const email = document.querySelector('#email');
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");

// 사용자가 email blcok안에 키보드 입력을 감지.
email.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  email.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/user/validate-email", {
      body: JSON.stringify({ email: emailVal }), //JSON 문자열로 변환할 값
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.email_error) {
          email.classList.add("is-invalid");
          emailfeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        }
      });
  }
});




// 사용자가 username block안에 키보드 입력을 감지. 
username.addEventListener('keyup', (e) => {
  const usernameVal = e.target.value;

  username.classList.remove("is-invalid");
  feedBackArea.style.display = "none";

  if (usernameVal.length > 0) {
    fetch("/user/validate-username", {
      body: JSON.stringify({username: usernameVal }), //JSON 문자열로 변환할 값
      method:"POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.username_error){
          username.classList.add("is-invalid");
          //get error from data and display in in feedBackArea
          feedBackArea.style.display ="block";
          feedBackArea.innerHTML=`<p>${data.username_error}</p>`;
        }
      });
  }
});