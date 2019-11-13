from app import app, db
from app.models import Article, Sentence, Task
import json
from nltk.tokenize import sent_tokenize

from flask_script import Manager
from app import app

manager = Manager(app)

@manager.command
def load():
    import os

    directory = os.fsencode('./articles')
    article_titles = [x[0] for x in db.session.query(Article.title).select_from(Article).all()]

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            with open(os.path.join('articles', filename)) as json_file:
                js = json.load(json_file)
                if js["title"] not in article_titles:
                    article = Article(
                                    title=js["title"],
                                    # pub_date=js["pub_date"],
                                    # access_date=js["access_date"],
                                    url=js["url"],
                                    query=js["query"]
                                )
                    sentences = sent_tokenize(js["body"])
                    for i, s in enumerate(sentences):
                        sentence = Sentence(
                            body=s,
                            sequence_nr=i+1,
                            to_evaluate=True,
                            article=article
                        )
                        task = Task(
                            sentence=sentence
                        )
                        db.session.add(task)
                    db.session.commit()
                else:
                    print("Article \"" + js["title"] + "\" is already in a database.")
        else:
            continue


if __name__ == "__main__":
    manager.run()