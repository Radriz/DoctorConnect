let clients = {};
let counter = 0;
let stageNumber = 1;
let initial_procedure_container;
//document.getElementById('sub-procedure').addEventListener('change', function() {
//    const subtype = this.value;
//    proc = document.getElementById('procedure-select');
//    const url = `/procedure/get/${proc.value}/${subtype}`;
//
//    fetch(url)
//    .then(response => response.json())
//    .then(data => {
//        generateProcedureHTML(data);
//    })
//    .catch(error => {
//        console.error('Error fetching procedure data:', error);
//    });
//});
//document.getElementById('manual').addEventListener('click', function() {
//    subtype_block = document.getElementById('sub-procedure');
//    subtype_block.style.display = 'block';
//});
function updateType(event) {
    const type = event.target.value;
    addTemplate(event.target.closest(".procedure-block"));
//    selected_elements = event.target
//    for (var i = 1; i < selected_elements.options.length; i++) {
//        let option = selected_elements.options[i];
//        if(option.value === type){
//            option.selected = true;
//        }else{
//            option.selected = false;
//        }
//    }
    };



//    const url = `/procedure/subtype/${type}`;
//    subtype_block = document.getElementById('sub-procedure');
//    template_block = document.getElementById('template');
//    template_block.style.display = 'block';
//    manual_block = document.getElementById('manual');
//    manual_block.style.display = 'block';
//
//
//    fetch(url)
//    .then(response => response.json())
//    .then(data => {
//        subtype_block.innerHTML = '<option value="None" disabled selected hidden>Выбрать поднаправление</option>';
//        data.forEach((subtype) => {
//              const subtype_option = document.createElement('option');
//              subtype_option.value = subtype;
//              subtype_option.textContent  = subtype;
//              subtype_block.appendChild(subtype_option)
//        })
//    })
//    .catch(error => {
//        console.error('Error fetching procedure data:', error);
//    });

document.getElementById('combobox').addEventListener('input',() => {
    const fio = document.querySelector('.fio').value;
    console.log('Имя и фамилия:', fio,fio in clients);
    if (fio in clients) {
        const birthday = clients[fio];
        document.getElementById('calendar').value = birthday;
        console.log('Дата рождения:', birthday);
        }});


