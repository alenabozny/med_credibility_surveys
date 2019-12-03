
let isChecked = false;
const elements = document.querySelectorAll('#sentences input');

document.querySelector('#toggleAll').addEventListener('click', (e) => {
    e.preventDefault();
    isChecked = !isChecked;
    elements.forEach(element => element.checked = isChecked);
});


document.querySelector('#every2').addEventListener('click', (e) => {
    e.preventDefault();
    elements.forEach((element, index) => element.checked = index % 2 === 0);
});


document.querySelector('#every3').addEventListener('click', (e) => {
    e.preventDefault();
    elements.forEach((element, index) => element.checked = index % 3 === 0);
});
