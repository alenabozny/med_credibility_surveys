from flask import render_template, url_for
from flask import request, redirect, flash
from sqlalchemy import null, and_, not_, or_
from app import db
from app.admin import bp_admin
from app.admin.admin_required import admin_required
from app.admin.forms import UserSecondTaskForm, UserTaskForm, ChangePasswordForm, RegisterForm, EditSentenceForm, UserRemoveTasksForm, UserRemoveSecondTasksForm
from app.models import SecondTask, Task, User, Article, Sentence


@bp_admin.route('/')
@bp_admin.route('/index')
@admin_required
def admin():
    users = User.query.outerjoin(Task).all()
    articles = Article.query.all()

    return render_template(
        'admin.html',
        title='Admin',
        users=users,
        articles=articles
    )


@bp_admin.route('/user_add', methods=['GET', 'POST'])
@admin_required
def user_add():
    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            name = form.name.data
            surname = form.surname.data

            user = User(username=username, email=email, password=password, name=name, surname=surname)
            db.session.add(user)
            db.session.commit()
            flash('User was added')
        else:
            flash('bad form data')

    return render_template('user_add.html', form=form)


@bp_admin.route('/user/<int:user_id>')
@admin_required
def user_details(user_id):
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
@admin_required
def remove_user_tasks():
    form = UserRemoveTasksForm(request.form)
    print(form.tasks)

    for task_id in form.tasks.data:
        task = Task.query.filter_by(task_id=task_id).first()
        task.user_id = None
        task.steps = None
        task.rate = None
        task.time_start = None
        task.time_end = None
        task.reason = None
    db.session.commit()
    flash('Tasks were cleared')

    return redirect(url_for('admin.user_details', user_id=form.user_id.data))

@bp_admin.route('/removeUserSecondTasks', methods=['POST'])
@admin_required
def remove_user_second_tasks():
    form = UserRemoveSecondTasksForm(request.form)
    print(form.second_tasks.data)

    for s_task_id in form.second_tasks.data:
        s_task = SecondTask.query.filter_by(s_task_id=s_task_id).first()
        s_task.user_id = None
        s_task.steps = None
        s_task.rate = None
        s_task.time_start = None
        s_task.time_end = None
        s_task.own_reason = None
    db.session.commit()
    flash('Second Tasks were cleared')

    return redirect(url_for('admin.user_details', user_id=form.user_id.data))


@bp_admin.route('/changePassword', methods=['POST'])
@admin_required
def change_password():
    form = ChangePasswordForm(request.form)
    user_id = form.user_id.data
    user = User.query.filter_by(id=user_id).outerjoin(Task).first()

    if not user:
        flash('User not found')
        return redirect(url_for('admin'))

    if form.validate():
        password = form.password.data
        user.password = password
        db.session.commit()
        flash('Password changed')

    return redirect(url_for('admin.user_details', user_id=user_id))


@bp_admin.route('/user/<int:user_id>/addTasks', methods=['GET', 'POST'])
@admin_required
def add_tasks(user_id):
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

        for f_art in filtered_articles:
            q = db.session.execute("SELECT * FROM Sentence \
                                JOIN Article ON Sentence.article_id=Article.article_id \
                                JOIN Task ON Sentence.sentence_id=Task.sentence_id \
                                WHERE Article.article_id=:id \
                                AND Task.user_id IS NULL",
                                {"id": f_art.article_id}
                               )

            unassigned_sentences = len([x for x in q])
            if unassigned_sentences != 0:
                form.article.choices.append(
                                            (f_art.article_id, f_art.title + \
                                            " (Unassigned: " + str(unassigned_sentences) + ")")
                                        )

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

