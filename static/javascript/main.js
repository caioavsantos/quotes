let profilebutton = document.querySelector(".profileBtn");
let loginbox = document.querySelector(".loginbox");


if (profilebutton && loginbox) {

    profilebutton.addEventListener("click", function () {
        loginbox.style.display = "block";
    });

    window.addEventListener("click", function (e) {
        if (!loginbox.contains(e.target) && e.target !== profilebutton) {
            loginbox.style.display = "none";
        }
    });
}