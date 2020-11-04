<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
</head>
<body>

<section>
<h1 class="page-title">{{title}}</h1>
</section>
<form>
    <p class='question-asked'>{{question}}</p>

    % for answer in answers:
    <div class="form-answer">
        <input type='radio' name='answer' id='{{answer}}' value='{{answer}}'/>
        <label for='{{answer}}'>
            {{answer}}
        </label>
    </div>
    % end

</form>
</body>
</html>