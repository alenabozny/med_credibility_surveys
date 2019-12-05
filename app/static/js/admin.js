
let isChecked = false;
const elements = Array.from(document.querySelectorAll('#sentences input'));

document.querySelector('#toggleAll').addEventListener('click', (e) => {
    e.preventDefault();
    isChecked = !isChecked;
    elements
        .filter(element => !element.disabled)
        .forEach(element => element.checked = isChecked);
});


document.querySelector('#every2').addEventListener('click', (e) => {
    e.preventDefault();
    elements
        .forEach((element, index) => {
            if (!element.disabled) {
                element.checked = index % 2 === 0
            }
        });
});


document.querySelector('#every3').addEventListener('click', (e) => {
    e.preventDefault();
    elements
        .forEach((element, index) => {
            if (!element.disabled) {
                element.checked = index % 3 === 0
            }
        });
});


disabledOptions.forEach(option => document.querySelector(`[type="checkbox"][value="${option}"]`).disabled = true);
checkedOptions.forEach(option => document.querySelector(`[type="checkbox"][value="${option}"]`).checked= true);
