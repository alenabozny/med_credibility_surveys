const dialog = document.querySelector('dialog');
const showDialogButton = document.querySelector('#show-dialog');

showDialogButton.addEventListener('click', () => {
    dialog.showModal();
});

dialog.querySelector('.close').addEventListener('click', function() {
    dialog.close();
});


const saveBtn = document.querySelector('#save')

const time_start = new Date().toISOString();


saveBtn.addEventListener('click', async () => {
    const time_end = new Date().toISOString();
    const rate = "noncredible";

    const response = await fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            time_start,
            time_end,
            rate
        })
    });

    const { nextId } = await response.json();

    window.location.href = `/task/${nextId}`
});
