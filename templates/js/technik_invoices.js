
function delete_invoice(id){
    fetch(`/technik/invoice/delete/${id}`, {
        method: 'DELETE',
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
        console.error("Ошибка:", error);
    });
}