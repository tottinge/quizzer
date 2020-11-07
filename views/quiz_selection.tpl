<!DOCTYPE html>
<html>

<head>
<title>{{ title }}</title>
</head>

<body>
    <h1> {{ title }} </h1>
    <form>
    % for (name, description, filename) in choices:
    <button type="button" class="quiz_button" value="{{name}}">{{ description }}</button>
    % end
    </form>
</body>

</html>
