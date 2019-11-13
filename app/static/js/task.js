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

const tags = document.querySelector('#tags');
const checkboxes = document.querySelectorAll('[name="rate"]');

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
        if (e.target.id === 'noncredible') {
            tags.classList.remove('hide');
        } else {
            tags.classList.add('hide');
            tags.querySelectorAll('input').forEach(checkbox => checkbox.checked = false)
        }
        saveBtn.removeAttribute('disabled');
    })
});


let context_index = 1;

let renderSentences = [{
    txt: initSentence,
    first: true
}];

const sentenceBody = document.querySelector('#sentenceBody');

const sentencesToHTML = (sentences) => {
    const box = document.createElement('div');

    sentences.forEach(sentence => {
        const sBox = document.createElement('p');

        if (sentence.first) {
            sBox.classList.add('main-sentence');
        }

        sBox.innerText = sentence.txt;
        box.appendChild(sBox);
    });

    sentenceBody.innerHTML = "";
    sentenceBody.appendChild(box);
};

sentencesToHTML(renderSentences);

document.querySelector('#moreContext').addEventListener('click', (e) => {
    e.preventDefault();
    const next = sentences[context_index];
    if(next) {
        const {left, right} = next;

        if (left) {
            renderSentences = [{
                txt: left
            }, ...renderSentences];
        }

        if (right) {
            renderSentences = [...renderSentences, {
                txt: right
            }];
        }

        context_index += 1;
        document.querySelector('[name="steps"]').value = context_index;
        sentencesToHTML(renderSentences);
        if (!sentences[context_index]) {
            e.currentTarget.disabled = true;
        }
    }
});
