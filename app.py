from flask import Flask, request, render_template, redirect, flash, jsonify, session 
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
title = satisfaction_survey.title
instructions = satisfaction_survey.instructions
questions = {}
index = 0
for x in satisfaction_survey.questions:
    questions[index] =  {"question": x.question,
                         "choices": x.choices,
                         "allow_text": x.allow_text
                         }
    index += 1
    

@app.route("/")
def home_page():
    """show questionaire start page"""
    responses = []
    print("RESPONSES => ",responses)
    return render_template("home.html", title=title,instructions=instructions,questions=questions)

@app.route("/questions", methods=["POST"])
def do_questions():
    """show next question"""
    res = request.form["choice"]
    print("RES ", res)
    print("RESPONSES ", responses)
    if res != "choice":
        responses.append(res)
    if len(responses) == index:
        return render_template("/results.html", questions= questions, responses=responses)
    
    return render_template("questions.html", title=title,instructions=instructions,questions=questions, questions_index=len(responses))

@app.errorhandler(404)
def not_found(e):
    flash("You’re trying to access an invalid question.")
    return redirect("/")