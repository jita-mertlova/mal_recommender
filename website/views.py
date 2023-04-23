from flask import Blueprint, render_template, request, flash, jsonify
import json
from flask_login import login_required, current_user

from .controller import recalc, addRating
from .models import Note
from . import db, items

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            print("Have been in delete function")

    return jsonify({})

@views.route('/rating', methods=['GET', 'POST'])
@login_required
def rating():
    if request.method == 'POST':
        item = request.form.get('item')
        action = request.form.get('action')
        num = 0
        if action == 'approve':
            num = 1
        if action == 'disapprove':
            num = -1
        idx = items.index[items['Title'] == item].tolist()
        addRating(idx[0], num)
    return render_template("rating.html", user=current_user, items=items['Title'])

@views.route('/reccommend', methods=['GET', 'POST'])
@login_required
def reccommend():
    resultNames = eval(current_user.reccommended_names)
    resultNumbers = eval(current_user.reccommended_numbers)
    return render_template("reccommend.html", user=current_user, animesNames=resultNames, animesNumbers=resultNumbers)

@views.route('/recalculate', methods=['GET', 'POST'])
@login_required
def recalculate():
    if current_user.is_admin:
        recalc()
        return render_template("recalculate.html", user=current_user)
    else:
        return render_template("error.html", user=current_user)

