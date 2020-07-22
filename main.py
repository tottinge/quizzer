from bottle import route, run, template


def render_question(question):
    title = question['title']
    questions = question['questions']
    asked = questions[0].get('question', 'nothing asked')
    answers = questions[0].get('answers', [])
    return render_html(title=title, question=asked, answers=answers)


@route('/')
def render_html(title='Magically Delicious', question="are you happy?", answers=[]):
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
<selection>
<p class='question-asked'>{question}</p>
<option>{answers[0]}</option>
</selection>
</body>

</html>"""

if __name__ == '__main__':
    run(debug=True)