from bottle import route, run, template
from box import Box


def render_question(question):
    qbox = Box(question)
    return render_html(qbox.title, qbox.questions[0])


@route('/')
def poop():
    doc = {
            'title':"Magically Delicious",
            'questions':[
                { 'question':"Are you happy now?", 'answers':['Yes','No'] }
            ]
    }
    return render_question(doc)

def render_html(title, question):
    text = question.question
    answers=question.answers
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

if __name__ == '__main__':
    run(reloader=True, debug=True)
