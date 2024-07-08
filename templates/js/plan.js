
let counter = 0;

document.getElementById('sub-procedure').addEventListener('change', function() {
    const subtype = this.value;
    proc = document.getElementById('procedure-select');
    const url = `/procedure/get/${proc.value}/${subtype}`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
        generateProcedureHTML(data);
    })
    .catch(error => {
        console.error('Error fetching procedure data:', error);
    });
});
document.getElementById('manual').addEventListener('click', function() {
    subtype_block = document.getElementById('sub-procedure');
    subtype_block.style.display = 'block';
});
document.getElementById('procedure-select').addEventListener('change', function() {
    const type = this.value;
    const url = `/procedure/subtype/${type}`;
    subtype_block = document.getElementById('sub-procedure');
    template_block = document.getElementById('template');
    template_block.style.display = 'block';
    manual_block = document.getElementById('manual');
    manual_block.style.display = 'block';


    fetch(url)
    .then(response => response.json())
    .then(data => {
        subtype_block.innerHTML = '<option value="None" disabled selected hidden>Выбрать поднаправление</option>';
        data.forEach((subtype) => {
              const subtype_option = document.createElement('option');
              subtype_option.value = subtype;
              subtype_option.textContent  = subtype;
              subtype_block.appendChild(subtype_option)
        })
    })
    .catch(error => {
        console.error('Error fetching procedure data:', error);
    });
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

function generateTemplateProcedureHTML(data) {
    const all_templates = document.getElementById('all_procedure');
    all_templates.innerHTML = '';

    Object.keys(data).forEach(key=> {
        const template = data[key];
        const procedureBlock = document.createElement('div');
        procedureBlock.className = 'template_procedure_block';
        procedureBlock

        const leftDiv = document.createElement('div');
        leftDiv.className = 'left';
        const columnDiv = document.createElement('div');
        columnDiv.className = 'column'

        const label = document.createElement('label');
        label.htmlFor = `template${key}`;
        label.textContent = template.name;
        columnDiv.appendChild(label);

        const change = document.createElement('a');
        change.htmlFor = 'template' + key;
        change.textContent = "Изменить";
        const currentProcedure = template.procedure;
        change.onclick = function() {
          open_template_procedure(currentProcedure, key, template.name);
        };
        change.style.cursor = 'pointer';
        columnDiv.appendChild(change);

        leftDiv.append(columnDiv)

        const rightDiv = document.createElement('div');
        rightDiv.className = 'right';

        const decrementButton = document.createElement('button');
        decrementButton.textContent = ' - ';
        decrementButton.onclick = () => decrement(key);
        rightDiv.appendChild(decrementButton);

        const numberDiv = document.createElement('div');
        numberDiv.id = `number${key}`;
        numberDiv.textContent = '0';
        rightDiv.appendChild(numberDiv);

        const incrementButton = document.createElement('button');
        incrementButton.textContent = ' + ';
        incrementButton.onclick = () => increment(key);
        rightDiv.appendChild(incrementButton);

        procedureBlock.appendChild(leftDiv);
        procedureBlock.appendChild(rightDiv);

        all_templates.appendChild(procedureBlock);
    });
}

function increment(id) {
    const numberElement = document.getElementById("number" + id);
    let currentNumber = parseInt(numberElement.innerText);
    numberElement.innerText = currentNumber + 1;
}

function decrement(id) {
    const numberElement = document.getElementById("number" + id);
    let currentNumber = parseInt(numberElement.innerText);
    if (currentNumber > 0) {
        numberElement.innerText = currentNumber - 1;
    }
}

function addTemplate() {
    const type = document.getElementById('procedure-select').value
    const url = "/procedure/template/get/" + type
    fetch(url)
    .then(response => response.json())
    .then(data => {
         generateTemplateProcedureHTML(data);
    })
    .catch(error => {
        console.error('Error fetching procedure data:', error);
    });
}

function open_template_procedure(data, template_id,template_name) {
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');
    document.getElementById('saveProcedures').onclick= function() {saveChanges(template_id);}
    modalBody.innerHTML = '';
    
    const label = document.createElement('input');
    label.id = 'template-name'
    label.className = 'modal-template-name'
    label.value=template_name;
    label.type="text";
    label.style.fontSize="25px;"
    modalBody.appendChild(label);

    data.forEach(item => {
        addField(item);
    });

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
    priceInput.type = 'number';
    if (item.id) {
        priceInput.id = `price${item.id}`
    } else{
        priceInput.id = `pricenew${counter}`;
    }
    priceInput.value = item.price || 0;
    priceInput.placeholder = 'Цена';
    rightDiv.appendChild(priceInput);

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

function saveChanges(template_id) {
    const fields = document.querySelectorAll('.procedure_block');
    console.log(fields)
    fields.forEach(field => {
        const id = field.getAttribute('id').split("-").pop();
        const name = field.querySelector(`#label${id}`).value;
        const price = field.querySelector(`#price${id}`).value;
        const amount = field.querySelector(`#amount${id}`).innerText;
        const type = document.getElementById('procedure-select').value;
        console.log(amount);
        if (id.startsWith('new')) {
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
    addTemplate();
}