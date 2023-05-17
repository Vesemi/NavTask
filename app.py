import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from forms import *
from models import *
from config import Config
from flask_migrate import Migrate
from extensions import db, login
from flask import get_flashed_messages
from routes import *

app = Flask(__name__)
app.config.from_object(Config)
login.init_app(app)
login.login_view = 'login'


@app.route('/')
@login_required
def index():
    form2 = TaskButtons()
    return render_template("content.html", tasks=Task.query.filter_by(contractor_id=current_user.id), form2=form2)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nieprawidłowe hasło bądź login!')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Logowanie', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Rejestracja poprawna')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    return render_template("users.html", users=User.query.all())


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    form2 = TaskButtons()
    return render_template("tasks.html", tasks=Task.query.all(), form2=form2)


@app.route('/task/<int:id>', methods=['GET', 'POST'])
@login_required
def task(id):
    form2 = TaskButtons()
    current_task = Task.query.filter_by(id=id).first()
    comment_form = AddComment()
    if comment_form.validate_on_submit():
        creator = User.query.filter_by(username=str(current_user)).first()
        comment = Comment(text=comment_form.text.data, creator_id=creator.id, task=id)
        add_comment(comment)
        return redirect(url_for('task', id=id))
    return render_template("task.html", task=current_task, form2=form2, comment_form=comment_form)


def add_comment(comment):
    comment = comment
    db.session.rollback()
    db.session.add(comment)
    db.session.commit()


@app.route('/addtask', methods=['GET', 'POST'])
@login_required
def addtask():
    get_flashed_messages()
    form = AddTask()
    form.contractor.choices = [r.username for r in User.query.all()]
    form.creator.data = current_user
    if form.validate_on_submit():
        contractor = User.query.filter_by(username=form.contractor.data).first_or_404()
        creator = User.query.filter_by(username=str(current_user)).first_or_404()
        task = Task(title=form.title.data, description=form.description.data,
                    creator_id=creator.id, contractor_id=contractor.id,
                    timestamp_deadline=form.timestamp_deadline.data)

        db.session.rollback()
        db.session.add(task)
        db.session.commit()
        comment = Comment(text=f'Task added on {datetime.utcnow()}', creator_id=0, task=task.id)
        add_comment(comment)
        flash(f'Zadanie {task.title} zostało pomyślnie dodane!')
        return redirect(url_for('addtask'))
    return render_template("addtask.html", form=form)


@app.route('/edittask/<int:id>', methods=['GET', 'POST'])
@login_required
def edittask(id):
    task = Task.query.filter_by(id=id).first_or_404()
    creator = User.query.filter_by(id=task.creator_id).first_or_404()
    contractor = User.query.filter_by(id=task.contractor_id).first_or_404()
    form = AddTask(title=task.title, description=task.description, contractor=contractor.username,
                   timestamp_deadline=task.timestamp_deadline, timestamp_created=task.timestamp_created,
                   creator=creator.username)
    form.contractor.choices = [r.username for r in User.query.all()]
    if request.method == 'POST':
        if form.validate_on_submit():
            task = Task.query.filter_by(id=id).first()
            contractor = User.query.filter_by(username=form.contractor.data).first_or_404()
            task.contractor_id = contractor.id
            task.description = form.description.data
            task.title = form.title.data
            db.session.commit()
            comment = Comment(text=f'Task edited by {current_user} on {datetime.utcnow()}', creator_id=0, task=id)
            add_comment(comment)
            return redirect(url_for('tasks'))

    return render_template("edittask.html", form=form, id=id)


@app.route('/deletetask/<int:id>', methods=['GET', 'POST'])
@login_required
def deletetask(id):
    Task.query.filter_by(id=id).delete()
    Comment.query.filter_by(task=id).delete()
    db.session.commit()
    return redirect(url_for('tasks'))


@app.route('/finishtask/<int:id>', methods=['GET', 'POST'])
@login_required
def finishtask(id):
    task = Task.query.filter_by(id=id).first()
    task.timestamp_finished = datetime.utcnow()
    db.session.commit()
    comment = Comment(text=f'Task finished by {current_user} on {datetime.utcnow()}', creator_id=0, task=task.id)
    add_comment(comment)
    return redirect(url_for('tasks'))


@app.route('/user/<username>')
@login_required
def user(username):
    #user = User.query.filter_by(username=username).first_or_404()
    user = current_user
    if user.colors == 'dark':
        user.colors = 'white'
    else:
        user.colors = 'dark'

    db.session.commit()
    tasks = user.tasks
    return render_template('user.html', user=user, tasks=tasks)


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)


register_extensions(app)

if __name__ == "__main__":
    app.run(debug=True)
