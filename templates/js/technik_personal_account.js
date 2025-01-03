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

    // Получаем все строки таблицы на первом уровне
    const rows = table.querySelectorAll('tr[data-doctor-id]'); // Только родительские строки с атрибутом

    console.log(selectedDoctor);

    // Проходим по всем строкам
    rows.forEach(row => {
        const doctorId = row.getAttribute('data-doctor-id'); // Получаем id врача из атрибута строки
        const clientName = row.cells[1]?.textContent.toLowerCase() || ""; // Проверка на null

        // Условие отображения строки
        const matchesDoctor = selectedDoctor === "None" || doctorId === selectedDoctor;
        const matchesClient = text === "" || clientName.includes(text);

        // Показываем или скрываем родительские строки
        if (matchesDoctor && matchesClient) {
            row.style.display = ""; // Показываем строку
        } else {
            row.style.display = "none"; // Скрываем строку
        }
    });
}
