from flask import Flask
from flask_login import LoginManager
from flaskext.markdown import Markdown

app = Flask(__name__)
app.secret_key = "ASDFASDF@#adff2f234AD234#211rreer"

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)

Markdown(app)

from blog import models
from blog import views

from blog import database
database.init_db()