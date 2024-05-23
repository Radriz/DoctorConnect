var buttonTooth=document.querySelectorAll('.button-tooth')
var toothNumbers=[]
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
