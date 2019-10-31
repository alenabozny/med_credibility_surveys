from flask import render_template
from flask import jsonify
from app import app
from app.forms import LoginForm
from app.models import Task, Sentence

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
def perform_task(task_id):
    task = Task.query.filter_by(task_id=task_id)
    sentence = Sentence.query.filter_by(sentence_id=task.first().sentence_id).first()

    return render_template(
        'example_task.html',
        title='Task',
        sentences=['s1', 's2', 's3'],
        sentence=sentence,
        keywords=(',').join(['keywords1', 'keywords2', 'keywords3'])
    )
