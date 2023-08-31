import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from db import db_session
import constants
from db.tasks import Task
from db.users import User

app = Flask(__name__)

app.config['FLASK_ADMIN_SWATCH'] = 'united'
app.config['SECRET_KEY'] = constants.web_secret_key

db_session.global_init(constants.db_location)
admin = Admin(app, name='Задачи Нейромантиков', template_mode='bootstrap4')
db_s = db_session.create_session()
admin.add_view(ModelView(User, db_s))
admin.add_view(ModelView(Task, db_s))


@app.route('/')
def hello():
    return 'Я работаю, а ты?'


def run_web():
    port = int(os.environ.get("PORT", 5000))
    print(port)
    app.run(host='0.0.0.0', port=port)

# TODO возможно нужно сделать авторизацию в админке