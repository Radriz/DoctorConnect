var buttonTooth=document.querySelectorAll('.button-tooth')
var submitButton=document.getElementById('submit')
async function submit() {
    var orderBlocks = document.querySelectorAll('.order-block')
    fio = document.getElementById('fio');
    if (fio.value == "") {
        alert('Введите имя и фамилию пациента');
        return;
    }
    orderBlocks.forEach( async function(orderBlock){
        console.log(orderBlock)
        var toothNumbers = []
        buttonTooth = orderBlock.querySelectorAll('.button-tooth')
        buttonTooth.forEach(function(button){
            if(button.style.backgroundColor == "rgb(126, 247, 139)"){
                toothNumbers.push(button.innerText.trim())
            }
        });
        tooths = toothNumbers.join(", ");
        tech = document.getElementById('technik');
        type = orderBlock.querySelector('#type');
        color_letter = orderBlock.querySelector('#color_letter');
        color_number = orderBlock.querySelector('#color_number');
        text = orderBlock.querySelector('#text');
        date_fitting = orderBlock.querySelector('#date_fitting');
        date_deadline = orderBlock.querySelector('#date_deadline');
        data = {
         "patient" : fio.value,
         "formula" : tooths,
         "type" : type.value,
         "comment" : text.value,
         "fitting" : date_fitting.value,
         "deadline" : date_deadline.value,
         "technik" : tech.value,
         "color_letter" : color_letter.value,
         "color_number" : color_number.value,
        }
        console.log(data)
        try{
            const response = await fetch("/order/create", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(data),
            });

            const result = await response.json();
            console.log("Success:", result);
            alert("Заказ отправлен успешно")
            window.location.href = "/account"
        } catch (error) {
            console.error("Error:", error);
        }
    });
}
submitButton.addEventListener('click', submit);

let orderContainerInnerHtml;


document.addEventListener('DOMContentLoaded', function() {
    var orderContainer = document.getElementById('order-container');
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
    newOrderBlock.innerHTML = orderContainerInnerHtml;
    buttonTooth=newOrderBlock.querySelectorAll('.button-tooth')
    console.log(buttonTooth)
    setTooth(buttonTooth)



    container.insertBefore(newOrderBlock, document.getElementById('add-order'));
}

const today = new Date();
const formattedDate = today.toISOString().split('T')[0];
document.getElementById('date_fitting').setAttribute('min', formattedDate);
document.getElementById('date_deadline').setAttribute('min', formattedDate);

