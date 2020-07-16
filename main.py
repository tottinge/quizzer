from bottle import route, run

@route('/')
def render_html(title='Magically Delicious'):
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
</head>
<body>

</body>

</html>"""

if __name__ == '__main__':
    run(debug=True)