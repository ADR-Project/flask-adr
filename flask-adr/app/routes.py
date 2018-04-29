from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


from utils import get_drug_details


@app.route("/")
def home():
    return render_template('home.html', title='Home')


@app.route("/drug")
def get_do():
    try:
        drug_name = request.args['drug_name']
        temp = request.args['temp']
        pressure = request.args['pressure']
    except KeyError as err:
        d = {
            "status": "error",
            "message": "{field} parameter missing".format(
                field=err.args[0]),
        }
    else:
        result = get_drug_details(
            drug_name=drug_name, temp=temp, pressure=pressure
        )
        if not result:
            d = {
                "status": "error",
                "message": "No drug data found",
            }
        else:
            d = {
                'status': 'SUCCESS',
                'data': result,
            }
    return jsonify(d)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # TODO: fix circular import
    from . import db
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run()
