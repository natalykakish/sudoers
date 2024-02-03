from flask import Flask, redirect, url_for, render_template, url_for, redirect, flash
from requests import request
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_bcrypt import Bcrypt

# DB Import
from dbConfig import *

# Forms Import
from forms import *

#Construct Flask App and Configure DB
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'key'

#Initialize SQLAlchemy with Flask App
db.init_app(app)
# Use manual request to create all tables defined in dbConfig
with app.app_context():
    db.create_all()


bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('index.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password = hashed)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
=======
import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('my_template.html')
