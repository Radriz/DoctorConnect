var fittingCheckBox = document.getElementById('fitting_done');
var doneCheckBox = document.getElementById('done');
var fileList = []

fittingCheckBox.addEventListener('change', function() {
document.getElementById('fitting_done_form').submit();
});
doneCheckBox.addEventListener('change', function() {
document.getElementById('done_form').submit();
});

async function update_price() {
    var price = document.getElementById('price').value;
    var comment = document.getElementById('technik_comment').value;
    console.log(comment);
    try {
        const order_id = window.location.href.split('/').filter(Boolean).pop();
        const response = await fetch(
            `/order/price/${order_id}?price=${parseInt(price)}&comment=${comment}`,  // Добавляем price как query параметр
            {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' }
            }
        );

        const data = await response.json();
        console.log('Success:', data);
        await saveFiles();

        window.location.reload();
    } catch (error) {
        console.error('Error:', error);
    }
}
function deleteFile(photoName) {
    event.preventDefault();
    fetch(`/order/technik/file/delete/${photoName}`, {
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

async function saveFiles(){
    const order_id = window.location.href.split('/').filter(Boolean).pop();
    const formData = new FormData();
    for (let i = 0; i < fileList.length; i++) {
        formData.append('files', fileList[i]);
    }

    console.log(formData);
    if(fileList.length === 0){
        return;
    }

    return fetch(`/order/technik/file/upload/${order_id}`, {
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