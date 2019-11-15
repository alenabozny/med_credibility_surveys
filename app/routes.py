from flask import render_template
from flask import request, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm
from app.models import Task, User, CredibilityRates
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, login_required, logout_user
from datetime import datetime

TAGS = ['tag1', 'tag2', 'tag3']

@app.route('/')
@app.route('/index')
@login_required
def index():
    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).filter(Task.rate != None).all()

    nextTask = Task.query.filter_by(
        user_id=current_user.id,
        rate=None
    ).first()

    return render_template(
        'index.html',
        title='Home',
        tasks=tasks,
        nextTask=nextTask
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

        if user and check_password_hash(user.password_hash, password):
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
        ).first()

        if nextTask:
            return redirect(url_for('perform_task', task_id=nextTask.task_id))
        else:
            flash('Thanks. You do not have any pending tasks')
            return redirect(url_for('index'))
