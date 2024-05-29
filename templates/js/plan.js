document.getElementById('procedure-select').addEventListener('change', function() {
    const type = this.value;
    const url = `/procedure/${type}`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
        generateProcedureHTML(data);
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
