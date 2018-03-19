from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_modus import Modus

app = Flask(__name__)
modus = Modus(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/m2m'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "MOVE ME TO AN ENV FILE!"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from project.employees.views import employees_blueprint
from project.departments.views import departments_blueprint

app.register_blueprint(departments_blueprint, url_prefix='/departments')
app.register_blueprint(employees_blueprint, url_prefix='/employees')


@app.route('/')
def root():
    return redirect('/employees')
