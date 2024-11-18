var fittingCheckBox = document.getElementById('fitting_done');
var doneCheckBox = document.getElementById('done');

fittingCheckBox.addEventListener('change', function() {
document.getElementById('fitting_done_form').submit();
});
doneCheckBox.addEventListener('change', function() {
document.getElementById('done_form').submit();
});

async function update_price() {
    var price = document.getElementById('price').value;
    try {
        const order_id = window.location.href.split('/').filter(Boolean).pop();
        const response = await fetch(
            `/order/price/${order_id}?price=${parseInt(price)}`,  // Добавляем price как query параметр
            {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' }
            }
        );

        const data = await response.json();
        console.log('Success:', data);
        window.location.reload();
    } catch (error) {
        console.error('Error:', error);
    }
}