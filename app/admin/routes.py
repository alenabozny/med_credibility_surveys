from flask import render_template, url_for
from flask import request, redirect, flash
from sqlalchemy import null
from app import db
from app.admin import bp_admin
from app.admin.forms import UserTaskForm, ChangePasswordForm
from app.forms import RegisterForm
from app.models import Task, User, Article, Sentence
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_required


@bp_admin.route('/')
@bp_admin.route('/index', methods=['GET', 'POST'])
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


@bp_admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_details(user_id):
    if not current_user.is_admin:
        return redirect("/")

    articles = Article.query.filter(Article.title is not None).all()
    arts = [(i.article_id, i.title) for i in articles]
    form = ChangePasswordForm()
    taskForm = UserTaskForm()
    taskForm.article.choices = arts
    user = User.query.filter_by(id=user_id).outerjoin(Task).first()

    if not user:
        flash('User not found')
        return redirect(url_for('admin'))

    return render_template(
        'user_admin.html',
        itle=user.username,
        user=user,
        form=form,
        taskForm=taskForm,
        articles=articles
    )


@bp_admin.route('/user/<int:user_id>/changePassword', methods=['POST'])
@login_required
def change_password(user_id):
    if not current_user.is_admin:
        return redirect("/")

    form = ChangePasswordForm(request.form)
    user = User.query.filter_by(id=user_id).outerjoin(Task).first()

    if not user:
        flash('User not found')
        return redirect(url_for('admin'))

    if form.validate():
        password = generate_password_hash(request.form['password'])
        user.password_hash = password
        db.session.commit()
        flash('Password changed')

    return redirect(url_for('admin.user_details', user_id=user_id))


@bp_admin.route('/user/<int:user_id>/addTasks', methods=['POST'])
@login_required
def add_tasks(user_id):
    if not current_user.is_admin:
        return redirect("/")

    form = UserTaskForm(request.form)
    user = User.query.filter_by(id=user_id).outerjoin(Task).first()

    if not user:
        flash('User not found')
        return redirect(url_for('admin'))

    article_id = request.form['article']

    sentences = Sentence.query.filter_by(article_id=article_id).all()

    for sentence in sentences:
        try:
            if sentence.task[0].user_id == None:
                sentence.task[0].user_id = user_id
                db.session.commit()
            else:
                user_task = User.query.filter_by(user_id=user_id)
                flash('Task is already taken by the user {}'.format(user_task))
        except:
            flash('Task is alerdy added')

    return redirect(url_for('admin.user_details', user_id=user_id))


@bp_admin.route('/remove/<int:user_id>')
@login_required
def remove_user(user_id):
    if not current_user.is_admin:
        return redirect("/")

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('User was deleted')
    return redirect(url_for('admin'))


@bp_admin.route('/toggle_admin/<int:user_id>')
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        return redirect("/")

    user = User.query.filter_by(id=user_id).first()
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('Admin role chaned')
    return redirect(url_for('admin'))


@bp_admin.route('/user/<int:user_id>/clearTask/<int:task_id>')
@login_required
def clear_task(user_id, task_id):
    if not current_user.is_admin:
        return redirect("/")

    task = Task.query.filter_by(task_id=task_id, user_id=user_id).first()
    task.rate = null()
    task.tags = null()
    task.time_end = null()
    task.time_start = null()
    task.steps = null()
    db.session.commit()

    return redirect(url_for('admin.user_details', user_id=user_id))

@bp_admin.route('/user/<int:user_id>/removeTask/<int:task_id>')
@login_required
def remove_task(user_id, task_id):
    if not current_user.is_admin:
        return redirect("/")

    task = Task.query.filter_by(task_id=task_id, user_id=user_id).first()
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('admin.user_details', user_id=user_id))
