"""
Endpoint/app for author a quiz.
We should define this RESTfully,
   quiz > list of quizzes
   quiz/<quizname>  whole quiz
   quiz/<quizname>/question list of quiz questions
   quiz/<quizname>/question/<id> the quiz question
Should support get, post, delete... which other verbs? Patch? Put?
"""
import json
from dataclasses import asdict

import bottle
from bottle import view

from apps.author.author_controller import AuthorController
from quizzes.quiz import Quiz
from shared.quizzology import Quizzology

app = bottle.Bottle()
app.resources.add_path("./apps/author/views")
LOCAL_PATHS = ['./apps/author/views', *bottle.TEMPLATE_PATH]


@app.route('/')
@view('quiz_author_home', template_lookup=LOCAL_PATHS)
def cover_page():
    return {
        'title': 'Welcome Author'
    }


@app.route('/quiz')
def quiz_list():
    return "<h1>Quiz list</h1>"


@app.get('/edit/<quiz_name>')
@view('quiz_authoring_form', template_lookup=LOCAL_PATHS)
def edit_existing(quiz_name: str):
    # ToDo - this is no way to acquire a controller
    author_controller = AuthorController(Quizzology())
    quiz = author_controller.get_quiz(quiz_name)
    return {
        'title': 'Edit Existing Quiz',
        'quiz': quiz,
        'raw_quiz': json.dumps(asdict(quiz)),
        'schema': {}
    }


@app.get('/edit')
@view('quiz_authoring_form', template_lookup=LOCAL_PATHS)
def do_nothing_interesting():
    return {
        'quiz': Quiz(name='name', title='title'),
        'title': "Edit Quiz"
    }


@app.post('/edit')
def update_quiz_from_html_form():
    doc_field_value = bottle.request.forms.get('chaplin')
    return f"""
     <p>Document is {doc_field_value}</p>
     """
