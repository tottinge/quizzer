% rebase('skeleton.tpl', title=title)
% include('sub_progress.tpl')

<form class="w3-con" action="/quizzes/{{quiz_name}}/{{question_number}}" method="POST">
    % from random import shuffle
    % choices = [*decoys,answer]
    % shuffle(choices)

    <section class="w3-card">
        <p class="w3-panel w3-teal w3-card-4 question-asked">{{question}}</p>
        % for answer in choices:
        <div class="form-answer">
            <input type='radio' class="w3-radio" name='answer' id='{{answer}}' value='{{answer}}'/>
            <label for='{{answer}}'>
                {{answer}}
            </label>
        </div>
        % end
        <br/>
    </section>
    <br/>
    <button class="w3-btn w3-teal w3-round">Check Answer</button>
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
