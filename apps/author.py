"""
Endpoint/app for authoring a quiz.
We should define this RESTfully,
   quiz > list of quizzes
   quiz/<quizname>  whole quiz
   quiz/<quizname>/question list of quiz questions
   quiz/<quizname>/question/<id> the quiz question
Should support get, post, delete... which other verbs? Patch? Put?
"""
import bottle

app = bottle.Bottle()


@app.route('quiz')
def quiz_list():
    return "Quiz list"
