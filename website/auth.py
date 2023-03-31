# here we will store standard routes for the website (e.g. where users can actually go to
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", myVariable=False)

@auth.route('/logout')
def logout():
    return "LogOUT"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email) < 2:
            flash('Email must be at least 2 characters.', category='error')
        elif len(first_name) < 2:
                flash('Name must be at least 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 2:
            flash('Password must be at least 2 characters.', category='error')
    return render_template("sign_up.html")
