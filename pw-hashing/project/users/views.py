from flask import redirect, render_template, request, url_for, Blueprint
from project.users.forms import UserForm
from project.users.models import User
from project import db,bcrypt

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

@users_blueprint.route('/users')
def index():
    return render_template('users/index.html')

@users_blueprint.route('/signup', methods =["GET", "POST"])
def signup():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User.register(form.data['username'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            return render_template('users/signup.html', form=form)
        return redirect(url_for('users.login'))
    return render_template('users/signup.html', form=form)


@users_blueprint.route('/login', methods = ["GET", "POST"])
def login():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        found_user = User.query.filter_by(username = form.data['username']).first()
        if found_user:
            authenticated_user = User.authenticate(found_user.username, form.data['password'])
            if authenticated_user:
                return redirect(url_for('users.welcome'))
    return render_template('users/login.html', form=form)

@users_blueprint.route('/welcome')
def welcome():
    return render_template('users/welcome.html')