document.getElementById('submit').addEventListener('click', async (event) => {
    event.preventDefault();
    const fio = document.querySelector('.fio').value;
    const birthday = document.getElementById('calendar').value;
    const stages = document.getElementById('stage');
    const procedureBlocks = stages.querySelectorAll('.procedure-block');
    let planId = null;

    try {
        // Create the plan
        const planResponse = await fetch('/plan/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'fio':fio , 'birthday': birthday }),
        });

        if (!planResponse.ok) {
            throw new Error('Ошибка при создании плана');
        }

        const planData = await planResponse.json();
        planId = planData.plan_id;

        // Create services for each procedure block
        for (let procedureBlock_i of procedureBlocks) {
            const stageName = procedureBlock_i.querySelector('#stage-name').value;
            let currentTooth = [];
            const buttons = procedureBlock_i.querySelectorAll('.tooth-selection button');
            buttons.forEach(button => {
                if(button.style.backgroundColor == "rgb(126, 247, 139)"){
                    currentTooth.push(button.innerText.trim())
                }
            });

            const templateProcedureBlocks = procedureBlock_i.querySelectorAll('.template_procedure_block');
            for (let tpb of templateProcedureBlocks) {
                const tpbId = tpb.id.split('_').at(-1);
                if (tpb.querySelector('#number' + tpbId) === null) {
                    continue;
                }
                const amount = tpb.querySelector('#number' + tpbId).textContent.trim();

                if (amount !== "0") {
                console.log({
                            stage: stageName,
                            template_id: parseInt(tpbId),
                            tooths: currentTooth.join(','),
                            plan_id: planId,
                            amount: parseInt(amount)
                        })
                    // Create service
                    const serviceResponse = await fetch('/plan/service/create', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            stage: stageName,
                            template_id: parseInt(tpbId),
                            tooths: currentTooth.join(','),
                            plan_id: planId,
                            amount: parseInt(amount)
                        })
                    });

                    if (!serviceResponse.ok) {
                        throw new Error('Ошибка при создании услуги');
                    }
                }
            }
            await fetch(`/plan/document/${planId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        }



        alert('План и услуги успешно созданы');
    } catch (error) {
        console.error(error);
        alert('Произошла ошибка при создании плана или услуг');
    }
});


function generateProcedureHTML(data) {
    const all_procedures = document.getElementById('all_procedure');
    all_procedures.innerHTML = '';

    data.procedure.forEach((procedure) => {
        const procedureBlock = document.createElement('div');
        procedureBlock.className = 'procedure_block';

        const leftDiv = document.createElement('div');
        leftDiv.className = 'left';

        const checkbox = document.createElement('input');
        checkbox.id = `procedure${procedure.id}`;
        checkbox.type = 'checkbox';
        leftDiv.appendChild(checkbox);

        const label = document.createElement('label');
        label.htmlFor = `procedure${procedure.id}`;
        label.textContent = procedure.name;
        leftDiv.appendChild(label);

        const rightDiv = document.createElement('div');
        rightDiv.className = 'right';

        const decrementButton = document.createElement('button');
        decrementButton.textContent = ' - ';
        decrementButton.onclick = () => decrement(procedure.id);
        rightDiv.appendChild(decrementButton);

        const numberDiv = document.createElement('div');
        numberDiv.id = `number${procedure.id}`;
        numberDiv.textContent = '0';
        rightDiv.appendChild(numberDiv);

        const incrementButton = document.createElement('button');
        incrementButton.textContent = ' + ';
        incrementButton.onclick = () => increment(procedure.id);
        rightDiv.appendChild(incrementButton);

        procedureBlock.appendChild(leftDiv);
        procedureBlock.appendChild(rightDiv);

        all_procedures.appendChild(procedureBlock);
    });
}

function generateTemplateProcedureHTML(stage, data) {
    const all_templates = stage.querySelector('#all_procedure');
    var stageCurrentNumber = stage.id.split("-").at(-1);
    all_templates.innerHTML = '<label class="label">Список медицинских услуг:</label>';
    Object.keys(data).forEach(key=> {
        const template = data[key];
        const procedureBlock = document.createElement('div');
        procedureBlock.className = 'template_procedure_block';
        procedureBlock.id = 'template_procedure_block_' + key;

        const leftDiv = document.createElement('div');
        leftDiv.className = 'left';
        const columnDiv = document.createElement('div');
        columnDiv.className = 'column'

        const label = document.createElement('label');
        label.htmlFor = `template${key}`;
        label.textContent = template.name;
        label.style.fontSize = "20px"
        columnDiv.appendChild(label);

        const change = document.createElement('a');
        change.textContent = "Изменить";
        const currentProcedure = template.procedure;
        change.onclick = function() {
          open_template_procedure(stage, currentProcedure, key, template.name);
        };
        change.style.cursor = 'pointer';
        columnDiv.appendChild(change);

        leftDiv.append(columnDiv)

        const rightDiv = document.createElement('div');
        rightDiv.className = 'right';


        const numberDiv = document.createElement('div');
        numberDiv.id = `number${key}`;
        numberDiv.textContent = '0';

        const decrementButton = document.createElement('button');
        decrementButton.textContent = ' - ';
        decrementButton.onclick = () => decrement(numberDiv);
        rightDiv.appendChild(decrementButton);

        rightDiv.appendChild(numberDiv);

        const incrementButton = document.createElement('button');
        incrementButton.textContent = ' + ';
        incrementButton.onclick = () => increment(numberDiv);
        rightDiv.appendChild(incrementButton);


        procedureBlock.appendChild(leftDiv);

        const stickerDiv = document.createElement('div')
        stickerDiv.className = "dropdown";
        const stickerButton = document.createElement('button');
        const dropdownContent = generateDropdownContent(stickerButton, key)
        stickerButton.onclick = () =>  dropdownContent.classList.toggle('show');
        stickerDiv.appendChild(stickerButton)
        stickerDiv.appendChild(dropdownContent)
        if (template.sticker != null){
             selectImage(stickerButton, dropdownContent, template.sticker, key)
        }else{
            selectImage(stickerButton, dropdownContent, "tooth", key)
        }

        procedureBlock.appendChild(stickerDiv)
        procedureBlock.appendChild(rightDiv);

        const price = document.createElement('label');
        price.htmlFor = `template${key}`;
        price.textContent = template.price + " руб.";
        price.style.marginBottom = "0px"
        price.style.fontSize = "30px"
        procedureBlock.appendChild(price);

        const removeButton = document.createElement('button');
        removeButton.className = 'remove-btn';
        removeButton.textContent = '×';
        removeButton.onclick = function() { removeTemplate(`${key}`, procedureBlock);}

        procedureBlock.appendChild(removeButton);

        all_templates.appendChild(procedureBlock);


    });
    const procedureBlock = document.createElement('div');
    procedureBlock.className = 'template_procedure_block';
    procedureBlock.innerHTML = 'Добавить медицинскую услугу'
    procedureBlock.style.cursor = 'pointer'
    procedureBlock.style.textAlign = 'center'
    procedureBlock.style.display = 'flex'
    procedureBlock.style.justifyContent = 'center'
    procedureBlock.onclick = function() {
          open_template_procedure(stage, null, 'new', "");
        };

    all_templates.appendChild(procedureBlock);

}

function increment(numberElement) {
    let currentNumber = parseInt(numberElement.innerText);
    numberElement.innerText = currentNumber + 1;
}

function decrement(numberElement) {
    let currentNumber = parseInt(numberElement.innerText);
    if (currentNumber > 0) {
        numberElement.innerText = currentNumber - 1;
    }
}

function addTemplate(document) {
    var stageCurrentNumber = document.id.split("-").at(-1);
    console.log(document)
    const type = document.querySelector('#procedure-select').value
    const url = "/procedure/template/get/" + type
    fetch(url)
    .then(response => response.json())
    .then(data => {
         generateTemplateProcedureHTML(document, data);
    })
    .catch(error => {
        console.error('Error fetching procedure data:', error);
    });
}

function open_template_procedure(stage, data, template_id,template_name) {
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');
    document.getElementById('saveProcedures').onclick= function() {saveChanges(stage, template_id);}
    modalBody.innerHTML = '';

    
    const label = document.createElement('input');
    label.placeholder = 'Введите название медицинской услуги'
    label.id = 'template-name'
    label.className = 'modal-template-name'
    label.value=template_name;
    label.type="text";
    label.style.fontSize="25px;"
    modalBody.appendChild(label);
    if (data == null){
        addField()
        console.log("Ок")
    }else{
     data.forEach(item => {
        addField(item);
    });
    }



    modal.style.display = "block";
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = "none";
}

function incrementTemplate(numberElement) {
    let currentNumber = parseInt(numberElement.innerText);
    numberElement.innerText = currentNumber + 1;
}

function decrementTemplate(numberElement) {
    let currentNumber = parseInt(numberElement.innerText);
    if (currentNumber > 0) {
        numberElement.innerText = currentNumber - 1;
    }
}

function addField(item = {}) {
    const modalBody = document.getElementById('modal-body');
    const procedureBlock = document.createElement('div');
    procedureBlock.className = 'procedure_block';
    if (item.id) {
        procedureBlock.id = `template-procedure-${item.id}`
    } else{
        procedureBlock.id = `template-procedure-new${counter}`;
    }

    const leftDiv = document.createElement('div');
    leftDiv.className = 'left';

    const label = document.createElement('input');
    if (item.id) {
        label.id = `label${item.id}`
    } else {
        label.id = `labelnew${counter}`;
    }
    label.type="text"
    label.placeholder = "Название процедуры"
    label.style.fontSize = "16px"
    label.value = item.name || '';
    label.style.marginBottom = "0px"
    leftDiv.append(label);

    const rightDiv = document.createElement('div');
    rightDiv.className = 'right';



    const numberDiv = document.createElement('div');
    if (item.id) {
        numberDiv.id = `amount${item.id}`;
    } else{
        numberDiv.id = `amountnew${counter}`;
    }
    numberDiv.textContent = item.amount || 1;

    const decrementButton = document.createElement('button');
    decrementButton.textContent = ' - ';
    decrementButton.onclick = () => decrementTemplate(numberDiv);
    rightDiv.appendChild(decrementButton);

    rightDiv.appendChild(numberDiv);

    const incrementButton = document.createElement('button');
    incrementButton.textContent = ' + ';
    incrementButton.onclick = () => incrementTemplate(numberDiv);
    rightDiv.appendChild(incrementButton);


    const priceInput = document.createElement('input');
    priceInput.style.fontSize = '16px';
    priceInput.style.marginBottom = "0px";
    priceInput.style.marginLeft = "20px";
    priceInput.style.width = "80px";
    priceInput.type = 'number';
    if (item.id) {
        priceInput.id = `price${item.id}`
    } else{
        priceInput.id = `pricenew${counter}`;
    }
    priceInput.value = item.price || 0;
    priceInput.placeholder = 'Цена';

    rightDiv.appendChild(priceInput);
    const rub = document.createElement('p');
    rub.textContent = 'руб.'
    rub.style.marginLeft = "4px";
    rightDiv.appendChild(rub);



    procedureBlock.appendChild(leftDiv);
    procedureBlock.appendChild(rightDiv);

    const removeButton = document.createElement('button');
    removeButton.className = 'remove-btn';
    removeButton.textContent = '×';
    if (item.id) {
        removeButton.onclick = function() { removeField(`${item.id}`, procedureBlock);}
    } else {
        removeButton.onclick = function() { removeField('new' + counter, procedureBlock); }
    }

    procedureBlock.appendChild(removeButton);

    modalBody.appendChild(procedureBlock);
}

function addNewField() {
    counter += 1;
    addField();
}

function removeField(id, fieldContainer) {
    console.log(id);
//    const fieldContainer = document.getElementById(`template-procedure-${id}`);

    if (!id.startsWith('new')) {
        fetch(`/procedure/user/${id}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                fieldContainer.remove();
            })
            .catch(error => console.error('Error:', error));
    } else {
        fieldContainer.remove();
    }
}
function removeTemplate(id, fieldContainer) {
    console.log(id);
    const fieldContainers = document.querySelectorAll(`#template_procedure_block_${id}`);


    fetch(`/procedure/template/${id}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            fieldContainers.forEach(fieldContainer => {
                fieldContainer.remove();
            })
        })
        .catch(error => console.error('Error:', error));
}

async function saveChanges(stage, temp_template_id) {
    var template_id = temp_template_id;
    const template_name = document.getElementById('template-name').value;

    if (template_id === 'new') {
        try {
            const response = await fetch(`/procedure/template/create/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ template_name: template_name })
            });
            const data = await response.json();
            console.log('Success:', data);
            template_id = data.id;
        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        try {
            const response = await fetch(`/procedure/template/${template_id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ template_name: template_name })
            });
            const data = await response.json();
            console.log('Success:', data);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    console.log('Updated template_id:', template_id);

    const fields = document.querySelectorAll('.procedure_block');
    fields.forEach(field => {
        const id = field.getAttribute('id').split("-").pop();
        const name = field.querySelector(`#label${id}`).value;
        const price = field.querySelector(`#price${id}`).value;
        const amount = field.querySelector(`#amount${id}`).innerText;
        const type = document.getElementById('procedure-select').value;
        console.log(amount);
        if (id.startsWith('new')) {
            console.log({ name, type, price: parseInt(price), template_id: template_id, amount: parseInt(amount) })
            fetch('/procedure/user/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, type, price: parseInt(price), template_id: template_id, amount: parseInt(amount) })
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch(error => console.error('Error:', error));
        } else {
            fetch(`/procedure/user/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, type, price: parseInt(price), template_id: template_id, amount: parseInt(amount) })
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch(error => console.error('Error:', error));
        }
    });

    closeModal();
    addTemplate(stage);

    const stageProcedureSelectValue = stage.querySelector(`#procedure-select`).value;

    // Получаем div с id 'stage'
    const stageElement = document.getElementById('stage');

    // Пробегаемся по каждому div внутри stage с классом 'procedure_block'
    const procedureBlocks = stageElement.querySelectorAll('.procedure-block');
    procedureBlocks.forEach(procedureBlock => {
        const procedureSelect = procedureBlock.querySelector(`#procedure-select`);
        console.log(`Stages: ${procedureSelect.value} ${stageProcedureSelectValue}`)
        if (procedureSelect && procedureSelect.value === stageProcedureSelectValue) {
            // Вызываем addTemplate для этого блока
            addTemplate(procedureBlock);
        }
    });
}

const imgArray = ["core_tab", "implant", "seal"]; // Array of image names
const dropdownContent = document.getElementById('dropdownContent');

// Function to generate dropdown content
function generateDropdownContent(button, template_id) {
    let dropdownContent = document.createElement('div');
    dropdownContent.id ="dropdownContent"
    dropdownContent.className="dropdown-content"
    imgArray.forEach(imgName => {
        const div = document.createElement('div');
        const img = document.createElement('img');
        img.src = `/images/stickers/${imgName}.png`;
        img.alt = `imgName`;
        img.onclick = () => selectImage(button, dropdownContent, imgName, template_id);
        div.appendChild(img);
        dropdownContent.appendChild(div);
    });
    return dropdownContent
}

// Function to handle image selection
async function selectImage(dropdownButton, dropdownContent, src, template_id) {
    dropdownButton.innerHTML = `<img src="/images/stickers/${src}.png" alt="src">`;
    dropdownContent.classList.remove('show');
    try {
            const response = await fetch(`/procedure/sticker/template`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ template_id: Number(template_id), sticker: src})
            });
            const data = await response.json();
            console.log('Success:', data);
        } catch (error) {
            console.error('Error:', error);
        }
}

document.addEventListener("DOMContentLoaded", async function () {
    initial_procedure_container = document.getElementById('procedure-container-1').innerHTML;
    var buttonTooth=document.querySelectorAll('.button-tooth')
    try {
            const response = await fetch(`/clients`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });
            const data = await response.json();
            console.log('Success:', data);
            template_id = data.id;
            data["clients"].forEach((client) => {
            clients[client.fio] = client.birthday;
            });
        } catch (error) {
            console.error('Error:', error);
        }
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
});

