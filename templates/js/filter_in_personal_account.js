function filters(){
    // Получаем выбранного врача
    const selectedDoctor = document.getElementById('doctor').value;
    const text = document.getElementById("client").value.toLowerCase();
    console.log(text)
    // Фильтруем заказы для каждой таблицы
    filterOrdersByDoctor('not-done-orders', selectedDoctor, text);
    filterOrdersByDoctor('fitting-done-orders', selectedDoctor, text);
    filterOrdersByDoctor('done-orders', selectedDoctor, text);
}

document.getElementById('doctor').addEventListener('change', () => filters());
document.getElementById("client").addEventListener("input", () => filters());

// Функция фильтрации заказов по идентификатору врача
function filterOrdersByDoctor(tableId, selectedDoctor, text) {
    // Получаем таблицу
    const table = document.getElementById(tableId);

    let clientColumnIndex = -1;

    const headers = table.querySelectorAll('th');
    headers.forEach((header, index) => {
        console.log(header.textContent);
        if (header.textContent.trim() === "ФИО пациента") {
            clientColumnIndex = index;
        }
    });

    // Проверка, нашли ли мы нужный столбец
    if (clientColumnIndex === -1) {
        console.error("Не найден столбец с заголовком 'ФИО пациента'.");
        return;
    }

    // Получаем все строки таблицы на первом уровне
    const rows = table.querySelectorAll('tr[data-user-id]'); // Только родительские строки с атрибутом


    // Проходим по всем строкам
    rows.forEach(row => {
        const doctorId = row.getAttribute('data-user-id'); // Получаем id врача из атрибута строки
        const clientName = row.cells[clientColumnIndex]?.textContent.toLowerCase() || ""; // Проверка на null

        // Условие отображения строки
        const matchesDoctor = selectedDoctor === "None" || doctorId === selectedDoctor;
        const matchesClient = text === "" || clientName.includes(text);
        row.style.display = "";
        // Показываем или скрываем родительские строки
        if (matchesDoctor && matchesClient) {
            row.classList.remove("not-match-search"); // Показываем строку
        } else {
            row.classList.add("not-match-search"); // Скрываем строку
        }
    });
    console.log("Фильтрация завершена, вызываем showButton.");
    window.showButton();
}

