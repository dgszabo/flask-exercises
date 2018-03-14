from flask import Flask, request, redirect, url_for, render_template
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgres://localhost/flask_one_to_many"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
modus = Modus(app)
db = SQLAlchemy(app)
Migrate(app, db)


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    excuses = db.relationship('Excuse', backref='student', lazy='dynamic')


class Excuse(db.Model):

    __tablename__ = "excuses"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    is_believable = db.Column(db.Boolean)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))


@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/students', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        new_student = Student(request.form['first_name'],
                              request.form['last_name'])
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', students=Student.query.all())


@app.route('/students/new')
def new():
    return render_template('new.html')


@app.route('/students/<int:id>/edit')
def edit(id):
    return render_template('edit.html', student=Student.query.get(id))


@app.route('/students/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    found_student = Student.query.get(id)
    if request.method == b'PATCH':
        found_student.first_name = request.form['first_name']
        found_student.last_name = request.form['last_name']
        db.session.add(found_student)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == b'DELETE':
        db.session.delete(found_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('show.html', student=found_student)
