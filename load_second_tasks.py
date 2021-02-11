from flask_script import Manager
from app import app, db

manager = Manager(app)

@manager.command
def create_second_tasks():
	try:
		db.session.execute("INSERT INTO second_task(sentence_id) (SELECT sentence.sentence_id FROM sentence INNER JOIN task ON task.sentence_id = sentence.sentence_id WHERE task.rate is not NULL)", {})
	except IntegrityError:
		print("Second Taska for a subset of sentences already exist.")