function addOrderBlock(){
    // Получаем все текущие элементы с выбранными значениями
    var all_procedures_selected = document.querySelectorAll('#procedure-select');
    var procedures_selected = [];

    all_procedures_selected.forEach((ps) => {
        procedures_selected.push(ps.value);
    });

    stageNumber += 1;
    console.log(stageNumber);

    // Создаем новый блок этапа
    var newProcedureBlock = document.createElement('div');
    newProcedureBlock.id = 'procedure-container-' + stageNumber;
    newProcedureBlock.className = 'procedure-block';
    newProcedureBlock.innerHTML = initial_procedure_container;

    // Добавляем новый блок в контейнер stages
    var stages = document.getElementById('stage');
    stages.appendChild(newProcedureBlock);

    // Повторно получаем элементы после добавления нового блока
    all_procedures_selected = document.querySelectorAll('#procedure-select');

    // Восстанавливаем выбранные значения
    for(var i = 0; i < procedures_selected.length; i++){
        all_procedures_selected[i].value = procedures_selected[i];
    }

    // Проверяем восстановленные значения в консоли
    for(var i = 0; i < procedures_selected.length; i++){
       console.log(all_procedures_selected[i].value);
    }

    // Привязываем обработчики событий только к новым кнопкам
    var newButtons = newProcedureBlock.querySelectorAll('.button-tooth');
    setTooth(newButtons);
}

function setTooth(buttonTooth){
    buttonTooth.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (this.style.backgroundColor == "rgb(126, 247, 139)"){
                this.style.backgroundColor = "transparent";
            } else {
                this.style.backgroundColor = "#7ef78b";
            }
            event.preventDefault();
       });
    });
}

function deleteOrderBlock(button) {
    var orderBlock = button.closest('.procedure-block');
    orderBlock.parentNode.removeChild(orderBlock);

}



