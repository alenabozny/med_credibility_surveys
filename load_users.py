from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash
from flask_script import Manager
from app import app

manager = Manager(app)


@manager.command
def load_users():
    try:
        user = User(username="test", email="test@test.pl", password_hash=generate_password_hash("test"), name="Jan",
                    surname="Testowski", is_admin=True)
        db.session.add(user)
        db.session.commit()
    except:
        print("User test exists")

    try:
        user = User(username="admin", email="admin@admin.pl", password_hash=generate_password_hash("admin"), name="Jan",
                    surname="Adminowski", is_admin=True)
        db.session.add(user)
        db.session.commit()
    except:
        print("User test exists")


if __name__ == "__main__":
    manager.run()
