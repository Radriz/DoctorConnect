// Получаем элементы DOM
const checkboxes = document.querySelectorAll('input[name="orders"]');
const totalPriceElement = document.getElementById('total_price');

// Функция для пересчёта стоимости
function updateTotalPrice() {
    let total = 0;

    // Проходим по всем чекбоксам
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            // Получаем строку таблицы, соответствующую чекбоксу
            const row = checkbox.closest('tr');
            // Ищем ячейку с ценой
            const priceCell = row.querySelector('td:nth-child(6)');
            if (priceCell) {
                // Извлекаем цену и добавляем к общей стоимости
                const price = parseFloat(priceCell.textContent.replace(/[^\d.]/g, ''));
                if (!isNaN(price)) {
                    total += price;
                }
            }
        }
    });

    // Обновляем итоговую стоимость
    totalPriceElement.textContent = total;
}

// Добавляем обработчики событий на чекбоксы
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateTotalPrice);
});

function filters(){
    // Получаем выбранного врача
    const selectedDoctor = document.getElementById('doctor').value;
    console.log(text)
    // Фильтруем заказы для каждой таблицы
    filterOrdersByDoctor('not-done-orders', selectedDoctor, text);
}


document.getElementById('doctor').addEventListener('change', () => filters());

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
