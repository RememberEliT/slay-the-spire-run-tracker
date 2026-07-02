from urllib.parse import urlsplit

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user, login_user, login_required
import sqlalchemy as sa

from app import db
from app.models import Run, User
from app.forms import RunForm, RegistrationForm, LoginForm
from app import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_run", methods=["GET", "POST"])
@login_required
def create_run():
    form = RunForm()
    if form.validate_on_submit():
        run = Run(
            character = form.character.data,
            floor_reached = form.floor_reached.data,
            ascension_level = form.ascension_level.data,
            win = form.win.data,
            user = current_user,
            notes = form.notes.data
        )
        db.session.add(run)
        db.session.commit()
        flash('Successfully added the run')
        return redirect(url_for('list_runs'))

    return render_template("create_run.html", form=form)

@app.route("/runs")
@login_required
def list_runs():
    #gets all runs for the user
    runs = Run.query.filter_by(user_id = current_user.id).all()
    return render_template("list.html", runs=runs)

@app.route("/run/<int:run_id>")
@login_required
def run_detail(run_id):
    run = Run.query.get_or_404(run_id, user_id = current_user.id)
    return render_template("detail.html", run=run)

@app.route("/runs/<int:run_id>/edit", methods=["GET", "POST"])
@login_required
def run_edit(run_id):
    run = Run.query.get_or_404(run_id, user_id = current_user.id)
    form = RunForm(obj=run)

    if form.validate_on_submit():
        run.character = form.character.data
        run.floor_reached = form.floor_reached.data
        run.ascension_level = form.ascension_level.data
        run.win = form.win.data
        run.notes = form.notes.data
        db.session.commit()
        flash('You have successfully updated a run')
        return redirect(url_for('list_runs'))

    return render_template('create_run.html', form=form)

@app.route("/runs/<int:run_id>/delete", methods=["POST"])
@login_required
def run_delete(run_id):
    run = Run.query.get_or_404(run_id, user_id = current_user.id)
    db.session.delete(run)
    db.session.commit()
    flash('You have successfully deleted a run')
    return redirect(url_for('list_runs'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

if __name__ == "__main__":
    app.run(debug=True)