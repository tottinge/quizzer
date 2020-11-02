from bottle import route, run, template
from box import Box
import json


def render_quiz(quiz):
    quiz = Box(quiz)
    title = quiz.title
    question = quiz.questions[0]
    print(question)
    text = question.question
    answers = question.answers
    # Thi is not good -- all hard-coded to exactly two answers. Not grand. 
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
</head>
<body>

<section>
<h1 class="page-title">{title}<h1>
</section>
<form>
<p class='question-asked'>{text}</p>
<input type='radio' name='answer', id={answers[0]}, value={answers[0]}> 
<label for={answers[0]}>{answers[0]}</label>
<input type='radio' name='answer', id={answers[1]}, value={answers[1]}> 
<label for={answers[1]}>{answers[1]}</label>
</form>
</body>
</html>"""


@route('/')
def begin_quiz():
    doc = None
    try:
        with open("quiz_doc.txt") as quiz:
            doc = json.load(quiz)
    except JSONDecodeError as err:
        print("Quiz file is invalid json")
        raise
    return render_quiz(doc)


if __name__ == '__main__':
    run(reloader=True, debug=True)
