
function toggleTable(button) {
    const table = button.previousElementSibling; // Таблица перед кнопкой
   const rows = table.querySelectorAll('tr[data-user-id]:not(.not-match-search)'); // Все строки таблицы
    const isCollapsed = button.querySelector("img").getAttribute("src").includes("down_arrow");

    // Установка видимости строк
    rows.forEach((row, index) => {
        if (index > 4) {
            row.style.display = isCollapsed ? "" : "none";
        }
    });

    // Изменение изображения стрелки
    const img = button.querySelector("img");
    img.setAttribute("src", isCollapsed ? "/images/up_arrow.png" : "/images/down_arrow.png");
    img.setAttribute("alt", isCollapsed ? "Показать меньше" : "Показать больше");
}

function showButton() {
 document.querySelectorAll(".table-container").forEach(container => {
        const table = container.querySelector("table");
        const button = container.querySelector(".toggle-button");
        const rows = table.querySelectorAll('tr[data-user-id]:not(.not-match-search)');
        console.log(rows)
        // Если строк меньше или равно 18, скрываем кнопку
        if (rows.length <= 4) {
            button.style.display = "none";
        } else {
            // Если строк больше 18, ограничиваем видимость до 6 (заголовок + 5 строк)
            rows.forEach((row, index) => {
                if (index > 4) row.style.display = "none";
            });
            button.style.display = "flex"; // Отображаем кнопку
        }
    });

}
document.addEventListener("DOMContentLoaded", () => {
    showButton();
});
window.showButton = showButton;