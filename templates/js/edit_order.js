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
        img = this.querySelector('img');

        if(this.style.backgroundColor == "rgb(126, 247, 139)"){
            this.style.backgroundColor = "transparent";
            tooth_number = this.innerText.trim()
            if (img.src.includes('/images/missing_tooth.png')){
                tooth_number = "0"+tooth_number;
            }
            const index = toothNumbers.indexOf(tooth_number);
            toothNumbers.splice(index,1);
        } else{
            this.style.backgroundColor = "#7ef78b";
            tooth_number = this.innerText.trim()
            if (img.src.includes('/images/missing_tooth.png')){
                tooth_number = "0"+tooth_number;
            }
            toothNumbers.push(tooth_number);
        }
        console.log(toothNumbers);
        event.preventDefault();
   });
    button.addEventListener('dblclick', function(event) {
       img = this.querySelector('img');
       tooth_number = parseInt(this.textContent)
       console.log(img.src, tooth_number);

       if(!img.src.includes('/images/missing_tooth.png') ){
             img.src = "/images/missing_tooth.png";
            const index = toothNumbers.indexOf(tooth_number);
            toothNumbers.splice(index,1);
            toothNumbers.push("0"+tooth_number);
       } else if(tooth_number % 10 > 0 && tooth_number % 10 <6 ) {
             img.src = "/images/incisor.png";
             const index = toothNumbers.indexOf("0"+tooth_number);
            toothNumbers.splice(index,1);
            toothNumbers.push(tooth_number);
       } else {
             img.src = "/images/tooth.png";
             const index = toothNumbers.indexOf("0"+tooth_number);
            toothNumbers.splice(index,1);
            toothNumbers.push(tooth_number);
       }})
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
            img = button.querySelector('img');
            tooth_number = button.innerText.trim()
            if (img.src.includes('/images/missing_tooth.png')){
                tooth_number = "0"+tooth_number;
            }
            toothNumbers.push(tooth_number)
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
function savePhotos(){
    const order_id = window.location.href.split('/').filter(Boolean).pop();
    const formData = new FormData();
    for (let i = 0; i < fileList.length; i++) {
        formData.append('photos', fileList[i]);
    }

    console.log(formData);

    return fetch(`/order/photo/upload/${order_id}`, {
        method: 'POST',
        body: formData
    })
    .then(uploadResponse => {
        if (!uploadResponse.ok) {
            throw new Error('Upload failed');
        }
        return uploadResponse.json();
    })
    .then(uploadResult => {
        console.log('Upload successful:', uploadResult);
    })
    .catch(uploadError => {
        console.error('Error uploading photos:', uploadError);
    });
}
const today = new Date();
const formattedDate = today.toISOString().split('T')[0];
document.getElementById('date_fitting').setAttribute('min', formattedDate);
document.getElementById('date_deadline').setAttribute('min', formattedDate);