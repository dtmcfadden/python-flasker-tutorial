import os
from dotenv import load_dotenv
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

load_dotenv()

db = SQLAlchemy()
# Create a Flask Instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# Secret Key!
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)


# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create Model


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create A String
    def __rept__(self):
        return '<Name %r>' % self.name

# Create a Blog Post model


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))


with app.app_context():
    db.create_all()


# Create a Form class

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', [InputRequired(), EqualTo(
        'password_hash2', message='Passwords must match')])
    password_hash2 = PasswordField('Confirm Password')
    # password_hash = PasswordField("Password", validators=[DataRequired()])
    # password_hash2 = PasswordField(
    #     "Confirm Password", validators=[DataRequired(), EqualTo(
    #         password_hash, message='Passwords Must Match!')])
    # password_hash = PasswordField(
    #     "Password", validators=[DataRequired(), EqualTo(
    #         password_hash2, message='Passwords Must Match!')])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[InputRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    email = StringField("What's Your Email", validators=[InputRequired()])
    password_hash = PasswordField(
        "What's Your Password", validators=[InputRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[
                          InputRequired()], widget=TextArea())
    author = StringField("Author", validators=[InputRequired()])
    slug = StringField("Slug", validators=[InputRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField()

# Create a route decorator

# Create Login Page


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Successful!!')
                return redirect('dashboard')
            else:
                flash('Wrong Password - Try Again!')
        else:
            flash('User Doesn\'t Exist. Try Again.')
    return render_template('login.html', form=form)

# Create Logout Page


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You Have Been Logged Out! Thanks for visiting!')
    return redirect(url_for('login'))

# Create Dashboard Page


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash('User Updated Successfully!')
            return render_template('dashboard.html', form=form, name_to_update=name_to_update)
        except:
            flash('Error! Looks like there was a problem! Please try again.')
            return render_template('dashboard.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('dashboard.html', form=form, name_to_update=name_to_update)
    return render_template('dashboard.html')


@app.route('/')
# def index():
#     return '<h1>Hello World!</h1>'
def index():
    first_name = "bob"
    stuff = "This is <strong>Bold</strong> text"
    favorite_pizza = ["Pepperoni", "Cheese", 41]
    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)


# localhost:5000/user/john
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)

# Delete Database Record


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    form = UserForm()
    name = None
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully!')
    except:
        flash('Error! Looks like there was a problem! Please try again.')
    finally:
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html', name=name, form=form, our_users=our_users)

# Update Database Record


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash('User Updated Successfully!')
            return render_template('update.html', form=form, name_to_update=name_to_update)
        except:
            flash('Error! Looks like there was a problem! Please try again.')
            return render_template('update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update)


# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    form = NamerForm()
    name = None
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template('name.html', name=name, form=form)


# Get user name and email
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    name = None
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pwd = generate_password_hash(
                form.password_hash.data, "sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data,
                         favorite_color=form.favorite_color.data,
                         password_hash=hashed_pwd)
            db.session.add(user)
            db.session.commit()
            flash("User Added Successfully")
            form.username.data = ''
            form.name.data = ''
            form.email.data = ''
            form.favorite_color.data = ''
            form.password_hash.data = ''
            form.password_hash2.data = ''
        else:
            flash("User Already Exists")

        name = form.name.data

    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', name=name, form=form, our_users=our_users)

# Create Password Test Page


@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    form = PasswordForm()
    email = None
    password = None
    pw_to_check = None
    passed = None

    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password_hash = form.password_hash.data

        # Lookup user by email
        pw_to_check = Users.query.filter_by(email=email).first()

        # Check Hashed Password
        passed = check_password_hash(
            pw_to_check.password_hash, form.password_hash.data)

        form.email.data = ''
        form.password_hash.data = ''

        # flash("Form Submitted Successfully")
    return render_template('test_pw.html', email=email, pw_to_check=pw_to_check, passed=passed, form=form)

# Return JSON


@app.route('/date')
def get_current_date():
    favorite_pizza = {
        "John": "Pepperoni",
        "Mary": "Cheese",
        "Tim": "Mushroom"
    }
    return favorite_pizza
    # return {"Date": datetime.today()}


# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data,
                     author=form.author.data, slug=form.author.data)
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        db.session.add(post)
        db.session.commit()

        flash('blog Post Submitted Successfully')

    return render_template('add_post.html', form=form)


@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)


@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()
        flash('Post Has Been Updated')

        return redirect(url_for('post', id=post.id))

    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)


@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Blog Post Was Deleted')
    except:
        flash("Whoops! Problem Deleting Post")
    finally:
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts=posts)

# Create Custom Error Pages

# Invalid URL


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("error/500.html"), 500
