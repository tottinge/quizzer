<!DOCTYPE html>
<html>

<head>
<title>{{ title }}</title>
</head>

<body>
    <h1> {{ title }} </h1>
    <form>
    % for (name, description, filename) in choices:
    <a class="quiz_selection" href="/quizzes/{{name}}/0">{{ description }}</a>
    <br>
    % end
    </form>
</body>

</html>
