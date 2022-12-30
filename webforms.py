from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    favorite_color = StringField("Favorite Color")
    about_author = TextAreaField("About Author")
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
    # content = StringField("Content", validators=[
    #                       InputRequired()], widget=TextArea())
    content = CKEditorField('Content', validators=[InputRequired()])
    # author = StringField("Author", validators=[InputRequired()])
    slug = StringField("Slug", validators=[InputRequired()])
    submit = SubmitField()


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[InputRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField()
