# here we will store standard routes for the website (e.g. where users can actuallz go to
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') # slash because main paige of the website
def home():
    return render_template("home.html")

