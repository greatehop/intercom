from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from random import choice
import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
path_db = os.path.join(basedir, 'intercom.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % path_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class IntercomDB(object):

    def __init__(self, path_db, code_list):
        if not os.path.exists(path_db):
            self.create_db(code_list)

    def create_db(self, code_list):
        db.create_all()
        for code in code_list:
            data = Code(code=code)
            db.session.add(data)
        db.session.commit()

    def get_code_list(self):
        code_list = Code.query.all()
        return code_list

    def update_code(self, code_id):
        data = {'is_done': True, 'datetime': datetime.utcnow()}
        db.session.query(Code).filter_by(id=code_id).update(data)
        db.session.commit()


class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), index=True, unique=True)
    is_done = db.Column(db.Boolean, default=False)
    datetime = db.Column(db.DateTime, default=None)


@app.route('/', strict_slashes=False)
@app.route('/<int:code_id>', strict_slashes=False)
def index(code_id=None):

    if code_id is not None:
        intercom_db.update_code(code_id)
        return redirect('/')

    code_list_total = intercom_db.get_code_list()
    code_list_done = sorted([i for i in code_list_total if i.is_done],
                            key=lambda i: i.datetime, reverse=True)
    code_list_in_progress = [i for i in code_list_total if not i.is_done]
    code_random = choice(code_list_in_progress)
    code_details = {
        'done': len(code_list_done),
        'in_progress': len(code_list_in_progress),
        'total': len(code_list_total)}

    return render_template('index.html',
                           code_list_in_progress=code_list_in_progress,
                           code_list_done=code_list_done,
                           code_random=code_random,
                           code_details=code_details)


if __name__ == '__main__':

    # generate list of codes
    code_list = [i for i in range(1000, 9999)]

    # create db object
    intercom_db = IntercomDB(path_db, code_list)

    # run WebUI
    flask_args = {'host': '0.0.0.0', 'port': 5000, 'debug': False}
    app.run(**flask_args)
