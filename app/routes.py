from flask import render_template
from flask import jsonify
from app import app
from app.forms import LoginForm

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


@app.route('/example')
def example():
    return render_template(
        'example_task.html',
        title='Task',
        sentences=['test1', 'test2', 'test3'],
        keywords=['keywords1', 'keywords2', 'keywords3'].join(', ')
    )
