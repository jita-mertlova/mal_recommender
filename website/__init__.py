from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .controller import empty_profile, default_preferences
from .const import nr_tags, nr_items, tags, idf, default_recommendation_numbers, default_recommendation_names

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jitaMertlova'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            add_defaut_users()
            print('Created database & added default users!')


def add_defaut_users():
    from .models import User
    my_admin_pref = default_preferences(nr_items, [1, 1, 0, -1, 1])
    my_user_pref = default_preferences(nr_items, [1, -1, 1, -1, -1])
    my_second_user_pref = default_preferences(nr_items, [-1, -1, -1, -1, -1])
    my_admin = create_default_user(email="admin@a", first_name="Admin", password="aa", is_admin=True, preferences=my_admin_pref)
    my_user = create_default_user(email="a@a", first_name="Test", password="aa", is_admin=False, preferences=my_user_pref)
    my_second_user = create_default_user(email="a@b", first_name="Test", password="aa", is_admin=False, preferences=my_second_user_pref)
    db.session.add(my_admin)
    db.session.add(my_user)
    db.session.add(my_second_user)
    db.session.commit()

def create_default_user(email: str, first_name: str, password: str, is_admin: bool, preferences):
    from .models import User
    return User(email=email, first_name=first_name, password=generate_password_hash(password, method='sha256'),
                is_admin=is_admin, preferences=preferences, vector=empty_profile(nr_tags), recommended_names=default_recommendation_names, recommended_numbers=default_recommendation_numbers)


