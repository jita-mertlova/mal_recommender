# here we will store standard routes for the website (e.g. where users can actuallz go to
from flask import Blueprint, render_template, request, flash, jsonify
import json
from flask_login import login_required, current_user

from .controller import recalc
from .models import Note
from . import db
#from controller.py import recalculate

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])         # slash because main paige of the website
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')#Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note
            db.session.add(new_note) #adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            print("Been in delete")

    return jsonify({})

@views.route('/rating', methods=['GET', 'POST'])
@login_required
def rating():
    return render_template("rating.html", user=current_user)

@views.route('/reccommend', methods=['GET', 'POST'])
@login_required
def reccommend():
    return render_template("reccommend.html", user=current_user)

@views.route('/recalculate', methods=['GET', 'POST'])
@login_required
def recalculate():
    if current_user.is_admin:
        recalc()
        return render_template("recalculate.html", user=current_user)
    else:
        return render_template("error.html", user=current_user)

