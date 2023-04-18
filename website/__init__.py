from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import pandas as pd
from .controller import emptyProfile, defaultPreferences

db = SQLAlchemy()
DB_NAME = "database.db"
items = pd.read_csv('items.csv')
idf = pd.read_csv('idf.csv')
nr_items = items.shape[0]
nr_tags = items.shape[1] - 1
print("Number of items: ", nr_items)
print("Number of tags: ", nr_tags)
tags = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy', 'Game', 'Harem', 'Hentai', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts', 'Mecha', 'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life', 'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller', 'Vampire', 'Yaoi', 'Yuri']

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
            addDefaut()
            print('Created database & added default users!')


def addDefaut():
    from .models import User
    my_admin_pref = defaultPreferences(nr_items, [1, 1, 0, -1, 1])
    my_user_pref = defaultPreferences(nr_items, [1, -1, 1, -1, -1])
    my_admin = User(email="admin@a", first_name="Admin", password=generate_password_hash("aa", method='sha256'),
                   is_admin=True, preferences=my_admin_pref, vector=emptyProfile(nr_tags))
    my_user = User(email="a@a", first_name="Test", password=generate_password_hash("aa", method='sha256'),
                  is_admin=False, preferences=my_user_pref, vector=emptyProfile(nr_tags))
    db.session.add(my_admin)
    db.session.add(my_user)
    db.session.commit()