@bp_admin.route('/user/<int:user_id>/addSecondTasks', methods=['GET', 'POST'])
@admin_required
def add_second_tasks(user_id):
    form = UserSecondTaskForm(request.form)
    user = User.query.filter_by(id=user_id).first()
    disabledOptions = []
    checkedOptions = []

    if form.sentences.data.__len__() != 0:
        second_tasks = SecondTask.query.filter(
            and_(
                SecondTask.sentence.has(article_id=form.article.data),
                SecondTask.user_id == user_id,
                SecondTask.steps.is_(None)
            )
        ).all()

        for second_task in second_tasks:
            print(second_task)
            second_task.user_id = None

        for id in form.sentences.data:
            second_task = SecondTask.query.filter(SecondTask.s_task_id == id).first()
            second_task.user_id = user_id

        db.session.commit()
        flash('changed')
        return redirect(url_for('admin.user_details', user_id=user_id))

    if form.article.data is None:
        articles = Article.query.filter(Article.title is not None).all()

        filtered_articles = filter(lambda article: article.sentences.__len__() > 0, articles)

        for f_art in filtered_articles:
            q = db.session.execute("SELECT * FROM Sentence \
                                JOIN Article ON Sentence.article_id=Article.article_id \
                                JOIN second_task ON Sentence.sentence_id=second_task.sentence_id \
                                WHERE Article.article_id=:id \
                                AND second_task.user_id IS NULL",
                                {"id": f_art.article_id}
                               )

            unassigned_sentences = len([x for x in q])
            if unassigned_sentences != 0:
                form.article.choices.append(
                                            (f_art.article_id, f_art.title + \
                                            " (Unassigned: " + str(unassigned_sentences) + ")")
                                        )

    if form.article.data is not None:
        second_tasks = SecondTask.query.filter(SecondTask.sentence.has(article_id=form.article.data))

        form.sentences.choices = [
            (second_task.s_task_id, second_task.sentence.body) for second_task in second_tasks.all()
            ]
        disabledOptions = second_tasks.filter(
                                            or_(
                                                SecondTask.user_id != user_id,
                                                and_(SecondTask.user_id == user_id, 
                                                not_(SecondTask.steps.is_(None)))
                                                )
                                            ).all()
        checkedOptions = second_tasks.filter(
                                            and_(SecondTask.user_id == user_id)
                                        ).all()

    return render_template(
        'add_task_admin.html',
        form=form,
        user=user,
        disabledOptions=list(map(lambda second_task: second_task.s_task_id, disabledOptions)),
        checkedOptions=list(map(lambda second_task: second_task.s_task_id, checkedOptions))
    )


@bp_admin.route('/remove/<int:user_id>')
@admin_required
def remove_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('User was deleted')
    return redirect(url_for('admin'))


@bp_admin.route('/toggle_admin/<int:user_id>')
@admin_required
def toggle_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('Admin role changed')
    return redirect(url_for('admin.admin'))


@bp_admin.route('/user/<int:user_id>/clearTask/<int:task_id>')
@admin_required
def clear_task(user_id, task_id):
    task = Task.query.filter_by(task_id=task_id, user_id=user_id).first()
    task.rate = null()
    task.tags = null()
    task.time_end = null()
    task.time_start = null()
    task.steps = null()
    task.reason = null()
    db.session.commit()

    return redirect(url_for('admin.user_details', user_id=user_id))

@bp_admin.route('/user/<int:user_id>/clearSecondTask/<int:s_task_id>')
@admin_required
def clear_second_task(user_id, s_task_id):
    second_task = SecondTask.query.filter_by(s_task_id=s_task_id, user_id=user_id).first()
    second_task.rate = null()
    second_task.tags = null()
    second_task.time_end = null()
    second_task.time_start = null()
    second_task.steps = null()
    second_task.own_reason = null()
    db.session.commit()

    return redirect(url_for('admin.user_details', user_id=user_id))

@bp_admin.route('/article/<int:article_id>')
@admin_required
def article_details(article_id):
    article = Article.query.filter_by(article_id=article_id).first()

    return render_template(
        'article_admin.html',
        article=article
    )


@bp_admin.route('/sentence/<int:sentence_id>', methods=['GET', 'POST'])
@admin_required
def sentence_details(sentence_id):
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
