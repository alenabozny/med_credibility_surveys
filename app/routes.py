from flask import render_template
from flask import request, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm
from app.models import Task, User, CredibilityRates, SecondTask
from flask_login import current_user, login_user, login_required, logout_user
from datetime import datetime
from sqlalchemy import func, and_, not_

# 1. W zdaniu jest namowa do szkodliwego działania;
# 2. zdanie zawiera błędne dane liczbowe (np. 20% porodów w Ameryce kończy się cesarskim cięciem);
# 3. zdanie zawiera przedawnione informacje;
# 4. zdanie cytuje badania wykonane na bardzo małej próbie (badania wstępne, jeszcze nie potwierdzone na dużej próbie);
# 5. zdanie zawiera argument, który jest bardzo słaby/nieistotny w kontekście omawianego tematu (mimo że prawdziwy);
# 6. zdanie stanowi reklamę niesprawdzonego leku lub substancji albo niesprawdzonej terapii
# 7. autor zdania wykazuje braki wiedzy merytorycznej lub nie jest obiektywny
# 8. zdanie ma charakter anegdoty lub plotki
# 9. zdanie jest niezrozumiałe lub niegramatyczne

TAGS = [
    "namowa do szkodliwego działania",
    "zawiera błędne dane liczbowe",
    "przedawnione informacje",
    "cytuje badania wykonane na bardzo małej próbie",
    "zawiera argument, który jest bardzo słaby/nieistotny w kontekście omawianego tematu",
    "stanowi reklamę niesprawdzonego leku lub substancji albo niesprawdzonej terapii",
    "autor zdania wykazuje braki wiedzy merytorycznej lub nie jest obiektywny",
    "ma charakter anegdoty lub plotki",
    "jest niezrozumiałe lub niegramatyczne"
]

TAGS_2 = [
    "false",
    "slippery_slope", 
    "alleged_negative_consequences",
    "twisting_word",
    "hedging"
]

@app.route('/')
@app.route('/index')
@login_required
def index():
    tasks = Task.query.filter_by(
        user_id = current_user.id
    ).all()

    second_tasks = SecondTask.query.filter_by(
        user_id = current_user.id
    ).all()

    tasks_incomplete = Task.query.filter_by(
        user_id=current_user.id,
        rate=None
    ).all()

    second_tasks_incomplete = SecondTask.query.filter_by(
        user_id=current_user.id,
        rate=None
    ).all()

    completed_tasks_len = tasks.__len__() - tasks_incomplete.__len__()
    total_tasks_len = tasks.__len__()

    completed_second_tasks_len = second_tasks.__len__() - second_tasks_incomplete.__len__()
    total_second_tasks_len = second_tasks.__len__()

    nextTask = Task.query.filter_by(
        user_id=current_user.id,
        rate=None
    ).first()

    next_second_task = SecondTask.query.filter_by(
        user_id=current_user.id,
        rate=None
    ).first()

    return render_template(
        'index.html',
        title='Home',
        tasks=tasks,
        second_tasks=second_tasks,
        completed_tasks_len=completed_tasks_len,
        completed_second_tasks_len=completed_second_tasks_len,
        total_tasks_len=total_tasks_len,
        total_second_tasks_len=total_second_tasks_len,
        nextTask=nextTask,
        next_second_task=next_second_task
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

        if user and user.is_password_correct(password):
            login_user(user, remember=remember)
            return redirect("/")
        else:
            flash('Wrong username or password')

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
        task = Task.query.filter_by(task_id=task_id, user_id=current_user.id).first()

        if task.time_end:
            flash('Your task was expired')
            return redirect(url_for('index'))

        try:
            keywords = task.sentence.article.keywords.split(', ')
        except AttributeError:
            keywords = ""

        return render_template(
            'task.html',
            title='Task',
            sentences=task.sentence.get_context_sentences(),
            options=[e.value for e in CredibilityRates],
            sentence=task.sentence,
            keywords=keywords,
            tags=TAGS
        )
    if request.method == 'POST':
        time_start = request.form['time_start']
        time_end = request.form['time_end']
        rate = request.form['rate']
        steps = request.form['steps']
        tags = request.form.getlist('tag')
        reason = request.form['reason']

        task = Task.query.filter_by(task_id=task_id, user_id=current_user.id).first()
        task.time_start = datetime.fromtimestamp(int(time_start) / 1000)
        task.time_end = datetime.fromtimestamp(int(time_end) / 1000)
        task.rate = CredibilityRates(rate)
        task.tags = ','.join(tags)
        task.steps = int(steps)
        task.reason = reason

        db.session.commit()

        nextTask = Task.query.filter_by(
            user_id=current_user.id,
            rate=None
        ).order_by(func.random()).first()

        if nextTask:
            return redirect(url_for('perform_task', task_id=nextTask.task_id))
        else:
            flash('Thanks. You do not have any pending tasks')
            return redirect(url_for('index'))

@app.route('/second_task/<int:s_task_id>', methods=['GET', 'POST'])
@login_required
def perform_second_task(s_task_id):
    # return("Welcome to the second task round. Secondary Task Index: " + str(s_task_id))
    if request.method == 'GET':
        task = SecondTask.query.filter_by(s_task_id=s_task_id, user_id=current_user.id).first()

        if task.time_end:
            flash('Your task was expired')
            return redirect(url_for('index'))

        try:
            keywords = task.sentence.article.keywords.split(', ')
        except AttributeError:
            keywords = ""

        return render_template(
            'task.html',
            title='SecondTask',
            sentences=task.sentence.get_context_sentences(),
            options=["credible", 
                     "noncredible",
                     "neutral/irrelevant"],
            sentence=task.sentence,
            keywords=keywords,
            tags=TAGS_2
        )
    if request.method == 'POST':
        time_start = request.form['time_start']
        time_end = request.form['time_end']
        rate = request.form['rate']
        steps = request.form['steps']
        tags = request.form.getlist('tag')
        own_reason = request.form['reason']

        second_task = SecondTask.query.filter_by(s_task_id=s_task_id, user_id=current_user.id).first()
        second_task.time_start = datetime.fromtimestamp(int(time_start) / 1000)
        second_task.time_end = datetime.fromtimestamp(int(time_end) / 1000)
        second_task.rate = rate
        second_task.tags = ','.join(tags) if tags != [] else None
        second_task.steps = int(steps)
        second_task.own_reason = own_reason

        db.session.commit()

        nextTask = SecondTask.query.filter_by(
            user_id=current_user.id,
            rate=None
        ).order_by(func.random()).first()

        if nextTask:
            return redirect(url_for('perform_second_task', s_task_id=nextTask.s_task_id))
        else:
            flash('Thanks. You do not have any pending tasks')
            return redirect(url_for('index'))
