from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask import (flash, g, jsonify, redirect, render_template, request,
                   url_for)
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context
from utils import get_drug_details
from werkzeug.urls import url_parse

auth = HTTPBasicAuth()


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
        user = User(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    print("Aaaaaaaaaaaaaaaaaaaa")
    print(email_or_token, password)
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with email/password
        user = User.query.filter_by(email=email_or_token).first()
        print("user", user)
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.email})


@app.route('/api/users', methods=['POST'])
def new_user():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
    except KeyError as err:
        d = {
            "status": "error",
            "message": "{field} parameter missing".format(
                field=err.args[0]),
        }
        return jsonify(d)
    if User.query.filter_by(email=email).first() is not None:
        d = {
            "status": "error",
            "message": "email already exists",
        }
        return jsonify(d)
    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {
            'status': 'SUCCESS',
            'data': {
                'email': user.email,
            },
        }
    )


if __name__ == '__main__':
    app.run()
