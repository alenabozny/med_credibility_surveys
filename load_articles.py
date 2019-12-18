from app import app, db
from app.models import Article, Sentence, Task
import json
from nltk.tokenize import sent_tokenize
import re
import os
import dateparser

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

                title = js['title']
                if len(title) > 150:
                    title = title[0:149]

                if title not in article_titles:
                    if len(js['url'])>150:
                        print(filename)

                    article = Article(
                                    title=title,
                                    pub_date=dateparser.parse(str(js["pub_date"])),
                                    access_date=dateparser.parse(str(js["access_date"])),
                                    url=js["url"],
                                    query=js["query"],
                                    keywords=js["keywords"]
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
                    print("LOADED - " + js["title"])
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

                title = "COPY " + js["title"]
                if len(title) > 150:
                    title = title[0:149]

                if js["title"] in article_titles and title not in article_titles:
                    if len(js['url'])>150:
                        print("Too long url: " + filename)

                    article = Article(
                                    title=title,
                                    pub_date=dateparser.parse(str(js["pub_date"])),
                                    access_date=dateparser.parse(str(js["access_date"])),
                                    url=js["url"],
                                    query=js["query"]
                                )

                    sentences = sent_tokenize(js["body"])
                    for i, s in enumerate(sentences):
                        if len(s)>1000:
                            print("Too long sentence: " + filename)
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
