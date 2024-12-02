document.getElementById("speciality").addEventListener("change", function() {
    const speciality = document.getElementById("speciality").value;
    if (speciality == "doctor") {
        document.getElementById("clinic_div").style.display = "block";
    } else {
        document.getElementById("clinic_div").style.display = "none";
    }
});

const form = document.getElementById("formReg");
const modal = document.getElementById("modal");
const closeModal = document.querySelector(".close");
const confirmButton = document.getElementById("confirmButton");

form.addEventListener("submit", async function(event) {
    event.preventDefault();
    email = document.getElementById("email").value;


    modal.style.display = "flex";
    // Закрытие модального окна
    closeModal.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Закрытие при клике вне окна
    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // Отправка кода на email
    const codeResponse = await fetch('/send/email/code?email=' + email, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    });

    if (!codeResponse.ok) {
        alert('Ошибка при отправке письма с кодом');
        return;
    }

    const codeResponseData = await codeResponse.json();
    const code = codeResponseData.code;



    // Обработка кнопки подтверждения в модальном окне
    confirmButton.addEventListener("click", function() {
        const userCode = document.getElementById("confirmationCode").value;
        if (parseInt(code) === parseInt(userCode)){
            alert("Вы успешно зарегистрировались!");
            modal.style.display = "none";
            form.submit();
        } else {
            alert("Неверный код подтверждения! Попробуйте еще раз.");
        }
    });


});
