var buttonTooth=document.querySelectorAll('.button-tooth')
var submitButton=document.getElementById('submit')
let counter = 1;
let fileList = {}
fileList[counter] = [];

async function submit() {
    var orderBlocks = document.querySelectorAll('.order-block');
    var fio = document.getElementById('fio');

    if (fio.value == "") {
        alert('Введите имя и фамилию пациента');
        return;
    }

    // Show loading overlay
    document.getElementById('loading-overlay').style.display = 'flex';

    var promises = [];

    orderBlocks.forEach(function(orderBlock) {
        var toothNumbers = [];
        var buttonTooth = orderBlock.querySelectorAll('.button-tooth');

        buttonTooth.forEach(function(button) {
            if (button.style.backgroundColor == "rgb(126, 247, 139)") {
                toothNumbers.push(button.innerText.trim());
            }
        });

        var tooths = toothNumbers.join(", ");
        var tech = document.getElementById('technik');
        var type = orderBlock.querySelector('#type');
        var color_letter = orderBlock.querySelector('#color_letter');
        var color_number = orderBlock.querySelector('#color_number');
        var text = orderBlock.querySelector('#text');
        var date_fitting = orderBlock.querySelector('#date_fitting');
        var date_deadline = orderBlock.querySelector('#date_deadline');
        type_and_price = type.value.split('|')
        console.log(type_and_price)
        var data = {
            "patient": fio.value,
            "formula": tooths,
            "type": type_and_price[0],
            "price": type_and_price[1],
            "comment": text.value,
            "fitting": date_fitting.value,
            "deadline": date_deadline.value,
            "technik": tech.value,
            "color_letter": color_letter.value,
            "color_number": color_number.value
        };

        console.log(data);

        var orderPromise = fetch("/order/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then(async response => {
            if (!response.ok) throw new Error('Failed to create order');
            const result = await response.json();
            console.log("Success:", result);
            const order_id = result.order_id;

            if (fileList[orderBlock.id]) {
                const formData = new FormData();
                for (let i = 0; i < fileList[orderBlock.id].length; i++) {
                    formData.append('photos', fileList[orderBlock.id][i]);
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
        })
        .catch(orderError => {
            console.error("Error:", orderError);
        });

        promises.push(orderPromise);
    });

    Promise.all(promises)
    .then(() => {
        document.getElementById('loading-overlay').style.display = 'none';
        window.location.href = "/account";
    })
    .catch(error => {
        console.error("Error in processing orders:", error);
    })
    .finally(() => {
        // Hide loading overlay
        document.getElementById('loading-overlay').style.display = 'none';
    });
}


submitButton.addEventListener('click', submit);

let orderContainerInnerHtml;


document.addEventListener('DOMContentLoaded', function() {
    var orderContainer = document.getElementById('order-container-1');
    orderContainerInnerHtml = orderContainer.innerHTML;
});

function setTooth(buttonTooth){
    buttonTooth.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if(this.style.backgroundColor == "rgb(126, 247, 139)"){
                this.style.backgroundColor = "transparent";;
            } else{
                this.style.backgroundColor = "#7ef78b";
            }
            event.preventDefault();
       });
    });
}

setTooth(buttonTooth)

function selectBottomRow(button) {
     var orderBlock = button.closest('.order-block');
     const allBottomTooth = orderBlock.querySelector('#bottom-tooth').querySelectorAll('button');
     let allSelected = true;
     allBottomTooth.forEach((bt) => {
          if (bt.style.backgroundColor != "rgb(126, 247, 139)"){
              allSelected = false;
          }
     });
     allBottomTooth.forEach((bt) => {
          if (allSelected){
              bt.style.backgroundColor = "transparent";
          } else {
              bt.style.backgroundColor = "#7ef78b";
          }
     });
}
function selectTopRow(button) {
     var orderBlock = button.closest('.order-block');
     const allTopTooth = orderBlock.querySelector('#top-tooth').querySelectorAll('button');
     let allSelected = true;
     allTopTooth.forEach((bt) => {
          if (bt.style.backgroundColor != "rgb(126, 247, 139)"){
              allSelected = false;
          }
     });
     allTopTooth.forEach((bt) => {
          if (allSelected){
              bt.style.backgroundColor = "transparent";
          } else {
              bt.style.backgroundColor = "#7ef78b";
          }
     });
}
function deleteOrderBlock(button) {
    var orderBlock = button.closest('.order-block');
    orderBlock.parentNode.removeChild(orderBlock);
}

function addOrderBlock() {
    var container = document.querySelector('.plan');
    var newOrderBlock = document.createElement('div');
    newOrderBlock.classList.add('order-block');
    counter += 1;
    newOrderBlock.id = 'order-block-' + counter;
    fileList['order-block-' + counter] = []
    newOrderBlock.innerHTML = orderContainerInnerHtml;
    buttonTooth=newOrderBlock.querySelectorAll('.button-tooth');
    console.log(buttonTooth)
    setTooth(buttonTooth)
    container.insertBefore(newOrderBlock, document.getElementById('add-order'));
}

const today = new Date();
const formattedDate = today.toISOString().split('T')[0];
document.getElementById('date_fitting').setAttribute('min', formattedDate);
document.getElementById('date_deadline').setAttribute('min', formattedDate);

function handleFileChange(event){
    const orderBlock = event.target.closest('.order-block');
    const textFiles = orderBlock.querySelector('.input-file-text');
    textFiles.innerHTML = '';
    let size = 0
    fileList[orderBlock.id] = [];
    Array.from(event.target.files).forEach((file) => {
        fileList[orderBlock.id].push(file);
        size += file.size / 1024 / 1024;
	    textFiles.textContent += file.name + ", "
    });
    textFiles.textContent.slice(0, -1) + '.';
    console.log(size)
    if (size > 50){
        textFiles.textContent = 'Превышен допустимый размер файлов(до 50мб) ';
        fileList[orderBlock.id] = [];
    }
}

$(document).ready(function() {
  $('#technik').select2({
    placeholder: 'Выберите техника',
    allowClear: true
  }).val(null).trigger('change');
  // Применение стиля к select2
  $('.select2-selection').css({
    'width': '100%',
    'max-width': '500px',
    'padding': '10px',
    'border': '1px solid #ccc',
    'border-radius': '5px',
    'font-size': '18px',
    'box-sizing': 'border-box',
    'height':'auto'
  });

  $('.select2-container').css({
    'width': '100%',
    'max-width': '500px'
  });
  $('.select2-selection__arrow').css({
    'height': '100%',
    'display': 'flex',
    'align-items': 'center',
    'justify-content': 'center'
  });
  $('#technik').on('select2:open', function() {
    $('.select2-search__field').css({
      'font-size': '20px',
      'padding': '10px'
    });
  });
  $('#technik').on('change', function() {
    const selectedValue = $(this).val();
    console.log('Выбранное значение:', selectedValue);
    fetch('/technik/service/get/'+ selectedValue, {
        method: 'get',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        $('#type').empty();
        data.services.forEach(service => {
            $('#type').append(new Option(`${service.name} - ${service.price} руб.`, `${service.name}|${service.price}` ))
        })
        $('#type').append(new Option('Другое - цена договорная', -1 ))

        console.log(data);
    })
    .catch(error => {
        console.error("Ошибка:", error);
    });
  });
});

