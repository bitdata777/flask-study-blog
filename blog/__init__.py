from flask import Flask
from flask_login import LoginManager
from flaskext.markdown import Markdown

app = Flask(__name__)
app.secret_key = "'\xbf\x91\xf9\x10\xa2t\x17\xce\xe3\xf7\xaa#:)\xd8\x01\r\xdd\xca\xe4j\xc9\xef\n'"

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)

Markdown(app)

from blog import models
from blog import views

from blog import database
database.init_db()