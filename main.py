from bottle import route, run

@route('/')
def render_question(question):
    title = question['title']
    questions = question['questions']
    asked = questions[0].get('question', 'nothing asked')
    answers = questions[0].get('answers', [])
    return render_html(title=title, question=asked)


def render_html(title='Magically Delicious', question="are you happy?"):
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
</selection>
</body>

</html>"""

if __name__ == '__main__':
    run(debug=True)