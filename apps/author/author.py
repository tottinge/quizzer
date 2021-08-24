"""
Endpoint/app for author a quiz.
We should define this RESTfully,
   quiz > list of quizzes
   quiz/<quizname>  whole quiz
   quiz/<quizname>/question list of quiz questions
   quiz/<quizname>/question/<id> the quiz question
Should support get, post, delete... which other verbs? Patch? Put?
"""
import bottle
from bottle import view

from quizzes.quiz import Quiz

app = bottle.Bottle()
app.resources.add_path("./apps/author/views")


@app.route('/quiz')
def quiz_list():
    return "<h1>Quiz list</h1>"


LOCAL_PATHS = ['./apps/author/views', *bottle.TEMPLATE_PATH]


@app.get('/edit')
@view('quiz_authoring_form', template_lookup=LOCAL_PATHS)
def do_nothing_interesting():
    return {
        'quiz': Quiz(name='name', title='title'),
        'title': "Edit Quiz"
    }


@app.post('/edit')
def just_looking_move_along():
    return {}
