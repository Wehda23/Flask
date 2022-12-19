from flask import Blueprint,render_template,request,flash,jsonify
from flask.helpers import url_for
from flask.json import jsonify
from flask_login import current_user,login_required
from werkzeug.utils import redirect
from . import db
from .models import Note

views = Blueprint('views',__name__)
import json


#Home Page
@views.route("/home/")
@views.route("/")
@login_required
def home():
    # if request.method =='POST':
    #     note = request.form.get('note')
    #     if len(note) < 1:
    #         flash("Note is too short",category='error')
    #     else:
    #         new_note = Note(data=note,user_id =current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash("Note added!",category='success')
    return render_template("home.html",user=current_user)

@views.route("/delete-note",methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note deleted!",category='error')
            return jsonify({})


@views.route("/add-note",methods=['POST'])
def add_note():
    note = request.form.get('note')
    if len(note) < 1:
        flash("Note is too short",category='error')
    else:
        new_note = Note(data=note,user_id =current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("Note added!",category='success')
    return redirect(url_for('views.home'))



