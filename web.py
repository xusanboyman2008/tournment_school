from flask import Flask, request, jsonify
import secrets
from flask_cors import CORS

from database import get_or_create_candidates, update_candidate, get_questions_and_answers, init, all_users

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

CORS(app)  # enable CORS for all routes


@app.route('/')
def index():
    return jsonify({
        'success': False,
        'message': '/create_user [POST], /get_questions_and_answers [GET], /update_user [GET]'
    })


@app.route("/create_user", methods=["POST"])
def create_user():
    name = request.form.get('name','')
    surname = request.form.get("surname", "")
    subject = request.form.get("subject", "")
    grade = request.form.get("grade", "")

    if not name or not surname or not subject or not grade:
        return jsonify({"success": False, "message": "name, surname, subject, grade is required"})

    user = get_or_create_candidates(name, surname, grade, subject)

    return jsonify({"success": True, "user": user})



@app.route("/get_questions_and_answers", methods=["GET"])
def get_questions_and_answers_route():
    subject_name = request.args.get("subject_name", "")
    grade = request.args.get("grade", "")

    if not subject_name or not grade:
        return jsonify({"success": False, 'message': 'subject_name and grade are required'})

    result = get_questions_and_answers(subject_name, grade)
    if not result:
        return jsonify({"success": False, "message": "No questions found"})

    return jsonify({
        "success": True,
        "questions": {
            "id": result.id,
            "subject_name": result.subject_name,
            "grade": result.grade,
            "questions": result.questions,
            "answers": result.answers,
            "created_at": str(result.created_at)
        }
    })


@app.route("/update_user", methods=["POST"])
def update_user_web():
    id = request.form.get("id", "")
    score = request.form.get("score", "")
    answers = request.form.get("answers", "")

    if not id or not score:
        return jsonify({"success": False, 'message': 'id and score are required'})

    result = update_candidate(id, score,answers)
    if result:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "User not found"})


@app.route("/all_users", methods=["GET"])
def all_users_route():
    return jsonify({
        "success": True,'message': all_users()
    })

if __name__ == "__main__":
    init()
    app.run(debug=True, port=8000)
