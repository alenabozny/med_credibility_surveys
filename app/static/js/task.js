const dialog = document.querySelector('dialog');
const showDialogButton = document.querySelector('#show-dialog');

showDialogButton.addEventListener('click', (e) => {
    e.preventDefault();
    dialog.showModal();
});

dialog.querySelector('.close').addEventListener('click', function() {
    dialog.close();
});

const saveBtn = document.querySelector('#save');

document.querySelector('[name="time_start"]').value = Date.now();


saveBtn.addEventListener('click', async () => {
    document.querySelector('[name="time_end"]').value = Date.now();
});


const checkboxes = document.querySelectorAll('[name="rate"]');

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        saveBtn.removeAttribute('disabled');
    })
});

document.querySelector('#moreContext').addEventListener('click', (e) => {
    e.preventDefault();
    console.log('more cpontext');
})
