<!DOCTYPE html>
<html>

<head>
<title>{{ title }}</title>
</head>

<body>
    <section>
        <img src="/favicon.ico" width="25" hspace="5" align="left" />
        <h1 id="title" class="page-title">{{title}}</h1>
    </section>
    <form>
    % for (name, description, filename) in choices:
    <a class="quiz_selection" href="/quizzes/{{name}}/0">{{ description }}</a>
    <br/>
    % end
    </form>
</body>

</html>
