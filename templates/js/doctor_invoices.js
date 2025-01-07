
function pay_invoice(id){
    fetch(`/doctor/invoice/pay/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        window.location.reload();
    })
    .catch(error => {
        alert("Не удалось оплатить счет, возможно он уже был оплачен")
        console.error("Ошибка:", error);
    });
}

async function showDetails(invoiceId) {
    const detailsRow = document.getElementById(`details-${invoiceId}`);
    const detailsContent = detailsRow.querySelector('.details-content');

    if (detailsRow.style.display === 'table-row') {
        detailsRow.style.display = 'none';
        return;
    }

    detailsRow.style.display = 'table-row';

    try {
        const response = await fetch(`/technik/invoice/${invoiceId}/orders`);
        if (!response.ok) {
            throw new Error('Ошибка загрузки данных');
        }

        const data = await response.json();
        const orders = data.orders;

        let detailsHTML = '<table><tr><th>ФИО пациента</th><th>Зубная формула</th><th>Вид работы</th><th>Цена</th><th>Подробнее</th></tr>';
        for (const order of orders) {
            detailsHTML += `
                <tr>
                    <td>${order.patient}</td>
                    <td>
                        <table class="tooth-formula">
                            <tr>
                                <td>${filterTooth(order.formula, 1)}</td>
                                <td>${filterTooth(order.formula, 2)}</td>
                            </tr>
                            <tr>
                                <td>${filterTooth(order.formula, 3)}</td>
                                <td>${filterTooth(order.formula, 4)}</td>
                            </tr>
                        </table>
                    </td>
                    <td>${order.type}</td>
                    <td>${order.price} руб.</td>
                    <td><a href="/order/get/${order.id}">Подробнее</a></td>
                </tr>`;
        }
        detailsHTML += '</table>';

        detailsContent.innerHTML = detailsHTML;
    } catch (error) {
        detailsContent.innerHTML = '<p>Ошибка загрузки данных.</p>';
    }
}

function filterTooth(toothString, quarter) {
    const teeth = toothString.split(',').map(num => num.trim());
    const multiplier = {
        1: -1,
        2: 1,
        3: -1,
        4: 1,
    };
    const quarters = {
        1: Array.from({ length: 8 }, (_, i) => 11 + i), // Верхняя правая
        2: Array.from({ length: 8 }, (_, i) => 21 + i), // Верхняя левая
        3: Array.from({ length: 8 }, (_, i) => 41 + i), // Нижняя левая
        4: Array.from({ length: 8 }, (_, i) => 31 + i), // Нижняя правая
    };
    const quarterTeeth = teeth.filter(tooth => quarters[quarter].includes(parseInt(tooth, 10)))
                              .sort((a, b) => multiplier[quarter] * (parseInt(a, 10) - parseInt(b, 10)));
    return quarterTeeth.join(' ');
}
