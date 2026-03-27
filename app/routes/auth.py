from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, MCQQuestion, XPLog
import random, json

auth_bp = Blueprint("auth", __name__)


def seed_mcq_questions():
    """Seed MCQ level-test questions if not present."""
    if MCQQuestion.query.count() > 0:
        return
    questions = [
        # Easy
        {"question": "What does HTML stand for?", "options": ["HyperText Markup Language", "High Text Machine Language", "HyperTool Markup Logic", "None"], "answer": "HyperText Markup Language", "difficulty": "easy", "topic": "web"},
        {"question": "Which symbol is used for comments in Python?", "options": ["//", "#", "/*", "--"], "answer": "#", "difficulty": "easy", "topic": "python"},
        {"question": "What is the output of print(2 + 3)?", "options": ["23", "5", "Error", "None"], "answer": "5", "difficulty": "easy", "topic": "python"},
        {"question": "Which tag creates a hyperlink in HTML?", "options": ["<link>", "<a>", "<href>", "<url>"], "answer": "<a>", "difficulty": "easy", "topic": "web"},
        {"question": "What does CSS stand for?", "options": ["Cascading Style Sheets", "Creative Style Syntax", "Computer Style System", "None"], "answer": "Cascading Style Sheets", "difficulty": "easy", "topic": "web"},
        {"question": "Which data type is used for text in Python?", "options": ["int", "float", "str", "char"], "answer": "str", "difficulty": "easy", "topic": "python"},
        {"question": "What is a variable?", "options": ["A fixed value", "A storage location", "A loop", "A function"], "answer": "A storage location", "difficulty": "easy", "topic": "general"},
        # Medium
        {"question": "What is a loop used for?", "options": ["Define a function", "Repeat code", "Import a module", "Store data"], "answer": "Repeat code", "difficulty": "medium", "topic": "general"},
        {"question": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "function"], "answer": "def", "difficulty": "medium", "topic": "python"},
        {"question": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query List", "System Query Logic", "None"], "answer": "Structured Query Language", "difficulty": "medium", "topic": "database"},
        {"question": "What is the difference between == and =?", "options": ["No difference", "== assigns, = compares", "= assigns, == compares", "Both compare"], "answer": "= assigns, == compares", "difficulty": "medium", "topic": "general"},
        {"question": "Which method adds an item to a Python list?", "options": ["add()", "append()", "insert_end()", "push()"], "answer": "append()", "difficulty": "medium", "topic": "python"},
        {"question": "What is an API?", "options": ["A database", "A programming interface", "A design tool", "A type of loop"], "answer": "A programming interface", "difficulty": "medium", "topic": "general"},
        {"question": "What does git commit do?", "options": ["Upload code", "Save a snapshot", "Create a branch", "Merge changes"], "answer": "Save a snapshot", "difficulty": "medium", "topic": "tools"},
        # Hard
        {"question": "What is Big O notation?", "options": ["Algorithm memory usage", "Algorithm time complexity", "Code style guide", "Error handling"], "answer": "Algorithm time complexity", "difficulty": "hard", "topic": "cs"},
        {"question": "What is a RESTful API?", "options": ["A secure API", "An API using HTTP methods", "A database API", "A Python library"], "answer": "An API using HTTP methods", "difficulty": "hard", "topic": "web"},
        {"question": "What is recursion?", "options": ["A loop", "A function calling itself", "A data type", "An import"], "answer": "A function calling itself", "difficulty": "hard", "topic": "general"},
        {"question": "What is the purpose of a virtual environment in Python?", "options": ["Run code faster", "Isolate dependencies", "Connect to internet", "Handle errors"], "answer": "Isolate dependencies", "difficulty": "hard", "topic": "python"},
        {"question": "What does OOP stand for?", "options": ["Object-Oriented Programming", "Output Operation Protocol", "Open Object Pipeline", "None"], "answer": "Object-Oriented Programming", "difficulty": "hard", "topic": "general"},
        {"question": "What is normalization in databases?", "options": ["Speeding up queries", "Organizing data to reduce redundancy", "Encrypting data", "Backing up data"], "answer": "Organizing data to reduce redundancy", "difficulty": "hard", "topic": "database"},
    ]
    for q in questions:
        mcq = MCQQuestion(
            question=q["question"],
            options=json.dumps(q["options"]),
            answer=q["answer"],
            difficulty=q["difficulty"],
            topic=q["topic"],
        )
        db.session.add(mcq)
    db.session.commit()


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "student")

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger")
            return render_template("auth/register.html")
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return render_template("auth/register.html")

        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed, role=role)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        if role == "student":
            seed_mcq_questions()
            return redirect(url_for("auth.level_test"))
        return redirect(url_for("teacher.dashboard"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.role == "teacher":
            return redirect(url_for("teacher.dashboard"))
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == "teacher":
                return redirect(url_for("teacher.dashboard"))
            if not user.level_test_done:
                seed_mcq_questions()
                return redirect(url_for("auth.level_test"))
            return redirect(url_for("main.dashboard"))
        flash("Invalid credentials.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/level-test", methods=["GET", "POST"])
@login_required
def level_test():
    if current_user.level_test_done:
        return redirect(url_for("main.dashboard"))

    seed_mcq_questions()

    if request.method == "POST":
        questions_json = request.form.get("questions_data", "[]")
        questions_ids = json.loads(questions_json)
        questions = MCQQuestion.query.filter(MCQQuestion.id.in_(questions_ids)).all()
        questions_map = {q.id: q for q in questions}

        total = len(questions_ids)
        score = 0
        for qid in questions_ids:
            selected = request.form.get(f"q_{qid}", "")
            q = questions_map.get(qid)
            if q and selected == q.answer:
                if q.difficulty == "easy":
                    score += 1
                elif q.difficulty == "medium":
                    score += 2
                else:
                    score += 3

        max_score = sum(
            3 if questions_map[qid].difficulty == "hard"
            else 2 if questions_map[qid].difficulty == "medium"
            else 1
            for qid in questions_ids if qid in questions_map
        )
        pct = (score / max_score * 100) if max_score > 0 else 0

        if pct < 40:
            level = "beginner"
        elif pct < 70:
            level = "intermediate"
        else:
            level = "advanced"

        current_user.level = level
        current_user.level_test_done = True
        current_user.xp += 20
        db.session.add(XPLog(user_id=current_user.id, amount=20, reason="Completed level test"))
        db.session.commit()

        flash(f"Level assessment complete! You are: {level.capitalize()} 🎉", "success")
        return redirect(url_for("main.dashboard"))

    # Pick random questions: 3 easy, 3 medium, 2 hard
    easy = MCQQuestion.query.filter_by(difficulty="easy").order_by(db.func.random()).limit(3).all()
    medium = MCQQuestion.query.filter_by(difficulty="medium").order_by(db.func.random()).limit(3).all()
    hard = MCQQuestion.query.filter_by(difficulty="hard").order_by(db.func.random()).limit(2).all()
    questions = easy + medium + hard
    random.shuffle(questions)
    questions_ids = [q.id for q in questions]

    return render_template("auth/level_test.html", questions=questions, questions_ids=json.dumps(questions_ids))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("main.landing"))
