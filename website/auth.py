from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response 
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Query the database to see if the user exists.
        user = User.query.filter_by(email=email).first()

        # Check if user exists, then if password matches, then login
        if user:
            if check_password_hash(user.password, password):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    # How to properly redirect AND return the response object?
                    return redirect(url_for('views.home'), code=302, Response=make_response(jsonify(responseObject))) # Redirect user to home page

            else:
                flash('Senha incorreta. Tente novamente.', category='error')

                return redirect(url_for('auth.signin'))

        else:
            flash('Email não cadastrado.', category='error')

            return redirect(url_for('auth.signin'))

    return render_template("signin.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.signin'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')
        name = request.form.get('name')
        age = request.form.get('age')
        address = request.form.get('address')

        # Query the database to see if the user exists.
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email já cadastrado.', category='error')
        elif len(username) < 2:
            flash('Username precisa ter mais do que 1 caracter.', category='error')
        elif len(email) < 5:
            flash('Email precisa ter mais do que 4 caracteres.', category='error')
        elif password1 != password2:
            flash('Senhas não coincidem.', category='error')
        elif len(password1) < 7:
            flash('Senha muito curta.', category='error')
        elif len(name) < 2:
            flash('Nome precisa ter mais do que 1 caracter.', category='error')
        elif int(age) > 150:
            flash('Idade Inválida.', category='error')
        elif len(address) < 5:
            flash('Email precisa ter mais do que 4 caracteres.', category='error')
        else:
            # Add user to database
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'), name=name, age=age, address=address)
            db.session.add(new_user)
            db.session.commit()

            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }

            flash('Usuário cadastrado.', category='success')
            login_user(new_user, remember=True) # Logs in the user and remembers the fact that the user is logged in.

            # How to properly redirect AND return the response object?
            return redirect(url_for('views.home'), code=302, Response=make_response(jsonify(responseObject))) # Redirect user to home page

    return render_template("signup.html", user=current_user)