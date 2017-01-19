from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from blog import app
from blog import login_manager
from blog.database import db
from blog.forms import LoginForm
from blog.forms import SignupForm
from blog.forms import AddForm
from blog.models import Admin
from blog.models import Post
from blog.utils import request_to_class


login_manager.login_view = 'login'


@app.route('/')
def index():
    post = Post.query.order_by(Post.id.desc()).first()
    return render_template('post.html', post=post)


@app.route('/<title>')
def post(title):
    post = Post.query.filter_by(title=title).first()

    offset = Post.query.with_entities(Post.id).filter_by(title=post.title).\
        first().id
    previous = Post.query.order_by(Post.id.asc()).limit(1).offset(offset-2).\
        first()
    newer = Post.query.order_by(Post.id.asc()).limit(1).offset(offset).\
        first()
    print("-"*30)
    print(" >>>>> ", previous)
    print(" >>>>> ", newer)
    print("-" * 30)
    return render_template('post.html', post=post, previous=previous, newer=newer)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        post = Post(form.title.data, form.content.data, form.author.data)
        db.add(post)
        db.commit()
        return redirect(url_for('post', title=post.title))
    return render_template('add.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if Admin.query.count() == 0:
        return redirect(url_for('signup'))
    form =LoginForm()
    if form.validate_on_submit():
        admin = Admin.get_by_adminname(form.adminname.data)
        if admin is not None and admin.check_password(form.password.data):
            # login_user(admin, form.remember_me.data)
            login_user(admin, remember=True)
            flash('Logged in!')
            return redirect(url_for('index'))
        flash('Error')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(id): # 인자값은 index 값? 으로 들어옴
    return Admin.get_by_id(id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        admin = Admin(adminname=form.adminname.data,
                    password=form.password.data)
        db.add(admin)
        db.commit()
        flash('Welcome, {}! Please login.'.format(admin.adminname))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)