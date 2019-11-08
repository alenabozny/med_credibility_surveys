from flask import render_template
from flask import request, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm, RegisterForm, ChangePasswordForm
from app.models import Task, User, CredibilityRates
from werkzeug.security import generate_password_hash, check_password_hash
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

        return render_template(
            'example_task.html',
            title='Task',
            sentences=task.sentence.get_context_sentences(),
            options=[e.value for e in CredibilityRates],
            sentence=task.sentence,
            keywords=task.sentence.article.keywords.split(', '),
            tags=TAGS
        )
    if request.method == 'POST':
        time_start = request.form['time_start']
        time_end = request.form['time_end']
        rate = request.form['rate']
        steps = request.form['steps']

        task = Task.query.filter_by(task_id=task_id, user_id=current_user.id).first()
        task.time_start = datetime.fromtimestamp(int(time_start) / 1000)
        task.time_end = datetime.fromtimestamp(int(time_end) / 1000)
        task.rate = CredibilityRates(rate)
        task.steps = int(steps)

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


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect("/")

    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate():
            username = request.form['username']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])

            user = User(username=username, email=email, password_hash=password)
            db.session.add(user)
            db.session.commit()
            flash('User was added')
        else:
            flash('bad form data')

    users = User.query.outerjoin(Task).all()

    return render_template('admin.html', title='Admin', users=users, form=form)


@app.route('/admin/remove/<int:user_id>')
@login_required
def remove_user(user_id):
    if not current_user.is_admin:
        return redirect("/")

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('User was deleted')
    return redirect(url_for('admin'))


@app.route('/admin/toggle_admin/<int:user_id>')
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        return redirect("/")

    user = User.query.filter_by(id=user_id).first()
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('Admin role chaned')
    return redirect(url_for('admin'))


@app.route('/admin/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_details(user_id):
    if not current_user.is_admin:
        return redirect("/")

    form = ChangePasswordForm(request.form)
    user = User.query.filter_by(id=user_id).outerjoin(Task).first()

    if not user:
        flash('User not found')
        return redirect(url_for('admin'))

    if request.method == 'POST':
        if form.validate():
            password = generate_password_hash(request.form['password'])
            user.password_hash = password
            db.session.commit()
            flash('Password changed')

    return render_template('user_admin.html', title=user.username, user=user, form=form)
