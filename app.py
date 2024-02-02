from flask import Flask, redirect, url_for, render_template, url_for
import openai
from requests import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import bcrypt


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'key'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)



class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder":"Passowrd"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        exists = User.query.filter_by(username=username.data).first()
        if exists:
            raise ValidationError("Username already exists, please choose a different one.")
        

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder":"Passowrd"})
    submit = SubmitField("Login")


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password = hashed)
        db.session.add(new_user)
        db.session.commit()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)