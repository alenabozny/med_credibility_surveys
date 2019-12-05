from flask import render_template, url_for
from flask import request, redirect, flash
from sqlalchemy import null, and_, not_, or_
from app import db
from app.admin import bp_admin
from app.admin.forms import UserTaskForm, ChangePasswordForm, RegisterForm, EditSentenceForm, UserRemoveTasksForm
from app.models import Task, User, Article, Sentence
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_required


@bp_admin.route('/')
@bp_admin.route('/index')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect("/")

    users = User.query.outerjoin(Task).all()
    articles = Article.query.all()

    return render_template(
        'admin.html',
        title='Admin',
        users=users,
        articles=articles
    )


@bp_admin.route('/user_add', methods=['GET', 'POST'])
@login_required
def user_add():
    if not current_user.is_admin:
        return redirect("/")

    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate():
            username = request.form['username']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])
            name = request.form['name']
            surname = request.form['surname']

            user = User(username=username, email=email, password_hash=password, name=name, surname=surname)
            db.session.add(user)
            db.session.commit()
            flash('User was added')
        else:
            flash('bad form data')

    return render_template('user_add.html', form=form)


@bp_admin.route('/user/<int:user_id>')
@login_required
def user_details(user_id):
    if not current_user.is_admin:
        return redirect("/")

    articles = Article.query.filter(Article.title is not None).all()
    form = ChangePasswordForm()
    form.user_id.data = user_id
    removeForm = UserRemoveTasksForm()
    removeForm.user_id.data = user_id
    user = User.query.filter_by(id=user_id).outerjoin(Task).first()

    if not user:
        flash('User not found')
        return redirect(url_for('admin'))

    return render_template(
        'user_admin.html',
        itle=user.username,
        user=user,
        form=form,
        removeForm=removeForm,
        articles=articles
    )


@bp_admin.route('/removeUserTasks', methods=['POST'])
@login_required
def remove_user_tasks():
    if not current_user.is_admin:
        return redirect("/")
    form = UserRemoveTasksForm(request.form)

    for task_id in form.tasks.data:
        task = Task.query.filter_by(task_id=task_id).first()
        task.user_id = None
    db.session.commit()
    flash('Tasks were deleted')

    return redirect(url_for('admin.user_details', user_id=form.user_id.data))


@bp_admin.route('/changePassword', methods=['POST'])
@login_required
def change_password():
    if not current_user.is_admin:
        return redirect("/")

    form = ChangePasswordForm(request.form)
    user_id = form.user_id.data
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


@bp_admin.route('/user/<int:user_id>/addTasks', methods=['GET', 'POST'])
@login_required
def add_tasks(user_id):
    if not current_user.is_admin:
        return redirect("/")

    form = UserTaskForm(request.form)
    user = User.query.filter_by(id=user_id).first()
    disabledOptions = []
    checkedOptions = []

    if form.sentences.data.__len__() is not 0:
        tasks = Task.query.filter(
            and_(
                Task.sentence.has(article_id=form.article.data),
                Task.user_id == user_id,
                Task.steps.is_(None)
            )
        ).all()

        for task in tasks:
            print(task)
            task.user_id = None

        for id in form.sentences.data:
            task = Task.query.filter(Task.task_id == id).first()
            task.user_id = user_id
        db.session.commit()
        flash('changed')
        return redirect(url_for('admin.user_details', user_id=user_id))

    if form.article.data is None:
        articles = Article.query.filter(Article.title is not None).all()

        filtered_articles = filter(lambda article: article.sentences.__len__() > 0, articles)
        form.article.choices = [(i.article_id, i.title + " (Sentences: " + str(i.sentences.__len__()) + ")") for i in
                                filtered_articles]

    if form.article.data is not None:
        tasks = Task.query.filter(Task.sentence.has(article_id=form.article.data))

        form.sentences.choices = [(task.task_id, task.sentence.body) for task in tasks.all()]
        disabledOptions = tasks.filter(
            or_(
                Task.user_id != user_id,
                and_(Task.user_id == user_id, not_(Task.steps.is_(None)))
            )
        ).all()
        checkedOptions = tasks.filter(
            and_(Task.user_id == user_id)
        ).all()

    return render_template(
        'add_task_admin.html',
        form=form,
        user=user,
        disabledOptions=list(map(lambda task: task.task_id, disabledOptions)),
        checkedOptions=list(map(lambda task: task.task_id, checkedOptions))
    )


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
    flash('Admin role changed')
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
    task.reason = null()
    db.session.commit()

    return redirect(url_for('admin.user_details', user_id=user_id))


@bp_admin.route('/article/<int:article_id>')
@login_required
def article_details(article_id):
    if not current_user.is_admin:
        return redirect("/")

    article = Article.query.filter_by(article_id=article_id).first()

    return render_template(
        'article_admin.html',
        article=article
    )


@bp_admin.route('/sentence/<int:sentence_id>', methods=['GET', 'POST'])
@login_required
def sentence_details(sentence_id):
    if not current_user.is_admin:
        return redirect("/")

    form = EditSentenceForm(request.form)
    sentence = Sentence.query.filter_by(sentence_id=sentence_id).first()

    if request.method == 'POST':
        sentence.body = form.body.data
        db.session.commit()

    form.sentence_id.data = sentence.sentence_id
    form.body.data = sentence.body

    return render_template(
        'sentence_admin.html',
        form=form,
        sentence=sentence
    )
