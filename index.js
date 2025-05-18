console.log('Happy developing ✨');

const form = document.getElementById("loginForm");
const message = document.getElementById("message");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (username === "") {
        message.textContent = "Kullanıcı adı boş olamaz!";
        message.classList.add("error");
        message.classList.remove("success");
        return;
    }

    if (password === "") {
        message.textContent = "Parola boş olamaz!";
        message.classList.add("error");
        message.classList.remove("success");
        return;
    }

    if (username === "admin" && password === "1234") {
        message.textContent = "Giriş Başarılı!";
        message.classList.add("success");
        message.classList.remove("error");
    } else {
        message.textContent = "Hatalı kullanıcı adı veya parola!";
        message.classList.add("error");
        message.classList.remove("success");
    }
});