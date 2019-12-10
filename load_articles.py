from app import app, db
from app.models import Article, Sentence, Task
import json
from nltk.tokenize import sent_tokenize
import re
import os

from flask_script import Manager
from app import app

manager = Manager(app)

@manager.command
def load_original():
    ### LOAD ORIGINAL ARTICLE, WITHOUT MODIFICATIONS
    directory = os.fsencode('./articles')
    article_titles = [x[0] for x in db.session.query(Article.title).select_from(Article).all()]
    # [print(title+'\n') for title in article_titles]

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
                            article=article,
                            modification=None
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


@manager.command
def load_modified():
    directory = os.fsencode('./articles_modified')
    article_titles = [x[0] for x in db.session.query(Article.title).select_from(Article).all()]

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            with open(os.path.join('articles_modified', filename)) as json_file:
                js = json.load(json_file)
                if js["title"] in article_titles and ("COPY " + js["title"]) not in article_titles:
                    article = Article(
                                    title="COPY " + js["title"],
                                    # pub_date=js["pub_date"],
                                    # access_date=js["access_date"],
                                    url=js["url"],
                                    query=js["query"]
                                )

                    sentences = sent_tokenize(js["body"])
                    for i, s in enumerate(sentences):
                        mod_types = {
                            'HEDGE': "hedging",
                            'AHEDGE': "antihedging",
                            'NEG': "negation",
                            'HYPER': "hyperonymy",
                            'HYPO': "hyponymy",
                            'SYN': "synonymy"
                        }

                        reg = '\s*{{2}(?P<type>HEDGE|AHEDGE|NEG|HYPER|HYPO|SYN)\}{2}'
                        try:
                            type = re.match(reg, s).group('type')
                            s = s.replace('{{'+type+'}}', '')
                            modification = mod_types[type]
                        except AttributeError:
                            modification = None

                        sentence = Sentence(
                            body=s,
                            sequence_nr=i + 1,
                            to_evaluate=True,
                            article=article,
                            modif=modification
                        )

                        if modification:
                            task = Task(
                                sentence=sentence
                            )
                            db.session.add(task)
                        else:
                            db.session.add(sentence)

                    db.session.commit()
                else:
                    print("Cannot load Article: \"" + js["title"] + "\" when it's original "\
                                                                    "version is not yet in a database "\
                                                                    "OR the COPY is already in a database")
        else:
            continue


if __name__ == "__main__":
    manager.run()