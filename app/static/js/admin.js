
const selectElement = document.querySelector('#article');
const sentenceContainer = document.querySelector('#sentenceContainer tbody');
let checkboxes = [];

selectElement.addEventListener('change', async (e) => {
    const value = e.target.value;

    const req = await fetch(`/admin/article/${value}/sentences`);
    const data = await req.json();
    checkboxes = [];

    sentenceContainer.innerHTML = "";
    data.forEach(sentence => {
        const tr = document.createElement('tr');
        const td1 = document.createElement('td');
        const td2 = document.createElement('td');
        const td3 = document.createElement('td');
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'article[]';
        checkbox.value = sentence.sentence_id;
        checkbox.checked = true;

        td1.appendChild(checkbox);
        td2.innerText = sentence.sentence_id;
        td3.innerText = sentence.body;

        tr.addEventListener('click', () => {
           checkbox.checked = !checkbox.checked;
        });
        checkboxes.push(checkbox);

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        sentenceContainer.appendChild(tr);
    });
});

document.querySelector('#btnNone').addEventListener('click', (e) => {
    checkboxes.forEach(checkbox => checkbox.checked = false);
    e.preventDefault();
});

document.querySelector('#btnAll').addEventListener('click', (e) => {
    checkboxes.forEach(checkbox => checkbox.checked = true);
    e.preventDefault();
});

document.querySelector('#btnEvery2').addEventListener('click', (e) => {
    checkboxes.forEach((checkbox, index) => checkbox.checked = index % 2 === 0);
    e.preventDefault();
});

document.querySelector('#btnEvery3').addEventListener('click', (e) => {
    checkboxes.forEach((checkbox, index) => checkbox.checked = index % 3 === 0);
    e.preventDefault();
});
