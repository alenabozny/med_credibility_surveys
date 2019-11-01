from flask import render_template
from flask import request
from flask import redirect
from app import app
from app.forms import LoginForm
from app.models import Task, Sentence, User
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, login_required, logout_user

@app.route('/')

@app.route('/index')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all() #filtrowac po niewypelnionych zadaniach
    return render_template(
        'index.html',
        title='Home',
        tasks=tasks
    )

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', title='Sign In', form=form)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember_me') else False


        user = User.query.filter_by(username=username).first()


        if not user or not check_password_hash(user.password_hash, password):
            print("nie ok " + generate_password_hash('test'))
        else:
            print("loguje")
            login_user(user, remember=remember)
            return redirect("/")

        return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def perform_task(task_id):
    if request.method == 'GET':
        task = Task.query.filter_by(task_id=task_id, user_id=current_user.id)
        sentence = Sentence.query.filter_by(sentence_id=task.first().sentence_id).first()
        sentences = Sentence.query.filter_by(sentence_id=task.first().sentence_id).all()


        # KW: Totalnie nie rozumiem jak pobrac liste zdan dla tasku. potrzebuje by doladowywac kolejne.
        sentencesList = []
        for sentence in sentences:
            sentencesList.append({ sentence.sequence_nr: sentence.body})

        return render_template(
            'example_task.html',
            title='Task',
            sentences=sentencesList,
            sentence=sentence,
            keywords=(',').join(['keywords1', 'keywords2', 'keywords3']) #TODO skad pobierac slowa kluczowe ?
        )
    if request.method == 'POST':
        content = request.json

        time_start = content['time_start'] #iso string
        time_end = content['time_end'] # iso string
        rate = content['rate'] # string

        # TODO Zapisac do bazy zwrotke
        # TODO Do response dodac id kolejnego zadania

        resp = jsonify(nextId=2)
        return resp

