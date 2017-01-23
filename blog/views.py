from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request
from flask import jsonify
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from sqlalchemy import func
from blog import app
from blog import login_manager
from blog.database import db
from blog.forms import LoginForm
from blog.forms import SignupForm
from blog.forms import AddForm
from blog.forms import ModifyForm
from blog.models import Admin
from blog.models import Post
from blog.models import Tag
from blog.utils import request_to_class


login_manager.login_view = 'login'


@app.route('/')
def index():
    post = get_post()
    if post:
        previous = get_pager(post.title, 'previous')
        newer = get_pager(post.title, 'newer')
        return render_template('post.html', post=post, previous=previous,
                               newer=newer, tags=top_tags())
    return render_template('post.html', tags=top_tags())


@app.route('/<title>', methods=['GET'])
def read(title):
    post = get_post(title)
    previous = get_pager(title, 'previous')
    newer = get_pager(title, 'newer')
    return render_template('post.html', post=post, previous=previous,
                           newer=newer, tags=top_tags())


def get_post(title=None):
    post = Post.query.order_by(Post.id.desc())
    if title:
        return post.filter_by(title=title).first()
    return post.first()


def get_pager(title, pager):
    offset = get_post(title).id
    post = Post.query
    if pager == 'previous':
        return post.with_entities(func.max(Post.id), Post.title).\
            filter(Post.id < offset).first()[1]
    return post.with_entities(func.min(Post.id), Post.title).\
        filter(Post.id > offset).first()[1]


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddForm()
    if form.validate_on_submit():
        post = Post(form.title.data, form.content.data, form.author.data,
                    form.tag.data)
        add_tag(form.tag.data)
        db.add(post)
        db.commit()
        return redirect(url_for('read', title=post.title))
    return render_template('add.html', form=form)


@app.route('/<title>/modify', methods=['GET', 'PUT'])
@login_required
def modify(title):
    form = ModifyForm()
    if request.method == 'PUT':
        fields = request_to_class(request, 'content', 'tag')
        post = get_post(title)
        post.title = fields.title
        post.content = fields.content
        modify_tag(post.tag, fields.tag)
        post.tag = fields.tag
        db.add(post)
        db.commit()
        return jsonify(status='ok')
    post = get_post(title)
    form.title.data = post.title
    form.content.data = post.content
    form.tag.data = post.tag
    return render_template('modify.html', form=form)


@app.route('/<title>', methods=['DELETE'])
def remove(title):
    if title is not None:
        post = get_post(title)
        modify_tag(post.tag)
        db.delete(post)
        db.commit()
        return jsonify(status='ok')
    return jsonify(status='error')


def has_tag(tag):
    if get_tag(tag):
        return True
    return False


def get_tag(tag):
    return Tag.query.filter_by(name=tag).first()


def tag_add_or_hitup(tag):
    if not tag:
        return
    if has_tag(tag):
        tag = get_tag(tag)
        tag.hit += 1
        db.add(tag)
        db.commit()
        return
    tag = Tag(tag)
    db.add(tag)
    db.commit()


def add_tag(tag):
    tags = tag_to_list(tag)
    for tag in tags:
        tag_add_or_hitup(tag)


def tag_to_list(tag):
    if tag is not None:
        return tag.replace(" ", "").split(",")
    return list()


def tag_remove_or_hitdown(tag):
    tag = get_tag(tag)
    if tag is None:
        return
    tag.hit -= 1
    if tag.hit == 0:
        db.delete(tag)
        db.commit()
        return
    db.add(tag)
    db.commit()


def modify_tag(post_tag, form_tag=None):
    if form_tag is None:
        post_tag = tag_to_list(post_tag)
        for tag in post_tag:
            tag_remove_or_hitdown(tag)
        return

    post_tag = set(tag_to_list(post_tag))
    form_tags = set(tag_to_list(form_tag))
    remove_or_down = post_tag - form_tags
    if remove_or_down is not None:
        for tag in remove_or_down:
            tag_remove_or_hitdown(tag)
    add_or_up = form_tags - post_tag
    if add_or_up is not None:
        for tag in add_or_up:
            tag_add_or_hitup(tag)



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


def top_tags(number=10):
    return Tag.query.order_by(Tag.hit.desc()).limit(number).all()


@app.template_filter('tag_to_list')
def tag_to_list_filter(tags):
    if tags is not None:
        return tags.replace(" ", "").split(",")
    return list()
