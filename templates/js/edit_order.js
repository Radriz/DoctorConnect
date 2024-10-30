var buttonTooth=document.querySelectorAll('.button-tooth')
var toothNumbers=[]
var fileList = []
var submitButton=document.getElementById('submit')
submitButton.addEventListener('click', function() {
    var orderForm=document.getElementById('order_form');
    var inputArray = document.createElement('input');
    inputArray.type = 'hidden';
    inputArray.name = 'formula';
    inputArray.value = toothNumbers.join(", ")
    orderForm.appendChild(inputArray);
    orderForm.submit();

});

buttonTooth.forEach(function(button) {
    button.addEventListener('click', function(event) {
        if(this.style.backgroundColor == "rgb(126, 247, 139)"){
            this.style.backgroundColor = "transparent";
            const index = toothNumbers.indexOf(this.innerText.trim());
            toothNumbers.splice(index,1);
        } else{
            this.style.backgroundColor = "#7ef78b";
            toothNumbers.push(this.innerText.trim())
        }
        console.log(toothNumbers);
        event.preventDefault();
   });
});

function deletePhoto(photoName) {
    event.preventDefault();
    fetch(`/order/photo/delete/${photoName}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert('Failed to delete photo');
        }
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    buttonTooth.forEach(function(button) {
        console.log(button.style.backgroundColor);
        if (button.style.backgroundColor == "rgb(126, 247, 139)"){
         toothNumbers.push(button.innerText.trim())
        }
    });
});
function handleFileChange(event){
    const textFiles = document.querySelector('.input-file-text');
    textFiles.innerHTML = '';
    let size = 0
    fileList = [];
    Array.from(event.target.files).forEach((file) => {
        fileList.push(file);
        size += file.size / 1024 / 1024;
	    textFiles.textContent += file.name + ", "
    });
    textFiles.textContent.slice(0, -1) + '.';
    console.log(size)
    if (size > 50){
        textFiles.textContent = 'Превышен допустимый размер файлов(до 50мб) ';
        fileList = [];
    }
}

const today = new Date();
const formattedDate = today.toISOString().split('T')[0];
document.getElementById('date_fitting').setAttribute('min', formattedDate);
document.getElementById('date_deadline').setAttribute('min', formattedDate);