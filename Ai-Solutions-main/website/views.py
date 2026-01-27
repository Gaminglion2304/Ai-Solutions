from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from .llm import cisg_assistant, call_model
import json

views = Blueprint('views', __name__)

# -------------------------
# HOME PAGE
# -------------------------
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


# -------------------------
# DELETE NOTE
# -------------------------
@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = request.get_json()
    if not data or 'noteId' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    note = Note.query.get(data['noteId'])
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()

    return jsonify({})


# -------------------------
# GENERAL CHATBOT
# -------------------------
@views.route('/chat', methods=['POST'])
def chat():

    if not current_user.is_authenticated:
        return jsonify({"reply": "Please log in to chat."}), 401

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Empty message."}), 400

    try:
        # USE call_model INSTEAD OF client
        bot_reply = call_model(user_message)

    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        bot_reply = "I’m having trouble responding right now."

    return jsonify({"reply": bot_reply})


# -------------------------
# CISG LEGAL ASSISTANT
# -------------------------
@views.route("/cisg", methods=["GET", "POST"])
def cisg_page():
    if request.method == "POST":
        question = request.form.get("question")
        answer = cisg_assistant(call_model, question)
        return render_template("cisg.html", question=question, answer=answer, user=current_user)

    return render_template("cisg.html", user=current_user)

