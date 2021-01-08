<!DOCTYPE html>
<html>
<head>
    <title>{{title}}</title>
</head>
<body>

% include('session_progress.tpl')

<section>
<form action="/quizzes/{{quiz_name}}/{{question_number}}" method="POST">
    % from random import shuffle
    % choices = [*decoys,answer]
    % shuffle(choices)

    <p class='question-asked'>{{question}}</p>
    % for answer in choices:
    <div class="form-answer">
        <input type='radio' name='answer' id='{{answer}}' value='{{answer}}'/>
        <label for='{{answer}}'>
            {{answer}}
        </label>
    </div>
    % end
    <button>Check Answer</button>
    <div id="result_text">You haven't answered yet.</div>
</form>
</section>

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