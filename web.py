from flask import Flask, request, jsonify
import secrets
from flask_cors import CORS

from database import get_or_create_candidates, update_candidate, get_questions_and_answers, init, all_users, \
    delete_candidate, create_quests_and_answers

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
(CORS(app, resources={r"/*": {"origins": "*"}}))



@app.route('/')
def index():
    return jsonify({
        'success': False,
        'message': '/create_user [POST], /get_questions_and_answers [GET], /update_user [GET]'
    })


@app.route("/create_user", methods=["POST"])
def create_user():
    name = request.args.get('name','')
    surname = request.args.get("surname", "")
    subject = request.args.get("subject", "")
    grade = request.args.get("grade", "")

    if not name or not surname or not subject or not grade:
        return jsonify({"success": False, "message": "name, surname, subject, grade is required"})

    user = get_or_create_candidates(name, surname, grade, subject)

    return jsonify({"success": True, "user": user})


@app.route("/update_user", methods=["POST"])
def update_user_web():
    id = request.args.get("id")
    score = request.args.get("score")
    answers = request.args.get("answers",None)

    if not id or not score:
        return jsonify({"success": False, 'message': 'id and score are required'})

    result = update_candidate(id, score,answers)
    if result:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "User not found"})


@app.route("/all_users", methods=["GET"])
def all_users_route():
    subject_name = request.args.get('subject_name')
    users = all_users(subject_name)
    if not users:
        return jsonify({"success": False, "message": "No users found"})
    return jsonify({
        "success": True,'message': users,
    })



@app.route("/get_questions", methods=["GET"])
def get_questions_and_answers_route():
    subject_name = request.args.get('subject_name')
    grade = request.args.get('grade')
    if not subject_name or not grade:
        return jsonify({"success": False, 'message': 'subject and grade are required'})
    subject_questions = get_questions_and_answers(subject_name,grade)
    return jsonify({"message": subject_questions, "success": True})


@app.route("/create_questions", methods=["POST"])
def create_questions_and_answers_route():
    subject_name = request.args.get('subject_name')
    grade = request.args.get('grade')
    questions = request.args.get('questions')
    if not subject_name or not grade or not questions:
        return jsonify({"success": False, 'message': 'subject and grade are required'})
    result = create_quests_and_answers(subject_name,grade,questions)
    if result:
        return jsonify({"success": True})


@app.route("/delete_user", methods=["POST"])
def delete_user():
    candidate_id = request.args.get("candidate_id")
    result = delete_candidate(candidate_id)
    if result:
        return jsonify({
            "success": True,'message': result
        })
    return jsonify({"success": False})


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0")