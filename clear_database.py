from flask_script import Manager
from app import app, db

manager = Manager(app)

@manager.command
def clear():
    meta = db.metadata
    article = db.Table('article', meta)
    sentence = db.Table('sentence', meta)
    task = db.Table('task', meta)
    # user = db.Table('user', meta)

    for table in [task, sentence, article]:
        print('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()

if __name__ == "__main__":
    manager.run()
