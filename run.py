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

    def get_codes(self):
        codes = Code.query.all()
        return codes

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

    if code_id:
        intercom_db.update_code(code_id)
        return redirect('/')

    codes_total = intercom_db.get_codes()
    codes_done = sorted([i for i in codes_total if i.is_done],
                            key=lambda i: i.datetime, reverse=True)
    codes_in_progress = [i for i in codes_total if not i.is_done]
    code_random = choice(codes_in_progress)

    codes_limit = 10
    codes = {
        'details': {
            'done': len(codes_done),
            'in_progress': len(codes_in_progress),
            'total': len(codes_total)},
        'random': code_random,
        'done': codes_done[:codes_limit],
        'in_progress': codes_in_progress[:codes_limit]
    }
    return render_template('index.html', codes=codes)


if __name__ == '__main__':

    # generate list of codes
    code_list = [i for i in range(1000, 10000)]

    # create db object
    intercom_db = IntercomDB(path_db, code_list)

    # run WebUI
    flask_args = {'host': '0.0.0.0', 'port': 5000, 'debug': False}
    app.run(**flask_args)
