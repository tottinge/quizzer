<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
</head>
<body>

<section>
<h1 id="title" class="page-title">{{title}}</h1>
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
% if resources:
<section id="resources">
<h2>Additional Resources</h2>
% for (text, url) in resources:
<a href="{{ url }}" target="_blank" rel="noreferrer noopener">{{ text }}</a>
<br>
% end
</section>
% end
</body>
</html>