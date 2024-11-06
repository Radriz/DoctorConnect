document.addEventListener("DOMContentLoaded", () => {
    const addServiceBtn = document.getElementById("addServiceBtn");
    const saveServicesBtn = document.getElementById("saveServicesBtn");
    const servicesContainer = document.getElementById("servicesContainer");

    // Добавление новой услуги
    addServiceBtn.addEventListener("click", () => {
        createServiceItem();
    });

    // Сохранение всех услуг
    saveServicesBtn.addEventListener("click", (event) => {
        event.preventDefault();

        document.querySelectorAll(".service-item").forEach(item => {
            const name = item.querySelector("input[type='text']").value;
            const price = item.querySelector("input[type='number']").value;
            const id = item.id || -1;
            if (name && price) {

                service = { id:id, name:name, price:price };
                console.log(service);
                 fetch('/technik/service/edit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(service)
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                })
                .catch(error => {
                    console.error("Ошибка:", error);
                });
            }
        });
    });

    // Создание нового элемента услуги
    function createServiceItem(service = {}) {
        const serviceItem = document.createElement("div");
        serviceItem.classList.add("service-item");

        // Добавляем id услуги, если он есть
        if (service.id) {
            serviceItem.id = service.id;
        } else {
            serviceItem.id = '-1'
        }

        const serviceNameInput = document.createElement("input");
        serviceNameInput.setAttribute("type", "text");
        serviceNameInput.setAttribute("placeholder", "Название услуги");
        serviceNameInput.value = service.name || "";

        const servicePriceInput = document.createElement("input");
        servicePriceInput.setAttribute("type", "number");
        servicePriceInput.setAttribute("placeholder", "Цена");
        servicePriceInput.value = service.price || "";

        const deleteBtn = document.createElement("button");
        deleteBtn.classList.add("delete-btn");
        deleteBtn.innerText = "✕";

        // Обработчик удаления услуги
        deleteBtn.addEventListener("click", () => {serviceItem.remove()});

        serviceItem.appendChild(serviceNameInput);
        serviceItem.appendChild(servicePriceInput);
        serviceItem.appendChild(deleteBtn);
        servicesContainer.appendChild(serviceItem);
    }
});

function delete_service(id){
    const serviceItem = document.getElementById(id);
    fetch(`/technik/service/delete/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        serviceItem.remove();
    })
    .catch(error => {
        console.error("Ошибка:", error);
    });
}