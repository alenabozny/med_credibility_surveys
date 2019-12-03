from flask import render_template, url_for
from flask import request, redirect, flash
from sqlalchemy import null
from app import db
from app.admin import bp_admin
from app.admin.forms import UserTaskForm, ChangePasswordForm, RegisterForm, CopyArticleForm, EditSentenceForm
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


@bp_admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_details(user_id):
    if not current_user.is_admin:
        return redirect("/")

    articles = Article.query.filter(Article.title is not None).all()
    form = ChangePasswordForm()
    user = User.query.filter_by(id=user_id).outerjoin(Task).first()

    if not user:
        flash('User not found')
        return redirect(url_for('admin'))

    return render_template(
        'user_admin.html',
        itle=user.username,
        user=user,
        form=form,
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


@bp_admin.route('/user/<int:user_id>/addTasks', methods=['GET', 'POST'])
@login_required
def add_tasks(user_id):
    if not current_user.is_admin:
        return redirect("/")

    form = UserTaskForm(request.form)
    user = User.query.filter_by(id=user_id).first()

    if form.sentences.data.__len__() is not 0:
        print(form.sentences.data)  # id zdan
        print(user_id)  # id usera
        flash('Added')  # nie wiem co dalej jak to zapisac
        return redirect(url_for('admin.user_details', user_id=user_id))

    if form.article.data is None:
        articles = Article.query.filter(Article.title is not None).all()

        filtered_articles = filter(lambda article: article.sentences.__len__() > 0, articles)
        form.article.choices = [(i.article_id, i.title + " (Sentences: " + str(i.sentences.__len__()) + ")") for i in
                                filtered_articles]

    if form.article.data is not None:
        sentences = Sentence.query.filter_by(article_id=form.article.data).all()
        form.sentences.choices = [(sentence.sentence_id, sentence.body) for sentence in sentences]

    return render_template(
        'add_task_admin.html',
        form=form,
        user=user
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


@bp_admin.route('/user/<int:user_id>/removeTask/<int:task_id>')
@login_required
def remove_task(user_id, task_id):
    if not current_user.is_admin:
        return redirect("/")

    task = Task.query.filter_by(task_id=task_id, user_id=user_id).first()
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('admin.user_details', user_id=user_id))


@bp_admin.route('/article/<int:article_id>')
@login_required
def article_details(article_id):
    if not current_user.is_admin:
        return redirect("/")

    article = Article.query.filter_by(article_id=article_id).first()

    form = CopyArticleForm()
    form.title.data = article.title + ' (Copy)'
    form.article_id.data = article.article_id

    return render_template(
        'article_admin.html',
        article=article,
        form=form
    )


@bp_admin.route('/article/copy', methods=['POST'])
@login_required
def copy_article():
    form = CopyArticleForm(request.form)

    old_article = Article.query.filter_by(article_id=form.article_id.data).first()

    article = Article(
        pub_date=old_article.pub_date,
        access_date=old_article.access_date,
        url=old_article.url,
        title=form.title.data,
        queryTxt=old_article.queryTxt,
        keywords=old_article.keywords
    )

    db.session.add(article)
    db.session.commit()

    for old_sentence in old_article.sentences:
        sentence = Sentence(
            body=old_sentence.body,
            article_id=article.article_id,
            sequence_nr=old_sentence.sequence_nr,
            to_evaluate=old_sentence.to_evaluate
        )
        db.session.add(sentence)
    db.session.commit()

    return redirect(url_for('admin.article_details', article_id=article.article_id))


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
