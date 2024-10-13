document.getElementById('doctor').addEventListener('change', () => {
    // Получаем выбранного врача
    const selectedDoctor = document.getElementById('doctor').value;

    // Фильтруем заказы для каждой таблицы
    filterOrdersByDoctor('not-done-orders', selectedDoctor);
    filterOrdersByDoctor('fitting-done-orders', selectedDoctor);
    filterOrdersByDoctor('done-orders', selectedDoctor);
});

// Функция фильтрации заказов по идентификатору врача
function filterOrdersByDoctor(tableId, selectedDoctor) {
    // Получаем таблицу
    const table = document.getElementById(tableId);

    // Получаем все строки таблицы
    const rows = table.getElementsByTagName('tr');
    console.log(selectedDoctor)
    // Проходим по всем строкам таблицы
    for (let i = 1; i < rows.length; i++) { // Пропускаем первую строку (заголовки)
        const doctorId = rows[i].getAttribute('data-doctor-id'); // Получаем id врача из атрибута строки
        console.log(doctorId)
        // Если выбран врач или выбрано "Все врачи", показываем строку, иначе скрываем
        if (selectedDoctor === "None" || doctorId === selectedDoctor) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
}
