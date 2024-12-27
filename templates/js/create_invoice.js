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
// Функция для снятия выделения со всех чекбоксов
function clearAllCheckboxes() {
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
}

function filters(){
    // Получаем выбранного врача
    const selectedDoctor = document.getElementById('doctor').value;
    // Фильтруем заказы для каждой таблицы
    filterOrdersByDoctor('not-done-orders', selectedDoctor);
    clearAllCheckboxes();
     updateTotalPrice()
}


document.getElementById('doctor').addEventListener('change', () => filters());

function filterOrdersByDoctor(tableId, selectedDoctor) {
    // Получаем таблицу
    const table = document.getElementById(tableId);

    // Получаем все строки таблицы на первом уровне
    const rows = table.querySelectorAll('tr[data-doctor-id]'); // Только родительские строки с атрибутом

    console.log(selectedDoctor);

    // Проходим по всем строкам
    rows.forEach(row => {
        const doctorId = row.getAttribute('data-doctor-id'); // Получаем id врача из атрибута строки

        // Условие отображения строки
        const matchesDoctor = selectedDoctor === "None" || doctorId === selectedDoctor;

        // Показываем или скрываем родительские строки
        if (matchesDoctor) {
            row.style.display = ""; // Показываем строку
        } else {
            row.style.display = "none"; // Скрываем строку
        }
    });
}

document.getElementById('create_invoice').addEventListener('click', async (event) => {
    event.preventDefault();

    // Получаем выбранного врача
    const doctorSelect = document.getElementById('doctor');
    const doctorId = doctorSelect.value;

    if (!doctorId || doctorId === "None") {
        alert("Пожалуйста, выберите врача.");
        return;
    }

    // Собираем выбранные заказы
    const selectedOrders = Array.from(document.querySelectorAll('input[name="orders"]:checked')).map(input => input.value);

    if (selectedOrders.length === 0) {
        alert("Пожалуйста, выберите хотя бы один заказ.");
        return;
    }

    // Создаем тело запроса
    const requestBody = {
        doctor_id: parseInt(doctorId),
        orders: selectedOrders.map(Number),
    };

    try {
        // Выполняем POST-запрос
        const response = await fetch('/technik/invoice/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        if (response.ok) {
            // Перенаправляем на страницу /technik/invoice/show
            window.location.href = '/technik/invoice/show';
        } else {
            const errorMessage = await response.text();
            alert(`Ошибка создания счета: ${errorMessage}`);
        }
    } catch (error) {
        console.error('Ошибка при создании счета:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте еще раз.');
    }
});


document.addEventListener('DOMContentLoaded', function() {
    filters();
});
